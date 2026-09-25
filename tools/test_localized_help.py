"""Regression checks for documented controls, independent of any PR locale scope.

These checks establish navigation and known corruption regressions, not fluency.
They intentionally read every resource XML (including default release files).
"""
from pathlib import Path
import re
import unicodedata
import unittest
import xml.etree.ElementTree as ET


RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
MANUAL = "ui_the_arrow_on_the_left_directly_below_the"
ASSEMBLY = "ui_add_up_to_20_images_with_android_s"
ACTIVE_GALLERY = ("ui_irasutoya_help34", "ui_openclipart_help34", "gallery_description")


def catalogues():
    result = {}
    for directory in sorted(RES.glob("values*")):
        strings = {}
        for path in sorted(directory.glob("*.xml")):
            for node in ET.parse(path).getroot():
                if node.tag == "string":
                    strings[node.get("name")] = "".join(node.itertext())
        result[directory.name] = strings
    return result


def displayed(value):
    value = value.replace(r"\'", "'").replace(r'\"', '"')
    value = unicodedata.normalize("NFC", value).casefold()
    # Hyphens separate the same words in some Ainu/Hakka help captions. Spaces,
    # quote style and standalone final punctuation are layout, not inflection.
    return re.sub(r'[\s\-‐‑"「」『』«»“”［］]+', "", value)


def caption(value):
    return displayed(value.rstrip(" \t\r\n.,;:!?…。！？；：།༎"))


def route_pattern(rendered, keys):
    return r"[།༎]*[>→]".join(re.escape(caption(rendered[key])) for key in keys)


class LocalizedHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.locales = catalogues()

    def test_active_gallery_routes_name_the_actual_controls(self):
        keys = ("ui_menu_file", "ui_about_credits23", "ui_image_credits")
        for locale, local in self.locales.items():
            rendered = {**self.locales["values"], **local}
            for resource in ACTIVE_GALLERY:
                if resource not in local:
                    continue
                with self.subTest(locale=locale, resource=resource):
                    self.assertRegex(displayed(local[resource]), route_pattern(rendered, keys))

    def test_final_copyright_paragraph_names_its_actual_panel(self):
        # The earlier check searched the whole manual and passed when its import
        # paragraph was right but its final copyright paragraph still said Help.
        keys = ("ui_menu_file", "ui_about_credits23")
        for locale, local in self.locales.items():
            if MANUAL not in local:
                continue
            rendered = {**self.locales["values"], **local}
            final_paragraph = re.split(r"\\n\\n|\n\s*\n", local[MANUAL])[-1]
            with self.subTest(locale=locale):
                self.assertRegex(displayed(final_paragraph), route_pattern(rendered, keys))

    def test_known_show_all_caption_corruptions_do_not_return(self):
        # A substring check would accept 示全部 inside the incorrect 顯示全部變更.
        # These phrases are known mistranslations of the source verb "changes";
        # this is deliberately not a general grammar or fluency classifier.
        corruptions = (
            "Show all changes zoom", "Show all changes view zoom",
            "すべての変更を表示", "顯示全部變更",
            "Afficher toutes les modifications", "Alle Änderungen anzeigen",
            "Показать все изменения", "Montri ĉiujn ŝanĝojn",
            "Ipakita ang lahat ng pagbabago", "Ipakita ang tanang kausaban",
            "Tunjuk semua perubahan",
        )
        for locale, local in self.locales.items():
            for resource in (MANUAL, ASSEMBLY):
                if resource not in local:
                    continue
                text = unicodedata.normalize("NFC", local[resource]).casefold()
                for wrong in corruptions:
                    with self.subTest(locale=locale, resource=resource, wrong=wrong):
                        self.assertNotIn(wrong.casefold(), text)


if __name__ == "__main__":
    unittest.main()
