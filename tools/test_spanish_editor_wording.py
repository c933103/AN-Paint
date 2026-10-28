"""Bounded es-ES wording contracts; no Android, layout or fluency certification."""
from collections import Counter
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues


KEYS = {
    'colour_truncated_metadata',
    'ui_all',
    'ui_collapse_tool_category',
    'ui_d_d_pixels_2f_mp_exceeds_the_current',
    'ui_drawing_canvas_pinch_and_move_two_fingers_to',
    'ui_expand_tool_category',
    'ui_none',
    'ui_trim_expand_canvas_by_touch',
}
TAGS = {'default', 'es-ES'}
MEMORY = 'ui_d_d_pixels_2f_mp_exceeds_the_current'
CANVAS = 'ui_drawing_canvas_pinch_and_move_two_fingers_to'
FIXTURE = 'spanish_editor_current_wording.json'
CURRENT = 'portuguese_spanish_priority_wording.json'


def reviewed_memory_fixture(previous, current):
    """One exact reviewed successor; keep the historical fixture immutable."""
    data = deepcopy(previous)
    row = current['locales']['es-ES']['values'][MEMORY]
    values = data['values'][MEMORY]
    constraints = data['constraints'][MEMORY]
    if (values['default'] != row['source'] or values['es-ES'] != row['previous_target']
            or constraints['attributes'] != row['previous_attributes']
            or row['attributes'] != row['previous_attributes']
            or row['target'] != row['previous_target'].replace('píxeles', 'px')
            or row['previous_target'].count('píxeles') != 1):
        raise ValueError('Spanish warning successor differs from its exact reviewed predecessor')
    values['es-ES'] = row['target']
    return data


class SpanishEditorWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(reviewed_memory_fixture(fixture(FIXTURE), fixture(CURRENT)), KEYS, TAGS)
        cls.xml = {
            'default': (catalogues.RES / 'values/strings.xml').read_text(encoding='utf-8'),
            'es-ES': (catalogues.RES / 'values-b+es+ES/strings.xml').read_text(encoding='utf-8'),
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
                    require_string(self.xml[tag], key, expected, constraints)

    def test_fixture_requires_all_eight_keys_both_locales_and_constraints(self):
        for key in KEYS:
            for mutation in ('missing-key', 'missing-locale', 'empty-text', 'missing-constraint'):
                changed = deepcopy(self.data)
                if mutation == 'missing-key':
                    del changed['values'][key]
                elif mutation == 'missing-locale':
                    del changed['values'][key]['es-ES']
                elif mutation == 'empty-text':
                    changed['values'][key]['es-ES'] = ''
                else:
                    del changed['constraints'][key]
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, TAGS)

    def test_truncated_or_duplicate_messages_and_attribute_changes_are_rejected(self):
        for key in KEYS:
            expected = self.data['values'][key]['es-ES']
            constraints = self.data['constraints'][key]
            for mutation in ('truncate', 'duplicate', 'missing', 'format-flag', 'markup'):
                root = ET.fromstring(self.xml['es-ES'])
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

    def test_placeholder_type_loss_and_unescaped_apostrophes_are_rejected(self):
        expected = self.data['values'][MEMORY]['es-ES']
        constraints = self.data['constraints'][MEMORY]
        for changed in (expected.replace('%1$d', '%1$s'),
                        expected.replace('%3$.2f', '%3$f'),
                        expected.replace('%4$.2f', ''), expected + " '"):
            root = ET.fromstring(self.xml['es-ES'])
            root.find(f"./string[@name='{MEMORY}']").text = changed
            # Matching the mutated wording still must not bypass syntax/type checks.
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                require_string(ET.tostring(root, encoding='unicode'), MEMORY, changed, constraints)

    def test_complete_catalogue_and_android_string_syntax(self):
        self.assertEqual([], catalogues.validate_catalogue('es-ES', require_complete=True))
        root = ET.fromstring(self.xml['es-ES'])
        identities = [(node.tag, node.get('name')) for node in root]
        self.assertEqual(len(identities), len(set(identities)))
        for node in root.findall('string'):
            value = ''.join(node.itertext())
            with self.subTest(key=node.get('name')):
                self.assertEqual([], catalogues.android_string_errors(value))
                self.assertEqual([], catalogues.format_string_errors(value, node.get('formatted') != 'false'))

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

    def test_memory_successor_rejects_source_value_attribute_and_unreviewed_target_drift(self):
        previous, current = fixture(FIXTURE), fixture(CURRENT)
        projected = reviewed_memory_fixture(previous, current)
        for key in KEYS - {MEMORY}:
            self.assertEqual(previous['values'][key], projected['values'][key])
        self.assertEqual(previous['constraints'], projected['constraints'])
        self.assertIn('píxeles', previous['values'][MEMORY]['es-ES'])
        self.assertNotEqual(previous['values'][MEMORY]['es-ES'], projected['values'][MEMORY]['es-ES'])
        for mutation in ('source', 'previous', 'attributes', 'target-attributes', 'target', 'second-word'):
            old, new = deepcopy(previous), deepcopy(current)
            row = new['locales']['es-ES']['values'][MEMORY]
            if mutation == 'source': old['values'][MEMORY]['default'] += ' changed'
            elif mutation == 'previous': old['values'][MEMORY]['es-ES'] += ' changed'
            elif mutation == 'attributes': old['constraints'][MEMORY]['attributes']['formatted'] = 'false'
            elif mutation == 'target-attributes': row['attributes']['formatted'] = 'false'
            elif mutation == 'target': row['target'] += ' changed'
            else:
                old['values'][MEMORY]['es-ES'] += ' píxeles'
                row['previous_target'] = old['values'][MEMORY]['es-ES']
                row['target'] = row['previous_target'].replace('píxeles', 'px')
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                reviewed_memory_fixture(old, new)

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

    def test_unresolved_palette_and_abbreviation_values_remain_unchanged(self):
        strings = self.strings['es-ES']
        self.assertEqual(('FG', 'BG'), (strings['ui_fg'], strings['ui_bg']))
        self.assertEqual('Primer plano %1$s, fondo %2$s. Paleta de colores %3$s.',
                         strings['ui_foreground_background_colour_palette'])


if __name__ == '__main__':
    unittest.main()
