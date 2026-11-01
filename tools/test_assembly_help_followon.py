"""Current Assembly Help caption bindings and specific Hakka script regressions.

Repeated approved prose and synthetic sentence mutations are historical evidence.
Shared source-language mode/safety assertions live in test_assembly_help_modes;
historical per-PR clause tables are not active wording oracles.
"""
import unittest
import assembly_help_checks as help_checks
from current_localization_contracts import current_display

DIRECTORIES = ('values-hu', 'values-pt-rBR', 'values-b+lzh+Hant', 'values-b+yue+Latn', 'values-zh-rCN', 'values-b+nan+Latn+TW', 'values-b+lv', 'values-ms', 'values-b+mn+Cyrl+MN', 'values-b+yue+Hant', 'values-ru', 'values-tr', 'values-lt', 'values-b+nan+Hant+TW', 'values-nl', 'values-vi', 'values-sw', 'values-fi', 'values-b+fil', 'values-b+hak+Hant+TW', 'values-b+hak+Latn+TW', 'values-b+jje', 'values-in', 'values-b+eo', 'values-b+es+419', 'values-b+et', 'values-b+ceb', 'values-b+dz', 'values-el')
CAPTIONS = ('ui_about_credits23',
 'ui_assembly_exact_position',
 'ui_batch_crop',
 'ui_crop_image',
 'ui_edit_in_paint',
 'ui_largest',
 'ui_menu_file',
 'ui_redo',
 'ui_remove',
 'ui_reset_crop',
 'ui_restore_original_sizes',
 'ui_same_height',
 'ui_same_width',
 'ui_save_png',
 'ui_show_all',
 'ui_smallest',
 'ui_undo',
 'ui_unplace')
EXTRA_CAPTIONS = {'values-b+ceb': (),
 'values-b+dz': (),
 'values-b+fil': ('ui_percent', 'ui_pixels'),
 'values-b+hak+Hant+TW': ('ui_percent', 'ui_pixels'),
 'values-b+hak+Latn+TW': ('ui_percent', 'ui_pixels'),
 'values-b+lv': ('ui_percent', 'ui_pixels'),
 'values-b+lzh+Hant': ('ui_percent', 'ui_pixels'),
 'values-b+nan+Hant+TW': ('ui_percent', 'ui_pixels'),
 'values-b+nan+Latn+TW': ('ui_percent', 'ui_pixels'),
 'values-el': (),
 'values-fi': ('ui_percent', 'ui_pixels'),
 'values-in': ('ui_percent', 'ui_pixels'),
 'values-lt': ('ui_percent', 'ui_pixels')}

class AssemblyHelpFollowonTests(unittest.TestCase):
    def test_current_help_references_actual_controls_without_freezing_translated_prose(self):
        for directory in DIRECTORIES:
            keys = CAPTIONS + EXTRA_CAPTIONS.get(directory, ())
            if directory == 'values-b+dz':
                # The original DZ binding never required the differently phrased Undo/Redo captions.
                keys = tuple(key for key in keys if key not in ('ui_undo', 'ui_redo'))
            with self.subTest(locale=directory):
                help_checks.check_current_help(self, directory, [(None, key) for key in keys])

        # Only the bindings previously required by the retired Wuu/Nôm wrappers.
        for tag, keys, quotes in (
            ('wuu-Hans', ('ui_same_width', 'ui_same_height'), ('', '')),
            ('vi-Hani', ('ui_assembly_exact_position', 'ui_same_width', 'ui_same_height', 'ui_remove'), ('「', '」')),
        ):
            value = current_display(tag, help_checks.KEY)
            for key in keys:
                with self.subTest(locale=tag, caption=key):
                    self.assertIn(quotes[0] + current_display(tag, key) + quotes[1], value)

    def test_hakka_latin_help_keeps_script_and_specific_corrected_readings(self):
        text, _ = help_checks.current_help('values-b+hak+Latn+TW')
        for directory in ('values-b+hak+Latn+TW', 'values-b+nan+Latn+TW'):
            latin, _ = help_checks.current_help(directory)
            with self.subTest(script=directory):
                self.assertNotRegex(latin, r'[㐀-鿿𠀀-𲎯]')
        self.assertIn('chha̍t hâ-lòi', text)
        self.assertNotIn('chhet hâ-lòi', text)
        self.assertIn('fat thu” ya-he “Siông-thùng', text)
        self.assertNotIn('fat thu” ia-he “Siông-thùng', text)

if __name__ == '__main__':
    unittest.main()
