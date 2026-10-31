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

    def test_actual_consumer_passes_reference_crop_dimensions_and_selected_image_count(self):
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        dialog = (classic / 'ImageCropDialog.kt').read_text()
        self.assertIn('val count = images.count { it.id in selected }', dialog)
        self.assertIn('uiQuantity(activity.resources,R.plurals.ui_crop_preview_images,count,crop.width(),crop.height(),count)', dialog)
        model = (classic / 'ImageAssembly.kt').read_text()
        self.assertIn('val parent = resolve(byId[a.anchor]', model)
        self.assertIn('x = if (a.edge == SnapEdge.RIGHT) parent.right else parent.left', model)
        self.assertIn('y = if (a.edge == SnapEdge.BOTTOM) parent.bottom else parent.top', model)

if __name__ == "__main__":
    unittest.main()
