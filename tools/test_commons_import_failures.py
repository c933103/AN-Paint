"""Current failure-diagnostic distinctions; real routing/cleanup tests live in Kotlin."""
import unittest
import translation_catalogues as catalogues

DIAGNOSTICS = ('gallery_image_component_unavailable', 'gallery_external_link_no_handler',
               'ui_the_gallery_redirected_outside_its_supported_hosts',
               'ui_no_gallery_images_have_been_inserted')

class CommonsImportFailureContractTest(unittest.TestCase):
    def test_diagnostics_do_not_interpolate_private_urls_or_component_details(self):
        for tag, path in {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}.items():
            values = catalogues.read_strings(path)
            for key in DIAGNOSTICS:
                if key in values:
                    with self.subTest(tag=tag, key=key):
                        self.assertTrue(values[key])
                        self.assertFalse(catalogues.placeholders(values[key]))
            for generic, specific in (('gallery_image_component_unavailable', 'colour_converter_unavailable'),
                                      ('gallery_external_link_no_handler', 'gallery_load_error')):
                if generic in values and specific in values:
                    self.assertNotEqual(values[generic], values[specific], tag)

    def test_source_diagnoses_remain_neutral_and_do_not_blame_the_wrong_cause(self):
        values = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        credit = values['ui_no_gallery_images_have_been_inserted'].casefold()
        self.assertIn('credit', credit); self.assertNotIn('inserted', credit)
        component = values['gallery_image_component_unavailable'].casefold()
        self.assertIn('component', component); self.assertNotIn('provider', component)
        self.assertIn('converter', values['colour_converter_unavailable'].casefold())
        link = values['gallery_external_link_no_handler']
        for word in ('Android', 'app', 'link'):
            self.assertIn(word, link)

if __name__ == '__main__': unittest.main()
