"""Source-bound installed Korean consumer contracts and corrupt-export controls.

Host models check the harness, never substitute for real emulator screenshots.
"""
import copy
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

from app_instrumentation_matrix import DIALOG, DIALOG_METHODS, PHASE_TIMEOUTS, app_partition
from dialog_evidence_transport import (KOREAN_METHODS, KOREAN_EXPECTATIONS, METHOD_SCREENS,
                                       verify_receipt)
from run_android_instrumentation import declared_tests
from test_assembly_help_pr8 import code_locations, kotlin_block
from test_dialog_evidence_transport import DIGEST, observation, receipt

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'app/src/androidTest/java/paint/anpaint/android/LocalizedDialogDeviceTest.kt'


class KoreanConsumerDeviceContracts(unittest.TestCase):
    def test_expectations_bind_complete_current_resources_and_reviewed_changed_values(self):
        expected = json.loads(KOREAN_EXPECTATIONS.read_text(encoding='utf-8'))
        reviewed = json.loads((ROOT / 'tools/fixtures/current_localization/korean_image_attribution.json').read_text())
        reviewed_values = {(e['directory'], e['key']): e['value'].replace(r'\n', '\n') for e in reviewed['entries']}
        self.assertEqual({'ko-KP', 'ko-KR', 'ko-Kore-KR'}, set(expected))
        for tag, entries in expected.items():
            directory = 'values-b+' + tag.replace('-', '+')
            xml = ET.parse(ROOT / 'Paintroid/src/main/res' / directory / 'strings.xml').getroot()
            self.assertEqual({'resource_tag', 'ui_image_credits', 'gallery_copy_credit', 'ui_crop_preview_images'}, set(entries))
            self.assertEqual(tag + ('-anpaint' if tag == 'ko-Kore-KR' else ''), entries['resource_tag'])
            for key in ('ui_image_credits', 'gallery_copy_credit', 'ui_crop_preview_images'):
                with self.subTest(tag=tag, key=key):
                    path = f"./plurals[@name='{key}']/item[@quantity='other']" if key == 'ui_crop_preview_images' else f"./string[@name='{key}']"
                    self.assertEqual(xml.find(path).text.replace(r'\n', '\n'), entries[key])
                    if (directory, key) in reviewed_values:
                        self.assertEqual(reviewed_values[directory, key], entries[key])
            self.assertIn('조정될 수 있습니다.', entries['ui_crop_preview_images'])
        self.assertNotEqual(expected['ko-KR']['gallery_copy_credit'], expected['ko-Kore-KR']['gallery_copy_credit'])

    def test_real_picker_and_dialog_consumers_keep_bounded_synthetic_scope(self):
        source = SOURCE.read_text()
        bindings = dict(re.findall(r'@Test fun (\w+)\(\)=koreanConsumers\("([^"]+)"\)', source))
        self.assertEqual(KOREAN_METHODS, bindings)
        consumers = kotlin_block(source, 'private fun koreanConsumers(tag: String)=fixture("en-US",1f) {')
        picker = kotlin_block(source, 'private fun chooseKoreanLanguage(tag: String,resourceTag: String) {')
        for fragment in ('chooseKoreanLanguage(tag,expected.getString("resource_tag"))',
                         'activity.document.attachImageCredit(credit)', 'openAbout()',
                         'tapRow(onMain {aboutList()},expected.getString("ui_image_credits"))',
                         'ImageCropDialog(activity,images,{bitmap},{applications++}).show()',
                         'position=ImagePosition(0,0)', 'attachment=Attachment("korean-base",SnapEdge.RIGHT)',
                         'root.findViewWithTag<EditText>("crop_left").setText("2")',
                         'checkCrop(1)', 'checkCrop(2)',
                         'tap("korean crop include linked"', 'tap("korean crop cancel"',
                         'nativeBack("korean-credit-discard"',
                         '.put("copy_scope","display-accessibility-layout-only")'):
            self.assertTrue(code_locations(consumers, fragment), fragment)
        for fragment in ('original.onItemClick(parent,view,position,id)', 'tap("korean language row",row)',
                         'getString("language-tag",null)==tag', 'applicationLocales.toLanguageTags()==tag',
                         'configuration.locales[0].toLanguageTag()==resourceTag'):
            self.assertTrue(code_locations(picker, fragment), fragment)
        for forbidden in ('.performClick(', 'AppLanguage.select(', 'putString("language-tag"', 'createConfigurationContext'):
            self.assertFalse(code_locations(picker, forbidden), forbidden)
        self.assertFalse(code_locations(consumers, 'setText(expected'))
        self.assertFalse(code_locations(consumers, 'tap("credit copy"'))
        self.assertIn('assertEquals("Complete accessible consumer text: $key",expected,node.text.toString())', source)
        self.assertIn('try {revealText(view)} finally {measuredConsumerKey=null}', source)
        self.assertIn('SystemClock.uptimeMillis()<deadline', source)
        self.assertEqual(300, PHASE_TIMEOUTS['dialog'])
        self.assertIn('deadline=started+45000', source)

    def test_three_cases_are_required_once_on_api35_and_suppressed_on_api30(self):
        identities = {(DIALOG, method) for method in KOREAN_METHODS}
        for sdk in (30, 35):
            eligible = declared_tests(ROOT / 'app/src/androidTest', sdk_level=sdk)
            phases = app_partition(eligible, sdk)
            self.assertEqual(identities if sdk == 35 else set(), eligible & identities)
            if sdk == 35:
                self.assertTrue(identities <= phases['dialog'])
                self.assertFalse(identities & set.union(*(value for key, value in phases.items() if key != 'dialog')))
        self.assertTrue(set(KOREAN_METHODS) <= DIALOG_METHODS)
        for method in KOREAN_METHODS:
            self.assertEqual(['0-korean-attribution-title.png', '1-korean-attribution-copy.png',
                              '2-korean-crop-one.png', '3-korean-crop-two.png'], METHOD_SCREENS[method])

    def test_korean_exports_reject_wrong_locale_text_counts_scope_and_missing_consumer_layout(self):
        for method in KOREAN_METHODS:
            valid = receipt(method)
            verify_receipt(valid, method, DIGEST)
            changes = [
                lambda r: observation(r, 'korean-picker-selection').update(locale='ko-KR-wrong'),
                lambda r: observation(r, 'korean-picker-selection').update(platform_locale='en-US'),
                lambda r: observation(r, 'korean-picker-selection').update(resource_locale='en-US'),
                lambda r: observation(r, 'korean-picker-selection').update(selected_index=0),
                lambda r: observation(r, 'korean-crop-state').update(width=24),
                lambda r: observation(r, 'korean-crop-state').update(count=2),
                lambda r: observation(r, 'korean-crop-state').update(linked_peer=False),
                lambda r: observation(r, 'korean-consumers-complete').update(copy_scope='clipboard-tested'),
                lambda r: observation(r, 'korean-consumers-complete').update(applications=1),
                lambda r: observation(r, 'korean-consumers-complete').update(crop_cancelled=False),
                lambda r: observation(r, 'native-back-after')['state'].update(synthetic_credit_unchanged=False),
                lambda r: r['screenshots'].pop(),
            ]
            for index in range(4):
                def caption(r, index=index):
                    return [o for o in r['observations'] if o['kind'] == 'korean-consumer-caption'][index]
                changes.extend([
                    lambda r, caption=caption: caption(r).update(text=caption(r)['text'][:-1]),
                    lambda r, caption=caption: caption(r).update(accessible_text='truncated'),
                ])
            for kind in ('intrinsic-caption', 'caption-line-reached'):
                changes.append(lambda r, kind=kind: r.update(observations=[o for o in r['observations']
                    if not (o['kind'] == kind and o.get('consumer_key') == 'gallery_copy_credit')]))
            for index, change in enumerate(changes):
                mutated = copy.deepcopy(valid)
                change(mutated)
                with self.subTest(method=method, mutation=index):
                    with self.assertRaises(ValueError):
                        verify_receipt(mutated, method, DIGEST)


if __name__ == '__main__':
    unittest.main()
