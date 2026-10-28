"""Build-only variant workaround; installed picker tests prove framework resolution."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
OLD = 'values-b+ca+ES+valencia'
NEW = 'values-b+ca+Latn+ES+valencia'

class ValencianVariantPackagingTest(unittest.TestCase):
    def test_build_stages_all_resources_with_exact_variant_and_legacy_language_replacements(self):
        build = (ROOT / 'Paintroid/build.gradle').read_text()
        block = build.split("tasks.register('generateVariantSafeResources', Sync)", 1)[1].split('// Android infers Kore', 1)[0]
        self.assertEqual(["src/main/res", f"src/main/res/{OLD}", "src/main/res/values-b+yi"], re.findall(r"from\('([^']+)'\)", block))
        self.assertEqual([OLD + '/**', 'values-b+yi/**'], re.findall(r"exclude '([^']+)'", block))
        self.assertEqual([NEW, 'values-ji'], re.findall(r"into '([^']+)'", block))
        self.assertIn('actual.keySet() != expected.keySet()', block)
        self.assertIn('java.util.Arrays.equals(source.bytes, actual[relative].bytes)', block)
        self.assertIn('expected.put(target, source) != null', block)
        self.assertIn('android.sourceSets.main.res.setSrcDirs([variantSafeResourceDirectory])', block)
        self.assertIn("tasks.named('preBuild').configure { dependsOn(generateVariantSafeResources) }", block)
        self.assertIn('dependsOn(generateExactScriptResources, generateVariantSafeResources)', build)
        self.assertNotIn('filter(', block)
        self.assertNotIn('expand(', block)
        # Existing generated resources remain separate registered inputs after staging.
        for name in ('exactScriptResourceDirectory', 'sourceTextDirectory'):
            self.assertIn(f'android.sourceSets.main.res.srcDir({name})', build)
        self.assertLess(build.index('res.setSrcDirs'), build.index('res.srcDir(exactScriptResourceDirectory)'))

    def test_canonical_variant_and_parent_remain_only_editable_catalogues(self):
        res = ROOT / 'Paintroid/src/main/res'
        self.assertTrue((res / OLD / 'strings.xml').is_file())
        self.assertFalse((res / NEW).exists())
        app = (ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt').read_text()
        mapping = app.split('internal fun resourceLocale(',1)[1].split('    fun wrap(',1)[0]
        self.assertNotIn('valencia', mapping)
        self.assertIn('else chosen', mapping)
        self.assertIn('Aquesta imatge fa servir', (res/'values-ca/strings.xml').read_text())
        self.assertIn('Esta imatge utilitza', (res/OLD/'strings.xml').read_text())

    def test_sdk33_dispatch_is_not_mistaken_for_cldr48_catalogue_categories(self):
        source = (ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/TibetanDzongkhaValencianPriorityWordingTest.kt').read_text()
        method=source.split('fun compiledCropPluralUsesCompleteReviewedQuantityForOneTwoAndMany()',1)[1]
        self.assertIn('@Config(sdk = [33])', source)
        self.assertIn('val quantity=if(tag=="ca-ES-valencia" && count==1) "one" else "other"', method)
        self.assertIn('quantity,rules.select(count.toDouble())', method)
        self.assertIn('1_000_000,2_000_000',method)
        # The canonical many branch remains accepted and available for newer ICU.
        import xml.etree.ElementTree as E
        root=E.parse(ROOT/'Paintroid/src/main/res'/OLD/'strings.xml').getroot()
        plural=next(e for e in root if e.get('name')=='ui_crop_preview_images')
        self.assertEqual({'one','many','other'},{e.get('quantity') for e in plural})

    def test_installed_probe_uses_real_picker_and_rotation_without_replacing_expected_text(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/EditorDeviceTest.kt').read_text()
        method=source.split('fun valencianUsesItsWholeCatalogueAcrossRealPickerSwitchesAndRotation()',1)[1]
        for required in ('chooseAppLanguage("ca-ES-valencia")','chooseAppLanguage("ca")',
                         'config.screenWidthDp!=beforeWidth','config.screenHeightDp!=beforeHeight',
                         'Esta imatge utilitza','Aquesta imatge fa servir','val configured=tag',
                         '"Guarda" else "Desa"','"Public persisted identity"','"Public platform identity"'):
            self.assertIn(required,method)
        self.assertNotIn('.edit()',method)

if __name__=='__main__': unittest.main()
