"""Italian priority wording regressions; static composition, not device acceptance."""
from copy import deepcopy
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
FIXTURE = 'italian_priority_current_wording.json'
EXPECTED_KEYS = {
    'save20_destination_error',
    'ui_export_did_not_save23',
    'ui_recovery_copy_exported_extract_canvas_png_from_the',
    'language20_translation_note',
    'ui_collapse_tool_category',
    'ui_expand_tool_category',
    'ui_drawing_canvas_pinch_and_move_two_fingers_to',
}


def wording():
    return require_wording_shape(fixture(FIXTURE), EXPECTED_KEYS, {'it'})


class ItalianPriorityWording(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = catalogues.catalogue_paths()['it']
        cls.xml = cls.path.read_text()
        cls.values = catalogues.read_strings(cls.path)

    def test_complete_values_attributes_and_typed_arguments(self):
        data = wording()
        defaults, _, _, _ = catalogues.default_resources()
        for key, translations in data['values'].items():
            with self.subTest(key=key):
                actual = require_string(self.xml, key, translations['it'], data['constraints'][key])
                self.assertEqual(catalogues.placeholders(defaults[key]),
                                 catalogues.placeholders(actual))

    def test_fixture_cannot_omit_keys_locales_constraints_or_text(self):
        original = wording()
        for key in EXPECTED_KEYS:
            for mutation in ('key', 'constraint', 'locale', 'empty'):
                data = deepcopy(original)
                if mutation == 'key':
                    del data['values'][key]
                elif mutation == 'constraint':
                    del data['constraints'][key]
                elif mutation == 'locale':
                    data['values'][key] = {}
                else:
                    data['values'][key]['it'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(data, EXPECTED_KEYS, {'it'})

    def test_missing_duplicate_truncated_wrong_type_and_attribute_mutations_fail(self):
        data = wording()
        root = ET.fromstring(self.xml)
        for key, translations in data['values'].items():
            node = root.find(f"./string[@name='{key}']")
            line = ET.tostring(node, encoding='unicode')
            truncated = deepcopy(node)
            truncated.text = truncated.text[:-1]
            wrong_attribute = deepcopy(node)
            wrong_attribute.set('formatted', 'true' if node.get('formatted') == 'false' else 'false')
            wrong_type = deepcopy(node)
            arguments = list(catalogues.placeholders(translations['it']))
            if arguments:
                token = arguments[0]
                wrong_type.text = wrong_type.text.replace(token, token[:-1] + 'd', 1)
            else:
                wrong_type.text += ' %1$d'
            cases = {
                'missing': '',
                'duplicate': line + line,
                'truncated': ET.tostring(truncated, encoding='unicode'),
                'wrong-type': ET.tostring(wrong_type, encoding='unicode'),
                'wrong-attribute': ET.tostring(wrong_attribute, encoding='unicode'),
            }
            for mutation, broken in cases.items():
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string('<resources>' + broken + '</resources>',
                                   key, translations['it'], data['constraints'][key])

    def test_catalogue_completeness_uniqueness_and_android_syntax(self):
        root = ET.fromstring(self.xml)
        identities = [(node.tag, node.get('name')) for node in root]
        self.assertEqual(len(identities), len(set(identities)))
        self.assertEqual([], catalogues.validate_catalogue('it', require_complete=True))
        for node in root.findall('string'):
            value = ''.join(node.itertext())
            with self.subTest(key=node.get('name')):
                self.assertEqual([], catalogues.android_string_errors(value))
                self.assertEqual([], catalogues.format_string_errors(
                    value, node.get('formatted') != 'false'))

    def test_warning_routes_use_exact_live_menu_labels_and_keep_safety_clauses(self):
        export_warning = self.values['ui_export_did_not_save23']
        self.assertIn('«' + self.values['ui_save'] + '»', export_warning)
        self.assertIn('«' + self.values['save20_title'] + '»', export_warning)
        self.assertIn('L’esportazione è stata creata.', export_warning)
        self.assertIn('per salvare l’immagine corrente prima di continuare.', export_warning)
        recovery = self.values['ui_recovery_copy_exported_extract_canvas_png_from_the']
        self.assertIn('«' + self.values['ui_menu_file'] + ' > ' + self.values['ui_load_image'] + '»', recovery)
        self.assertIn('Copia di recupero esportata.', recovery)
        self.assertIn('Estrai canvas.png dallo ZIP', recovery)
        self.assertIn('le impostazioni della bozza e l’eventuale selezione flottante.', recovery)
        # Bind labels to inspected production menu commands, without claiming UI execution.
        source = (CLASSIC / 'ClassicPaintActivity.kt').read_text()
        for call in ('ui(R.string.ui_load_image) to {confirmReplacement {launchOpen(false)}}',
                     'ui(R.string.save20_title) to {showSaveOptions('):
            self.assertIn(call, source)

    def test_selected_tool_grammar_for_actual_category_tool_labels(self):
        source = (CLASSIC / 'ToolCategoryButton.kt').read_text()
        document = (CLASSIC / 'PaintDocument.kt').read_text()
        tool_ids = dict(re.findall(r'\b([A-Z_]+)\(R\.string\.(\w+),\s*R\.string\.\w+\)', document))
        categories = re.findall(r'\b[A-Z_]+\(R\.string\.(\w+),listOf\((.*?)\)\)', source, re.S)
        self.assertTrue(categories)
        seen = set()
        for category_key, body in categories:
            tools = re.findall(r'PaintTool\.(\w+)', body)
            self.assertTrue(tools)
            for tool in tools:
                label = self.values[tool_ids[tool]]
                seen.add(label)
                for key, action in (('ui_expand_tool_category', 'Espandi'),
                                    ('ui_collapse_tool_category', 'Comprimi')):
                    rendered = self.values[key].replace('%1$s', self.values[category_key]).replace('%2$s', label)
                    with self.subTest(category=category_key, tool=tool, key=key):
                        self.assertEqual(self.values[category_key] + '. Strumento selezionato: ' + label +
                                         '. ' + action + ' strumenti e opzioni', rendered)
                        self.assertNotIn(label + ' selezionato', rendered)
        self.assertTrue({'Matita', 'Linea', 'Ellisse', 'Selezione rettangolare'} <= seen)
        self.assertIn('R.string.ui_collapse_tool_category else R.string.ui_expand_tool_category,'
                      'ui(category.labelId),selectedTool.label)', source)

    def test_destination_file_fallback_scope_and_bidirectional_gestures(self):
        destination = self.values['save20_destination_error']
        self.assertIn('sostituire il file di destinazione con l’immagine completata', destination)
        fallback = self.values['language20_translation_note']
        self.assertTrue(fallback.startswith(self.values['language20_app_language'] + '\\n\\n'))
        self.assertIn('I testi nuovi o non tradotti appaiono in inglese.', fallback)
        gesture = self.values['ui_drawing_canvas_pinch_and_move_two_fingers_to']
        self.assertIn('Avvicina o allontana due dita per ridurre o ingrandire la vista', gesture)
        self.assertIn('muovile insieme per spostarla.', gesture)
        self.assertIn('La modalità ' + self.values['ui_navigate'] +
                      ' consente anche lo spostamento con un dito.', gesture)
        source = (CLASSIC / 'PaintCanvas.kt').read_text()
        self.assertIn('zoomAt(zoom*span/pinchSpan,pinchFocus.x,pinchFocus.y)', source)
        self.assertIn('panX+=focus.x-pinchFocus.x;panY+=focus.y-pinchFocus.y', source)
        self.assertIn('panning = tool == PaintTool.ZOOM', source)

    def test_save_alias_remains_distinct_from_discard_and_keep_editing(self):
        self.assertEqual('@string/ui_save', self.values['ui_save_a5d0d9'])
        self.assertEqual('Salva', self.values['ui_save'])
        self.assertEqual('Scarta le modifiche', self.values['ui_discard_changes23'])
        self.assertEqual('Continua a modificare', self.values['ui_keep_editing23'])
        source = (CLASSIC / 'ClassicPaintActivity.kt').read_text()
        self.assertIn('.setPositiveButton(ui(R.string.ui_save_a5d0d9)) '
                      '{ _, _ -> afterSave = action; requestSave(false) }', source)
        self.assertIn('if(target==null) showSaveOptions(ImageFormat.PNG)', source)
        self.assertIn('else {exportOptions=target.options;isExporting=false;shareAfterSave=false;writeImage(target.uri)}', source)

    def test_required_clause_mutations_fail_the_full_value_contract(self):
        data = wording()
        clauses = {
            'save20_destination_error': ['il file di destinazione', 'l’immagine completata'],
            'ui_export_did_not_save23': ['«Salva con nome…»', 'prima di continuare'],
            'ui_recovery_copy_exported_extract_canvas_png_from_the': ['canvas.png', '«File > Apri immagine…»',
                'le impostazioni della bozza e l’eventuale selezione flottante'],
            'language20_translation_note': ['nuovi o non tradotti', 'in inglese'],
            'ui_expand_tool_category': ['Strumento selezionato:', 'Espandi strumenti e opzioni'],
            'ui_collapse_tool_category': ['Strumento selezionato:', 'Comprimi strumenti e opzioni'],
            'ui_drawing_canvas_pinch_and_move_two_fingers_to': ['ridurre o ingrandire',
                'muovile insieme per spostarla', 'La modalità Naviga consente anche lo spostamento con un dito.'],
        }
        for key, required in clauses.items():
            for clause in required:
                with self.subTest(key=key, clause=clause):
                    self.assertIn(clause, self.values[key])
                    node = ET.Element('string', data['constraints'][key]['attributes'])
                    node.text = self.values[key].replace(clause, '', 1)
                    with self.assertRaises(ValueError):
                        require_string('<resources>' + ET.tostring(node, encoding='unicode') + '</resources>',
                                       key, data['values'][key]['it'], data['constraints'][key])


if __name__ == '__main__':
    unittest.main()
