"""Narrow guards for Hakka contextual readings and the missing-picker warning.

These compare reviewed Han/PFS terms in their resource context. They do not
certify the rest of either catalogue or generate translations.
"""
import json
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET
from latin_sinitic_priority_expectations import bound_fixture, require_row


RES = pathlib.Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"


def strings(qualifier):
    return {
        node.get("name"): "".join(node.itertext())
        for node in ET.parse(RES / qualifier / "strings.xml").getroot()
        if node.tag == "string"
    }

def require_latin_save_label(value):
    row=bound_fixture('hak-Latn-TW')['rows']['ui_save_a5d0d9']
    require_row('hak-Latn-TW','ui_save_a5d0d9',row)
    if value!=row['reviewed_value']:raise ValueError('Exact independently reviewed Save label differs')
    return value


class HakkaContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.han = strings("values-b+hak+Hant+TW")
        cls.latin = strings("values-b+hak+Latn+TW")

    def assert_paired_term(self, han_term, pfs_pattern):
        keys = [key for key, text in self.han.items() if han_term in text]
        self.assertTrue(keys, han_term)
        for key in keys:
            with self.subTest(key=key, term=han_term):
                self.assertEqual(
                    self.han[key].count(han_term),
                    len(re.findall(pfs_pattern, self.latin[key], re.IGNORECASE)),
                )

    def test_full_missing_picker_warning_keeps_failure_and_recovery_steps(self):
        # The fixture binds all clauses, not just the corrected result complement.
        # Matching it does not certify fluency or the rest of either catalogue.
        fixture = json.loads(
            (pathlib.Path(__file__).with_name("fixtures") /
             "hakka_file_picker_warning.json").read_text(encoding="utf-8")
        )
        key = fixture["key"]
        self.assertEqual(fixture["source"], strings("values")[key])
        self.assertEqual(fixture["han"], self.han[key])
        self.assertEqual(fixture["pfs"], self.latin[key])

    def test_spatial_back_is_not_the_carrying_reading(self):
        # MOE boi55 -> PFS poi; ba11 -> pà is the verb "carry".
        self.assert_paired_term("肚背", r"\btú[- ]poi\b")
        self.assert_paired_term("下背", r"\bhâ[- ]poi\b")

    def test_next_time_is_not_spatial_below(self):
        # MOE 下擺 ha55 bai31, versus 下背 ha24 boi55.
        self.assert_paired_term("下擺", r"\bha[- ]pái\b")

    def test_save_and_system_terms_remain_paired_in_every_occurrence(self):
        self.assert_paired_term("保存", r"\bpó[- ]sùn\b")
        self.assert_paired_term("系統", r"\bne[- ]thúng\b")
        self.assertEqual("@string/ui_save", self.han["ui_save_a5d0d9"])
        self.assertEqual("Pó-sùn…",require_latin_save_label(self.latin["ui_save_a5d0d9"]))
        self.assertNotEqual(self.latin["ui_save"],self.latin["ui_save_a5d0d9"])

    def test_latin_save_complete_label_rejects_alias_and_changed_action(self):
        for value in ['@string/ui_save','Pó-sùn','forged']:
            with self.assertRaises(ValueError):require_latin_save_label(value)

if __name__ == "__main__":
    unittest.main()
