"""Current source warning contracts; historical catalogue approval mirrors are retired."""
import json
from pathlib import Path
from current_localization_contracts import fixture, CURRENT_CATALOGUE_TAGS as MIRROR_CATALOGUE_TAGS
from memory_warning_successors import current_warning_expectation
import translation_catalogues as catalogues
RECORD = Path(__file__).resolve().parents[1] / 'translations/source-review/memory-warnings-20261021.json'
KEYS = {'ui_no_resize_fits_decoder_memory', 'ui_assembly_source_memory_floor'}
PRIORITY_TAGS = frozenset({'bg', 'bn'})
# Sparse residual packets are historical too; this is lookup scope, not an approval oracle.
CURRENT_CATALOGUE_TAGS = MIRROR_CATALOGUE_TAGS | {'ang', 'non', 'shn'}

def review_record():
    return json.loads(RECORD.read_text(encoding='utf-8'))

def current_source_expectation(key, tag, historical_value):
    # This branch is a current-resource lookup, not an independent wording oracle.
    if tag in CURRENT_CATALOGUE_TAGS and key in KEYS:
        return catalogues.read_strings(catalogues.catalogue_paths()[tag]).get(key, historical_value)
    if key not in KEYS:
        return historical_value
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
