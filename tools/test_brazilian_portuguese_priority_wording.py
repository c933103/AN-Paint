"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

RECOVERY = 'ui_recovery_copy_exported_extract_canvas_png_from_the'

NOTE = 'language20_translation_note'

COLLAPSE = 'ui_collapse_tool_category'

EXPAND = 'ui_expand_tool_category'

COUNT = 'ui_d_d_px_d_pixels_2f_mp'

GESTURE = 'ui_drawing_canvas_pinch_and_move_two_fingers_to'

NONE = 'ui_none'

UNIT = 'ui_pixels_6ec9c2'

CLASSIC = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class BrazilianPortuguesePriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in {'default': 'values', 'pt-BR': 'values-pt-rBR'}.items()}
        cls.strings = {tag: {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(xml)
                            if n.tag == 'string'} for tag, xml in cls.xml.items()}
        cls.activity = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')

    def test_recovery_names_actual_file_command_and_retains_complete_archive_guidance(self):
        strings = self.strings['pt-BR']
        command = strings['ui_load_image'].rstrip('…')
        self.assertIn(strings['ui_menu_file'] + ' > ' + command, strings[RECOVERY])
        self.assertIn('canvas.png', strings[RECOVERY])
        self.assertIn('ZIP', strings[RECOVERY])
        self.assertIn('configurações do rascunho', strings[RECOVERY])
        self.assertIn('qualquer seleção flutuante', strings[RECOVERY])
        # Recovery-export notification has no independently mapped runtime binding yet.
        self.assertIn('message(ui(R.string.' + RECOVERY + '))', self.activity)

    def test_language_note_retains_both_fallback_cases_and_paragraph_boundary(self):
        value = self.strings['pt-BR'][NOTE]
        self.assertIn('novos ou não traduzidos', value)
        self.assertEqual(2, value.count(r'\n'))

    def test_selected_tool_agreement_uses_fixed_feminine_noun_in_both_states(self):
        for key, verb in ((COLLAPSE, 'Recolher'), (EXPAND, 'Expandir')):
            self.assertEqual('%1$s. Ferramenta selecionada: %2$s. ' + verb + ' ferramentas e opções',
                             self.strings['pt-BR'][key])

    def test_pixel_count_uses_a_count_neutral_head(self):
        self.assertIn('Quantidade de pixels: %3$,d', self.strings['pt-BR'][COUNT])

    def test_gesture_guidance_distinguishes_both_zoom_directions_and_finger_counts(self):
        value = self.strings['pt-BR'][GESTURE]
        for distinction in ('ampliar', 'reduzir', 'dois dedos', 'um dedo'):
            self.assertIn(distinction, value)

    def test_none_matches_image_checklist_and_composed_units_stay_lowercase(self):
        s = self.strings['pt-BR']
        self.assertEqual('pixels', s[UNIT])
        self.assertEqual('Pixels', s['ui_pixels'])

if __name__ == '__main__':
    unittest.main()
