"""Host receipt/collector contracts. Synthetic headers are never rendered evidence."""
import copy
import json
from pathlib import Path
import struct
import tempfile
import unittest
from vertical_control_reachability import CASES, LABELS, STATES, complete, contains, verify

ROOT=Path(__file__).resolve().parents[1]


def fixture(directory):
    directory.mkdir(parents=True,exist_ok=True)
    geometry=dict(raw=[20,20,120,70],visible=[20,20,120,70],fully_visible=True,
                  parents=[dict(scroll_x=100,scroll_y=0)])
    for case in CASES:
        captures=[dict(kind='capture',state=s,filename='fixture.jpg',
                       quality=1 if s=='minimum' else 100,geometry=geometry,seekbar=geometry,
                       readout=geometry,thumb=[20,20,30,30]) for s in STATES if s!='returned']
        endpoints=[dict(kind='endpoint',before=100 if v==1 else 1,value=v,
                        **{'from':[25,25],'to':[30,30]},geometry=geometry,seekbar=geometry,
                        thumb=[20,20,30,30]) for v in (1,100)]
        observations=[dict(kind='reachable',label=label,geometry=geometry) for label in LABELS]+endpoints+captures
        observations += [dict(kind='scroll-before',geometry=dict(geometry,parents=[dict(scroll_x=0,scroll_y=0)])),
                         dict(kind='scroll-after',geometry=geometry)]
        receipt=dict(case=case,success=True,device_sdk=35,filename='fixture.jpg',endpoint_values=[1,100],
                     cancel_preserved_quality=True,remembered_quality_before_cancel=95,cancel_draft_quality=100,
                     canvas_and_document_preserved=True,
                     confirmed_quality=100 if case.endswith('-landscape') else 1,destination_requests=1,
                     destination_action='android.intent.action.CREATE_DOCUMENT',destination_mime='image/jpeg',
                     destination_filename='fixture.jpg',native_scroll_gestures=1,observations=observations,
                     screenshots=[f'{case}-{s}.png' for s in STATES])
        (directory/f'{case}.json').write_text(json.dumps(receipt))
        for state in STATES:
            dimensions=(240,120) if case.endswith('-landscape') else (120,240)
            (directory/f'{case}-{state}.png').write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'+
                struct.pack('>II',*dimensions)+b'\0'*9+(case+state).encode())


class ReachabilityReceiptTest(unittest.TestCase):
    def test_complete_eight_case_inventory_and_file_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);fixture(directory);result=verify(directory)
            self.assertEqual(8,len(result['cases']));self.assertEqual(64,result['screenshots'])
            self.assertEqual(72,len(result['files']))
            with self.assertRaisesRegex(ValueError,'device SDK'): verify(directory,30)

    def test_visibility_requires_all_four_bounds_and_positive_area(self):
        self.assertTrue(contains([0,0,100,100],[1,1,99,99]))
        for raw in ([-1,0,99,99],[0,0,101,99],[0,-1,99,99],[0,0,99,101],[1,1,1,2]):
            self.assertFalse(complete(dict(raw=raw,visible=[0,0,100,100],fully_visible=True)))
        self.assertFalse(complete(dict(raw=[1,1,2,2],visible=[0,0,100,100],fully_visible=False)))

    def test_failure_missing_endpoint_clipping_lost_state_and_fake_motion_fail_closed(self):
        mutations=[lambda r:r.update(success=False),lambda r:r.update(failure='failed'),
            lambda r:r.update(endpoint_values=[1]),lambda r:r.update(device_sdk='35'),
            lambda r:r.update(remembered_quality_before_cancel=100),
            lambda r:r.update(cancel_draft_quality=95),
            lambda r:r.update(cancel_draft_quality=50),
            lambda r:r.update(cancel_preserved_quality=False),lambda r:r.update(canvas_and_document_preserved=False),
            lambda r:r.update(destination_filename='lost.jpg'),lambda r:r.update(destination_requests=2),
            lambda r:r.update(confirmed_quality=50),lambda r:r.update(native_scroll_gestures=0),
            lambda r:r['screenshots'].pop(),
            lambda r:r.update(observations=[o for o in r['observations'] if o.get('label')!='Cancel action']),
            lambda r:r.update(observations=[o for o in r['observations'] if o.get('value')!=1]),
            lambda r:next(o for o in r['observations'] if o['kind']=='endpoint').update(before=1),
            lambda r:next(o for o in r['observations'] if o['kind']=='endpoint').update(to=[0,0]),
            lambda r:next(o for o in r['observations'] if o['kind']=='endpoint').update(thumb=[0,0,25,25]),
            lambda r:next(o for o in r['observations'] if o.get('state')=='minimum').update(quality=95),
            lambda r:next(o for o in r['observations'] if o.get('state')=='maximum')['readout'].update(visible=[20,20,110,70]),
            lambda r:next(o for o in r['observations'] if o['kind']=='capture').update(filename='lost.jpg'),
            lambda r:next(o for o in r['observations'] if o['kind']=='scroll-before').update(
                geometry=next(o['geometry'] for o in r['observations'] if o['kind']=='scroll-after'))]
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);fixture(directory);path=directory/f'{sorted(CASES)[0]}.json';good=json.loads(path.read_text())
            for mutate in mutations:
                with self.subTest(mutation=mutate):
                    broken=copy.deepcopy(good);mutate(broken);path.write_text(json.dumps(broken))
                    with self.assertRaises(ValueError): verify(directory)
            path.write_text(json.dumps(good));self.assertTrue(verify(directory)['success'])

    def test_distinct_cancel_receipt_rejects_equal_landscape_endpoint_preconditions(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);fixture(directory)
            case='mnc-Mong-landscape';path=directory/f'{case}.json'
            good=json.loads(path.read_text())
            good.update(remembered_quality_before_cancel=1,cancel_draft_quality=100)
            path.write_text(json.dumps(good));self.assertTrue(verify(directory)['success'])
            # Reproduce the reviewed hole: remembered1 and draft1 even though
            # endpoint movement 1/100 and every other receipt claim looks valid.
            bad=copy.deepcopy(good);bad['cancel_draft_quality']=1
            next(o for o in bad['observations'] if o.get('state')=='cancel-ready')['quality']=1
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'Incomplete successful'): verify(directory)

    def test_both_visibility_helpers_discard_false_nonempty_output_and_have_installed_negatives(self):
        def check(source):
            self.assertIn('if(!view.getGlobalVisibleRect(bounds)) return Rect()',source)
            self.assertIn('override fun getGlobalVisibleRect(bounds: Rect,offset: Point?): Boolean',source)
            self.assertIn('observed=true;bounds.set(10,20,110,120);return false',source)
            self.assertIn('visibleBounds(fullyClipped).isEmpty',source)
            self.assertIn('assertFailedVisibilityIsEmpty()',source)
        for name in ('VerticalControlReachabilityProbe','VerticalLocaleDeviceTest'):
            source=(ROOT/f'app/src/androidTest/java/paint/anpaint/android/{name}.kt').read_text()
            with self.subTest(helper=name):
                check(source)
                # This is a source/negative-fixture contract, not execution of
                # Android/Kotlin. The actual fake-View negative runs installed.
                with self.assertRaises(AssertionError):
                    check(source.replace('if(!view.getGlobalVisibleRect(bounds)) return Rect()',
                                         'if(!view.getGlobalVisibleRect(bounds)) return bounds'))

    def test_missing_extra_corrupt_identical_endpoint_and_wrong_orientation_images_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);fixture(directory);case=sorted(CASES)[0]
            path=directory/f'{case}-minimum.png';original=path.read_bytes();path.unlink()
            with self.assertRaises(ValueError): verify(directory)
            path.write_bytes(b'broken')
            with self.assertRaises(ValueError): verify(directory)
            path.write_bytes((directory/f'{case}-maximum.png').read_bytes())
            with self.assertRaisesRegex(ValueError,'Identical'): verify(directory)
            path.write_bytes(original);extra=directory/'unexpected.png';extra.write_bytes(original)
            with self.assertRaises(ValueError): verify(directory)
            extra.unlink();bad=bytearray(original);bad[16:24]=original[20:24]+original[16:20];path.write_bytes(bad)
            with self.assertRaisesRegex(ValueError,'orientation'): verify(directory)

    def test_proposed_native_probe_has_no_programmatic_input_substitutes(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/VerticalControlReachabilityProbe.kt').read_text()
        for forbidden in ('.performClick(','.requestRectangleOnScreen(','.scrollTo(','.scrollBy(',
                          '.setProgress(','.progress=', '.setOnSeekBarChangeListener(','.setSelection(',
                          '.requestDisallowInterceptTouchEvent(','.setNestedScrollingEnabled(',
                          '.isNestedScrollingEnabled=', '.setOnScrollChangeListener(',
                          '.setHorizontalScrollBarEnabled(','.isHorizontalScrollBarEnabled='):
            self.assertNotIn(forbidden,source)
        for required in ('device.swipe(', 'device.click(', 'visible.contains(raw)', 'canvas.sameAs(',
                         'assertNotEquals("Endpoint requires a real value change"', 'thumbBounds()',
                         'registerFrameCommitCallback', 'destination_requests'):
            self.assertIn(required,source)
        driver=(ROOT/'tools/ci_emulator.sh').read_text()
        self.assertIn('--suite app-vertical --timeout-seconds 180',driver)
        self.assertIn('tools/vertical_control_reachability.py',driver)

    def test_diagnostic_touch_listener_is_non_consuming_and_does_not_replace_value_listener(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/VerticalControlReachabilityProbe.kt').read_text()
        production=(ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/NumericSlider.kt').read_text()
        # This is a source contract, not an Android event-delivery claim.
        self.assertNotIn('setOnTouchListener',production)
        dialog=(ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt').read_text()
        self.assertNotIn('setOnTouchListener',dialog)
        self.assertIn('NumericSlider(activity,ui(R.string.ui_quality),quality,1,100)',dialog)
        self.assertIn('slider.setOnSeekBarChangeListener(',production)
        def check(text):
            listener=text.split('private val touch=View.OnTouchListener',1)[1].split('private val scroll=',1)[0]
            self.assertIn('false // Never consume DOWN, MOVE, UP or CANCEL.',listener)
            self.assertNotIn('true // Never consume',listener)
            self.assertIn('slider.setOnTouchListener(null)',text)
            self.assertIn('observer.removeOnScrollChangedListener(scroll)',text)
            self.assertNotIn('setOnSeekBarChangeListener(',text)
        check(source)
        with self.assertRaises(AssertionError):
            check(source.replace('false // Never consume','true // Never consume'))

    def test_native_drag_requires_ownership_without_mutating_test_routing(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/VerticalControlReachabilityProbe.kt').read_text()
        production=(ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/NumericSlider.kt').read_text()
        self.assertIn('trace.assertOwnedGesture()',source)
        for assertion in ('Slider receives native DOWN','Slider receives native MOVE','Slider receives native UP',
                          'Ancestor must not cancel the slider drag','Slider drag must not scroll ancestor',
                          'No native drag events dropped','No native scroll observations dropped'):
            self.assertIn(assertion,source)
        # The production child claims only its own enabled touch stream. The
        # native probe remains observational and cannot change event ownership.
        self.assertNotIn('requestDisallowInterceptTouchEvent',source)
        self.assertNotIn('setOnTouchListener',production)
        self.assertIn('val slider: SeekBar=object: SeekBar(context)',production)
        self.assertLess(production.index('requestDisallowInterceptTouchEvent(true)'),
                        production.index('handled=super.onTouchEvent(event)'))
        self.assertIn('event.actionMasked==MotionEvent.ACTION_DOWN',production)
        self.assertIn('if(isEnabled)',production)
        self.assertIn('event.actionMasked==MotionEvent.ACTION_UP',production)
        self.assertIn('event.actionMasked==MotionEvent.ACTION_CANCEL',production)
        self.assertIn('if(!handled ||',production)
        self.assertIn('if(!enabled) releaseDrag()',production)
        self.assertIn('override fun onDetachedFromWindow()',production)
        self.assertNotIn('MotionEvent.ACTION_POINTER_UP',production)

    def test_diagnostic_failure_keeps_requested_delivered_and_final_geometry(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/VerticalControlReachabilityProbe.kt').read_text()
        wrapper=source.split('private fun observeNativeDrag',1)[1].split('private fun dragState',1)[0]
        self.assertLess(wrapper.index('writeReceipt()'),wrapper.index('trace.attach()'))
        self.assertLess(wrapper.index('trace.attach()'),wrapper.index('action(trace)'))
        self.assertIn('finally {',wrapper)
        self.assertIn('trace.detach();trace.record.put("after",dragState(trace.slider))',wrapper)
        self.assertIn('throw error',wrapper)
        self.assertIn('failure.addSuppressed(error)',wrapper)
        for field in ('requested_quality','before','after_injection','after','outcome','event_time_ms',
                      'down_time_ms','action_masked','local','screen','source','pointer_count',
                      'history_size','before-widget-handler','touch_slop','padding','thumb_offset',
                      'layout_direction','window_focus','scroll_changes','errors','observers_removed'):
            self.assertIn('"'+field+'"',source)
        self.assertIn('val contents=onMain {receipt.toString(2)',source)
        self.assertIn('events.length()<128',source)
        self.assertIn('scrollChanges.length()<64',source)
        self.assertIn('record.getInt("dropped_events")+1',source)
        self.assertIn('record.getInt("dropped_scroll_changes")+1',source)

    def test_diagnostic_preserves_original_gesture_endpoint_wait_and_assertions(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/VerticalControlReachabilityProbe.kt').read_text()
        self.assertIn('device.swipe(arrayOf(first,last,last,last),12)',source)
        self.assertIn('waitUntil("native quality equals $value") {quality().slider.progress+quality().minimum==value}',source)
        self.assertIn('SystemClock.uptimeMillis()+15000',source)
        self.assertIn('assertDraft();assertQualityGeometry()',source)
        self.assertIn('assertNotEquals("Endpoint requires a real value change",value,current)',source)
        self.assertIn('assertNotEquals("Cancel must discard a genuinely changed draft"',source)
        self.assertIn('"Visible numeric readout matches actual native value"',source)
        self.assertEqual(1,source.count('device.click(')) # Existing Choose location only, no tap fallback.


if __name__=='__main__': unittest.main()
