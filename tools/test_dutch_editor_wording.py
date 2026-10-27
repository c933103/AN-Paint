"""Bounded Dutch text/resource contracts; no Android or native-fluency claim."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues
from memory_warning_source_review import current_source_expectation
from galician_priority_expectations import wording_successor

FIXTURE = 'dutch_editor_current_wording.json'
MEMORY = 'ui_d_d_pixels_2f_mp_exceeds_the_current'
RESIZE = 'ui_the_full_image_and_working_buffers_exceed_the'
COUNT = 'ui_d_d_px_d_pixels_2f_mp'
NOTE = 'language20_translation_note'
KEYS = {MEMORY, RESIZE, COUNT, NOTE, 'ui_the_encoder_did_not_finish',
        'ui_ellipse', 'ui_pixels_6ec9c2'}
TAGS = {'default', 'nl'}


class DutchEditorWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture(FIXTURE), KEYS, TAGS)
        cls.xml = {
            'default': (catalogues.RES / 'values/strings.xml').read_text(encoding='utf-8'),
            'nl': (catalogues.RES / 'values-nl/strings.xml').read_text(encoding='utf-8'),
        }
        cls.strings = {
            tag: {node.get('name'): ''.join(node.itertext()) for node in ET.fromstring(xml)
                  if node.tag == 'string'}
            for tag, xml in cls.xml.items()
        }

    def test_complete_wording_attributes_and_typed_placeholders(self):
        for key, values in self.data['values'].items():
            constraints = self.data['constraints'][key]
            self.assertEqual({'attributes', 'placeholders', 'formatted'}, set(constraints))
            self.assertEqual({'name': key}, constraints['attributes'])
            self.assertIs(True, constraints['formatted'])
            self.assertEqual(catalogues.placeholders(values['default']),
                             Counter(constraints['placeholders']), key)
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, current_source_expectation(key,tag,expected), constraints)

    def test_fixture_requires_all_seven_keys_locales_and_constraints(self):
        for key in KEYS:
            for mutation in ('missing-key', 'missing-locale', 'empty-text', 'missing-constraint'):
                changed = deepcopy(self.data)
                if mutation == 'missing-key':
                    del changed['values'][key]
                elif mutation == 'missing-locale':
                    del changed['values'][key]['nl']
                elif mutation == 'empty-text':
                    changed['values'][key]['nl'] = ''
                else:
                    del changed['constraints'][key]
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, TAGS)

    def test_truncation_duplicates_missing_entries_attributes_and_markup_fail_closed(self):
        for key in KEYS:
            expected = current_source_expectation(key,'nl',self.data['values'][key]['nl'])
            constraints = self.data['constraints'][key]
            for mutation in ('truncate', 'duplicate', 'missing', 'format-flag', 'markup'):
                root = ET.fromstring(self.xml['nl'])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'truncate':
                    node.text = node.text[:-1]
                elif mutation == 'duplicate':
                    root.append(deepcopy(node))
                elif mutation == 'missing':
                    root.remove(node)
                elif mutation == 'format-flag':
                    node.set('formatted', 'false')
                else:
                    child = ET.SubElement(node, 'b')
                    child.text, node.text = node.text, None
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, expected, constraints)

    def test_placeholder_loss_type_precision_and_apostrophe_mutations_are_rejected(self):
        for key in (MEMORY, COUNT):
            expected = current_source_expectation(key,'nl',self.data['values'][key]['nl'])
            constraints = self.data['constraints'][key]
            mutations = [expected.replace('%1$d', '%1$s'),
                         expected.replace('%1$d', ''), expected + " '"]
            if key == MEMORY:
                mutations.append(expected.replace('%3$.2f', '%3$f'))
            else:
                mutations.append(expected.replace('%3$,d', '%3$d'))
            for changed in mutations:
                root = ET.fromstring(self.xml['nl'])
                root.find(f"./string[@name='{key}']").text = changed
                # Matching altered text must not bypass syntax/typed-argument checks.
                with self.subTest(key=key, changed=changed), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, changed, constraints)

    def test_complete_dutch_catalogue_and_android_string_syntax(self):
        self.assertEqual([], catalogues.validate_catalogue('nl', require_complete=True))
        for tag, xml in self.xml.items():
            root = ET.fromstring(xml)
            identities = [(node.tag, node.get('name')) for node in root]
            self.assertEqual(len(identities), len(set(identities)))
            for node in root.findall('string'):
                value = ''.join(node.itertext())
                with self.subTest(locale=tag, key=node.get('name')):
                    self.assertEqual([], catalogues.android_string_errors(value))
                    self.assertEqual([], catalogues.format_string_errors(value, node.get('formatted') != 'false'))

    def test_all_memory_warning_clauses_are_kept_and_allocation_names_memory(self):
        value = self.strings['nl'][MEMORY]
        clauses = (
            '%1$d × %2$d pixels (%3$.2f MP) overschrijdt de huidige veilige bewerkingslimiet van %4$.2f MP.',
            'AN Paint houdt de volledige afbeelding in het geheugen en reserveert ruimte voor transformaties en selecties.',
            'Het beschikbare geheugen bepaalt deze limiet.',
            'De bewerking is gestopt voordat er geheugen voor de te grote bitmap werd toegewezen.',
            'Er is niet automatisch verkleind.',
        )
        self.assertEqual(' '.join(clauses), self.data['values'][MEMORY]['nl'])
        self.assertEqual(wording_successor('nl',MEMORY,' '.join(clauses)),value)
        clauses=(clauses[0].replace('pixels','px',1),)+clauses[1:]
        self.assertEqual(' '.join(clauses),value)
        for clause in clauses:
            root = ET.fromstring(self.xml['nl'])
            root.find(f"./string[@name='{MEMORY}']").text = value.replace(clause, '')
            with self.subTest(omitted=clause), self.assertRaises(ValueError):
                require_string(ET.tostring(root, encoding='unicode'), MEMORY, value,
                               self.data['constraints'][MEMORY])

    def test_resize_reason_keeps_both_causes_copy_target_and_unchanged_original(self):
        value = self.strings['nl'][RESIZE]
        self.assertEqual(
            'De volledige afbeelding en werkbuffers overschrijden de huidige veilige geheugenlimiet, '
            'of Android kon er geen geheugen voor toewijzen. '
            'Wijzig het formaat van een kopie om deze te bewerken. '
            'Uw oorspronkelijke bestand blijft ongewijzigd.', value)

    def test_language_note_explains_maintenance_and_english_fallback_without_claiming_completeness(self):
        value = self.strings['nl'][NOTE]
        self.assertEqual(
            'App-taal\\n\\nVertalingen worden onderhouden in de taalbestanden van AN Paint. '
            'Nieuwe of onvertaalde tekst verschijnt in het Engels.', value)
        self.assertEqual(2, value.count('\\n'))
        self.assertNotIn('alle vertaalbare interfacetekst', value)

    def test_encoder_reports_unfinished_operation(self):
        self.assertEqual('De encoder heeft de bewerking niet voltooid.',
                         self.strings['nl']['ui_the_encoder_did_not_finish'])

    def test_ellipse_is_a_drawing_tool_and_is_distinct_from_selection(self):
        strings = self.strings['nl']
        self.assertEqual('Ellips', strings['ui_ellipse'])
        self.assertEqual(('Rechthoekige selectie', 'Vrije selectie'),
                         (strings['ui_rectangle_select'], strings['ui_free_form_select']))
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        document = (classic / 'PaintDocument.kt').read_text()
        categories = (classic / 'ToolCategoryButton.kt').read_text()
        self.assertRegex(document, r'ELLIPSE\(R\.string\.ui_ellipse\s*,')
        insert = re.search(r'INSERT\(R\.string\.ui_category_insert,listOf\((.*?)\)\)', categories, re.S)
        self.assertIsNotNone(insert)
        self.assertIn('PaintTool.ELLIPSE', insert.group(1))
        self.assertNotIn('PaintTool.SELECT', insert.group(1))

    def test_count_label_is_number_neutral_and_unit_labels_compose_in_lowercase(self):
        strings = self.strings['nl']
        self.assertEqual('%1$d × %2$d px · Aantal pixels: %3$,d (%4$.2f MP)', strings[COUNT])
        self.assertEqual('pixels', strings['ui_pixels_6ec9c2'])
        # Host-side text composition, not Android/TalkBack execution.
        for key, expected in (('ui_width_in', 'Breedte in pixels'),
                              ('ui_height_in', 'Hoogte in pixels')):
            self.assertEqual(expected, strings[key].replace('%1$s', strings['ui_pixels_6ec9c2']))

    def test_existing_save_choices_colour_abbreviations_and_prior_memory_text_are_preserved(self):
        strings = self.strings['nl']
        self.assertEqual(('Opslaan', 'Wijzigingen verwerpen', 'Doorgaan met bewerken'),
                         tuple(strings[k] for k in ('ui_save_a5d0d9', 'ui_discard_changes23', 'ui_keep_editing23')))
        self.assertEqual(('VG', 'AG'), (strings['ui_fg'], strings['ui_bg']))
        self.assertEqual(
            'De schattingen omvatten het huidige canvas en klembord, decodering met subsampling en bewerkingsbuffers. '
            'Het werkelijke geheugengebruik varieert. Een kleinere kopie verliest detail. '
            'Het oorspronkelijke bestand blijft ongewijzigd.', strings['ui_sampled_resize_memory_explanation'])

    def test_unresolved_palette_main_remain_unchanged_and_swap_has_exact_wording_only_successor(self):
        strings = self.strings['nl']
        self.assertEqual('Voorgrond %1$s, achtergrond %2$s. Kleurenpalet %3$s.',
                         strings['ui_foreground_background_colour_palette'])
        self.assertEqual('Start', strings['ui_main23'])
        self.assertEqual(wording_successor('nl','ui_swap_foreground_background','Kleuren wisselen'), strings['ui_swap_foreground_background'])


if __name__ == '__main__':
    unittest.main()
