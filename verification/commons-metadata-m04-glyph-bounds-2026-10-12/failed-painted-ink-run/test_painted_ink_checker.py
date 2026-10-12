import unittest,tempfile,pathlib,json,copy
import numpy as np
from PIL import Image
import audit_painted_ink as a
class PixelCheckerTest(unittest.TestCase):
    def frame(self,delta=0,clip=None):
        cw=12;ox=2;oy=1;left=min(0,delta)-2;right=max(cw,cw+delta)+2;top=-2;bottom=8
        ref=np.zeros((bottom-top,right-left,4),dtype=np.uint8)
        ref[2-top:4-top,3+delta-left:6+delta-left]=[25,35,45,255]
        ref[2-top,3+delta-left]=[12,17,22,1]
        actual=np.zeros((10,16,4),dtype=np.uint8)
        for y,x in zip(*np.nonzero(ref[:,:,3])):
            vx=x+left+ox;vy=y+top+oy
            if 0<=vx<16 and 0<=vy<10:actual[vy,vx]=ref[y,x]
        if clip=='first':actual[:,:ox+4]=0
        elif clip=='last':actual[:,ox+5:]=0
        data={'reference_source':a.REF_SOURCE,'evidence_kind':a.EVIDENCE,'reference_box':f'[{left},{top}][{right},{bottom}]','glyph_bounds':f'RectF({3+delta}, 2 - {6+delta}, 4)','origin_x':ox,'origin_y':oy,'content_width':cw,'alpha_cutoff':0,'position_tolerance_px':0,'color_tolerance':0}
        data.update(a.metrics(actual,ref,data));return data,actual,ref
    def write(self,directory,stem,delta=0,clip=None):
        data,actual,ref=self.frame(delta,clip);(directory/(stem+'.json')).write_text(json.dumps(data));Image.fromarray(actual).save(directory/(stem+'-actual-textview.png'));Image.fromarray(ref).save(directory/(stem+'-complete-layout.png'));return data
    def fixture(self,directory):
        for t in a.TAGS:
            for s in (1.0,2.0):
                for action in ('copy','insert'):self.write(directory,f'api35-{t}-640x320-font{s}-{action}')
        for s in (1.0,2.0):
            receipts=[]
            for t in a.CONTROL_TAGS:
                base=f'api35-{t}-640x320-font{s}-negative-controls';self.write(directory,base+'-intact');cases=[]
                for mutation,delta,clip in [('left-overflow',-4,None),('right-overflow',7,None),('wholly-left-of-view',-48,None),('wholly-right-of-view',48,None),('clip-first-spatial-ink',0,'first'),('clip-last-spatial-ink',0,'last')]:
                    data=self.write(directory,base+'-'+mutation,delta,clip);data.pop('evidence_kind');cases.append(data|{'mutation':mutation,'rejected':True,'reason':'clipped expected ink' if clip else 'horizontal painted-ink overflow'})
                receipts.append({'locale':t,'font_scale':s,'intact_passed':True,'logical_first_character_is_rtl':t=='ar','cases':cases})
            (directory/f'native-negative-controls-font{s}.json').write_text(json.dumps(receipts))
    def test_full_schema_positive_and_72_real_pixel_mutants(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp);self.fixture(p);r=a.audit(p);self.assertEqual('PASS',r['status'],r['errors']);self.assertEqual(120,r['checked_frames']);self.assertEqual(2,len(r['control_receipts']))
    def test_alpha_one_pixel_and_one_color_level_are_not_masked(self):
        data,actual,ref=self.frame();self.assertEqual(6,data['ink_pixels']);actual[3,5,0]+=1
        self.assertEqual(1,a.metrics(actual,ref,data)['different_argb_pixels']);actual[3,5]=0
        self.assertEqual(1,a.metrics(actual,ref,data)['missing_expected_ink_pixels'])
    def test_wholly_displaced_reference_retains_ink_and_catches_overflow(self):
        for delta in (-48,48):
            data,actual,ref=self.frame(delta);self.assertEqual(6,data['ink_pixels']);self.assertEqual(6,data['horizontal_overflow_pixels']);self.assertEqual(6,data['outside_view_pixels']);self.assertEqual(0,data['allocation_edge_pixels']);self.assertFalse(actual.any())
    def test_missing_duplicate_receipt_or_relaxed_tolerance_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp);self.fixture(p);summary=p/'native-negative-controls-font1.0.json';original=summary.read_bytes();rows=json.loads(original);rows[0]['cases'][1]=copy.deepcopy(rows[0]['cases'][0]);summary.write_text(json.dumps(rows));self.assertEqual('FAIL',a.audit(p)['status']);summary.write_bytes(original)
            m=p/'api35-en-GB-640x320-font1.0-copy.json';data=json.loads(m.read_bytes());data['alpha_cutoff']=1;m.write_text(json.dumps(data));self.assertEqual('FAIL',a.audit(p)['status']);m.unlink();self.assertEqual('FAIL',a.audit(p)['status'])
    def test_false_report_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp);self.fixture(p);stem='api35-en-GB-640x320-font1.0-negative-controls-left-overflow';meta=p/(stem+'.json');data=json.loads(meta.read_bytes());data['horizontal_overflow_pixels']=0;meta.write_text(json.dumps(data));self.assertEqual('FAIL',a.audit(p)['status'])
    def test_unapplied_actual_translation_rejected_even_with_forged_consistent_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp);self.fixture(p);base='api35-en-GB-640x320-font1.0-negative-controls';stem=base+'-left-overflow'
            actualpath=p/(stem+'-actual-textview.png');actualpath.write_bytes((p/(base+'-intact-actual-textview.png')).read_bytes())
            meta=p/(stem+'.json');data=json.loads(meta.read_bytes());data.update(a.metrics(a.read_rgba(actualpath),a.read_rgba(p/(stem+'-complete-layout.png')),data));meta.write_text(json.dumps(data))
            summary=p/'native-negative-controls-font1.0.json';rows=json.loads(summary.read_bytes());rows[0]['cases'][0]={k:v for k,v in data.items() if k!='evidence_kind'}|{'mutation':'left-overflow','rejected':True,'reason':'horizontal painted-ink overflow'};summary.write_text(json.dumps(rows))
            result=a.audit(p);self.assertEqual('FAIL',result['status']);self.assertTrue(any('actual native translation differs' in str(e) for e in result['errors']),result['errors'])
if __name__=='__main__':unittest.main()
