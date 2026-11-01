"""Count-neutral grammatical heads and typed slots, not approved chooser prose."""
import unittest
import translation_catalogues as catalogues

class CountWordingTest(unittest.TestCase):
    def test_english_overrides_do_not_restore_the_singular_defect(self):
        paths = catalogues.catalogue_paths()
        paths = {tag: path for tag, path in paths.items() if tag.startswith('en-')}
        paths['default'] = catalogues.RES / 'values/strings.xml'
        for tag, path in paths.items():
            values = catalogues.read_strings(path)
            for key, head in (
                ('ui_d_d_px_d_pixels_2f_mp', 'Pixel count: %3$,d'),
                ('formats22_page_description', 'Number of pages: %3$d'),
                ('ui_you_can_add_more_images_select_fewer_files', 'Number of images you can still add: %1$s'),
                ('ui_rendering_images', 'Images processed: %1$s / %2$s'),
            ):
                with self.subTest(tag=tag, key=key):
                    self.assertIn(head, values[key])

    def test_french_count_heads_and_argument_types(self):
        actual = catalogues.read_strings(catalogues.catalogue_paths()['fr'])
        source = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        for key, heads in (
            ('ui_d_d_px_d_pixels_2f_mp', ('Nombre de pixels : %3$,d',)),
            ('formats22_page_description', ('Nombre de pages : %3$d',)),
            ('ui_an_paint_image_assembly_20_images_placed', ('Images : %1$s', 'Images placées : %2$s')),
            ('ui_you_can_add_more_images_select_fewer_files', ('Nombre d’images pouvant encore être ajoutées : %1$s',)),
            ('ui_rendering_images', ('Images traitées : %1$s / %2$s',)),
        ):
            for head in heads:
                self.assertIn(head, actual[key])
            self.assertEqual(catalogues.placeholders(source[key]), catalogues.placeholders(actual[key]))

    def test_japanese_page_count_keeps_its_valid_invariant_wording(self):
        value = catalogues.read_strings(catalogues.catalogue_paths()['ja'])['formats22_page_description']
        self.assertIn('全%3$dページ', value)
        self.assertEqual({'%1$s': 1, '%2$s': 1, '%3$d': 1}, catalogues.placeholders(value))

if __name__ == '__main__':
    unittest.main()
