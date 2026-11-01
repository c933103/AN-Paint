"""TIFF compression semantics, not copied reviewed descriptions."""
import unittest
import translation_catalogues as catalogues

KEY = 'formats22_tiff_description'

class TiffDescriptionWordingTests(unittest.TestCase):
    def test_default_source_qualifies_size_but_keeps_pixels_and_unchecked_instruction(self):
        value = catalogues.read_strings(catalogues.RES / 'values/strings.xml')[KEY]
        for boundary in ('one RGB page', 'may reduce', 'without changing pixels', 'uncompressed TIFF'):
            self.assertIn(boundary, value)

    def test_current_descriptions_remain_argument_free(self):
        paths = {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}
        for tag, path in paths.items():
            values = catalogues.read_strings(path)
            if KEY in values:
                with self.subTest(tag=tag):
                    self.assertFalse(catalogues.placeholders(values[KEY]))

if __name__ == '__main__': unittest.main()
