#!/usr/bin/env python3
"""Validate saved historical evidence, without executing Android or app code."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'savedFirstCreditSurvivesRecreationAndCancellationOfAnEmptySecondDraft',
    'cancelledRecreatedGalleryDraftKeepsTheOriginalDocumentAndCredits',
    'confirmedRecreatedGalleryDraftReturnsToTheCoveredRecreatedEditor',
}


def main():
    hashes = json.loads((ROOT / 'files.sha256.json').read_text())
    actual = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in ROOT.rglob('*') if p.is_file() and p.name != 'files.sha256.json'
              and '__pycache__' not in p.parts}
    assert actual == hashes, 'Retained evidence file inventory or hashes differ'
    provenance = json.loads((ROOT / 'provenance.json').read_text())
    assert provenance['new_android_execution'] is False
    assert provenance['historical_equal_tree'] == 'e5f9a122ceaad54d1d73ef752d627cbc0b39ceae'
    assert all(x['downloaded_sha256_matches'] for x in provenance['artifacts'])
    summary = json.loads((ROOT / 'historical/gallery-summary.json').read_text())
    assert summary['success'] and summary['expected_tests'] == summary['completed_tests'] == 3
    assert not any(summary[key] for key in ('missing', 'unexpected', 'errors'))
    assert {x['name'] for x in summary['cases']} == EXPECTED
    assert all(x['status'] == 'passed' for x in summary['cases'])
    suite = ET.parse(ROOT / 'historical/gallery-junit.xml').getroot()
    assert suite.get('tests') == '3'
    assert all(suite.get(key) == '0' for key in ('failures', 'errors', 'skipped'))
    assert {x.get('name') for x in suite.findall('testcase')} == EXPECTED
    composition = ET.parse(ROOT / 'historical/composition-junit.xml').getroot()
    assert composition.get('tests') == '3'
    assert all(composition.get(key) == '0' for key in ('failures', 'errors', 'skipped'))
    aggregate = json.loads((ROOT / 'historical/derived-aggregate.json').read_text())
    assert aggregate['jvm_total'] == {'tests': 329, 'failures': 0, 'errors': 0, 'skipped': 0}
    assert aggregate['installed_total'] == 91
    assert aggregate['lint_issue_count'] == 0
    trace = (ROOT / 'historical/gallery-logcat-excerpt.txt').read_text()
    assert set(re.findall(r'task=(\d+)', trace)) == {'34', '36', '38'}
    assert all('GalleryDraftDeviceTest' in line for line in trace.splitlines())
    assert sum('I GalleryDraftDeviceTest:' in line for line in trace.splitlines()) == 153
    print('Historical evidence hashes, three gallery cases, aggregate counts and lifecycle excerpt verified.')


if __name__ == '__main__':
    main()
