"""Exact build-only Yiddish alias and live public-identity probe contracts.

Android ResourcesImpl adjusts yi to native ji even on API35. The canonical
catalogue/picker stay yi; standalone Gradle/AAPT and installed evidence are
separate gates, not inferred from these host source assertions.
"""
from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import current_display

ROOT = Path(__file__).resolve().parents[1]
METHOD = 'yiddishUsesItsWholeCatalogueAcrossRealPickerSwitchesAndRotation'


def require_staging(build):
    block=build.split("tasks.register('generateVariantSafeResources', Sync)",1)[1].split('// Android infers Kore',1)[0]
    if re.findall(r"from\('([^']+)'\)",block) != ['src/main/res','src/main/res/values-b+ca+ES+valencia','src/main/res/values-b+yi']:
        raise ValueError('Exact staged input identities differ')
    if re.findall(r"exclude '([^']+)'",block) != ['values-b+ca+ES+valencia/**','values-b+yi/**']:
        raise ValueError('Canonical source exclusions differ')
    if re.findall(r"into '([^']+)'",block) != ['values-b+ca+Latn+ES+valencia','values-ji']:
        raise ValueError('Exact compiled aliases differ')
    required=["relative.startsWith('values-b+yi/') ? relative.replaceFirst('values-b\\\\+yi/', 'values-ji/') : relative",
              'expected.put(target, source) != null','actual.keySet() != expected.keySet()',
              'java.util.Arrays.equals(source.bytes, actual[relative].bytes)',
              'android.sourceSets.main.res.setSrcDirs([variantSafeResourceDirectory])',
              "tasks.named('preBuild').configure { dependsOn(generateVariantSafeResources) }"]
    if any(value not in block for value in required):raise ValueError('Missing bijection/bytes/task invariant')
    if any(value in block for value in ('filter(', 'expand(')):raise ValueError('Staging must not transform resource contents')
    if 'dependsOn(generateExactScriptResources, generateVariantSafeResources)' not in build:
        raise ValueError('Source-text consumer must depend on staged producer')


def probe_method(source):
    signature='    @Test @SdkSuppress(minSdkVersion=35,maxSdkVersion=35)\n    fun '+METHOD+'()'
    if signature not in source:raise ValueError('Exact API35 probe absent')
    return source.split(signature,1)[1].split('    @Test ',1)[0]


def require_probe(source, yiddish, english):
    method=probe_method(source)
    for value in ('config.screenWidthDp!=beforeWidth','config.screenHeightDp!=beforeHeight',
                  'config.orientation==expectedOrientation','it.paintCanvas.width>0 && it.paintCanvas.height>0',
                  'it.resources.configuration.locales[0].toLanguageTag()==tag',
                  'Locale.getDefault().toLanguageTag()', 'applicationLocales.toLanguageTags()',
                  'getString("language-tag",null)', 'finally {onMain {it.requestedOrientation=originalOrientation}}'):
        if value not in method:raise ValueError('Missing live picker/rotation/identity contract')
    if re.findall(r'chooseAppLanguage\("([^"]+)"\)',method)!=['yi','en-US','yi']:
        raise ValueError('Real picker sequence differs')
    if re.findall(r'assertCatalogue\("([^"]+)"\)',method)!=['yi','yi','en-US','yi']:
        raise ValueError('All four unconditional exact phases required')
    for value in (yiddish['ui_save'],yiddish['save20_unsupported_image_colour'],english['save20_unsupported_image_colour']):
        if json.dumps(value,ensure_ascii=False) not in method:raise ValueError('Complete accepted control text differs')
    if '.edit(' in method or '.putString(' in method or 'catch(' in method or 'catch (' in method:
        raise ValueError('Probe must not seed selected preference or swallow failure')


class YiddishResourcePackagingTest(unittest.TestCase):
    def controls(self):
        yi={k:current_display('yi',k) for k in ('ui_save','save20_unsupported_image_colour')}
        en={e.get('name'):e.text for e in ET.parse(ROOT/'Paintroid/src/main/res/values-en-rUS/strings.xml').getroot()}
        return yi,en

    def test_exact_staging_preserves_public_catalogue_and_task_order(self):
        require_staging((ROOT/'Paintroid/build.gradle').read_text())
        res=ROOT/'Paintroid/src/main/res'
        self.assertTrue((res/'values-b+yi/strings.xml').is_file())
        self.assertFalse((res/'values-ji').exists())
        tags=[e.text for e in ET.parse(res/'values/app_language_tags.xml').getroot().find("./string-array[@name='app_language_tags']")]
        self.assertIn('yi',tags);self.assertNotIn('ji',tags)
        mapping=(ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt').read_text().split('internal fun resourceLocale(',1)[1].split('    fun wrap(',1)[0]
        self.assertNotIn('"yi"',mapping);self.assertNotIn('"ji"',mapping)

    def test_staging_rejects_missing_duplicate_wrong_or_content_changing_alias(self):
        build=(ROOT/'Paintroid/build.gradle').read_text()
        for old,new in [("exclude 'values-b+yi/**'",''),("into 'values-ji'","into 'values-yi'"),
                        ("from('src/main/res/values-b+yi')","from('src/main/res/values-b+yi')\n    from('src/main/res/values-b+yi')"),
                        ("relative.startsWith('values-b+yi/')","relative.startsWith('values-b+xx/')"),
                        ('actual.keySet() != expected.keySet()','false'),
                        ('java.util.Arrays.equals(source.bytes, actual[relative].bytes)','true'),
                        ('expected.put(target, source) != null','false'),
                        ('dependsOn(generateExactScriptResources, generateVariantSafeResources)','dependsOn(generateExactScriptResources)'),
                        ('    into variantSafeResourceDirectory','    filter(anything)\n    into variantSafeResourceDirectory')]:
            with self.subTest(old=old):
                self.assertIn(old,build)
                with self.assertRaises(ValueError):require_staging(build.replace(old,new,1))

    def test_installed_probe_asserts_complete_values_after_real_picker_rotation_and_reselection(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/EditorDeviceTest.kt').read_text()
        require_probe(source,*self.controls())

    def test_probe_rejects_lost_phase_wrong_text_or_fake_selection(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/EditorDeviceTest.kt').read_text();yi,en=self.controls()
        for old,new in [('assertCatalogue("yi")','assertCatalogue("en-US")'),
                        ('config.screenWidthDp!=beforeWidth','true'),
                        ('config.screenHeightDp!=beforeHeight','true'),
                        (json.dumps(yi['ui_save'],ensure_ascii=False),'"Save"'),
                        (json.dumps(yi['save20_unsupported_image_colour'],ensure_ascii=False),'"English fallback"'),
                        ('chooseAppLanguage("yi")','chooseAppLanguage("ji")')]:
            with self.subTest(old=old):
                self.assertIn(old,source)
                method=probe_method(source)
                self.assertIn(old,method)
                changed=source.replace(method,method.replace(old,new,1),1)
                with self.assertRaises(ValueError):require_probe(changed,yi,en)

if __name__=='__main__':unittest.main()
