"""One finite forward expectation update for the reviewed UK/LT/RO priority cohort.

Historical fixtures stay byte-for-byte. Only exact previous values/attributes
may advance to the explicit accepted current value; no source reconstruction,
recursive history, unspecified locale, or blanket preservation bypass is used.
"""
from copy import deepcopy
from functools import lru_cache
from current_localization_contracts import fixture

CURRENT = 'ukrainian_lithuanian_romanian_priority_wording.json'
REPLACEMENTS = {
    'uk': frozenset(['save20_dither', 'save20_file_format', 'ui_category_selection', 'ui_crop_image', 'ui_crop_to_selection', 'ui_fit_entire_canvas_in_view', 'ui_free_form_select', 'ui_keep_editing23', 'ui_menu_image', 'ui_percent', 'ui_percent_fd8671', 'ui_pixels', 'ui_pixels_6ec9c2', 'ui_ready', 'ui_rectangle_select', 'ui_select_all', 'ui_solid_fill']),
    'lt': frozenset(['formats22_animation_message', 'formats22_animation_unknown', 'gallery_credit_could_not_save', 'gallery_credit_too_large', 'language20_translation_note', 'legacy_credits_unreadable', 'save20_dither', 'save20_gif_description', 'ui_collapse_tool_category', 'ui_colour_palette_tap_for_foreground_hold_for_background', 'ui_colour_tap_foreground_hold_background', 'ui_d_d_pixels_2f_mp_exceeds_the_current', 'ui_d_d_px_d_pixels_2f_mp', 'ui_enter_valid_dimensions', 'ui_expand_tool_category', 'ui_height_in', 'ui_none', 'ui_percent_fd8671', 'ui_pixels_6ec9c2', 'ui_trim_in_percent', 'ui_trim_in_pixels', 'ui_width_in']),
    'ro': frozenset(['formats22_animation_message', 'save20_file_format', 'ui_autosave_is_paused_to_protect_that_draft_use', 'ui_cut', 'ui_done', 'ui_fit_entire_canvas_in_view', 'ui_keep_editing23', 'ui_line', 'ui_new_image', 'ui_outline', 'ui_paste', 'ui_percent_fd8671', 'ui_pixels_6ec9c2', 'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_solid_fill', 'ui_watercolor']),
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
    data = deepcopy(fixture(name))
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
    return {key for key,row in data['values'].items() if row['previous_target'] is None} if data else set()


def catalogue_count(tag, previous_count):
    return previous_count + len(added_keys(tag))


def current_display(tag,key):
    data = cohort()[tag]
    return (data['values'].get(key) or data['context'][key])['display']
