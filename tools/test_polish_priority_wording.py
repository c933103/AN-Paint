"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

MEMORY = 'ui_d_d_pixels_2f_mp_exceeds_the_current'

def display(value):
    """Only strip the ordinary complete Android quotation wrapper used by these inputs."""
    return value[1:-1] if value.startswith('"') and value.endswith('"') else value

class PolishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {
            tag: (catalogues.RES / directory / 'strings.xml').read_text(encoding='utf-8')
            for tag, directory in [('default', 'values'), ('pl', 'values-pl')]
        }
        cls.nodes = {tag: {n.get('name'): n for n in ET.fromstring(xml) if n.tag == 'string'}
                     for tag, xml in cls.xml.items()}
        cls.strings = {tag: {key: ''.join(node.itertext()) for key, node in nodes.items()}
                       for tag, nodes in cls.nodes.items()}

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

    def test_safety_choices_and_discard_alias_remain_distinct(self):
        strings = self.strings['pl']
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual(strings['ui_discard_changes23'], strings['ui_discard'])
        self.assertNotEqual(strings['ui_keep_editing23'], strings['ui_discard'])
        self.assertEqual(3, len({strings[k] for k in ('ui_save', 'ui_discard_changes23', 'ui_keep_editing23')}))

    def test_memory_and_recovery_ownership_distinctions(self):
        strings = self.strings['pl']
        self.assertIn('Nie zastosowano automatycznej zmiany rozmiaru', strings[MEMORY])
        floor = strings['ui_assembly_source_memory_floor']
        self.assertIn('Samo zmniejszenie', floor)
        self.assertIn('Kompozycja pozostaje bez zmian', floor)
        self.assertIn('Oryginalny plik pozostanie bez zmian', strings['ui_the_full_image_and_working_buffers_exceed_the'])
        self.assertIn('kopia odzyskiwania', strings['ui_history_unavailable34'])
        self.assertIn('chronić tę wersję roboczą', strings['ui_autosave_is_paused_to_protect_that_draft_use'])
        self.assertIn('canvas.png', strings['ui_a_separate_recovery_copy_has_been_kept_use'])
        self.assertIn('ZIP', strings['ui_a_separate_recovery_copy_has_been_kept_use'])
        self.assertIn('miejsce zapisu pozostanie bez zmian', strings['ui_share_explanation34'])

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
