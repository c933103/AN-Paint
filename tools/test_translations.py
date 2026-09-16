"""Host checks for provenance, the selected shared vocabulary, and locale declarations."""
import json
import hashlib
import ast
import re
import gimp_translations
import krita_translations
import mainstream_translations
import unittest
from unittest import mock
import pathlib
import xml.etree.ElementTree as ET
import reuse_upstream_translations as translations


class TranslationTests(unittest.TestCase):
    def test_requested_main_menu_coverage_includes_every_command_and_exact_locale(self):
        data = json.loads((translations.DATA / "main-menu-translations.json").read_text())
        requested = set("ja zh-TW zh-HK zh-CN yue-Hant yue-Latn lzh-Hant ar de pl ru es-419 es-ES pt-PT pt-BR it fr he ko-KR ko-KP id ms vi tl th el sr-Cyrl sr-Latn tr hy".split())
        self.assertEqual(requested, set(data["locales"]))
        source = (translations.ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt").read_text()
        commands = source.split('private fun menuActions(', 1)[1].split('private fun menuActionEnabled', 1)[0]
        keys = set(re.findall(r'R.string.([a-z_0-9]+)', commands))
        groups = source.split('private enum class EditGroup(', 1)[1].split('private lateinit var toolDrawer', 1)[0]
        keys.update(re.findall(r'R.string.([a-z_0-9]+)', groups))
        # The two messages are command outcomes, not first-level labels.
        keys -= {"ui_select_an_area_first"}
        keys |= {"ui_menu_view", "ui_draw26", "ui_menu_file", "ui_menu_edit", "ui_colour_tab23",
                 "ui_drawing23", "ui_category_selection", "ui_category_insert", "ui_eraser", "ui_bucket_fill", "ui_eyedropper", "ui_navigate",
                 "ui_fg", "ui_bg", "ui_swap23", "ui_reset_bw23", "ui_advanced", "ui_add_colour26"}
        self.assertLessEqual(keys, set(data["required_keys"]))
        self.assertIn("ui_disable_cursor_drawing33", data["required_keys"])
        self.assertIn("ui_cursor_tap_hint37", data["required_keys"])
        for tag, terms in data["locales"].items():
            self.assertNotRegex(terms["ui_pixel_grid33"], r"800|%|％", tag)
        report = json.loads((translations.DATA / "coverage.json").read_text())
        for tag, terms in data["locales"].items():
            row = next(r for r in report["coverage"] if r["language_tag"] == tag)
            self.assertIn(tag, row["offered_tags"])
            rendered = translations.read_strings(translations.ROOT / row["generated_resource"])
            for key in data["required_keys"]:
                self.assertEqual(terms[key].replace("'", "\\'"), rendered[key], f"{tag}/{key}")
            if tag in ("yue-Latn", "sr-Latn"):
                self.assertNotRegex("".join(terms.values()), r"[\u0400-\u04ff\u3400-\u9fff]")

    def test_generated_translations_match_verified_upstream_bytes(self):
        for path, text in translations.generate().items():
            self.assertEqual(text, path.read_text(), str(path))

    def test_generation_is_independent_of_filesystem_enumeration_order(self):
        expected = translations.generate()
        original = pathlib.Path.glob
        def reversed_glob(path, pattern):
            return iter(reversed(list(original(path, pattern))))
        with mock.patch.object(pathlib.Path, "glob", reversed_glob):
            self.assertEqual(expected, translations.generate())

    def test_every_mapped_resource_exists_in_default_catalogue(self):
        names = set()
        for path in (translations.RES / "values").glob("*.xml"):
            names.update(node.get("name") for node in ET.parse(path).getroot())
        mapping = json.loads((translations.DATA / "common-terms.json").read_text())
        self.assertTrue(set(mapping) <= names, set(mapping) - names)

    def test_picker_and_android_locale_list_agree_and_coverage_accounts_for_every_option(self):
        tags = [node.text for node in ET.parse(translations.RES / "values/app_language_tags.xml").findall(".//item")]
        platform = [node.get("{http://schemas.android.com/apk/res/android}name")
                    for node in ET.parse(translations.RES / "xml/app_locales.xml").getroot()]
        self.assertEqual(tags, platform)
        self.assertEqual(len(tags), len(set(tags)))
        self.assertEqual(tags[0], "en-001")
        self.assertEqual(tags[1:], sorted(tags[1:], key=str.casefold))
        self.assertNotIn("zh-Hant", tags)
        for tag in ("zh-TW", "zh-HK", "mn-Cyrl-MN", "mn-Mong"):
            self.assertIn(tag, tags)
        self.assertIn("en-US", tags)
        self.assertNotIn("en", tags)
        self.assertIn("ja", tags)
        self.assertIn("ar", tags)
        self.assertIn("sr-Latn", tags)
        self.assertIn("sr-Cyrl", tags)
        coverage = json.loads((translations.DATA / "coverage.json").read_text())
        accounted = []
        for row in coverage["coverage"]:
            accounted.extend(row["offered_tags"])
            if row["offered_in_app"]:
                self.assertTrue((translations.ROOT / row["generated_resource"]).is_file())
            if row["offered_in_app"] and not row.get("name_only") and not row["language_tag"].startswith("en-"):
                self.assertGreater(row["entries_different_from_upstream_english"], 0)
        self.assertCountEqual(tags, accounted)
        self.assertEqual([], coverage["name_only_options"])
        self.assertIn("tdd", tags)
        self.assertNotIn("tai", tags)
        names = ET.parse(translations.RES / "values/app_language_names.xml")
        labels = names.findall(".//string-array[@name='app_language_names']/item")
        self.assertEqual(len(tags), len(labels))
        self.assertTrue(all(item.text and item.text.strip() for item in labels))

    def test_unsaved_prompt_never_reuses_the_discard_label_for_keep_editing(self):
        def normalized(value):
            return value.strip().strip('"').casefold()
        for path in translations.RES.glob("values*/strings.xml"):
            strings = translations.read_strings(path)
            if "ui_discard_changes23" in strings:
                self.assertNotEqual(normalized(strings["ui_discard_changes23"]), normalized(strings["ui_keep_editing23"]), str(path))
        for qualifier in ("values-b+lzh+Hant", "values-b+mn+Mong", "values-zh-rHK", "values-b+mn+Cyrl+MN"):
            strings = translations.read_strings(translations.RES / qualifier / "strings.xml")
            self.assertNotEqual(strings["ui_discard_changes23"], strings["ui_keep_editing23"])
            self.assertTrue(strings["ui_cut"].strip())

    def test_no_locale_duplicates_resources_across_generated_and_reviewed_catalogues(self):
        for folder in translations.RES.glob("values*"):
            seen = set()
            for path in folder.glob("*.xml"):
                for node in ET.parse(path).getroot():
                    if node.tag != "string":
                        continue
                    key = node.get("name")
                    self.assertNotIn(key, seen, str(path) + "/" + key)
                    seen.add(key)
        offered = [node.text for node in ET.parse(translations.RES / "values/app_language_tags.xml").findall(".//item")]
        self.assertIn("lzh-Hant", offered)
        self.assertIn("mn-Mong", offered)

    def test_every_offered_language_has_exactly_one_string_catalogue(self):
        basic = json.loads((translations.DATA / "basic-translations.json").read_text())
        for tag in basic:
            self.assertTrue((translations.RES / translations.qualifier_for_tag(tag) / "strings.xml").is_file(), tag)
        for folder in translations.RES.glob("values*"):
            self.assertLessEqual(len(list(folder.glob("strings*.xml"))), 1, str(folder))

    def test_starter_save_translation_is_shared_with_the_unsaved_prompt(self):
        basic = json.loads((translations.DATA / "basic-translations.json").read_text())
        for tag, terms in basic.items():
            strings = translations.read_strings(translations.RES / translations.qualifier_for_tag(tag) / "strings.xml")
            if terms:
                self.assertEqual("@string/ui_save", strings["ui_save_a5d0d9"], tag)
            else:
                self.assertEqual({}, strings, tag)


class GimpTranslationTests(unittest.TestCase):
    def test_selected_entries_preserve_original_po_text_and_context(self):
        snapshot = json.loads((translations.DATA / "gimp-catalogues.json").read_text())
        self.assertEqual("e670132a59be1e8fb98d5b935824e4f57937b4ae", snapshot["revision"])
        self.assertEqual("GPL-3.0-or-later", snapshot["license"])
        self.assertNotIn("tt", snapshot["locale_map"], "GIMP's old Latin Tatar catalogue must not replace the Cyrillic starter locale")
        notices = (translations.RES.parent / "assets/legal/GIMP_TRANSLATION_NOTICES.txt").read_bytes().decode()
        for source in snapshot["sources"]:
            self.assertIn(source["header"], notices)
            self.assertRegex(source["source_sha256"], r"^[0-9a-f]{64}$")
            for entry in source["entries"]:
                parsed = {}; field = None
                for line in entry["raw"].splitlines():
                    if line.startswith(("msgctxt ", "msgid ", "msgstr ")):
                        field, value = line.split(" ", 1); parsed[field] = ast.literal_eval(value)
                    elif line.startswith('"') and field:
                        parsed[field] += ast.literal_eval(line)
                for key in ("msgctxt", "msgid", "msgstr"):
                    self.assertEqual(entry.get(key), parsed.get(key), source["path"])
                self.assertNotRegex(entry["raw"], r"(?m)^#,.*\bfuzzy\b")

    def test_context_mapping_preserves_clipboard_and_flip_meanings(self):
        mapping = json.loads((translations.DATA / "gimp-terms.json").read_text())
        for key in ("ui_cut", "ui_copy", "ui_paste"):
            self.assertEqual("edit-action", mapping[key]["msgctxt"])
        self.assertEqual("Flip _Horizontally", mapping["ui_flip_horizontal"]["msgid"])
        self.assertEqual("Flip _Vertically", mapping["ui_flip_vertical"]["msgid"])
        ja = translations.read_strings(translations.RES / "values-ja/strings.xml")
        self.assertEqual("左右反転", ja["ui_flip_horizontal"])
        self.assertEqual("上下反転", ja["ui_flip_vertical"])
        self.assertEqual("進階…", gimp_translations.adapt("進階(_A)...", "Advanced…"))
        self.assertEqual("Qualité (%)", gimp_translations.adapt("_Qualité:", "Quality (%)", " (%)"))

    def test_coverage_reports_actual_imported_terms_without_claiming_complete_localization(self):
        report = json.loads((translations.DATA / "coverage.json").read_text())
        rows = [r for r in report["coverage"] if r.get("gimp_translation_entries")]
        self.assertGreaterEqual(len(rows), 55)
        self.assertGreater(sum(r["gimp_translation_entries"] for r in rows), 3500)
        for row in rows:
            self.assertLessEqual(row["gimp_translation_entries"], row["gimp_available_entries"])


class KritaTranslationTests(unittest.TestCase):
    def test_selected_entries_preserve_context_notices_and_source_identity(self):
        snapshot = json.loads((translations.DATA / 'krita-catalogues.json').read_text())
        self.assertEqual('428d44705de20770434ea2915021241dc073879c', snapshot['revision'])
        self.assertEqual(14, len(snapshot['audited_sources']))
        notice = (translations.RES.parent / 'assets/legal/KRITA_TRANSLATION_NOTICES.txt').read_text()
        self.assertIn((translations.DATA / 'KRITA-COPYING.txt').read_text(), notice)
        for source in snapshot['sources']:
            self.assertIn(source['header'], notice)
            self.assertRegex(source['blob_sha'], r'^[0-9a-f]{40}$')
            for entry in source['entries']:
                parsed = {}; field = None
                for line in entry['raw'].splitlines():
                    if line.startswith(('msgctxt ', 'msgid ', 'msgstr ')):
                        field, value = line.split(' ', 1); parsed[field] = ast.literal_eval(value)
                    elif line.startswith('"') and field:
                        parsed[field] += ast.literal_eval(line)
                for key in ('msgctxt', 'msgid', 'msgstr'):
                    self.assertEqual(entry.get(key), parsed.get(key), source['path'])
                self.assertNotRegex(entry['raw'], r'(?m)^#,.*\bfuzzy\b')

    def test_new_choices_have_real_vocabulary_and_do_not_invent_empty_catalogues(self):
        options = json.loads((translations.DATA / 'language-options.json').read_text())
        added = {o['tag'] for o in options['options'] if o.get('translation_source') == 'Krita'}
        self.assertEqual({'cy','fy','hne','ia','mai','tok','uz-Latn','wa'}, added)
        report = json.loads((translations.DATA / 'coverage.json').read_text())
        for tag in added:
            row = next(r for r in report['coverage'] if r['language_tag'] == tag)
            self.assertGreater(row['krita_translation_entries'], 0)
            self.assertFalse(row.get('main_menu_complete', False))
        self.assertNotIn('tg', added); self.assertNotIn('uz-Cyrl', added)
        uz = translations.read_strings(translations.RES / 'values-b+uz+Latn/strings.xml')
        self.assertNotRegex(''.join(uz.values()), r'[\u0400-\u04ff]')

    def test_semantic_rejections_and_exact_gap_fill_counts_are_retained(self):
        report = json.loads((translations.DATA / 'coverage.json').read_text())
        for row in report['coverage']:
            if not row.get('krita_gap_fill_keys'):
                continue
            rendered = translations.read_strings(translations.ROOT / row['generated_resource'])
            self.assertLessEqual(row['krita_translation_entries'], row['krita_available_entries'])
            self.assertTrue(set(row['krita_gap_fill_keys']) <= set(rendered))
        af = translations.read_strings(translations.RES / 'values-b+af/strings.xml')
        self.assertNotIn('Driehoek', af.get('ui_rectangle', ''))
        self.assertEqual('保存…', krita_translations.adapt('保存(&S)...', 'Save…'))
        # Existing GIMP/locally reviewed terms have precedence over supplements.
        self.assertEqual('左右反転', translations.read_strings(translations.RES / 'values-ja/strings.xml')['ui_flip_horizontal'])


class MainstreamTranslationTests(unittest.TestCase):
    def test_exact_source_contexts_and_translator_notices_are_preserved(self):
        for project, revision, count, licence in (
            ('libreoffice', '84fc1f3ce6a7d0ff415ac93495ba172b8ce2bac6', 14, 'LIBREOFFICE-COPYING.MPL'),
            ('mediawiki', 'ea83228d5fe2b1f9559196a2716c8580cdb2407d', 8, 'MEDIAWIKI-COPYING.txt'),
        ):
            data = json.loads((translations.DATA / f'{project}-catalogues.json').read_text())
            self.assertEqual(revision, data['revision'])
            self.assertEqual(count, len(data['sources']))
            raw_licence = (translations.DATA / licence).read_bytes()
            self.assertEqual(data['license_blob_sha'], hashlib.sha1(b'blob ' + str(len(raw_licence)).encode() + b'\0' + raw_licence).hexdigest())
            notice = (translations.RES.parent / f'assets/legal/{project.upper()}_TRANSLATION_NOTICES.txt').read_text()
            self.assertIn((translations.DATA / licence).read_text(), notice)
            for source in data['sources']:
                self.assertRegex(source['blob_sha'], r'^[0-9a-f]{40}$')
                self.assertIn(source['blob_sha'], notice)
                if project == 'mediawiki':
                    for author in source['metadata']['authors']:
                        self.assertIn(author, notice)
                    continue
                self.assertIn(source['header'], notice)
                for entry in source['entries']:
                    parsed = {}; field = None
                    for line in entry['raw'].splitlines():
                        if line.startswith(('msgctxt ', 'msgid ', 'msgstr ')):
                            field, value = line.split(' ', 1); parsed[field] = ast.literal_eval(value)
                        elif line.startswith('"') and field:
                            parsed[field] += ast.literal_eval(line)
                    self.assertEqual({k: entry[k] for k in ('msgctxt', 'msgid', 'msgstr')}, parsed)
                    self.assertNotRegex(entry['raw'], r'(?m)^#,.*\bfuzzy\b')

    def test_supplements_preserve_every_existing_translated_label(self):
        after = translations.generate()
        with mock.patch.object(mainstream_translations, 'load', return_value={}):
            before = translations.generate()
        defaults = {}
        for path in (translations.RES / 'values').glob('*.xml'):
            defaults.update(translations.read_strings(path))
        normal = lambda s: s.strip().strip('"').replace("\\'", "'").rstrip(':：').casefold()
        for path, content in before.items():
            if path.name != 'strings.xml':
                continue
            old = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(content)}
            new = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(after[path])}
            for key, value in old.items():
                if normal(value) != normal(defaults.get(key, '')):
                    self.assertEqual(value, new[key], f'{path}/{key}')

    def test_gap_counts_scripts_and_contexts_are_auditable(self):
        report = json.loads((translations.DATA / 'coverage.json').read_text())
        self.assertEqual(135, report['offered_language_count_including_english'])
        for project, total in (('libreoffice', 206), ('mediawiki', 26)):
            self.assertEqual(total, sum(r.get(project + '_translation_entries', 0) for r in report['coverage']))
        mapping = json.loads((translations.DATA / 'libreoffice-terms.json').read_text())
        self.assertIn('Popups..uno:PickList\nLabel', mapping['ui_menu_file']['msgctxt'])
        self.assertIn('Commands..uno:FlipHorizontal\nLabel', mapping['ui_flip_horizontal']['msgctxt'])
        self.assertNotIn('ui_clear', mapping)  # Reset-formatting Clear is not Clear canvas.
        bo = translations.read_strings(translations.RES / 'values-b+bo/strings.xml')
        self.assertEqual('"ཡིག་ཆ།"', bo['ui_menu_file'])
        lo = translations.read_strings(translations.RES / 'values-b+lo/strings.xml')
        self.assertEqual('"ໄຟລ໌"', lo['ui_menu_file'])
        za = translations.read_strings(translations.RES / 'values-b+za/strings.xml')
        self.assertEqual('"Bangcoh"', za['ui_menu_help'])
        uz = translations.read_strings(translations.RES / 'values-b+uz+Latn/strings.xml')
        self.assertNotRegex(''.join(uz.values()), r'[\u0400-\u04ff]')
        self.assertEqual('ཡིག་ཆ།', mainstream_translations.adapt('ཡིག་ཆ།(~F)', 'File', 'libreoffice'))


class TatarScriptTests(unittest.TestCase):
    def test_latin_catalogue_is_derived_from_the_complete_cyrillic_vocabulary(self):
        source = json.loads((translations.DATA / "tatar-transcription.json").read_text())
        basic = json.loads((translations.DATA / "basic-translations.json").read_text())["tt"]
        latin = translations.read_strings(translations.RES / "values-b+tt+Latn/strings.xml")
        self.assertEqual(set(basic.values()), set(source["cyrillic_to_latin"]))
        self.assertEqual("@string/ui_save", latin.pop("ui_save_a5d0d9"))
        self.assertEqual({k: source["cyrillic_to_latin"][v] for k,v in basic.items()}, latin)
        for value in latin.values():
            self.assertNotRegex(value, r"[\u0400-\u04ff]")
        self.assertEqual("Saqlaw", latin["ui_save"])
        self.assertNotEqual(latin["ui_discard_changes23"], latin["ui_keep_editing23"])
        for app_key, upstream_key in source["mapping"].items():
            original = source["original_strings"][upstream_key]
            self.assertEqual(original[0].upper()+original[1:], basic[app_key])

    def test_every_new_gimp_option_has_actual_selected_vocabulary(self):
        options = json.loads((translations.DATA / "language-options.json").read_text())
        report = json.loads((translations.DATA / "coverage.json").read_text())
        added = {o["tag"] for o in options["options"] if o.get("translation_source") == "GIMP"}
        self.assertEqual(20, len(added))
        self.assertEqual("tt-Cyrl", options["aliases"]["tt"])
        self.assertTrue({"tt-Cyrl", "tt-Latn"} <= {o["tag"] for o in options["options"]})
        for tag in added:
            row = next(r for r in report["coverage"] if r["language_tag"] == tag)
            self.assertGreater(row["gimp_translation_entries"], 0, tag)
        self.assertNotIn("kw", added)  # No translated matching term in pinned GIMP Cornish.
