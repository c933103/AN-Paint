"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import translation_catalogues as catalogues

MEMORY = "ui_d_d_pixels_2f_mp_exceeds_the_current"
RESIZE = "ui_the_full_image_and_working_buffers_exceed_the"
COUNT = "ui_d_d_px_d_pixels_2f_mp"
NOTE = "language20_translation_note"

class DutchEditorWordingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = catalogues.catalogue_paths()['nl']
        cls.xml = {'nl': path.read_text()}
        cls.strings = {'nl': catalogues.read_strings(path)}

    def test_allocation_names_memory_and_does_not_claim_automatic_resize(self):
        value = self.strings['nl'][MEMORY]
        self.assertIn('geheugen', value)
        self.assertIn('niet automatisch verkleind', value.lower())

    def test_resize_reason_keeps_both_causes_copy_target_and_unchanged_original(self):
        value = self.strings['nl'][RESIZE]
        self.assertIn('of Android', value)
        self.assertIn('een kopie', value)
        self.assertIn('oorspronkelijke bestand blijft ongewijzigd', value)

    def test_language_note_explains_maintenance_and_english_fallback_without_claiming_completeness(self):
        value = self.strings['nl'][NOTE]
        self.assertIn('Nieuwe of onvertaalde', value)
        self.assertIn('Engels', value)
        self.assertEqual(2, value.count('\\n'))
        self.assertNotIn('alle vertaalbare interfacetekst', value)

    def test_encoder_reports_unfinished_operation(self):
        self.assertIn('niet voltooid', self.strings['nl']['ui_the_encoder_did_not_finish'])

    def test_ellipse_is_a_drawing_tool_and_is_distinct_from_selection(self):
        strings = self.strings['nl']
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        document = (classic / 'PaintDocument.kt').read_text()
        categories = (classic / 'ToolCategoryButton.kt').read_text()
        self.assertRegex(document, r'ELLIPSE\(R\.string\.ui_ellipse\s*,')
        insert = re.search(r'INSERT\(R\.string\.ui_category_insert,listOf\((.*?)\)\)', categories, re.S)
        self.assertIsNotNone(insert)
        self.assertIn('PaintTool.ELLIPSE', insert.group(1))
        self.assertNotIn('PaintTool.SELECT', insert.group(1))

    def test_count_label_is_number_neutral_and_unit_labels_compose_in_lowercase(self):
        strings = self.strings['nl']
        self.assertEqual('%1$d × %2$d px · Aantal pixels: %3$,d (%4$.2f MP)', strings[COUNT])
        self.assertEqual('pixels', strings['ui_pixels_6ec9c2'])
        # Host-side text composition, not Android/TalkBack execution.
        for key, expected in (('ui_width_in', 'Breedte in pixels'),
                              ('ui_height_in', 'Hoogte in pixels')):
            self.assertEqual(expected, strings[key].replace('%1$s', strings['ui_pixels_6ec9c2']))

    def test_save_choices_and_colour_abbreviations_keep_distinct_roles(self):
        strings = self.strings['nl']
        self.assertEqual(3, len({strings[k] for k in ('ui_save_a5d0d9', 'ui_discard_changes23', 'ui_keep_editing23')}))
        self.assertNotEqual(strings['ui_fg'], strings['ui_bg'])

    def test_colour_swap_names_both_actual_colour_roles(self):
        value = self.strings['nl']['ui_swap_foreground_background']
        self.assertIn('Voorgrond', value)
        self.assertIn('achtergrondkleur', value)

if __name__ == '__main__':
    unittest.main()
