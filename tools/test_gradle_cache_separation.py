"""Structural contracts for the exact-key Gradle-only fallback (not runtime cache proof)."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/android.yml').read_text()
NAME = '      - name: Restore exact Gradle dependencies independently of native fetch scripts\n'

class GradleCacheSeparationTest(unittest.TestCase):
    def test_resource_job_restores_only_exact_build_dependency_archive(self):
        source = WORKFLOW.split('\n  exact-script-resources:\n', 1)[1].split('\n  build:\n', 1)[0]
        name = '      - name: Restore exact native-source dependency cache from APK builds\n'
        self.assertEqual(source.count(name), 1)
        step = source.split(name, 1)[1].split('      - ', 1)[0]
        build = WORKFLOW.split('\n  build:\n', 1)[1]
        producer = build.split('      - uses: actions/cache@', 1)[1].split('      - ', 1)[0]
        # Cache versions include the path list, not just the displayed key.
        def paths(block):
            return [line.strip() for line in block.split('          path: |\n', 1)[1]
                    .split('          key:', 1)[0].splitlines() if line.strip()]
        expected = ['~/.gradle/caches/modules-2', '~/.gradle/wrapper/dists',
                    'Paintroid/build/jxl-source', 'Paintroid/build/webp-source',
                    'Paintroid/build/heif-source', 'Paintroid/build/tiff-source']
        self.assertEqual(paths(step), expected)
        self.assertEqual(paths(producer), expected)
        cache_key = next(line.strip() for line in step.splitlines() if line.startswith('          key:'))
        self.assertIn(cache_key, producer)
        self.assertIn("'tools/fetch_*_sources.py'", cache_key)
        self.assertIn('uses: actions/cache/restore@55cc8345863c7cc4c66a329aec7e433d2d1c52a9', step)
        self.assertNotIn('restore-keys:', step)
        self.assertNotIn('continue-on-error:', step)
        self.assertNotIn('if:', step)
        self.assertLess(source.index('key: android-resource-deps-v1-'), source.index(name))
        self.assertLess(source.index(name), source.index('      - name: Prepare build tools and notices'))

    def test_cache_hit_or_miss_never_skips_resource_preparation_or_probe(self):
        source = WORKFLOW.split('\n  exact-script-resources:\n', 1)[1].split('\n  build:\n', 1)[0]
        for name, command, limit in (
                ('Prepare build tools and notices', 'bash tools/ci_prepare_build.sh', 8),
                ('Check clean and incremental resource graph in a disposable worktree',
                 'python3 tools/verify_exact_script_generation.py', 10)):
            step = source.split('      - name: ' + name + '\n', 1)[1].split('      - ', 1)[0]
            self.assertIn('run: ' + command, step)
            self.assertIn('timeout-minutes: ' + str(limit), step)
            self.assertNotIn('if:', step)
            self.assertNotIn('continue-on-error:', step)
        self.assertIn('    timeout-minutes: 20\n', source)

    def test_both_producers_restore_before_preparation(self):
        for job in ('checks', 'build'):
            source = WORKFLOW.split('\n  ' + job + ':\n', 1)[1]
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
