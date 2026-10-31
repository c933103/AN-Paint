"""Current Korean attribution, script and consumer semantics, not approval snapshots."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
from test_assembly_help_pr8 import code_locations, kotlin_block

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
KP = 'values-b+ko+KP'
DIRECTORIES = (KP, 'values-b+ko+KR', 'values-b+ko+Kore+KR')
MANUAL = 'ui_the_arrow_on_the_left_directly_below_the'
ASSEMBLY = 'ui_add_up_to_20_images_with_android_s'
CROP = 'ui_crop_preview_images'
PARTICLE = 'ui_d_d_pixels_2f_mp_exceeds_the_current'


class KoreanImageAttributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kp = catalogues.read_strings(RES / KP / 'strings.xml')

    def test_attribution_is_not_financial_credit_or_general_acknowledgements(self):
        for key in ('ui_image_credits', 'gallery_copy_credit', 'gallery_edit_credits',
                    'legacy_credits_title', 'legacy_credits_hint'):
            value = self.kp[key]
            self.assertIn('저작자·출처 정보', value)
            self.assertNotIn('감사의 말', value)
            self.assertNotIn('신용', value)
        self.assertIn('감사의 말', self.kp['ui_about_credits23'])
        self.assertNotEqual(self.kp['ui_about_credits23'], self.kp['ui_image_credits'])
        self.assertIn(self.kp['ui_about_credits23'], self.kp[ASSEMBLY])
        self.assertIn('MP)는', self.kp[PARTICLE])
        self.assertNotIn('MP)은', self.kp[PARTICLE])

    def test_crop_and_assembly_conditionally_move_attached_images_in_each_script(self):
        for directory in DIRECTORIES:
            root = ET.parse(RES / directory / 'strings.xml').getroot()
            crop = root.find("./plurals[@name='ui_crop_preview_images']/item[@quantity='other']").text
            help_text = root.find(f"./string[@name='{ASSEMBLY}']").text
            attached = '련결된 화상' if directory == KP else ('連結된 이미지' if 'Kore' in directory else '연결된 이미지')
            self.assertIn(attached, crop)
            self.assertIn('조정될 수 있습니다.', crop)
            self.assertNotIn('조정됩니다.', crop)
            crop_clauses = [part for part in help_text.split('. ') if attached in part and '자르면' in part]
            self.assertEqual(1, len(crop_clauses))
            self.assertIn('이동할수 있습니다.' if directory == KP else '이동할 수 있습니다.', crop_clauses[0] + '.')
            self.assertNotIn('이동합니다.', crop_clauses[0] + '.')
            if 'Kore' in directory:
                self.assertIn('配置', crop)
                self.assertIn('位置', crop)

    def test_dependent_routes_and_copy_edit_captions_match_actual_labels(self):
        parts = [self.kp[k] for k in ('ui_menu_file', 'ui_about_credits23', 'ui_image_credits')]
        for key, separator in (
            ('gallery_description', ' → '),
            ('ui_catrobat_s_own_artwork_uses_cc_by_sa', ' > '),
            (MANUAL, ' > '), ('ui_irasutoya_help34', ' → '),
            ('ui_openclipart_help34', ' → '),
        ):
            with self.subTest(key=key):
                self.assertEqual(1, self.kp[key].count(separator.join(parts)))
        for key in ('gallery_copy_credit', 'gallery_edit_credits'):
            self.assertEqual(1, self.kp['gallery_description'].count(self.kp[key]))
        self.assertEqual('화상 저작자·출처 정보', self.kp['ui_image_credits'])
        self.assertEqual('저작자·출처 정보 복사', self.kp['gallery_copy_credit'])
        self.assertEqual('저작자·출처 정보 편집', self.kp['gallery_edit_credits'])

    def test_production_parent_submenu_and_caption_routes(self):
        classic = (CLASSIC / 'ClassicPaintActivity.kt').read_text()
        about = kotlin_block(classic, 'private fun showAboutOptions() {')
        for source, fragment in (
            (classic, 'ui(R.string.ui_about_credits23) to {showAboutOptions()}'),
            (about, 'ui(R.string.ui_image_credits) to {showImageCredits()}'),
            (about, 'setScrollableTitle(ui(R.string.ui_about_credits23))'),
            ((CLASSIC / 'GalleryCredits.kt').read_text(),
             'EditorDialogBuilder(activity).setTitle(ui(R.string.ui_image_credits))'),
            ((CLASSIC / 'GalleryCredits.kt').read_text(),
             '.setNegativeButton(ui(R.string.gallery_copy_credit),null)'),
            ((CLASSIC / 'MediaGalleryActivity.kt').read_text(),
             'action(ui(R.string.gallery_edit_credits),"gallery_edit_credits") {showCreditEditor()}'),
            ((CLASSIC / 'MediaGalleryActivity.kt').read_text(),
             'IllustrationPage.script(provider,ui(R.string.gallery_use_image),ui(R.string.gallery_copy_credit))'),
        ):
            with self.subTest(fragment=fragment):
                self.assertTrue(code_locations(source, fragment))

    def test_crop_and_help_source_routes_keep_active_and_dormant_text_distinct(self):
        assembly = (CLASSIC / 'AssemblyActivity.kt').read_text()
        crop = (CLASSIC / 'ImageCropDialog.kt').read_text()
        self.assertTrue(code_locations(assembly, 'private fun showHelp() = message(ui(R.string.' + ASSEMBLY + '))'))
        guarded = ('status.text = uiQuantity(activity.resources,'
                   'R.plurals.ui_crop_preview_images,count,crop.width(),crop.height(),count)')
        def require_guarded(source): self.assertTrue(code_locations(source, guarded))
        require_guarded(crop)
        with self.assertRaises(AssertionError):
            require_guarded(crop.replace('uiQuantity(activity.resources,', 'activity.resources.getQuantityString('))
        classic = (CLASSIC / 'ClassicPaintActivity.kt').read_text()
        self.assertTrue(code_locations(classic, 'private fun showHelp() = message(ui(R.string.ui_help23))'))
        for path in CLASSIC.glob('*.kt'):
            self.assertFalse(code_locations(path.read_text(), 'R.string.' + MANUAL), path.name)

if __name__ == "__main__":
    unittest.main()
