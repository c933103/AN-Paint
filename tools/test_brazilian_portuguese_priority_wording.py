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
        s = self.strings['pt-BR']
        self.assertEqual('Arquivo', s['ui_menu_file'])
        self.assertEqual('Abrir imagem…', s['ui_load_image'])
        self.assertEqual('Cópia de recuperação exportada. Extraia canvas.png do ZIP e abra essa imagem com '
                         + s['ui_menu_file'] + ' > ' + s['ui_load_image'].rstrip('…')
                         + '. O ZIP também contém as configurações do rascunho e qualquer seleção flutuante.', s[RECOVERY])
        self.assertRegex(self.activity, r'ui\(R\.string\.ui_load_image\) to \{confirmReplacement \{launchOpen\(false\)\}\}')
        self.assertIn('message(ui(R.string.' + RECOVERY + '))', self.activity)

    def test_language_note_retains_both_fallback_cases_and_paragraph_boundary(self):
        self.assertEqual(r'Idioma do aplicativo\n\nAs traduções são mantidas nos recursos de idioma do AN Paint. '
                         'Textos novos ou não traduzidos aparecem em inglês.', self.strings['pt-BR'][NOTE])
        picker = (CLASSIC / 'AppLanguage.kt').read_text(encoding='utf-8')
        self.assertIn('text = ui(R.string.' + NOTE + ')', picker)

    def test_selected_tool_agreement_uses_fixed_feminine_noun_in_both_states(self):
        for key, verb in ((COLLAPSE, 'Recolher'), (EXPAND, 'Expandir')):
            self.assertEqual('%1$s. Ferramenta selecionada: %2$s. ' + verb + ' ferramentas e opções',
                             self.strings['pt-BR'][key])
        source = (CLASSIC / 'ToolCategoryButton.kt').read_text(encoding='utf-8')
        self.assertRegex(source, r'contentDescription=ui\(if\(expanded\) R\.string\.' + COLLAPSE +
                         r' else R\.string\.' + EXPAND + r',ui\(category.labelId\),selectedTool.label\)')
        self.assertIn('LocaleTooltip.set(this,contentDescription)', source)

    def test_pixel_count_is_a_label_followed_by_count_for_all_valid_sizes(self):
        self.assertEqual('%1$d × %2$d px · Quantidade de pixels: %3$,d (%4$.2f MP)', self.strings['pt-BR'][COUNT])
        source = (CLASSIC / 'ImageImport.kt').read_text(encoding='utf-8')
        self.assertIn('width > 0 && height > 0', source)
        self.assertIn('val pixels: Long get() = width.toLong() * height', source)
        self.assertIn('ui(R.string.' + COUNT + ', width, height, pixels, pixels / 1_000_000.0)', source)

    def test_zoom_and_pan_instructions_match_real_gesture_span_and_focus(self):
        self.assertEqual('Tela de desenho. Afaste dois dedos para ampliar e aproxime-os para reduzir o zoom. '
                         'Arraste os dois dedos juntos para deslocar a visualização. '
                         'No modo Navegar, também é possível deslocar a visualização com um dedo.', self.strings['pt-BR'][GESTURE])
        source = (CLASSIC / 'PaintCanvas.kt').read_text(encoding='utf-8')
        self.assertIn('contentDescription = ui(R.string.' + GESTURE + ')', source)
        self.assertIn('if (event.pointerCount > 1)', source)
        self.assertIn('zoomAt(zoom*span/pinchSpan,pinchFocus.x,pinchFocus.y)', source)
        self.assertIn('panX+=focus.x-pinchFocus.x;panY+=focus.y-pinchFocus.y', source)
        self.assertIn('panning = tool == PaintTool.ZOOM', source)
        self.assertRegex(source, r'if \(panning\) \{\s*fitMode=false;panX \+= event.x - screenPrevious.x; panY \+= event.y - screenPrevious.y')

    def test_none_matches_image_checklist_and_composed_units_stay_lowercase(self):
        s = self.strings['pt-BR']
        self.assertEqual('Nenhuma', s[NONE])
        self.assertEqual('pixels', s[UNIT])
        self.assertEqual('Pixels', s['ui_pixels'])
        crop = (CLASSIC / 'ImageCropDialog.kt').read_text(encoding='utf-8')
        self.assertIn('ui(R.string.ui_apply_to_these_images)', crop)
        self.assertIn('ui(R.string.ui_none) to false', crop)
        self.assertIn('checks.forEach { it.isChecked = checked }', crop)
        dimensions = (CLASSIC / 'DimensionControls.kt').read_text(encoding='utf-8')
        for key in ('ui_width_in', 'ui_height_in'):
            self.assertRegex(dimensions, r'contentDescription = ui\(R\.string\.' + key + r',.*ui\(R\.string\.' + UNIT + r'\)\)')

if __name__ == '__main__':
    unittest.main()
