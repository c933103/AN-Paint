"""Finite reviewed Tajik additions; historical option registration is not rewritten."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as E
from language_option_additions import SECOND_ADDITIONS_PATH, require_untranslated_option

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'tools/fixtures/current_localization/kazakh_tajik_pashto_priority_wording/tg.json'
FIXTURE_SHA256='8e751faa510cd5cc1e0b01ad7cd8938a1b8ec1be7741276ab8e2f11d3e9f05cd'
TAJIK_OPTION_STATUS='bounded-priority-model-review; incomplete catalogue; no native-human/layout certification'

def resource(e):
 result={'value':e.text if e.tag=='string' else {x.get('quantity'):x.text for x in e},'attributes':dict(e.attrib)}
 if e.tag!='string':result['children_attributes']={x.get('quantity'):dict(x.attrib) for x in e}
 return result

def require_tajik_option_successor(row,xml):
 historical=next(r for r in json.loads(SECOND_ADDITIONS_PATH.read_text())['languages'] if r['tag']=='tg')
 if row!=historical:raise ValueError('Only the exact historical Tajik option may acquire this successor')
 require_untranslated_option(row,'<resources/>')
 raw=FIXTURE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=FIXTURE_SHA256:raise ValueError('Complete reviewed Tajik contract differs')
 fixture=json.loads(raw)
 if fixture['catalogue_path']!=row['catalogue'] or fixture['original_catalogue']:
  raise ValueError('Historical Tajik catalogue must remain explicitly empty')
 from kazakh_tajik_pashto_priority_expectations import require_catalogue
 from current_localization_contracts import residual_rows
 accepted=fixture['values'];root=E.fromstring(xml)
 require_catalogue('tg',root,fixture)
 successors={key:review for (tag,key),review in residual_rows().items() if tag=='tg'}
 nodes={node.get('name'):node for node in root}
 if root.tag!='resources' or root.attrib or (root.text or '').strip() or len(root)!=len(nodes) or set(nodes)!=set(accepted)|set(successors):
  raise ValueError('Tajik successor must contain exactly the reviewed typed resources')
 english={node.get('name'):node for node in E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot()}
 for key,review in successors.items():
  if review['previous_target'] is not None or resource(english[key])!={'value':review['source'],'attributes':review['attributes']}:
   raise ValueError('Tajik residual source/predecessor contract differs: '+key)
 for key,review in accepted.items():
  if 'previous_target' not in review or review['previous_target'] is not None or resource(english[key])!=review['source']:
   raise ValueError('Tajik source/predecessor contract differs: '+key)
  node=nodes[key]
  if (node.tail or '').strip():raise ValueError('Unexpected text after Tajik resource: '+key)
  if node.tag!=review['type'] or node.attrib!=review['reviewed_attributes'] or resource(node)['value']!=review['reviewed_value']:
   raise ValueError('Complete Tajik reviewed resource differs: '+key)
  if node.tag=='string' and len(node):raise ValueError('Unexpected Tajik string markup: '+key)
  if node.tag=='plurals' and ((node.text or '').strip() or len(node)!=len(review['reviewed_value']) or resource(node)['children_attributes']!=review['reviewed_children_attributes'] or any(child.tag!='item' or len(child) or (child.tail or '').strip() for child in node)):
   raise ValueError('Tajik complete plural quantities/attributes differ: '+key)
 return root
