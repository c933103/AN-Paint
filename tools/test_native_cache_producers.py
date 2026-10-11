"""Immutable cache producers must not prevent other ABI/variant producers saving."""
from pathlib import Path
import itertools
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/android.yml').read_text()


def cache(job):
    source = WORKFLOW.split(f'\n  {job}:\n', 1)[1]
    source = source.split('      - name: Restore content-checked native compiler cache\n', 1)[1]
    return source.split('      - name:', 1)[0]


def key(job, variant):
    line = next(x.strip()[5:] for x in cache(job).splitlines() if x.startswith('          key: '))
    return re.sub(r"\$\{\{ hashFiles\(.*?\) \}\}", 'fixed-source-hash', line).replace('${{ env.BUILD_VARIANT }}', variant)


class NativeCacheProducerTest(unittest.TestCase):
    def test_primary_keys_are_distinct_for_both_producers_and_variants(self):
        keys = [key(job, variant) for job in ('checks', 'build') for variant in ('debug', 'release')]
        self.assertEqual(len(set(keys)), 4)
        self.assertTrue(key('checks', 'release').endswith('-release-checks-x86_64'))
        self.assertTrue(key('build', 'release').endswith('-release-universal'))

    def test_either_save_order_retains_each_producers_full_entry(self):
        for order in itertools.permutations(('checks', 'build')):
            saved = {}
            payloads = {'checks': {'x86_64'}, 'build': {'x86_64', 'x86', 'arm64-v8a', 'armeabi-v7a'}}
            for job in order:
                saved.setdefault(key(job, 'release'), payloads[job])
            self.assertEqual(saved[key('build', 'release')], payloads['build'])
            self.assertEqual(saved[key('checks', 'release')], payloads['checks'])
        # Negative control reproduces the old first-writer shared-key loss.
        old = {}
        old.setdefault('shared', {'x86_64'})
        old.setdefault('shared', payloads['build'])
        self.assertNotEqual(old['shared'], payloads['build'])

    def test_shared_restore_prefers_same_source_variant_and_keeps_legacy_fallback(self):
        restores = []
        for job in ('checks', 'build'):
            lines = cache(job).split('          restore-keys: |\n', 1)[1].splitlines()
            prefixes = [x.strip() for x in lines if x.strip()]
            self.assertEqual(len(prefixes), 3)
            self.assertIn("hashFiles('Paintroid/src/main/cpp/**', 'tools/fetch_*_sources.py')", prefixes[0])
            self.assertTrue(prefixes[0].endswith('${{ env.BUILD_VARIANT }}-'))
            self.assertEqual(prefixes[-1], 'native-ccache-v1-ubuntu22-4.5.1-')
            restores.append(prefixes)
        self.assertEqual(*restores)

    def test_no_run_identity_or_compiled_output_cache_is_introduced(self):
        for job in ('checks', 'build'):
            source = cache(job)
            self.assertIn('path: ${{ env.CCACHE_DIR }}', source)
            for token in ('github.run_id', 'github.run_attempt', 'path: .cxx', 'path: app/build', 'path: Paintroid/build'):
                self.assertNotIn(token, source)
