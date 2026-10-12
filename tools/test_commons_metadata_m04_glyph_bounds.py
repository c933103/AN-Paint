"""Exact successor/source contracts; native and installed acceptance remain hosted gates."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch
from commons_metadata_m04_glyph_bounds_scope import ROOT, FIXTURE, PATHS, scope, before_glyph_bounds
from commons_metadata_m04_painted_ink_scope import before_painted_ink
from commons_metadata_m04_receiver_scope import before_receiver_fix

FLOW='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
GALLERY='Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt'
DEVICE='app/src/androidTest/java/paint/anpaint/android/GalleryViewportDeviceTest.kt'
EVIDENCE=ROOT/'verification/commons-metadata-m04-glyph-bounds-2026-10-12'

def historical_bytes(path): return before_receiver_fix(path, (ROOT/path).read_bytes())
def digest(b): return hashlib.sha256(b).hexdigest()
def methods(s): return re.findall(r'@Test\b(?:(?!\bfun\b).)*\bfun\s+(\w+)\s*\(',s,re.S)

class GlyphBoundsSuccessorContracts(unittest.TestCase):
    def test_seven_exact_inverse_endpoints_keep_all_historical_fixtures(self):
        data=scope();self.assertEqual('e7855e04a1a4647a1fae3a14937df0c17c3f4d79',data['base_head'])
        self.assertEqual('8752ed99c9350235da46fac1b4a188ca89296889',data['base_tree'])
        self.assertEqual(7,len(data['entries']));self.assertEqual(PATHS,{r['path'] for r in data['entries']})
        self.assertEqual({GALLERY},{r['path'] for r in data['entries'] if '/src/main/' in r['path']})
        self.assertEqual(data['historical_painted_ink_scope_sha256'],digest((ROOT/'tools/fixtures/commons_metadata_m04_painted_ink_successor_scope.json').read_bytes()))
        for row in data['entries']:
            raw=historical_bytes(row['path']);self.assertEqual(row['after_sha256'],digest(raw))
            old=before_glyph_bounds(row['path'],raw,allow_original=False)
            self.assertEqual(row['before_sha256'],digest(old));self.assertEqual(old,before_glyph_bounds(row['path'],old))

    def test_deleted_restored_duplicated_corrupted_or_unrelated_live_content_fails_closed(self):
        for row in scope()['entries']:
            raw=historical_bytes(row['path']);old=before_glyph_bounds(row['path'],raw,allow_original=False)
            for bad in [old,raw+b'\n// unrelated\n']:
                with self.assertRaises(AssertionError):before_glyph_bounds(row['path'],bad,allow_original=False)
            for edit in row['edits']:
                for replacement in ['',edit['before'],edit['after']*2]:
                    bad=raw.replace(edit['after'].encode(),replacement.encode(),1)
                    self.assertNotEqual(raw,bad)
                    with self.assertRaises(AssertionError):before_glyph_bounds(row['path'],bad,allow_original=False)

    def test_fixture_corruption_is_rejected_even_with_optimized_python(self):
        read=Path.read_bytes
        for mutation in ['missing','duplicate','hash','extra']:
            data=scope()
            if mutation=='missing':data['entries'].pop()
            if mutation=='duplicate':data['entries'].append(data['entries'][0])
            if mutation=='hash':data['entries'][0]['before_sha256']='0'*64
            if mutation=='extra':data['entries'].append({'path':'unrelated'})
            raw=json.dumps(data).encode()
            with patch.object(Path,'read_bytes',lambda p:raw if p==FIXTURE else read(p)),self.assertRaises(AssertionError):scope()

    def test_production_margin_is_measured_absolute_bounded_and_resets(self):
        live=historical_bytes(GALLERY).decode()
        self.assertIn('if(android.os.Build.VERSION.SDK_INT>=35 && !VerticalText.uiVertical())\n            GlyphBoundsStatusView(this) else TextView(this)',live)
        self.assertIn('if(android.os.Build.VERSION.SDK_INT>=35 && status is GlyphBoundsStatusView)',live)
        body=live.split('private class GlyphBoundsStatusView',1)[1]
        for token in ['useBoundsForWidth=true','shiftDrawingOffsetForStartOverhang=false',
                      'sourceText=message;leadingInset=0;measuredSignature=null;text=message',
                      'widthMeasureSpec,paint.textSize,paint.textScaleX,paint.textSkewX',
                      'signature!=measuredSignature','if(leadingInset!=0) {leadingInset=0;text=message}',
                      'repeat(3)','android.graphics.RectF(measured.computeDrawingBoundingBox())',
                      'measured.getParagraphDirection(it)>0','measured.getParagraphDirection(it)<0',
                      'if(needed<=leadingInset) return','val next=needed','paint.textSize*2f',
                      'android.text.SpannableString(message)','LeadingMarginSpan.Standard(leadingInset),0,length']:
            self.assertIn(token,body)
        for forbidden in ['leadingInset+needed','setTextSize','setTypeface','substring','take(','replace(']:self.assertNotIn(forbidden,body)

    def test_strict_pixel_assertions_are_byte_identical_and_known_margin_is_fully_allocated(self):
        live=historical_bytes(FLOW).decode();old=before_glyph_bounds(FLOW,live.encode(),allow_original=False).decode()
        part=lambda s:s.split('    private fun assertPaintedInk(',1)[1].split('    private fun paintedInkReport',1)[0]
        self.assertEqual(part(old),part(live))
        for token in ['spans.size<=1','LeadingMarginSpan.Standard::class.java,span.javaClass',
                      'spanned!!.getSpanStart(span)','spanned.getSpanEnd(span)','spanned.getSpanFlags(span)',
                      'margin.getLeadingMargin(false)','bounds.left-leadingInset,bounds.right+leadingInset',
                      'view.shiftDrawingOffsetForStartOverhang','layout.shiftDrawingOffsetForStartOverhang',
                      'if((pixel ushr 24)==0) continue','actualPixels[y*actual.width+x]!=expected']:
            self.assertIn(token,live)
        self.assertEqual(before_painted_ink(FLOW,old.encode()),before_painted_ink(FLOW,live.encode()))

    def test_before_control_and_six_script_resets_retain_defect_specific_mutations(self):
        live=historical_bytes(FLOW).decode()
        for token in ['Original Arabic native start bearing must overflow','Original Arabic draw must really lose expected ink',
                      'capturePaintedInk(beforeView,expectedBoundsWidth=false)','original-plain-before',
                      'Remeasure must not accumulate the margin','measure(width-48)','originalSize*.75f',
                      'mixed-paragraphs','A new short status must not retain the old margin','check("restored",original)',
                      'checkInsetReset(activity,view,width,height,label)','native-inset-resets-font$scale.json',
                      'The oracle must reject the native draw mutation','failure.message.orEmpty().contains(cause)']:
            self.assertIn(token,live)
        self.assertEqual(6,live.count('                rejects("'))
        self.assertIn('listOf("en-GB","ain-Kana","bo","ar","ja","vi-Hani")',live)
        self.assertIn('assertArrayEquals("Clipping changes the actual draw only",intact.referencePixels,frame.referencePixels)',live)

    def test_installed_profile_preserves_prior_checks_and_requires_full_rasters_without_new_status_codes(self):
        live=historical_bytes(DEVICE).decode();old=before_glyph_bounds(DEVICE,live.encode(),allow_original=False).decode()
        self.assertEqual(methods(old),methods(live))
        for token in ['else listOf("fr","mn-Mong")','tag=="ar" && landscape','for(insert in listOf(false,true))',
                      'commons_metadata_query_failed','commons_credit_copy_failed_reason','ui_could_not_load_gallery_image',
                      'capturePaintedInk(view)','actual_png','reference_png','anpaint_source_tests_sha256',
                      '128*1024','parcel.dataSize()<=512*1024','anpaint_m04_glyph_bounds_$route',
                      'instrumentation.addResults','assertEquals(2,allResults.size())','failures.isEmpty()',
                      'not network-route or hardware screenshot proof']:
            self.assertIn(token,live)
        self.assertNotIn('instrumentation.sendStatus',live)
        self.assertNotIn('org.catrobat.paintroid.classic.VerticalText',live)
        self.assertEqual(1,live.count('private fun setFontScale(scale: Float)'))
        old_tail=old.split('    private fun selectLanguage(tag: String)',1)[1]
        self.assertEqual(old_tail,live.split('    private fun selectLanguage(tag: String)',1)[1])

    def test_fresh_source_inventory_and_three_failed_checkpoints_remain_distinct(self):
        new=json.loads((EVIDENCE/'expected-jvm-identities.json').read_text())
        old=json.loads((ROOT/new['frozen_inventory_path']).read_text())
        self.assertEqual(892,len(new['expected']));self.assertEqual(old['expected'],new['expected'])
        self.assertEqual([],new['added_execution_identities']);self.assertEqual([],new['removed_execution_identities'])
        self.assertEqual(digest(historical_bytes(FLOW)),new['flow_source_sha256'])
        binding=json.loads((EVIDENCE/'historical-failure-binding.json').read_text())
        self.assertEqual([38239121942,38244193872,38250189049],[r['run_id'] for r in binding['checkpoints']])
        self.assertTrue(all(r['status']=='failed' for r in binding['checkpoints']))
        expected=json.loads((EVIDENCE/'native-artifact-expectations.json').read_text())
        self.assertEqual(181,expected['expected_raster_pairs']);self.assertEqual(181,len(expected['stems']))
        self.assertEqual(104,expected['api35_installed_identities']);self.assertEqual(72,expected['expected_rejected_mutations'])

if __name__=='__main__':unittest.main()
