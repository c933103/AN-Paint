"""Current English expectations and the pending two-term review queue.

Historical paired-language fixtures stay unchanged. Default-English and explicitly receipt-bound current successors are selected here;
no historical fixture or receipt is rewritten.
"""
import json
from current_localization_contracts import fixture
from memory_warning_successors import current_warning_expectation
from pathlib import Path

RECORD = Path(__file__).resolve().parents[1] / 'translations/source-review/memory-warnings-20261021.json'
KEYS = {'ui_no_resize_fits_decoder_memory', 'ui_assembly_source_memory_floor'}
PRIORITY_TAGS = frozenset({'bg', 'bn'})
PRIORITY_ADDITIONS = frozenset({('uk','ui_assembly_source_memory_floor'),
    ('uk','ui_no_resize_fits_decoder_memory'),('ro','ui_no_resize_fits_decoder_memory')})
SK_SL_CA_ADDITIONS = frozenset((tag, 'ui_no_resize_fits_decoder_memory') for tag in ('sk','sl','ca'))
SINGLE_KEY_FIXTURES = {
    'nn': 'nynorsk_p0_remaining_wording.json',
    'da': 'danish_norwegian_p0_wording.json',
    'no': 'danish_norwegian_p0_wording.json',
    'ca': 'catalan_romanian_completion_wording.json',
    'ro': 'catalan_romanian_completion_wording.json',
    'sk': 'slovak_slovenian_p0_wording.json',
    'sl': 'slovak_slovenian_p0_wording.json',
    'sr-Cyrl': 'serbian_p0_wording.json',
    'sr-Latn': 'serbian_p0_wording.json',
    'hr': 'croatian_bosnian_p0_wording.json',
    'bs': 'croatian_bosnian_p0_wording.json',
}
SINGLE_KEY_EXPECTATIONS = frozenset(
    (tag, 'ui_assembly_source_memory_floor') for tag in SINGLE_KEY_FIXTURES)


def review_record():
    return json.loads(RECORD.read_text(encoding='utf-8'))


def current_source_expectation(key, tag, historical_value):
    """Keep historical evidence; select only explicitly bound current expectations.

Reject a changed historical English pair instead of letting the correction hide
fixture corruption. This selects explicitly bound paired and single-key
expectations, not a catalogue generator, review result or reconstruction of an
old source snapshot.
"""
    if key not in KEYS:
        return historical_value
    if (tag, key) in SK_SL_CA_ADDITIONS:
        queue = review_record()
        old = next(o for o in queue['options'] if o['tag'] == tag)['terms'][key]['value']
        row = fixture('slovak_slovenian_catalan_priority_wording.json')['locales'][tag]['values'][key]
        if historical_value is not None or old is not None or row['previous_target'] is not None:
            raise ValueError('Historical priority addition must be absent: '+tag+'/'+key)
        if row['source'] != queue['keys'][key]['corrected_english'] or row['attributes'] != {'name':key}:
            raise ValueError('Priority addition source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag, key) in PRIORITY_ADDITIONS:
        queue = review_record()
        old = next(o for o in queue['options'] if o['tag'] == tag)['terms'][key]['value']
        row = fixture('ukrainian_lithuanian_romanian_priority_wording.json')['locales'][tag]['values'][key]
        if historical_value is not None or old is not None or row['previous_target'] is not None:
            raise ValueError('Historical priority addition must be absent: '+tag+'/'+key)
        if row['source'] != queue['keys'][key]['corrected_english'] or row['attributes'] != {'name':key}:
            raise ValueError('Priority addition source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag, key) in SINGLE_KEY_EXPECTATIONS:
        # Explicit P0-only reviews. The paired oracle and missing P1
        # companion retain their separate scope and frozen historical absence.
        queue = review_record()
        old = next(o for o in queue['options'] if o['tag'] == tag)['terms'][key]['value']
        if historical_value is not None or old is not None:
            raise ValueError('Historical single-key warning was absent: ' + tag + '/' + key)
        data = fixture(SINGLE_KEY_FIXTURES[tag])
        if data['values'][key]['default'] != queue['keys'][key]['corrected_english']:
            raise ValueError('Single-key warning source differs: ' + key)
        return data['values'][key][tag]
    if tag in PRIORITY_TAGS:
        # These four newly translated values have qualified priority review,
        # not entries in the separately accepted-warning inventory. Keep the
        # initial queue's absence intact and reject a forged historical pair.
        if historical_value is not None:
            raise ValueError('Historical priority warning was absent: ' + tag + '/' + key)
        data = fixture('bulgarian_bengali_priority_wording.json')
        if data['values'][key]['default'] != review_record()['keys'][key]['corrected_english']:
            raise ValueError('Priority warning source differs: ' + key)
        return data['values'][key][tag]
    if tag != 'default':
        return current_warning_expectation(key, tag, historical_value)
    correction = review_record()['keys'][key]
    if historical_value != correction['old_english']:
        raise ValueError('Historical English binding differs: ' + key)
    return correction['corrected_english']
