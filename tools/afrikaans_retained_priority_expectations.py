"""Finite current Afrikaans expectations; complete earlier acceptances remain immutable."""
import re
from current_localization_contracts import fixture
NAME='afrikaans_retained_priority_wording.json'
def current_row(key):
 d=fixture(NAME)
 if d['locale']!='af' or key not in d['accepted']:raise ValueError('Outside accepted Afrikaans scope')
 return {'source':d['sources'][key]['value'],'target':d['accepted'][key],'type':d['sources'][key]['type'],'attributes':d['attributes'][key],'previous':d['predecessors'].get(key)}
def decode(v):
 if v.startswith('"')and v.endswith('"'):v=v[1:-1]
 return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),v)
def display(key):
 v=current_row(key)['target']
 if isinstance(v,dict):return {q:decode(t)for q,t in v.items()}
 if v.startswith('@string/'):
  if (key,v)!=('ui_save_a5d0d9','@string/ui_save'):raise ValueError('Unexpected alias')
  return decode(current_row('ui_save')['target'])
 return decode(v)
