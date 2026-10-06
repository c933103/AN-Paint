"""Narrow guards for the Hakka contextual readings rechecked on 2026-10-06.

These compare reviewed Han/PFS terms in their resource context. They do not
certify the rest of either catalogue or generate translations.
"""
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET


RES = pathlib.Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"


def strings(qualifier):
    return {
        node.get("name"): "".join(node.itertext())
        for node in ET.parse(RES / qualifier / "strings.xml").getroot()
        if node.tag == "string"
    }


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
        self.assertEqual("@string/ui_save", self.latin["ui_save_a5d0d9"])


if __name__ == "__main__":
    unittest.main()
