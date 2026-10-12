"""Synthetic checker controls only; none of these pixels are Android evidence."""
import copy,json,pathlib,tempfile,unittest
import numpy as np
from PIL import Image
import audit_glyph_ink as a
MESSAGES={(t,route):route+' '+t for t in a.TAGS for route in ('copy','insert')}
class GlyphInkCheckerTest(unittest.TestCase):
 def frame(self,delta=0,clip=None,cw=60,before=False):
  ox=2;oy=1;left=min(0,3+delta)-2;right=max(cw,6+delta)+2;top=-2;bottom=10
  ref=np.zeros((bottom-top,right-left,4),dtype=np.uint8)
  ref[2-top:4-top,3+delta-left:6+delta-left]=[25,35,45,255]
  ref[2-top,3+delta-left]=[12,17,22,1]
  actual=np.zeros((10,cw+4,4),dtype=np.uint8)
  for y,x in zip(*np.nonzero(ref[:,:,3])):
   vx=x+left+ox;vy=y+top+oy
   if 0<=vx<actual.shape[1] and 0<=vy<10:actual[vy,vx]=ref[y,x]
  if clip=='first':actual[:,:ox+4]=0
  if clip=='last':actual[:,ox+5:]=0
  if before:actual[:,ox+cw:]=0
  data={'reference_source':a.REF_SOURCE,'evidence_kind':a.EVIDENCE,'reference_box':f'[{left},{top}][{right},{bottom}]','glyph_bounds':f'RectF({3+delta}.0, 2.0, {6+delta}.0, 4.0)','origin_x':ox,'origin_y':oy,'content_width':cw,'alpha_cutoff':0,'position_tolerance_px':0,'color_tolerance':0,'view_use_bounds_for_width':not before,'layout_use_bounds_for_width':not before,'shift_drawing_offset_for_start_overhang':False,'measured_leading_inset_px':0}
  data.update(a.metrics(actual,ref,data));return data,actual,ref
 def write(self,directory,stem,**kw):
  data,actual,ref=self.frame(**kw);(directory/(stem+'.json')).write_text(json.dumps(data));Image.fromarray(actual).save(directory/(stem+'-actual-textview.png'));Image.fromarray(ref).save(directory/(stem+'-complete-layout.png'));return data
 def fixture(self,directory):
  for t in a.TAGS:
   for scale in (1.0,2.0):
    for action in ('copy','insert'):self.write(directory,f'api35-{t}-640x320-font{scale}-{action}')
  for scale in (1.0,2.0):
   outcomes=[];resets=[]
   for t in a.CONTROL_TAGS:
    base=f'api35-{t}-640x320-font{scale}-negative-controls';self.write(directory,base+'-intact');cases=[]
    for mutation,delta,clip in [('left-overflow',-4,None),('right-overflow',55,None),('wholly-left-of-view',-240,None),('wholly-right-of-view',240,None),('clip-first-spatial-ink',0,'first'),('clip-last-spatial-ink',0,'last')]:
     data=self.write(directory,base+'-'+mutation,delta=delta,clip=clip);data.pop('evidence_kind');cases.append(data|{'mutation':mutation,'rejected':True,'reason':'clipped expected ink' if clip else 'horizontal painted-ink overflow'})
    outcomes.append({'locale':t,'font_scale':scale,'intact_passed':True,'logical_first_character_is_rtl':t=='ar','cases':cases})
    cases=[]
    for kind in ('width','font','mixed-paragraphs','short-message','restored'):
     data=self.write(directory,base+'-reset-'+kind,cw=12 if kind=='width' else 60);data.pop('evidence_kind')
     msg=MESSAGES[(t,'copy')]
     if kind=='mixed-paragraphs':msg+='\nABC\nالعربية'
     if kind=='short-message':msg='OK'
     cases.append(data|{'case':kind,'message':msg,'text_size_px':15 if kind=='font' else 20,'view_width':16 if kind=='width' else 64})
    resets.append({'profile':base,'initial_inset':0,'repeat_count':3,'cases':cases,'all_passed':True})
   (directory/f'native-negative-controls-font{scale}.json').write_text(json.dumps(outcomes));(directory/f'native-inset-resets-font{scale}.json').write_text(json.dumps(resets))
  self.write(directory,'api35-ar-640x320-font2.0-negative-controls-original-plain-before',delta=55,before=True)
 def test_complete_181_frames_and_four_receipts(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);self.fixture(p);r=a.audit(p,MESSAGES);self.assertEqual('PASS',r['status'],r['errors']);self.assertEqual(181,r['checked_frames']);self.assertEqual(4,len(r['control_receipts']))
 def test_alpha_one_and_exact_argb_are_retained(self):
  d,actual,ref=self.frame();self.assertEqual(6,d['ink_pixels']);actual[3,5,0]+=1;self.assertEqual(1,a.metrics(actual,ref,d)['different_argb_pixels']);actual[3,5]=0;self.assertEqual(1,a.metrics(actual,ref,d)['missing_expected_ink_pixels'])
 def test_wrong_mode_shift_or_tolerance_fails(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);self.fixture(p);m=p/'api35-en-GB-640x320-font1.0-copy.json';raw=m.read_bytes()
   for key,value in [('view_use_bounds_for_width',False),('shift_drawing_offset_for_start_overhang',True),('alpha_cutoff',1)]:
    d=json.loads(raw);d[key]=value;m.write_text(json.dumps(d));self.assertEqual('FAIL',a.audit(p,MESSAGES)['status']);m.write_bytes(raw)
 def test_false_reset_receipt_and_missing_before_fail(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);self.fixture(p);m=p/'native-inset-resets-font1.0.json';raw=m.read_bytes();rows=json.loads(raw);rows[0]['cases'][0]['message']='wrong';m.write_text(json.dumps(rows));self.assertEqual('FAIL',a.audit(p,MESSAGES)['status']);m.write_bytes(raw)
   (p/'api35-ar-640x320-font2.0-negative-controls-original-plain-before.json').unlink();self.assertEqual('FAIL',a.audit(p,MESSAGES)['status'])
 def test_original_before_must_really_clip(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);self.fixture(p);self.write(p,'api35-ar-640x320-font2.0-negative-controls-original-plain-before',before=True);r=a.audit(p,MESSAGES);self.assertEqual('FAIL',r['status']);self.assertTrue(any('did not reproduce' in str(x) for x in r['errors']))
 def test_unapplied_translation_cannot_be_hidden_by_updated_counts(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);self.fixture(p);base='api35-en-GB-640x320-font1.0-negative-controls';stem=base+'-left-overflow';actual=p/(stem+'-actual-textview.png');actual.write_bytes((p/(base+'-intact-actual-textview.png')).read_bytes());m=p/(stem+'.json');d=json.loads(m.read_bytes());d.update(a.metrics(a.read_rgba(actual),a.read_rgba(p/(stem+'-complete-layout.png')),d));m.write_text(json.dumps(d));receipt=p/'native-negative-controls-font1.0.json';rows=json.loads(receipt.read_bytes());rows[0]['cases'][0]={k:v for k,v in d.items() if k!='evidence_kind'}|{'mutation':'left-overflow','rejected':True,'reason':'horizontal painted-ink overflow'};receipt.write_text(json.dumps(rows));r=a.audit(p,MESSAGES);self.assertEqual('FAIL',r['status']);self.assertTrue(any('actual native translation differs' in str(x) for x in r['errors']),r['errors'])
if __name__=='__main__':unittest.main()
