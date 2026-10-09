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
    value = re.sub(r"\\u([0-9a-fA-F]{4})", lambda match: chr(int(match[1], 16)), value)
    value = unicodedata.normalize("NFC", value).casefold()
    # Hyphens separate the same words in some Ainu/Hakka help captions. Spaces,
    # quote style and standalone final punctuation are layout, not inflection.
    return re.sub(r'[\s\-‐‑"「」『』«»“”„‟［］]+', "", value)


def caption(value):
    return displayed(value.rstrip(" \t\r\n.,;:!?…。！？；：།༎"))


def route_pattern(rendered, keys):
    def resolve(key):
        seen = set()
        while key not in seen:
            seen.add(key)
            value = rendered[key]
            if not value.startswith("@string/"):
                return value
            key = value.removeprefix("@string/")
        raise AssertionError(f"Cyclic caption reference: {key}")

    return r"[།༎]*[>→]".join(re.escape(caption(resolve(key))) for key in keys)


class LocalizedHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.locales = catalogues()

    def test_mongolian_legacy_assembly_help_preserves_the_image_limit(self):
        # Check the assembly section of this specific legacy resource. The
        # separate assembly manual and limit-error labels cannot satisfy it.
        source = (RES.parent / "java/org/catrobat/paintroid/classic/ImageAssembly.kt").read_text()
        limit = int(re.search(r"const val MAX_IMAGES = (\d+)", source)[1])
        manual = self.locales["values-b+mn+Mong"][MANUAL]
        route = "«ᠹᠠᠶᠢᠯ» > ᠵᠢᠷᠤᠭ ᠨᠡᠶᠢᠯᠡᠭᠦᠯᠬᠦ"
        section = re.split(r"\\n\\n|\n\s*\n", manual.split(route, 1)[1])[0]
        self.assertRegex(section, rf"\b{limit}\s+ᠬᠦᠷᠲᠡᠯᠡᠬᠢ\s+ᠵᠢᠷᠤᠭ\b")

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

    def test_paste_hints_name_the_actual_insert_controls(self):
        # The category caption is ui_category_insert, not the similarly named
        # ui_insert dialog action; Literary Chinese uses distinct words here.
        keys = ("ui_draw26", "ui_category_insert", "ui_other_images34")
        for locale, local in self.locales.items():
            rendered = {**self.locales["values"], **local}
            for resource in ("ui_paste_hint34", "ui_copy_an_area_or_use_file_insert_image"):
                if resource not in local:
                    continue
                with self.subTest(locale=locale, resource=resource):
                    self.assertRegex(displayed(local[resource]), route_pattern(rendered, keys))

    def test_cursor_help_includes_the_actual_settings_route(self):
        keys = ("ui_draw26", "ui_drawing23")
        for locale, local in self.locales.items():
            if "ui_cursor_help31" not in local:
                continue
            rendered = {**self.locales["values"], **local}
            with self.subTest(locale=locale):
                self.assertRegex(displayed(local["ui_cursor_help31"]), route_pattern(rendered, keys))

    def test_protected_draft_warning_names_recovery_and_save_as_routes(self):
        # recoverEditor() blocks autosave only when preserving the old draft
        # separately fails. The File menu exports that ZIP; Save as opens the
        # current image's format chooser. ProtectedDraftWarningTest exercises
        # those real handlers, including both PNG/JPEG choices and cancellation.
        # This guard checks every translated warning, not locale-wide fluency.
        resource = "ui_autosave_is_paused_to_protect_that_draft_use"
        for locale, local in self.locales.items():
            if resource not in local:
                continue
            rendered = {**self.locales["values"], **local}
            text = displayed(local[resource])
            with self.subTest(locale=locale):
                self.assertEqual(["%1$s"], re.findall(r"%\d+\$[a-zA-Z]", local[resource]))
                recovery = re.search(route_pattern(rendered, ("ui_menu_file", "ui_export_recovery_copy")), text)
                save = re.search(route_pattern(rendered, ("ui_menu_file", "save20_title")), text)
                self.assertIsNotNone(recovery, "Missing protected-draft export route")
                self.assertIsNotNone(save, "Missing current-work Save as route")
                self.assertLess(recovery.end(), save.start())
                # The recommended formats must follow Save as, rather than
                # being mistaken for part of the recovery ZIP export command.
                formats = text[save.end():]
                self.assertIn("png", formats)
                self.assertIn("jpeg", formats)

    def test_selection_hint_does_not_quote_the_resize_dialog_checkbox(self):
        # Selection uses ui_lock_proportions; ui_lock_aspect_ratio belongs to
        # the size dialog. A native paraphrase need not quote either caption.
        resource = "ui_drag_a_selection_drag_inside_to_move_square"
        for locale, local in self.locales.items():
            if resource not in local:
                continue
            rendered = {**self.locales["values"], **local}
            selection = caption(rendered["ui_lock_proportions"])
            resize = caption(rendered["ui_lock_aspect_ratio"])
            text = displayed(local[resource])
            if selection != resize and selection not in text:
                with self.subTest(locale=locale):
                    self.assertNotIn(resize, text)

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
