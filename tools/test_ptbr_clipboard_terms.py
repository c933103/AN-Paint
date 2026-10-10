"""Bounded regression guard for reviewed P07-008 Brazilian Portuguese wording.

This protects a documented glossary and one recovered mistranslation. It is not
a fluency test, UI execution, or acceptance of the complete pt-BR catalogue.
Review evidence: verification/ptbr-clipboard-recheck-2026-10-10/README.md.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


RESOURCE = (Path(__file__).resolve().parents[1]
            / "Paintroid/src/main/res/values-pt-rBR/strings.xml")
MEMORY = "ui_estimates_include_the_current_canvas_and_clipboard_sampled"
REVIEWED_LABELS = {
    "ui_cut": "Recortar",
    "ui_copy": "Copiar",
    "ui_paste": "Colar",
    "ui_copy_all": "Copiar tudo",
    "gallery_copy_credit": "Copiar crédito",
    "gallery_credit_copied": "Crédito copiado",
    "ui_full_text_copied": "Texto completo copiado",
}


def wording_errors(strings):
    errors = [key for key, wording in REVIEWED_LABELS.items()
              if strings.get(key) != wording]
    memory = strings.get(MEMORY, "")
    if "área de transferência" not in memory or "área de download" in memory:
        errors.append(MEMORY)
    return errors


class BrazilianPortugueseClipboardTermsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strings = {node.attrib["name"]: "".join(node.itertext())
                       for node in ET.parse(RESOURCE).getroot()
                       if node.tag == "string"}

    def test_current_reviewed_glossary(self):
        self.assertEqual([], wording_errors(self.strings))

    def test_each_reviewed_label_rejects_an_unreviewed_replacement(self):
        for key in REVIEWED_LABELS:
            with self.subTest(resource=key):
                changed = {**self.strings, key: "UNREVIEWED REPLACEMENT"}
                self.assertEqual([key], wording_errors(changed))

    def test_recovered_download_area_mistranslation_is_rejected(self):
        changed = dict(self.strings)
        changed[MEMORY] = changed[MEMORY].replace(
            "área de transferência", "área de download")
        self.assertEqual([MEMORY], wording_errors(changed))

    def test_missing_reviewed_resources_are_rejected_individually(self):
        for key in (*REVIEWED_LABELS, MEMORY):
            with self.subTest(resource=key):
                changed = dict(self.strings)
                del changed[key]
                self.assertEqual([key], wording_errors(changed))


if __name__ == "__main__":
    unittest.main()
