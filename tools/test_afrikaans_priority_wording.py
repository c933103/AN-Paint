"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class AfrikaansPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / path / 'strings.xml').read_text()
                   for tag, path in [('default', 'values'), ('af', 'values-b+af')]}
        cls.strings = {n.get('name'): ''.join(n.itertext())
                       for n in ET.fromstring(cls.xml['af']) if n.tag == 'string'}

    def test_encoder_failure_is_bound_to_failed_compression(self):
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        for filename in ('ImageExporter.kt', 'TextImageCodec.kt', 'IcoCodec.kt'):
            with self.subTest(filename=filename):
                source = (classic / filename).read_text()
                self.assertIn('compress(', source)
                self.assertIn('throw IOException(ui(R.string.ui_the_encoder_did_not_finish))', source)

    def test_live_lossless_checkbox_and_explanation_use_same_term(self):
        self.assertEqual('%1$s sonder verlies', self.strings['ui_lossless_format'])
        self.assertIn('Kompressie sonder verlies behou elke kleurwaarde.',
                      self.strings['ui_higher_quality_usually_makes_a_larger_file_lossless'])
        source = (catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt').read_text()
        self.assertIn('losslessBox.text=ui(R.string.ui_lossless_format,format.label)', source)
        self.assertIn('R.string.ui_higher_quality_usually_makes_a_larger_file_lossless', source)

    def test_sharing_warning_preserves_saved_state_and_error_slot(self):
        value = self.strings['ui_the_image_was_saved_but_android_could_not']
        self.assertTrue(value.startswith('Die beeld is gestoor, maar Android kon nie '))
        self.assertTrue(value.endswith('deelopsies oopmaak nie: %1$s'))
        self.assertEqual({'%1$s': 1}, catalogues.placeholders(value))
        source = (catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt').read_text()
        body = source.split('private fun shareSavedImage(', 1)[1].split('private fun exportSourceTo(', 1)[0]
        self.assertIn('startActivity(Intent.createChooser(send,ui(R.string.ui_share_saved_image)))', body)
        self.assertIn('message(ui(R.string.ui_the_image_was_saved_but_android_could_not, error.message))', body)

    def test_save_alias_and_foreground_background_roles_stay_distinct(self):
        self.assertEqual('@string/ui_save', self.strings['ui_save_a5d0d9'])
        self.assertNotEqual(self.strings['ui_fg'], self.strings['ui_bg'])

if __name__ == '__main__':
    unittest.main()
