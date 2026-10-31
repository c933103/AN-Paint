"""Current resource semantics; historical approval snapshots are not active text freezes."""
import unittest
import translation_catalogues as catalogues

MEMORY = "ui_d_d_pixels_2f_mp_exceeds_the_current"
CANVAS = "ui_drawing_canvas_pinch_and_move_two_fingers_to"

class SpanishEditorWordingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = catalogues.catalogue_paths()['es-ES']
        cls.xml = {'es-ES': path.read_text()}
        cls.strings = {'es-ES': catalogues.read_strings(path)}

    def test_memory_warning_does_not_claim_automatic_resize(self):
        value = self.strings['es-ES'][MEMORY]
        self.assertIn('memoria', value)
        self.assertIn('No se aplicó', value)
        self.assertIn('automático', value)

    def test_feminine_and_masculine_tool_names_have_an_explicit_grammatical_head(self):
        strings = self.strings['es-ES']
        for tool_key, tool_name in (('ui_eraser', 'Goma de borrar'),
                                    ('ui_rectangle_select', 'Selección rectangular'),
                                    ('ui_pencil', 'Lápiz')):
            self.assertEqual(tool_name, strings[tool_key])
            for key, action in (('ui_expand_tool_category', 'Expandir'),
                                ('ui_collapse_tool_category', 'Contraer')):
                # A host text composition, not an Android/TalkBack execution claim.
                composed = strings[key].replace('%1$s', strings['ui_category_brush']).replace('%2$s', tool_name)
                with self.subTest(key=key, tool=tool_name):
                    self.assertEqual(
                        f'Pincel. Herramienta seleccionada: {tool_name}. {action} herramientas y opciones',
                        composed)

    def test_image_list_choices_keep_feminine_agreement(self):
        strings = self.strings['es-ES']
        self.assertEqual(('Todas', 'Ninguna'), (strings['ui_all'], strings['ui_none']))

    def test_save_alias_and_distinct_unsaved_change_choices_are_preserved(self):
        strings = self.strings['es-ES']
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual(3, len({strings[key] for key in
                                ('ui_save', 'ui_discard_changes23', 'ui_keep_editing23')}))

if __name__ == '__main__':
    unittest.main()
