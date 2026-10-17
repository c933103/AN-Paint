"""Bounded Finnish full-value contracts; actual consumers have Robolectric tests."""
from copy import deepcopy
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

KEYS = {'language20_translation_note', 'ui_width_in', 'ui_percent_fd8671', 'ui_d_d_px_d_pixels_2f_mp', 'ui_height_in', 'ui_the_encoder_did_not_finish', 'ui_pixels_6ec9c2'}

class FinnishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('finnish_priority_current_wording.json'), KEYS, {'default', 'fi'})
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text() for tag, path in [('default', 'values'), ('fi', 'values-fi')]}
        cls.strings = {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(cls.xml['fi']) if n.tag == 'string'}

    def test_complete_values_attributes_and_syntax(self):
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, expected, self.data['constraints'][key])

    def test_missing_keys_locales_and_constraints_fail_closed(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'constraint', 'empty'):
                changed = deepcopy(self.data)
                if mutation == 'key': del changed['values'][key]
                elif mutation == 'locale': del changed['values'][key]['fi']
                elif mutation == 'constraint': del changed['constraints'][key]
                else: changed['values'][key]['fi'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, {'default', 'fi'})

    def test_old_complete_values_and_structural_mutations_are_rejected(self):
        old = {'ui_the_encoder_did_not_finish': 'Kooderi ei valmistunut.', 'language20_translation_note': 'Tämä kieliversio sisältää kaikki AN Paintin käännettävät käyttöliittymätekstit.', 'ui_d_d_px_d_pixels_2f_mp': '%1$d × %2$d px · %3$,d pikseliä (%4$.2f MP)', 'ui_height_in': 'Korkeus yksikössä %1$s', 'ui_width_in': 'Leveys yksikössä %1$s', 'ui_pixels_6ec9c2': 'pikseliä', 'ui_percent_fd8671': 'prosentti'}
        for key in KEYS:
            for mutation in ('old', 'missing', 'duplicate', 'truncated', 'markup', 'format-flag'):
                root = ET.fromstring(self.xml['fi']); node = root.find(f"./string[@name='{key}']")
                if mutation == 'old': node.text = old[key]
                elif mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                else: node.set('formatted', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, self.data['values'][key]['fi'], self.data['constraints'][key])

    def test_encoder_failure_names_unfinished_operation(self):
        self.assertEqual('Kooderi ei suorittanut koodausta loppuun.', self.strings['ui_the_encoder_did_not_finish'])
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        for filename in ('ImageExporter.kt', 'TextImageCodec.kt', 'IcoCodec.kt'):
            with self.subTest(filename=filename):
                text = (classic / filename).read_text()
                self.assertIn('compress(', text)
                self.assertIn('throw IOException(ui(R.string.ui_the_encoder_did_not_finish))', text)

    def test_unit_compositions_and_standalone_labels(self):
        self.assertEqual(('Pikselit', 'Prosentti'), (self.strings['ui_pixels'], self.strings['ui_percent']))
        for key, noun in [('ui_width_in', 'Leveys'), ('ui_height_in', 'Korkeus')]:
            for unit, expected in [('ui_pixels_6ec9c2', 'pikseleinä'), ('ui_percent_fd8671', 'prosentteina')]:
                self.assertEqual(noun + ' ' + expected, self.strings[key].replace('%1$s', self.strings[unit]))
        self.assertEqual(('Leveys (%1$s)', 'Korkeus (%1$s)'), (self.strings['ui_width'], self.strings['ui_height']))

    def test_count_neutral_summary_and_truthful_fallback_note(self):
        self.assertEqual('%1$d × %2$d px · Pikselimäärä: %3$,d (%4$.2f MP)', self.strings['ui_d_d_px_d_pixels_2f_mp'])
        self.assertEqual(self.data['values']['language20_translation_note']['fi'], self.strings['language20_translation_note'])
        self.assertNotIn('sisältää kaikki', self.strings['language20_translation_note'])

    def test_full_catalogue_and_existing_uncertainties_remain(self):
        self.assertEqual([], catalogues.validate_catalogue('fi', require_complete=True))
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertEqual('Tallenna', self.strings['ui_save'])
        self.assertEqual('Etuala %1$s, tausta %2$s. Väripaletti %3$s.', self.strings['ui_foreground_background_colour_palette'])
        self.assertEqual(('ET', 'TA'), (self.strings['ui_fg'], self.strings['ui_bg']))
        self.assertEqual('Luonnosta tallennetaan. Yritä hetken kuluttua uudelleen.', self.strings['ui_the_draft_is_saving_try_again_shortly'])

if __name__ == '__main__': unittest.main()
