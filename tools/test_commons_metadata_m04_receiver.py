"""Receiver and natural-traversal corrections; host checks are not Kotlin/native execution."""
import hashlib
import json
import re
import unittest
from pathlib import Path
from unittest.mock import patch
from commons_metadata_m04_receiver_scope import ROOT,FIXTURE,PATHS,scope,before_receiver_fix

FLOW='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
GALLERY='Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt'
DEVICE='app/src/androidTest/java/paint/anpaint/android/GalleryViewportDeviceTest.kt'
RESET='''            assertFalse("Status is settled before same-height replacement",view.isLayoutRequested)
            show(original)
            assertTrue("Status setter must request its own glyph remeasurement",view.isLayoutRequested)
'''
OLD='useBoundsForWidth=false;shiftDrawingOffsetForStartOverhang=false;text=view.text.toString()'
NEW=OLD.replace(';text=',';this.text=')
def sha(b):return hashlib.sha256(b).hexdigest()

class ReceiverSuccessorContracts(unittest.TestCase):
    def test_exact_five_endpoints_restore_the_failed_source(self):
        data=scope()
        self.assertEqual('d5fb31f6cb1562eecba51e5ccff9b118a7e71714',data['base_head'])
        self.assertEqual('8f9f0d5399f88d173a508e0ce5c96682ca173ed4',data['base_tree'])
        self.assertEqual(5,len(data['entries']));self.assertEqual(PATHS,{x['path'] for x in data['entries']})
        self.assertEqual({GALLERY,DEVICE},{p for p in PATHS if '/src/main/' in p or '/androidTest/' in p})
        for row in data['entries']:
            raw=(ROOT/row['path']).read_bytes();self.assertEqual(row['after_sha256'],sha(raw))
            old=before_receiver_fix(row['path'],raw,allow_original=False)
            self.assertEqual(row['before_sha256'],sha(old));self.assertEqual(old,before_receiver_fix(row['path'],old))

    def test_explicit_textview_receiver_and_pending_measure_check_are_the_only_flow_edits(self):
        raw=(ROOT/FLOW).read_bytes();old=before_receiver_fix(FLOW,raw,allow_original=False)
        self.assertEqual(1,old.decode().count(OLD));self.assertEqual(1,raw.decode().count(NEW))
        self.assertEqual(1,raw.decode().count(RESET))
        self.assertEqual(old.decode().replace(OLD,NEW,1),raw.decode().replace(RESET,''))
        self.assertNotIn(OLD,raw.decode())
        methods=lambda b:re.findall(r'@Test\b(?:(?!\bfun\b).)*\bfun\s+(\w+)\s*\(',b.decode(),re.S)
        self.assertEqual(methods(old),methods(raw));self.assertEqual(18,len(methods(raw)))

    def test_production_only_schedules_the_existing_glyph_measurement(self):
        raw=(ROOT/GALLERY).read_bytes();old=before_receiver_fix(GALLERY,raw,allow_original=False)
        added="""        // TextView can replace a fixed-width, same-height Layout without remeasurement.
        // The new message must still run our glyph-inset measurement on normal traversal.
        requestLayout()
"""
        self.assertEqual(1,raw.decode().count(added));self.assertEqual(old.decode(),raw.decode().replace(added,''))
        setter=raw.decode().split('    fun setStatusText(message: String)',1)[1].split('    override fun onMeasure',1)[0]
        self.assertLess(setter.index('text=message'),setter.index('requestLayout()'))

    def test_installed_replacements_require_natural_settled_same_height_traversal(self):
        raw=(ROOT/DEVICE).read_bytes();old=before_receiver_fix(DEVICE,raw,allow_original=False)
        split=lambda b:b.decode().split('    private fun checkInstalledArabicStatusInk(',1)
        live_prefix,live_rest=split(raw);old_prefix,old_rest=split(old)
        body,tail=live_rest.split('    private data class PaintedInkFrame(',1)
        old_body,old_tail=old_rest.split('    private data class PaintedInkFrame(',1)
        self.assertEqual(old_prefix,live_prefix);self.assertEqual(old_tail,tail)
        for forbidden in ['.measure(','.layout(','.requestLayout(','.forceLayout(']:self.assertNotIn(forbidden,body)
        for token in ['org.catrobat.paintroid.classic.GlyphBoundsStatusView','view.javaClass.name',
                      'assertFalse("Root is settled before replacement",root.isLayoutRequested)',
                      'assertFalse("Status is settled before replacement",view.isLayoutRequested)',
                      'oldText!=message','assertTrue(oldHeight>0)','show(message)',
                      'assertTrue("Production setter must request glyph remeasurement",requested)',
                      'naturalUpdate.getInt("old_layout_height"),requireNotNull(view.layout).height',
                      'assertEquals(naturalUpdate.getInt("view_width"),view.width)',
                      'GalleryStatusNaturalUpdate','source_tests_sha256','old_message',
                      'view_requested_before','view_requested_after','root_requested_settled',
                      'complete_layout_text','capturePaintedInk(view)','assertPaintedInk(frame,',
                      'for(insert in listOf(false,true))','assertEquals(2,allResults.size())']:
            self.assertIn(token,body)
        # Preserve the full raster transport and zero-tolerance acceptance exactly.
        marker='                capturePaintedInk(view).use {frame ->'
        self.assertEqual(old_body.split(marker,1)[1],body.split(marker,1)[1])

    def test_missing_duplicate_reverted_or_unrelated_live_edits_fail_closed(self):
        for row in scope()['entries']:
            raw=(ROOT/row['path']).read_bytes();old=before_receiver_fix(row['path'],raw,allow_original=False)
            bads=[old,raw+b'\n# unrelated\n']
            for e in row['edits']:
                for replacement in ['',e['before'],e['after']*2]:bads.append(raw.replace(e['after'].encode(),replacement.encode(),1))
            for bad in bads:
                self.assertNotEqual(raw,bad)
                with self.assertRaises(AssertionError):before_receiver_fix(row['path'],bad,allow_original=False)

    def test_fixture_corruption_fails_even_under_optimized_python(self):
        read=Path.read_bytes
        for kind in ['missing','duplicate','hash','unrelated']:
            data=scope()
            if kind=='missing':data['entries'].pop()
            elif kind=='duplicate':data['entries'].append(data['entries'][0])
            elif kind=='hash':data['entries'][0]['before_sha256']='0'*64
            else:data['extra']='unreviewed'
            bad=json.dumps(data).encode()
            with patch.object(Path,'read_bytes',lambda p:bad if p==FIXTURE else read(p)),self.assertRaises(AssertionError):scope()

    def test_original_glyph_fixture_and_pixel_guard_are_unchanged(self):
        old_fixture=ROOT/'tools/fixtures/commons_metadata_m04_glyph_bounds_successor_scope.json'
        self.assertEqual('824cb01cbd9f9c9edf3e7283b1ccdc18da7c0e7bb1fc88a4a59a3a38ff4a0639',sha(old_fixture.read_bytes()))
        raw=(ROOT/FLOW).read_bytes();old=before_receiver_fix(FLOW,raw)
        guard=lambda b:b.split(b'    private fun assertPaintedInk(',1)[1].split(b'    private fun paintedInkReport',1)[0]
        self.assertEqual(guard(old),guard(raw))

if __name__=='__main__':unittest.main()
