"""Bounded German wording regressions; no device or whole-locale certification."""
from copy import deepcopy
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues
from memory_warning_successors import current_warning_expectation
from test_danish_norwegian_p0_wording import full_format_tokens


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = 'german_priority_current_wording.json'
MEMORY = 'ui_d_d_pixels_2f_mp_exceeds_the_current'
EXPECTED_KEYS = {
    'formats22_animation_unknown',
    'save20_destination_error',
    'ui_cannot_create_the_undo_cache_free_some_device',
    'ui_d_d_pixels_2f_mp_exceeds_the_current',
    'ui_recovery_copy_exported_extract_canvas_png_from_the',
    'ui_share_explanation34',
    'ui_the_image_was_saved_but_android_could_not',
    'ui_the_previous_draft_could_not_be_moved_to',
    'ui_the_trim_would_remove_the_entire_image',
    'colour_truncated_metadata',
    'ui_bg',
    'ui_crop_preview_drag_an_edge_or_corner_drag',
    'ui_draft_pending',
    'ui_drawing_canvas_pinch_and_move_two_fingers_to',
    'ui_enter_a_trim_amount_for_every_edge',
    'ui_enter_all_four_trim_amounts',
    'ui_fg',
    'ui_no_resize_fits_decoder_memory',
    'ui_pixels_6ec9c2',
    'ui_the_picker_returned_no_file_please_choose_the',
    'ui_the_picker_returned_no_files',
    'ui_trim_amounts_must_be_zero_or_greater',
    'ui_trim_amounts_must_fit_inside_each_image_use',
}


def wording():
    return require_wording_shape(fixture(FIXTURE), EXPECTED_KEYS, {'de'})


class GermanPriorityWording(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = catalogues.catalogue_paths()['de']
        cls.xml = cls.path.read_text()
        cls.values = catalogues.read_strings(cls.path)

    def test_complete_wording_attributes_and_typed_arguments(self):
        data = wording()
        defaults, _, _, _ = catalogues.default_resources()
        for key, values in data['values'].items():
            with self.subTest(key=key):
                if key == MEMORY:
                    # Current typed resource and independent semantic clauses below, not copied approval text.
                    node = ET.fromstring(self.xml).find(f"./string[@name='{key}']")
                    self.assertIsNotNone(node)
                    self.assertEqual(data['constraints'][key]['attributes'], node.attrib)
                    self.assertEqual([], list(node))
                    self.assertEqual(full_format_tokens(defaults[key]), full_format_tokens(node.text))
                    continue
                expected = current_warning_expectation(key, 'de', values['de']) if key == 'ui_no_resize_fits_decoder_memory' else values['de']
                actual = require_string(self.xml, key, expected, data['constraints'][key])
                self.assertEqual(catalogues.placeholders(defaults[key]),
                                 catalogues.placeholders(actual))

    def test_fixture_cannot_silently_drop_keys_locales_or_constraints(self):
        original = wording()
        for key in EXPECTED_KEYS - {MEMORY}:
            for mutation in ('missing-key', 'missing-constraint', 'missing-locale', 'empty-text'):
                data = deepcopy(original)
                if mutation == 'missing-key':
                    del data['values'][key]
                elif mutation == 'missing-constraint':
                    del data['constraints'][key]
                elif mutation == 'missing-locale':
                    data['values'][key] = {}
                else:
                    data['values'][key]['de'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(data, EXPECTED_KEYS, {'de'})

    def test_missing_duplicate_truncated_wrong_type_and_attribute_mutations_fail(self):
        data = wording()
        root = ET.fromstring(self.xml)
        for key, values in data['values'].items():
            if key == MEMORY:
                continue  # Generic XML/format tests cover shape; the retired wording is no longer an oracle.
            node = root.find(f"./string[@name='{key}']")
            line = ET.tostring(node, encoding='unicode')
            changed_attribute = deepcopy(node)
            changed_attribute.set('formatted', 'true' if node.get('formatted') == 'false' else 'false')
            changed_type = deepcopy(node)
            typed = list(catalogues.placeholders(values['de']))
            if typed:
                token = typed[0]
                replacement = token[:-1] + ('d' if token[-1] != 'd' else 's')
                changed_type.text = changed_type.text.replace(token, replacement, 1)
            else:
                changed_type.text += ' %1$d'
            cases = {
                'missing': '',
                'duplicate': line + line,
                'truncated': line.replace(values['de'][-1] + '</string>', '</string>'),
                'wrong-type': ET.tostring(changed_type, encoding='unicode'),
                'wrong-attribute': ET.tostring(changed_attribute, encoding='unicode'),
            }
            for mutation, broken in cases.items():
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string('<resources>' + broken + '</resources>',
                                   key, current_warning_expectation(key, 'de', values['de']) if key == 'ui_no_resize_fits_decoder_memory' else values['de'], data['constraints'][key])

    def test_german_catalogue_is_complete_and_has_unique_resource_names(self):
        root = ET.fromstring(self.xml)
        identities = [(node.tag, node.get('name')) for node in root]
        self.assertEqual(len(identities), len(set(identities)))
        self.assertEqual([], catalogues.validate_catalogue('de', require_complete=True))
        for node in root.findall('string'):
            value = ''.join(node.itertext())
            with self.subTest(key=node.get('name')):
                self.assertEqual([], catalogues.android_string_errors(value))
                self.assertEqual([], catalogues.format_string_errors(
                    value, node.get('formatted') != 'false'))

    def test_pixel_unit_is_declined_only_in_width_and_height_descriptions(self):
        self.assertEqual('Pixel', self.values['ui_pixels'])
        self.assertEqual('Pixeln', self.values['ui_pixels_6ec9c2'])
        for key, label in (('ui_width_in', 'Breite'), ('ui_height_in', 'Höhe')):
            template = self.values[key]
            self.assertEqual(label + ' in %1$s', template)
            self.assertEqual(label + ' in Pixeln', template.replace('%1$s', self.values['ui_pixels_6ec9c2']))
            self.assertEqual(label + ' in Prozent', template.replace('%1$s', self.values['ui_percent_fd8671']))
        # Static consumer binding, not an assertion of Android runtime behavior.
        source = (ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt').read_text()
        self.assertIn('listOf(ui(R.string.ui_pixels), ui(R.string.ui_percent))', source)
        for key in ('ui_width_in', 'ui_height_in'):
            self.assertIn('ui(R.string.' + key + ', if (percent) ui(R.string.ui_percent_fd8671) '
                          'else ui(R.string.ui_pixels_6ec9c2))', source)

    def test_foreground_background_abbreviations_remain_distinct_two_character_labels(self):
        self.assertEqual(('VG', 'HG'), (self.values['ui_fg'], self.values['ui_bg']))
        self.assertEqual([2, 2], [len(self.values[key]) for key in ('ui_fg', 'ui_bg')])

    def test_safety_and_accessibility_clauses_are_retained_in_full(self):
        clauses = {
            'formats22_animation_unknown': [
                'AN Paint öffnet nur ein Standbild und erhält keine Animation.',
            ],
            'ui_d_d_pixels_2f_mp_exceeds_the_current': [
                'AN Paint hält das vollständige Bild im Speicher und reserviert Platz für Transformationen und Auswahlen.',
                'Der verfügbare Speicher bestimmt dieses Limit.',
                'Der Vorgang wurde gestoppt, bevor die übergroße Bitmap angelegt wurde.',
                'Es wurde keine automatische Größenänderung vorgenommen.',
            ],
            'ui_no_resize_fits_decoder_memory': [
                'Brechen Sie ab und verwenden Sie ein kleineres Quellbild.',
            ],
            'ui_recovery_copy_exported_extract_canvas_png_from_the': [
                'canvas.png', 'ZIP-Datei', 'öffnen Sie dieses Bild über Datei > Bild laden',
                'Die ZIP-Datei enthält auch Entwurfseinstellungen und eine eventuell schwebende Auswahl.',
            ],
            'ui_share_explanation34': [
                'Das bisherige Speicherziel bleibt unverändert.',
            ],
            'ui_drawing_canvas_pinch_and_move_two_fingers_to': [
                'zwei Finger auseinander oder zusammen',
                'Im Navigationsmodus können Sie die Ansicht auch mit einem Finger verschieben.',
            ],
        }
        data = wording()
        for key, required in clauses.items():
            for clause in required:
                with self.subTest(key=key, clause=clause):
                    self.assertIn(clause, self.values[key])
                    if key == MEMORY:
                        continue  # Clauses are independent semantics, not a new whole-message freeze.
                    node = ET.Element('string', data['constraints'][key]['attributes'])
                    node.text = self.values[key].replace(clause, '', 1)
                    with self.assertRaises(ValueError):
                        require_string('<resources>' + ET.tostring(node, encoding='unicode') + '</resources>',
                                       key, current_warning_expectation(key, 'de', data['values'][key]['de']) if key == 'ui_no_resize_fits_decoder_memory' else data['values'][key]['de'], data['constraints'][key])


if __name__ == '__main__':
    unittest.main()
