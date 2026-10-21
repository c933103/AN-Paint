"""Current English expectations and the pending two-term review queue.

Historical paired-language fixtures stay unchanged. Only their default-English
expectation is superseded here; no translation is accepted by this substitution.
"""
import json
from pathlib import Path

RECORD = Path(__file__).resolve().parents[1] / 'translations/source-review/memory-warnings-20261021.json'
KEYS = {'ui_no_resize_fits_decoder_memory', 'ui_assembly_source_memory_floor'}


def review_record():
    return json.loads(RECORD.read_text(encoding='utf-8'))


def current_source_expectation(key, tag, historical_value):
    """Keep historical translation evidence; assert the corrected English only.

Reject a changed historical English pair instead of letting the correction hide
fixture corruption. This is an explicit two-key successor, not a catalogue
generator, review result or reconstruction of an old source snapshot.
"""
    if tag != 'default' or key not in KEYS:
        return historical_value
    correction = review_record()['keys'][key]
    if historical_value != correction['old_english']:
        raise ValueError('Historical English binding differs: ' + key)
    return correction['corrected_english']
