"""Complete independently reviewed values; JVM progress behavior is a separate gate."""
import json,unittest,xml.etree.ElementTree as ET
from current_localization_contracts import require_string
import translation_catalogues as c
def canonical_path(row):
 path=(c.ROOT/row["path"]).resolve()
 expected=c.catalogue_paths().get(row["tag"])
 if expected is None or path != expected.resolve():
  raise ValueError("Locale tag/path mismatch")
 return path

class OpenReviewRecoveryTest(unittest.TestCase):
 def test_all_six_values_and_source_bindings(self):
  rows=json.loads((c.ROOT/'tools/fixtures/current_localization/open_review_recovery.json').read_text())
  self.assertEqual(6,len(rows));self.assertEqual(6,len({(r['tag'],r['key']) for r in rows}))
  english=ET.parse(c.RES/'values/strings.xml').getroot()
  for r in rows:
   self.assertEqual(r['english'],english.find(f"string[@name='{r['key']}']").text)
   text=canonical_path(r).read_text()
   limits={'attributes':r['attributes'],'formatted':r['attributes'].get('formatted')!='false','placeholders':c.placeholders(r['english']),'escaped_newline_count':r['english'].count('\\n')}
   require_string(text,r['key'],r['value'],limits)
   for value in ['',r['value'][:-1],r['value']+' %9$s']:
    root=ET.fromstring(text);root.find(f"string[@name='{r['key']}']").text=value
    with self.assertRaises(ValueError):require_string(ET.tostring(root,encoding='unicode'),r['key'],r['value'],limits)
 def test_relabels_and_noncanonical_paths_are_rejected(self):
  rows=json.loads((c.ROOT/"tools/fixtures/current_localization/open_review_recovery.json").read_text())
  for row in rows:
   for mutation in [dict(row,tag="id" if row["tag"] != "id" else "ms"),dict(row,path="tools/fixtures/not-an-android-catalogue.xml")]:
    with self.assertRaises(ValueError): canonical_path(mutation)
 def test_progress_remains_an_ordered_processed_count(self):
  rows=json.loads((c.ROOT/'tools/fixtures/current_localization/open_review_recovery.json').read_text())
  rows=[r for r in rows if r['key']=='ui_rendering_images']
  self.assertEqual({'ms','id','ja','zh-HK'},{r['tag'] for r in rows})
  for r in rows:
   self.assertLess(r['value'].index('%1$s'),r['value'].index('%2$s'))
   self.assertTrue(r['value'].endswith('…'))
if __name__=='__main__':unittest.main()
