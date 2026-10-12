import sys,pathlib,json,unittest,io
from unittest.mock import patch
s=pathlib.Path('/workspace/shared/anpaint-pr55-reviewability-migration-20261012');sys.path.insert(0,str(s/'tools'))
import test_current_localization_contracts as m
real=m.fixture

def mutated(name):
 d=real(name)
 if name=='commons_metadata_current_wording.json':
  for field in ('values','constraints','nfc_and_no_category_C_required','special_codepoint_counts'):
   d.get(field,{}).pop('commons_metadata_http_error',None)
 if name=='commons_svg_current_wording.json':
  d['values']={};d['constraints']={};d['special_codepoint_counts']={}
 return d
with patch.object(m,'fixture',mutated):
 stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(m))
 print(stream.getvalue());print(json.dumps({'negative_fixture_mutation':'Remove HTTP contract and all SVG value contracts from compact fixtures in memory','tests':r.testsRun,'unexpectedly_all_pass':r.wasSuccessful(),'source_or_fixture_files_changed':False}))
