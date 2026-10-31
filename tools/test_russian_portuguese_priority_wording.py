"""Current locale semantics; historical approval snapshots live in immutable source history."""
from pathlib import Path
import unittest
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]

CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class RussianPortuguesePriorityWording(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = {tag: catalogues.catalogue_paths()[tag] for tag in ('ru', 'pt-PT')}
        cls.values = {tag: catalogues.read_strings(path) for tag, path in cls.paths.items()}

    def test_category_descriptions_anchor_agreement_to_a_fixed_tool_noun(self):
        # Substitute real category-member labels with differing grammatical genders.
        # This is string composition and static binding, not Android execution.
        cases = {
            'ru': ('Выбранный инструмент:', ('Свернуть', 'Развернуть')),
            'pt-PT': ('Ferramenta selecionada:', ('Recolher', 'Expandir')),
        }
        for tag, (head, actions) in cases.items():
            values = self.values[tag]
            for action, key in zip(actions, ('ui_collapse_tool_category', 'ui_expand_tool_category')):
                for tool_key in ('ui_pencil', 'ui_brush', 'ui_line', 'ui_ellipse', 'ui_text', 'ui_free_form_select', 'ui_rectangle_select'):
                    tool = values[tool_key]
                    category = values['ui_drawing23']
                    text = values[key].replace('%1$s', category).replace('%2$s', tool)
                    with self.subTest(locale=tag, key=key, tool=tool):
                        self.assertIn(head + ' ' + tool + '.', text)
                        self.assertTrue(text.startswith(category + '. '))
                        self.assertIn(action, text)
                        self.assertNotIn('%', text)

    def test_russian_pixel_count_is_a_label_for_every_count_class(self):
        value = self.values['ru']['ui_d_d_px_d_pixels_2f_mp']
        self.assertIn('Число пикселей: %3$,d', value)
        for count in (1, 2, 5, 11, 21, 22, 25, 101, 1001):
            # A deliberately narrow host substitution; Java formatting is not claimed.
            text = value.replace('%1$d', str(count)).replace('%2$d', '1')
            text = text.replace('%3$,d', format(count, ',d')).replace('%4$.2f', format(count / 1_000_000, '.2f'))
            with self.subTest(count=count):
                self.assertIn('Число пикселей: ' + format(count, ',d'), text)
                self.assertNotIn(str(count) + ' пикселей', text)

    def test_russian_memory_warning_does_not_claim_automatic_resize(self):
        value = self.values['ru']['ui_d_d_pixels_2f_mp_exceeds_the_current']
        self.assertIn('памят', value)
        self.assertIn('Автоматическое изменение размера не применялось', value)

    def test_portuguese_canvas_recovery_names_the_actual_undo_command(self):
        values = self.values['pt-PT']
        warning = values['ui_keeps_pixels_at_the_top_left_smaller_canvas']
        self.assertEqual('Desfazer', values['ui_undo'])
        self.assertIn('«' + values['ui_undo'] + '» restaura-os.', warning)
        self.assertIn('canto superior esquerdo', warning)
        self.assertIn('eliminam os píxeis além da margem direita/inferior', warning)
        self.assertNotIn('Anular', warning)
        self.assertIn('UNDO(R.string.ui_undo)', (CLASSIC / 'ActionButton.kt').read_text())
        self.assertIn('ui(R.string.ui_keeps_pixels_at_the_top_left_smaller_canvas)', (CLASSIC / 'ClassicPaintActivity.kt').read_text())

    def test_portuguese_language_note_has_new_or_untranslated_fallback_and_two_line_breaks(self):
        key = 'language20_translation_note'
        value = self.values['pt-PT'][key]
        self.assertIn('O texto novo ou não traduzido aparece em inglês.', value)
        self.assertNotIn('temporariamente', value)
        self.assertEqual(2, value.count(r'\n'))
        self.assertNotIn(r'\\n', value)

    def test_portuguese_zoom_help_preserves_both_directions_pan_and_navigate(self):
        value = self.values['pt-PT']['ui_drawing_canvas_pinch_and_move_two_fingers_to']
        for phrase in ('Afaste ou junte dois dedos', 'ampliar ou reduzir', 'mova-os para deslocar',
                       'O modo Navegar também permite deslocar com um dedo.'):
            self.assertIn(phrase, value)


    def test_portuguese_pixel_spelling_and_composed_accessibility_units(self):
        values = self.values['pt-PT']
        self.assertEqual(('Píxeis', 'píxeis'), (values['ui_pixels'], values['ui_pixels_6ec9c2']))
        for key, expected in (('ui_width_in', 'Largura em píxeis'), ('ui_height_in', 'Altura em píxeis')):
            self.assertEqual(expected, values[key].replace('%1$s', values['ui_pixels_6ec9c2']))

if __name__ == '__main__':
    unittest.main()
