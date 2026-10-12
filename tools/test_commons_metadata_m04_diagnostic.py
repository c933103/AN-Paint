"""Fail-closed contracts for the PR55 observability successor, never Android acceptance."""
import hashlib
import json
import re
from pathlib import Path
import unittest
from unittest.mock import patch

from commons_metadata_m04_diagnostic_scope import FIXTURE, ROOT, before_diagnostic, scope
from commons_metadata_m04_painted_ink_scope import before_painted_ink

FLOW = 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
EVIDENCE = ROOT / 'verification/commons-metadata-m04-diagnostic-2026-10-12'
GUARD = 'layout.getLineLeft(line)>=-1f && layout.getLineRight(line)<=layout.width+1f'


def digest(content):
    return hashlib.sha256(content).hexdigest()


def methods(text):
    return re.findall(r'@Test\b(?:(?!\bfun\b).)*\bfun\s+(\w+)\s*\(', text, re.S)


class CommonsMetadataM04DiagnosticContracts(unittest.TestCase):
    def test_successor_is_exactly_test_observability_and_three_host_adapters(self):
        data = scope()
        self.assertEqual('b95c9a682c77f5dfa9b9a1f4eacabd9d9a03265a', data['failed_head'])
        self.assertEqual('d80218496e45bbefcaa378d40e5cd9846b7988ee', data['failed_tree'])
        self.assertEqual(38239121942, data['failed_run'])
        self.assertEqual('14b1fdf8e02ebe6f765d63906f05c7e808524b76', data['failed_merge'])
        self.assertEqual(890, data['expected_jvm_count'])
        self.assertEqual({FLOW, 'tools/commons_metadata_m04_composition_scope.py',
                          'tools/test_commons_metadata_m04_composition.py',
                          'tools/test_localized_dialog_composition.py'},
                         {row['path'] for row in data['entries']})
        self.assertEqual(4, len(data['entries']))
        self.assertEqual(data['historical_m04_scope_sha256'], digest(
            (ROOT / 'tools/fixtures/commons_metadata_m04_pr52_successor_scope.json').read_bytes()))
        for row in data['entries']:
            content = before_painted_ink(row['path'], (ROOT / row['path']).read_bytes())
            self.assertEqual(row['after_sha256'], digest(content))
            self.assertEqual(row['before_sha256'], digest(before_diagnostic(row['path'], content)))

    def test_missing_duplicated_corrupted_and_unrelated_successor_content_is_rejected(self):
        for row in scope()['entries']:
            content = before_painted_ink(row['path'], (ROOT / row['path']).read_bytes())
            original = before_diagnostic(row['path'], content)
            for invalid in (original, content + b'\n# unrelated\n'):
                with self.subTest(path=row['path']), self.assertRaises(AssertionError):
                    before_diagnostic(row['path'], invalid)
            for edit in row['edits']:
                for replacement in ('', edit['after'] * 2, edit['before']):
                    invalid = content.replace(edit['after'].encode(), replacement.encode(), 1)
                    self.assertNotEqual(content, invalid)
                    with self.subTest(path=row['path']), self.assertRaises(AssertionError):
                        before_diagnostic(row['path'], invalid)

    def test_scope_corruption_fails_even_under_optimized_python(self):
        original_read = Path.read_bytes
        for mutation in ('missing', 'duplicate', 'changed', 'expanded'):
            data = scope()
            if mutation == 'missing': data['entries'].pop()
            if mutation == 'duplicate': data['entries'].append(data['entries'][0])
            if mutation == 'changed': data['entries'][0]['after_sha256'] = '0' * 64
            if mutation == 'expanded': data['entries'].append({'path': 'unrelated'})
            raw = json.dumps(data).encode()
            def read_bytes(path):
                return raw if path == FIXTURE else original_read(path)
            with patch.object(Path, 'read_bytes', read_bytes), self.assertRaises(AssertionError):
                scope()

    def test_all_original_jvm_identities_and_failure_conditions_are_preserved(self):
        live = before_painted_ink(FLOW, (ROOT / FLOW).read_bytes()).decode()
        original = before_diagnostic(FLOW, live.encode()).decode()
        self.assertEqual(methods(original), methods(live))
        self.assertEqual(16, len(methods(live)))
        self.assertEqual(1, original.count(GUARD))
        self.assertEqual(2, live.count(GUARD))  # unchanged assertion + observational JSON boolean
        for token in ('assertEquals(0,layout.getEllipsisCount(line))',
                      'assertEquals(text.length,layout.getLineEnd(layout.lineCount-1))',
                      'assertTrue(layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)',
                      'assertEquals(0,start.top)', 'assertEquals(view.height,end.bottom)',
                      'if(position==0) assertEquals(0,visible.left)',
                      'if(position==end) assertEquals(view.width,visible.right)',
                      'GallerySvgReadabilityFixture.assertEntireMessageVisible(view)'):
            self.assertEqual(original.count(token), live.count(token), token)
        self.assertIn('if(!metadataFinished) throw failure', live)
        self.assertIn('catch(failure: AssertionError)', live)
        self.assertNotIn('catch(failure: Exception)', live)
        self.assertIn('assertTrue("Readability profile failures:\\n"+failures.joinToString("\\n"),failures.isEmpty())', live)
        self.assertEqual(original.count('TimeUnit.SECONDS.toNanos(12)'), live.count('TimeUnit.SECONDS.toNanos(12)'))
        self.assertNotIn('@Ignore', live)

    def test_pre_guard_pixels_metrics_and_completed_vertical_capture_are_required(self):
        live = before_painted_ink(FLOW, (ROOT / FLOW).read_bytes()).decode()
        readable = live.split('    private fun readable(', 1)[1].split('    private fun recordLandscapeDiagnostic', 1)[0]
        self.assertLess(readable.index('recordLandscapeDiagnostic(root,view,tag,insert,scale)'),
                        readable.index('assertEquals(text.length,layout.getLineEnd'))
        self.assertLess(readable.index('recordLandscapeDiagnostic(root,view,tag,insert,scale)'),
                        readable.index(GUARD))
        for token in ('root.draw(android.graphics.Canvas(screen))', 'layout.draw(canvas)',
                      'save(ink,"-expanded-layout")', '"ink_pixels_outside_layout"',
                      '"width_including_trailing_whitespace"', '"content_width"',
                      '"layout_width"', '"text_locales"', '"expanded_canvas_edge_touch"', '"normal-landscape-outcomes.json"'):
            self.assertIn(token, live)
        vertical = readable.split('rail.resetToReadingStart()', 1)[1].split('} else {', 1)[0]
        self.assertIn('root.measure(', vertical); self.assertIn('root.layout(0,0,width,height)', vertical)
        self.assertIn('rail.scrollX)', vertical)

    def test_new_inventory_keeps_the_old_890_manifest_and_adds_no_runtime_identity(self):
        old_path = ROOT / 'verification/commons-metadata-m04-pr52-composition-2026-10-12/expected-jvm-identities.json'
        old = json.loads(old_path.read_text())
        new = json.loads((EVIDENCE / 'expected-jvm-identities.json').read_text())
        self.assertEqual(digest(old_path.read_bytes()), new['frozen_inventory_sha256'])
        self.assertEqual(890, len(old['expected'])); self.assertEqual(old['expected'], new['expected'])
        self.assertEqual(890, new['expected_count'])
        self.assertEqual(digest(before_painted_ink(FLOW, (ROOT / FLOW).read_bytes())), new['diagnostic_flow_sha256'])
        self.assertEqual([], new['added_execution_identities'])
        self.assertEqual([], new['removed_execution_identities'])


if __name__ == '__main__': unittest.main()
