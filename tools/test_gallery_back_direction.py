"""Source contracts only; production Activity/navigation assertions live in the JVM test."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ACTIVITY = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt'
TEST = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/GalleryBackDirectionTest.kt'

class GalleryBackDirectionContractTest(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main(verbosity=2)
