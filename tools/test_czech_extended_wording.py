"""Bounded Czech wording and composition contracts, not a fluency/layout certificate."""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET
import current_localization_contracts as contracts
import translation_catalogues as catalogues


def identities(xml):
    return {(e.tag, e.get('name')) for e in ET.fromstring(xml)
            if e.get('translatable') != 'false'}


class CzechExtendedWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = contracts.fixture('czech_extended_wording.json')
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text()
                   for tag, folder in [('default', 'values'), ('cs', 'values-cs')]}
        cls.strings = catalogues.read_strings(catalogues.RES / 'values-cs/strings.xml')

    def test_current_identity_coverage_does_not_silently_accept_held_legacy_manual(self):
        source, target = (identities(self.xml[t]) for t in ('default', 'cs'))
        self.assertEqual({('string', 'ui_the_arrow_on_the_left_directly_below_the')}, source - target)
        self.assertEqual(['ui_the_arrow_on_the_left_directly_below_the'], self.data['held_missing'])
        self.assertFalse(target - source)
        self.assertEqual([], catalogues.validate_catalogue('cs'))
        self.assertEqual('Hlavní', self.strings['ui_main23'])
        self.assertEqual('"Přizpůsobit obrázek oknu"', self.strings['ui_fit'])
        self.assertEqual(31, len(set(self.data['prior_held'])))
        self.assertIn('ui_fit', self.data['prior_held'])
        self.assertIn('ui_foreground_background_colour_palette', self.data['prior_held'])
        self.assertIn('ui_edit_palette23', self.data['additional_context_holds'])
        self.assertEqual(41, len(set(self.data['additional_context_holds'])))

    def test_complete_critical_values_attributes_and_format_contracts(self):
        contracts.require_wording_shape(self.data, set(self.data['values']), {'default', 'cs'})
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    contracts.require_string(self.xml[tag], key, expected, self.data['constraints'][key])

    def test_missing_duplicate_fragment_markup_and_format_mutations_fail(self):
        for key, values in self.data['values'].items():
            node = ET.fromstring(self.xml['cs']).find(f"./string[@name='{key}']")
            for mutation in ('missing', 'duplicate', 'fragment', 'markup', 'format'):
                root = ET.Element('resources'); changed = deepcopy(node)
                if mutation != 'missing': root.append(changed)
                if mutation == 'duplicate': root.append(deepcopy(changed))
                elif mutation == 'fragment': changed.text = changed.text[:-1]
                elif mutation == 'markup': ET.SubElement(changed, 'b').text, changed.text = changed.text, None
                elif mutation == 'format': changed.set('formatted', 'true' if changed.get('formatted') == 'false' else 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    contracts.require_string(ET.tostring(root, encoding='unicode'), key, values['cs'], self.data['constraints'][key])

    def test_czech_one_few_other_keep_complete_conditional_movement_warning(self):
        entry = self.data['plural']
        for tag in ('default', 'cs'):
            nodes = ET.fromstring(self.xml[tag]).findall(f"./plurals[@name='{entry['key']}']")
            self.assertEqual(1, len(nodes)); items = nodes[0].findall('item')
            self.assertEqual(['one', 'few', 'other'] if tag == 'cs' else ['one', 'other'],
                             [n.get('quantity') for n in items])
            self.assertEqual(entry[tag], {n.get('quantity'): n.text for n in items})
            for node in items:
                self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$d': 1}, catalogues.placeholders(node.text))
        for quantity, noun in [('one', 'obrázek'), ('few', 'obrázky'), ('other', 'obrázků')]:
            value = entry['cs'][quantity]
            self.assertIn('%3$d '+noun+'.', value)
            self.assertIn('může posunout obrázky, které jsou k nim připojené.', value)
            self.assertEqual(1, value.count('\\n'))

    def test_live_help_preserves_actual_navigation_and_distinct_save_actions(self):
        s = {k: v.strip('"') for k, v in self.strings.items()}
        help_text = s['ui_help23']
        for key in ('ui_menu_view', 'ui_navigate', 'ui_draw26', 'ui_drawing23', 'ui_category_selection',
                    'ui_category_insert', 'ui_swap23', 'ui_reset_bw23', 'ui_use_colour', 'ui_add_colour26',
                    'ui_advanced', 'ui_pixel_grid33', 'ui_cursor_drawing32', 'ui_about_credits23', 'commons_blank_maps'):
            self.assertIn(s[key], help_text, key)
        navigation = f"{s['ui_menu_file']} → {s['ui_about_credits23']} → {s['ui_image_credits']}"
        for key in ('gallery_description', 'ui_irasutoya_help34', 'ui_openclipart_help34'):
            self.assertIn(navigation, s[key]); self.assertIn(s['gallery_use_image'], s[key])
        self.assertIn(s['gallery_copy_credit'], s['gallery_description'])
        self.assertIn('aniž označí kresbu za uloženou.', help_text)
        self.assertIn('Aktuální cíl příkazu Uložit zůstane zachován.', help_text)
        self.assertIn('obě historie Zpět/Znovu', help_text)
        self.assertEqual('@string/ui_cursor_help31', s['ui_cursor_help29'])

    def test_geometry_and_data_safety_distinctions_are_preserved(self):
        s = self.strings
        self.assertEqual('Barevný kruh', s['ui_wheel'])
        self.assertEqual('Kvalita (%)', s['ui_quality'])
        self.assertIn('Rozměry: %3$s × %4$s px.', s['ui_by_pixels_hold_and_drag_to_place'])
        self.assertIn('Zde je překrývání povoleno;', s['ui_assembly_position_help'])
        self.assertIn('Ostatní obrázky si zachovají aktuální polohu.', s['ui_assembly_position_help'])
        self.assertIn('později importované obrázky se vykreslí navrchu.', s['ui_assembly_position_help'])
        self.assertIn('Ořezy a velikosti zůstanou beze změny.', s['ui_assembly_position_help'])
        self.assertIn('Obrázek nebyl importován.', s['gallery_image_component_unavailable'])
        self.assertIn('může zmenšit soubor beze změny pixelů', s['formats22_tiff_description'])
        self.assertIn('antiAlias=false; strokeDashArray=none; background=#FFFFFF.', s['commons_import_svg_changes'])
        self.assertIn('background=#FFFFFF', s['commons_import_raster_changes'])

    def test_assembly_help_keeps_snapping_and_exact_position_modes_separate(self):
        s = {k: v.strip('"') for k, v in self.strings.items()}
        value = s['ui_add_up_to_20_images_with_android_s']; paragraphs = value.split(r'\n\n')
        self.assertEqual(8, len(paragraphs))
        self.assertIn('Při přichytávání není překrývání povoleno.', paragraphs[2])
        self.assertIn('počínaje nulou', paragraphs[3])
        self.assertIn('Ostatní obrázky si zachovají polohu a překrývání je povoleno.', paragraphs[3])
        self.assertIn('se mohou posunout a vyplnit mezeru', paragraphs[5])
        for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                    'ui_same_width', 'ui_same_height', 'ui_smallest', 'ui_largest',
                    'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all',
                    'ui_save_png', 'ui_edit_in_paint', 'ui_menu_file', 'ui_about_credits23'):
            self.assertIn(s[key], value, key)


if __name__ == '__main__': unittest.main()
