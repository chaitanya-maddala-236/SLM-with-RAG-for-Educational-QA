"""
multimodal_processor.py
-----------------------
Multimodal extension for the Educational RAG system.

Provides:
  - CLIPEmbedder       — multimodal image/text encoder (CLIP / SigLIP / OpenCLIP)
  - ImageCaptioner     — BLIP-based image captioner (Salesforce/blip-image-captioning-base)
  - VisionImageAnalyzer — Vision LLM-based image analyzer (Groq vision → Ollama LLaVA → BLIP)
  - ImageFAISSIndex    — FAISS inner-product index for fast image similarity search
  - ImageRecord        — Metadata container for an indexed image (no embedding stored)
  - extract_images_from_pdf()    — Extract images from a PDF file
  - build_image_index()          — Ingest PDFs → CLIP embed → FAISS index
  - load_or_build_image_index()  — Load persisted index or build from scratch
  - fuse_multimodal_context()    — Merge text chunks + image captions into one context string

Design notes:
  - All heavy model loading is lazy and guarded by availability flags so the
    rest of the system degrades gracefully when optional packages are absent.
  - VisionImageAnalyzer provides a three-tier fallback for image understanding:
      1. Groq vision API (llama-3.2-11b-vision-preview) — best quality, requires GROQ_API_KEY
      2. Ollama LLaVA (any llava/bakllava model) — local, no API key needed
      3. BLIP captioner — basic caption when no vision LLM is available
    The analyzer generates a rich educational description that includes all visible
    text, labels, formulas, and diagram components — far beyond a generic caption.
  - Multimodal text-encoder is exposed so that a plain text query can search the
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
        AutoModel,
        AutoProcessor,
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

_GROQ_AVAILABLE = False
try:
    from langchain_groq import ChatGroq as _ChatGroq  # type: ignore[import]
    from langchain_core.messages import HumanMessage as _HumanMessage  # type: ignore[import]
    _GROQ_AVAILABLE = True
except ImportError:
    pass

_OLLAMA_AVAILABLE = False
try:
    import ollama as _ollama  # type: ignore[import]
    _OLLAMA_AVAILABLE = True
except ImportError:
    pass

# ── Model identifiers ─────────────────────────────────────────────────────────

CLIP_MODEL_ID = "openai/clip-vit-base-patch32"
BLIP_MODEL_ID = "Salesforce/blip-image-captioning-base"
# Vision LLM model IDs — used by VisionImageAnalyzer
GROQ_VISION_MODEL_ID = "llama-3.2-11b-vision-preview"
OLLAMA_VISION_MODEL_CANDIDATES = ["llava", "llava:7b", "llava:13b", "bakllava", "llava-phi3", "llama3.2-vision"]

# ── Default index paths ───────────────────────────────────────────────────────

DEFAULT_INDEX_PATH = "image_index.faiss"
DEFAULT_META_PATH = "image_meta.json"

# Multimodal embedding backbones.
# Keys can be selected via MULTIMODAL_EMBEDDING_MODEL env var.
MULTIMODAL_EMBEDDING_REGISTRY = {
    "clip": {
        "model_id": "openai/clip-vit-base-patch32",
        "family": "clip",
        "dimension": 512,
    },
    "siglip": {
        "model_id": "google/siglip-base-patch16-224",
        "family": "siglip",
        "dimension": 768,
    },
    "openclip": {
        "model_id": "laion/CLIP-ViT-B-32-laion2B-s34B-b79K",
        "family": "clip",
        "dimension": 512,
    },
}

DEFAULT_MULTIMODAL_EMBEDDING_NAME = os.environ.get(
    "MULTIMODAL_EMBEDDING_MODEL", "clip"
).strip().lower() or "clip"

# Embedding dimension fallback for legacy callers
CLIP_DIM = int(
    MULTIMODAL_EMBEDDING_REGISTRY.get(
        DEFAULT_MULTIMODAL_EMBEDDING_NAME,
        MULTIMODAL_EMBEDDING_REGISTRY["clip"],
    )["dimension"]
)

# ── API key validation helper ─────────────────────────────────────────────────

_API_KEY_PLACEHOLDER_MARKERS = ("replace_with", "your_", "example", "placeholder")


def _is_api_key_placeholder(key: str) -> bool:
    """Return True if *key* looks like an unfilled placeholder value.

    Centralises the placeholder check used by both ``VisionImageAnalyzer``
    and ``vision_llm_available()`` so the marker list stays in one place.
    """
    lower = key.lower()
    return any(marker in lower for marker in _API_KEY_PLACEHOLDER_MARKERS)


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
        selected_name = DEFAULT_MULTIMODAL_EMBEDDING_NAME
        self._selected_name = selected_name
        cfg = MULTIMODAL_EMBEDDING_REGISTRY.get(selected_name)
        if cfg:
            model_id = cfg["model_id"]
            self._family = cfg["family"]
        else:
            self._family = "clip"

        print(f"  [MM Embedding] Loading model: {model_id} (family={self._family})")
        if self._family == "siglip":
            self._processor = AutoProcessor.from_pretrained(model_id)
            self._model = AutoModel.from_pretrained(model_id)
        else:
            self._processor = CLIPProcessor.from_pretrained(model_id)
            self._model = CLIPModel.from_pretrained(model_id)
        self._model.eval()
        self._dim = self._infer_dimension()

    @property
    def dimension(self) -> int:
        """Embedding dimensionality of the active multimodal model."""
        return self._dim

    def _infer_dimension(self) -> int:
        """Infer embedding dimensionality from config metadata with safe fallback."""
        cfg = MULTIMODAL_EMBEDDING_REGISTRY.get(self._selected_name)
        if cfg:
            return int(cfg["dimension"])
        if not _PIL_AVAILABLE:
            print(
                "  [MM Embedding] Warning: Pillow unavailable and embedding config "
                "not found; falling back to default CLIP dimension."
            )
            return CLIP_DIM
        try:
            sample = _PILImage.new("RGB", (32, 32), color=(255, 255, 255))
            vec = self.embed_image(sample)
            return int(len(vec))
        except Exception:
            cfg = MULTIMODAL_EMBEDDING_REGISTRY.get(DEFAULT_MULTIMODAL_EMBEDDING_NAME)
            if cfg:
                return int(cfg["dimension"])
            return CLIP_DIM

    def _normalize(self, tensor):
        return tensor / tensor.norm(dim=-1, keepdim=True)

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
            if hasattr(self._model, "get_image_features"):
                features = self._model.get_image_features(**inputs)
            else:
                out = self._model(**inputs)
                features = getattr(out, "image_embeds", None)
                if features is None:
                    features = getattr(out, "pooler_output", None)
                if features is None:
                    raise RuntimeError("Unable to extract image features from model output.")
            features = self._normalize(features)
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
            if hasattr(self._model, "get_text_features"):
                features = self._model.get_text_features(**inputs)
            else:
                out = self._model(**inputs)
                features = getattr(out, "text_embeds", None)
                if features is None:
                    features = getattr(out, "pooler_output", None)
                if features is None:
                    raise RuntimeError("Unable to extract text features from model output.")
            features = self._normalize(features)
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


# ── Vision LLM image analyzer ────────────────────────────────────────────────

class VisionImageAnalyzer:
    """
    Vision LLM-based image analyzer for educational content.

    Generates a rich, structured educational description of an uploaded image by
    actually reading its contents — text labels, formulas, diagram components,
    arrows, values — rather than just generating a generic caption.

    Fallback chain (highest quality first):
      1. Groq vision API  — ``llama-3.2-11b-vision-preview`` (requires GROQ_API_KEY)
      2. Ollama LLaVA     — any locally-pulled llava/bakllava model (no API key)
      3. BLIP captioner   — short generic caption when no vision LLM is available

    Usage::

        analyzer = VisionImageAnalyzer()
        description = analyzer.analyze(image_bytes, question="What does the diagram show?")
    """

    # Prompt sent to the vision LLM together with the image.
    # The {question} placeholder is filled with the user's actual query so the
    # model focuses its analysis on answering the specific question.
    _EDUCATIONAL_ANALYSIS_PROMPT = (
        "You are an educational AI assistant. Carefully examine this image and provide "
        "a detailed educational analysis.\n\n"
        "Include ALL of the following:\n"
        "1. **Type**: What kind of image this is (diagram, chart, flowchart, equation, "
        "photograph, graph, table, etc.)\n"
        "2. **Visible text**: Every label, heading, annotation, number, formula, "
        "or unit visible in the image — transcribe them exactly.\n"
        "3. **Concept**: What educational topic or scientific concept this illustrates.\n"
        "4. **Structure**: Key components, steps, relationships, arrows, or processes shown.\n"
        "5. **Answer**: {question}\n\n"
        "Be thorough and precise — a student needs to understand this image completely "
        "from your description alone."
    )

    def __init__(self) -> None:
        self._groq_ready: bool = False
        self._ollama_model: str | None = None
        self._blip_ready: bool = _TRANSFORMERS_AVAILABLE and _PIL_AVAILABLE
        self._blip_captioner: Optional["ImageCaptioner"] = None

        self._try_init_groq()
        if not self._groq_ready:
            self._try_init_ollama_llava()

    # ── Initialisation helpers ────────────────────────────────────────────────

    def _try_init_groq(self) -> None:
        """Check whether a non-placeholder GROQ_API_KEY is set."""
        if not _GROQ_AVAILABLE:
            return
        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key or _is_api_key_placeholder(api_key):
            return
        self._groq_api_key = api_key
        self._groq_ready = True
        print(f"  [VisionAnalyzer] Groq vision ready ({GROQ_VISION_MODEL_ID})")

    def _try_init_ollama_llava(self) -> None:
        """Auto-detect any locally-pulled LLaVA-family model via Ollama."""
        if not _OLLAMA_AVAILABLE:
            return
        try:
            models_resp = _ollama.list()
            pulled = [
                m.get("name", m.get("model", ""))
                for m in models_resp.get("models", [])
            ]
            for candidate in OLLAMA_VISION_MODEL_CANDIDATES:
                if any(candidate in p for p in pulled):
                    self._ollama_model = candidate
                    print(f"  [VisionAnalyzer] Ollama LLaVA ready ({candidate})")
                    return
        except Exception as exc:
            print(f"  [VisionAnalyzer] Ollama probe failed: {exc}")

    # ── Public API ────────────────────────────────────────────────────────────

    def analyze(self, image_bytes: bytes, question: str = "") -> str:
        """
        Analyze an image and return a detailed educational description.

        The description includes all visible text, labels, diagram components,
        and a direct answer to *question* when provided.

        Args:
            image_bytes: Raw image bytes (PNG/JPEG/WebP).
            question:    The user's educational question about the image.

        Returns:
            Multi-paragraph educational analysis string.
        """
        prompt = self._EDUCATIONAL_ANALYSIS_PROMPT.format(
            question=question if question.strip()
            else "Describe all educational content visible in this image in detail."
        )

        if self._groq_ready:
            result = self._analyze_groq(image_bytes, prompt)
            if result:
                return result

        if self._ollama_model:
            result = self._analyze_ollama(image_bytes, prompt)
            if result:
                return result

        if self._blip_ready:
            return self._analyze_blip(image_bytes)

        return (
            "Image analysis unavailable — install a vision LLM "
            "(set GROQ_API_KEY or run `ollama pull llava`) for full image understanding."
        )

    @property
    def available(self) -> bool:
        """Return True if any vision capability is available."""
        return self._groq_ready or (self._ollama_model is not None) or self._blip_ready

    @property
    def is_vision_llm(self) -> bool:
        """Return True when a real vision LLM (Groq or Ollama LLaVA) is active.

        Distinguishes the true vision-LLM path from the BLIP-only fallback so
        callers can decide which prompt template to use without inspecting the
        ``method`` string.
        """
        return self._groq_ready or (self._ollama_model is not None)

    @property
    def method(self) -> str:
        """Return a short description of the active vision backend."""
        if self._groq_ready:
            return f"Groq ({GROQ_VISION_MODEL_ID})"
        if self._ollama_model:
            return f"Ollama ({self._ollama_model})"
        if self._blip_ready:
            return "BLIP (caption only — no vision LLM available)"
        return "none"

    # ── Backend implementations ───────────────────────────────────────────────

    def _analyze_groq(self, image_bytes: bytes, prompt: str) -> Optional[str]:
        """Send image + prompt to Groq vision API and return the analysis."""
        try:
            import base64
            img_b64 = base64.b64encode(image_bytes).decode("utf-8")
            # Detect image format from magic bytes:
            #   PNG  → \x89PNG
            #   WebP → RIFF????WEBP
            #   JPEG → \xff\xd8 (default fallback)
            if image_bytes[:4] == b"\x89PNG":
                img_fmt = "png"
            elif len(image_bytes) >= 12 and image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
                img_fmt = "webp"
            else:
                img_fmt = "jpeg"

            llm = _ChatGroq(
                model=GROQ_VISION_MODEL_ID,
                api_key=self._groq_api_key,
                temperature=0.1,
            )
            msg = _HumanMessage(content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/{img_fmt};base64,{img_b64}"},
                },
            ])
            response = llm.invoke([msg])
            text = response.content if hasattr(response, "content") else str(response)
            result = str(text).strip()
            if result:
                print("  [VisionAnalyzer] Groq vision analysis complete")
                return result
        except Exception as exc:
            print(f"  [VisionAnalyzer] Groq vision error: {exc}")
        return None

    def _analyze_ollama(self, image_bytes: bytes, prompt: str) -> Optional[str]:
        """Send image + prompt to Ollama LLaVA and return the analysis."""
        try:
            import base64
            img_b64 = base64.b64encode(image_bytes).decode("utf-8")
            response = _ollama.chat(
                model=self._ollama_model,
                messages=[{
                    "role": "user",
                    "content": prompt,
                    "images": [img_b64],
                }],
            )
            text = ""
            if isinstance(response, dict):
                text = response.get("message", {}).get("content", "")
            elif hasattr(response, "message"):
                msg = response.message
                text = msg.content if hasattr(msg, "content") else str(msg)
            result = str(text).strip()
            if result:
                print(f"  [VisionAnalyzer] Ollama ({self._ollama_model}) analysis complete")
                return result
        except Exception as exc:
            print(f"  [VisionAnalyzer] Ollama LLaVA error: {exc}")
        return None

    def _analyze_blip(self, image_bytes: bytes) -> str:
        """Generate a BLIP caption as the last-resort fallback."""
        try:
            if self._blip_captioner is None:
                self._blip_captioner = ImageCaptioner()
            pil_img = _PILImage.open(io.BytesIO(image_bytes)).convert("RGB")
            caption = self._blip_captioner.caption(pil_img, max_new_tokens=120)
            print("  [VisionAnalyzer] BLIP fallback caption generated")
            return (
                f"[Auto-generated image description — upgrade to a vision LLM for better results]\n"
                f"{caption}"
            )
        except Exception as exc:
            print(f"  [VisionAnalyzer] BLIP fallback error: {exc}")
            return "Could not analyze the image."


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
    idx = ImageFAISSIndex(dim=embedder.dimension)

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
    """Return True when uploaded-image multimodal flow is available.

    Multimodal input is available when at least one image-understanding path
    is possible:
      - Groq vision API (just needs langchain-groq + GROQ_API_KEY)
      - Ollama LLaVA    (just needs ollama + a pulled llava model)
      - PIL + transformers (BLIP fallback)
    """
    if _GROQ_AVAILABLE and _PIL_AVAILABLE:
        # Can analyse with Groq even without torch/transformers
        return True
    if _OLLAMA_AVAILABLE and _PIL_AVAILABLE:
        return True
    return _TRANSFORMERS_AVAILABLE and _PIL_AVAILABLE


def image_index_available() -> bool:
    """Return True when FAISS-backed image indexing/search is available."""
    return _TRANSFORMERS_AVAILABLE and _PIL_AVAILABLE and _FAISS_AVAILABLE


def vision_llm_available() -> bool:
    """Return True when a proper vision LLM (Groq or Ollama LLaVA) is accessible.

    Distinguishes true vision-LLM capability from BLIP-only fallback.
    """
    if _GROQ_AVAILABLE:
        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if api_key and not _is_api_key_placeholder(api_key):
            return True
    if _OLLAMA_AVAILABLE:
        try:
            models_resp = _ollama.list()
            pulled = [
                m.get("name", m.get("model", ""))
                for m in models_resp.get("models", [])
            ]
            if any(
                c in p
                for c in OLLAMA_VISION_MODEL_CANDIDATES
                for p in pulled
            ):
                return True
        except Exception:
            pass
    return False


def get_missing_dependencies() -> list[str]:
    """Return a list of missing optional dependency names."""
    missing: list[str] = []
    if not _PIL_AVAILABLE:
        missing.append("Pillow")
    if not _TRANSFORMERS_AVAILABLE:
        missing.append("transformers / torch (BLIP captioner)")
    if not _GROQ_AVAILABLE:
        missing.append("langchain-groq (Groq vision API)")
    if not _OLLAMA_AVAILABLE:
        missing.append("ollama (local LLaVA vision)")
    if not _FAISS_AVAILABLE:
        missing.append("faiss-cpu (image index retrieval)")
    if not _PYPDF_AVAILABLE:
        missing.append("pypdf (PDF image extraction)")
    return missing
