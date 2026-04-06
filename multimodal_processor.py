"""
multimodal_processor.py
-----------------------
Multimodal extension for the Educational RAG system.

Provides:
  - CLIPEmbedder       — CLIP-based image/text encoder (openai/clip-vit-base-patch32)
  - ImageCaptioner     — BLIP-based image captioner (Salesforce/blip-image-captioning-base)
  - ImageFAISSIndex    — FAISS inner-product index for fast image similarity search
  - ImageRecord        — Metadata container for an indexed image (no embedding stored)
  - extract_images_from_pdf()    — Extract images from a PDF file
  - build_image_index()          — Ingest PDFs → CLIP embed → FAISS index
  - load_or_build_image_index()  — Load persisted index or build from scratch
  - fuse_multimodal_context()    — Merge text chunks + image captions into one context string

Design notes:
  - All heavy model loading is lazy and guarded by availability flags so the
    rest of the system degrades gracefully when optional packages are absent.
  - CLIP text-encoder is also exposed so that a plain text query can search the
    image index (shared embedding space).
  - Image embeddings are L2-normalised before insertion; FAISS IndexFlatIP
    (inner product) then gives cosine similarity directly.
  - Embeddings are stored only inside FAISS (not duplicated on ImageRecord) to
    keep memory and disk usage lean as the image corpus grows.
  - Metadata is persisted as JSON (not pickle) so the sidecar file is
    human-readable and safe to load without code-execution risks.
"""

from __future__ import annotations

import io
import json
import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

import numpy as np

if TYPE_CHECKING:
    from langchain_core.documents import Document

# ── Optional heavy dependencies ───────────────────────────────────────────────

_TRANSFORMERS_AVAILABLE = False
try:
    import torch
    from transformers import (  # type: ignore[import]
        CLIPModel,
        CLIPProcessor,
        BlipForConditionalGeneration,
        BlipProcessor,
    )
    _TRANSFORMERS_AVAILABLE = True
except ImportError:
    pass

_PIL_AVAILABLE = False
try:
    from PIL import Image as _PILImage  # type: ignore[import]
    _PIL_AVAILABLE = True
except ImportError:
    pass

_FAISS_AVAILABLE = False
try:
    import faiss  # type: ignore[import]
    _FAISS_AVAILABLE = True
except ImportError:
    pass

_PYPDF_AVAILABLE = False
try:
    import pypdf  # type: ignore[import]
    _PYPDF_AVAILABLE = True
except ImportError:
    pass

# ── Model identifiers ─────────────────────────────────────────────────────────

CLIP_MODEL_ID = "openai/clip-vit-base-patch32"
BLIP_MODEL_ID = "Salesforce/blip-image-captioning-base"

# ── Default index paths ───────────────────────────────────────────────────────

DEFAULT_INDEX_PATH = "image_index.faiss"
DEFAULT_META_PATH = "image_meta.json"

# Embedding dimension for openai/clip-vit-base-patch32
CLIP_DIM = 512


# ── Data class ────────────────────────────────────────────────────────────────

@dataclass
class ImageRecord:
    """Metadata for a single indexed image.

    Note: embeddings are intentionally *not* stored here; they live only inside
    the FAISS index.  Storing them again in Python would double memory/disk usage
    for large corpora without any benefit — the index handles all similarity math.
    """

    image_id: str
    source: str       # e.g. PDF filename or "upload"
    page: int         # 1-based page number (0 for uploads)
    caption: str = ""


# ── CLIP embedder ─────────────────────────────────────────────────────────────

class CLIPEmbedder:
    """
    Wrapper around openai/clip-vit-base-patch32 for image and text embeddings.

    Both image and text embeddings are L2-normalised so that inner-product
    similarity equals cosine similarity.
    """

    def __init__(self, model_id: str = CLIP_MODEL_ID) -> None:
        if not _TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "transformers and torch are required for CLIP embeddings. "
                "Install with: pip install transformers torch"
            )
        if not _PIL_AVAILABLE:
            raise ImportError(
                "Pillow is required for image processing. "
                "Install with: pip install Pillow"
            )
        print(f"  [CLIP] Loading model: {model_id}")
        self._processor: CLIPProcessor = CLIPProcessor.from_pretrained(model_id)
        self._model: CLIPModel = CLIPModel.from_pretrained(model_id)
        self._model.eval()

    def embed_image(self, image: "_PILImage.Image") -> list[float]:
        """
        Encode a PIL Image into a normalised CLIP embedding vector.

        Args:
            image: RGB PIL Image.

        Returns:
            List of floats (length CLIP_DIM=512), L2-normalised.
        """
        inputs = self._processor(images=image, return_tensors="pt")
        with torch.no_grad():
            features = self._model.get_image_features(**inputs)
            features = features / features.norm(dim=-1, keepdim=True)
        return features[0].tolist()

    def embed_text(self, text: str) -> list[float]:
        """
        Encode a text string into the CLIP text embedding space.

        Allows text queries to search the image index directly.

        Args:
            text: Query string.

        Returns:
            List of floats (length CLIP_DIM=512), L2-normalised.
        """
        inputs = self._processor(
            text=[text], return_tensors="pt", padding=True, truncation=True
        )
        with torch.no_grad():
            features = self._model.get_text_features(**inputs)
            features = features / features.norm(dim=-1, keepdim=True)
        return features[0].tolist()


# ── BLIP image captioner ──────────────────────────────────────────────────────

class ImageCaptioner:
    """
    BLIP-based image captioner that converts images to natural-language descriptions.

    The generated captions are embedded as regular text and stored alongside the
    image embeddings so they can be included in the SLM context.
    """

    def __init__(self, model_id: str = BLIP_MODEL_ID) -> None:
        if not _TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "transformers and torch are required for BLIP captioning. "
                "Install with: pip install transformers torch"
            )
        if not _PIL_AVAILABLE:
            raise ImportError(
                "Pillow is required for image processing. "
                "Install with: pip install Pillow"
            )
        print(f"  [BLIP] Loading captioner: {model_id}")
        self._processor: BlipProcessor = BlipProcessor.from_pretrained(model_id)
        self._model: BlipForConditionalGeneration = (
            BlipForConditionalGeneration.from_pretrained(model_id)
        )
        self._model.eval()

    def caption(self, image: "_PILImage.Image", max_new_tokens: int = 60) -> str:
        """
        Generate a text caption for a PIL Image.

        Args:
            image:          RGB PIL Image.
            max_new_tokens: Maximum number of tokens to generate.

        Returns:
            Caption string.
        """
        inputs = self._processor(image, return_tensors="pt")
        with torch.no_grad():
            out = self._model.generate(**inputs, max_new_tokens=max_new_tokens)
        return self._processor.decode(out[0], skip_special_tokens=True)


# ── FAISS image index ─────────────────────────────────────────────────────────

class ImageFAISSIndex:
    """
    FAISS inner-product index for fast image embedding similarity search.

    Since embeddings are L2-normalised, inner-product equals cosine similarity.
    Index is persisted to disk as a ``.faiss`` binary file + a JSON metadata sidecar.
    """

    def __init__(self, dim: int = CLIP_DIM) -> None:
        if not _FAISS_AVAILABLE:
            raise ImportError(
                "faiss-cpu is required for image indexing. "
                "Install with: pip install faiss-cpu"
            )
        self._dim = dim
        self._index = faiss.IndexFlatIP(dim)
        self._records: list[ImageRecord] = []

    # ── Mutation ──────────────────────────────────────────────────────────────

    def add(self, record: ImageRecord, embedding: list[float]) -> None:
        """
        Add an ImageRecord to the index.

        The embedding is inserted into FAISS and is *not* stored on the record
        itself — keeping metadata lean and avoiding duplication.

        Args:
            record:    ImageRecord with id/source/page/caption fields populated.
            embedding: Pre-computed, L2-normalised CLIP embedding for this image.
        """
        vec = np.array(embedding, dtype=np.float32).reshape(1, -1)
        self._index.add(vec)
        self._records.append(record)

    # ── Search ────────────────────────────────────────────────────────────────

    def search(
        self, query_vec: list[float], k: int = 5
    ) -> list[tuple[ImageRecord, float]]:
        """
        Return the top-*k* most similar ImageRecords.

        Args:
            query_vec: L2-normalised query vector (CLIP image or text embedding).
            k:         Maximum number of results.

        Returns:
            List of (ImageRecord, cosine_similarity_score) sorted by descending score.
        """
        if self._index.ntotal == 0:
            return []
        q = np.array(query_vec, dtype=np.float32).reshape(1, -1)
        k = min(k, self._index.ntotal)
        scores, indices = self._index.search(q, k)
        return [
            (self._records[i], float(scores[0][j]))
            for j, i in enumerate(indices[0])
            if i >= 0
        ]

    # ── Persistence ───────────────────────────────────────────────────────────

    def save(
        self,
        index_path: str = DEFAULT_INDEX_PATH,
        meta_path: str = DEFAULT_META_PATH,
    ) -> None:
        """Persist the FAISS index and metadata to disk.

        The FAISS index is written as a binary ``.faiss`` file.  Metadata
        (id, source, page, caption — no embeddings) is written as JSON so the
        sidecar is human-readable and safe to load without trust concerns.
        """
        faiss.write_index(self._index, index_path)
        records_data = [
            {
                "image_id": r.image_id,
                "source": r.source,
                "page": r.page,
                "caption": r.caption,
            }
            for r in self._records
        ]
        with open(meta_path, "w", encoding="utf-8") as fh:
            json.dump(records_data, fh, ensure_ascii=False, indent=2)

    @classmethod
    def load(
        cls,
        index_path: str = DEFAULT_INDEX_PATH,
        meta_path: str = DEFAULT_META_PATH,
    ) -> "ImageFAISSIndex":
        """
        Load a previously saved index from disk.

        Metadata is read from a JSON sidecar (safe — no code execution).

        Args:
            index_path: Path to the ``.faiss`` file.
            meta_path:  Path to the JSON metadata file.

        Returns:
            Populated ImageFAISSIndex.
        """
        if not _FAISS_AVAILABLE:
            raise ImportError(
                "faiss-cpu is required for image indexing. "
                "Install with: pip install faiss-cpu"
            )
        obj: ImageFAISSIndex = cls.__new__(cls)
        obj._index = faiss.read_index(index_path)
        obj._dim = obj._index.d
        with open(meta_path, "r", encoding="utf-8") as fh:
            records_data = json.load(fh)
        obj._records = [
            ImageRecord(
                image_id=r["image_id"],
                source=r["source"],
                page=r["page"],
                caption=r.get("caption", ""),
            )
            for r in records_data
        ]
        return obj

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def count(self) -> int:
        """Number of images currently in the index."""
        return int(self._index.ntotal)


# ── PDF image extraction ──────────────────────────────────────────────────────

def extract_images_from_pdf(
    pdf_path: str,
) -> list[tuple[int, "_PILImage.Image"]]:
    """
    Extract all embedded images from a PDF file.

    Args:
        pdf_path: Absolute path to the PDF file.

    Returns:
        List of (page_number, PIL.Image) tuples (page numbers are 1-based).

    Raises:
        ImportError: If pypdf or Pillow are not installed.
        FileNotFoundError: If the PDF does not exist.
    """
    if not _PYPDF_AVAILABLE:
        raise ImportError(
            "pypdf is required for PDF image extraction. "
            "Install with: pip install pypdf"
        )
    if not _PIL_AVAILABLE:
        raise ImportError(
            "Pillow is required for image processing. "
            "Install with: pip install Pillow"
        )
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    results: list[tuple[int, "_PILImage.Image"]] = []
    reader = pypdf.PdfReader(pdf_path)
    for page_num, page in enumerate(reader.pages, start=1):
        for img_obj in page.images:
            try:
                img = _PILImage.open(io.BytesIO(img_obj.data)).convert("RGB")
                results.append((page_num, img))
            except Exception:
                # Skip unreadable or corrupt image objects
                continue
    return results


# ── Index builder ─────────────────────────────────────────────────────────────

def build_image_index(
    pdf_paths: list[str],
    index_path: str = DEFAULT_INDEX_PATH,
    meta_path: str = DEFAULT_META_PATH,
    with_captions: bool = True,
) -> ImageFAISSIndex:
    """
    Build a FAISS image index by ingesting images from a list of PDF files.

    For each image found:
      1. Generate a CLIP embedding.
      2. Optionally generate a BLIP caption.
      3. Store as an ImageRecord in the FAISS index.

    The resulting index is saved to disk at *index_path* / *meta_path*.

    Args:
        pdf_paths:    List of PDF file paths to process.
        index_path:   Output path for the FAISS index file.
        meta_path:    Output path for the JSON metadata sidecar.
        with_captions: Whether to generate BLIP captions (requires extra RAM).

    Returns:
        Populated and persisted ImageFAISSIndex.
    """
    embedder = CLIPEmbedder()
    captioner = ImageCaptioner() if with_captions else None
    idx = ImageFAISSIndex(dim=CLIP_DIM)

    for pdf_path in pdf_paths:
        print(f"  [ImageIndex] Processing: {pdf_path}")
        try:
            images = extract_images_from_pdf(pdf_path)
        except (ImportError, FileNotFoundError) as exc:
            print(f"  [ImageIndex] Skipping {pdf_path}: {exc}")
            continue

        for img_num, (page_num, img) in enumerate(images):
            # Use a per-PDF image counter (img_num) so that image_id is stable
            # and deterministic regardless of the order images are added to the
            # global index.
            image_id = f"{os.path.basename(pdf_path)}_p{page_num}_i{img_num}"
            embedding = embedder.embed_image(img)
            caption = captioner.caption(img) if captioner else ""
            record = ImageRecord(
                image_id=image_id,
                source=pdf_path,
                page=page_num,
                caption=caption,
            )
            idx.add(record, embedding)
            preview = caption[:60] if caption else "(no caption)"
            print(f"    + {image_id}: '{preview}…'")

    idx.save(index_path, meta_path)
    print(f"  [ImageIndex] Saved {idx.count} image(s) to {index_path}")
    return idx


def load_or_build_image_index(
    pdf_paths: Optional[list[str]] = None,
    index_path: str = DEFAULT_INDEX_PATH,
    meta_path: str = DEFAULT_META_PATH,
) -> Optional[ImageFAISSIndex]:
    """
    Load an existing image index from disk, or build one from PDFs if provided.

    Returns ``None`` when faiss-cpu is not installed or when neither an existing
    index nor any PDF paths are available — allowing the rest of the pipeline to
    operate in text-only mode transparently.

    Args:
        pdf_paths:  PDF files to ingest when building a fresh index.
        index_path: Path to the FAISS index file.
        meta_path:  Path to the JSON metadata sidecar.

    Returns:
        ImageFAISSIndex, or None if unavailable.
    """
    if not _FAISS_AVAILABLE:
        print("  [ImageIndex] faiss-cpu not installed; skipping image index.")
        return None

    if os.path.isfile(index_path) and os.path.isfile(meta_path):
        print("  [ImageIndex] Loading existing image index from disk…")
        return ImageFAISSIndex.load(index_path, meta_path)

    if pdf_paths:
        print("  [ImageIndex] Building image index from PDFs…")
        return build_image_index(pdf_paths, index_path, meta_path)

    print("  [ImageIndex] No index on disk and no PDFs provided; image retrieval disabled.")
    return None


# ── Context fusion ────────────────────────────────────────────────────────────

def fuse_multimodal_context(
    text_docs: list["Document"],
    image_hits: list[tuple[ImageRecord, float]],
) -> str:
    """
    Merge retrieved text chunks and image captions into a single context string
    for the SLM prompt.

    Text chunks are included verbatim.  Image records contribute their captions
    (if available) labelled with their source and page number.

    Args:
        text_docs:  Retrieved LangChain Document objects (text context).
        image_hits: List of (ImageRecord, similarity_score) from the image index.

    Returns:
        Unified context string ready to be inserted into the SLM prompt.
    """
    parts: list[str] = []

    if text_docs:
        parts.append("=== Text Context ===")
        for doc in text_docs:
            parts.append(doc.page_content)

    caption_parts: list[str] = [
        f"[Image — {rec.source}, page {rec.page}]: {rec.caption}"
        for rec, _ in image_hits
        if rec.caption
    ]
    if caption_parts:
        parts.append("=== Visual Context (from diagrams/images) ===")
        parts.extend(caption_parts)

    return "\n\n".join(parts)


# ── Availability helpers ──────────────────────────────────────────────────────

def multimodal_available() -> bool:
    """Return True when all optional multimodal dependencies are installed."""
    return _TRANSFORMERS_AVAILABLE and _PIL_AVAILABLE and _FAISS_AVAILABLE


def get_missing_dependencies() -> list[str]:
    """Return a list of missing optional dependency names."""
    missing: list[str] = []
    if not _TRANSFORMERS_AVAILABLE:
        missing.append("transformers / torch")
    if not _PIL_AVAILABLE:
        missing.append("Pillow")
    if not _FAISS_AVAILABLE:
        missing.append("faiss-cpu")
    if not _PYPDF_AVAILABLE:
        missing.append("pypdf (PDF ingestion only)")
    return missing
