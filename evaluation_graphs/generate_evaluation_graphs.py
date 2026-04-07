"""
Generate evaluation graphs from research_evaluator result files.

Usage examples:
    python evaluation_graphs/generate_evaluation_graphs.py
    python evaluation_graphs/generate_evaluation_graphs.py --input model_comparison_results.txt
    python evaluation_graphs/generate_evaluation_graphs.py --output-dir evaluation_graphs/output
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


DEFAULT_INPUT_FILES = [
    "ablation_results.txt",
    "model_comparison_results.txt",
    "embedding_comparison_results.txt",
    "full_matrix_results.txt",
    "token_comparison_results.txt",
    "slm_vs_llm_results.txt",
]


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
        default="evaluation_graphs/output",
        help="Directory where graphs will be saved.",
    )
    return parser.parse_args()


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

        if any(h in line for h in ("TopicAcc", "ModeAcc", "AvgCost", "AvgTotal", "AvgTotTok", "AvgInput", "AvgInTok")):
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

    for row in rows:
        label = row[label_index].strip()
        if not label:
            continue
        labels.append(label)

        topic_vals.append(_to_number(row[indices["topic_acc"]]) if "topic_acc" in indices else float("nan"))
        mode_vals.append(_to_number(row[indices["mode_acc"]]) if "mode_acc" in indices else float("nan"))
        latency_vals.append(_to_number(row[indices["latency"]]) if "latency" in indices else float("nan"))
        cost_vals.append(_to_number(row[indices["avg_cost"]]) if "avg_cost" in indices else float("nan"))
        total_tokens_vals.append(_to_number(row[indices["avg_total"]]) if "avg_total" in indices else float("nan"))
        input_tokens_vals.append(_to_number(row[indices["avg_input"]]) if "avg_input" in indices else float("nan"))
        output_tokens_vals.append(_to_number(row[indices["avg_output"]]) if "avg_output" in indices else float("nan"))

    def _clean(vals: list[float]) -> list[float]:
        return [v for v in vals if v == v]

    created: list[Path] = []
    prefix = f"{base_name}_table_{table_index}"

    if "topic_acc" in indices and "mode_acc" in indices:
        p = output_dir / f"{prefix}_accuracy.png"
        _save_grouped_accuracy_chart(labels, topic_vals, mode_vals, f"{base_name} - Accuracy", p)
        created.append(p)

    if "latency" in indices:
        clean = _clean(latency_vals)
        if clean:
            p = output_dir / f"{prefix}_latency.png"
            _save_bar_chart(labels, latency_vals, f"{base_name} - Latency", "Latency (ms)", p, color="#9BBB59")
            created.append(p)

    if "avg_cost" in indices:
        clean = _clean(cost_vals)
        if clean:
            p = output_dir / f"{prefix}_cost.png"
            _save_bar_chart(labels, cost_vals, f"{base_name} - Avg Cost", "Cost (USD/query)", p, color="#8064A2")
            created.append(p)

    if "avg_total" in indices:
        clean = _clean(total_tokens_vals)
        if clean:
            p = output_dir / f"{prefix}_avg_total_tokens.png"
            _save_bar_chart(labels, total_tokens_vals, f"{base_name} - Avg Total Tokens", "Tokens/query", p, color="#F79646")
            created.append(p)

    if "avg_input" in indices and "avg_output" in indices:
        clean_in = _clean(input_tokens_vals)
        clean_out = _clean(output_tokens_vals)
        if clean_in and clean_out:
            x = list(range(len(labels)))
            width = 0.38
            left = [i - width / 2 for i in x]
            right = [i + width / 2 for i in x]
            p = output_dir / f"{prefix}_input_output_tokens.png"
            plt.figure(figsize=(max(8, len(labels) * 0.9), 5))
            plt.bar(left, input_tokens_vals, width=width, label="Avg Input Tokens", color="#4BACC6")
            plt.bar(right, output_tokens_vals, width=width, label="Avg Output Tokens", color="#C0504D")
            plt.xticks(x, labels, rotation=30, ha="right")
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
