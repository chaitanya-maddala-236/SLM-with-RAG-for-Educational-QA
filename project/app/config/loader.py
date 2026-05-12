from __future__ import annotations

import logging
from pathlib import Path

import yaml

from .schema import Settings

logger = logging.getLogger(__name__)


def load_settings(path: str | Path | None = None) -> Settings:
    config_path = Path(path or "project/app/config/defaults.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    settings = Settings.model_validate(data)
    logger.info("Loaded config from %s", config_path)
    return settings
