"""
Generate evaluation graphs from research_evaluator result files.

Usage examples:
    python evaluation_graphs/generate_evaluation_graphs.py
    python evaluation_graphs/generate_evaluation_graphs.py --input model_comparison_results.txt
    python evaluation_graphs/generate_evaluation_graphs.py --output-dir evaluation_graphs/output
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research_config import (
    ABLATION_RESULTS_FILE,
    EMBEDDING_COMPARISON_FILE,
    FULL_MATRIX_FILE,
    MODEL_COMPARISON_FILE,
    SLM_VS_LLM_FILE,
    TOKEN_COMPARISON_FILE,
    RESULTS_DIR,
)

# Lazy-initialized so `--help` works even when matplotlib is not installed.
plt: ModuleType | None = None


DEFAULT_INPUT_FILES = [
    ABLATION_RESULTS_FILE,
    MODEL_COMPARISON_FILE,
    EMBEDDING_COMPARISON_FILE,
    FULL_MATRIX_FILE,
    TOKEN_COMPARISON_FILE,
    SLM_VS_LLM_FILE,
]

TABLE_HEADER_MARKERS = (
    "TopicAcc",
    "ModeAcc",
    "AvgCost",
    "AvgTotal",
    "AvgTotTok",
    "AvgInput",
    "AvgInTok",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create PNG charts from evaluation result text files."
    )
    parser.add_argument(
        "--input",
        nargs="+",
        default=DEFAULT_INPUT_FILES,
        help="One or more result files to parse.",
    )
    parser.add_argument(
        "--output-dir",
        default=f"{RESULTS_DIR}/graphs",
        help="Directory where graphs will be saved.",
    )
    return parser.parse_args()


def _init_plotting_backend() -> bool:
    global plt
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as _plt

        plt = _plt
        _plt.style.use("seaborn-v0_8-whitegrid")
        _plt.rcParams.update(
            {
                "figure.dpi": 220,
                "savefig.dpi": 300,
                "axes.titlesize": 14,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10,
            }
        )
        return True
    except ModuleNotFoundError:
        print(
            "matplotlib not found. "
            "Please ensure dependencies are installed: `pip install -r requirements.txt`."
        )
        return False
    except Exception as exc:
        print(f"Failed to initialize matplotlib backend: {exc}")
        return False


def _is_separator_line(line: str) -> bool:
    text = line.strip()
    if not text:
        return True
    return bool(re.fullmatch(r"[=\-─_ ]+", text))


def _normalize_header(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _to_number(value: str) -> float | None:
    cleaned = value.strip()
    cleaned = cleaned.replace(",", "")
    cleaned = cleaned.replace("%", "")
    cleaned = cleaned.replace("ms", "")
    cleaned = cleaned.replace("$", "")
    cleaned = cleaned.strip()
    if cleaned == "":
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _to_number_or_nan(value: str) -> float:
    parsed = _to_number(value)
    return parsed if parsed is not None else float("nan")


def _extract_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    tables: list[tuple[list[str], list[list[str]]]] = []
    current_header: list[str] | None = None
    current_rows: list[list[str]] = []

    for raw_line in text.splitlines():
        if "|" not in raw_line:
            if current_header and current_rows:
                tables.append((current_header, current_rows))
                current_header = None
                current_rows = []
            continue

        line = raw_line.strip()
        if _is_separator_line(line):
            continue

        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 2:
            continue

        if any(marker in line for marker in TABLE_HEADER_MARKERS):
            if current_header and current_rows:
                tables.append((current_header, current_rows))
                current_rows = []
            current_header = cells
            continue

        if current_header:
            if len(cells) != len(current_header):
                continue
            first = cells[0]
            if first.startswith("──") or first.startswith("Winner"):
                continue
            current_rows.append(cells)

    if current_header and current_rows:
        tables.append((current_header, current_rows))

    return tables


def _get_column_indices(headers: list[str]) -> dict[str, int]:
    normalized = [_normalize_header(h) for h in headers]
    mapping: dict[str, int] = {}
    aliases = {
        "label": ("mode", "model", "embedding"),
        "topic_acc": ("topicacc",),
        "mode_acc": ("modeacc",),
        "latency": ("lat", "latms"),
        "avg_cost": ("avgcost",),
        "avg_total": ("avgtotal", "avgtottok"),
        "avg_input": ("avginput", "avgintok"),
        "avg_output": ("avgoutput", "avgouttok"),
        "hallucination": ("hall", "halluc", "hallucrate", "hallucinationrate"),
    }

    mapping["label"] = 0
    for key, options in aliases.items():
        if key == "label":
            continue
        for i, item in enumerate(normalized):
            if item in options:
                mapping[key] = i
                break

    return mapping


def _save_bar_chart(
    labels: list[str],
    values: list[float],
    title: str,
    ylabel: str,
    output_path: Path,
    color: str = "#4F81BD",
) -> None:
    assert plt is not None
    if not labels or not values:
        return
    plt.figure(figsize=(max(8, len(labels) * 0.9), 5))
    plt.bar(labels, values, color=color)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def _save_grouped_accuracy_chart(
    labels: list[str],
    topic_values: list[float],
    mode_values: list[float],
    title: str,
    output_path: Path,
) -> None:
    assert plt is not None
    if not labels:
        return
    x = list(range(len(labels)))
    width = 0.38
    left = [i - width / 2 for i in x]
    right = [i + width / 2 for i in x]

    plt.figure(figsize=(max(8, len(labels) * 0.9), 5))
    plt.bar(left, topic_values, width=width, label="Topic Accuracy (%)", color="#4F81BD")
    plt.bar(right, mode_values, width=width, label="Mode Accuracy (%)", color="#C0504D")
    plt.xticks(x, labels, rotation=30, ha="right")
    plt.ylabel("Accuracy (%)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def _build_graphs_for_table(
    headers: list[str],
    rows: list[list[str]],
    base_name: str,
    table_index: int,
    output_dir: Path,
) -> list[Path]:
    assert plt is not None
    indices = _get_column_indices(headers)
    label_index = indices["label"]

    labels: list[str] = []
    topic_vals: list[float] = []
    mode_vals: list[float] = []
    latency_vals: list[float] = []
    cost_vals: list[float] = []
    total_tokens_vals: list[float] = []
    input_tokens_vals: list[float] = []
    output_tokens_vals: list[float] = []
    hallucination_vals: list[float] = []

    def _row_value_or_nan(row_values: list[str], col_name: str) -> float:
        index = indices.get(col_name)
        if index is None or index >= len(row_values):
            return float("nan")
        return _to_number_or_nan(row_values[index])

    for row in rows:
        if label_index >= len(row):
            continue
        label = row[label_index].strip()
        if not label:
            continue
        labels.append(label)

        topic_vals.append(_row_value_or_nan(row, "topic_acc"))
        mode_vals.append(_row_value_or_nan(row, "mode_acc"))
        latency_vals.append(_row_value_or_nan(row, "latency"))
        cost_vals.append(_row_value_or_nan(row, "avg_cost"))
        total_tokens_vals.append(_row_value_or_nan(row, "avg_total"))
        input_tokens_vals.append(_row_value_or_nan(row, "avg_input"))
        output_tokens_vals.append(_row_value_or_nan(row, "avg_output"))
        hallucination_vals.append(_row_value_or_nan(row, "hallucination"))

    def _filter_valid_pairs(xs: list[str], ys: list[float]) -> tuple[list[str], list[float]]:
        valid: list[tuple[str, float]] = []
        for x, y in zip(xs, ys, strict=True):
            if math.isnan(y):
                continue
            valid.append((x, y))
        if not valid:
            return [], []
        x_out, y_out = zip(*valid)
        return list(x_out), list(y_out)

    def _filter_valid_triples(
        xs: list[str], ys1: list[float], ys2: list[float]
    ) -> tuple[list[str], list[float], list[float]]:
        valid: list[tuple[str, float, float]] = []
        for x, y1, y2 in zip(xs, ys1, ys2, strict=True):
            if math.isnan(y1) or math.isnan(y2):
                continue
            valid.append((x, y1, y2))
        if not valid:
            return [], [], []
        x_out, y1_out, y2_out = zip(*valid)
        return list(x_out), list(y1_out), list(y2_out)

    created: list[Path] = []
    prefix = f"{base_name}_table_{table_index}"

    if "topic_acc" in indices and "mode_acc" in indices:
        labels_clean, topic_clean, mode_clean = _filter_valid_triples(labels, topic_vals, mode_vals)
        if topic_clean and mode_clean:
            p = output_dir / f"{prefix}_accuracy.png"
            _save_grouped_accuracy_chart(labels_clean, topic_clean, mode_clean, f"{base_name} - Accuracy", p)
            created.append(p)

    if "latency" in indices:
        labels_clean, latency_clean = _filter_valid_pairs(labels, latency_vals)
        if latency_clean:
            p = output_dir / f"{prefix}_latency.png"
            _save_bar_chart(labels_clean, latency_clean, f"{base_name} - Latency", "Latency (ms)", p, color="#9BBB59")
            created.append(p)

    if "hallucination" in indices:
        labels_clean, hall_clean = _filter_valid_pairs(labels, hallucination_vals)
        if hall_clean:
            p = output_dir / f"{prefix}_hallucination_rate.png"
            _save_bar_chart(
                labels_clean,
                hall_clean,
                f"{base_name} - Hallucination Rate",
                "Hallucination Rate (%)",
                p,
                color="#C0504D",
            )
            created.append(p)

    if "topic_acc" in indices and "latency" in indices:
        lbl, lat_clean, acc_clean = _filter_valid_triples(labels, latency_vals, topic_vals)
        if lat_clean and acc_clean:
            p = output_dir / f"{prefix}_latency_vs_accuracy.png"
            plt.figure(figsize=(8, 6))
            plt.scatter(lat_clean, acc_clean, color="#4F81BD", s=80, alpha=0.9)
            for i, name in enumerate(lbl):
                plt.annotate(name, (lat_clean[i], acc_clean[i]), xytext=(4, 4), textcoords="offset points")
            plt.xlabel("Latency (ms)")
            plt.ylabel("Topic Accuracy (%)")
            plt.title(f"{base_name} - Latency vs Accuracy")
            plt.tight_layout()
            plt.savefig(p, dpi=300)
            plt.close()
            created.append(p)

    if "avg_cost" in indices:
        labels_clean, cost_clean = _filter_valid_pairs(labels, cost_vals)
        if cost_clean:
            p = output_dir / f"{prefix}_cost.png"
            _save_bar_chart(labels_clean, cost_clean, f"{base_name} - Avg Cost", "Cost (USD/query)", p, color="#8064A2")
            created.append(p)

    if "avg_total" in indices:
        labels_clean, total_clean = _filter_valid_pairs(labels, total_tokens_vals)
        if total_clean:
            p = output_dir / f"{prefix}_avg_total_tokens.png"
            _save_bar_chart(labels_clean, total_clean, f"{base_name} - Avg Total Tokens", "Tokens/query", p, color="#F79646")
            created.append(p)

    if "avg_input" in indices and "avg_output" in indices:
        labels_clean, clean_in, clean_out = _filter_valid_triples(labels, input_tokens_vals, output_tokens_vals)
        if clean_in and clean_out:
            x = list(range(len(labels_clean)))
            width = 0.38
            left = [i - width / 2 for i in x]
            right = [i + width / 2 for i in x]
            p = output_dir / f"{prefix}_input_output_tokens.png"
            plt.figure(figsize=(max(8, len(labels_clean) * 0.9), 5))
            plt.bar(left, clean_in, width=width, label="Avg Input Tokens", color="#4BACC6")
            plt.bar(right, clean_out, width=width, label="Avg Output Tokens", color="#C0504D")
            plt.xticks(x, labels_clean, rotation=30, ha="right")
            plt.ylabel("Tokens/query")
            plt.title(f"{base_name} - Avg Input vs Output Tokens")
            plt.legend()
            plt.tight_layout()
            plt.savefig(p, dpi=200)
            plt.close()
            created.append(p)

    return created


def main() -> None:
    args = _parse_args()
    if not _init_plotting_backend():
        return
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_created: list[Path] = []
    for input_path in args.input:
        path = Path(input_path)
        if not path.exists():
            print(f"[skip] File not found: {path}")
            continue

        text = path.read_text(encoding="utf-8")
        tables = _extract_tables(text)
        if not tables:
            print(f"[skip] No comparison table found in: {path}")
            continue

        base_name = path.stem
        for idx, (headers, rows) in enumerate(tables, start=1):
            created = _build_graphs_for_table(
                headers=headers,
                rows=rows,
                base_name=base_name,
                table_index=idx,
                output_dir=output_dir,
            )
            all_created.extend(created)

    if all_created:
        print("Generated graphs:")
        for p in all_created:
            print(f"  - {p}")
    else:
        print("No graphs were generated. Ensure result files contain comparison tables.")


if __name__ == "__main__":
    main()
