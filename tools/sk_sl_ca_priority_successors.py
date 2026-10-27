"""One finite forward expectation update for the reviewed SK/SL/CA priority cohort.

Historical fixtures stay byte-for-byte. Only exact previous values/attributes
may advance to the explicit accepted current value; no source reconstruction,
recursive history, unspecified locale, or blanket preservation bypass is used.
"""
from copy import deepcopy
from functools import lru_cache
from current_localization_contracts import fixture
import priority_wording_successors as earlier

CURRENT = 'slovak_slovenian_catalan_priority_wording.json'
REPLACEMENTS = {
    'sk': frozenset(['save20_file_format', 'ui_autosave_is_paused_to_protect_that_draft_use', 'ui_done', 'ui_fit', 'ui_fit_entire_canvas_in_view', 'ui_keep_editing23', 'ui_left', 'ui_outline', 'ui_pixels', 'ui_pixels_6ec9c2', 'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_right', 'ui_save_your_changes', 'ui_solid_fill', 'ui_watercolor']),
    'sl': frozenset(['save20_file_format', 'ui_autosave_is_paused_to_protect_that_draft_use', 'ui_bottom', 'ui_fit', 'ui_fit_entire_canvas_in_view', 'ui_keep_editing23', 'ui_outline', 'ui_percent', 'ui_percent_fd8671', 'ui_pixels', 'ui_pixels_6ec9c2', 'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_top', 'ui_watercolor']),
    'ca': frozenset(['save20_file_format', 'ui_autosave_is_paused_to_protect_that_draft_use', 'ui_done', 'ui_fit', 'ui_fit_entire_canvas_in_view', 'ui_keep_editing23', 'ui_outline', 'ui_preview', 'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_save_your_changes', 'ui_solid_fill', 'ui_watercolor']),
}

@lru_cache(maxsize=1)
def cohort():
    data = fixture(CURRENT)['locales']
    if set(data) != set(REPLACEMENTS):
        raise ValueError('Explicit successor locale scope differs')
    for tag, rows in data.items():
        actual = {key for key,row in rows['values'].items() if row['previous_target'] is not None}
        if actual != REPLACEMENTS[tag]:
            raise ValueError('Explicit replacement scope differs: '+tag)
    return data


def current_value(tag, key, previous, attributes=None):
    data = cohort().get(tag)
    row = data['values'].get(key) if data else None
    if row is None or row['previous_target'] is None:
        return previous
    if previous != row['previous_target']:
        raise ValueError(tag+'/'+key+': previous accepted value does not match successor binding')
    if attributes is not None and attributes != row['previous_attributes']:
        raise ValueError(tag+'/'+key+': previous attributes do not match successor binding')
    return row['target']


def current_fixture(name):
    """Project only keys already in a bounded family; never expand its review scope."""
    data = earlier.current_fixture(name)
    # Disjoint cohorts: the earlier exact forward bindings remain untouched.
    for key, values in data.get('values', {}).items():
        for tag, value in values.items():
            row = cohort().get(tag, {}).get('values', {}).get(key)
            if row and row['previous_target'] is not None and values.get('default') != row['source']:
                raise ValueError(tag+'/'+key+': previous English source differs')
            values[tag] = current_value(tag,key,value,data.get('constraints',{}).get(key,{}).get(tag,{}).get('attributes'))
    for tag, values in data.get('preserved_values', {}).items():
        for key, row in values.items():
            row['value'] = current_value(tag,key,row['value'],row['attributes'])
    return data


def added_keys(tag):
    data = cohort().get(tag)
    return ({key for key,row in data['values'].items() if row['previous_target'] is None} if data else set()) | earlier.added_keys(tag)


def catalogue_count(tag, previous_count):
    return previous_count + len(added_keys(tag))


def current_display(tag,key):
    if tag not in cohort():
        return earlier.current_display(tag,key)
    data = cohort()[tag]
    return (data['values'].get(key) or data['context'][key])['display']
