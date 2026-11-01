"""Current Hakka/Wu conditional crop meaning and real argument consumers."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class HakkaWuCropTests(unittest.TestCase):
    def test_attached_other_images_may_move_with_typed_reference_dimensions(self):
        for tag, clauses in (
            ('hak-Hant-TW', ('接到該張圖像个其他圖像', '可能會徙')),
            ('hak-Latn-TW', ('chiap to ke chông thù-siong', 'nang-ngoi thù-siong', 'khó-nèn voi sái')),
            ('wuu-Hans', ('接牢搿张图片个图片', '有可能会移位')),
        ):
            items = ET.parse(catalogues.catalogue_paths()[tag]).findall("./plurals[@name='ui_crop_preview_images']/item")
            self.assertEqual(['other'], [n.get('quantity') for n in items])
            value = items[0].text
            self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$d': 1}, catalogues.placeholders(value))
            for clause in clauses:
                self.assertIn(clause, value)

if __name__ == "__main__":
    unittest.main()
