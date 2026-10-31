"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import translation_catalogues as catalogues

class KoreanPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strings = catalogues.read_strings(catalogues.RES / 'values-b+ko+KR/strings.xml')

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

    def test_foreground_and_background_labels_keep_their_roles(self):
        self.assertEqual(('전경색', '배경색'), tuple(self.strings[k] for k in ('ui_foreground_colour', 'ui_background_colour')))
        self.assertEqual(('전경', '배경'), tuple(self.strings[k] for k in ('ui_fg', 'ui_bg')))

    def test_memory_recovery_and_unchanged_assembly_remain_explicit(self):
        s = self.strings
        self.assertIn('현재 한도에서는 이미지 조합의 크기를 줄이는 것만으로는 충분하지 않습니다.', s['ui_assembly_source_memory_floor'])
        self.assertTrue(s['ui_assembly_source_memory_floor'].endswith('현재 이미지 조합은 변경되지 않았습니다.'))
        self.assertTrue(s['ui_no_resize_fits_decoder_memory'].endswith('취소하고 더 작은 원본 이미지를 사용하세요.'))
        self.assertIn('오른쪽이나 아래쪽 경계 밖의 픽셀은 삭제되며, 실행 취소로 복원할 수 있습니다.', s['ui_keeps_pixels_at_the_top_left_smaller_canvas'])

if __name__ == '__main__': unittest.main()
