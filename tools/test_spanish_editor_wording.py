"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


MEMORY = "ui_d_d_pixels_2f_mp_exceeds_the_current"
CANVAS = "ui_drawing_canvas_pinch_and_move_two_fingers_to"

class SpanishEditorWordingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = catalogues.catalogue_paths()['es-ES']
        cls.xml = {'es-ES': path.read_text()}
        cls.strings = {'es-ES': catalogues.read_strings(path)}

    def test_memory_warning_preserves_every_safety_clause(self):
        value = self.strings['es-ES'][MEMORY]
        self.assertTrue(value.startswith('Una imagen de %1$d × %2$d px (%3$.2f MP) supera '))
        clauses = (
            'el límite seguro de edición actual de %4$.2f MP.',
            'AN Paint mantiene la imagen completa en memoria y reserva espacio para transformaciones y selecciones.',
            'La memoria disponible determina este límite.',
            'La operación se detuvo antes de asignar el mapa de bits sobredimensionado.',
            'No se aplicó ningún cambio de tamaño automático.',
        )
        for clause in clauses:
            self.assertIn(clause, value)

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

    def test_image_list_gender_and_bidirectional_zoom_keep_navigation_instruction(self):
        strings = self.strings['es-ES']
        self.assertEqual(('Todas', 'Ninguna'), (strings['ui_all'], strings['ui_none']))
        self.assertEqual(
            'Lienzo de dibujo. Pellizca y mueve dos dedos para hacer zoom y desplazar. '
            'El modo Navegar también permite desplazar con un dedo.', strings[CANVAS])

    def test_save_alias_and_distinct_unsaved_change_choices_are_preserved(self):
        strings = self.strings['es-ES']
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual('Guardar', strings['ui_save'])
        self.assertEqual('Descartar cambios', strings['ui_discard_changes23'])
        self.assertEqual('Seguir editando', strings['ui_keep_editing23'])
        self.assertEqual(3, len({strings[key] for key in
                                ('ui_save', 'ui_discard_changes23', 'ui_keep_editing23')}))

if __name__ == '__main__':
    unittest.main()
