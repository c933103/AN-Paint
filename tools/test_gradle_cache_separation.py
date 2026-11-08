"""Structural contracts for the exact-key Gradle-only fallback (not runtime cache proof)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/android.yml').read_text()
NAME = '      - name: Restore exact Gradle dependencies independently of native fetch scripts\n'

class GradleCacheSeparationTest(unittest.TestCase):
    def test_both_producers_restore_before_preparation(self):
        for job in ('checks', 'build'):
            source = WORKFLOW.split('\n  ' + job + ':\n', 1)[1]
            import re
            source = re.split(r'\n  [a-z][a-z-]*:\n', source, maxsplit=1)[0]
            # Job blocks have four-space fields; split at next two-space job.
            self.assertEqual(source.count(NAME), 1)
            self.assertLess(source.index(NAME), source.index('      - name: Prepare build tools and notices'))
            # Restored WebP has build.gradle; evaluating **/*.gradle after restore changes the key.
            self.assertLess(source.index(NAME), source.index('            Paintroid/build/jxl-source'))
            step = source.split(NAME, 1)[1].split('      - ', 1)[0]
            self.assertIn('uses: actions/cache/restore@55cc8345863c7cc4c66a329aec7e433d2d1c52a9', step)
            self.assertNotIn('restore-keys:', step)
            self.assertNotIn('fetch_', step)
            self.assertNotIn('continue-on-error:', step)
            paths = step.split('          path: |\n', 1)[1].split('          key:', 1)[0]
            self.assertEqual([p.strip() for p in paths.splitlines() if p.strip()],
                             ['~/.gradle/caches/modules-2', '~/.gradle/wrapper/dists'])
            expected = "android-resource-deps-v1-${{ runner.os }}-${{ hashFiles('**/*.gradle', 'gradle/wrapper/gradle-wrapper.properties') }}"
            self.assertIn('key: ' + expected, step)
            resource_job = WORKFLOW.split('\n  exact-script-resources:\n', 1)[1].split('\n  build:\n', 1)[0]
            self.assertIn('key: ' + expected, resource_job)

    def test_native_cache_identity_still_includes_fetch_scripts(self):
        self.assertEqual(WORKFLOW.count("restore-keys: android-deps-v1-${{ runner.os }}-${{ hashFiles('**/*.gradle', 'gradle/wrapper/gradle-wrapper.properties', 'tools/fetch_*_sources.py') }}-"), 2)
        properties = (ROOT / 'gradle/wrapper/gradle-wrapper.properties').read_text()
        self.assertIn('distributionSha256Sum=20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78', properties)
