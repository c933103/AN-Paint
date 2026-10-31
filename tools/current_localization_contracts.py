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


def require_wording_shape(data, expected_keys, expected_tags):
    if data.get('schema_version') != 1 or set(data.get('values',{})) != set(expected_keys):
        raise ValueError('Current message family/key inventory differs')
    if set(data.get('constraints',{})) != set(expected_keys):
        raise ValueError('Current message constraints are incomplete')
    for key,values in data['values'].items():
        if set(values) != set(expected_tags) or not all(isinstance(v,str) and v for v in values.values()):
            raise ValueError('Current message locale inventory is empty or differs: '+key)
    return data


def require_locale_scope(data, expected_scoped_tags, offered_tags):
    """Require the explicit, disjoint current scope; absence never implies review."""
    if data.get('schema_version') != 1 or data.get('default_tag') != 'default':
        raise ValueError('Current locale scope schema differs')
    groups = []
    for field in ('scoped_tags', 'fallback_tags'):
        tags = data.get(field)
        if (not isinstance(tags, list) or not tags or
                not all(isinstance(tag, str) and tag for tag in tags) or
                len(tags) != len(set(tags))):
            raise ValueError('Missing, empty or duplicate locale scope: '+field)
        groups.append(set(tags))
    scoped, fallback = groups
    if scoped != set(expected_scoped_tags) or scoped & fallback:
        raise ValueError('Reviewed scope differs or overlaps fallback scope')
    if len(offered_tags) != len(set(offered_tags)) or scoped | fallback != set(offered_tags):
        raise ValueError('Explicit locale scope does not match current picker')
    return scoped, fallback


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


# Current XML owns these catalogues; immutable review history is not a text freeze.
CURRENT_CATALOGUE_TAGS = frozenset(['tt-Latn', 'ain-Latn', 'mn-Mong', 'yue-Latn', 'hak-Latn-TW', 'nan-Latn-TW', 'ary', 'as', 'ast', 'az', 'be', 'bo', 'br', 'bs', 'ca', 'ca-ES-valencia', 'ceb', 'ckb', 'csb', 'cy', 'da', 'de', 'dz', 'el', 'en-AU', 'es-ES', 'eu-ES', 'fa', 'fa-IR', 'fil', 'fr', 'fy', 'ga', 'gd', 'gl', 'gu', 'ha', 'he', 'hi', 'hne', 'hr', 'ht', 'hy', 'ia', 'ig', 'is', 'it', 'ja', 'jv', 'ka', 'kab', 'kk', 'km', 'kn', 'ko-KP', 'ku', 'ky', 'la', 'ln', 'lo', 'lt', 'mai', 'mi', 'mk', 'ml-IN', 'mn-Cyrl-MN', 'mr', 'mww', 'my', 'nds', 'ne', 'nl', 'nn', 'no', 'oc', 'pa-IN', 'pcm', 'ps', 'pt-PT', 'ro', 'rw', 'sa', 'sd', 'se', 'si', 'sk', 'sl', 'sm', 'so', 'sq', 'sr-Cyrl', 'sr-Latn', 'su', 'ta', 'te', 'tg', 'th', 'tok', 'tpi', 'tr', 'tt-Cyrl', 'ug', 'uk', 'ur', 'uz-Latn', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh-HK', 'zu'])


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
