"""Current source warning contracts; historical catalogue approval mirrors are retired."""
import json
from pathlib import Path
from current_localization_contracts import fixture, CURRENT_CATALOGUE_TAGS
from exact_script_priority_expectations import MEMORY_ADDITIONS as EXACT_SCRIPT_ADDITIONS, require_addition as exact_script_addition
from memory_warning_successors import current_warning_expectation
import translation_catalogues as catalogues
RECORD = Path(__file__).resolve().parents[1] / 'translations/source-review/memory-warnings-20261021.json'
KEYS = {'ui_no_resize_fits_decoder_memory', 'ui_assembly_source_memory_floor'}
PRIORITY_TAGS = frozenset({'bg', 'bn'})
REMAINING_ACCEPTED_ADDITIONS = frozenset({('ang', 'ui_no_resize_fits_decoder_memory'), ('non', 'ui_assembly_source_memory_floor'), ('shn', 'ui_no_resize_fits_decoder_memory')})

def review_record():
    return json.loads(RECORD.read_text(encoding='utf-8'))

def current_source_expectation(key, tag, historical_value):
    # This branch is a current-resource lookup, not an independent wording oracle.
    if tag in CURRENT_CATALOGUE_TAGS and key in KEYS:
        return catalogues.read_strings(catalogues.catalogue_paths()[tag]).get(key, historical_value)
    if key not in KEYS:
        return historical_value
    if (tag,key) in REMAINING_ACCEPTED_ADDITIONS:
        from current_localization_contracts import residual_rows
        row=residual_rows()[(tag,key)]
        old=next(o for o in review_record()['options'] if o['tag']==tag)['terms'][key]['value']
        if historical_value is not None or old is not None or row['previous_target'] is not None or row['source']!=review_record()['keys'][key]['corrected_english']:
            raise ValueError('Exact sparse memory-warning predecessor/source differs')
        return row['target']
    if (tag,key) in EXACT_SCRIPT_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        if old is not None:raise ValueError('Tatar-Latin queue predecessor is not absent')
        return exact_script_addition(tag,key,historical_value,queue['keys'][key]['corrected_english'])['reviewed_value']
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
