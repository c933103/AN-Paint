"""Host checks for canonical locale XML and retained translation provenance."""
import ast
import hashlib
import json
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET

import gimp_translations
import krita_translations
import mainstream_translations
import translation_catalogues as translations


class TranslationCatalogueTests(unittest.TestCase):
    def test_picker_android_locale_list_and_canonical_catalogues_agree(self):
        tags = translations.offered_tags()
        platform = [
            node.get("{http://schemas.android.com/apk/res/android}name")
            for node in ET.parse(translations.RES / "xml/app_locales.xml").getroot()
        ]
        self.assertEqual(tags, platform)
        self.assertEqual(len(tags), len(set(tags)))
        self.assertEqual(tags[0], "en-001")
        self.assertEqual(tags[1:], sorted(tags[1:], key=str.casefold))
        self.assertNotIn("zh-Hant", tags)
        for tag in ("zh-TW", "zh-HK", "mn-Cyrl-MN", "mn-Mong", "tdd",
                    "sr-Latn", "sr-Cyrl", "en-US", "ja", "ar"):
            self.assertIn(tag, tags)

        catalogues = translations.catalogue_paths()
        for tag in tags:
            self.assertIn(tag, catalogues, f"{tag} has no exact strings.xml catalogue")

        names = ET.parse(translations.RES / "values/app_language_names.xml")
        labels = names.findall(".//string-array[@name='app_language_names']/item")
        self.assertEqual(len(tags), len(labels))
        self.assertTrue(all(item.text and item.text.strip() for item in labels))

    def test_canonical_catalogues_are_structurally_valid(self):
        self.assertEqual([], translations.validate_all(require_complete=False))


    def test_completed_korean_and_vietnamese_catalogues_are_complete(self):
        for tag in ("ko-KR", "ko-KP", "ko-Kore-KR", "vi", "vi-Hani"):
            self.assertEqual(
                [],
                translations.validate_catalogue(tag, require_complete=True),
                tag,
            )

    def test_new_korean_and_vietnamese_script_variants_are_registered(self):
        tags = translations.offered_tags()
        self.assertIn("ko-Kore-KR", tags)
        self.assertIn("vi-Hani", tags)
        self.assertNotIn("ko-Hani", tags)

        vi_hani = "".join(
            translations.read_strings(
                translations.catalogue_paths()["vi-Hani"]
            ).values()
        )
        self.assertRegex(vi_hani, r"[\u3400-\u9fff\uf900-\ufaff]")

        ko_kore = "".join(
            translations.read_strings(
                translations.catalogue_paths()["ko-Kore-KR"]
            ).values()
        )
        self.assertRegex(ko_kore, r"[\uac00-\ud7a3]")
        self.assertRegex(ko_kore, r"[\u3400-\u9fff\uf900-\ufaff]")
        # Quốc Ngữ letters with Vietnamese-specific diacritics must not leak
        # into the Hán-Nôm UI. Latin technical/product names are allowed.
        self.assertNotRegex(
            vi_hani,
            r"[ĂÂĐÊÔƠƯăâđêôơư"
            r"ÀÁẠẢÃẦẤẬẨẪẰẮẶẲẴ"
            r"ÈÉẸẺẼỀẾỆỂỄ"
            r"ÌÍỊỈĨ"
            r"ÒÓỌỎÕỒỐỘỔỖỜỚỢỞỠ"
            r"ÙÚỤỦŨỪỨỰỬỮ"
            r"ỲÝỴỶỸ"
            r"àáạảãầấậẩẫằắặẳẵ"
            r"èéẹẻẽềếệểễ"
            r"ìíịỉĩ"
            r"òóọỏõồốộổỗờớợởỡ"
            r"ùúụủũừứựửữ"
            r"ỳýỵỷỹ]",
        )

    def test_default_catalogue_has_no_duplicate_string_or_plural_keys(self):
        seen = set()
        for path in sorted((translations.RES / "values").glob("*.xml")):
            for node in ET.parse(path).getroot():
                if node.tag not in ("string", "plurals"):
                    continue
                key = (node.tag, node.get("name"))
                self.assertNotIn(key, seen, f"{path}/{node.get('name')}")
                seen.add(key)

    def test_locales_do_not_duplicate_string_keys_across_files(self):
        for folder in translations.RES.glob("values*"):
            seen = set()
            for path in folder.glob("*.xml"):
                for node in ET.parse(path).getroot():
                    if node.tag != "string":
                        continue
                    key = node.get("name")
                    self.assertNotIn(key, seen, str(path) + "/" + key)
                    seen.add(key)

    def test_requested_main_menu_surface_exists_without_freezing_old_wording(self):
        data = json.loads((translations.DATA / "main-menu-translations.json").read_text())
        requested = set(
            "ja zh-TW zh-HK zh-CN yue-Hant yue-Latn lzh-Hant ar de pl ru "
            "es-419 es-ES pt-PT pt-BR it fr he ko-KR ko-KP id ms vi tl th "
            "el sr-Cyrl sr-Latn tr hy".split()
        )
        self.assertEqual(requested, set(data["locales"]))
        source = (
            translations.ROOT
            / "Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt"
        ).read_text()
        commands = source.split("private fun menuActions(", 1)[1].split(
            "private fun menuActionEnabled", 1
        )[0]
        keys = set(re.findall(r"R.string.([a-z_0-9]+)", commands))
        groups = source.split("private enum class EditGroup(", 1)[1].split(
            "private lateinit var toolDrawer", 1
        )[0]
        keys.update(re.findall(r"R.string.([a-z_0-9]+)", groups))
        keys -= {"ui_select_an_area_first"}
        keys |= {
            "ui_menu_view", "ui_draw26", "ui_menu_file", "ui_menu_edit",
            "ui_colour_tab23", "ui_drawing23", "ui_category_selection",
            "ui_category_insert", "ui_eraser", "ui_bucket_fill", "ui_eyedropper",
            "ui_navigate", "ui_fg", "ui_bg", "ui_swap23", "ui_reset_bw23",
            "ui_advanced", "ui_add_colour26",
        }
        self.assertLessEqual(keys, set(data["required_keys"]))
        catalogues = translations.catalogue_paths()
        for tag in requested:
            rendered = translations.read_strings(catalogues[tag])
            self.assertLessEqual(set(data["required_keys"]), set(rendered), tag)

    def test_known_semantic_corrections_remain_correct(self):
        ja = translations.read_strings(translations.catalogue_paths()["ja"])
        self.assertEqual("左右反転", ja["ui_flip_horizontal"])
        self.assertEqual("上下反転", ja["ui_flip_vertical"])

    def test_unsaved_prompt_actions_are_distinct(self):
        def normalized(value):
            return value.strip().strip('"').casefold()

        for tag, path in translations.catalogue_paths().items():
            strings = translations.read_strings(path)
            if "ui_discard_changes23" not in strings or "ui_keep_editing23" not in strings:
                continue
            self.assertNotEqual(
                normalized(strings["ui_discard_changes23"]),
                normalized(strings["ui_keep_editing23"]),
                tag,
            )

    def test_latin_script_catalogues_do_not_regress_to_other_scripts(self):
        catalogues = translations.catalogue_paths()
        for tag in ("yue-Latn", "sr-Latn", "uz-Latn", "tt-Latn"):
            text = "".join(translations.read_strings(catalogues[tag]).values())
            if tag == "yue-Latn":
                self.assertNotRegex(text, r"[\u3400-\u9fff]")
            else:
                self.assertNotRegex(text, r"[\u0400-\u04ff]")


class GimpProvenanceTests(unittest.TestCase):
    def test_selected_entries_preserve_original_po_text_and_context(self):
        snapshot = json.loads((translations.DATA / "gimp-catalogues.json").read_text())
        self.assertEqual("e670132a59be1e8fb98d5b935824e4f57937b4ae", snapshot["revision"])
        self.assertEqual("GPL-3.0-or-later", snapshot["license"])
        self.assertNotIn(
            "tt",
            snapshot["locale_map"],
            "GIMP's old Latin Tatar catalogue must not be treated as Cyrillic Tatar",
        )
        notices = (
            translations.RES.parent / "assets/legal/GIMP_TRANSLATION_NOTICES.txt"
        ).read_bytes().decode()
        for source in snapshot["sources"]:
            self.assertIn(source["header"], notices)
            self.assertRegex(source["source_sha256"], r"^[0-9a-f]{64}$")
            for entry in source["entries"]:
                parsed = {}
                field = None
                for line in entry["raw"].splitlines():
                    if line.startswith(("msgctxt ", "msgid ", "msgstr ")):
                        field, value = line.split(" ", 1)
                        parsed[field] = ast.literal_eval(value)
                    elif line.startswith('"') and field:
                        parsed[field] += ast.literal_eval(line)
                for key in ("msgctxt", "msgid", "msgstr"):
                    self.assertEqual(entry.get(key), parsed.get(key), source["path"])
                self.assertNotRegex(entry["raw"], r"(?m)^#,.*\bfuzzy\b")

    def test_context_mapping_still_describes_the_reference_material(self):
        mapping = json.loads((translations.DATA / "gimp-terms.json").read_text())
        for key in ("ui_cut", "ui_copy", "ui_paste"):
            self.assertEqual("edit-action", mapping[key]["msgctxt"])
        self.assertEqual("Flip _Horizontally", mapping["ui_flip_horizontal"]["msgid"])
        self.assertEqual("Flip _Vertically", mapping["ui_flip_vertical"]["msgid"])
        self.assertEqual("進階…", gimp_translations.adapt("進階(_A)...", "Advanced…"))


class KritaProvenanceTests(unittest.TestCase):
    def test_selected_entries_preserve_context_notices_and_source_identity(self):
        snapshot = json.loads((translations.DATA / "krita-catalogues.json").read_text())
        self.assertEqual("428d44705de20770434ea2915021241dc073879c", snapshot["revision"])
        self.assertEqual(14, len(snapshot["audited_sources"]))
        notice = (
            translations.RES.parent / "assets/legal/KRITA_TRANSLATION_NOTICES.txt"
        ).read_text()
        self.assertIn((translations.DATA / "KRITA-COPYING.txt").read_text(), notice)
        for source in snapshot["sources"]:
            self.assertIn(source["header"], notice)
            self.assertRegex(source["blob_sha"], r"^[0-9a-f]{40}$")
            for entry in source["entries"]:
                parsed = {}
                field = None
                for line in entry["raw"].splitlines():
                    if line.startswith(("msgctxt ", "msgid ", "msgstr ")):
                        field, value = line.split(" ", 1)
                        parsed[field] = ast.literal_eval(value)
                    elif line.startswith('"') and field:
                        parsed[field] += ast.literal_eval(line)
                for key in ("msgctxt", "msgid", "msgstr"):
                    self.assertEqual(entry.get(key), parsed.get(key), source["path"])
                self.assertNotRegex(entry["raw"], r"(?m)^#,.*\bfuzzy\b")


class MainstreamProvenanceTests(unittest.TestCase):
    def test_exact_source_contexts_and_translator_notices_are_preserved(self):
        for project, revision, count, licence in (
            ("libreoffice", "84fc1f3ce6a7d0ff415ac93495ba172b8ce2bac6", 14, "LIBREOFFICE-COPYING.MPL"),
            ("mediawiki", "ea83228d5fe2b1f9559196a2716c8580cdb2407d", 8, "MEDIAWIKI-COPYING.txt"),
        ):
            data = json.loads((translations.DATA / f"{project}-catalogues.json").read_text())
            self.assertEqual(revision, data["revision"])
            self.assertEqual(count, len(data["sources"]))
            raw_licence = (translations.DATA / licence).read_bytes()
            self.assertEqual(
                data["license_blob_sha"],
                hashlib.sha1(
                    b"blob " + str(len(raw_licence)).encode() + b"\0" + raw_licence
                ).hexdigest(),
            )
            notice = (
                translations.RES.parent
                / f"assets/legal/{project.upper()}_TRANSLATION_NOTICES.txt"
            ).read_text()
            self.assertIn((translations.DATA / licence).read_text(), notice)
            for source in data["sources"]:
                self.assertRegex(source["blob_sha"], r"^[0-9a-f]{40}$")
                self.assertIn(source["blob_sha"], notice)
                if project == "mediawiki":
                    for author in source["metadata"]["authors"]:
                        self.assertIn(author, notice)
                    continue
                self.assertIn(source["header"], notice)
                for entry in source["entries"]:
                    parsed = {}
                    field = None
                    for line in entry["raw"].splitlines():
                        if line.startswith(("msgctxt ", "msgid ", "msgstr ")):
                            field, value = line.split(" ", 1)
                            parsed[field] = ast.literal_eval(value)
                        elif line.startswith('"') and field:
                            parsed[field] += ast.literal_eval(line)
                    self.assertEqual(
                        {k: entry[k] for k in ("msgctxt", "msgid", "msgstr")},
                        parsed,
                    )
                    self.assertNotRegex(entry["raw"], r"(?m)^#,.*\bfuzzy\b")

    def test_reference_mappings_keep_known_semantic_rejections(self):
        mapping = json.loads((translations.DATA / "libreoffice-terms.json").read_text())
        self.assertIn("Popups..uno:PickList\nLabel", mapping["ui_menu_file"]["msgctxt"])
        self.assertIn(
            "Commands..uno:FlipHorizontal\nLabel",
            mapping["ui_flip_horizontal"]["msgctxt"],
        )
        self.assertNotIn("ui_clear", mapping)


class TatarReferenceTests(unittest.TestCase):
    def test_reviewed_tatar_transcription_reference_is_internally_consistent(self):
        source = json.loads((translations.DATA / "tatar-transcription.json").read_text())
        basic = json.loads((translations.DATA / "basic-translations.json").read_text())["tt"]
        self.assertEqual(set(basic.values()), set(source["cyrillic_to_latin"]))
        for app_key, upstream_key in source["mapping"].items():
            original = source["original_strings"][upstream_key]
            self.assertEqual(original[0].upper() + original[1:], basic[app_key])


if __name__ == "__main__":
    unittest.main()
