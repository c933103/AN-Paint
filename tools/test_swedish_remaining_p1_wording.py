"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import translation_catalogues as catalogues

class SwedishRemainingP1WordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strings = catalogues.read_strings(catalogues.RES / 'values-sv/strings.xml')

    def test_actual_navigation_names_and_action_distinctions(self):
        s = {key: value.strip('"') for key, value in self.strings.items()}
        self.assertEqual(f"Kopiera ett område eller välj {s['ui_draw26']} → {s['ui_category_insert']} → {s['ui_other_images34']}.",
                         s['ui_paste_hint34'])
        self.assertIn(f"I läget {s['ui_navigate']}", s['ui_drawing_canvas_pinch_and_move_two_fingers_to'])
        self.assertEqual('Anpassa bilden till ritytan', s['ui_fit_selection34'])
        self.assertEqual('Fäst markeringen', s['ui_commit_selection'])
        self.assertEqual('Radera markeringen', s['ui_delete_selection'])
        self.assertNotEqual(s['ui_apply_crop'], s['ui_reset_crop'])
        self.assertEqual(('Alla', 'Inga'), (s['ui_all'], s['ui_none']))

    def test_no_automatic_resize_or_success_is_invented(self):
        s = self.strings
        for key, clause in {
            'colour_converter_unavailable': 'Bilden importerades inte.',
            'commons_svg_original_size_too_large': 'Ingen storleksändring gjordes.',
            'commons_svg_original_size_unavailable': 'Ingen storlek baserad på ritytan användes i stället.',
            'ui_the_full_image_and_working_buffers_exceed_the': 'Originalfilen förblir oförändrad.',
            'ui_choose_a_smaller_output_copy_the_source_images': 'Källbilderna och beskärningsinställningarna behålls i originalupplösningen.',
            'ui_codec_resize_memory_floor': 'Även en mindre utdatabild kan kräva mer minne',
            'ui_no_resize_fits_decoder_memory': 'Avbryt och använd en mindre källbild.',
        }.items():
            with self.subTest(key=key): self.assertIn(clause, s[key])
        self.assertIn('512 MiB', s['formats22_import_limit'])
        self.assertIn('bilddata som Base64-text', s['ui_this_file_is_not_a_supported_image_use'])
        self.assertNotIn('bildtext', s['ui_this_file_is_not_a_supported_image_use'])

    def test_palette_gestures_and_geometry_remain_distinct(self):
        s = self.strings
        palette = s['ui_foreground_background_colour_palette']
        self.assertIn('Förgrundsfärg', palette)
        self.assertIn('bakgrundsfärg', palette)
        for key in ('ui_colour_palette_tap_for_foreground_hold_for_background',
                    'ui_colour_tap_foreground_hold_background'):
            self.assertIn('Tryck för att välja förgrundsfärg.', s[key])
            self.assertIn('Tryck och håll för att välja bakgrundsfärg.', s[key])
        self.assertEqual('Beskärningsområdet måste ligga inom ritytan.', s['ui_crop_must_stay_inside_the_canvas'])
        self.assertEqual('Beskärningsområdet måste ligga inom bilden.', s['ui_the_crop_must_stay_inside_the_image'])
        self.assertIn('minst en bildpunkt', s['ui_the_crop_must_contain_at_least_one_pixel'])
        self.assertIn('noll eller större', s['ui_trim_amounts_must_be_zero_or_greater'])
        self.assertEqual(r'%1$.0f × %2$.0f px\n%3$.1f°', s['ui_0f_0f_px_1f'])

if __name__ == '__main__':
    unittest.main()
