"""Current locale semantics; historical approval snapshots live in immutable source history."""
from pathlib import Path
import re
import unittest
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]

CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class ItalianPriorityWording(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = catalogues.catalogue_paths()['it']
        cls.values = catalogues.read_strings(cls.path)

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

if __name__ == '__main__':
    unittest.main()
