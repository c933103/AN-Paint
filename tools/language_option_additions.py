"""Accepted option identities and truthful empty-catalogue fallback contracts."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

FIXTURES = Path(__file__).resolve().parent / "fixtures"
ADDITIONS_PATH = FIXTURES / "language_option_additions_20261012.json"
SECOND_ADDITIONS_PATH = FIXTURES / "language_option_additions_20261012_second.json"
FIRST_ADDED_TAGS = {row["tag"] for row in json.loads(ADDITIONS_PATH.read_text())["languages"]}
SECOND_ADDED_TAGS = {row["tag"] for row in json.loads(SECOND_ADDITIONS_PATH.read_text())["languages"]}
ADDED_TAGS = FIRST_ADDED_TAGS | SECOND_ADDED_TAGS


def require_untranslated_option(row, xml):
    for field, expected in (('translation_status', 'not-started'),
                            ('linguistic_review', 'not-started'),
                            ('fallback', 'default-English'),
                            ('source_strings_present', 0),
                            ('source_plurals_present', 0)):
        if row.get(field) != expected:
            raise ValueError('Untranslated option status differs: '+field)
    root = ET.fromstring(xml)
    if root.tag != 'resources' or root.attrib or list(root) or (root.text or '').strip():
        raise ValueError('Untranslated fallback catalogue must remain empty')
