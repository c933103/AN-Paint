"""Exact PCM/TPI additions to unchanged historical option registration."""
import json
from pathlib import Path
import xml.etree.ElementTree as E
from language_option_additions import SECOND_ADDITIONS_PATH, require_untranslated_option
from sindhi_nigerian_pidgin_tok_pisin_priority_expectations import bound_fixture, require_catalogue
ROOT=Path(__file__).resolve().parents[1]
TAGS=('pcm','tpi')

def resource(node):
    d={'value':node.text if node.tag=='string' else {x.get('quantity'):x.text for x in node},'attributes':dict(node.attrib)}
    if node.tag=='plurals':d['children_attributes']={x.get('quantity'):dict(x.attrib)for x in node}
    return d

def require_pidgin_option_successor(row,xml):
    if not isinstance(row,dict) or row.get('tag') not in TAGS:raise ValueError('Outside exact two-option scope')
    tag=row['tag'];historical=next(r for r in json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']if r['tag']==tag)
    if row!=historical:raise ValueError('Historical option registration differs')
    require_untranslated_option(row,'<resources/>')
    data=bound_fixture(tag)
    if data['catalogue_path']!=row['catalogue'] or data['original_catalogue']:raise ValueError('Expected exact historical empty catalogue')
    english={n.get('name'):n for n in E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot()}
    for key,r in data['values'].items():
        if 'previous_target' not in r or r['previous_target'] is not None or resource(english[key])!=r['source']:raise ValueError('Actual source or absent predecessor differs: '+key)
    try:root=E.fromstring(xml)
    except (E.ParseError,TypeError) as error:raise ValueError('Malformed option XML') from error
    return require_catalogue(tag,root,data)
