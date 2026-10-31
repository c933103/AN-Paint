"""Japanese provider qualification and live Help labels; no prose mirror."""
import unittest
import translation_catalogues as catalogues

HELP = 'ui_add_up_to_20_images_with_android_s'


class JapaneseAssemblyHelpTest(unittest.TestCase):
    def test_only_provider_timestamp_is_optional_and_attached_movement_is_conditional(self):
        value = catalogues.read_strings(catalogues.catalogue_paths()['ja'])[HELP]
        self.assertIn('サムネイル、ファイル名、', value)
        self.assertIn('画像寸法が表示されます。', value)
        self.assertIn('提供元からファイル更新日時を取得できる場合は、その日時も表示されます。', value)
        self.assertIn('接続した画像も移動する場合があります。', value)
        self.assertIn('接続された画像が隙間を埋めるように移動する場合があります。', value)
        self.assertNotIn('後続の画像は隙間を詰めます', value)

    def test_help_uses_current_control_names_including_redo_and_units(self):
        strings = catalogues.read_strings(catalogues.catalogue_paths()['ja'])
        for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                    'ui_same_width', 'ui_same_height', 'ui_smallest', 'ui_largest', 'ui_pixels', 'ui_percent',
                    'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all',
                    'ui_undo', 'ui_redo', 'ui_save_png', 'ui_edit_in_paint', 'ui_about_credits23'):
            self.assertIn('［' + strings[key] + '］', strings[HELP])


if __name__ == '__main__':
    unittest.main()
