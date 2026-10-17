"""Polish priority draft regression contracts; independent linguistic review is separate."""
from collections import Counter
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string
import translation_catalogues as catalogues

KEYS = set('''save20_file_format ui_keep_editing23 ui_background_colour
ui_foreground_colour ui_pixels_6ec9c2 ui_solid_fill formats22_animation_message
formats22_animation_poster formats22_animation_still formats22_animation_unknown
formats22_at_least_frames ui_share_explanation34
ui_a_separate_recovery_copy_has_been_kept_use
ui_autosave_is_paused_to_protect_that_draft_use
ui_d_d_pixels_2f_mp_exceeds_the_current
ui_the_full_image_and_working_buffers_exceed_the ui_codec_resize_memory_floor
ui_no_resize_fits_decoder_memory ui_history_unavailable34 ui_height_in ui_width_in
ui_percent_fd8671 ui_pixels ui_percent ui_expand_tool_category
ui_collapse_tool_category ui_drawing_canvas_pinch_and_move_two_fingers_to
ui_paste_hint34 ui_trim_amounts_must_be_zero_or_greater
ui_trim_amounts_must_fit_inside_each_image_use ui_the_trim_would_remove_the_entire_image
ui_trim_expand_canvas_by_touch'''.split())
TAGS = {'default', 'pl'}
FIXTURE = 'polish_priority_draft_wording.json'
MEMORY = 'ui_d_d_pixels_2f_mp_exceeds_the_current'


def require_family(data):
    if data.get('schema_version') != 1 or set(data.get('values', {})) != KEYS:
        raise ValueError('Polish draft message inventory differs')
    if set(data.get('constraints', {})) != KEYS:
        raise ValueError('Polish draft constraints are incomplete')
    for key in KEYS:
        if set(data['values'][key]) != TAGS or set(data['constraints'][key]) != TAGS:
            raise ValueError('Polish draft locale inventory differs: ' + key)
        for tag in TAGS:
            if not isinstance(data['values'][key][tag], str) or not data['values'][key][tag]:
                raise ValueError('Empty Polish draft wording: ' + key)
            if set(data['constraints'][key][tag]) != {'attributes', 'formatted', 'placeholders'}:
                raise ValueError('Polish draft constraint fields differ: ' + key)
    return data


def display(value):
    """Only strip the ordinary complete Android quotation wrapper used by these inputs."""
    return value[1:-1] if value.startswith('"') and value.endswith('"') else value


class PolishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_family(fixture(FIXTURE))
        cls.xml = {
            tag: (catalogues.RES / directory / 'strings.xml').read_text(encoding='utf-8')
            for tag, directory in [('default', 'values'), ('pl', 'values-pl')]
        }
        cls.nodes = {tag: {n.get('name'): n for n in ET.fromstring(xml) if n.tag == 'string'}
                     for tag, xml in cls.xml.items()}
        cls.strings = {tag: {key: ''.join(node.itertext()) for key, node in nodes.items()}
                       for tag, nodes in cls.nodes.items()}

    def test_complete_wording_attributes_and_typed_placeholders(self):
        for key in KEYS:
            for tag in TAGS:
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, self.data['values'][key][tag],
                                   self.data['constraints'][key][tag])
            self.assertEqual(catalogues.placeholders(self.data['values'][key]['default']),
                             catalogues.placeholders(self.data['values'][key]['pl']), key)

    def test_fixture_rejects_missing_key_locale_wording_and_constraints(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'empty', 'constraint'):
                data = deepcopy(self.data)
                if mutation == 'key':
                    del data['values'][key]
                elif mutation == 'locale':
                    del data['values'][key]['pl']
                elif mutation == 'empty':
                    data['values'][key]['pl'] = ''
                else:
                    del data['constraints'][key]['pl']
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_family(data)

    def test_changed_missing_duplicate_or_markup_messages_are_rejected(self):
        for key in KEYS:
            for mutation in ('truncate', 'missing', 'duplicate', 'markup', 'attribute'):
                root = ET.fromstring(self.xml['pl'])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'truncate':
                    node.text = node.text[:-1]
                elif mutation == 'missing':
                    root.remove(node)
                elif mutation == 'duplicate':
                    root.append(deepcopy(node))
                elif mutation == 'markup':
                    child = ET.SubElement(node, 'b')
                    child.text, node.text = node.text, None
                else:
                    node.set('translatable', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key,
                                   self.data['values'][key]['pl'], self.data['constraints'][key]['pl'])

    def test_placeholder_type_precision_loss_and_unescaped_apostrophes_are_rejected(self):
        expected = self.strings['pl'][MEMORY]
        for value in (expected.replace('%1$d', '%1$s'), expected.replace('%3$.2f', '%3$f'),
                      expected.replace('%4$.2f', ''), expected + " '"):
            root = ET.fromstring(self.xml['pl'])
            root.find(f"./string[@name='{MEMORY}']").text = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                require_string(ET.tostring(root, encoding='unicode'), MEMORY, value,
                               self.data['constraints'][MEMORY]['pl'])

    def test_priority_inventory_present_and_catalogue_syntax_valid(self):
        # Completeness is only the current manifest's priority subset, not all Polish strings.
        manifest = json.loads((catalogues.ROOT / 'translations/string-importance.json').read_text())
        priority = {key.split('/', 1)[1] for tier in manifest['tiers'] if tier['id'] in {'P0', 'P1'}
                    for key in tier['keys']}
        self.assertFalse(priority - self.strings['pl'].keys())
        self.assertEqual([], catalogues.validate_catalogue('pl', require_complete=False))
        root = ET.fromstring(self.xml['pl'])
        identities = [(node.tag, node.get('name')) for node in root]
        self.assertEqual(len(identities), len(set(identities)))
        for node in root.findall('string'):
            value = ''.join(node.itertext())
            with self.subTest(key=node.get('name')):
                self.assertEqual([], catalogues.android_string_errors(value))
                self.assertEqual([], catalogues.format_string_errors(value, node.get('formatted') != 'false'))
                key = node.get('name')
                if not value.startswith('@string/'):
                    self.assertEqual(catalogues.placeholders(self.strings['default'][key]),
                                     catalogues.placeholders(value))

    def test_dimension_units_compose_in_locative_both_axes(self):
        strings = self.strings['pl']
        self.assertEqual('piksele', display(strings['ui_pixels']))
        self.assertEqual('Procenty', strings['ui_percent'])
        for key, label in (('ui_width_in', 'Szerokość'), ('ui_height_in', 'Wysokość')):
            for unit_key, unit in (('ui_pixels_6ec9c2', 'pikselach'), ('ui_percent_fd8671', 'procentach')):
                with self.subTest(key=key, unit=unit):
                    self.assertEqual(f'{label} w {unit}',
                                     strings[key].replace('%1$s', display(strings[unit_key])))

    def test_animation_count_composes_without_numeral_agreement_or_english_fallback(self):
        strings = self.strings['pl']
        for count in (2, 5, 21, 22, 100):
            for value in (str(count), strings['formats22_at_least_frames'].replace('%1$d', str(count))):
                composed = strings['formats22_animation_message'].replace('%1$s', 'GIF').replace('%2$s', value)
                self.assertEqual(f'Liczba klatek w tym pliku GIF: {value}. '
                                 'AN Paint edytuje obrazy nieruchome i nie zachowuje animacji.', composed)
        self.assertIn('zamiast klatek animacji', strings['formats22_animation_poster'])
        self.assertIn('tylko pierwsza klatka', strings['formats22_animation_still'])
        self.assertIn('nie zachowa żadnej animacji', strings['formats22_animation_unknown'])

    def test_dynamic_tool_gender_is_avoided_by_named_head(self):
        strings = self.strings['pl']
        for key, action in (('ui_expand_tool_category', 'Rozwiń'), ('ui_collapse_tool_category', 'Zwiń')):
            for tool_key in ('ui_brush', 'ui_eraser', 'ui_rectangle_select'):
                tool = display(strings[tool_key])
                value = strings[key].replace('%1$s', strings['ui_drawing23']).replace('%2$s', tool)
                self.assertEqual(f'Narzędzia rysowania. Wybrane narzędzie: {tool}. {action} narzędzia i opcje', value)

    def test_safety_choices_alias_and_preserved_uncertain_values(self):
        strings = self.strings['pl']
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual(('Zapisz', 'Odrzuć zmiany', 'Kontynuuj edycję'),
                         tuple(strings[k] for k in ('ui_save', 'ui_discard_changes23', 'ui_keep_editing23')))
        for key, expected in {'ui_discard': 'Odrzuć zmiany', 'ui_fit_image': '"Cały obraz w\u00a0oknie"',
                              'ui_main23': 'Główne', 'ui_swap_foreground_background': '"Zamień kolory"'}.items():
            self.assertEqual(expected, strings[key])
        self.assertEqual(('Pierwszy plan', 'Tło'), (strings['ui_fg'], strings['ui_bg']))

    def test_memory_recovery_and_original_file_guarantees_are_complete(self):
        strings = self.strings['pl']
        for clause in ('%1$d × %2$d px (%3$.2f MP)', '%4$.2f MP.',
                       'przechowuje cały obraz w pamięci', 'przekształcenia oraz zaznaczenia',
                       'Ten limit zależy od dostępnej pamięci.',
                       'przed przydzieleniem pamięci na zbyt dużą bitmapę',
                       'Nie zastosowano automatycznej zmiany rozmiaru.'):
            self.assertIn(clause, strings[MEMORY])
        self.assertIn('Oryginalny plik pozostanie bez zmian.', strings['ui_the_full_image_and_working_buffers_exceed_the'])
        self.assertIn('jako kopia odzyskiwania', strings['ui_history_unavailable34'])
        self.assertIn('aby chronić tę wersję roboczą', strings['ui_autosave_is_paused_to_protect_that_draft_use'])
        self.assertIn('canvas.png', strings['ui_a_separate_recovery_copy_has_been_kept_use'])
        self.assertIn('ZIP', strings['ui_a_separate_recovery_copy_has_been_kept_use'])
        self.assertIn('Bieżące miejsce zapisu pozostanie bez zmian.', strings['ui_share_explanation34'])

    def test_route_labels_and_pan_zoom_distinctions_match(self):
        strings = self.strings['pl']
        route = ' → '.join(strings[key] for key in ('ui_draw26', 'ui_category_insert', 'ui_other_images34'))
        self.assertIn(route, strings['ui_paste_hint34'])
        canvas = strings['ui_drawing_canvas_pinch_and_move_two_fingers_to']
        self.assertIn('Zbliżaj lub rozsuwaj dwa palce', canvas)
        self.assertIn(f'Tryb „{strings["ui_navigate"]}”', canvas)
        self.assertIn('jednym palcem', canvas)
        self.assertEqual('Jednolite wypełnienie', strings['ui_solid_fill'])
        self.assertNotEqual(strings['ui_outline'], strings['ui_solid_fill'])


if __name__ == '__main__':
    unittest.main()
