import copy,unittest
from audit_retained_notice import check_rails,EVIDENCE
class RetainedNoticeControls(unittest.TestCase):
 def sample(self,tag='lzh-Hant',offset=47):
  return {'evidence_kind':EVIDENCE,'rails':[{'range':200,'scroll_x':200-offset if tag=='lzh-Hant' else offset,'reading_offset':offset,'viewport_width':400} for _ in range(2)]}
 def test_both_directions_both_offsets(self):
  for tag in ('lzh-Hant','mn-Mong'):
   for offset in (0,47):check_rails(self.sample(tag,offset),tag,offset)
 def test_changed_offset_rejected(self):
  d=self.sample();d['rails'][0]['reading_offset']=0
  with self.assertRaises(ValueError):check_rails(d,'lzh-Hant',47)
 def test_wrong_direction_rejected(self):
  with self.assertRaises(ValueError):check_rails(self.sample(),'mn-Mong',47)
 def test_invalid_range_rejected(self):
  d=self.sample();d['rails'][0]['range']=47
  with self.assertRaises(ValueError):check_rails(d,'lzh-Hant',47)
 def test_missing_duplicate_shape_rejected(self):
  for n in (0,1,3):
   d=self.sample();d['rails']=(d['rails']*2)[:n]
   with self.assertRaises(ValueError):check_rails(d,'lzh-Hant',47)
 def test_invalid_viewport_rejected(self):
  d=self.sample();d['rails'][0]['viewport_width']=0
  with self.assertRaises(ValueError):check_rails(d,'lzh-Hant',47)
 def test_boolean_geometry_rejected(self):
  d=self.sample();d['rails'][0]['viewport_width']=True
  with self.assertRaises(ValueError):check_rails(d,'lzh-Hant',47)
 def test_extra_fields_rejected(self):
  d=self.sample();d['rails'][0]['ignored']=1
  with self.assertRaises(ValueError):check_rails(d,'lzh-Hant',47)
if __name__=='__main__':unittest.main()
