"""Synthetic comparator tests; these are not installed Android captures."""
from audit_natural_artifacts import SOURCE_SHA,LIBRARY_SHA
import base64,hashlib,json,pathlib,tempfile,unittest
from unittest.mock import patch
from PIL import Image
import audit_installed_pixels as a
import numpy as np
from audit_natural_ink import metrics
def frame():
 ref=np.zeros((12,64,4),dtype=np.uint8);ref[4:6,5:8]=[25,35,45,255];ref[4,5]=[12,17,22,1]
 actual=np.zeros((10,64,4),dtype=np.uint8);actual[3:5,5:8]=ref[4:6,5:8]
 d=dict(reference_box="[-2,-2][62,10]",origin_x=2,origin_y=1,content_width=60,alpha_cutoff=0,position_tolerance_px=0,color_tolerance=0,view_use_bounds_for_width=True,layout_use_bounds_for_width=True,shift_drawing_offset_for_start_overhang=False,measured_leading_inset_px=0)
 d.update(metrics(actual,ref,d));return d,actual,ref
class InstalledPixelCheckerTest(unittest.TestCase):
 def write(self,p,mutate=None):
  for route in ('copy','insert'):
   d,actual,ref=frame()
   if mutate:mutate(d,actual,ref)
   d.update(source_tests_sha256=SOURCE_SHA,locale='ar',api=35,target_sdk=35,font_scale=2,message=route,accessibility_text=route,complete_layout_text=route,root_width=1280,root_height=640,density=2,fingerprint='synthetic-only',default_textview_use_bounds_for_width=False)
   for kind,im in [('actual',actual),('reference',ref)]:
    f=p/(route+'-'+kind+'.png');Image.fromarray(im).save(f);raw=f.read_bytes()
    d[kind+'_png']={'width':im.shape[1],'height':im.shape[0],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'base64':base64.b64encode(raw).decode()}
   (p/(route+'.json')).write_text(json.dumps(d))
 def run_fixture(self,mutate=None):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);self.write(p,mutate)
   compiled={'status':'PASS','tree':a.TREE,'merge':a.MERGE,'run_id':int(a.RUN),'apk_sha256':'synthetic-only','composed_route_text':{r:r for r in ('copy','insert')}}
   with patch.object(a,'messages',return_value={('ar',r):r for r in ('copy','insert')}),patch.object(a,'compiled_report',return_value=compiled),patch.object(a,'compiled_report_digest',return_value='synthetic-only'):return a.audit(p,p)
 def test_both_full_images_pass(self):self.assertEqual('PASS',self.run_fixture()['status'])
 def test_removed_alpha_one_fails(self):
  def mutate(d,actual,reference):actual[3,5]=0
  with self.assertRaisesRegex(ValueError,'metric differs'):self.run_fixture(mutate)
 def test_argb_changed_fails(self):
  def mutate(d,actual,reference):actual[3,5,0]+=1
  with self.assertRaisesRegex(ValueError,'metric differs'):self.run_fixture(mutate)
 def test_relaxed_alpha_or_shift_mode_fails(self):
  for k,v in [('alpha_cutoff',1),('shift_drawing_offset_for_start_overhang',True)]:
   with self.assertRaises(ValueError):self.run_fixture(lambda d,a,r:d.update({k:v}))
if __name__=='__main__':unittest.main()
