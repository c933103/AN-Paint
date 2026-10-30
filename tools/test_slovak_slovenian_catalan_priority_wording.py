"""Current complete-value and composition contracts; no fluency/whole-UI certification."""
from current_localization_contracts import RESIDUAL_KEYS, require_residual_or_previous
from collections import Counter
from copy import deepcopy
import json
import re
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_string_root
from test_danish_norwegian_p0_wording import FULL_FORMAT_TOKEN
import translation_catalogues as catalogues

TAGS = {'sk','sl','ca'}
CHANGED_KEYS = {
    'sk': frozenset('''
        colour_converter_unavailable
        colour_invalid_metadata
        colour_truncated_metadata
        colour_unsupported_icc_model
        commons_svg_original_size_too_large
        commons_svg_original_size_unavailable
        formats22_at_least_frames
        formats22_import_limit
        language20_current
        language20_translation_note
        save20_file_format
        ui_0f_0f_px_1f
        ui_100
        ui_1_px
        ui_1f_s
        ui_actual_size_100
        ui_add_colour26
        ui_add_text
        ui_all
        ui_android_blocked_the_file_picker
        ui_android_could_not_decode_this_image
        ui_android_could_not_find_a_file_picker_enable
        ui_apply_bounds
        ui_apply_crop
        ui_autosave_is_paused_to_protect_that_draft_use
        ui_autosaving_draft
        ui_background_edit_colour
        ui_basic_colours
        ui_canvas_bounds
        ui_canvas_zoom
        ui_canvas_zoom_771f84
        ui_choose_a_smaller_output_copy_the_source_images
        ui_choose_a_smaller_size
        ui_choose_at_least_one_image
        ui_choose_dimensions_no_larger_than_the_original
        ui_choose_location
        ui_codec_resize_memory_floor
        ui_collapse_colour_palette
        ui_collapse_tool_category
        ui_collapse_toolbox
        ui_colour
        ui_colour_palette_tap_for_foreground_hold_for_background
        ui_colour_tap_foreground_hold_background
        ui_commit_selection
        ui_copy_all
        ui_could_not_apply_the_crop
        ui_could_not_complete_the_edit
        ui_could_not_complete_the_operation
        ui_could_not_place_the_image
        ui_could_not_prepare_the_image
        ui_crop
        ui_crop_must_stay_inside_the_canvas
        ui_crop_preview_drag_an_edge_or_corner_drag
        ui_d_d_px_d_pixels_2f_mp
        ui_delete_selection
        ui_done
        ui_draft_pending
        ui_draw_again
        ui_drawing_canvas_pinch_and_move_two_fingers_to
        ui_drawing_settings
        ui_drawing_settings_d900c6
        ui_edit_canvas33
        ui_edit_transform33
        ui_enter_a_number_from_to
        ui_enter_a_positive_size
        ui_enter_a_trim_amount_for_every_edge
        ui_enter_a_whole_number_from_to
        ui_enter_all_four_trim_amounts
        ui_enter_positive_canvas_dimensions_within_android_s_coordinate
        ui_enter_positive_dimensions
        ui_enter_positive_dimensions_no_larger_than_the_original
        ui_enter_positive_dimensions_that_resolve_to_at_least
        ui_enter_positive_image_dimensions
        ui_enter_valid_dimensions
        ui_expand_colour_palette
        ui_expand_tool_category
        ui_expand_toolbox
        ui_fit
        ui_fit_entire_canvas_in_view
        ui_fit_selection34
        ui_font_family
        ui_foreground_edit_colour
        ui_from_device34
        ui_full_text_copied
        ui_height
        ui_height_in
        ui_heights
        ui_hex_rrggbb
        ui_hide_editor_controls
        ui_insert_image_into_canvas
        ui_invalid_colour
        ui_invalid_selection_outline
        ui_invert_colours
        ui_keep_editing23
        ui_left
        ui_left_arrow_collapse
        ui_line_spacing
        ui_load_image
        ui_lock_aspect_ratio
        ui_lock_proportions
        ui_magnification
        ui_navigate
        ui_new_colour
        ui_no_readable_image_data
        ui_no_resize_fits_decoder_memory
        ui_none
        ui_not_enough_memory_to_finish_opening_this_image
        ui_not_enough_memory_to_inspect_this_image
        ui_numeric_slider_value
        ui_original_size34
        ui_other_images34
        ui_outline
        ui_paste_hint34
        ui_pixels
        ui_pixels_6ec9c2
        ui_place_text
        ui_please_try_again
        ui_please_wait_for_the_current_operation
        ui_px
        ui_px_724eb3
        ui_recovery_copy_exported_extract_canvas_png_from_the
        ui_reset_bw23
        ui_reset_crop
        ui_reset_to_black_white
        ui_resize_and_load
        ui_resize_the_copy
        ui_right
        ui_save_your_changes
        ui_scales_the_image_unlock_the_ratio_to_stretch
        ui_select_an_area
        ui_select_an_area_first
        ui_selected_colour23
        ui_selection_dimensions_are_too_large
        ui_share_saved_image
        ui_show_all
        ui_show_controls
        ui_show_editor_controls
        ui_show_magnified_drawing_preview
        ui_size_pixels
        ui_size_px
        ui_solid_fill
        ui_tap_an_image_first
        ui_tap_canvas_to_type
        ui_tap_to_type_a_number
        ui_text_direction23
        ui_the_crop_must_contain_at_least_one_pixel
        ui_the_crop_must_stay_inside_the_image
        ui_the_decoder_and_editing_buffers_need_about_the
        ui_the_full_image_and_working_buffers_exceed_the
        ui_the_picker_returned_no_file_please_choose_the
        ui_the_picker_returned_no_files
        ui_the_selected_provider_did_not_return_any_image
        ui_this_file_is_not_a_supported_image_use
        ui_tolerance
        ui_too_large_for_the_current_budget_reduce_the
        ui_tool_categories
        ui_trim_amounts_must_be_zero_or_greater
        ui_trim_amounts_must_fit_inside_each_image_use
        ui_trim_expand_canvas_by_touch
        ui_trim_in_percent
        ui_trim_in_pixels
        ui_try_a_different_file_or_location
        ui_type_text
        ui_use_1_1024_pixels
        ui_use_50_300
        ui_use_a_positive_target_dimension
        ui_use_colour
        ui_use_rrggbb
        ui_watercolor
        ui_width
        ui_width_in
        ui_working
    '''.split()),
    'sl': frozenset('''
        colour_converter_unavailable
        colour_invalid_metadata
        colour_truncated_metadata
        colour_unsupported_icc_model
        commons_svg_original_size_too_large
        commons_svg_original_size_unavailable
        formats22_at_least_frames
        formats22_import_limit
        language20_current
        language20_translation_note
        save20_file_format
        ui_0f_0f_px_1f
        ui_100
        ui_1_px
        ui_1f_s
        ui_actual_size_100
        ui_add_colour26
        ui_add_text
        ui_all
        ui_android_blocked_the_file_picker
        ui_android_could_not_decode_this_image
        ui_android_could_not_find_a_file_picker_enable
        ui_apply_bounds
        ui_apply_crop
        ui_autosave_is_paused_to_protect_that_draft_use
        ui_autosaving_draft
        ui_background_edit_colour
        ui_basic_colours
        ui_bottom
        ui_canvas_bounds
        ui_canvas_zoom
        ui_canvas_zoom_771f84
        ui_choose_a_smaller_output_copy_the_source_images
        ui_choose_a_smaller_size
        ui_choose_at_least_one_image
        ui_choose_dimensions_no_larger_than_the_original
        ui_choose_location
        ui_codec_resize_memory_floor
        ui_collapse_colour_palette
        ui_collapse_tool_category
        ui_collapse_toolbox
        ui_colour
        ui_colour_palette_tap_for_foreground_hold_for_background
        ui_colour_tap_foreground_hold_background
        ui_commit_selection
        ui_copy_all
        ui_could_not_apply_the_crop
        ui_could_not_complete_the_edit
        ui_could_not_complete_the_operation
        ui_could_not_place_the_image
        ui_could_not_prepare_the_image
        ui_crop
        ui_crop_must_stay_inside_the_canvas
        ui_crop_preview_drag_an_edge_or_corner_drag
        ui_d_d_px_d_pixels_2f_mp
        ui_delete_selection
        ui_draft_pending
        ui_draw_again
        ui_drawing_canvas_pinch_and_move_two_fingers_to
        ui_drawing_settings
        ui_drawing_settings_d900c6
        ui_edit_canvas33
        ui_edit_transform33
        ui_enter_a_number_from_to
        ui_enter_a_positive_size
        ui_enter_a_trim_amount_for_every_edge
        ui_enter_a_whole_number_from_to
        ui_enter_all_four_trim_amounts
        ui_enter_positive_canvas_dimensions_within_android_s_coordinate
        ui_enter_positive_dimensions
        ui_enter_positive_dimensions_no_larger_than_the_original
        ui_enter_positive_dimensions_that_resolve_to_at_least
        ui_enter_positive_image_dimensions
        ui_enter_valid_dimensions
        ui_expand_colour_palette
        ui_expand_tool_category
        ui_expand_toolbox
        ui_fit
        ui_fit_entire_canvas_in_view
        ui_fit_selection34
        ui_font_family
        ui_foreground_edit_colour
        ui_from_device34
        ui_full_text_copied
        ui_height
        ui_height_in
        ui_heights
        ui_hex_rrggbb
        ui_hide_editor_controls
        ui_insert_image_into_canvas
        ui_invalid_colour
        ui_invalid_selection_outline
        ui_invert_colours
        ui_keep_editing23
        ui_left_arrow_collapse
        ui_line_spacing
        ui_load_image
        ui_lock_aspect_ratio
        ui_lock_proportions
        ui_magnification
        ui_navigate
        ui_new_colour
        ui_no_readable_image_data
        ui_no_resize_fits_decoder_memory
        ui_none
        ui_not_enough_memory_to_finish_opening_this_image
        ui_not_enough_memory_to_inspect_this_image
        ui_numeric_slider_value
        ui_original_size34
        ui_other_images34
        ui_outline
        ui_paste_hint34
        ui_percent
        ui_percent_fd8671
        ui_pixels
        ui_pixels_6ec9c2
        ui_place_text
        ui_please_try_again
        ui_please_wait_for_the_current_operation
        ui_px
        ui_px_724eb3
        ui_recovery_copy_exported_extract_canvas_png_from_the
        ui_reset_bw23
        ui_reset_crop
        ui_reset_to_black_white
        ui_resize_and_load
        ui_resize_the_copy
        ui_scales_the_image_unlock_the_ratio_to_stretch
        ui_select_an_area
        ui_select_an_area_first
        ui_selected_colour23
        ui_selection_dimensions_are_too_large
        ui_share_saved_image
        ui_show_all
        ui_show_controls
        ui_show_editor_controls
        ui_show_magnified_drawing_preview
        ui_size_pixels
        ui_size_px
        ui_tap_an_image_first
        ui_tap_canvas_to_type
        ui_tap_to_type_a_number
        ui_text_direction23
        ui_the_crop_must_contain_at_least_one_pixel
        ui_the_crop_must_stay_inside_the_image
        ui_the_decoder_and_editing_buffers_need_about_the
        ui_the_full_image_and_working_buffers_exceed_the
        ui_the_picker_returned_no_file_please_choose_the
        ui_the_picker_returned_no_files
        ui_the_selected_provider_did_not_return_any_image
        ui_this_file_is_not_a_supported_image_use
        ui_tolerance
        ui_too_large_for_the_current_budget_reduce_the
        ui_tool_categories
        ui_top
        ui_trim_amounts_must_be_zero_or_greater
        ui_trim_amounts_must_fit_inside_each_image_use
        ui_trim_expand_canvas_by_touch
        ui_trim_in_percent
        ui_trim_in_pixels
        ui_try_a_different_file_or_location
        ui_type_text
        ui_use_1_1024_pixels
        ui_use_50_300
        ui_use_a_positive_target_dimension
        ui_use_colour
        ui_use_rrggbb
        ui_watercolor
        ui_width
        ui_width_in
        ui_working
    '''.split()),
    'ca': frozenset('''
        colour_converter_unavailable
        colour_invalid_metadata
        colour_truncated_metadata
        colour_unsupported_icc_model
        commons_svg_original_size_too_large
        commons_svg_original_size_unavailable
        formats22_at_least_frames
        formats22_import_limit
        language20_current
        language20_translation_note
        save20_file_format
        ui_0f_0f_px_1f
        ui_100
        ui_1_px
        ui_1f_s
        ui_actual_size_100
        ui_add_colour26
        ui_add_text
        ui_all
        ui_android_blocked_the_file_picker
        ui_android_could_not_decode_this_image
        ui_android_could_not_find_a_file_picker_enable
        ui_apply_bounds
        ui_apply_crop
        ui_autosave_is_paused_to_protect_that_draft_use
        ui_autosaving_draft
        ui_background_edit_colour
        ui_basic_colours
        ui_canvas_bounds
        ui_canvas_zoom
        ui_canvas_zoom_771f84
        ui_choose_a_smaller_output_copy_the_source_images
        ui_choose_a_smaller_size
        ui_choose_at_least_one_image
        ui_choose_dimensions_no_larger_than_the_original
        ui_choose_location
        ui_codec_resize_memory_floor
        ui_collapse_colour_palette
        ui_collapse_tool_category
        ui_collapse_toolbox
        ui_colour
        ui_colour_palette_tap_for_foreground_hold_for_background
        ui_colour_tap_foreground_hold_background
        ui_commit_selection
        ui_copy_all
        ui_could_not_apply_the_crop
        ui_could_not_complete_the_edit
        ui_could_not_complete_the_operation
        ui_could_not_place_the_image
        ui_could_not_prepare_the_image
        ui_crop
        ui_crop_must_stay_inside_the_canvas
        ui_crop_preview_drag_an_edge_or_corner_drag
        ui_d_d_px_d_pixels_2f_mp
        ui_delete_selection
        ui_done
        ui_draft_pending
        ui_draw_again
        ui_drawing_canvas_pinch_and_move_two_fingers_to
        ui_drawing_settings
        ui_drawing_settings_d900c6
        ui_edit_canvas33
        ui_edit_transform33
        ui_enter_a_number_from_to
        ui_enter_a_positive_size
        ui_enter_a_trim_amount_for_every_edge
        ui_enter_a_whole_number_from_to
        ui_enter_all_four_trim_amounts
        ui_enter_positive_canvas_dimensions_within_android_s_coordinate
        ui_enter_positive_dimensions
        ui_enter_positive_dimensions_no_larger_than_the_original
        ui_enter_positive_dimensions_that_resolve_to_at_least
        ui_enter_positive_image_dimensions
        ui_enter_valid_dimensions
        ui_expand_colour_palette
        ui_expand_tool_category
        ui_expand_toolbox
        ui_fit
        ui_fit_entire_canvas_in_view
        ui_fit_selection34
        ui_font_family
        ui_foreground_edit_colour
        ui_from_device34
        ui_full_text_copied
        ui_height
        ui_height_in
        ui_heights
        ui_hex_rrggbb
        ui_hide_editor_controls
        ui_insert_image_into_canvas
        ui_invalid_colour
        ui_invalid_selection_outline
        ui_invert_colours
        ui_keep_editing23
        ui_left_arrow_collapse
        ui_line_spacing
        ui_load_image
        ui_lock_aspect_ratio
        ui_lock_proportions
        ui_magnification
        ui_navigate
        ui_new_colour
        ui_no_readable_image_data
        ui_no_resize_fits_decoder_memory
        ui_none
        ui_not_enough_memory_to_finish_opening_this_image
        ui_not_enough_memory_to_inspect_this_image
        ui_numeric_slider_value
        ui_original_size34
        ui_other_images34
        ui_outline
        ui_paste_hint34
        ui_place_text
        ui_please_try_again
        ui_please_wait_for_the_current_operation
        ui_preview
        ui_px
        ui_px_724eb3
        ui_recovery_copy_exported_extract_canvas_png_from_the
        ui_reset_bw23
        ui_reset_crop
        ui_reset_to_black_white
        ui_resize_and_load
        ui_resize_the_copy
        ui_save_your_changes
        ui_scales_the_image_unlock_the_ratio_to_stretch
        ui_select_an_area
        ui_select_an_area_first
        ui_selected_colour23
        ui_selection_dimensions_are_too_large
        ui_share_saved_image
        ui_show_all
        ui_show_controls
        ui_show_editor_controls
        ui_show_magnified_drawing_preview
        ui_size_pixels
        ui_size_px
        ui_solid_fill
        ui_tap_an_image_first
        ui_tap_canvas_to_type
        ui_tap_to_type_a_number
        ui_text_direction23
        ui_the_crop_must_contain_at_least_one_pixel
        ui_the_crop_must_stay_inside_the_image
        ui_the_decoder_and_editing_buffers_need_about_the
        ui_the_full_image_and_working_buffers_exceed_the
        ui_the_picker_returned_no_file_please_choose_the
        ui_the_picker_returned_no_files
        ui_the_selected_provider_did_not_return_any_image
        ui_this_file_is_not_a_supported_image_use
        ui_tolerance
        ui_too_large_for_the_current_budget_reduce_the
        ui_tool_categories
        ui_trim_amounts_must_be_zero_or_greater
        ui_trim_amounts_must_fit_inside_each_image_use
        ui_trim_expand_canvas_by_touch
        ui_trim_in_percent
        ui_trim_in_pixels
        ui_try_a_different_file_or_location
        ui_type_text
        ui_use_1_1024_pixels
        ui_use_50_300
        ui_use_a_positive_target_dimension
        ui_use_colour
        ui_use_rrggbb
        ui_watercolor
        ui_width
        ui_width_in
        ui_working
    '''.split()),
}

P0_HOLDS = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg',
            'ui_save_as_jpeg_xl', 'ui_save_as_png'}
PALETTE_HOLD = 'ui_foreground_background_colour_palette'


def require_current_shape(data):
    if data.get('schema_version') != 1 or set(data.get('locales',{})) != TAGS:
        raise ValueError('Current cohort locale/schema differs')
    for tag,expected in CHANGED_KEYS.items():
        values=data['locales'][tag].get('values',{})
        if set(values) != expected:
            raise ValueError('Current changed-key scope differs: '+tag)
        for key,row in values.items():
            if not isinstance(row,dict) or not all(isinstance(row.get(field),str) and row[field] for field in ('source','target','display','tier','scope')):
                raise ValueError('Incomplete current value: '+tag+'/'+key)
        manifest=json.loads((catalogues.DATA/'string-importance.json').read_text())
        identities={k for t in manifest['tiers'] if t['id'] in ('P0','P1') for k in t['keys']}
        if set(data['locales'][tag].get('priority_status',{}))!=identities:
            raise ValueError('Priority identity inventory differs: '+tag)
        holds=P0_HOLDS|{PALETTE_HOLD,'ui_pinch_and_pan_mode'}
        if set(data['locales'][tag].get('held_absent',[]))!=holds:
            raise ValueError('Hold inventory differs: '+tag)
        statuses=data['locales'][tag]['priority_status']
        if {k for k,v in statuses.items() if v.startswith('hold:')}!={'string/'+k for k in holds}:
            raise ValueError('Hold dispositions differ: '+tag)
    return data


def token_contract(value):
    """Complete printf tokens plus literal-percent count; malformed percent text fails."""
    tokens = Counter(FULL_FORMAT_TOKEN.findall(value))
    remainder = FULL_FORMAT_TOKEN.sub('', value)
    # Source P1 includes literal 100%, (%) and 50–300% with formatted=false.
    # Those do not authorize unknown conversions or partial printf syntax.
    if re.search(r'%(?:[A-Za-z0-9$]|\.[A-Za-z0-9])', remainder):
        raise ValueError('Malformed format syntax')
    return tokens, remainder.count('%')


def require_complete(xml, key, row):
    value = require_string(xml, key, row['target'], {'attributes': row['attributes']})
    if token_contract(value) != token_contract(row['source']):
        raise ValueError(key + ': full printf/literal-percent contract differs')
    if value.count('\\n') != row['source'].count('\\n'):
        raise ValueError(key + ': explicit newline count differs')
    return value


class SlovakSlovenianCatalanPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_current_shape(fixture('slovak_slovenian_catalan_priority_wording.json'))
        cls.xml = {tag: (catalogues.RES / ('values-' + tag) / 'strings.xml').read_text() for tag in TAGS}
        cls.roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}
        cls.default = ET.parse(catalogues.RES / 'values/strings.xml').getroot()
        manifest = json.loads((catalogues.DATA / 'string-importance.json').read_text())
        cls.tiers = {t['id']: set(t['keys']) for t in manifest['tiers']}

    def test_changed_family_inventory_rejects_missing_extra_empty_and_wrong_locale(self):
        self.assertEqual({'sk':172,'sl':171,'ca':169},{tag:len(keys) for tag,keys in CHANGED_KEYS.items()})
        for tag in TAGS:
            key=next(iter(CHANGED_KEYS[tag]))
            for mutation in ('missing','extra','empty','wrong-locale','wrong-schema','missing-identity','extra-identity','wrong-hold','false-hold'):
                data=deepcopy(self.data)
                if mutation=='missing':data['locales'][tag]['values'].pop(key)
                elif mutation=='extra':data['locales'][tag]['values']['unexpected']=deepcopy(data['locales'][tag]['values'][key])
                elif mutation=='empty':data['locales'][tag]['values'][key]['target']=''
                elif mutation=='wrong-locale':data['locales']['unexpected']=data['locales'].pop(tag)
                elif mutation=='wrong-schema':data['schema_version']=2
                elif mutation=='missing-identity':data['locales'][tag]['priority_status'].pop('string/ui_apply')
                elif mutation=='extra-identity':data['locales'][tag]['priority_status']['string/invented']='accept'
                elif mutation=='wrong-hold':data['locales'][tag]['held_absent'].remove('ui_save_as_png')
                else:data['locales'][tag]['priority_status']['string/ui_apply']='hold:invented'
                with self.subTest(tag=tag,mutation=mutation),self.assertRaises(ValueError):require_current_shape(data)

    def test_full_three_language_scope_has_exact_92_plus_249_identity_accounting(self):
        self.assertEqual(TAGS, set(self.data['locales']))
        self.assertEqual(92, len(self.tiers['P0']));self.assertEqual(249, len(self.tiers['P1']))
        for tag, data in self.data['locales'].items():
            with self.subTest(tag=tag):
                self.assertEqual(self.tiers['P0'] | self.tiers['P1'], set(data['priority_status']))
                self.assertEqual(341, len(data['priority_status']))
                self.assertTrue(all(data['priority_status'].values()))
                expected_holds = P0_HOLDS | {PALETTE_HOLD,'ui_pinch_and_pan_mode'}
                self.assertEqual(expected_holds, set(data['held_absent']))
                actual = {node.tag + '/' + node.get('name') for node in self.roots[tag]}
                missing = (self.tiers['P0'] | self.tiers['P1']) - actual
                self.assertEqual({'string/' + k for k in expected_holds-set(RESIDUAL_KEYS.get(tag,()))}, missing)

    def test_complete_changed_values_and_context_match_canonical_values_attributes_and_tokens(self):
        for tag, data in self.data['locales'].items():
            self.assertTrue(data['values'])
            for key, row in data['values'].items():
                with self.subTest(tag=tag,key=key):
                    source = self.default.find(f"./string[@name='{key}']")
                    self.assertIsNotNone(source)
                    self.assertEqual(source.text, row['source']);self.assertEqual(source.attrib,row['attributes'])
                    self.assertIn('string/' + key,self.tiers[row['tier']])
                    require_complete(self.xml[tag],key,row)
            for key, row in data['context'].items():
                with self.subTest(tag=tag,context=key):
                    require_string_root(self.roots[tag],key,row['target'],{'attributes':row['attributes']})

    def test_every_changed_value_rejects_absence_duplicate_wrong_type_markup_attributes_and_truncation(self):
        for tag, data in self.data['locales'].items():
            for key,row in data['values'].items():
                original = self.roots[tag].find(f"./string[@name='{key}']")
                for mutation in ('missing','duplicate','wrong-type','markup','attribute','empty','truncate','token','wrong-locale'):
                    root=ET.Element('resources');node=deepcopy(original)
                    if mutation!='missing':root.append(node)
                    if mutation=='duplicate':root.append(deepcopy(node))
                    elif mutation=='wrong-type':node.tag='plurals'
                    elif mutation=='markup':ET.SubElement(node,'b').text,node.text=node.text,None
                    elif mutation=='attribute':node.set('translatable','false')
                    elif mutation=='empty':node.text=''
                    elif mutation=='truncate':node.text=node.text[:-1]
                    elif mutation=='token':node.text+=' %9$s'
                    elif mutation=='wrong-locale':
                        alternatives=[other['values'][key]['target'] for other_tag,other in self.data['locales'].items()
                                      if other_tag!=tag and key in other['values'] and other['values'][key]['target']!=row['target']]
                        if not alternatives:continue # Invariant numeric-only values carry no language distinction.
                        node.text=alternatives[0]
                    with self.subTest(tag=tag,key=key,mutation=mutation),self.assertRaises(ValueError):
                        require_complete(ET.tostring(root,encoding='unicode'),key,row)

    def test_refreshed_expected_cannot_hide_index_type_precision_width_flags_or_extra_percent(self):
        key='ui_d_d_px_d_pixels_2f_mp'
        for tag,data in self.data['locales'].items():
            row=data['values'][key]
            for old,new in [('%1$d','%2$d'),('%1$d','%1$s'),('%1$d','%d'),('%3$,d','%3$d'),
                            ('%4$.2f','%4$.1f'),('%4$.2f','%4$4.2f'),('%4$.2f','%4$+.2f')]:
                changed=deepcopy(row);changed['target']=row['target'].replace(old,new)
                root=ET.Element('resources');ET.SubElement(root,'string',row['attributes']).text=changed['target']
                with self.subTest(tag=tag,replacement=new),self.assertRaises(ValueError):
                    require_complete(ET.tostring(root,encoding='unicode'),key,changed)
            for suffix in (' %9$s',' %s',' %n',' %%',' %',' %q',' %1$',' %.2q'):
                changed=deepcopy(row);changed['target']+=suffix
                root=ET.Element('resources');ET.SubElement(root,'string',row['attributes']).text=changed['target']
                with self.subTest(tag=tag,suffix=suffix),self.assertRaises(ValueError):
                    require_complete(ET.tostring(root,encoding='unicode'),key,changed)

    def test_literal_percent_labels_keep_their_nonformat_contract(self):
        for tag in ('sk','sl','ca'):
            for key in ('ui_100','ui_actual_size_100','ui_line_spacing','ui_magnification','ui_use_50_300'):
                row=self.data['locales'][tag]['values'][key]
                self.assertEqual('false',row['attributes'].get('formatted'))
                self.assertEqual((Counter(),1),token_contract(row['target']))
                require_complete(self.xml[tag],key,row)
                for suffix in (' %s',' %q',' %%',' %1$'):
                    changed=deepcopy(row);changed['target']+=suffix
                    root=ET.Element('resources');ET.SubElement(root,'string',row['attributes']).text=changed['target']
                    with self.subTest(tag=tag,key=key,suffix=suffix),self.assertRaises(ValueError):
                        require_complete(ET.tostring(root,encoding='unicode'),key,changed)

    def test_dimension_and_crop_dependencies_are_atomic(self):
        required={'ui_width_in','ui_height_in','ui_pixels_6ec9c2','ui_percent_fd8671',
                  'ui_trim_in_pixels','ui_trim_in_percent'}
        for tag,data in self.data['locales'].items():
            self.assertTrue(required <= (set(data['values'])|set(data['context'])))
            for key in ('ui_width_in','ui_height_in','ui_trim_in_pixels','ui_trim_in_percent'):
                self.assertEqual((Counter({'%1$s':1}),0),token_contract(data['values'][key]['target']))
            self.assertTrue({'ui_left','ui_right','ui_bottom','ui_top'} <= (set(data['values'])|set(data['context'])))

    def test_recovery_commands_and_format_labels_match_actual_translated_controls(self):
        for tag in ('sk','sl','ca'):
            data=self.data['locales'][tag]
            value=lambda k:(data['values'].get(k) or data['context'][k])['display']
            paused=value('ui_autosave_is_paused_to_protect_that_draft_use')
            for key in ('ui_menu_file','save20_title','save20_file_format','ui_export_recovery_copy'):
                self.assertIn(value(key),paused)
            self.assertIn(value('ui_load_image'),value('ui_recovery_copy_exported_extract_canvas_png_from_the'))
            for key in ('ui_a_separate_recovery_copy_has_been_kept_use','ui_recovery_copy_exported_extract_canvas_png_from_the'):
                self.assertIn('canvas.png',value(key));self.assertIn('ZIP',value(key))
            self.assertEqual(value('ui_export_recovery_copy_144b8a')+'…',value('ui_export_recovery_copy'))

    def test_no_held_resource_is_silently_added_or_receives_runtime_credit(self):
        for tag in ('sk','sl','ca'):
            data=self.data['locales'][tag]
            for key in P0_HOLDS|{PALETTE_HOLD,'ui_pinch_and_pan_mode'}:
                self.assertNotIn(key,data['values'])
                require_residual_or_previous(self.roots[tag],tag,key)
            dormant=[k for k,v in data['values'].items() if v['scope']=='wording-only-no-direct-consumer']
            self.assertEqual(13,len(dormant))
            self.assertTrue(all('P1'==data['values'][k]['tier'] for k in dormant))

    def test_finite_forward_successors_reject_wrong_previous_values_attributes_and_unknown_scope(self):
        from sk_sl_ca_priority_successors import current_value, current_fixture, REPLACEMENTS
        self.assertEqual({'sk':15,'sl':14,'ca':12},{tag:len(keys) for tag,keys in REPLACEMENTS.items()})
        for tag,keys in REPLACEMENTS.items():
            for key in keys:
                row=self.data['locales'][tag]['values'][key]
                self.assertEqual(row['target'],current_value(tag,key,row['previous_target'],row['previous_attributes']))
                with self.assertRaises(ValueError):current_value(tag,key,row['previous_target']+' changed')
                with self.assertRaises(ValueError):current_value(tag,key,row['previous_target'],{'name':key,'translatable':'false'})
        self.assertEqual('untouched',current_value('unknown','ui_keep_editing23','untouched'))
        self.assertEqual('untouched',current_value('sk','unknown','untouched'))
        self.assertEqual('not a predecessor',current_value('sk','ui_choose_location','not a predecessor'))
        old=fixture('slovak_slovenian_p0_wording.json')
        projected=current_fixture('slovak_slovenian_p0_wording.json')
        for key,values in old['values'].items():
            for tag,value in values.items():
                if key not in {'ui_autosave_is_paused_to_protect_that_draft_use','ui_recovery_copy_exported_extract_canvas_png_from_the'}:
                    self.assertEqual(value,projected['values'][key][tag])
        self.assertEqual(old,fixture('slovak_slovenian_p0_wording.json'))

    def test_three_memory_additions_require_exact_historical_absence_and_corrected_source(self):
        from unittest.mock import patch
        import memory_warning_source_review as warnings
        expected={(tag,'ui_no_resize_fits_decoder_memory') for tag in TAGS}
        self.assertEqual(expected,set(warnings.SK_SL_CA_ADDITIONS))
        for tag,key in expected:
            row=self.data['locales'][tag]['values'][key]
            self.assertIsNone(row['previous_target'])
            self.assertEqual(row['target'],warnings.current_source_expectation(key,tag,None))
            with self.assertRaises(ValueError):warnings.current_source_expectation(key,tag,row['target'])
            for mutation in ('source','predecessor','attributes'):
                data=deepcopy(self.data);changed=data['locales'][tag]['values'][key]
                if mutation=='source':changed['source']+=' changed'
                elif mutation=='predecessor':changed['previous_target']='forged'
                else:changed['attributes']['formatted']='false'
                with patch.object(warnings,'fixture',return_value=data),self.assertRaises(ValueError):
                    warnings.current_source_expectation(key,tag,None)

    def test_complete_catalogue_identity_inventory_remains_unique_and_scoped(self):
        from test_translations import SCOPED_TAGS
        for tag,data in self.data['locales'].items():
            names=[node.tag+'/'+node.get('name') for node in self.roots[tag]]
            self.assertEqual(len(names),len(set(names)))
            self.assertEqual(set(data['catalogue_keys'])|{'string/'+k for k in RESIDUAL_KEYS.get(tag,())},set(names))
            self.assertEqual([],catalogues.validate_catalogue(tag,require_complete=False))
        self.assertEqual(59,len(SCOPED_TAGS));self.assertTrue(TAGS.isdisjoint(SCOPED_TAGS))
        self.assertEqual(171,len(catalogues.offered_tags()))

if __name__=='__main__':unittest.main()
