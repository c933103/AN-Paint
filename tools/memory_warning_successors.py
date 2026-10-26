"""Offline exact-current-warning behavior oracle; detailed provenance is external.

Only explicit accepted locale/key constants are substituted. Historical arguments
are checked against the existing frozen queue, never used to reconstruct sources.
"""
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'translations/source-review/memory-warning-successors-20261025.json'
QUEUE = ROOT / 'translations/source-review/memory-warnings-20261021.json'
# This seals only the compact behavioral fixture, never production source files.
ORACLE_HASH = 'd7a40b123878ae60788c900d98343eb96b862b718700fd0acd481150ad7bacf7'
SOURCES = {'ui_no_resize_fits_decoder_memory': 'Even at the smallest output size, this image cannot be loaded for editing within the current memory limits. Cancel and use a smaller source image.', 'ui_assembly_source_memory_floor': 'This assembly is estimated to exceed the current working-memory budget, even at the smallest output size. Reducing the assembly dimensions alone is not enough under the current limits. Close other documents or prepare a smaller source image before trying again. Your assembly is unchanged.'}
KEYS = frozenset(SOURCES)
ACCEPTED_TAGS = frozenset(('af', 'ain-Kana', 'ain-Latn', 'ar', 'bo', 'ceb', 'cs', 'de', 'dz', 'el', 'en-AU', 'en-CA', 'en-GB', 'en-IN', 'en-SG', 'en-US', 'en-XV', 'eo', 'es-419', 'es-ES', 'et', 'fi', 'fil', 'fr', 'hak-Hant-TW', 'hak-Latn-TW', 'hu', 'id', 'it', 'ja', 'ko-Kore-KR', 'ko-KP', 'ko-KR', 'lt', 'lv', 'lzh-Hant', 'mn-Cyrl-MN', 'mn-Mong', 'mnc-Mong', 'ms', 'nan-Hant-TW', 'nan-Latn-TW', 'nl', 'pl', 'pt-BR', 'pt-PT', 'qaa-Zsye-XV', 'ru', 'ryu', 'sv', 'sw', 'tr', 'vi', 'wuu-Hans', 'yue-Hant', 'yue-Latn', 'zh-CN', 'zh-HK', 'zh-TW'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_oracle():
    raw = RECORD.read_bytes()
    require(sha256(raw).hexdigest() == ORACLE_HASH, 'Behavior oracle changed')
    return json.loads(raw)


def validated_successors(data):
    """Bind explicit expected literals to known source, locale and historical key."""
    oracle = read_oracle()
    require(isinstance(data, dict) and data.get('schema') == 2, 'Bad oracle schema')
    require(data.get('sources') == SOURCES, 'Corrected source differs')
    values = data.get('values')
    require(isinstance(values, dict) and set(values) == ACCEPTED_TAGS, 'Accepted locale inventory differs')
    queue = json.loads(QUEUE.read_text(encoding='utf-8'))
    for key, source in SOURCES.items():
        require(queue['keys'][key]['corrected_english'] == source, 'Historical source binding differs')
    options = {o['tag']: o for o in queue['options']}
    result = {}
    for tag, terms in values.items():
        require(isinstance(terms, dict) and set(terms) == KEYS, 'Accepted key inventory differs')
        for key, expected in terms.items():
            require(isinstance(expected, str) and expected == oracle['values'][tag][key], 'Expected warning differs')
            old = options[tag]['terms'][key]['value']
            require(isinstance(old, str) and old != expected, 'Historical target binding differs')
            result[(tag, key)] = (old, expected, SOURCES[key], options[tag]['catalogue'])
    require(len(result) == 118, 'Accepted inventory differs')
    return MappingProxyType(result)


@lru_cache(maxsize=1)
def successors():
    return validated_successors(read_oracle())


def current_warning_expectation(key, tag, historical_value):
    """Bounded substitution; unknown/held text cannot obtain acceptance."""
    if key not in KEYS:
        return historical_value
    frozen = {(o['tag'], k): term['value']
              for o in json.loads(QUEUE.read_text(encoding='utf-8'))['options']
              for k, term in o['terms'].items()}
    require((tag, key) in frozen, 'Unknown historical tag/key')
    require(historical_value == frozen[(tag, key)], 'Historical target binding differs')
    binding = successors().get((tag, key))
    return historical_value if binding is None else binding[1]


def accepted_warning(key, tag):
    """Return one explicitly accepted full literal, never an actual output."""
    binding = successors().get((tag, key))
    require(binding is not None, 'No accepted successor: ' + tag + '/' + key)
    return binding[1]
