"""Negative controls of candidate bindings/tokens, including actual formatted=false values."""
import copy,json,unittest
from pathlib import Path
import verify_candidates as v
R=Path(__file__).resolve().parents[1]
class CandidateControls(unittest.TestCase):
 def test_all_real_values_reject_binding_encoding_and_format_corruption(self):
  src={e['identity']:e for e in v.load(R/'packet/shared-source-context.json')['entries']}
  mutations=0;false_mutations=0
  for tag in ('sr-Cyrl','sr-Latn'):
   for original in v.load(R/'drafts'/f'{tag}-candidates.json')['candidates']:
    e=src[original['identity']]
    for field,changed in [('source',original['source']+'x'),('attributes',dict(original['attributes'],formatted='invented')),('identity','string/held'),('proposed_xml_text',''),('proposed_xml_text','""'),('semantic_rationale',''),('uncertainties',None)]:
     d=copy.deepcopy(original);d[field]=changed
     with self.subTest(tag=tag,key=e['identity'],field=field),self.assertRaises(ValueError):v.verify_entry(d,e)
     mutations+=1
    for suffix in [' %9$s',' %n',' %%',' %s',' %',' %q',' %1$',' %.2f']:
     d=copy.deepcopy(original);d['proposed_xml_text']=d['proposed_xml_text'][:-1]+suffix+'"'
     with self.subTest(tag=tag,key=e['identity'],suffix=suffix),self.assertRaises(ValueError):v.verify_entry(d,e)
     mutations+=1
     if e['attributes'].get('formatted')=='false':false_mutations+=1
  self.assertEqual(2220,mutations);self.assertEqual(16,false_mutations)
 def test_duplicate_JSON_identity_is_rejected(self):
  with self.assertRaises(ValueError):json.loads('{"a":1,"a":2}',object_pairs_hook=v.unique)
 def test_source_token_parser_keeps_index_type_precision_flags(self):
  original='%1$d %2$d %3$.2f %4$.2f'
  for x in ['%3$.3f','%3$f','%3$-10.2f','%9$.2f','%.2f','%3$.2d']:
   self.assertNotEqual(v.tokens(original),v.tokens(original.replace('%3$.2f',x)))
if __name__=='__main__':unittest.main()
