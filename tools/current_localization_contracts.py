"""Current resource contracts. Historical source formatting is intentionally irrelevant."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

FIXTURES = Path(__file__).resolve().parent / 'fixtures/current_localization'


def _parse_fixture(text):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result: raise ValueError('Duplicate fixture key: '+key)
            result[key]=value
        return result
    return json.loads(text,object_pairs_hook=unique)


def fixture(name):
    return _parse_fixture((FIXTURES / name).read_text())


def require_string(xml, key, expected, constraints=None):
    """Validate one complete Android string, rejecting missing/duplicate definitions."""
    return require_string_root(ET.fromstring(xml), key, expected, constraints)


def require_string_root(root, key, expected, constraints=None):
    """Validate an already parsed resource root without mutating it."""
    constraints = constraints or {}
    nodes = root.findall(f"./string[@name='{key}']")
    if len(nodes) != 1:
        raise ValueError(f'{key}: expected exactly one definition, found {len(nodes)}')
    node = nodes[0]
    value = ''.join(node.itertext())
    if value != expected:
        raise ValueError(f'{key}: wording differs')
    if len(node) != constraints.get('child_elements', 0):
        raise ValueError(f'{key}: unexpected child markup')
    if 'attributes' in constraints and node.attrib != constraints['attributes']:
        raise ValueError(f'{key}: attributes differ')
    if catalogues.placeholders(value) != constraints.get('placeholders', catalogues.placeholders(expected)):
        raise ValueError(f'{key}: format arguments differ')
    formatted = constraints.get('formatted', node.get('formatted') != 'false')
    if 'formatted' in constraints and (node.get('formatted') != 'false') != formatted:
        raise ValueError(f'{key}: formatted attribute differs')
    errors = catalogues.android_string_errors(value) + catalogues.format_string_errors(value, formatted)
    if errors:
        raise ValueError(f'{key}: {errors}')
    for literal in constraints.get('required_literals', []):
        if literal not in value:
            raise ValueError(f'{key}: missing literal {literal}')
    for literal, count in constraints.get('legal_identifier_counts', {}).items():
        if value.count(literal) != count:
            raise ValueError(f'{key}: legal identifier count differs')
    if 'escaped_newline_count' in constraints and value.count('\\n') != constraints['escaped_newline_count']:
        raise ValueError(f'{key}: escaped newlines differ')
    if any(part in value.casefold() for part in constraints.get('forbidden_casefold_substrings', [])):
        raise ValueError(f'{key}: forbidden wording')
    return value


def decode_display(raw):
    """Decode canonical Android source for host semantic checks; compiled checks remain required."""
    if not isinstance(raw, str):
        raise ValueError('Non-string display input')
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    else:
        raw = re.sub(r'[ \t\r\n]+', ' ', raw).strip(' \t\r\n')
    return re.sub(r'\\(.)', lambda m: {'n': '\n', 't': '\t', 'r': '\r'}.get(m[1], m[1]), raw)


def current_display(tag, key):
    """Read current canonical text for semantic assertions, not an expected-value oracle."""
    import translation_catalogues as catalogues
    path = catalogues.RES / 'values/strings.xml' if tag == 'default' else catalogues.catalogue_paths()[tag]
    strings = catalogues.read_strings(path)
    seen = set()
    while True:
        if key in seen or key not in strings:
            raise ValueError('Missing or cyclic current resource reference: ' + key)
        seen.add(key)
        value = strings[key]
        if not value.startswith('@string/'):
            return decode_display(value)
        key = value[len('@string/'):]
