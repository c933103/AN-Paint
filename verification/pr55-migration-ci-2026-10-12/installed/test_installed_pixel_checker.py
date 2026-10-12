"""Synthetic comparator tests; these are not installed Android captures."""
import base64,hashlib,json,pathlib,tempfile,unittest
from unittest.mock import patch
from PIL import Image
import audit_installed_pixels as a
import test_natural_ink_checker as fixtures
class InstalledPixelCheckerTest(unittest.TestCase):
 def write(self,p,mutate=None):
  for route in ('copy','insert'):
   d,actual,ref=fixtures.GlyphInkCheckerTest().frame()
   if mutate:mutate(d,actual,ref)
   d.update(source_tests_sha256='f8f8de6d967000411de5dc6a3e8a8309b6fd61f2eba9e4393556e3ad35fafe3e',locale='ar',api=35,target_sdk=35,font_scale=2,message=route,accessibility_text=route,complete_layout_text=route,root_width=1280,root_height=640,density=2,fingerprint='synthetic-only',default_textview_use_bounds_for_width=False)
   for kind,im in [('actual',actual),('reference',ref)]:
    f=p/(route+'-'+kind+'.png');Image.fromarray(im).save(f);raw=f.read_bytes()
    d[kind+'_png']={'width':im.shape[1],'height':im.shape[0],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'base64':base64.b64encode(raw).decode()}
   (p/(route+'.json')).write_text(json.dumps(d))
 def run_fixture(self,mutate=None):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);self.write(p,mutate)
   with patch.object(a,'messages',return_value={('ar',r):r for r in ('copy','insert')}):return a.audit(p,p)
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
