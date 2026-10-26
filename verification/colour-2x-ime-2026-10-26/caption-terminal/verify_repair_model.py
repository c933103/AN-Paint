"""Verify actual focused JVM XML against the frozen repair's declared methods."""
from pathlib import Path
from copy import deepcopy
import argparse, hashlib, json, re, zipfile
import xml.etree.ElementTree as ET

def need(value, message):
    if not value:
        raise ValueError(message)

def verify(root, expected):
    need(root.tag == 'testsuite', 'JVM suite root')
    need(root.get('name') == 'org.catrobat.paintroid.local.AdvancedColourViewportTest', 'JVM class')
    cases = root.findall('testcase')
    need(int(root.get('tests')) == len(cases) == len(expected), 'JVM declared/actual count')
    actual = {(case.get('classname'), case.get('name')) for case in cases}
    need(len(actual) == len(cases) and actual == expected, 'JVM exact source/variant inventory')
    need(all(int(root.get(key, 0)) == 0 for key in ('failures', 'errors', 'skipped')), 'JVM failure/error/skip')
    need(all(not list(case) for case in cases), 'JVM non-passing case')
    return [{'name': case.get('name'), 'seconds': case.get('time')} for case in cases]

p = argparse.ArgumentParser()
p.add_argument('--source-root', type=Path, required=True)
p.add_argument('--directory', type=Path, required=True)
a = p.parse_args()
source = a.source_root / 'Paintroid/src/test/java/org/catrobat/paintroid/local/AdvancedColourViewportTest.kt'
text = source.read_text()
need('@Config(sdk=[30,35]' in text, 'Configured model SDK inventory')
methods = re.findall(r'@Test\s+(?:@[\w.]+(?:\([^()]*\))?\s+)*fun\s+(\w+)\s*\(', text)
need(len(methods) == len(set(methods)) == len(re.findall(r'@Test\b', text)) == 9, 'Unparsed or changed model inventory')
need({'largeShortEditorScrollsTabsAndEveryFullCaptionLineWithoutShrinking',
      'modestlyEnlargedEditorRetainsCaptionsAndIdentityAcrossRepeatedReparenting'} <= set(methods), 'Missing new strict models')
owner = 'org.catrobat.paintroid.local.AdvancedColourViewportTest'
expected = {(owner, method + suffix) for method in methods for suffix in ('', '[30]')}
name = 'Paintroid/build/test-results/testDebugUnitTest/TEST-' + owner + '.xml'
archive = a.directory / 'regression-and-lint.zip'
with zipfile.ZipFile(archive) as z:
    need(z.namelist().count(name) == 1, 'Missing/duplicate actual JVM XML')
    raw = z.read(name)
root = ET.fromstring(raw)
cases = verify(root, expected)
rejected = 0
for mutation in ('missing-variant', 'duplicate-variant', 'skipped', 'renamed-case'):
    broken = deepcopy(root)
    if mutation == 'missing-variant':
        broken.remove(broken.findall('testcase')[0]); broken.set('tests', str(len(expected)-1))
    elif mutation == 'duplicate-variant':
        broken.findall('testcase')[0].set('name', broken.findall('testcase')[1].get('name'))
    elif mutation == 'skipped':
        ET.SubElement(broken.findall('testcase')[0], 'skipped')
    else:
        broken.findall('testcase')[0].set('name', 'unrelatedCase')
    try:
        verify(broken, expected)
    except ValueError:
        rejected += 1
    else:
        raise ValueError('Model negative was accepted: ' + mutation)
out = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
       'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
       'xml_member': name, 'xml_sha256': hashlib.sha256(raw).hexdigest(),
       'declared_source_methods': methods, 'configured_sdks': [30, 35],
       'runner_case_suffixes': ['', '[30]'], 'exact_cases': cases,
       'passed': len(cases), 'failed': 0, 'skipped': 0,
       'mutated_negative_controls_rejected': rejected,
       'limits': 'Actual native-rendered JVM model cases only; not installed gestures, rotation, IME or universal usability. Source/APK/CI provenance is separately bound.'}
(a.directory / 'focused-repair-model-verification.json').write_text(json.dumps(out, indent=2) + '\n')
print('Verified 18 source-exact model variants, including both enlarged settings; 4 negatives rejected')
