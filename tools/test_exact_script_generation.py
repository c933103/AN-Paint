"""Tests of the probe's strict verdicts; these do not execute Gradle or Android."""
import pathlib
import tempfile
import unittest

import verify_exact_script_generation as probe

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ExactScriptGenerationProbeTests(unittest.TestCase):
    def test_byte_identical_mirror_passes_and_changed_or_stale_outputs_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            canonical = root / probe.CANONICAL
            generated = root / probe.GENERATED / probe.QUALIFIER
            canonical.mkdir(parents=True)
            generated.mkdir(parents=True)
            data = '<resources><string name="probe">複寫</string></resources>\n'.encode()
            (canonical / 'strings.xml').write_bytes(data)
            (generated / 'strings.xml').write_bytes(data)
            self.assertEqual({f'{probe.QUALIFIER}/strings.xml': probe.sha(data)}, probe.mirror_hashes(root))
            (generated / 'strings.xml').write_bytes(data + b' ')
            with self.assertRaisesRegex(AssertionError, 'differs'):
                probe.mirror_hashes(root)
            (generated / 'strings.xml').write_bytes(data)
            (generated / 'stale.xml').write_text('<resources/>')
            with self.assertRaisesRegex(AssertionError, 'stale'):
                probe.mirror_hashes(root)

    def test_missing_canonical_inputs_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(AssertionError, 'inputs are missing'):
                probe.mirror_hashes(pathlib.Path(directory))

    def test_generator_must_execute_once_before_every_requested_consumer(self):
        gen = f'> Task {probe.GENERATOR}\n'
        merges = ''.join(f'> Task {task}\n' for task in probe.MERGES)
        probe.require_generation_before(gen + merges, probe.MERGES)
        for bad in (merges, merges + gen, gen + gen + merges,
                    gen + f'> Task {probe.MERGES[0]}\n'):
            with self.subTest(log=bad), self.assertRaises(AssertionError):
                probe.require_generation_before(bad, probe.MERGES)

    def test_unchanged_probe_requires_up_to_date_and_mutation_requires_execution(self):
        up_to_date = f'> Task {probe.GENERATOR} UP-TO-DATE\n'
        probe.require_generation_before(up_to_date, (), up_to_date=True)
        with self.assertRaises(AssertionError):
            probe.require_generation_before(up_to_date, ())
        for state in ('', ' FROM-CACHE', ' SKIPPED', ' NO-SOURCE', ' FAILED'):
            with self.subTest(state=state), self.assertRaises(AssertionError):
                probe.require_generation_before(f'> Task {probe.GENERATOR}{state}\n', (), up_to_date=True)

    def test_installed_probe_uses_real_picker_rotation_and_both_strict_catalogues(self):
        source = (ROOT / 'app/src/androidTest/java/paint/anpaint/android/EditorDeviceTest.kt').read_text()
        method = source.split('fun mixedScriptKoreanUsesItsCatalogueAcrossRealPickerSwitchesAndRotation()', 1)[1]
        method = method.split('private fun restoreOriginalLanguage', 1)[0]
        self.assertEqual(2, method.count('chooseAppLanguage("ko-Kore-KR")'))
        self.assertIn('chooseAppLanguage("ko-KR")', method)
        self.assertIn('"複寫" else "복사"', method)
        self.assertIn('"貯藏" else "저장"', method)
        self.assertIn('config.screenWidthDp!=beforeWidth', method)
        self.assertIn('config.screenHeightDp!=beforeHeight', method)
        self.assertIn('applicationLocales.toLanguageTags()', method)
        self.assertNotIn('.edit()', method)
        self.assertNotIn('performClick', method)
        self.assertNotIn('onConfigurationChanged(', method)

    def test_workflow_keeps_probe_independent_and_always_retains_its_report(self):
        source = (ROOT / '.github/workflows/android.yml').read_text()
        job = source.split('  exact-script-resources:', 1)[1].split('  build:', 1)[0]
        self.assertIn('python3 tools/verify_exact_script_generation.py', job)
        self.assertIn('if: always()', job)
        self.assertIn('build/reports/exact-script-generation/', job)
        self.assertNotIn('needs:', job)
        self.assertNotIn('continue-on-error', job)

    def test_full_matrix_pr_label_reuses_the_existing_android_jobs(self):
        source = (ROOT / '.github/workflows/android.yml').read_text()
        matrix = source.split('      matrix:', 1)[1].split('    steps:', 1)[0]
        self.assertIn("contains(github.event.pull_request.labels.*.name, 'ci:full-android')", matrix)
        self.assertIn("'[30,35]' || '[35]'", matrix)
        self.assertIn("inputs.device_tests == 'full'", matrix)
        self.assertNotIn('codex/an-w05', matrix)

    def test_older_locale_checks_keep_independent_text_and_public_identity_oracles(self):
        directory = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local'
        picker = (directory / 'DeviceLanguagePickerTest.kt').read_text()
        expected = picker.split('private fun expectedLabel(', 1)[1].split('private fun checkRow(', 1)[0]
        self.assertIn('if(deviceTag=="ko-Kore-KR") "시스템 言語 使用"', expected)
        self.assertNotIn('AppLanguage.', expected)
        gallery = (directory / 'GalleryBackDirectionTest.kt').read_text()
        self.assertIn('if(tag=="ko-Kore-KR") "ko-Kore-KR-anpaint" else tag', gallery)
        self.assertIn('assertEquals(tag,AppLanguage.selectedTag(activity))', gallery)
        self.assertIn('assertEquals(tag,Locale.getDefault().toLanguageTag())', gallery)
        self.assertIn('applicationLocales.toLanguageTags()', gallery)
        self.assertIn('assertEquals(tags.size,records.length())', gallery)


if __name__ == '__main__':
    unittest.main()
