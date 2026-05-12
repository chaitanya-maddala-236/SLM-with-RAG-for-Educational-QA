from __future__ import annotations

import re


def simple_token_count(text: str) -> int:
    return len(re.findall(r"\w+|[^\w\s]", text))


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
