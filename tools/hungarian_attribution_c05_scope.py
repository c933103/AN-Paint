"""Exact C05 successor reversal; historical source hashes stay authoritative."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = 'Paintroid/src/main/res/values-hu/strings.xml'
FIXTURE = ROOT / 'tools/fixtures/hungarian_attribution_c05_scope.json'
FIXTURE_SHA256 = '2dc109760b76f0c6b32c56a14d2bcb95c7cafa3b897b74dc514b43e51ac02ee8'
HELP_BEFORE = '7e3b7c773ed71d7aba0c169cda439b307b65398eda49ea7da6241be6b3c45f76'
HELP_AFTER = '7497f8acf98165ce939d1e7be21806431db43ca8bd5c8416416532c85b82b688'
OLD_ABOUT = 'Névjegy, licencek és jóváírások'
NEW_ABOUT = 'Névjegy, licencek és forrásmegjelölések'


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def scope():
    data = FIXTURE.read_bytes()
    if hashlib.sha256(data).hexdigest() != FIXTURE_SHA256:
        raise AssertionError('The pinned 17-entry C05 scope fixture changed')
    return json.loads(data)


def before_c05(path, text):
    """Undo exactly 17 approved Hungarian lines, never unrelated source edits."""
    if path != PATH:
        return text
    for row in scope()['entries']:
        if text.count(row['after']) != 1 or text.count(row['before']) != 0:
            raise AssertionError(f"{row['id']}: expected exactly one C05 replacement")
        text = text.replace(row['after'], row['before'], 1)
    return text


def historical_c03_help(tag, actual, row):
    """C05-HU-15 -> unchanged C03 -> unchanged pre-C03, with no hash waiver."""
    if tag != 'hu':
        return actual
    scope()  # Pin every permitted C05 source substitution independently.
    manifest = ROOT / 'verification/help-commons-provider-2026-10-09/translations.json'
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != '8bd7faf4ec72843827d0bc5e4effd95bc72a782a69f5f8f4323cc4c8cec3f74a':
        raise AssertionError('Historical C03 manifest changed')
    if row['after_help_sha256'] != HELP_BEFORE or digest(actual) != HELP_AFTER:
        raise AssertionError('C05 Help successor endpoint changed')
    if actual.count(NEW_ABOUT) != 1 or OLD_ABOUT in actual:
        raise AssertionError('Expected one exact C05 About reference')
    previous = actual.replace(NEW_ABOUT, OLD_ABOUT, 1)
    if digest(previous) != HELP_BEFORE:
        raise AssertionError('C05 reversal did not recover the historical C03 Help')
    return previous
