"""Bounded Russian/European Portuguese wording and static-consumer regressions.

These host checks do not certify Android runtime/layout, TalkBack, native-speaker
acceptance or either complete locale. No historical ledger is an acceptance oracle.
"""
from copy import deepcopy
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
EXPECTED_KEYS = {
    'ru': {
        'ui_d_d_pixels_2f_mp_exceeds_the_current',
        'ui_d_d_px_d_pixels_2f_mp',
        'ui_collapse_tool_category',
        'ui_expand_tool_category',
    },
    'pt-PT': {
        'ui_keeps_pixels_at_the_top_left_smaller_canvas',
        'language20_translation_note',
        'ui_collapse_tool_category',
        'ui_expand_tool_category',
        'ui_drawing_canvas_pinch_and_move_two_fingers_to',
        'ui_free_form_select',
        'ui_rectangle_select',
        'ui_none',
        'ui_pixels',
        'ui_pixels_6ec9c2',
    },
}
FIXTURES = {
    'ru': 'russian_priority_current_wording.json',
    'pt-PT': 'portuguese_priority_current_wording.json',
}


def wording(tag):
    return require_wording_shape(fixture(FIXTURES[tag]), EXPECTED_KEYS[tag], {tag})


class RussianPortuguesePriorityWording(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = {tag: catalogues.catalogue_paths()[tag] for tag in EXPECTED_KEYS}
        cls.xml = {tag: path.read_text() for tag, path in cls.paths.items()}
        cls.values = {tag: catalogues.read_strings(path) for tag, path in cls.paths.items()}

    def test_complete_wording_attributes_and_typed_arguments(self):
        defaults, _, _, _ = catalogues.default_resources()
        for tag in EXPECTED_KEYS:
            data = wording(tag)
            for key, values in data['values'].items():
                with self.subTest(locale=tag, key=key):
                    value = require_string(self.xml[tag], key, values[tag], data['constraints'][key])
                    self.assertEqual(catalogues.placeholders(defaults[key]), catalogues.placeholders(value))

    def test_fixture_cannot_drop_keys_constraints_locales_or_text(self):
        for tag in EXPECTED_KEYS:
            original = wording(tag)
            for key in EXPECTED_KEYS[tag]:
                for mutation in ('missing-key', 'missing-constraint', 'missing-locale', 'empty-text'):
                    data = deepcopy(original)
                    if mutation == 'missing-key':
                        del data['values'][key]
                    elif mutation == 'missing-constraint':
                        del data['constraints'][key]
                    elif mutation == 'missing-locale':
                        data['values'][key] = {}
                    else:
                        data['values'][key][tag] = ''
                    with self.subTest(locale=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                        require_wording_shape(data, EXPECTED_KEYS[tag], {tag})

    def test_missing_duplicate_truncated_wrong_type_and_attribute_mutations_fail(self):
        for tag in EXPECTED_KEYS:
            root = ET.fromstring(self.xml[tag])
            data = wording(tag)
            for key, values in data['values'].items():
                node = root.find(f"./string[@name='{key}']")
                line = ET.tostring(node, encoding='unicode')
                truncated = deepcopy(node)
                truncated.text = values[tag][:-1]
                wrong_type = deepcopy(node)
                tokens = list(catalogues.placeholders(values[tag]))
                if tokens:
                    token = tokens[0]
                    wrong_type.text = wrong_type.text.replace(token, token[:-1] + ('s' if token[-1] != 's' else 'd'), 1)
                else:
                    wrong_type.text += ' %1$d'
                wrong_attribute = deepcopy(node)
                wrong_attribute.set('formatted', 'true' if node.get('formatted') == 'false' else 'false')
                cases = {
                    'missing': '',
                    'duplicate': line + line,
                    'truncated': ET.tostring(truncated, encoding='unicode'),
                    'wrong-type': ET.tostring(wrong_type, encoding='unicode'),
                    'wrong-attribute': ET.tostring(wrong_attribute, encoding='unicode'),
                }
                for mutation, broken in cases.items():
                    with self.subTest(locale=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                        require_string('<resources>' + broken + '</resources>', key, values[tag], data['constraints'][key])

    def test_catalogues_are_complete_and_unique_with_valid_android_strings(self):
        for tag in EXPECTED_KEYS:
            root = ET.fromstring(self.xml[tag])
            identities = [(node.tag, node.get('name')) for node in root]
            with self.subTest(locale=tag):
                self.assertEqual(len(identities), len(set(identities)))
                self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=True))
            for node in root.findall('string'):
                value = ''.join(node.itertext())
                with self.subTest(locale=tag, key=node.get('name')):
                    self.assertEqual([], catalogues.android_string_errors(value))
                    self.assertEqual([], catalogues.format_string_errors(value, node.get('formatted') != 'false'))

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
        source = (CLASSIC / 'ToolCategoryButton.kt').read_text()
        self.assertIn('if(expanded) R.string.ui_collapse_tool_category else R.string.ui_expand_tool_category', source)
        self.assertIn('ui(category.labelId),selectedTool.label)', source)
        self.assertIn('LocaleTooltip.set(this,contentDescription)', source)

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
        source = (CLASSIC / 'ImageImport.kt').read_text()
        self.assertIn('val pixels: Long get() = width.toLong() * height', source)
        guarded = 'ui(R.string.ui_d_d_px_d_pixels_2f_mp, width, height, pixels, pixels / 1_000_000.0)'
        def require_guarded(code): self.assertIn(guarded, code)
        require_guarded(source)
        with self.assertRaises(AssertionError):
            require_guarded(source.replace(guarded, 'String.format(Locale.ROOT, ui(R.string.ui_d_d_px_d_pixels_2f_mp), width, height, pixels, pixels / 1_000_000.0)'))

    def test_russian_memory_warning_retains_all_safety_clauses(self):
        value = self.values['ru']['ui_d_d_pixels_2f_mp_exceeds_the_current']
        for clause in ('безопасный лимит редактирования %4$.2f Мп',
                       'хранит полное изображение в памяти', 'для преобразований и выделений',
                       'определяется доступной памятью',
                       'до выделения памяти для слишком большого растрового изображения',
                       'Автоматическое изменение размера не применялось.'):
            self.assertIn(clause, value)
        source = (CLASSIC / 'ImageMemoryPolicy.kt').read_text()
        self.assertIn('if (pixels > permitted) throw ImageSizeException', source)
        guarded = ('ui(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current,\n'
                   '            width, height, pixels / 1_000_000.0, permitted / 1_000_000.0)')
        def require_guarded(code): self.assertIn(guarded, code)
        require_guarded(source)
        with self.assertRaises(AssertionError):
            require_guarded(source.replace('ui(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current,',
                                          'String.format(Locale.ROOT, ui(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current),'))

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
        self.assertEqual(['Idioma da aplicação', '', 'As traduções são mantidas nos recursos de idioma do AN Paint. O texto novo ou não traduzido aparece em inglês.'], value.split(r'\n'))
        self.assertIn('text = ui(R.string.language20_translation_note)', (CLASSIC / 'AppLanguage.kt').read_text())
        data = wording('pt-PT')
        broken = ET.Element('string', name=key)
        broken.text = value.replace(r'\n', r'\\n')
        with self.assertRaises(ValueError):
            require_string('<resources>' + ET.tostring(broken, encoding='unicode') + '</resources>', key, value, data['constraints'][key])

    def test_portuguese_zoom_help_preserves_both_directions_pan_and_navigate(self):
        value = self.values['pt-PT']['ui_drawing_canvas_pinch_and_move_two_fingers_to']
        for phrase in ('Afaste ou junte dois dedos', 'ampliar ou reduzir', 'mova-os para deslocar',
                       'O modo Navegar também permite deslocar com um dedo.'):
            self.assertIn(phrase, value)
        source = (CLASSIC / 'PaintCanvas.kt').read_text()
        self.assertIn('zoomAt(zoom*span/pinchSpan,pinchFocus.x,pinchFocus.y)', source)
        self.assertIn('panX+=focus.x-pinchFocus.x;panY+=focus.y-pinchFocus.y', source)
        self.assertIn('contentDescription = ui(R.string.ui_drawing_canvas_pinch_and_move_two_fingers_to)', source)

    def test_portuguese_selection_names_and_none_match_tool_and_image_consumers(self):
        values = self.values['pt-PT']
        self.assertEqual(('Seleção livre', 'Seleção retangular', 'Nenhuma'),
                         (values['ui_free_form_select'], values['ui_rectangle_select'], values['ui_none']))
        document = (CLASSIC / 'PaintDocument.kt').read_text()
        self.assertIn('LASSO(R.string.ui_free_form_select,', document)
        self.assertIn('SELECT(R.string.ui_rectangle_select,', document)
        crop = (CLASSIC / 'ImageCropDialog.kt').read_text()
        self.assertIn('text = ui(R.string.ui_apply_to_these_images)', crop)
        self.assertIn('ui(R.string.ui_none) to false', crop)
        self.assertIn('checks.forEach { it.isChecked = checked }', crop)

    def test_portuguese_pixel_spelling_and_composed_accessibility_units(self):
        values = self.values['pt-PT']
        self.assertEqual(('Píxeis', 'píxeis'), (values['ui_pixels'], values['ui_pixels_6ec9c2']))
        for key, expected in (('ui_width_in', 'Largura em píxeis'), ('ui_height_in', 'Altura em píxeis')):
            self.assertEqual(expected, values[key].replace('%1$s', values['ui_pixels_6ec9c2']))
        source = (CLASSIC / 'DimensionControls.kt').read_text()
        self.assertIn('listOf(ui(R.string.ui_pixels), ui(R.string.ui_percent))', source)
        for key in ('ui_width_in', 'ui_height_in'):
            self.assertIn('ui(R.string.' + key + ', if (percent) ui(R.string.ui_percent_fd8671) else ui(R.string.ui_pixels_6ec9c2))', source)


if __name__ == '__main__':
    unittest.main()
