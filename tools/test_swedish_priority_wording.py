"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class SwedishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text() for tag, folder in [('default', 'values'), ('sv', 'values-sv')]}
        cls.strings = {n.get('name'): n.text.strip('"') for n in ET.fromstring(cls.xml['sv']) if n.tag == 'string'}

    def test_actual_command_names_in_recovery_and_export_guidance(self):
        s = self.strings
        for key in ('ui_a_separate_recovery_copy_has_been_kept_use', 'ui_autosave_is_paused_to_protect_that_draft_use'):
            self.assertIn(s['ui_export_recovery_copy'].removesuffix('…'), s[key])
        self.assertIn(s['ui_menu_file'] + ' > ' + s['ui_load_image'].removesuffix('…'), s['ui_recovery_copy_exported_extract_canvas_png_from_the'])
        self.assertIn('canvas.png', s['ui_recovery_copy_exported_extract_canvas_png_from_the'])
        self.assertIn(s['ui_save'] + ' eller ' + s['save20_title'].removesuffix('…'), s['ui_export_did_not_save23'])
        self.assertIn(s['save20_file_format'] + ': PNG / JPEG', s['ui_autosave_is_paused_to_protect_that_draft_use'])

    def test_frame_counts_include_the_localized_lower_bound(self):
        for count in (2, 21, 101):
            exact = self.strings['formats22_animation_message'].replace('%1$s', 'GIF').replace('%2$s', str(count))
            lower = self.strings['formats22_at_least_frames'].replace('%1$d', str(count))
            inexact = self.strings['formats22_animation_message'].replace('%1$s', 'GIF').replace('%2$s', lower)
            self.assertIn(f'innehåller {count} bildrutor.', exact)
            self.assertIn(f'innehåller minst {count} bildrutor.', inexact)
            self.assertIn('bevarar inte animeringar.', exact)
        self.assertIn('om den innehåller flera bildrutor', self.strings['formats22_animation_unknown'])

    def test_fixed_tool_and_action_meanings_are_distinct(self):
        self.assertNotEqual(self.strings['ui_outline'], self.strings['ui_solid_fill'])
        self.assertNotEqual(self.strings['ui_keep_editing23'], self.strings['ui_cancel'])
        self.assertIn('osparade ändringar', self.strings['ui_your_current_image_has_unsaved_changes'])

    def test_conditional_safety_and_retained_data_are_explicit(self):
        s = self.strings
        for key in ('ui_d_d_pixels_2f_mp_exceeds_the_current', 'ui_there_is_not_enough_memory_for_this_operation'):
            self.assertIn('Ingen automatisk storleksändring gjordes.', s[key])
        self.assertIn('Originalfilen förblir oförändrad.', s['ui_sampled_resize_memory_explanation'])
        self.assertIn('Bildmontaget är oförändrat.', s['ui_assembly_source_memory_floor'])
        self.assertIn('har behållits', s['ui_history_unavailable34'])
        self.assertIn('visas på engelska.', s['language20_translation_note'])

if __name__ == '__main__': unittest.main()
