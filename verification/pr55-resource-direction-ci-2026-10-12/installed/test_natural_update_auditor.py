"""Synthetic log-schema controls only; never installed or PNG execution evidence."""
import copy,json,unittest
import audit_natural_update as a
class NaturalUpdateAuditorTests(unittest.TestCase):
 def fixture(self):
  rows=[];frames={}
  for route in ('copy','insert'):
   d=dict(schema=1,route=route,source_tests_sha256=a.SOURCE_SHA,status_class=a.STATUS_CLASS,old_message=a.MESSAGES['insert' if route=='copy' else 'copy'],message=a.MESSAGES[route],old_layout_height=88,view_width=640,root_requested_before=False,view_requested_before=False,view_requested_after=True,root_requested_after=True,new_layout_height=88,complete_layout_text=a.MESSAGES[route],root_requested_settled=False,view_requested_settled=False)
   frames[route]=dict(source_tests_sha256=a.SOURCE_SHA,route=route,locale='ar',api=35,target_sdk=35,font_scale=2,message=d['message'],accessibility_text=d['message'],complete_layout_text=d['message'],ink_pixels=5,origin_y=0,actual_png={'width':640,'height':92},**dict.fromkeys(a.FAILURES,0));rows.append(d)
  return rows,frames
 def encoded(self,rows):return ('\n'.join('10-12 15:00:01.123  100  100 I GalleryStatusNaturalUpdate: '+(r if isinstance(r,str) else json.dumps(r,ensure_ascii=False)) for r in rows)+'\n').encode()
 def test_exact_pair_passes(self):
  rows,frames=self.fixture();self.assertEqual('PASS_NATURAL_LOG_CONSISTENCY',a.audit(self.encoded(rows),frames)['status'])
 def test_missing_duplicate_extra_and_reversed_routes_fail(self):
  rows,frames=self.fixture()
  for bad in [rows[:1],rows+[rows[0]],list(reversed(rows)),rows+[dict(rows[0],route='other')]]:
   with self.assertRaises(ValueError):a.audit(self.encoded(bad),frames)
 def test_malformed_duplicate_field_nonfinite_unknown_and_truncated_json_fail(self):
  rows,frames=self.fixture();text=json.dumps(rows[0])
  for bad in [text[:-1],text+'garbage',text.replace('"schema": 1','"schema": 1, "schema": 1'),text.replace('"old_layout_height": 88','"old_layout_height": NaN'),json.dumps(dict(rows[0],extra='unknown'))]:
   with self.assertRaises(ValueError):a.audit(self.encoded([bad,rows[1]]),frames)
 def test_wrong_source_class_text_or_state_fails(self):
  rows,frames=self.fixture()
  for key,value in [('source_tests_sha256','0'*64),('status_class','android.widget.TextView'),('old_message',rows[0]['message']),('message','wrong'),('complete_layout_text','wrong'),('root_requested_before',True),('view_requested_before',True),('view_requested_after',False),('view_requested_settled',True),('root_requested_settled',True),('root_requested_after',1)]:
   with self.assertRaises(ValueError):a.audit(self.encoded([dict(rows[0],**{key:value}),rows[1]]),frames)
 def test_zero_unequal_boolean_or_raster_mismatched_geometry_fails(self):
  rows,frames=self.fixture()
  for key,value in [('old_layout_height',0),('new_layout_height',89),('new_layout_height',True),('view_width',641)]:
   with self.assertRaises(ValueError):a.audit(self.encoded([dict(rows[0],**{key:value}),rows[1]]),frames)
 def test_failed_empty_wrong_source_or_incomplete_raster_is_not_promoted(self):
  rows,frames=self.fixture()
  for key,value in [('horizontal_overflow_pixels',1),('missing_expected_ink_pixels',1),('different_argb_pixels',1),('ink_pixels',0),('source_tests_sha256','0'*64),('complete_layout_text','cut')]:
   bad=copy.deepcopy(frames);bad['copy'][key]=value
   with self.assertRaises(ValueError):a.audit(self.encoded(rows),bad)
 def test_malformed_tagged_line_is_not_ignored(self):
  rows,frames=self.fixture();raw=self.encoded(rows)+b'bad GalleryStatusNaturalUpdate: {}\n'
  with self.assertRaises(ValueError):a.audit(raw,frames)
if __name__=='__main__':unittest.main()
