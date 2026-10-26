"""Current English expectations and the pending two-term review queue.

Historical paired-language fixtures stay unchanged. Default-English and explicitly receipt-bound current successors are selected here;
no historical fixture or receipt is rewritten.
"""
import json
from memory_warning_successors import current_warning_expectation
from pathlib import Path

RECORD = Path(__file__).resolve().parents[1] / 'translations/source-review/memory-warnings-20261021.json'
KEYS = {'ui_no_resize_fits_decoder_memory', 'ui_assembly_source_memory_floor'}


def review_record():
    return json.loads(RECORD.read_text(encoding='utf-8'))


def current_source_expectation(key, tag, historical_value):
    """Keep historical evidence; select only explicitly bound current expectations.

Reject a changed historical English pair instead of letting the correction hide
fixture corruption. This is an explicit two-key successor, not a catalogue
generator, review result or reconstruction of an old source snapshot.
"""
    if key not in KEYS:
        return historical_value
    if tag != 'default':
        return current_warning_expectation(key, tag, historical_value)
    correction = review_record()['keys'][key]
    if historical_value != correction['old_english']:
        raise ValueError('Historical English binding differs: ' + key)
    return correction['corrected_english']
