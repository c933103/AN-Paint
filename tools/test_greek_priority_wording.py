"""Greek priority text contracts; static checks, not runtime or fluency certification."""
from collections import Counter
from copy import deepcopy
import json
import re
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

FIXTURE = 'greek_priority_current_wording.json'
RECOVERY = 'ui_recovery_copy_exported_extract_canvas_png_from_the'
QUESTION = 'ui_save_your_changes'
NOTE = 'language20_translation_note'
FILL = 'ui_solid_fill'
KEYS = {RECOVERY, QUESTION, NOTE, FILL}
TAGS = {'default', 'el'}
CLASSIC = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'


class GreekPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture(FIXTURE), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('el', 'values-el')]}
        cls.strings = {tag: {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(xml) if n.tag == 'string'}
                       for tag, xml in cls.xml.items()}
        cls.activity = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')

    def test_complete_bilingual_wording_attributes_and_arguments(self):
        for key, values in self.data['values'].items():
            self.assertEqual(TAGS, set(self.data['constraints'][key]))
            for tag, expected in values.items():
                constraints = self.data['constraints'][key][tag]
                self.assertEqual({'attributes', 'formatted', 'placeholders', 'escaped_newline_count'}, set(constraints))
                self.assertEqual({'name': key}, constraints['attributes'])
                self.assertIs(True, constraints['formatted'])
                self.assertEqual({}, constraints['placeholders'])
                self.assertEqual(Counter(), catalogues.placeholders(expected))
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, expected, constraints)

    def test_fixture_cannot_omit_keys_locales_constraints_or_text(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'constraint', 'empty'):
                changed = deepcopy(self.data)
                if mutation == 'key':
                    del changed['values'][key]
                elif mutation == 'locale':
                    del changed['values'][key]['el']
                elif mutation == 'constraint':
                    del changed['constraints'][key]
                else:
                    changed['values'][key]['el'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, TAGS)

    def test_missing_duplicate_truncated_markup_and_attributes_fail_closed(self):
        for key in KEYS:
            for mutation in ('missing', 'duplicate', 'truncate', 'markup', 'formatted', 'wrong-type'):
                root = ET.fromstring(self.xml['el'])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing':
                    root.remove(node)
                elif mutation == 'duplicate':
                    root.append(deepcopy(node))
                elif mutation == 'truncate':
                    node.text = node.text[:-1]
                elif mutation == 'markup':
                    ET.SubElement(node, 'b').text, node.text = node.text, None
                elif mutation == 'formatted':
                    node.set('formatted', 'false')
                else:
                    node.tag = 'plurals'
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key,
                                   self.data['values'][key]['el'], self.data['constraints'][key]['el'])

    def test_unexpected_arguments_and_invalid_android_escapes_fail(self):
        for key in KEYS:
            for suffix in (' %1$s', " '"):
                root = ET.fromstring(self.xml['el'])
                changed = self.data['values'][key]['el'] + suffix
                root.find(f"./string[@name='{key}']").text = changed
                with self.subTest(key=key, suffix=suffix), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, changed,
                                   self.data['constraints'][key]['el'])

    def test_greek_catalogue_is_complete_and_retains_android_syntax(self):
        self.assertEqual([], catalogues.validate_catalogue('el', require_complete=True))
        for tag, xml in self.xml.items():
            root = ET.fromstring(xml)
            identities = [(n.tag, n.get('name')) for n in root]
            self.assertEqual(len(identities), len(set(identities)))
            for node in root:
                if node.tag == 'string':
                    value = ''.join(node.itertext())
                    with self.subTest(tag=tag, key=node.get('name')):
                        self.assertEqual([], catalogues.android_string_errors(value))
                        self.assertEqual([], catalogues.format_string_errors(value, node.get('formatted') != 'false'))

    def test_save_question_and_actions_are_consistent_in_replacement_dialog(self):
        strings = self.strings['el']
        self.assertEqual('Αποθήκευση των αλλαγών;', strings[QUESTION])
        self.assertEqual('Η τρέχουσα εικόνα έχει μη αποθηκευμένες αλλαγές.', strings['ui_your_current_image_has_unsaved_changes'])
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual('Αποθήκευση', strings['ui_save'])
        self.assertEqual('Απόρριψη αλλαγών', strings['ui_discard_changes23'])
        self.assertEqual('Συνέχεια επεξεργασίας', strings['ui_keep_editing23'])
        self.assertRegex(self.activity, r'fun confirmReplacement\(action: \(\) -> Unit\)')
        self.assertIn('.setTitle(ui(R.string.' + QUESTION + ')).setMessage(ui(R.string.ui_your_current_image_has_unsaved_changes))', self.activity)

    def test_recovery_instruction_names_current_file_open_command(self):
        strings = self.strings['el']
        command = strings['ui_load_image'].rstrip('…')
        self.assertEqual('Άνοιγμα εικόνας', command)
        self.assertEqual('Αρχείο', strings['ui_menu_file'])
        self.assertEqual('Το αντίγραφο ανάκτησης εξήχθη. Εξαγάγετε το canvas.png από το ZIP και ανοίξτε το με '
                         + strings['ui_menu_file'] + ' > ' + command
                         + '. Το ZIP περιέχει επίσης τις ρυθμίσεις του προχείρου και τυχόν αιωρούμενη επιλογή.', strings[RECOVERY])
        self.assertRegex(self.activity, r'"File"->\(listOf[\s\S]*?ui\(R\.string\.ui_load_image\) to \{confirmReplacement \{launchOpen\(false\)\}\}')
        self.assertIn('message(ui(R.string.' + RECOVERY + '))', self.activity)

    def test_language_note_keeps_new_and_untranslated_fallback_without_temporary_promise(self):
        self.assertEqual(r'Γλώσσα εφαρμογής\n\nΟι μεταφράσεις διατηρούνται στους γλωσσικούς πόρους του AN Paint. '
                         'Το νέο ή αμετάφραστο κείμενο εμφανίζεται στα αγγλικά.', self.strings['el'][NOTE])
        self.assertEqual(2, self.strings['el'][NOTE].count('\\n'))
        self.assertNotIn('προσωρινά', self.strings['el'][NOTE])
        picker = (CLASSIC / 'AppLanguage.kt').read_text(encoding='utf-8')
        self.assertIn('text = ui(R.string.' + NOTE + ')', picker)

    def test_shape_style_retains_distinct_outline_solid_and_outline_plus_fill_options(self):
        strings = self.strings['el']
        self.assertEqual(('Περίγραμμα', 'Συμπαγές γέμισμα', 'Γέμισμα + γραμμή'),
                         tuple(strings[key] for key in ('ui_outline', FILL, 'ui_fill_line')))
        self.assertIn('addChoice(listOf(ui(R.string.ui_outline), ui(R.string.' + FILL + '), ui(R.string.ui_fill_line)), document.shapeStyle)', self.activity)

    def test_priority_assignments_unchanged(self):
        data = json.loads((catalogues.ROOT / 'translations/string-importance.json').read_text())
        tiers = {key: group['id'] for group in data['tiers'] for key in group['keys']}
        self.assertEqual({'P0': 92, 'P1': 249}, {tier: sum(value == tier for value in tiers.values()) for tier in ('P0', 'P1')})
        for key in (RECOVERY, QUESTION):
            self.assertEqual('P0', tiers['string/' + key])
        for key in (NOTE, FILL):
            self.assertEqual('P1', tiers['string/' + key])


if __name__ == '__main__':
    unittest.main()
