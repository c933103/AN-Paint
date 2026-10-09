"""Source contracts only; production Activity/navigation assertions live in the JVM test."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ACTIVITY = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt'
TEST = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/GalleryBackDirectionTest.kt'


class GalleryBackDirectionContractTest(unittest.TestCase):
    def test_arrow_uses_effective_activity_direction_not_a_language_allowlist(self):
        source = ACTIVITY.read_text()
        self.assertIn('val backArrow=if(resources.configuration.layoutDirection==View.LAYOUT_DIRECTION_RTL) "→" else "←"', source)
        self.assertIn('galleryButton(this,backArrow,"gallery_back",verticalCaption=false)', source)
        self.assertNotIn('galleryButton(this,"←","gallery_back"', source)

    def test_existing_accessible_name_and_web_navigation_are_preserved(self):
        source = ACTIVITY.read_text()
        block = source.split('navigation.addView(galleryButton', 1)[1].split('val searchLabel=', 1)[0]
        self.assertIn('if(web.canGoBack()) web.goBack() else web.loadUrl(provider.home)', block)
        self.assertIn('contentDescription=ui(R.string.ui_gallery_back34)', block)
        self.assertNotIn('Locale.getDefault', block)

    def test_locale_changes_still_recreate_the_gallery(self):
        manifest = ET.parse(ROOT / 'Paintroid/src/main/AndroidManifest.xml').getroot()
        android = '{http://schemas.android.com/apk/res/android}'
        application = manifest.find('application')
        self.assertEqual('true', application.get(android + 'supportsRtl'))
        activity = next(a for a in application.findall('activity')
                        if a.get(android + 'name') == '.classic.MediaGalleryActivity')
        changes = activity.get(android + 'configChanges').split('|')
        self.assertNotIn('locale', changes)
        self.assertNotIn('layoutDirection', changes)

    def test_runtime_fixture_covers_every_offered_tag_and_retains_independent_rtl_oracle(self):
        source = TEST.read_text()
        tags = {i.text for i in ET.parse(ROOT / 'Paintroid/src/main/res/values/app_language_tags.xml')
                .find('string-array').findall('item')}
        declared = re.search(r'private val rtlTags=setOf\((.*?)\)', source).group(1)
        rtl = set(re.findall(r'"(.*?)"', declared))
        self.assertEqual({'ar', 'ckb', 'fa', 'fa-IR', 'he', 'ps', 'sd', 'ug', 'ur', 'yi'}, rtl)
        self.assertTrue(rtl <= tags)
        self.assertIn('for((index,tag) in tags.withIndex())', source)
        self.assertIn('controller.pause().stop().saveInstanceState(state).destroy()', source)
        self.assertIn('controller=open(IllustrationSource.COMMONS,state)', source)
        self.assertIn('syntheticResourceMutationKeepsTheOldLocaleCacheKey', source)
        self.assertIn('browser.pushEntryToHistory', source)
        self.assertIn('assertEquals(1,browser.goBackInvocations)', source)
        self.assertIn('"" to "→"', source)
        self.assertIn('ReplacementSpan::class.java', source)
        self.assertNotIn('setCanGoBack(', source)
        self.assertNotIn('openConnection(', source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
