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
                          '.setProgress(','.progress=', '.setOnSeekBarChangeListener(','.setSelection('):
            self.assertNotIn(forbidden,source)
        for required in ('device.swipe(', 'device.click(', 'visible.contains(raw)', 'canvas.sameAs(',
                         'assertNotEquals("Endpoint requires a real value change"', 'thumbBounds()',
                         'registerFrameCommitCallback', 'destination_requests'):
            self.assertIn(required,source)
        driver=(ROOT/'tools/ci_emulator.sh').read_text()
        self.assertIn('--suite app-vertical --timeout-seconds 180',driver)
        self.assertIn('tools/vertical_control_reachability.py',driver)


if __name__=='__main__': unittest.main()
