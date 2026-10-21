"""Bounded complete ko-KR corrections; live consumers also have JVM regressions."""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues
# The two memory translations remain pending review against the corrected source.
from memory_warning_source_review import current_source_expectation

KEYS = {
    'save20_unsupported_image_colour', 'ui_assembly_source_memory_floor',
    'ui_export_did_not_save23', 'ui_keeps_pixels_at_the_top_left_smaller_canvas',
    'ui_background_colour', 'ui_drawing_canvas_pinch_and_move_two_fingers_to',
    'ui_foreground_colour', 'ui_no_resize_fits_decoder_memory',
    'ui_trim_amounts_must_fit_inside_each_image_use', 'ui_untitled',
}


class KoreanPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('korean_priority_current_wording.json'), KEYS, {'default', 'ko-KR'})
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text()
                   for tag, folder in [('default', 'values'), ('ko-KR', 'values-b+ko+KR')]}
        cls.strings = catalogues.read_strings(catalogues.RES / 'values-b+ko+KR/strings.xml')

    def test_complete_values_attributes_placeholder_and_newline_contracts(self):
        for key, values in self.data['values'].items():
            self.assertEqual({}, self.data['constraints'][key]['ko-KR']['placeholders'])
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, current_source_expectation(key, tag, expected), self.data['constraints'][key][tag])
        self.assertEqual([], catalogues.validate_catalogue('ko-KR', require_complete=True))

    def test_missing_empty_or_duplicate_values_markup_and_format_mutations_fail(self):
        for key in KEYS:
            for mutation in ('missing', 'duplicate', 'empty', 'truncated', 'markup', 'format-flag', 'placeholder', 'newline'):
                root = ET.fromstring(self.xml['ko-KR']); node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'empty': node.text = ''
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                elif mutation == 'format-flag': node.set('formatted', 'true' if node.get('formatted') == 'false' else 'false')
                elif mutation == 'placeholder': node.text += ' %1$s'
                else: node.text += '\\n'
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, self.data['values'][key]['ko-KR'], self.data['constraints'][key]['ko-KR'])

    def test_missing_fixture_key_locale_or_constraint_fails(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'constraint', 'empty'):
                changed = deepcopy(self.data)
                if mutation == 'key': del changed['values'][key]
                elif mutation == 'locale': del changed['values'][key]['ko-KR']
                elif mutation == 'constraint': del changed['constraints'][key]
                else: changed['values'][key]['ko-KR'] = ''
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_wording_shape(changed, KEYS, {'default', 'ko-KR'})

    def test_navigation_guidance_names_the_real_tool_and_both_gestures(self):
        s = self.strings
        self.assertEqual('이동 및 확대·축소', s['ui_navigate'])
        guidance = s['ui_drawing_canvas_pinch_and_move_two_fingers_to']
        self.assertIn('「' + s['ui_navigate'] + '」 모드에서는 한 손가락으로도 화면을 이동할 수 있습니다.', guidance)
        self.assertIn('두 손가락을 오므리거나 벌려 확대·축소하고, 두 손가락을 움직여 화면을 이동하세요.', guidance)
        self.assertNotIn('탐색 모드', guidance)

    def test_export_guidance_binds_actual_save_and_save_as_commands(self):
        s = self.strings
        self.assertEqual('저장', s['ui_save'])
        self.assertEqual('다른 이름으로 저장…', s['save20_title'])
        self.assertEqual('내보내기가 완료되었습니다. 계속하기 전에 ' + s['ui_save'] + ' 또는 ' +
                         s['save20_title'].removesuffix('…') + '을 사용해 현재 이미지를 저장하세요.', s['ui_export_did_not_save23'])

    def test_complete_colour_family_oracle_matches_reviewed_value(self):
        expected = json.loads((catalogues.ROOT / 'Paintroid/src/test/resources/tagged-colour/expected.json').read_text())
        self.assertEqual(self.data['values']['save20_unsupported_image_colour']['ko-KR'], expected['ko-KR'])
        self.assertEqual(('전경색', '배경색'), tuple(self.strings[k] for k in ('ui_foreground_colour', 'ui_background_colour')))
        self.assertEqual(('전경', '배경'), tuple(self.strings[k] for k in ('ui_fg', 'ui_bg')))

    def test_memory_recovery_and_unchanged_assembly_remain_explicit(self):
        s = self.strings
        self.assertIn('이미지 조합의 크기를 줄여도 이 문제는 해결되지 않습니다.', s['ui_assembly_source_memory_floor'])
        self.assertTrue(s['ui_assembly_source_memory_floor'].endswith('현재 이미지 조합은 변경되지 않았습니다.'))
        self.assertTrue(s['ui_no_resize_fits_decoder_memory'].endswith('취소하고 더 작은 원본 이미지를 사용하세요.'))
        self.assertIn('오른쪽이나 아래쪽 경계 밖의 픽셀은 삭제되며, 실행 취소로 복원할 수 있습니다.', s['ui_keeps_pixels_at_the_top_left_smaller_canvas'])

    def test_context_holds_and_prior_receipt_are_not_new_corrections(self):
        holds = {'ui_discard', 'ui_save_as', 'ui_main23'}
        self.assertEqual(holds, set(self.data['retained_context_holds']))
        self.assertTrue(holds.isdisjoint(KEYS))
        # These are unchanged observations, explicitly not accepted wording or inferred callers.
        self.assertEqual(('변경 내용 버리기', '%1$s 형식으로 저장', '기본'), tuple(self.strings[k] for k in ('ui_discard', 'ui_save_as', 'ui_main23')))
        self.assertEqual('ui_sampled_resize_memory_explanation', self.data['prior_current_not_new']['key'])
        self.assertNotIn(self.data['prior_current_not_new']['key'], KEYS)


if __name__ == '__main__': unittest.main()
