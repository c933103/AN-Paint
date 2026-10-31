"""Source-language mode and safety boundaries; no whole-prose approval oracle."""
import unittest
from current_localization_contracts import current_display

KEY = 'ui_add_up_to_20_images_with_android_s'

class AssemblyHelpModesTest(unittest.TestCase):
    def test_snap_and_exact_position_have_distinct_origin_overlap_and_motion_rules(self):
        text = current_display('default', KEY)
        for clause in ('When snapping, the first image starts at the origin.',
                       'Overlaps are rejected when snapping.',
                       'top-left X/Y coordinates in whole pixels, starting at zero.',
                       'Other images keep their positions, and overlaps are allowed.',
                       'Attached images may move when their parent is cropped.',
                       'returns only the selected image to the tray.',
                       'Other images stay placed; attached images may move to fill the gap.'):
            self.assertIn(clause, text)
        self.assertNotIn('Following images fill its gap', text)

    def test_memory_normalization_replacement_and_provider_conditions_remain_distinct(self):
        text = current_display('default', KEY)
        for clause in ('file modification times when supplied by the provider.',
                       'image dimensions after cropping and any Same width or Same height adjustment',
                       "preserving each image's own aspect ratio.",
                       'removes normalization and keeps crops.',
                       'it never changes output dimensions.',
                       'as an undoable replacement.',
                       'choose a smaller output copy if offered.',
                       'shows a memory warning instead of a size chooser.',
                       'Original source files stay unchanged.'):
            self.assertIn(clause, text)

    def test_exact_position_controls_do_not_require_format_arguments(self):
        import translation_catalogues as catalogues
        values = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        for key in ('ui_assembly_exact_position', 'ui_assembly_target_x', 'ui_assembly_target_y',
                    'ui_assembly_position_help', 'ui_assembly_position_nonnegative', 'ui_assembly_unknown_image'):
            with self.subTest(key=key):
                self.assertTrue(values[key])
                self.assertFalse(catalogues.placeholders(values[key]))
                self.assertNotIn(r'\n', values[key])

if __name__ == '__main__':
    unittest.main()
