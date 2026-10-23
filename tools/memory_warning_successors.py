"""Strict, offline current-warning bindings; historical evidence stays immutable.

Expected wording is read only from pinned public project-evidence exports, never from
production resource output. Integrity checks use explicit exceptions under -O.
"""
import csv
from functools import lru_cache
from hashlib import sha256
import io
import json
from pathlib import Path
from types import MappingProxyType

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'translations/source-review/memory-warning-successors-20261023.json'
QUEUE = ROOT / 'translations/source-review/memory-warnings-20261021.json'
EVIDENCE = ROOT / 'verification/translations/memory-warning-successors-20261023'
INDEX_HASH = 'e10cddce134f8798f00c60f774997c93229c585a4e7a2a4befcbaefc8cb5cdff'
EXPORT_HASH = 'dbea2dcc17014c455f347035c3117beaa3217a3b61704c95d393196b172dbde0'
QUEUE_HASH = '7c27a21663dd970382ee481c09b79ea5db7a036299a6c9d32cabd3f8b6e8f12a'
KEYS = frozenset(('ui_no_resize_fits_decoder_memory', 'ui_assembly_source_memory_floor'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    require(isinstance(value, str), 'Expected text')
    return sha256(value.encode('utf-8')).hexdigest()


def validated_successors(data):
    """Validate metadata against pinned public exports and original receipt identities."""
    raw = QUEUE.read_bytes()
    require(sha256(raw).hexdigest() == QUEUE_HASH, 'Historical queue changed')
    queue = json.loads(raw)
    frozen = {(o['tag'], k): (o['catalogue'], term['value'])
              for o in queue['options'] for k, term in o['terms'].items()}
    raw = (EVIDENCE / 'accepted-value-receipts.tsv').read_bytes()
    require(sha256(raw).hexdigest() == INDEX_HASH, 'Independent receipt index changed')
    index_rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter='\t'))
    index = {(r['tag'], r['key']): r for r in index_rows}
    require(len(index_rows) == len(index) == 114, 'Receipt index inventory differs')
    require(data.get('schema') == 1 and isinstance(data.get('rows'), list), 'Bad successor schema')
    require(len(data['rows']) == 114, 'Successor inventory differs')
    export_raw = (EVIDENCE / 'receipt-exports.json').read_bytes()
    require(sha256(export_raw).hexdigest() == EXPORT_HASH, 'Project evidence export changed')
    export = json.loads(export_raw)
    require(export.get('schema') == 'public-project-exact-warning-receipts-v1', 'Bad export schema')
    require(export.get('original_index_sha256') == INDEX_HASH, 'Export index identity differs')
    evidence_rows = export.get('rows', [])
    evidence = {(r['tag'], r['key']): r for r in evidence_rows}
    require(len(evidence_rows) == len(evidence) == 114 and set(evidence) == set(index), 'Export inventory differs')
    result = {}
    for row in data['rows']:
        require(isinstance(row, dict), 'Invalid successor row')
        identity = (row.get('tag'), row.get('key'))
        require(identity in index and identity not in result, 'Unknown, held or duplicate successor identity')
        bound = index[identity]
        require(row.get('catalogue') == frozen[identity][0], 'Catalogue binding differs')
        require(row.get('historical_value') == frozen[identity][1], 'Historical target differs')
        require(digest(row['historical_value']) == row.get('historical_sha256') == bound['old_value_sha256'], 'Historical target hash differs')
        source = queue['keys'][row['key']]['corrected_english']
        require(row.get('source') == source, 'Corrected source differs')
        require(digest(source) == row.get('source_sha256') == bound['source_sha256'], 'Source hash differs')
        receipt = row.get('receipt')
        require(isinstance(receipt, dict), 'Missing receipt binding')
        require(receipt.get('path') == bound['final_receipt'] and receipt.get('selector') == bound['receipt_selector']
                and receipt.get('sha256') == bound['receipt_sha256'], 'Receipt identity differs')
        selected = evidence[identity]
        require(selected.get('original_receipt') == receipt, 'Export original receipt identity differs')
        require(selected.get('decision') == 'accept', 'Export does not accept candidate')
        require(selected.get('source') == source and selected.get('source_sha256') == row['source_sha256'], 'Export source differs')
        require(selected.get('historical_value') == row['historical_value'] and selected.get('historical_sha256') == row['historical_sha256'], 'Export old value differs')
        value = selected.get('value')
        require(value == row.get('value') and digest(value) == row.get('value_sha256') == selected.get('value_sha256') == bound['accepted_value_sha256'], 'Independent accepted value differs')
        result[identity] = (row['historical_value'], value, source, row['catalogue'])
    require(set(result) == set(index), 'Successor identity coverage differs')
    return MappingProxyType(result)


@lru_cache(maxsize=1)
def successors():
    return validated_successors(json.loads(RECORD.read_text(encoding='utf-8')))


def current_warning_expectation(key, tag, historical_value):
    """Bounded substitution; never treat unknown or held text as accepted."""
    if key not in KEYS:
        return historical_value
    raw = QUEUE.read_bytes()
    require(sha256(raw).hexdigest() == QUEUE_HASH, 'Historical queue changed')
    frozen = {(o['tag'], k): term['value'] for o in json.loads(raw)['options'] for k, term in o['terms'].items()}
    require((tag, key) in frozen, 'Unknown historical tag/key')
    require(historical_value == frozen[(tag, key)], 'Historical target binding differs')
    binding = successors().get((tag, key))
    if binding is None:
        return historical_value
    require(historical_value == binding[0], 'Historical target binding differs: ' + tag + '/' + key)
    return binding[1]


def accepted_warning(key, tag):
    """Return one explicitly accepted constant; fail for held/unmapped keys."""
    binding = successors().get((tag, key))
    require(binding is not None, 'No accepted successor: ' + tag + '/' + key)
    return binding[1]
