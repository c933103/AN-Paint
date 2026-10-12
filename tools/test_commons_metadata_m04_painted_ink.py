"""Exact source/negative-control contracts; native oracle execution remains a separate gate."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from commons_metadata_m04_painted_ink_scope import ROOT, FIXTURE, scope, before_painted_ink
from commons_metadata_m04_diagnostic_scope import before_diagnostic
from commons_metadata_m04_glyph_bounds_scope import before_glyph_bounds

FLOW = 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
EVIDENCE = ROOT / 'verification/commons-metadata-m04-painted-ink-2026-10-12'
GUARD = 'layout.getLineLeft(line)>=-1f && layout.getLineRight(line)<=layout.width+1f'


def source_bytes(path):
    return before_glyph_bounds(path, (ROOT / path).read_bytes())


def digest(content): return hashlib.sha256(content).hexdigest()


def methods(text):
    return re.findall(r'@Test\b(?:(?!\bfun\b).)*\bfun\s+(\w+)\s*\(', text, re.S)


class CommonsMetadataM04PaintedInkContracts(unittest.TestCase):
    def test_exact_successor_preserves_three_diagnostic_endpoints_and_frozen_fixture(self):
        data=scope()
        self.assertEqual('dc46abc2add7984358565a88fe65c5278212dcf6',data['diagnostic_head'])
        self.assertEqual('4ff7f479ffc73964fa8756b6c7e3202f624ad0f1',data['diagnostic_tree'])
        self.assertEqual(38244193872,data['diagnostic_run'])
        self.assertEqual(892,data['expected_jvm_count']);self.assertEqual(GUARD,data['original_advance_guard'])
        self.assertEqual({FLOW,'tools/commons_metadata_m04_diagnostic_scope.py','tools/test_commons_metadata_m04_diagnostic.py'},
                         {row['path'] for row in data['entries']})
        self.assertEqual(3,len(data['entries']))
        self.assertEqual(data['historical_diagnostic_scope_sha256'],digest(
            (ROOT/'tools/fixtures/commons_metadata_m04_diagnostic_successor_scope.json').read_bytes()))
        for row in data['entries']:
            content=source_bytes(row['path'])
            self.assertEqual(row['after_sha256'],digest(content))
            restored=before_painted_ink(row['path'],content,allow_original=False)
            self.assertEqual(row['before_sha256'],digest(restored))
            self.assertEqual(restored,before_painted_ink(row['path'],restored))

    def test_live_source_rejects_deleted_restored_duplicated_corrupted_and_unrelated_oracle(self):
        for row in scope()['entries']:
            content=source_bytes(row['path'])
            old=before_painted_ink(row['path'],content,allow_original=False)
            for invalid in (old,content+b'\n// unrelated\n'):
                with self.assertRaises(AssertionError): before_painted_ink(row['path'],invalid,allow_original=False)
            for edit in row['edits']:
                for replacement in ('',edit['before'],edit['after']*2):
                    invalid=content.replace(edit['after'].encode(),replacement.encode(),1)
                    self.assertNotEqual(content,invalid)
                    with self.assertRaises(AssertionError): before_painted_ink(row['path'],invalid,allow_original=False)

    def test_changed_scope_is_rejected_without_python_assert_statements(self):
        original=Path.read_bytes
        for mutation in ('missing','duplicate','changed','expanded'):
            data=scope()
            if mutation=='missing': data['entries'].pop()
            if mutation=='duplicate': data['entries'].append(data['entries'][0])
            if mutation=='changed': data['entries'][0]['after_sha256']='0'*64
            if mutation=='expanded': data['entries'].append({'path':'unrelated'})
            raw=json.dumps(data).encode()
            with patch.object(Path,'read_bytes',lambda p:raw if p==FIXTURE else original(p)),self.assertRaises(AssertionError):scope()

    def test_only_horizontal_landscape_proxy_changes_while_all_other_original_guards_restore(self):
        live=source_bytes(FLOW).decode();old=before_painted_ink(FLOW,live.encode(),allow_original=False).decode()
        self.assertEqual(2,old.count(GUARD));self.assertEqual(1,live.count(GUARD))
        self.assertIn('.put("original_horizontal_guard",'+GUARD+')',live)
        self.assertIn('.put("advance_guard_role","Diagnostic only;',live)
        self.assertNotIn('Diagnostic outcomes; original JUnit assertions remain authoritative',live)
        new_methods=set(methods(live))-set(methods(old))
        self.assertEqual({'paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtNormalScale',
                          'paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtDoubleScale'},new_methods)
        self.assertEqual(16,len(methods(old)));self.assertEqual(18,len(methods(live)))
        self.assertTrue(set(methods(old))<=set(methods(live)))
        start='                if(VerticalText.uiVertical()) {'
        old_route=old[old.index(start):old.index('                        for(line in 0 until layout.lineCount)',old.index(start))]
        live_route=live[live.index(start):live.index('                        for(line in 0 until layout.lineCount)',live.index(start))]
        self.assertEqual(old_route,live_route)
        for token in ['assertEquals(0,layout.getEllipsisCount(line))','assertEquals(0,start.top)',
                      'assertEquals(view.width,start.width())','assertEquals(view.height,end.bottom)',
                      'assertEquals(view.width,end.width())','assertEquals(0,restored.top)',
                      'assertEquals(text.length,layout.getLineEnd(layout.lineCount-1))',
                      'assertTrue(layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)']:
            self.assertEqual(old.count(token),live.count(token),token)
        self.assertEqual(before_diagnostic(FLOW,old.encode()),before_diagnostic(FLOW,live.encode()))

    def test_complete_native_geometry_and_exact_unmasked_pixels_drive_acceptance(self):
        live=source_bytes(FLOW).decode()
        for token in ['android.graphics.RectF(layout.computeDrawingBoundingBox()).apply','kotlin.math.floor(xs.minOrNull()!!)','kotlin.math.ceil(xs.maxOrNull()!!)',
                      'ys.add(layout.getLineTop(line).toFloat())','view.baseline-layout.getLineBaseline(0)',
                      'assertEquals(android.view.Gravity.TOP','assertEquals(0,view.scrollX);assertEquals(0,view.scrollY)',
                      'assertNull(view.background);assertNull(view.foreground)','assertTrue(view.compoundDrawables.all {it==null})',
                      'assertEquals(0f,view.shadowRadius,0f)','assertFalse(view.paint.isUnderlineText)',
                      'width.toLong()*height<=16_000_000L','if((pixel ushr 24)==0) continue',
                      'if(localX<0 || localX>=contentWidth) overflow++','actualPixels[y*actual.width+x]!=expected',
                      'assertEquals("$label horizontal painted-ink overflow",0,frame.horizontalOverflow)',
                      'assertEquals("$label clipped expected ink",0,frame.missingInk)',
                      'assertEquals("$label exact full-reference/actual-view ARGB mismatch",0,frame.differentPixels)']:
            self.assertIn(token,live)
        body=live.split('    private fun capturePaintedInk(',1)[1].split('    private fun assertPaintedInk',1)[0]
        for forbidden in ('view.text=','view.typeface=','view.setPadding','view.setTextColor','layout.increaseWidthTo'):
            self.assertNotIn(forbidden,body)

    def test_native_negative_controls_reach_exact_rejection_with_unchanged_full_reference(self):
        live=source_bytes(FLOW).decode()
        controls=live.split('    private fun inkOracleNegativeControls(',1)[1].split('    private fun recordLandscapeDiagnostic',1)[0]
        self.assertIn('listOf("en-GB","ain-Kana","bo","ar","ja","vi-Hani")',controls)
        self.assertIn('assertPaintedInk(intact,"$label intact")',controls)
        self.assertEqual(6,controls.count('                rejects("'))
        for token in ['translationX=-4*intact.contentWidth','translationX=4*intact.contentWidth',
                      'clipLeft=intact.originX+intact.inkLeft+1','clipRight=intact.originX+intact.inkRight-1',
                      'intact.referencePixels,frame.referencePixels','frame.missingInk>0','frame.horizontalOverflow>0',
                      'failure.message.orEmpty().contains(cause)','assertTrue("The oracle must reject the native draw mutation",rejected)',
                      'layout.isRtlCharAt(0)','view.createAccessibilityNodeInfo().text.toString()',
                      'originalBounds,layout.computeDrawingBoundingBox()', 'originalPaint,paintState()', 'originalGeometry,geometry()']:
            self.assertIn(token,controls)
        self.assertIn('actualCanvas.clipRect(clipLeft,0,clipRight,view.height)',live)
        self.assertIn('actualCanvas.translate(translationX.toFloat(),0f);view.draw(actualCanvas)',live)

    def test_explicit_892_identity_inventory_keeps_old_890_and_native_failure_files_unchanged(self):
        new=json.loads((EVIDENCE/'expected-jvm-identities.json').read_text());old_path=ROOT/new['frozen_inventory_path']
        old=json.loads(old_path.read_text());self.assertEqual(digest(old_path.read_bytes()),new['frozen_inventory_sha256'])
        self.assertEqual(890,len(old['expected']));self.assertEqual(892,new['expected_count'])
        self.assertEqual(set(map(tuple,old['expected']))|set(map(tuple,new['added_execution_identities'])),set(map(tuple,new['expected'])))
        self.assertEqual(2,len(new['added_execution_identities']));self.assertEqual([],new['removed_execution_identities'])
        self.assertEqual(digest(source_bytes(FLOW)),new['flow_source_sha256'])
        failure=json.loads((EVIDENCE/'historical-failure-binding.json').read_text())
        self.assertEqual(0,failure['line0']['painted_pixels_outside_layout'])
        self.assertGreater(failure['line0']['advance_right'],failure['line0']['layout_width']+failure['line0']['original_allowance_px'])
        for row in failure['files']:self.assertEqual(row['sha256'],digest(source_bytes(row['path'])))


if __name__=='__main__':unittest.main()
