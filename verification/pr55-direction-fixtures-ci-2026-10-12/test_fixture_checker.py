"""Synthetic controls for independent audit code, not Android runtime evidence."""
import json,pathlib,tempfile,unittest,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
import audit_fixture_ink as ink
import audit_fixture_artifacts as app
class FixtureCheckerControls(unittest.TestCase):
 def specimen(self):
  r=np.zeros((8,10,4),dtype=np.uint8);r[2,2:5]=[0,0,0,255];r[2,5]=[0,0,0,1];r[5,7]=[0,0,0,7]
  return r.copy(),r,{'reference_box':'[0,0][10,8]','origin_x':0,'origin_y':0,'content_width':10}
 def test_every_alpha_sample_counted(self):
  a,r,d=self.specimen();m=ink.metrics(a,r,d);self.assertEqual(5,m['ink_pixels']);self.assertEqual(2,m['ink_components']);self.assertEqual(0,m['missing_complete_components'])
 def test_partial_alpha_one_loss_remains_exact_difference(self):
  a,r,d=self.specimen();a[2,5]=0;m=ink.metrics(a,r,d);self.assertEqual(1,m['missing_expected_ink_pixels']);self.assertEqual(1,m['different_argb_pixels']);self.assertEqual(0,m['missing_complete_components']);self.assertEqual(0,m['missing_opaque_reference_pixels'])
 def test_detached_translucent_mark_loss_is_hard(self):
  a,r,d=self.specimen();a[5,7]=0;m=ink.metrics(a,r,d);self.assertEqual(1,m['missing_complete_components']);self.assertEqual(0,m['missing_opaque_reference_pixels'])
 def test_opaque_loss_guard_independent_of_component(self):
  a,r,d=self.specimen();a[2,3]=0;m=ink.metrics(a,r,d);self.assertEqual(1,m['missing_opaque_reference_pixels']);self.assertEqual(0,m['missing_complete_components'])
 def test_transparent_opaque_change_not_missing(self):
  a,r,d=self.specimen();a[2,3,3]=254;m=ink.metrics(a,r,d);self.assertEqual(0,m['missing_opaque_reference_pixels']);self.assertEqual(1,m['different_argb_pixels'])
 def test_outside_view_and_content_are_independent(self):
  a,r,d=self.specimen();d['origin_x']=20;m=ink.metrics(a,r,d);self.assertEqual(5,m['outside_view_pixels']);self.assertEqual(0,m['horizontal_overflow_pixels']);self.assertEqual(2,m['missing_complete_components'])
 def test_junit_exact_identity_multiset(self):
  expected=[('Example','one'),('Example','two')]
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td)
   def put(ids,skip=False):
    root=ET.Element('testsuite',tests=str(len(ids)),failures='0',errors='0',skipped=str(int(skip)))
    for i,(cls,name) in enumerate(ids):
     node=ET.SubElement(root,'testcase',classname=cls,name=name)
     if i==0 and skip:ET.SubElement(node,'skipped')
    (p/'TEST-check.xml').write_bytes(ET.tostring(root))
   put(expected);self.assertEqual('PASS',app.junit_audit(p,expected)['status'])
   for altered in (expected[:-1],[expected[0],expected[0]],[('Example','one'),('Example','foreign')]):
    put(altered);self.assertEqual('FAIL',app.junit_audit(p,expected)['status'])
   put(expected,True);self.assertEqual('FAIL',app.junit_audit(p,expected)['status'])
 def test_hard_positive_guard_does_not_hide_partial_differences(self):
  a,r,d=self.specimen();a[2,5]=0;m=ink.metrics(a,r,d);ink.intact(m)
  a[5,7]=0;m=ink.metrics(a,r,d)
  with self.assertRaisesRegex(ValueError,'missing_complete_components'):ink.intact(m)
if __name__=='__main__':unittest.main(verbosity=2)
