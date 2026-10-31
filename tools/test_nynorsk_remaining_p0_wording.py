"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


class NynorskRemainingP0Tests(unittest.TestCase):

    def test_recovery_and_animation_compositions_keep_actual_commands_and_quantity(self):
        value = lambda key: current_display('nn', key)
        recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
        self.assertIn('Fil > '+current_display('nn','ui_load_image'), recovery)
        self.assertIn('canvas.png', recovery);self.assertIn('ZIP', recovery)
        self.assertIn('eit eventuelt flytande utval.', recovery)
        paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
        self.assertIn(value('ui_export_recovery_copy'), paused)
        self.assertIn(value('save20_file_format') + ': PNG / JPEG', paused)
        for key in ('formats22_animation_poster', 'formats22_animation_still'):
            self.assertTrue(value(key).endswith('Ved lagring vert det laga eit stillbilete.'))
        self.assertEqual({'%1$d':1, '%2$d':1, '%3$.2f':1, '%4$.2f':1}, catalogues.placeholders(value('ui_d_d_pixels_2f_mp_exceeds_the_current')))

if __name__ == '__main__':
    unittest.main()
