"""Requested language-option identities; historical translation status is not a resource freeze."""
import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"
ADDITIONS_PATH = FIXTURES / "language_option_additions_20261012.json"
SECOND_ADDITIONS_PATH = FIXTURES / "language_option_additions_20261012_second.json"
FIRST_ADDED_TAGS = {row["tag"] for row in json.loads(ADDITIONS_PATH.read_text())["languages"]}
SECOND_ADDED_TAGS = {row["tag"] for row in json.loads(SECOND_ADDITIONS_PATH.read_text())["languages"]}
ADDED_TAGS = FIRST_ADDED_TAGS | SECOND_ADDED_TAGS
