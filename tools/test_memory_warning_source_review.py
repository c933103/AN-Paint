"""Independent source-warning modality and remedies, not a translation approval queue."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

IMPORT = 'ui_no_resize_fits_decoder_memory'
ASSEMBLY = 'ui_assembly_source_memory_floor'

class MemoryWarningSourceReviewTests(unittest.TestCase):
    def test_import_warning_is_current_limit_failure_not_decoder_only_diagnosis(self):
        value = catalogues.read_strings(catalogues.RES / 'values/strings.xml')[IMPORT]
        for clause in ('smallest output size', 'cannot be loaded for editing',
                       'current memory limits', 'Cancel', 'smaller source image'):
            self.assertIn(clause, value)
        self.assertNotIn('decoder', value.casefold())

    def test_assembly_warning_is_combined_estimate_and_preserves_remedies_and_document(self):
        value = catalogues.read_strings(catalogues.RES / 'values/strings.xml')[ASSEMBLY]
        for clause in ('estimated', 'working-memory budget', 'smallest output size',
                       'dimensions alone is not enough', 'current limits',
                       'Close other documents', 'smaller source image', 'assembly is unchanged'):
            self.assertIn(clause, value)
        self.assertNotIn('decoder', value.casefold())

    def test_warning_sources_remain_unique_plain_scalars_without_format_arguments(self):
        root = ET.parse(catalogues.RES / 'values/strings.xml').getroot()
        for key in (IMPORT, ASSEMBLY):
            with self.subTest(key=key):
                nodes = root.findall(f"./*[@name='{key}']")
                self.assertEqual(1, len(nodes)); self.assertEqual('string', nodes[0].tag)
                self.assertEqual({'name': key}, nodes[0].attrib); self.assertEqual(0, len(nodes[0]))
                value = nodes[0].text
                self.assertFalse(catalogues.placeholders(value))
                self.assertEqual([], catalogues.android_string_errors(value))

if __name__ == '__main__': unittest.main()
