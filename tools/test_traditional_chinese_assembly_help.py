"""Traditional Chinese provider qualifiers and current control labels.

The independent crop-dimension/memory clauses remain in test_review_followup_pr2.
Mode behavior is covered by shared assembly mode and real consumer regressions.
"""
import unittest
import translation_catalogues as catalogues
from current_localization_contracts import decode_display

HELP = 'ui_add_up_to_20_images_with_android_s'


class TraditionalChineseAssemblyHelpTests(unittest.TestCase):
    def test_only_modification_time_is_conditional_and_crop_unplace_movement_is_possible(self):
        for tag in ('zh-HK', 'zh-TW'):
            value = catalogues.read_strings(catalogues.catalogue_paths()[tag])[HELP]
            self.assertIn('下方托盤會顯示縮圖、檔案名稱，以及', value)
            self.assertIn('如檔案提供者有提供修改時間，', value)
            self.assertNotIn('下方托盤會在檔案提供者有提供資料時', value)
            crop = '裁剪' if tag == 'zh-HK' else '裁切'
            self.assertIn(crop + '母圖片時，連接到它的圖片可能會移動。', value)
            self.assertIn('相連的圖片可能會移動以填補空位。', value)
            self.assertNotIn('後面的圖片會填補空位', value)
            self.assertNotIn('現有連接會隨母圖片移動', value)

    def test_actual_control_names_are_used_in_help(self):
        for tag in ('zh-HK', 'zh-TW'):
            strings = catalogues.read_strings(catalogues.catalogue_paths()[tag])
            value = decode_display(strings[HELP])
            for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                        'ui_same_width', 'ui_same_height', 'ui_restore_original_sizes', 'ui_unplace',
                        'ui_remove', 'ui_undo', 'ui_redo', 'ui_show_all', 'ui_save_png', 'ui_edit_in_paint',
                        'ui_menu_file', 'ui_about_credits23'):
                self.assertIn(decode_display(strings[key]), value)


if __name__ == '__main__':
    unittest.main()
