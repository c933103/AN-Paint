"""Check the frozen independent receipt plus explicit assembly rebind against a checkout.
Usage: python3 verify_current_source_rebind.py /path/to/AN-Paint
This is structural binding, not a new linguistic or runtime review.
"""
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
root = Path(sys.argv[1])
receipt = json.loads((HERE / 'independent-review.json').read_text())
rebind = json.loads((HERE / 'assembly-current-source-rebind.json').read_text())
def catalogue(directory):
    result = {}
    for node in ET.parse(root / 'Paintroid/src/main/res' / directory / 'strings.xml').getroot():
        if node.get('translatable') == 'false':
            continue
        key = node.tag + '/' + node.get('name')
        if key in result:
            raise ValueError('Duplicate identity: ' + key)
        result[key] = node
    return result

def value(node):
    return {i.get('quantity'): i.text for i in node} if node.tag == 'plurals' else node.text

def require(actual, expected, description):
    if actual != expected:
        raise ValueError(description)

source, target = catalogue('values'), catalogue('values-sv')
require(set(source), {e['identity'] for e in receipt['entries']}, 'Current source identity drift')
bound = 0
for entry in receipt['entries']:
    identity = entry['identity']
    current_source = rebind['source'] if identity == rebind['identity'] else entry['english']
    require(value(source[identity]), current_source, 'Current source value drift: ' + identity)
    require(source[identity].attrib, entry['source_attributes'], 'Current source attribute drift: ' + identity)
    accepted = entry['decision'].startswith(('accepted_', 'retained_prior_')) or identity == rebind['identity']
    if accepted:
        proposed = rebind['target'] if identity == rebind['identity'] else entry['swedish']
        require(value(target[identity]), proposed, 'Application target drift: ' + identity)
        require(target[identity].attrib, entry['source_attributes'], 'Application attributes drift: ' + identity)
        bound += 1
require(bound, 714, 'Unexpected bounded count')
require(set(source) - set(target), {'string/ui_foreground_background_colour_palette',
                                  'string/ui_the_arrow_on_the_left_directly_below_the'}, 'Missing catalogue identities')
require(value(target['string/ui_main23']), 'Huvud', 'Held Main changed')
print('PASS: all 717 complete current source values and attributes; 714 bounded target values and attributes; 715 present; 3 explicit holds.')
