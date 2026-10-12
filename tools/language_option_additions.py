"""Compose current fallback checks without rewriting the historical 140-tag evidence."""
import json
from pathlib import Path

ADDITIONS_PATH = Path(__file__).resolve().parent / "fixtures/language_option_additions_20261012.json"
ADDED_TAGS = {row["tag"] for row in json.loads(ADDITIONS_PATH.read_text())["languages"]}
