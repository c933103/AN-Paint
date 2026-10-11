"""Exact accepted producer disposition; host checks are not combined runtime acceptance."""
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import dialog_colour_composition_scope as composition
from app_instrumentation_matrix import DIALOG, COLOUR, DIALOG_IDENTITIES, PHASE_TIMEOUTS, app_partition
from run_android_instrumentation import declared_tests

ROOT = Path(__file__).resolve().parents[1]


class DialogColourCompositionContracts(unittest.TestCase):
    def test_sources_and_historical_pr52_paths_have_pinned_endpoints(self):
        scope = composition.scope()
        self.assertEqual(scope['sources']['pr52']['commit'], '2755e30573d6ea2c071a128b6fa2940fc675af1a')
        self.assertEqual(scope['sources']['pr51']['commit'], '512360bffef3abb393557bce29a30217b03c5ecc')
        self.assertEqual(261, len(scope['pr52_changed_paths']))
        for row in scope['pr52_changed_paths']:
            with self.subTest(path=row['path']):
                self.assertEqual(row['sha256'], composition.digest(composition.before_colour_composition(
                    row['path'], (ROOT/row['path']).read_bytes())))

    def test_only_accepted_colour_production_changes_from_pr52(self):
        scope = composition.scope()
        actual = {str(p.relative_to(ROOT)) for module in ('Paintroid', 'app')
                  for p in (ROOT/module/'src/main').rglob('*') if p.is_file()}
        self.assertEqual(actual, {row['path'] for row in scope['production']})
        changed = [r for r in scope['production'] if r['pr52_sha256'] != r['combined_sha256']]
        self.assertEqual([r['path'] for r in changed],
                         ['Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt'])
        self.assertEqual(changed[0]['combined_sha256'], scope['accepted_colour_production_sha256'])
        for row in scope['production']:
            self.assertEqual(row['combined_sha256'], composition.digest((ROOT/row['path']).read_bytes()))

    def test_full_colour_source_is_exact_class_only_rename_of_accepted_pr51(self):
        row = composition.scope()['class_rename']
        original = (ROOT/row['original_path']).read_bytes()
        self.assertEqual(row['original_sha256'], composition.digest(original))
        current = (ROOT/row['path']).read_text()
        self.assertEqual(1, current.count(row['after']))
        self.assertEqual(0, current.count(row['before']))
        self.assertEqual(original, current.replace(row['after'], row['before'], 1).encode())
        model=ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/AdvancedColourViewportTest.kt'
        self.assertEqual(composition.scope()['accepted_colour_jvm_sha256'], composition.digest(model.read_bytes()))

    def test_retired_negative_method_is_preserved_and_unrelated_notice_source_is_exact(self):
        scope = composition.scope(); row = scope['retired_negative']
        retired = (ROOT/row['fragment_path']).read_bytes()
        self.assertEqual(row['fragment_sha256'], composition.digest(retired))
        current = (ROOT/row['source_path']).read_bytes()
        self.assertNotIn(row['name'].encode(), current)
        self.assertEqual(current.count(row['anchor'].encode()), 1)
        restored = current.replace(row['anchor'].encode(), retired+row['anchor'].encode(), 1)
        self.assertEqual(restored, composition.before_colour_composition(row['source_path'], current))
        self.assertEqual(4, len(re.findall(rb'@Test fun (\w+)', current)))

    def test_changed_endpoints_and_fixture_corruption_fail_closed(self):
        for row in composition.scope()['replaced_pr52_paths']:
            with self.subTest(path=row['path']), self.assertRaises(ValueError):
                composition.before_colour_composition(row['path'], (ROOT/row['path']).read_bytes()+b'\n')
        with tempfile.TemporaryDirectory() as folder:
            corrupt=Path(folder)/'scope.json';corrupt.write_bytes(composition.FIXTURE.read_bytes()+b'\n')
            with patch.object(composition,'FIXTURE',corrupt),self.assertRaises(ValueError):composition.scope()

    def test_expected_jvm_union_adds_only_six_strict_colour_identities(self):
        raw=(ROOT/'verification/dialog-colour-composition-2026-10-11/expected-jvm-union.json').read_bytes()
        self.assertEqual('a399cd5eb0f87f22b0dd928c7cfe82ed73d5ec50d206d7e559d73074e24aaa5a', composition.digest(raw))
        union=json.loads(raw)
        self.assertEqual(859, union['expected_count'])
        self.assertEqual(859, len({tuple(row) for row in union['expected']}))
        self.assertEqual(6, len(union['pr51_additions_to_pr52']))
        self.assertEqual({'org.catrobat.paintroid.local.AdvancedColourViewportTest'},
                         {owner for owner,_ in union['pr51_additions_to_pr52']})

    def test_explicit_installed_identity_disposition_and_deadlines(self):
        app=ROOT/'app/src/androidTest'; native=ROOT/'Paintroid/src/androidTest'
        self.assertEqual(7, len(DIALOG_IDENTITIES))
        self.assertEqual({DIALOG,COLOUR}, {owner for owner,_ in DIALOG_IDENTITIES})
        self.assertNotIn((DIALOG,'unchangedAdvancedColourReportsShortLandscapeLimitation'), DIALOG_IDENTITIES)
        for sdk, selected, native_count, suppressed in ((30,22,73,8),(35,32,74,0)):
            methods=declared_tests(app,sdk_level=sdk);parts=app_partition(methods,sdk)
            self.assertEqual(selected, sum(map(len,parts.values())))
            self.assertEqual(native_count,len(declared_tests(native,sdk_level=sdk)))
            self.assertEqual(suppressed,len(declared_tests(app)-methods))
            if sdk==35:self.assertEqual(DIALOG_IDENTITIES,parts['dialog'])
        self.assertEqual(300,PHASE_TIMEOUTS['dialog'])
        self.assertEqual(180,PHASE_TIMEOUTS['ordinary'])
        self.assertEqual(90,PHASE_TIMEOUTS['gallery-draft'])
        for name in ('LocalizedDialogDeviceTest.kt','ColourViewportDeviceTest.kt'):
            text=(app/'java/paint/anpaint/android'/name).read_text()
            self.assertIn('45000',text)
            self.assertIn('@SdkSuppress(minSdkVersion=35,maxSdkVersion=35)',text)


if __name__ == '__main__':unittest.main()
