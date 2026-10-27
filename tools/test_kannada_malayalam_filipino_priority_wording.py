"""Complete source/target/typed scope guards plus actual composition contracts."""
from collections import Counter
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture
from test_danish_norwegian_p0_wording import FULL_FORMAT_TOKEN
import translation_catalogues as catalogues
from kannada_malayalam_filipino_priority_expectations import NAME,TAGS,current_row,display

HOLDS=frozenset({'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png','ui_foreground_background_colour_palette','ui_pinch_and_pan_mode'})
DEPENDENCIES=frozenset({'formats22_at_least_frames','ui_top','ui_width_in','ui_lossless_format','save20_dither','ui_quality','ui_trim_in_pixels','ui_trim_in_percent','ui_rounded_rectangle','ui_star','ui_curve','ui_arrow','ui_heart','ui_image_shown_in_crop_preview','ui_crop_preview_images'})
# Insert exact independently accepted partitions and finite previous values here.
HELD_PRESENT = {'fil': {'formats22_derived_exported': {'attributes': {'name': 'formats22_derived_exported'},
                                        'target': 'Na-export ang %1$s. May hindi pa nase-save na pagbabago ang '
                                                  'buong drawing mo; mag-save muna ng buong kopya ng larawan bago '
                                                  'ito palitan.',
                                        'type': 'string'},
         'ui_foreground_background_colour_palette': {'attributes': {'name': 'ui_foreground_background_colour_palette'},
                                                     'target': 'Harap %1$s, likod %2$s. %3$s paleta ng kulay.',
                                                     'type': 'string'},
         'ui_save_as': {'attributes': {'name': 'ui_save_as'}, 'target': 'I-save bilang %1$s', 'type': 'string'},
         'ui_save_as_jpeg': {'attributes': {'name': 'ui_save_as_jpeg'},
                             'target': 'I-save bilang JPEG…',
                             'type': 'string'},
         'ui_save_as_jpeg_xl': {'attributes': {'name': 'ui_save_as_jpeg_xl'},
                                'target': 'I-save bilang JPEG XL…',
                                'type': 'string'},
         'ui_save_as_png': {'attributes': {'name': 'ui_save_as_png'},
                            'target': 'I-save bilang PNG…',
                            'type': 'string'}},
 'kn': {},
 'ml-IN': {}}

HELD_ABSENT = {'fil': set(),
 'kn': {'formats22_derived_exported',
        'ui_foreground_background_colour_palette',
        'ui_pinch_and_pan_mode',
        'ui_save_as',
        'ui_save_as_jpeg',
        'ui_save_as_jpeg_xl',
        'ui_save_as_png'},
 'ml-IN': {'formats22_derived_exported',
           'ui_foreground_background_colour_palette',
           'ui_pinch_and_pan_mode',
           'ui_save_as',
           'ui_save_as_jpeg',
           'ui_save_as_jpeg_xl',
           'ui_save_as_png'}}

PLURAL_QUANTITIES = {'fil': {'other'}, 'kn': {'one', 'other'}, 'ml-IN': {'one', 'other'}}

UNCHANGED = {'fil': {'colour_converter_unavailable',
         'colour_invalid_metadata',
         'colour_truncated_metadata',
         'colour_unsupported_icc_model',
         'commons_svg_original_size_too_large',
         'commons_svg_original_size_unavailable',
         'formats22_animation_message',
         'formats22_animation_poster',
         'formats22_animation_still',
         'formats22_animation_title',
         'formats22_animation_unknown',
         'formats22_ascii_description',
         'formats22_at_least_frames',
         'formats22_import_limit',
         'formats22_open_still',
         'formats22_pdf_raster_hint',
         'gallery_credit_could_not_save',
         'gallery_credit_too_large',
         'language20_app_language',
         'language20_current',
         'language20_device_default',
         'language20_settings',
         'language20_translation_note',
         'legacy_credits_unreadable',
         'save20_destination_error',
         'save20_dither',
         'save20_encoding_budget',
         'save20_file_format',
         'save20_file_name',
         'save20_gif_description',
         'save20_invalid_name',
         'save20_lossy_quality_description',
         'save20_title',
         'save20_unsupported_image_colour',
         'ui_0f_0f_px_1f',
         'ui_100',
         'ui_1_px',
         'ui_1f_s',
         'ui_a_separate_recovery_copy_has_been_kept_use',
         'ui_actual_size_100',
         'ui_add_colour26',
         'ui_add_text',
         'ui_airbrush',
         'ui_all',
         'ui_an_assembly_source_image_is_missing',
         'ui_android_blocked_the_file_picker',
         'ui_android_could_not_decode_this_image',
         'ui_android_could_not_find_a_file_picker_enable',
         'ui_apply',
         'ui_apply_bounds',
         'ui_apply_crop',
         'ui_arrow',
         'ui_assembly_saved',
         'ui_assembly_source_memory_floor',
         'ui_autosave_failed_use_save',
         'ui_autosave_image_encoding_failed',
         'ui_autosave_is_paused_to_protect_that_draft_use',
         'ui_autosave_metadata_is_missing',
         'ui_autosave_paused_use_save',
         'ui_autosave_pixels_are_missing',
         'ui_autosave_pixels_could_not_be_read',
         'ui_autosave_selection_encoding_failed',
         'ui_autosaving_draft',
         'ui_background_colour',
         'ui_background_edit_colour',
         'ui_basic_colours',
         'ui_bg',
         'ui_bold',
         'ui_bottom',
         'ui_brush',
         'ui_bucket_fill',
         'ui_cancel',
         'ui_cannot_create_the_undo_cache_free_some_device',
         'ui_canvas_bounds',
         'ui_canvas_size',
         'ui_canvas_size_30460e',
         'ui_canvas_zoom',
         'ui_canvas_zoom_771f84',
         'ui_category_brush',
         'ui_category_insert',
         'ui_category_selection',
         'ui_centred',
         'ui_choose_a_smaller_output_copy_the_source_images',
         'ui_choose_a_smaller_size',
         'ui_choose_at_least_one_image',
         'ui_choose_dimensions_no_larger_than_the_original',
         'ui_choose_location',
         'ui_clear_all',
         'ui_clear_image',
         'ui_codec_resize_memory_floor',
         'ui_collapse_colour_palette',
         'ui_collapse_tool_category',
         'ui_collapse_toolbox',
         'ui_colour',
         'ui_colour_palette_tap_for_foreground_hold_for_background',
         'ui_colour_tab23',
         'ui_colour_tap_foreground_hold_background',
         'ui_commit_selection',
         'ui_copy',
         'ui_copy_all',
         'ui_could_not_apply_the_crop',
         'ui_could_not_complete_the_edit',
         'ui_could_not_complete_the_operation',
         'ui_could_not_export_the_recovery_copy',
         'ui_could_not_open_image',
         'ui_could_not_place_the_image',
         'ui_could_not_prepare_the_image',
         'ui_could_not_save_image',
         'ui_could_not_save_the_assembly',
         'ui_could_not_store_the_assembly',
         'ui_crop',
         'ui_crop_image',
         'ui_crop_must_stay_inside_the_canvas',
         'ui_crop_preview_drag_an_edge_or_corner_drag',
         'ui_crop_to_selection',
         'ui_curve',
         'ui_cut',
         'ui_d_d_pixels_2f_mp_exceeds_the_current',
         'ui_d_d_px_d_pixels_2f_mp',
         'ui_delete_selection',
         'ui_discard_changes23',
         'ui_done',
         'ui_draft_not_saved_yet',
         'ui_draft_pending',
         'ui_draft_restored',
         'ui_draft_saved',
         'ui_draw26',
         'ui_drawing23',
         'ui_drawing_canvas_pinch_and_move_two_fingers_to',
         'ui_drawing_settings',
         'ui_drawing_settings_d900c6',
         'ui_edit_background',
         'ui_edit_canvas33',
         'ui_edit_colour26',
         'ui_edit_foreground',
         'ui_edit_transform33',
         'ui_ellipse',
         'ui_enter_a_number_from_to',
         'ui_enter_a_positive_size',
         'ui_enter_a_trim_amount_for_every_edge',
         'ui_enter_a_whole_number_from_to',
         'ui_enter_all_four_trim_amounts',
         'ui_enter_positive_canvas_dimensions_within_android_s_coordinate',
         'ui_enter_positive_dimensions',
         'ui_enter_positive_dimensions_no_larger_than_the_original',
         'ui_enter_positive_dimensions_that_resolve_to_at_least',
         'ui_enter_positive_image_dimensions',
         'ui_enter_valid_dimensions',
         'ui_eraser',
         'ui_expand_colour_palette',
         'ui_expand_tool_category',
         'ui_expand_toolbox',
         'ui_export_as23',
         'ui_export_did_not_save23',
         'ui_export_explanation23',
         'ui_export_recovery_copy',
         'ui_export_recovery_copy_144b8a',
         'ui_eyedropper',
         'ui_fg',
         'ui_fit',
         'ui_fit_entire_canvas_in_view',
         'ui_fit_image',
         'ui_fit_selection34',
         'ui_flip_horizontal',
         'ui_flip_vertical',
         'ui_font',
         'ui_font_family',
         'ui_foreground_colour',
         'ui_foreground_edit_colour',
         'ui_free_form_select',
         'ui_from_device34',
         'ui_full_text_copied',
         'ui_heart',
         'ui_height',
         'ui_height_in',
         'ui_heights',
         'ui_hex_rrggbb',
         'ui_hide_editor_controls',
         'ui_higher_quality_usually_makes_a_larger_file_lossless',
         'ui_history_unavailable34',
         'ui_image',
         'ui_image_shown_in_crop_preview',
         'ui_insert',
         'ui_insert_image_into_canvas',
         'ui_invalid_autosave_metadata',
         'ui_invalid_colour',
         'ui_invalid_selection_outline',
         'ui_invert_colours',
         'ui_italic',
         'ui_keep_editing23',
         'ui_keeps_pixels_at_the_top_left_smaller_canvas',
         'ui_languages23',
         'ui_left',
         'ui_left_aligned',
         'ui_left_arrow_collapse',
         'ui_line',
         'ui_line_spacing',
         'ui_load_image',
         'ui_lock_aspect_ratio',
         'ui_lock_proportions',
         'ui_lossless_format',
         'ui_magnification',
         'ui_main23',
         'ui_menu',
         'ui_menu_colours',
         'ui_menu_edit',
         'ui_menu_file',
         'ui_menu_help',
         'ui_menu_image',
         'ui_menu_view',
         'ui_navigate',
         'ui_new',
         'ui_new_colour',
         'ui_new_image',
         'ui_no_readable_image_data',
         'ui_no_resize_fits_decoder_memory',
         'ui_none',
         'ui_not_enough_memory_for_this_operation_the_assembly',
         'ui_not_enough_memory_to_finish_opening_this_image',
         'ui_not_enough_memory_to_inspect_this_image',
         'ui_not_enough_memory_to_save_in_this_format',
         'ui_numeric_slider_value',
         'ui_ok',
         'ui_original_size34',
         'ui_other_images34',
         'ui_outline',
         'ui_palette',
         'ui_paste',
         'ui_paste_hint34',
         'ui_pencil',
         'ui_percent',
         'ui_percent_fd8671',
         'ui_pinch_and_pan_mode',
         'ui_pixels',
         'ui_pixels_6ec9c2',
         'ui_place_text',
         'ui_please_try_again',
         'ui_please_wait_for_the_current_operation',
         'ui_png_encoding_failed',
         'ui_polygon',
         'ui_preview',
         'ui_previous_draft_kept_for_recovery',
         'ui_px',
         'ui_px_724eb3',
         'ui_quality',
         'ui_ready',
         'ui_recovered_image',
         'ui_recovery_copy_exported_extract_canvas_png_from_the',
         'ui_rectangle',
         'ui_rectangle_select',
         'ui_redo',
         'ui_remove',
         'ui_reset_bw23',
         'ui_reset_crop',
         'ui_reset_to_black_white',
         'ui_resize_and_load',
         'ui_resize_image',
         'ui_resize_image_ab28be',
         'ui_resize_large_image',
         'ui_resize_the_copy',
         'ui_right',
         'ui_right_aligned',
         'ui_rotate',
         'ui_rotate_180',
         'ui_rotate_90_clockwise',
         'ui_rounded_rectangle',
         'ui_sampled_resize_memory_explanation',
         'ui_save',
         'ui_save_a5d0d9',
         'ui_save_and_share',
         'ui_save_and_share_41edb4',
         'ui_save_explanation23',
         'ui_save_png',
         'ui_save_your_changes',
         'ui_saved',
         'ui_select_all',
         'ui_select_an_area',
         'ui_select_an_area_first',
         'ui_selected_colour23',
         'ui_selection_dimensions_are_too_large',
         'ui_share_explanation34',
         'ui_share_saved_image',
         'ui_show_all',
         'ui_show_controls',
         'ui_show_editor_controls',
         'ui_show_magnified_drawing_preview',
         'ui_size_pixels',
         'ui_size_px',
         'ui_star',
         'ui_swap23',
         'ui_swap_foreground_background',
         'ui_tap_an_image_first',
         'ui_tap_canvas_to_type',
         'ui_tap_to_type_a_number',
         'ui_text',
         'ui_text_alignment',
         'ui_text_direction23',
         'ui_the_crop_must_contain_at_least_one_pixel',
         'ui_the_crop_must_stay_inside_the_image',
         'ui_the_decoder_and_editing_buffers_need_about_the',
         'ui_the_draft_is_saving_try_again_shortly',
         'ui_the_encoder_did_not_finish',
         'ui_the_full_image_and_working_buffers_exceed_the',
         'ui_the_image_was_saved_but_android_could_not',
         'ui_the_picker_returned_no_file_please_choose_the',
         'ui_the_picker_returned_no_files',
         'ui_the_previous_draft_could_not_be_moved_to',
         'ui_the_previous_draft_could_not_be_preserved_separately',
         'ui_the_previous_draft_could_not_be_restored',
         'ui_the_previous_draft_needs_more_memory_to_reopen',
         'ui_the_saved_assembly_could_not_be_opened',
         'ui_the_selected_location_is_not_writable',
         'ui_the_selected_provider_did_not_return_any_image',
         'ui_the_trim_would_remove_the_entire_image',
         'ui_the_undo_cache_is_damaged',
         'ui_there_is_not_enough_memory_for_this_operation',
         'ui_this_file_is_not_a_supported_image_use',
         'ui_this_location_is_not_writable',
         'ui_tolerance',
         'ui_too_large_for_the_current_budget_reduce_the',
         'ui_tool_categories',
         'ui_top',
         'ui_trim_amounts_must_be_zero_or_greater',
         'ui_trim_amounts_must_fit_inside_each_image_use',
         'ui_trim_expand_canvas_by_touch',
         'ui_trim_in_percent',
         'ui_trim_in_pixels',
         'ui_try_a_different_file_or_location',
         'ui_type_text',
         'ui_underline',
         'ui_undo',
         'ui_unexpected_data_in_the_undo_cache',
         'ui_untitled',
         'ui_use_1_1024_pixels',
         'ui_use_50_300',
         'ui_use_a_positive_target_dimension',
         'ui_use_colour',
         'ui_use_rrggbb',
         'ui_watercolor',
         'ui_width',
         'ui_width_in',
         'ui_working',
         'ui_your_current_image_has_unsaved_changes',
         'ui_zoom_in',
         'ui_zoom_out'},
 'kn': {'language20_settings',
        'save20_file_name',
        'ui_arrow',
        'ui_cancel',
        'ui_canvas_size',
        'ui_canvas_size_30460e',
        'ui_category_insert',
        'ui_category_selection',
        'ui_copy',
        'ui_cut',
        'ui_discard_changes23',
        'ui_edit_background',
        'ui_edit_foreground',
        'ui_image',
        'ui_insert',
        'ui_ok',
        'ui_palette',
        'ui_paste',
        'ui_pencil',
        'ui_pixels',
        'ui_pixels_6ec9c2',
        'ui_preview',
        'ui_ready',
        'ui_rectangle',
        'ui_rectangle_select',
        'ui_remove',
        'ui_rotate',
        'ui_select_all',
        'ui_text',
        'ui_untitled',
        'ui_zoom_in',
        'ui_zoom_out'},
 'ml-IN': {'ui_cancel',
           'ui_copy',
           'ui_cut',
           'ui_image',
           'ui_languages23',
           'ui_ok',
           'ui_paste',
           'ui_pixels',
           'ui_pixels_6ec9c2',
           'ui_preview',
           'ui_ready',
           'ui_select_all',
           'ui_text',
           'ui_untitled',
           'ui_zoom_in',
           'ui_zoom_out'}}

PREDECESSORS = {'fil': {'ui_crop_preview_images': {'attributes': {'name': 'ui_crop_preview_images'},
                                    'target': {'other': 'Preview: %1$d × %2$d px\\nIlalapat sa %3$d larawan. '
                                                        'Kapag kino-crop ang nakapuwestong larawan, inaayos din '
                                                        'ang posisyon ng mga nakakabit na larawan.'},
                                    'type': 'plurals'},
         'ui_discard': {'attributes': {'name': 'ui_discard'},
                        'target': 'Itapon ang mga pagbabago',
                        'type': 'string'},
         'ui_draw_again': {'attributes': {'name': 'ui_draw_again'}, 'target': 'Gumuhit muli', 'type': 'string'},
         'ui_scales_the_image_unlock_the_ratio_to_stretch': {'attributes': {'name': 'ui_scales_the_image_unlock_the_ratio_to_stretch'},
                                                             'target': 'Sine-scale ang larawan. I-unlock ang '
                                                                       'ratio upang hiwalay na i-stretch ang '
                                                                       'lapad at taas.',
                                                             'type': 'string'},
         'ui_solid_fill': {'attributes': {'name': 'ui_solid_fill'}, 'target': 'Punuin', 'type': 'string'}},
 'kn': {'save20_file_format': {'attributes': {'name': 'save20_file_format'},
                               'target': 'Image format',
                               'type': 'string'},
        'ui_airbrush': {'attributes': {'name': 'ui_airbrush'}, 'target': 'Spray can', 'type': 'string'},
        'ui_apply': {'attributes': {'name': 'ui_apply'}, 'target': 'Apply', 'type': 'string'},
        'ui_brush': {'attributes': {'name': 'ui_brush'}, 'target': 'Brush', 'type': 'string'},
        'ui_bucket_fill': {'attributes': {'name': 'ui_bucket_fill'}, 'target': 'Fill', 'type': 'string'},
        'ui_category_brush': {'attributes': {'name': 'ui_category_brush'}, 'target': 'Brush', 'type': 'string'},
        'ui_discard': {'attributes': {'name': 'ui_discard'}, 'target': 'Discard', 'type': 'string'},
        'ui_done': {'attributes': {'name': 'ui_done'}, 'target': 'Done', 'type': 'string'},
        'ui_ellipse': {'attributes': {'name': 'ui_ellipse'}, 'target': 'Ellipse', 'type': 'string'},
        'ui_eraser': {'attributes': {'name': 'ui_eraser'}, 'target': 'Eraser', 'type': 'string'},
        'ui_eyedropper': {'attributes': {'name': 'ui_eyedropper'}, 'target': 'Pipette', 'type': 'string'},
        'ui_flip_horizontal': {'attributes': {'name': 'ui_flip_horizontal'},
                               'target': 'flip horizontal',
                               'type': 'string'},
        'ui_flip_vertical': {'attributes': {'name': 'ui_flip_vertical'},
                             'target': 'flip vertical',
                             'type': 'string'},
        'ui_heart': {'attributes': {'name': 'ui_heart'}, 'target': 'Heart', 'type': 'string'},
        'ui_keep_editing23': {'attributes': {'name': 'ui_keep_editing23'},
                              'target': '"ರದ್ದುಮಾಡಿ"',
                              'type': 'string'},
        'ui_line': {'attributes': {'name': 'ui_line'}, 'target': '"ಸಾಲು"', 'type': 'string'},
        'ui_menu_colours': {'attributes': {'name': 'ui_menu_colours'}, 'target': 'Color', 'type': 'string'},
        'ui_menu_help': {'attributes': {'name': 'ui_menu_help'}, 'target': 'Help', 'type': 'string'},
        'ui_new_image': {'attributes': {'name': 'ui_new_image'}, 'target': 'New image', 'type': 'string'},
        'ui_outline': {'attributes': {'name': 'ui_outline'}, 'target': 'Outline', 'type': 'string'},
        'ui_quality': {'attributes': {'name': 'ui_quality'}, 'target': 'Quality', 'type': 'string'},
        'ui_redo': {'attributes': {'name': 'ui_redo'}, 'target': 'Redo', 'type': 'string'},
        'ui_save': {'attributes': {'name': 'ui_save'}, 'target': 'Save', 'type': 'string'},
        'ui_save_a5d0d9': {'attributes': {'name': 'ui_save_a5d0d9'}, 'target': 'Save', 'type': 'string'},
        'ui_save_your_changes': {'attributes': {'name': 'ui_save_your_changes'},
                                 'target': 'Save changes?',
                                 'type': 'string'},
        'ui_solid_fill': {'attributes': {'name': 'ui_solid_fill'}, 'target': 'Fill', 'type': 'string'},
        'ui_star': {'attributes': {'name': 'ui_star'}, 'target': 'Star', 'type': 'string'},
        'ui_undo': {'attributes': {'name': 'ui_undo'}, 'target': 'Undo', 'type': 'string'},
        'ui_watercolor': {'attributes': {'name': 'ui_watercolor'}, 'target': 'Watercolor', 'type': 'string'}},
 'ml-IN': {'language20_app_language': {'attributes': {'name': 'language20_app_language'},
                                       'target': '"ഭാഷ"',
                                       'type': 'string'},
           'language20_settings': {'attributes': {'name': 'language20_settings'},
                                   'target': 'Settings',
                                   'type': 'string'},
           'save20_file_format': {'attributes': {'name': 'save20_file_format'},
                                  'target': 'Image format',
                                  'type': 'string'},
           'save20_file_name': {'attributes': {'name': 'save20_file_name'},
                                'target': 'Image name',
                                'type': 'string'},
           'ui_airbrush': {'attributes': {'name': 'ui_airbrush'}, 'target': 'Spray can', 'type': 'string'},
           'ui_apply': {'attributes': {'name': 'ui_apply'}, 'target': 'Apply', 'type': 'string'},
           'ui_brush': {'attributes': {'name': 'ui_brush'}, 'target': 'Brush', 'type': 'string'},
           'ui_bucket_fill': {'attributes': {'name': 'ui_bucket_fill'}, 'target': 'Fill', 'type': 'string'},
           'ui_category_brush': {'attributes': {'name': 'ui_category_brush'}, 'target': 'Brush', 'type': 'string'},
           'ui_discard': {'attributes': {'name': 'ui_discard'}, 'target': 'Discard', 'type': 'string'},
           'ui_discard_changes23': {'attributes': {'name': 'ui_discard_changes23'},
                                    'target': 'Discard',
                                    'type': 'string'},
           'ui_done': {'attributes': {'name': 'ui_done'}, 'target': 'Done', 'type': 'string'},
           'ui_edit_background': {'attributes': {'name': 'ui_edit_background'},
                                  'target': '"പശ്ചാതല നിറം മാറ്റുക…"',
                                  'type': 'string'},
           'ui_ellipse': {'attributes': {'name': 'ui_ellipse'}, 'target': 'Ellipse', 'type': 'string'},
           'ui_eraser': {'attributes': {'name': 'ui_eraser'}, 'target': 'Eraser', 'type': 'string'},
           'ui_eyedropper': {'attributes': {'name': 'ui_eyedropper'}, 'target': 'Pipette', 'type': 'string'},
           'ui_flip_horizontal': {'attributes': {'name': 'ui_flip_horizontal'},
                                  'target': 'flip horizontal',
                                  'type': 'string'},
           'ui_flip_vertical': {'attributes': {'name': 'ui_flip_vertical'},
                                'target': 'flip vertical',
                                'type': 'string'},
           'ui_heart': {'attributes': {'name': 'ui_heart'}, 'target': 'Heart', 'type': 'string'},
           'ui_keep_editing23': {'attributes': {'name': 'ui_keep_editing23'},
                                 'target': '"റദ്ദാക്കുക"',
                                 'type': 'string'},
           'ui_line': {'attributes': {'name': 'ui_line'}, 'target': 'Line', 'type': 'string'},
           'ui_menu_colours': {'attributes': {'name': 'ui_menu_colours'}, 'target': 'Color', 'type': 'string'},
           'ui_menu_help': {'attributes': {'name': 'ui_menu_help'}, 'target': 'Help', 'type': 'string'},
           'ui_new_image': {'attributes': {'name': 'ui_new_image'}, 'target': 'New image', 'type': 'string'},
           'ui_outline': {'attributes': {'name': 'ui_outline'}, 'target': 'Outline', 'type': 'string'},
           'ui_quality': {'attributes': {'name': 'ui_quality'}, 'target': 'Quality', 'type': 'string'},
           'ui_rectangle': {'attributes': {'name': 'ui_rectangle'}, 'target': 'Rectangle', 'type': 'string'},
           'ui_redo': {'attributes': {'name': 'ui_redo'}, 'target': 'Redo', 'type': 'string'},
           'ui_save': {'attributes': {'name': 'ui_save'}, 'target': 'Save', 'type': 'string'},
           'ui_save_a5d0d9': {'attributes': {'name': 'ui_save_a5d0d9'}, 'target': 'Save', 'type': 'string'},
           'ui_save_your_changes': {'attributes': {'name': 'ui_save_your_changes'},
                                    'target': 'Save changes?',
                                    'type': 'string'},
           'ui_solid_fill': {'attributes': {'name': 'ui_solid_fill'}, 'target': 'Fill', 'type': 'string'},
           'ui_star': {'attributes': {'name': 'ui_star'}, 'target': 'Star', 'type': 'string'},
           'ui_undo': {'attributes': {'name': 'ui_undo'}, 'target': 'Undo', 'type': 'string'},
           'ui_watercolor': {'attributes': {'name': 'ui_watercolor'}, 'target': 'Watercolor', 'type': 'string'}}}

OUTSIDE_REVIEW = {'fil': {'colour20_custom_selected_slot': {'attributes': {'name': 'colour20_custom_selected_slot'},
                                           'target': 'Mga pasadyang kulay · Napili ang slot %1$d',
                                           'type': 'string'},
         'colour20_empty_slot': {'attributes': {'name': 'colour20_empty_slot'},
                                 'target': 'Bakanteng slot %1$d. I-tap para piliin kung saan ise-save ang '
                                           'kasalukuyang kulay.',
                                 'type': 'string'},
         'colour20_replace_slot': {'attributes': {'name': 'colour20_replace_slot'},
                                   'target': 'Palitan ang slot %1$d',
                                   'type': 'string'},
         'colour20_save_slot': {'attributes': {'name': 'colour20_save_slot'},
                                'target': 'I-save sa slot %1$d',
                                'type': 'string'},
         'colour20_saved_slot': {'attributes': {'name': 'colour20_saved_slot'},
                                 'target': 'Na-save ang kulay sa slot %1$d',
                                 'type': 'string'},
         'colour20_stored_slot': {'attributes': {'name': 'colour20_stored_slot'},
                                  'target': 'Slot %1$d · %2$s. I-tap para gamitin; isaayos ang kulay, saka '
                                            'Palitan para i-save ang pagbabago.',
                                  'type': 'string'},
         'commons_blank_maps': {'attributes': {'name': 'commons_blank_maps'},
                                'target': 'Wikimedia Commons · Mga blangkong mapa…',
                                'type': 'string'},
         'commons_check_file_licence': {'attributes': {'name': 'commons_check_file_licence'},
                                        'target': 'Tingnan ang pahina ng file ng bawat mapa sa Commons para sa '
                                                  'gumawa nito, lisensiya at kailangang pagkilala sa may-akda. '
                                                  'Maaaring ituring na adaptasyon ang mga pagbabago.',
                                        'type': 'string'},
         'commons_credit_copy_failed': {'attributes': {'name': 'commons_credit_copy_failed'},
                                        'target': 'Hindi makopya ang pagkilala para sa larawan.',
                                        'type': 'string'},
         'commons_credit_copy_failed_reason': {'attributes': {'name': 'commons_credit_copy_failed_reason'},
                                               'target': 'Hindi makopya ang pagkilala para sa larawan: %1$s',
                                               'type': 'string'},
         'commons_credit_copy_out_of_memory': {'attributes': {'name': 'commons_credit_copy_out_of_memory'},
                                               'target': 'Kulang ang memory para kopyahin ang pagkilala para sa '
                                                         'larawan.',
                                               'type': 'string'},
         'commons_download_original_mismatch': {'attributes': {'name': 'commons_download_original_mismatch'},
                                                'target': 'Na-redirect ang pag-download mula sa Commons sa ibang '
                                                          'orihinal na file.',
                                                'type': 'string'},
         'commons_import_raster_changes': {'attributes': {'name': 'commons_import_raster_changes'},
                                           'target': 'AN Paint: background=#FFFFFF (pagsasama gamit ang alpha).',
                                           'type': 'string'},
         'commons_import_svg_changes': {'attributes': {'name': 'commons_import_svg_changes'},
                                        'target': 'AN Paint: SVG → PNG; orihinal na laki; antiAlias=false; '
                                                  'strokeDashArray=none; background=#FFFFFF.',
                                        'type': 'string'},
         'commons_metadata_ambiguous_file': {'attributes': {'name': 'commons_metadata_ambiguous_file'},
                                             'target': 'Hindi matukoy nang malinaw mula sa metadata ng Commons '
                                                       'kung aling file ang tinutukoy',
                                             'type': 'string'},
         'commons_metadata_cache_failed': {'attributes': {'name': 'commons_metadata_cache_failed'},
                                           'target': 'Hindi napanatili ang pagkilala para sa larawan mula sa '
                                                     'Commons',
                                           'type': 'string'},
         'commons_metadata_field_too_large': {'attributes': {'name': 'commons_metadata_field_too_large'},
                                              'target': 'Lumampas ang field ng pagkilala para sa larawan sa '
                                                        'Commons sa limitasyon sa haba ng teksto',
                                              'type': 'string'},
         'commons_metadata_http_error': {'attributes': {'name': 'commons_metadata_http_error'},
                                         'target': 'Metadata ng Commons: HTTP %1$s',
                                         'type': 'string'},
         'commons_metadata_invalid_page': {'attributes': {'name': 'commons_metadata_invalid_page'},
                                           'target': 'Hindi wastong pahina ng pagkilala para sa larawan sa '
                                                     'Commons',
                                           'type': 'string'},
         'commons_metadata_not_file_page': {'attributes': {'name': 'commons_metadata_not_file_page'},
                                            'target': 'Hindi ito pahina ng file sa Commons',
                                            'type': 'string'},
         'commons_metadata_original_mismatch': {'attributes': {'name': 'commons_metadata_original_mismatch'},
                                                'target': 'Ang pagkilala para sa larawan mula sa Commons ay hindi '
                                                          'tumutugma sa napiling orihinal na file',
                                                'type': 'string'},
         'commons_metadata_query_failed': {'attributes': {'name': 'commons_metadata_query_failed'},
                                           'target': 'Nabigo ang kahilingan para sa metadata ng Commons',
                                           'type': 'string'},
         'commons_metadata_response_too_large': {'attributes': {'name': 'commons_metadata_response_too_large'},
                                                 'target': 'Lumampas ang metadata mula sa Commons sa limitasyon '
                                                           'ng laki ng tugon',
                                                 'type': 'string'},
         'commons_metadata_unavailable': {'attributes': {'name': 'commons_metadata_unavailable'},
                                          'target': 'Hindi available ang metadata ng file sa Commons',
                                          'type': 'string'},
         'commons_svg_png_encode_failed': {'attributes': {'name': 'commons_svg_png_encode_failed'},
                                           'target': 'Hindi na-encode bilang PNG ang blangkong mapa',
                                           'type': 'string'},
         'commons_svg_too_large': {'attributes': {'name': 'commons_svg_too_large'},
                                   'target': 'SVG > 32 MiB',
                                   'type': 'string'},
         'formats22_ascii_columns': {'attributes': {'name': 'formats22_ascii_columns'},
                                     'target': 'Lapad (characters)',
                                     'type': 'string'},
         'formats22_ascii_invert': {'attributes': {'name': 'formats22_ascii_invert'},
                                    'target': 'Baligtarin ang maliwanag at madilim na character',
                                    'type': 'string'},
         'formats22_ascii_label': {'attributes': {'name': 'formats22_ascii_label'},
                                   'target': 'ASCII art',
                                   'type': 'string'},
         'formats22_base64_description': {'attributes': {'name': 'formats22_base64_description'},
                                          'target': 'Nagse-save ng lossless PNG bilang Base64 text na nagsisimula '
                                                    'sa data:image/png;base64,. Buksan muli ang text file na ito '
                                                    'para maibalik ang larawan. Mas malaki ang Base64 kaysa sa '
                                                    'PNG na laman nito.',
                                          'type': 'string'},
         'formats22_base64_label': {'attributes': {'name': 'formats22_base64_label'},
                                    'target': 'Base64 text',
                                    'type': 'string'},
         'formats22_dib_description': {'attributes': {'name': 'formats22_dib_description'},
                                       'target': 'Nagse-save ng uncompressed na 24-bit Windows DIB. Gumamit ng '
                                                 'BMP kung nangangailangan ang tumatanggap na app ng BMP file '
                                                 'header.',
                                       'type': 'string'},
         'formats22_dib_size_limit': {'attributes': {'name': 'formats22_dib_size_limit'},
                                      'target': 'Lumampas ang larawan sa limitasyon ng laki ng DIB file.',
                                      'type': 'string'},
         'formats22_ico_decode_budget': {'attributes': {'name': 'formats22_ico_decode_budget'},
                                         'target': 'Lumampas ang pag-decode ng icon na ito sa available na image '
                                                   'memory limit.',
                                         'type': 'string'},
         'formats22_ico_description': {'attributes': {'name': 'formats22_ico_description'},
                                       'target': 'Nagse-save ng isang PNG-compressed icon image sa napiling laki '
                                                 '(16–256 pixels). Pinananatili ng larawan ang proporsyon nito at '
                                                 'nakasentro ito sa transparent na parisukat.',
                                       'type': 'string'},
         'formats22_ico_dimensions_error': {'attributes': {'name': 'formats22_ico_dimensions_error'},
                                            'target': 'Hindi tugma ang sukat ng icon image sa directory nito.',
                                            'type': 'string'},
         'formats22_ico_invalid_size': {'attributes': {'name': 'formats22_ico_invalid_size'},
                                        'target': 'Pumili ng icon size na 16, 24, 32, 48, 64, 128 o 256 pixels.',
                                        'type': 'string'},
         'formats22_ico_size': {'attributes': {'name': 'formats22_ico_size'},
                                'target': 'Laki ng icon',
                                'type': 'string'},
         'formats22_loading_page': {'attributes': {'name': 'formats22_loading_page'},
                                    'target': 'Page %1$d ng %2$d · Nilo-load ang preview…',
                                    'type': 'string'},
         'formats22_next_page': {'attributes': {'name': 'formats22_next_page'},
                                 'target': 'Susunod na page',
                                 'type': 'string'},
         'formats22_open_page': {'attributes': {'name': 'formats22_open_page'},
                                 'target': 'Buksan ang page',
                                 'type': 'string'},
         'formats22_page_description': {'attributes': {'name': 'formats22_page_description'},
                                        'target': '%1$s · %2$s\\n%3$d page. Pumili ng isang page na ie-edit '
                                                  'bilang larawan.',
                                        'type': 'string'},
         'formats22_page_dimensions': {'attributes': {'name': 'formats22_page_dimensions'},
                                       'target': 'Page %1$d ng %2$d · %3$d × %4$d pixels',
                                       'type': 'string'},
         'formats22_page_number': {'attributes': {'name': 'formats22_page_number'},
                                   'target': 'Numero ng page',
                                   'type': 'string'},
         'formats22_page_preview': {'attributes': {'name': 'formats22_page_preview'},
                                    'target': 'Preview ng napiling page',
                                    'type': 'string'},
         'formats22_page_range': {'attributes': {'name': 'formats22_page_range'},
                                  'target': 'Maglagay ng page number mula 1 hanggang %1$d.',
                                  'type': 'string'},
         'formats22_pdf_crop': {'attributes': {'name': 'formats22_pdf_crop'},
                                'target': 'Dapat nasa loob ng napiling page ang parihabang crop ng PDF, at '
                                          'parehong higit sa zero ang lapad at taas nito.',
                                'type': 'string'},
         'formats22_pdf_dimensions': {'attributes': {'name': 'formats22_pdf_dimensions'},
                                      'target': 'Hindi wasto o masyadong malaki ang sukat ng PDF page para '
                                                'i-import.',
                                      'type': 'string'},
         'formats22_pdf_encrypted': {'attributes': {'name': 'formats22_pdf_encrypted'},
                                     'target': 'Nangangailangan ng password ang PDF o gumagamit ng hindi '
                                               'sinusuportahang encryption. Mag-save muna ng hindi protektadong '
                                               'kopya bago i-import.',
                                     'type': 'string'},
         'formats22_pdf_file_size': {'attributes': {'name': 'formats22_pdf_file_size'},
                                     'target': 'Dapat hindi walang laman ang PDF at hindi lalampas sa 512 MiB.',
                                     'type': 'string'},
         'formats22_pdf_invalid': {'attributes': {'name': 'formats22_pdf_invalid'},
                                   'target': 'Hindi mabasa ang PDF. Maaaring sira ang file o gumagamit ito ng '
                                             'feature na hindi sinusuportahan ng bersiyong ito ng Android.',
                                   'type': 'string'},
         'formats22_pdf_memory': {'attributes': {'name': 'formats22_pdf_memory'},
                                  'target': 'Lumampas ang PDF rendering sa available na image memory limit.',
                                  'type': 'string'},
         'formats22_pdf_page_count': {'attributes': {'name': 'formats22_pdf_page_count'},
                                      'target': 'Dapat may 1 hanggang %1$d page ang PDF.',
                                      'type': 'string'},
         'formats22_pdf_page_index': {'attributes': {'name': 'formats22_pdf_page_index'},
                                      'target': 'Hindi na wasto ang napiling PDF page. Pumili ng page mula sa '
                                                'dokumentong ito.',
                                      'type': 'string'},
         'formats22_preview_memory': {'attributes': {'name': 'formats22_preview_memory'},
                                      'target': 'Kulang ang memory para sa preview na ito. Kapag binuksan ang '
                                                'page, mag-aalok ng mas maliit na sukat kung posible.',
                                      'type': 'string'},
         'formats22_preview_unavailable': {'attributes': {'name': 'formats22_preview_unavailable'},
                                           'target': 'Hindi available ang preview: %1$s',
                                           'type': 'string'},
         'formats22_previous_page': {'attributes': {'name': 'formats22_previous_page'},
                                     'target': 'Nakaraang page',
                                     'type': 'string'},
         'formats22_select_page': {'attributes': {'name': 'formats22_select_page'},
                                   'target': 'Pumili ng page',
                                   'type': 'string'},
         'formats22_text_not_image': {'attributes': {'name': 'formats22_text_not_image'},
                                      'target': 'Walang sinusuportahang larawan ang Base64 text.',
                                      'type': 'string'},
         'formats22_tiff_compression': {'attributes': {'name': 'formats22_tiff_compression'},
                                        'target': 'Lossless compression (Deflate)',
                                        'type': 'string'},
         'formats22_tiff_description': {'attributes': {'name': 'formats22_tiff_description'},
                                        'target': 'Nagse-save ng isang RGB page. Maaaring bawasan ng compression '
                                                  'ang laki ng file nang hindi binabago ang pixels; i-off ito '
                                                  'para sa uncompressed TIFF.',
                                        'type': 'string'},
         'gallery_copy_credit': {'attributes': {'formatted': 'false', 'name': 'gallery_copy_credit'},
                                 'target': 'Kopyahin ang pagkilala',
                                 'type': 'string'},
         'gallery_credit_copied': {'attributes': {'name': 'gallery_credit_copied'},
                                   'target': 'Nakopya ang credit',
                                   'type': 'string'},
         'gallery_credit_edit_hint': {'attributes': {'name': 'gallery_credit_edit_hint'},
                                      'target': 'Bago mag-publish, panatilihin ang anumang nakapangalan na '
                                                'creator o copyright notice at magdagdag ng paglalarawan ng mga '
                                                'pagbabagong ginawa mo. Alisin ang mga source na wala sa '
                                                'inilathalang larawan. Mae-edit ang teksto sa ibaba.',
                                      'type': 'string'},
         'gallery_credit_gallery': {'attributes': {'name': 'gallery_credit_gallery'},
                                    'target': 'Gallery: %1$s',
                                    'type': 'string'},
         'gallery_credit_licence': {'attributes': {'name': 'gallery_credit_licence'},
                                    'target': 'Orihinal na artwork ng Catrobat: CC BY-SA 4.0 — %1$s',
                                    'type': 'string'},
         'gallery_credit_publisher': {'attributes': {'name': 'gallery_credit_publisher'},
                                      'target': 'Publisher: Catrobat project',
                                      'type': 'string'},
         'gallery_credit_saved': {'attributes': {'name': 'gallery_credit_saved'},
                                  'target': 'Na-save ang teksto ng credit',
                                  'type': 'string'},
         'gallery_credit_source': {'attributes': {'name': 'gallery_credit_source'},
                                   'target': 'Source: %1$s',
                                   'type': 'string'},
         'gallery_credit_title': {'attributes': {'name': 'gallery_credit_title'},
                                  'target': 'Artwork: %1$s',
                                  'type': 'string'},
         'gallery_description': {'attributes': {'name': 'gallery_description'},
                                 'target': 'I-tap ang Gamitin ang larawan para agad itong ipasok. Ang Kopyahin '
                                           'ang pagkilala sa tabi ng larawan ay kumokopya ng pamagat, publisher, '
                                           'source at lisensiya para sa paglalathala mo. CC BY-SA 4.0 ang '
                                           'orihinal na artwork ng Catrobat; panatilihin ang anumang hiwalay na '
                                           'nakapangalan na creator, copyright at iba pang abiso ng source. '
                                           'Ilarawan ang mga binago mo at ibahagi ang adaptasyon sa ilalim ng CC '
                                           'BY-SA 4.0 o compatible na lisensiya. Hinahayaan ka ng I-edit ang mga '
                                           'credit na idagdag ang mga detalyeng ito; nananatili ang mga naipasok '
                                           'na source sa File → Tungkol, mga lisensiya at pagkilala → Mga credit '
                                           'ng larawan.',
                                 'type': 'string'},
         'gallery_edit_credits': {'attributes': {'name': 'gallery_edit_credits'},
                                  'target': 'I-edit ang mga credit',
                                  'type': 'string'},
         'gallery_external_link_no_handler': {'attributes': {'name': 'gallery_external_link_no_handler'},
                                              'target': 'Hindi nakahanap ang Android ng app para buksan ang link '
                                                        'na ito.',
                                              'type': 'string'},
         'gallery_image_component_unavailable': {'attributes': {'name': 'gallery_image_component_unavailable'},
                                                 'target': 'Hindi magagamit ang isang kinakailangang bahagi para '
                                                           'sa pagproseso ng larawan. Hindi na-import ang '
                                                           'larawan.',
                                                 'type': 'string'},
         'gallery_use_image': {'attributes': {'formatted': 'false', 'name': 'gallery_use_image'},
                               'target': 'Gamitin ang larawan',
                               'type': 'string'},
         'legacy_credits_add': {'attributes': {'name': 'legacy_credits_add'},
                                'target': 'Idagdag ang napiling credit sa larawang ito',
                                'type': 'string'},
         'legacy_credits_added': {'attributes': {'name': 'legacy_credits_added'},
                                  'target': 'Naidagdag ang credit sa larawang ito.',
                                  'type': 'string'},
         'legacy_credits_existing': {'attributes': {'name': 'legacy_credits_existing'},
                                     'target': 'May credit na ang larawang ito para sa source na iyon. Pinanatili '
                                               'ang teksto nito.',
                                     'type': 'string'},
         'legacy_credits_hint': {'attributes': {'name': 'legacy_credits_hint'},
                                 'target': 'Na-save ang mga credit na ito noon at maaaring para sa ibang larawan. '
                                           'Pumili ng source upang idagdag ang credit nito sa larawang ito, o '
                                           'i-save ang buong teksto nito bilang file.',
                                 'type': 'string'},
         'legacy_credits_save_text': {'attributes': {'name': 'legacy_credits_save_text'},
                                      'target': 'I-save ang napiling credit bilang teksto',
                                      'type': 'string'},
         'legacy_credits_title': {'attributes': {'name': 'legacy_credits_title'},
                                  'target': 'Mga dating na-save na credit',
                                  'type': 'string'},
         'save20_bmp_description': {'attributes': {'name': 'save20_bmp_description'},
                                    'target': 'Uncompressed 24-bit RGB; eksaktong kulay, mas malaking file.',
                                    'type': 'string'},
         'save20_bmp_size_limit': {'attributes': {'name': 'save20_bmp_size_limit'},
                                   'target': 'Lumampas ang larawan sa limitasyon ng laki ng BMP file.',
                                   'type': 'string'},
         'save20_gif_size_limit': {'attributes': {'name': 'save20_gif_size_limit'},
                                   'target': 'Hindi maaaring lumampas sa 65,535 pixels bawat side ang sukat ng '
                                             'GIF.',
                                   'type': 'string'},
         'save20_unsupported_tagged_colour': {'attributes': {'name': 'save20_unsupported_tagged_colour'},
                                              'target': 'Gumagamit ang BMP o GIF na ito ng color profile na hindi '
                                                        'pa ma-convert ng AN Paint. I-convert muna ito sa sRGB '
                                                        'PNG sa color-managed editor bago i-import.',
                                              'type': 'string'},
         'ui_aa_bb_0123': {'attributes': {'name': 'ui_aa_bb_0123'},
                           'target': 'Aa Bb 0123 · あいう',
                           'type': 'string'},
         'ui_about_copyright': {'attributes': {'name': 'ui_about_copyright'},
                                'target': 'Tungkol at copyright',
                                'type': 'string'},
         'ui_about_copyright_licence': {'attributes': {'name': 'ui_about_copyright_licence'},
                                        'target': 'Tungkol, copyright at lisensiya',
                                        'type': 'string'},
         'ui_about_credits23': {'attributes': {'formatted': 'false', 'name': 'ui_about_credits23'},
                                'target': 'Tungkol, mga lisensiya at pagkilala',
                                'type': 'string'},
         'ui_add_active23': {'attributes': {'name': 'ui_add_active23'},
                             'target': 'Idagdag ang aktibong kulay',
                             'type': 'string'},
         'ui_add_images': {'attributes': {'name': 'ui_add_images'},
                           'target': 'Magdagdag ng mga larawan',
                           'type': 'string'},
         'ui_add_images_first': {'attributes': {'name': 'ui_add_images_first'},
                                 'target': 'Magdagdag muna ng mga larawan.',
                                 'type': 'string'},
         'ui_add_images_then_drag_a_thumbnail_here': {'attributes': {'name': 'ui_add_images_then_drag_a_thumbnail_here'},
                                                      'target': 'Magdagdag ng mga larawan, saka i-drag ang '
                                                                'thumbnail dito',
                                                      'type': 'string'},
         'ui_add_palette23': {'attributes': {'name': 'ui_add_palette23'},
                              'target': 'Idagdag sa paleta',
                              'type': 'string'},
         'ui_add_to_custom_colours': {'attributes': {'name': 'ui_add_to_custom_colours'},
                                      'target': 'Idagdag sa mga pasadyang kulay',
                                      'type': 'string'},
         'ui_add_up_to_20_images_with_android_s': {'attributes': {'name': 'ui_add_up_to_20_images_with_android_s'},
                                                   'target': 'Magdagdag ng hanggang 20 larawan gamit ang file '
                                                             'picker ng Android. Ipinapakita ng tray sa ibaba ang '
                                                             'mga thumbnail, pangalan ng file, sukat ng larawan '
                                                             'pagkatapos i-crop at pagkatapos ng anumang '
                                                             'pagsasaayos gamit ang Parehong lapad o Parehong '
                                                             'taas, at oras ng pagbabago ng file kapag ibinibigay '
                                                             'ng provider. Ayusin ayon sa pangalan ng file o oras '
                                                             'ng pagbabago; hindi muling inaayos ng sorting ang '
                                                             'mga larawang nailagay na.\\n\\nI-tap ang thumbnail '
                                                             'para piliin ito. Ang I-crop ang larawan ay '
                                                             'nagki-crop sa larawang iyon; ang Maramihang crop ay '
                                                             'naglalapat ng margin na pixel o porsiyento sa mga '
                                                             'napiling larawan. I-drag ang mga crop handle o '
                                                             'mag-type ng halaga. Gamitin ang I-reset ang crop '
                                                             'upang maibalik ang orihinal na mga gilid. Hindi '
                                                             'sinisira ng cropping ang pinagmulan at maaari itong '
                                                             'i-undo.\\n\\nPindutin nang matagal ang thumbnail, o '
                                                             'i-drag ang larawang nasa workspace na, saka ihulog '
                                                             'ito sa naka-highlight na gilid. Ipinapakita ng '
                                                             'translucent na preview ang eksaktong resulta ng '
                                                             'pagkakabit. Ang pagkakabit sa kanan ay nagpapantay '
                                                             'sa mga gilid sa itaas; ang pagkakabit sa ibaba ay '
                                                             'nagpapantay sa mga kaliwang gilid. Maaari ring '
                                                             'i-tap ang thumbnail at pagkatapos ang + target. '
                                                             'Kapag ikinakabit sa target, nagsisimula ang unang '
                                                             'larawan sa origin. Maaaring gumalaw ang mga '
                                                             'nakakabit na larawan kapag kino-crop ang larawang '
                                                             'pinagkakabitan ng mga ito. Hindi pinapayagan ang '
                                                             'overlap kapag ikinakabit sa target ang '
                                                             'larawan.\\n\\nPumili ng larawan at gamitin ang '
                                                             'Eksaktong posisyon upang itakda ang mga X/Y '
                                                             'coordinate ng kaliwang itaas na sulok nito sa mga '
                                                             'buong bilang ng pixel, simula sa zero. Nananatili '
                                                             'sa kanilang mga posisyon ang ibang mga larawan, at '
                                                             'pinapayagan ang overlap.\\n\\nAng Parehong lapad at '
                                                             'Parehong taas ay nagbibigay sa lahat ng input ng '
                                                             'iisang sukat habang pinananatili ang sariling '
                                                             'aspect ratio ng bawat larawan. Pumili ng Pixels, '
                                                             'Porsiyento, Pinakamaliit o Pinakamalaki. Inaalis ng '
                                                             'Ibalik ang orihinal na laki ang normalization '
                                                             'ngunit pinananatili ang mga crop.\\n\\nIbalik sa '
                                                             'tray ang napiling larawan lamang gamit ang Alisin '
                                                             'sa puwesto. Nananatiling nakapuwesto ang ibang mga '
                                                             'larawan; maaaring gumalaw ang mga nakakabit na '
                                                             'larawan upang punan ang puwang. Ang Alisin ay '
                                                             'nagtatanggal lamang ng input na iyon. Gamit ang '
                                                             'Ibalik/Ulitin, maaaring bawiin o ulitin ang mga '
                                                             'pagbabagong ito. I-drag ang nakapuwestong larawan '
                                                             'para muling ayusin ito; i-drag sa bakanteng espasyo '
                                                             'para mag-pan. Kurutin para mag-zoom. Inaayos ng '
                                                             'Ipakita lahat ang zoom upang makita ang buong '
                                                             'pagsasama; hindi nito kailanman binabago ang mga '
                                                             'sukat ng output.\\n\\nDirektang sine-save ng I-save '
                                                             'ang PNG ang pinagsamang larawan. Inililipat ito ng '
                                                             'I-edit sa Paint sa pangunahing editor bilang '
                                                             'pagpapalit na maaaring i-undo. Kung lumampas ang '
                                                             'output sa limitasyon ng memory, pumili ng mas '
                                                             'maliit na kopya ng output kung may iniaalok. Kung '
                                                             'kahit ang napakaliit na output ay lumampas sa '
                                                             'limitasyon, magpapakita ang app ng babala tungkol '
                                                             'sa memory sa halip na pagpipilian ng laki. Hindi '
                                                             'nagbabago ang mga orihinal na source file. Lokal na '
                                                             'sine-save ang kasalukuyang pagsasama at muling '
                                                             'bubuksan kapag bumalik ka.\\n\\nGinagamit ng mode '
                                                             'na ito ang parehong Catrobat/AGPL at mga credit ng '
                                                             'asset na nasa panel na «File > Tungkol, mga '
                                                             'lisensiya at pagkilala» ng pangunahing editor.',
                                                   'type': 'string'},
         'ui_added_palette23': {'attributes': {'name': 'ui_added_palette23'},
                                'target': 'Idinagdag sa paleta',
                                'type': 'string'},
         'ui_advanced': {'attributes': {'formatted': 'false', 'name': 'ui_advanced'},
                         'target': 'Mas maraming opsiyon',
                         'type': 'string'},
         'ui_agpl_licence': {'attributes': {'name': 'ui_agpl_licence'},
                             'target': 'Lisensiyang AGPL',
                             'type': 'string'},
         'ui_an_assembly_can_contain_up_to_20_images': {'attributes': {'name': 'ui_an_assembly_can_contain_up_to_20_images'},
                                                        'target': 'Ang isang pagsasama ay maaaring maglaman ng '
                                                                  'hanggang 20 larawan. Mag-alis ng larawan para '
                                                                  'makapagdagdag ng iba.',
                                                        'type': 'string'},
         'ui_an_assembly_can_contain_up_to_20_images_86d995': {'attributes': {'name': 'ui_an_assembly_can_contain_up_to_20_images_86d995'},
                                                               'target': 'Ang isang pagsasama ay maaaring '
                                                                         'maglaman ng hanggang 20 larawan.',
                                                               'type': 'string'},
         'ui_an_image_cannot_attach_to_itself_or_one': {'attributes': {'name': 'ui_an_image_cannot_attach_to_itself_or_one'},
                                                        'target': 'Hindi maaaring ikabit ang isang larawan sa '
                                                                  'sarili nito o sa isa sa mga larawang nakakabit '
                                                                  'dito.',
                                                        'type': 'string'},
         'ui_an_paint_assembly_image': {'attributes': {'name': 'ui_an_paint_assembly_image'},
                                        'target': 'Pinagsamang larawan ng AN Paint',
                                        'type': 'string'},
         'ui_an_paint_image': {'attributes': {'name': 'ui_an_paint_image'},
                               'target': 'Larawan ng AN Paint',
                               'type': 'string'},
         'ui_an_paint_image_assembly': {'attributes': {'name': 'ui_an_paint_image_assembly'},
                                        'target': 'AN Paint · Pagsasama ng larawan',
                                        'type': 'string'},
         'ui_an_paint_image_assembly_20_images_placed': {'attributes': {'name': 'ui_an_paint_image_assembly_20_images_placed'},
                                                         'target': 'AN Paint · Pagsasama ng larawan\\n%1$s/20 '
                                                                   'larawan · %2$s nakapuwesto',
                                                         'type': 'string'},
         'ui_apply_to_all': {'attributes': {'name': 'ui_apply_to_all'},
                             'target': 'Ilapat sa lahat',
                             'type': 'string'},
         'ui_apply_to_these_images': {'attributes': {'name': 'ui_apply_to_these_images'},
                                      'target': 'Ilapat sa mga larawang ito',
                                      'type': 'string'},
         'ui_assembly_decoded_output_estimated_editing_render_memory_at': {'attributes': {'name': 'ui_assembly_decoded_output_estimated_editing_render_memory_at'},
                                                                           'target': 'Pagsasama: %1$s\\nNa-decode '
                                                                                     'na output: '
                                                                                     '%2$s\\nTinatayang memory '
                                                                                     'para sa pag-edit/render sa '
                                                                                     'orihinal na laki: %3$s',
                                                                           'type': 'string'},
         'ui_assembly_exact_position': {'attributes': {'name': 'ui_assembly_exact_position'},
                                        'target': 'Eksaktong posisyon',
                                        'type': 'string'},
         'ui_assembly_output_size': {'attributes': {'name': 'ui_assembly_output_size'},
                                     'target': 'Laki ng output ng pagsasama',
                                     'type': 'string'},
         'ui_assembly_png': {'attributes': {'name': 'ui_assembly_png'},
                             'target': 'Pagsasama.png',
                             'type': 'string'},
         'ui_assembly_position_help': {'attributes': {'name': 'ui_assembly_position_help'},
                                       'target': 'Itakda ang posisyon ng kaliwang sulok sa itaas ng larawang ito '
                                                 'sa output canvas. Ang X at Y ay mga buong bilang ng pixel, '
                                                 'simula sa zero. Mananatili sa kasalukuyang posisyon ang ibang '
                                                 'mga larawan. Pinapayagan dito ang pagpapatong; ang mga larawang '
                                                 'na-import nang mas huli ay iguguhit sa ibabaw. Lalawak ang '
                                                 'canvas upang magkasya ang lahat ng nakapuwestong larawan. Hindi '
                                                 'magbabago ang mga crop at laki.',
                                       'type': 'string'},
         'ui_assembly_position_nonnegative': {'attributes': {'name': 'ui_assembly_position_nonnegative'},
                                              'target': 'Ang X at Y ay dapat na mga buong bilang mula 0 hanggang '
                                                        '2147483647.',
                                              'type': 'string'},
         'ui_assembly_target_x': {'attributes': {'name': 'ui_assembly_target_x'},
                                  'target': 'Posisyon X (mga pixel mula sa kaliwa)',
                                  'type': 'string'},
         'ui_assembly_target_y': {'attributes': {'name': 'ui_assembly_target_y'},
                                  'target': 'Posisyon Y (mga pixel mula sa itaas)',
                                  'type': 'string'},
         'ui_assembly_unknown_image': {'attributes': {'name': 'ui_assembly_unknown_image'},
                                       'target': 'Wala na sa pagsasamang ito ang napiling larawan.',
                                       'type': 'string'},
         'ui_batch_crop': {'attributes': {'name': 'ui_batch_crop'}, 'target': 'Maramihang crop', 'type': 'string'},
         'ui_batch_crop_images': {'attributes': {'name': 'ui_batch_crop_images'},
                                  'target': 'I-batch crop ang mga larawan',
                                  'type': 'string'},
         'ui_bottom23': {'attributes': {'name': 'ui_bottom23'}, 'target': 'Naka-align sa ibaba', 'type': 'string'},
         'ui_by_pixels_hold_and_drag_to_place': {'attributes': {'name': 'ui_by_pixels_hold_and_drag_to_place'},
                                                 'target': '%1$s. %2$s. %3$s × %4$s pixel. Pindutin nang matagal '
                                                           'at i-drag upang ilagay.',
                                                 'type': 'string'},
         'ui_calligraphy': {'attributes': {'name': 'ui_calligraphy'}, 'target': 'Kaligrapiya', 'type': 'string'},
         'ui_casual': {'attributes': {'name': 'ui_casual'}, 'target': 'Kaswal', 'type': 'string'},
         'ui_catrobat_online_gallery_artwork_by_its_credited_creators': {'attributes': {'name': 'ui_catrobat_online_gallery_artwork_by_its_credited_creators'},
                                                                         'target': 'Online gallery ng Catrobat · '
                                                                                   'mga likhang gawa ng mga '
                                                                                   'nakatalang creator',
                                                                         'type': 'string'},
         'ui_catrobat_s_own_artwork_uses_cc_by_sa': {'attributes': {'name': 'ui_catrobat_s_own_artwork_uses_cc_by_sa'},
                                                     'target': 'Gumagamit ng CC BY-SA 4.0 ang sariling artwork ng '
                                                               'Catrobat. Panatilihin ang credit ng creator at '
                                                               'ibahagi ang mga adaptasyon sa ilalim ng '
                                                               'lisensiyang iyon. Tingnan ang source page para sa '
                                                               'anumang hiwalay na attribution. Itatabi ang '
                                                               'source URL sa File > Tungkol, mga lisensiya at '
                                                               'pagkilala > Mga credit ng larawan.',
                                                     'type': 'string'},
         'ui_catrobat_sticker_gallery': {'attributes': {'formatted': 'false',
                                                        'name': 'ui_catrobat_sticker_gallery'},
                                         'target': 'Galerya ng mga sticker ng Catrobat…',
                                         'type': 'string'},
         'ui_close_polygon': {'attributes': {'name': 'ui_close_polygon'},
                              'target': 'Isara ang polygon',
                              'type': 'string'},
         'ui_colour_blue_range': {'attributes': {'name': 'ui_colour_blue_range'},
                                  'target': 'B · 0–255',
                                  'type': 'string'},
         'ui_colour_component_range': {'attributes': {'name': 'ui_colour_component_range'},
                                       'target': '0–%1$d',
                                       'type': 'string'},
         'ui_colour_green_range': {'attributes': {'name': 'ui_colour_green_range'},
                                   'target': 'G · 0–255',
                                   'type': 'string'},
         'ui_colour_hsl_hue_range': {'attributes': {'name': 'ui_colour_hsl_hue_range'},
                                     'target': 'HSL H · 0–360°',
                                     'type': 'string'},
         'ui_colour_hsl_lightness_range': {'attributes': {'formatted': 'false',
                                                          'name': 'ui_colour_hsl_lightness_range'},
                                           'target': 'HSL L · 0–100%',
                                           'type': 'string'},
         'ui_colour_hsl_saturation_range': {'attributes': {'formatted': 'false',
                                                           'name': 'ui_colour_hsl_saturation_range'},
                                            'target': 'HSL S · 0–100%',
                                            'type': 'string'},
         'ui_colour_hsv_hue_range': {'attributes': {'name': 'ui_colour_hsv_hue_range'},
                                     'target': 'HSV H · 0–360°',
                                     'type': 'string'},
         'ui_colour_hsv_saturation_range': {'attributes': {'formatted': 'false',
                                                           'name': 'ui_colour_hsv_saturation_range'},
                                            'target': 'HSV S · 0–100%',
                                            'type': 'string'},
         'ui_colour_hsv_value_range': {'attributes': {'formatted': 'false', 'name': 'ui_colour_hsv_value_range'},
                                       'target': 'HSV V · 0–100%',
                                       'type': 'string'},
         'ui_colour_red_range': {'attributes': {'name': 'ui_colour_red_range'},
                                 'target': 'R · 0–255',
                                 'type': 'string'},
         'ui_common_in': {'attributes': {'name': 'ui_common_in'},
                          'target': 'Parehong %1$s sa %2$s',
                          'type': 'string'},
         'ui_common_in_pixels': {'attributes': {'name': 'ui_common_in_pixels'},
                                 'target': 'Parehong %1$s sa pixels',
                                 'type': 'string'},
         'ui_copper': {'attributes': {'name': 'ui_copper'}, 'target': 'Tanso', 'type': 'string'},
         'ui_copy_an_area_or_use_file_insert_image': {'attributes': {'name': 'ui_copy_an_area_or_use_file_insert_image'},
                                                      'target': 'Kopyahin ang isang bahagi o gamitin ang Gumuhit '
                                                                '→ Ipasok → Iba pang larawan.',
                                                      'type': 'string'},
         'ui_copy_decoded_image_at_this_size_estimated_loading': {'attributes': {'name': 'ui_copy_decoded_image_at_this_size_estimated_loading'},
                                                                  'target': 'Kopya: %1$s\\nNa-decode na larawan '
                                                                            'sa laking ito: %2$s\\nTinatayang '
                                                                            'memory para sa pag-load/pag-edit: '
                                                                            '%3$s\\n',
                                                                  'type': 'string'},
         'ui_corners_and_edges_resize_round_handle_rotates': {'attributes': {'name': 'ui_corners_and_edges_resize_round_handle_rotates'},
                                                              'target': 'Binabago ng mga sulok at gilid ang laki. '
                                                                        'Ang bilog na handle ay umiikot.',
                                                              'type': 'string'},
         'ui_could_not_create_the_assembly': {'attributes': {'name': 'ui_could_not_create_the_assembly'},
                                              'target': 'Hindi makagawa ng pagsasama: %1$s',
                                              'type': 'string'},
         'ui_could_not_decode_the_cropped_region_of': {'attributes': {'name': 'ui_could_not_decode_the_cropped_region_of'},
                                                       'target': 'Hindi ma-decode ang na-crop na bahagi ng %1$s.',
                                                       'type': 'string'},
         'ui_could_not_export_source_code': {'attributes': {'name': 'ui_could_not_export_source_code'},
                                             'target': 'Hindi ma-export ang source code',
                                             'type': 'string'},
         'ui_could_not_load_gallery_image': {'attributes': {'name': 'ui_could_not_load_gallery_image'},
                                             'target': 'Hindi ma-load ang larawan sa gallery: %1$s',
                                             'type': 'string'},
         'ui_create_output': {'attributes': {'name': 'ui_create_output'},
                              'target': 'Gumawa ng output',
                              'type': 'string'},
         'ui_creator_on_source34': {'attributes': {'name': 'ui_creator_on_source34'},
                                    'target': 'Tingnan ang source page para sa contributor.',
                                    'type': 'string'},
         'ui_credits_terms': {'attributes': {'name': 'ui_credits_terms'},
                              'target': 'Mga credit at tuntunin',
                              'type': 'string'},
         'ui_cropped_thumbnail': {'attributes': {'name': 'ui_cropped_thumbnail'},
                                  'target': 'Na-crop na thumbnail: %1$s',
                                  'type': 'string'},
         'ui_current_safe_budget_2f_mp': {'attributes': {'name': 'ui_current_safe_budget_2f_mp'},
                                          'target': 'Kasalukuyang ligtas na limitasyon: %1$.2f MP.',
                                          'type': 'string'},
         'ui_current_safe_editing_budget_s_up_to_2f': {'attributes': {'name': 'ui_current_safe_editing_budget_s_up_to_2f'},
                                                       'target': 'Kasalukuyang ligtas na limitasyon sa pag-edit: '
                                                                 '%1$s · hanggang %2$.2f MP bago ang dagdag na '
                                                                 'gamit ng decoder',
                                                       'type': 'string'},
         'ui_cursive': {'attributes': {'name': 'ui_cursive'}, 'target': 'Kursibo', 'type': 'string'},
         'ui_cursor_drawing32': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_drawing32'},
                                 'target': 'Pagguhit gamit ang cursor',
                                 'type': 'string'},
         'ui_cursor_help29': {'attributes': {'name': 'ui_cursor_help29'},
                              'target': '@string/ui_cursor_help31',
                              'type': 'string'},
         'ui_cursor_help31': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_help31'},
                              'target': 'I-drag para ipuwesto ang cursor. I-tap ang button sa screen para sa '
                                        'pagguhit, saka i-drag para gumuhit. I-tap muli para huminto. Piliin ang '
                                        'brush at mga setting ng stroke sa Gumuhit → Pagguhit.',
                              'type': 'string'},
         'ui_cursor_ink30': {'attributes': {'name': 'ui_cursor_ink30'},
                             'target': 'Gumuhit gamit ang cursor',
                             'type': 'string'},
         'ui_cursor_marker_help31': {'attributes': {'name': 'ui_cursor_marker_help31'},
                                     'target': 'Pinapalaki ang cursor marker nang hindi binabago ang laki ng '
                                               'brush na ipinipinta.',
                                     'type': 'string'},
         'ui_cursor_marker_size31': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_marker_size31'},
                                     'target': 'Laki ng cursor marker (%)',
                                     'type': 'string'},
         'ui_cursor_pan_draw32': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_pan_draw32'},
                                  'target': 'I-drag para gumuhit. I-tap muli para tumigil sa pagguhit.',
                                  'type': 'string'},
         'ui_cursor_pan_move32': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_pan_move32'},
                                  'target': 'I-drag para ipuwesto ang cursor. I-tap ang pindutan ng pagguhit para '
                                            'magsimulang gumuhit.',
                                  'type': 'string'},
         'ui_cursor_position26': {'attributes': {'name': 'ui_cursor_position26'},
                                  'target': 'x: %1$d, y: %2$d',
                                  'type': 'string'},
         'ui_cursor_settings31': {'attributes': {'name': 'ui_cursor_settings31'},
                                  'target': 'Mga setting ng pagguhit gamit ang cursor…',
                                  'type': 'string'},
         'ui_cursor_shape31': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_shape31'},
                               'target': 'Hugis ng cursor',
                               'type': 'string'},
         'ui_cursor_start31': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_start31'},
                               'target': 'Simulang gumuhit',
                               'type': 'string'},
         'ui_cursor_stop31': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_stop31'},
                              'target': 'Itigil ang pagguhit',
                              'type': 'string'},
         'ui_cursor_tap_hint37': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_tap_hint37'},
                                  'target': 'I-tap ang cursor para simulan o ihinto ang pagguhit.',
                                  'type': 'string'},
         'ui_custom_colour': {'attributes': {'name': 'ui_custom_colour'},
                              'target': 'Pasadyang kulay %1$s',
                              'type': 'string'},
         'ui_custom_colours_hold_a_swatch_to_replace_it': {'attributes': {'name': 'ui_custom_colours_hold_a_swatch_to_replace_it'},
                                                           'target': 'Mga pasadyang kulay · pindutin nang matagal '
                                                                     'ang swatch para palitan ito',
                                                           'type': 'string'},
         'ui_disable_cursor_drawing': {'attributes': {'name': 'ui_disable_cursor_drawing'},
                                       'target': 'I-disable ang pagguhit gamit ang cursor',
                                       'type': 'string'},
         'ui_disable_cursor_drawing33': {'attributes': {'formatted': 'false',
                                                        'name': 'ui_disable_cursor_drawing33'},
                                         'target': 'I-disable ang pagguhit gamit ang cursor',
                                         'type': 'string'},
         'ui_downloading_image': {'attributes': {'name': 'ui_downloading_image'},
                                  'target': 'Dina-download ang larawan…',
                                  'type': 'string'},
         'ui_drag_a_line_then_drag_twice_to_set': {'attributes': {'name': 'ui_drag_a_line_then_drag_twice_to_set'},
                                                   'target': 'I-drag ang isang linya, pagkatapos ay i-drag nang '
                                                             'dalawang beses upang itakda ang dalawang liko nito. '
                                                             'Ilapat agad gamit ang Tapusin ang kurba.',
                                                   'type': 'string'},
         'ui_drag_a_selection_drag_inside_to_move_square': {'attributes': {'name': 'ui_drag_a_selection_drag_inside_to_move_square'},
                                                            'target': 'I-drag ang isang selection. I-drag ang '
                                                                      'loob para ilipat, ang parisukat na sulok o '
                                                                      'edge handle para baguhin ang laki, o ang '
                                                                      'bilog na handle para paikutin. '
                                                                      'Pinananatili ng I-lock ang proporsyon ang '
                                                                      'hugis nito.',
                                                            'type': 'string'},
         'ui_drag_across_the_ellipse_s_bounding_box': {'attributes': {'name': 'ui_drag_across_the_ellipse_s_bounding_box'},
                                                       'target': 'I-drag sa bounding box ng ellipse.',
                                                       'type': 'string'},
         'ui_drag_between_opposite_corners_choose_outline_or_fill': {'attributes': {'name': 'ui_drag_between_opposite_corners_choose_outline_or_fill'},
                                                                     'target': 'I-drag sa pagitan ng magkatapat '
                                                                               'na sulok. Piliin ang outline o '
                                                                               'fill sa ibaba.',
                                                                     'type': 'string'},
         'ui_drag_between_opposite_corners_to_draw_a_five': {'attributes': {'name': 'ui_drag_between_opposite_corners_to_draw_a_five'},
                                                             'target': 'I-drag sa pagitan ng magkatapat na sulok '
                                                                       'upang gumuhit ng bituing may limang '
                                                                       'tulis. Piliin ang outline o fill.',
                                                             'type': 'string'},
         'ui_drag_between_opposite_corners_to_draw_a_heart': {'attributes': {'name': 'ui_drag_between_opposite_corners_to_draw_a_heart'},
                                                              'target': 'I-drag sa pagitan ng magkatapat na sulok '
                                                                        'upang gumuhit ng puso. Piliin ang '
                                                                        'outline o fill.',
                                                              'type': 'string'},
         'ui_drag_from_the_start_to_the_end_of': {'attributes': {'name': 'ui_drag_from_the_start_to_the_end_of'},
                                                  'target': 'I-drag mula simula hanggang dulo ng linya.',
                                                  'type': 'string'},
         'ui_drag_from_the_tail_towards_the_arrowhead_choose': {'attributes': {'name': 'ui_drag_from_the_tail_towards_the_arrowhead_choose'},
                                                                'target': 'I-drag mula buntot patungo sa dulo ng '
                                                                          'arrow. Piliin ang outline o fill.',
                                                                'type': 'string'},
         'ui_drag_out_to_expand_in_to_trim_drag': {'attributes': {'name': 'ui_drag_out_to_expand_in_to_trim_drag'},
                                                   'target': 'I-drag palabas para palawakin, papasok para '
                                                             'bawasan. I-drag ang loob para ilipat ang hangganan. '
                                                             'Kurutin o gamitin ang Iangkop para sa mas maraming '
                                                             'espasyo. Pinupuno ng BG ang bagong espasyo.',
                                                   'type': 'string'},
         'ui_drag_placed_images_to_move_them_hold_and': {'attributes': {'name': 'ui_drag_placed_images_to_move_them_hold_and'},
                                                         'target': 'I-drag ang mga nakapuwestong larawan para '
                                                                   'ilipat ang mga ito. Pindutin nang matagal at '
                                                                   'i-drag ang thumbnail para idagdag ito.',
                                                         'type': 'string'},
         'ui_drag_to_erase_with_the_background_colour': {'attributes': {'name': 'ui_drag_to_erase_with_the_background_colour'},
                                                         'target': 'I-drag para magbura gamit ang kulay sa likod.',
                                                         'type': 'string'},
         'ui_drag_to_pan_without_drawing_pinch_with_two': {'attributes': {'name': 'ui_drag_to_pan_without_drawing_pinch_with_two'},
                                                           'target': 'I-drag para mag-pan nang hindi gumuguhit. '
                                                                     'Kurutin gamit ang dalawang daliri para '
                                                                     'mag-zoom at mag-pan. Gumagana rin ang '
                                                                     'two-finger navigation habang gumagamit ng '
                                                                     'drawing tools.',
                                                           'type': 'string'},
         'ui_draw_a_crisp_one_pixel_line': {'attributes': {'name': 'ui_draw_a_crisp_one_pixel_line'},
                                            'target': 'Gumuhit ng malinaw na linya. Isaayos ang Lapad mula 1 '
                                                      'hanggang 100 pixels.',
                                            'type': 'string'},
         'ui_draw_around_an_area_drag_inside_to_move': {'attributes': {'name': 'ui_draw_around_an_area_drag_inside_to_move'},
                                                        'target': 'Gumuhit sa paligid ng isang bahagi. I-drag ang '
                                                                  'loob para ilipat, ang parisukat na sulok o '
                                                                  'edge handle para baguhin ang laki, o ang bilog '
                                                                  'na handle para paikutin. Inilalapat ng Ilapat '
                                                                  'ang napili ang edit.',
                                                        'type': 'string'},
         'ui_draw_soft_watercolor_strokes_strength_controls_how_strongly': {'attributes': {'name': 'ui_draw_soft_watercolor_strokes_strength_controls_how_strongly'},
                                                                            'target': 'Gumuhit ng malalambot na '
                                                                                      'watercolor stroke. '
                                                                                      'Kinokontrol ng Lakas kung '
                                                                                      'gaano kalakas naghahalo '
                                                                                      'ang kulay sa canvas.',
                                                                            'type': 'string'},
         'ui_draw_with_the_selected_brush_tip_and_size': {'attributes': {'name': 'ui_draw_with_the_selected_brush_tip_and_size'},
                                                          'target': 'Gumuhit gamit ang napiling brush tip at '
                                                                    'laki.',
                                                          'type': 'string'},
         'ui_drop_at_a_highlighted_edge_right_top_aligned': {'attributes': {'name': 'ui_drop_at_a_highlighted_edge_right_top_aligned'},
                                                             'target': 'Ihulog sa naka-highlight na gilid: sa '
                                                                       'kanan na pantay ang itaas, o sa ibaba na '
                                                                       'pantay ang kaliwang gilid.',
                                                             'type': 'string'},
         'ui_each_px_px_percent_is_relative_to_the': {'attributes': {'name': 'ui_each_px_px_percent_is_relative_to_the'},
                                                      'target': 'Bawat %1$s: %2$s px\\n%3$s: %4$s–%5$s px\\nAng '
                                                                'porsiyento ay batay sa pinakamalaking '
                                                                'kasalukuyang %6$s: %7$s px. Muling inaayos ang '
                                                                'mga nakapuwestong larawan upang gumawa ng '
                                                                'puwang.',
                                                      'type': 'string'},
         'ui_edit_in_paint': {'attributes': {'name': 'ui_edit_in_paint'},
                              'target': 'I-edit sa Paint',
                              'type': 'string'},
         'ui_edit_palette23': {'attributes': {'name': 'ui_edit_palette23'},
                               'target': 'I-edit ang paleta',
                               'type': 'string'},
         'ui_empty_palette26': {'attributes': {'name': 'ui_empty_palette26'},
                                'target': 'Bakanteng slot ng paleta %1$d — magdagdag ng kulay',
                                'type': 'string'},
         'ui_enable_android_s_files_or_documents_app_then': {'attributes': {'name': 'ui_enable_android_s_files_or_documents_app_then'},
                                                             'target': 'I-enable ang Files o Documents app ng '
                                                                       'Android, saka subukan muli.',
                                                             'type': 'string'},
         'ui_enable_cursor_drawing': {'attributes': {'formatted': 'false', 'name': 'ui_enable_cursor_drawing'},
                                      'target': 'Paganahin ang pagguhit gamit ang cursor',
                                      'type': 'string'},
         'ui_estimated_memory_current_working_budget': {'attributes': {'name': 'ui_estimated_memory_current_working_budget'},
                                                        'target': 'Tinatayang memory: %1$s\\nKasalukuyang working '
                                                                  'limit: %2$s\\n',
                                                        'type': 'string'},
         'ui_estimates_include_the_current_canvas_and_clipboard_sampled': {'attributes': {'name': 'ui_estimates_include_the_current_canvas_and_clipboard_sampled'},
                                                                           'target': 'Kasama sa pagtataya ang '
                                                                                     'kasalukuyang canvas at '
                                                                                     'clipboard, sampled decoding '
                                                                                     'at mga buffer sa pag-edit. '
                                                                                     'Nag-iiba ang aktuwal na '
                                                                                     'paggamit ng memory. '
                                                                                     'Nawawalan ng detalye ang '
                                                                                     'mas maliit na kopya. '
                                                                                     'Ginagamit ng import ang '
                                                                                     'napiling opaque na '
                                                                                     'background; hindi nagbabago '
                                                                                     'ang orihinal na file.',
                                                                           'type': 'string'},
         'ui_export_this_version_s_source_code': {'attributes': {'name': 'ui_export_this_version_s_source_code'},
                                                  'target': 'I-export ang source code ng bersiyong ito…',
                                                  'type': 'string'},
         'ui_filename_a_z': {'attributes': {'name': 'ui_filename_a_z'},
                             'target': 'Pangalan ng file A–Z',
                             'type': 'string'},
         'ui_filename_z_a': {'attributes': {'name': 'ui_filename_z_a'},
                             'target': 'Pangalan ng file Z–A',
                             'type': 'string'},
         'ui_fill_line': {'attributes': {'name': 'ui_fill_line'}, 'target': 'Fill + linya', 'type': 'string'},
         'ui_fill_text_box_with_bg_colour': {'attributes': {'name': 'ui_fill_text_box_with_bg_colour'},
                                             'target': 'Punan ang text box gamit ang BG na kulay',
                                             'type': 'string'},
         'ui_finish_curve': {'attributes': {'name': 'ui_finish_curve'},
                             'target': 'Tapusin ang kurba',
                             'type': 'string'},
         'ui_finish_polygon': {'attributes': {'name': 'ui_finish_polygon'},
                               'target': 'Tapusin ang polygon',
                               'type': 'string'},
         'ui_fits_the_current_budget': {'attributes': {'name': 'ui_fits_the_current_budget'},
                                        'target': 'Pasok sa kasalukuyang limitasyon.',
                                        'type': 'string'},
         'ui_font_licences': {'attributes': {'name': 'ui_font_licences'},
                              'target': 'Mga lisensiya ng font',
                              'type': 'string'},
         'ui_fullscreen33': {'attributes': {'formatted': 'false', 'name': 'ui_fullscreen33'},
                             'target': 'Buong screen',
                             'type': 'string'},
         'ui_gallery_artwork_catrobat_and_its_credited_creators_cc': {'attributes': {'name': 'ui_gallery_artwork_catrobat_and_its_credited_creators_cc'},
                                                                      'target': 'Artwork sa gallery: Catrobat at '
                                                                                'ang mga nakatalang creator nito. '
                                                                                'CC BY-SA 4.0 maliban kung may '
                                                                                'ibang tuntunin ang source. '
                                                                                'I-credit ang artwork at ilarawan '
                                                                                'ang mga binago mo kapag '
                                                                                'nagbabahagi ng adaptasyon.\\n\\n',
                                                                      'type': 'string'},
         'ui_gallery_back34': {'attributes': {'formatted': 'false', 'name': 'ui_gallery_back34'},
                               'target': 'Bumalik',
                               'type': 'string'},
         'ui_gallery_image': {'attributes': {'name': 'ui_gallery_image'},
                              'target': 'Larawan sa gallery',
                              'type': 'string'},
         'ui_gallery_unsupported34': {'attributes': {'name': 'ui_gallery_unsupported34'},
                                      'target': 'Wala ang larawang ito sa napiling source ng illustration.',
                                      'type': 'string'},
         'ui_gimp_translations31': {'attributes': {'name': 'ui_gimp_translations31'},
                                    'target': 'Mga credit at lisensiya ng pagsasalin',
                                    'type': 'string'},
         'ui_give_all_images_the_same_each_image_keeps': {'attributes': {'name': 'ui_give_all_images_the_same_each_image_keeps'},
                                                          'target': 'Bigyan ang lahat ng %1$s larawan ng parehong '
                                                                    '%2$s. Pinananatili ng bawat larawan ang '
                                                                    'sarili nitong aspect ratio. Hindi nagbabago '
                                                                    'ang mga orihinal na file at crop setting.',
                                                          'type': 'string'},
         'ui_gnu_affero_general_public_license': {'attributes': {'name': 'ui_gnu_affero_general_public_license'},
                                                  'target': 'GNU Affero General Public License',
                                                  'type': 'string'},
         'ui_gnu_agpl_licence': {'attributes': {'name': 'ui_gnu_agpl_licence'},
                                 'target': 'Lisensiyang GNU AGPL',
                                 'type': 'string'},
         'ui_gold': {'attributes': {'name': 'ui_gold'}, 'target': 'Ginto', 'type': 'string'},
         'ui_heic_avif_codec_licences': {'attributes': {'name': 'ui_heic_avif_codec_licences'},
                                         'target': 'Mga lisensiya ng HEIC at AVIF codec',
                                         'type': 'string'},
         'ui_help23': {'attributes': {'name': 'ui_help23'},
                       'target': 'Pumili ng tab para ipakita ang mga control nito. Nagsisimula ang Tingnan sa '
                                 'Ilipat at i-zoom; nasa Gumuhit ang Pagguhit, Pagpili at Ipasok. Nagpa-pan ang '
                                 'Ilipat at i-zoom nang hindi gumuguhit; kurutin gamit ang dalawang daliri para '
                                 'mag-zoom. Kino-collapse ng arrow sa tabi ng mga tab ang panel. May label ang '
                                 'lahat ng tool. Binabago ng I-edit ang selection, hangganan ng canvas, sukat o '
                                 'larawan. Pinipili ng Mga kulay ang kulay sa harap at likod; pinagpapalit sila '
                                 'ng Pagpalitin ang mga kulay at nire-reset sila ng Itim / puti. Agad na '
                                 'pine-preview ng color picker ang pinili mo. Kinukumpirma ito ng Gamitin ang '
                                 'kulay; ibinabalik ng Kanselahin ang dating kulay. Magdagdag ng kulay o i-tap '
                                 'ang bakanteng saved slot para pumili at mag-save ng kulay. Pindutin nang '
                                 'matagal ang saved color para i-edit o alisin. Binubuksan ng Mas maraming '
                                 'opsiyon ang detalyadong editor sa tabi ng Itim / puti. Ipinapakita rin ng pixel '
                                 'grid ang image-pixel ruler; ipinapakita ng pagguhit gamit ang cursor ang live '
                                 'x/y sa tabi ng zoom. Pinipili ng I-save bilang ang format ng larawan, '
                                 'compression setting at lokasyon; muling nagsusulat doon ang I-save gamit ang '
                                 'mga setting na iyon. Gumagawa ang I-export bilang ng ICO, ASCII art o Base64 '
                                 'text nang hindi minamarkahan ang drawing bilang saved. Nagse-save ng kopya ang '
                                 'I-save at ibahagi, saka binubuksan ang Android sharing. Hindi nagbabago ang '
                                 'kasalukuyang destinasyon ng I-save. Nasa Gumuhit > Ipasok > Iba pang larawan '
                                 'ang mga file sa device, Catrobat, Irasutoya, Openclipart at “Wikimedia Commons '
                                 '· Mga blangkong mapa…”. Nananatiling napili ang mga naipasok na larawan; '
                                 'ipinapakita ng view ang mga handle nito kahit nasa labas ng canvas. Binabago ng '
                                 'Iangkop ang larawan sa canvas ang placement; ibinabalik ng Orihinal na laki ang '
                                 'source dimensions. Ibinabalik ng autosave ang draft at parehong undo/redo stack '
                                 'kapag binuksan mo muli ang app. Nasa File din ang pagsasama ng larawan, Paano '
                                 'gamitin, at Tungkol, mga lisensiya at pagkilala. Sinusuportahan ng Magpasok ng '
                                 'teksto ang pahalang at vertical na pagsulat.',
                       'type': 'string'},
         'ui_hide_pixel_grid_800': {'attributes': {'formatted': 'false', 'name': 'ui_hide_pixel_grid_800'},
                                    'target': 'Itago ang grid ng pixel (800% pataas)',
                                    'type': 'string'},
         'ui_hold_a_thumbnail_and_drag_it_here_or': {'attributes': {'name': 'ui_hold_a_thumbnail_and_drag_it_here_or'},
                                                     'target': 'Pindutin nang matagal ang thumbnail at i-drag '
                                                               'dito, o i-tap ito saka i-tap ang workspace.',
                                                     'type': 'string'},
         'ui_hold_or_drag_to_spray_colour': {'attributes': {'name': 'ui_hold_or_drag_to_spray_colour'},
                                             'target': 'Pindutin nang matagal o i-drag para mag-spray ng kulay.',
                                             'type': 'string'},
         'ui_honeycomb': {'attributes': {'name': 'ui_honeycomb'}, 'target': 'Bahay-pukyutan', 'type': 'string'},
         'ui_honeycomb_colour_06x': {'attributes': {'name': 'ui_honeycomb_colour_06x'},
                                     'target': 'Kulay sa honeycomb #%1$06X',
                                     'type': 'string'},
         'ui_honeycomb_colour_swatches_with_a_greyscale_row': {'attributes': {'name': 'ui_honeycomb_colour_swatches_with_a_greyscale_row'},
                                                               'target': 'Mga swatch ng kulay na honeycomb na may '
                                                                         'grayscale row',
                                                               'type': 'string'},
         'ui_horizontal23': {'attributes': {'name': 'ui_horizontal23'}, 'target': 'Pahalang', 'type': 'string'},
         'ui_how_to_use': {'attributes': {'formatted': 'false', 'name': 'ui_how_to_use'},
                           'target': 'Paano gamitin',
                           'type': 'string'},
         'ui_hue_and_saturation_spectrum_lightness_slider_on_the': {'attributes': {'name': 'ui_hue_and_saturation_spectrum_lightness_slider_on_the'},
                                                                    'target': 'Spectrum ng hue at saturation; '
                                                                              'lightness slider sa kanan',
                                                                    'type': 'string'},
         'ui_hue_and_saturation_wheel_value_slider_on_the': {'attributes': {'name': 'ui_hue_and_saturation_wheel_value_slider_on_the'},
                                                             'target': 'Color wheel ng hue at saturation; value '
                                                                       'slider sa kanan',
                                                             'type': 'string'},
         'ui_icon_licences': {'attributes': {'name': 'ui_icon_licences'},
                              'target': 'Mga lisensiya ng icon',
                              'type': 'string'},
         'ui_icon_licences_kde_breeze': {'attributes': {'name': 'ui_icon_licences_kde_breeze'},
                                         'target': 'Mga lisensiya ng icon — KDE Breeze',
                                         'type': 'string'},
         'ui_icons_artwork': {'attributes': {'name': 'ui_icons_artwork'},
                              'target': 'Mga icon at artwork',
                              'type': 'string'},
         'ui_icons_fonts_artwork_credits': {'attributes': {'name': 'ui_icons_fonts_artwork_credits'},
                                            'target': 'Mga credit ng icon, font at artwork',
                                            'type': 'string'},
         'ui_image_assembly': {'attributes': {'formatted': 'false', 'name': 'ui_image_assembly'},
                               'target': 'Pagsamahin ang mga larawan…',
                               'type': 'string'},
         'ui_image_assembly_workspace_drag_placed_images_or_drop': {'attributes': {'name': 'ui_image_assembly_workspace_drag_placed_images_or_drop'},
                                                                    'target': 'Workspace ng pagsasama ng mga '
                                                                              'larawan. I-drag ang mga '
                                                                              'nakapuwestong larawan o ihulog ang '
                                                                              'mga thumbnail para kumabit sa '
                                                                              'target sa kanan o ibaba. Kurutin '
                                                                              'para mag-zoom; i-drag ang '
                                                                              'bakanteng espasyo para mag-pan.',
                                                                    'type': 'string'},
         'ui_image_codec_licences': {'attributes': {'name': 'ui_image_codec_licences'},
                                     'target': 'Mga lisensiya ng image codec',
                                     'type': 'string'},
         'ui_image_credits': {'attributes': {'name': 'ui_image_credits'},
                              'target': 'Mga credit ng larawan',
                              'type': 'string'},
         'ui_image_placed_drag_it_to_move_or_hold': {'attributes': {'name': 'ui_image_placed_drag_it_to_move_or_hold'},
                                                     'target': 'Nakapuwesto ang larawan. I-drag para ilipat, o '
                                                               'pindutin nang matagal at i-drag ang isa pang '
                                                               'thumbnail.',
                                                     'type': 'string'},
         'ui_image_thumbnails_and_filenames_scroll_horizontally_for_more': {'attributes': {'name': 'ui_image_thumbnails_and_filenames_scroll_horizontally_for_more'},
                                                                            'target': 'Mga thumbnail at pangalan '
                                                                                      'ng file ng larawan. '
                                                                                      'Mag-scroll pahalang para '
                                                                                      'sa higit pa.',
                                                                            'type': 'string'},
         'ui_insert_gallery_image': {'attributes': {'name': 'ui_insert_gallery_image'},
                                     'target': 'Magpasok ng larawan mula sa gallery?',
                                     'type': 'string'},
         'ui_invalid_image_attachments': {'attributes': {'name': 'ui_invalid_image_attachments'},
                                          'target': 'Hindi wasto ang pagkakabit ng larawan.',
                                          'type': 'string'},
         'ui_irasutoya_credit34': {'attributes': {'name': 'ui_irasutoya_credit34'},
                                   'target': 'Nananatili sa creator ang copyright. Sakop ng mga tuntunin ng '
                                             'Irasutoya ang paggamit; hindi ito Creative Commons licence.',
                                   'type': 'string'},
         'ui_irasutoya_help34': {'attributes': {'name': 'ui_irasutoya_help34'},
                                 'target': 'Buksan ang page ng artwork at i-tap ang Gamitin ang larawan. Maghanap '
                                           'sa Ingles o Hapon; mananatiling nasa Hapon ang pamagat ng artwork at '
                                           'teksto ng site. Ang libreng paggamit ay sakop ng mga tuntunin ng '
                                           'Irasutoya: may bayad ang commercial design na gumagamit ng 21 o higit '
                                           'pang item. Maaaring may ibang kundisyon ang mga espesyal na '
                                           'collaboration. Itinatabi ang source page at credit sa File → Tungkol, '
                                           'mga lisensiya at pagkilala → Mga credit ng larawan.',
                                 'type': 'string'},
         'ui_jpeg_xl_codec_licences': {'attributes': {'name': 'ui_jpeg_xl_codec_licences'},
                                       'target': 'Mga lisensiya ng JPEG XL codec',
                                       'type': 'string'},
         'ui_largest': {'attributes': {'name': 'ui_largest'}, 'target': 'Pinakamalaki', 'type': 'string'},
         'ui_lossless_jpeg_xl': {'attributes': {'name': 'ui_lossless_jpeg_xl'},
                                 'target': 'Lossless JPEG XL',
                                 'type': 'string'},
         'ui_magnified_preview': {'attributes': {'formatted': 'false', 'name': 'ui_magnified_preview'},
                                  'target': 'Pinalaking paunang tingin…',
                                  'type': 'string'},
         'ui_magnified_preview_ea9209': {'attributes': {'name': 'ui_magnified_preview_ea9209'},
                                         'target': 'Pinalaking preview',
                                         'type': 'string'},
         'ui_magnifier33': {'attributes': {'formatted': 'false', 'name': 'ui_magnifier33'},
                            'target': 'Lente',
                            'type': 'string'},
         'ui_modified_newest_first': {'attributes': {'name': 'ui_modified_newest_first'},
                                      'target': 'Binago: pinakabago muna',
                                      'type': 'string'},
         'ui_modified_oldest_first': {'attributes': {'name': 'ui_modified_oldest_first'},
                                      'target': 'Binago: pinakaluma muna',
                                      'type': 'string'},
         'ui_monospace': {'attributes': {'name': 'ui_monospace'}, 'target': 'Monospace', 'type': 'string'},
         'ui_no_attachment_fits_within_the_current_coordinate_range': {'attributes': {'name': 'ui_no_attachment_fits_within_the_current_coordinate_range'},
                                                                       'target': 'Walang pagkakabit na kasya sa '
                                                                                 'kasalukuyang coordinate range. '
                                                                                 'Subukan ang mas maliliit na '
                                                                                 'laki ng larawan.',
                                                                       'type': 'string'},
         'ui_no_gallery_images_have_been_inserted': {'attributes': {'name': 'ui_no_gallery_images_have_been_inserted'},
                                                     'target': 'Walang tekstong magagamit para sa credit ng '
                                                               'larawan.',
                                                     'type': 'string'},
         'ui_normalize_height_info': {'attributes': {'name': 'ui_normalize_height_info'},
                                      'target': 'Taas ng bawat larawan: %1$d px\\nMga lapad: %2$d–%3$d px\\nAng '
                                                'porsiyento ay batay sa pinakamalaking kasalukuyang taas: %4$d '
                                                'px. Muling inaayos ang mga nakapuwestong larawan upang magkaroon '
                                                'ng puwang.',
                                      'type': 'string'},
         'ui_normalize_height_input_percent': {'attributes': {'name': 'ui_normalize_height_input_percent'},
                                               'target': 'Parehong taas bilang porsiyento ng pinakamalaking '
                                                         'kasalukuyang taas: %1$d px',
                                               'type': 'string'},
         'ui_normalize_height_intro': {'attributes': {'name': 'ui_normalize_height_intro'},
                                       'target': 'Bigyan ang lahat ng larawan ng parehong taas. Bilang ng mga '
                                                 'larawan: %1$d. Pinananatili ng bawat larawan ang sarili nitong '
                                                 'aspect ratio. Hindi nagbabago ang mga orihinal na file at crop '
                                                 'setting.',
                                       'type': 'string'},
         'ui_normalize_width_info': {'attributes': {'name': 'ui_normalize_width_info'},
                                     'target': 'Lapad ng bawat larawan: %1$d px\\nMga taas: %2$d–%3$d px\\nAng '
                                               'porsiyento ay batay sa pinakamalaking kasalukuyang lapad: %4$d '
                                               'px. Muling inaayos ang mga nakapuwestong larawan upang magkaroon '
                                               'ng puwang.',
                                     'type': 'string'},
         'ui_normalize_width_input_percent': {'attributes': {'name': 'ui_normalize_width_input_percent'},
                                              'target': 'Parehong lapad bilang porsiyento ng pinakamalaking '
                                                        'kasalukuyang lapad: %1$d px',
                                              'type': 'string'},
         'ui_normalize_width_intro': {'attributes': {'name': 'ui_normalize_width_intro'},
                                      'target': 'Bigyan ang lahat ng larawan ng parehong lapad. Bilang ng mga '
                                                'larawan: %1$d. Pinananatili ng bawat larawan ang sarili nitong '
                                                'aspect ratio. Hindi nagbabago ang mga orihinal na file at crop '
                                                'setting.',
                                      'type': 'string'},
         'ui_not_enough_memory_to_inspect_the_gallery_image': {'attributes': {'name': 'ui_not_enough_memory_to_inspect_the_gallery_image'},
                                                               'target': 'Kulang ang memory para siyasatin ang '
                                                                         'larawan sa gallery.',
                                                               'type': 'string'},
         'ui_not_placed': {'attributes': {'name': 'ui_not_placed'},
                           'target': 'Hindi nakapuwesto',
                           'type': 'string'},
         'ui_open_artwork34': {'attributes': {'name': 'ui_open_artwork34'},
                               'target': 'Buksan muna ang page ng artwork, saka i-tap ang Gamitin ang larawan.',
                               'type': 'string'},
         'ui_open_source_credits_and_notices': {'attributes': {'name': 'ui_open_source_credits_and_notices'},
                                                'target': 'Mga credit at abiso ng open source',
                                                'type': 'string'},
         'ui_openclipart_help34': {'attributes': {'name': 'ui_openclipart_help34'},
                                   'target': 'Buksan ang page ng artwork at i-tap ang Gamitin ang larawan sa tabi '
                                             'ng Large PNG download nito. Naglalathala ang Openclipart ng artwork '
                                             'sa ilalim ng CC0. Itinatabi ang source page at lisensiya sa File → '
                                             'Tungkol, mga lisensiya at pagkilala → Mga credit ng larawan.',
                                   'type': 'string'},
         'ui_original_decoded_image_rgba_4_bytes_pixel_estimated': {'attributes': {'name': 'ui_original_decoded_image_rgba_4_bytes_pixel_estimated'},
                                                                    'target': 'Orihinal: %1$s\\nNa-decode na '
                                                                              'larawan: %2$s (RGBA, 4 '
                                                                              'bytes/pixel)\\nTinatayang memory '
                                                                              'sa pag-edit nang walang resize: '
                                                                              '%3$s',
                                                                    'type': 'string'},
         'ui_other_terms': {'attributes': {'name': 'ui_other_terms'},
                            'target': 'Iba pang tuntunin',
                            'type': 'string'},
         'ui_pale_violet': {'attributes': {'name': 'ui_pale_violet'},
                            'target': 'Mapusyaw na lila',
                            'type': 'string'},
         'ui_pencil_crisp_adjustable_strokes': {'attributes': {'name': 'ui_pencil_crisp_adjustable_strokes'},
                                                'target': 'Pinananatili ng lapis ang malinaw na gilid sa anumang '
                                                          'napiling lapad.',
                                                'type': 'string'},
         'ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing': {'attributes': {'name': 'ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing'},
                                                                    'target': 'Pinananatili ng lapis ang malinaw '
                                                                              'na gilid sa anumang napiling '
                                                                              'lapad.',
                                                                    'type': 'string'},
         'ui_percent_of_pixels': {'attributes': {'name': 'ui_percent_of_pixels'},
                                  'target': 'porsiyento ng %1$s pixels',
                                  'type': 'string'},
         'ui_pinch_to_zoom_drag_to_pan': {'attributes': {'name': 'ui_pinch_to_zoom_drag_to_pan'},
                                          'target': 'Kurutin para mag-zoom. I-drag para mag-pan.',
                                          'type': 'string'},
         'ui_pixel_grid33': {'attributes': {'formatted': 'false', 'name': 'ui_pixel_grid33'},
                             'target': 'Grid ng pixel',
                             'type': 'string'},
         'ui_pixel_grid_help33': {'attributes': {'formatted': 'false', 'name': 'ui_pixel_grid_help33'},
                                  'target': 'Lilitaw ang grid ng pixel kapag naka-zoom nang 800% o higit pa. '
                                            'Ipinapakita ng mga ruler ang posisyon sa mga pixel ng larawan.',
                                  'type': 'string'},
         'ui_place_at_least_one_image_in_the_workspace': {'attributes': {'name': 'ui_place_at_least_one_image_in_the_workspace'},
                                                          'target': 'Maglagay muna ng kahit isang larawan sa '
                                                                    'workspace.',
                                                          'type': 'string'},
         'ui_placed': {'attributes': {'name': 'ui_placed'}, 'target': 'Nakapuwesto', 'type': 'string'},
         'ui_preview_memory_error': {'attributes': {'name': 'ui_preview_memory_error'},
                                     'target': '%1$s: kulang ang memory para sa preview nito.',
                                     'type': 'string'},
         'ui_px_drag_an_image_to_move_hold_a': {'attributes': {'name': 'ui_px_drag_an_image_to_move_hold_a'},
                                                'target': '%1$s × %2$s px · i-drag ang larawan para ilipat; '
                                                          'pindutin nang matagal ang thumbnail para idagdag.',
                                                'type': 'string'},
         'ui_radius_px': {'attributes': {'name': 'ui_radius_px'}, 'target': 'Radius (px)', 'type': 'string'},
         'ui_recent_colour_d_06x_tap_foreground_hold_background': {'attributes': {'name': 'ui_recent_colour_d_06x_tap_foreground_hold_background'},
                                                                   'target': 'Kamakailang kulay %1$d: #%2$06X. '
                                                                             'I-tap para sa harap, pindutin nang '
                                                                             'matagal para sa likod.',
                                                                   'type': 'string'},
         'ui_recent_colour_empty': {'attributes': {'name': 'ui_recent_colour_empty'},
                                    'target': 'Kamakailang kulay %1$s: walang laman',
                                    'type': 'string'},
         'ui_remove_palette23': {'attributes': {'name': 'ui_remove_palette23'},
                                 'target': 'Alisin sa paleta',
                                 'type': 'string'},
         'ui_rendering_images': {'attributes': {'name': 'ui_rendering_images'},
                                 'target': 'Nire-render ang %1$s / %2$s larawan…',
                                 'type': 'string'},
         'ui_replace_palette23': {'attributes': {'name': 'ui_replace_palette23'},
                                  'target': 'Puno ang paleta — pumili ng kulay na papalitan',
                                  'type': 'string'},
         'ui_replace_with_active23': {'attributes': {'name': 'ui_replace_with_active23'},
                                      'target': 'Palitan gamit ang aktibong kulay',
                                      'type': 'string'},
         'ui_restore_original_sizes': {'attributes': {'name': 'ui_restore_original_sizes'},
                                       'target': 'Ibalik ang orihinal na laki',
                                       'type': 'string'},
         'ui_right_arrow_expand': {'attributes': {'name': 'ui_right_arrow_expand'},
                                   'target': 'Kanang arrow: palawakin',
                                   'type': 'string'},
         'ui_round': {'attributes': {'formatted': 'false', 'name': 'ui_round'},
                      'target': 'Bilog',
                      'type': 'string'},
         'ui_same': {'attributes': {'name': 'ui_same'}, 'target': 'Parehong %1$s', 'type': 'string'},
         'ui_same_height': {'attributes': {'name': 'ui_same_height'}, 'target': 'Parehong taas', 'type': 'string'},
         'ui_same_width': {'attributes': {'name': 'ui_same_width'}, 'target': 'Parehong lapad', 'type': 'string'},
         'ui_sans_condensed': {'attributes': {'name': 'ui_sans_condensed'},
                               'target': 'Sans condensed',
                               'type': 'string'},
         'ui_sans_light': {'attributes': {'name': 'ui_sans_light'}, 'target': 'Sans light', 'type': 'string'},
         'ui_sans_medium': {'attributes': {'name': 'ui_sans_medium'}, 'target': 'Sans medium', 'type': 'string'},
         'ui_sans_serif': {'attributes': {'name': 'ui_sans_serif'}, 'target': 'Sans Serif', 'type': 'string'},
         'ui_sans_thin': {'attributes': {'name': 'ui_sans_thin'}, 'target': 'Sans thin', 'type': 'string'},
         'ui_save_as_avif': {'attributes': {'name': 'ui_save_as_avif'},
                             'target': 'I-save bilang AVIF…',
                             'type': 'string'},
         'ui_save_as_heic': {'attributes': {'name': 'ui_save_as_heic'},
                             'target': 'I-save bilang HEIC…',
                             'type': 'string'},
         'ui_save_as_webp': {'attributes': {'name': 'ui_save_as_webp'},
                             'target': 'I-save bilang WebP…',
                             'type': 'string'},
         'ui_saved_palette23': {'attributes': {'name': 'ui_saved_palette23'},
                                'target': 'Na-save na paleta',
                                'type': 'string'},
         'ui_search34': {'attributes': {'formatted': 'false', 'name': 'ui_search34'},
                         'target': 'Maghanap',
                         'type': 'string'},
         'ui_search_english34': {'attributes': {'formatted': 'false', 'name': 'ui_search_english34'},
                                 'target': 'Maghanap sa Ingles o Hapon',
                                 'type': 'string'},
         'ui_serif': {'attributes': {'name': 'ui_serif'}, 'target': 'Serif', 'type': 'string'},
         'ui_set_radius_px_then_drag_between_opposite_corners': {'attributes': {'name': 'ui_set_radius_px_then_drag_between_opposite_corners'},
                                                                 'target': 'Itakda ang Radius (px), saka i-drag '
                                                                           'sa pagitan ng magkatapat na sulok. '
                                                                           'Limitado ang radius sa kalahati ng '
                                                                           'mas maikling side ng bawat rectangle.',
                                                                 'type': 'string'},
         'ui_show_pixel_grid_800': {'attributes': {'formatted': 'false', 'name': 'ui_show_pixel_grid_800'},
                                    'target': 'Ipakita ang grid ng pixel (800% pataas)',
                                    'type': 'string'},
         'ui_shows_the_whole_assembly_image_and_output_sizes': {'attributes': {'name': 'ui_shows_the_whole_assembly_image_and_output_sizes'},
                                                                'target': 'Ipinapakita ang buong pagsasama. Hindi '
                                                                          'nagbabago ang laki ng larawan at '
                                                                          'output.',
                                                                'type': 'string'},
         'ui_silver': {'attributes': {'name': 'ui_silver'}, 'target': 'Pilak', 'type': 'string'},
         'ui_smallest': {'attributes': {'name': 'ui_smallest'}, 'target': 'Pinakamaliit', 'type': 'string'},
         'ui_smooth_freehand_strokes': {'attributes': {'name': 'ui_smooth_freehand_strokes'},
                                        'target': 'Pakinisin ang mga guhit na malayang iginuhit',
                                        'type': 'string'},
         'ui_smooth_pixel_edges_anti_aliasing': {'attributes': {'name': 'ui_smooth_pixel_edges_anti_aliasing'},
                                                 'target': 'Pakinisin ang mga gilid ng pixel (anti-aliasing)',
                                                 'type': 'string'},
         'ui_some_previews_could_not_be_decoded_you_can': {'attributes': {'name': 'ui_some_previews_could_not_be_decoded_you_can'},
                                                           'target': 'Hindi ma-decode ang ilang preview. Maaari '
                                                                     'mong alisin ang mga larawang iyon o '
                                                                     'subukang i-save ang pagsasama.',
                                                           'type': 'string'},
         'ui_sort_images_by_filename_or_modification_time': {'attributes': {'name': 'ui_sort_images_by_filename_or_modification_time'},
                                                             'target': 'Ayusin ang mga larawan ayon sa pangalan '
                                                                       'ng file o oras ng pagbabago',
                                                             'type': 'string'},
         'ui_sort_tray': {'attributes': {'name': 'ui_sort_tray'}, 'target': 'Ayusin ang tray', 'type': 'string'},
         'ui_source_code_exported_including_build_scripts_and_licence': {'attributes': {'name': 'ui_source_code_exported_including_build_scripts_and_licence'},
                                                                         'target': 'Na-export ang source code, '
                                                                                   'kasama ang mga build script '
                                                                                   'at abiso ng lisensiya.',
                                                                         'type': 'string'},
         'ui_spectrum': {'attributes': {'name': 'ui_spectrum'}, 'target': 'Spektrum', 'type': 'string'},
         'ui_spray_radius_px': {'attributes': {'name': 'ui_spray_radius_px'},
                                'target': 'Radius ng spray (px)',
                                'type': 'string'},
         'ui_square': {'attributes': {'formatted': 'false', 'name': 'ui_square'},
                       'target': 'Parisukat',
                       'type': 'string'},
         'ui_strength': {'attributes': {'formatted': 'false', 'name': 'ui_strength'},
                         'target': 'Lakas (%)',
                         'type': 'string'},
         'ui_strikethrough': {'attributes': {'name': 'ui_strikethrough'},
                              'target': 'Strikethrough',
                              'type': 'string'},
         'ui_tap_a_pixel': {'attributes': {'name': 'ui_tap_a_pixel'},
                            'target': 'I-tap ang isang pixel',
                            'type': 'string'},
         'ui_tap_an_enclosed_area_adjust_tolerance_for_similar': {'attributes': {'name': 'ui_tap_an_enclosed_area_adjust_tolerance_for_similar'},
                                                                  'target': 'I-tap ang nakasarang bahagi. Isaayos '
                                                                            'ang tolerance para sa magkahawig na '
                                                                            'kulay.',
                                                                  'type': 'string'},
         'ui_tap_an_image_thumbnail_first': {'attributes': {'name': 'ui_tap_an_image_thumbnail_first'},
                                             'target': 'I-tap muna ang thumbnail ng larawan.',
                                             'type': 'string'},
         'ui_tap_the_canvas_to_place_text_and_choose': {'attributes': {'name': 'ui_tap_the_canvas_to_place_text_and_choose'},
                                                        'target': 'I-tap ang canvas para ilagay ang teksto at '
                                                                  'piliin ang font at laki nito.',
                                                        'type': 'string'},
         'ui_tap_the_image_to_sample_the_foreground_colour': {'attributes': {'name': 'ui_tap_the_image_to_sample_the_foreground_colour'},
                                                              'target': 'I-tap ang larawan para kumuha ng sample '
                                                                        'ng kulay sa harap.',
                                                              'type': 'string'},
         'ui_tap_vertices_then_double_tap_the_last_vertex': {'attributes': {'name': 'ui_tap_vertices_then_double_tap_the_last_vertex'},
                                                             'target': 'I-tap ang mga vertex, saka i-double-tap '
                                                                       'ang huling vertex para isara ang polygon. '
                                                                       'Maaari ring gamitin ang Tapusin ang '
                                                                       'polygon. I-off ang Isara ang polygon para '
                                                                       'gumuhit ng magkakaugnay na bukas na line '
                                                                       'segment.',
                                                             'type': 'string'},
         'ui_that_arrangement_overlaps_another_image_use_a_different': {'attributes': {'name': 'ui_that_arrangement_overlaps_another_image_use_a_different'},
                                                                        'target': 'Nag-o-overlap ang ayos na iyon '
                                                                                  'sa ibang larawan. Gumamit ng '
                                                                                  'ibang gilid o alisin muna sa '
                                                                                  'puwesto ang mga nakakabit na '
                                                                                  'larawan.',
                                                                        'type': 'string'},
         'ui_the_arrow_on_the_left_directly_below_the': {'attributes': {'formatted': 'false',
                                                                        'name': 'ui_the_arrow_on_the_left_directly_below_the'},
                                                         'target': 'Ang arrow sa kaliwa, direkta sa ibaba ng '
                                                                   'toolbar, ang nagko-collapse o nagbabalik sa '
                                                                   'mga tool: pataas para i-collapse, pababa para '
                                                                   'palawakin. Sa portrait, pahalang na tumatakbo '
                                                                   'ang tool strip sa ibaba ng toolbar; mag-swipe '
                                                                   'para maabot ang iba pang tool. Sa landscape, '
                                                                   'nananatili ito sa kaliwa. Pinagsasama ng '
                                                                   'Brush ang Lapis, Brush, Watercolor at '
                                                                   'Airbrush. Pinagsasama ng Pagpili ang '
                                                                   'rectangle at free-form selection. Pinagsasama '
                                                                   'ng Ipasok ang mga linya, hugis at teksto. '
                                                                   'I-tap ang isang kategorya para palawakin ang '
                                                                   'mga tool at setting nito direkta sa ibaba ng '
                                                                   'strip sa portrait, o sa kanan nito sa '
                                                                   'landscape. I-tap muli para i-collapse; '
                                                                   'babaliktad ang arrow. Naaalala ng bawat '
                                                                   'kategorya ang huling ginamit na tool. '
                                                                   'I-scroll ang panel ng mga opsiyon na may '
                                                                   'takdang hangganan para sa iba pang setting at '
                                                                   'control sa pag-edit. Parehong nakabukas ang '
                                                                   'dalawang panel sa unang paggamit ng layout na '
                                                                   'ito; maaalala ang mga susunod na pagpili. Sa '
                                                                   'landscape, iisang row ang mga control sa '
                                                                   'itaas at nakasentro ang pangalan ng file. Mga '
                                                                   'credit at tuntunin: «File > Tungkol, mga '
                                                                   'lisensiya at pagkilala».\\n\\nNananatiling '
                                                                   'nakapirmi sa ibabang kaliwa ang FG/BG color '
                                                                   'indicator, katabi ng paleta. Bumubukas ang '
                                                                   'paleta direkta sa kanan nito sa parehong row. '
                                                                   'Nasa kanang gilid ang arrow nito: pakaliwa '
                                                                   'para i-collapse ang paleta, pakanan para '
                                                                   'palawakin. Itinatago ng pag-collapse ang mga '
                                                                   'dagdag na swatch nang hindi ginagalaw ang '
                                                                   'indicator. Maaari ring i-toggle ang paleta sa '
                                                                   'pag-tap sa color box. I-tap ang swatch para '
                                                                   'sa kulay sa harap o pindutin nang matagal '
                                                                   'para sa likod. Binubuksan ng FG/BG ang '
                                                                   'Paleta, Bahay-pukyutan at Mas maraming '
                                                                   'opsiyon. May spectrum, wheel, RGB, HSV, HSL '
                                                                   'at six-digit hex control ang Mas maraming '
                                                                   'opsiyon. Itinatabi ng apat na cell sa '
                                                                   'pinakakanan ang mga kamakailang kulay; i-tap '
                                                                   'para sa harap o pindutin nang matagal para sa '
                                                                   'likod. Nagsisimula ang mga pasadyang kulay sa '
                                                                   'Mapusyaw na lila #5B67FF, Ginto #FFD700, '
                                                                   'Pilak #C0C0C0 at Tanso #B87333. Pindutin nang '
                                                                   'matagal ang pasadyang swatch para palitan '
                                                                   'ito. Gumagamit ang pangunahing editor ng '
                                                                   'opaque na kulay; inilalagay ang transparent '
                                                                   'na import sa kasalukuyang BG na kulay. Hindi '
                                                                   'nagbabago ang orihinal na source '
                                                                   'file.\\n\\nPinalitan ng Ilipat at i-zoom ang '
                                                                   'magnifying-glass tool: i-drag gamit ang isang '
                                                                   'daliri para mag-pan, kurutin gamit ang '
                                                                   'dalawang daliri para mag-zoom at mag-pan. '
                                                                   'I-tap muli ang Ilipat at i-zoom o Gumuhit '
                                                                   'muli para bumalik sa pagguhit. Gumagana rin '
                                                                   'ang two-finger navigation habang nasa drawing '
                                                                   'tools nang hindi nag-iiwan ng marka. May '
                                                                   'center line sa 100% ang slider sa ibabang '
                                                                   'kanan. Humihinto sa 100% ang zoom in/out '
                                                                   'button kapag tatawid dito ang isang hakbang; '
                                                                   'pindutin muli para magpatuloy. Iniaangkop at '
                                                                   'isinisentro ng katabing Iangkop button ang '
                                                                   'canvas sa view. May 100% at pixel grid din sa '
                                                                   'Tingnan.\\n\\nItinatala ng autosave ang '
                                                                   'kasalukuyang draft pagkatapos ng maikling '
                                                                   'paghinto sa pag-edit at kapag umalis ka sa '
                                                                   'app. Ipinapakita ng status ang Na-save ang '
                                                                   'draft o autosave error. Kapag binuksan muli, '
                                                                   'ibinabalik ang draft, pangalan ng file, '
                                                                   'setting ng tool, floating selection at hindi '
                                                                   'pa tapos na geometry. Nagtatabi ang autosave '
                                                                   'ng pribadong working draft. Nag-aalok ang '
                                                                   'File ng PNG, adjustable-quality JPEG at HEIC, '
                                                                   'at lossless o lossy JPEG XL, WebP at AVIF. '
                                                                   'Pinipili ng I-save bilang ang format ng '
                                                                   'larawan, mga setting at lokasyon; muling '
                                                                   'nagsusulat doon ang I-save. Nagsusulat ng '
                                                                   'kopya ang I-export bilang at I-save at '
                                                                   'ibahagi nang hindi binabago ang kasalukuyang '
                                                                   'destinasyon ng I-save o minamarkahan ang '
                                                                   'drawing bilang saved. Pagkatapos, binubuksan '
                                                                   'ng I-save at ibahagi ang Android sharing. Ang '
                                                                   'bituin sa pangalan ng file ay '
                                                                   'nangangahulugang may hindi pa nase-save na '
                                                                   'pagbabago ang drawing. Hindi kailanman '
                                                                   'ino-overwrite ng autosave ang source '
                                                                   'image.\\n\\nMga selection: gumuhit ng '
                                                                   'rectangle o free-form outline. I-drag ang '
                                                                   'loob para ilipat, i-drag ang parisukat na '
                                                                   'sulok o midpoint ng gilid para baguhin ang '
                                                                   'laki, o i-drag ang bilog na Paikutin handle '
                                                                   'para paikutin. Naka-on bilang default ang '
                                                                   'I-lock ang proporsyon; i-off ito para hiwalay '
                                                                   'na i-stretch ang lapad at taas. Binabago ng '
                                                                   'edge handle ang laki sa napiling side. '
                                                                   'Pinananatili ng free-form selection ang '
                                                                   'napiling hugis sa loob ng transform box, pati '
                                                                   'pagkatapos ng rotation at autosave. Lumalabas '
                                                                   'sa sidebar ang sukat at angle. Inilalapat ng '
                                                                   'Ilapat ang napili ang resulta bilang isang '
                                                                   'selection edit na maaaring i-undo; '
                                                                   'pinananatili ng autosave ang hindi pa tapos '
                                                                   'na transform. Ginagamit ng Kopyahin, I-cut at '
                                                                   'Gupitin ayon sa napili ang transformed na '
                                                                   'larawan. Ang Piliin lahat ay nasa pangalawang '
                                                                   'row ng edit icon, at gumagana ang Ctrl+A sa '
                                                                   'external keyboard. Ang I-cut/Kopyahin at '
                                                                   'I-paste/Piliin lahat ay bumubuo ng dalawang '
                                                                   'row sa ibaba ng Paano gamitin. Pinananatili '
                                                                   'ng selection mask ang napiling hugis; '
                                                                   'nananatiling opaque ang dokumento.\\n\\nMga '
                                                                   'hangganan ng canvas: i-drag papasok ang '
                                                                   'handle para bawasan o palabas para palawakin '
                                                                   'ang alinmang side, saka Ilapat ang hangganan. '
                                                                   'BG ang ginagamit sa bagong espasyo; hindi '
                                                                   'sine-scale ang kasalukuyang pixels. Available '
                                                                   'ang Kanselahin at Ibalik. Tumatanggap din ang '
                                                                   'Baguhin ang laki ng larawan, Laki ng canvas '
                                                                   'at Bagong imahe ng Pixels o Porsiyento na may '
                                                                   'opsyonal na aspect lock.\\n\\nKurba: gumuhit '
                                                                   'ng linya at i-drag nang dalawang beses para '
                                                                   'baluktutin ito. Poligono: i-tap ang mga '
                                                                   'vertex, saka i-double-tap ang huling vertex o '
                                                                   'gamitin ang Tapusin ang polygon. I-off ang '
                                                                   'Isara ang polygon para gumuhit ng '
                                                                   'magkakaugnay na bukas na segment. Parihabang '
                                                                   'bilugan ang mga sulok: itakda ang Radius (px) '
                                                                   'gamit ang slider; nililimitahan ng bawat '
                                                                   'hugis ang radius sa kalahati ng mas maikling '
                                                                   'side. Teksto: i-tap ang canvas, pumili ng '
                                                                   'font na ipinapakita sa sarili nitong style at '
                                                                   'gamitin ang live preview. Kasama sa opsyon '
                                                                   'ang laki, bold, italic, underline, '
                                                                   'strikethrough, alignment, line spacing at BG '
                                                                   'text box. Nasa Brush category ang Watercolor '
                                                                   'katabi ng Brush at Airbrush; isaayos ang '
                                                                   'lakas para sa mas malambot na stroke. Umaabot '
                                                                   'sa 100 pixels ang size slider ng pencil, '
                                                                   'brush at tool. Nagsisimula ang Lapis sa 1 '
                                                                   'pixel at naaalala ang sarili nitong lapad. '
                                                                   'I-tap ang ipinapakitang numero para sa '
                                                                   'eksaktong numeric input. Pareho ang '
                                                                   'outline/fill choices ng Puso, Bituin at '
                                                                   'Palaso sa ibang hugis. Pinalalawak ng Tingnan '
                                                                   '> Pagguhit gamit ang cursor ang enable '
                                                                   'switch, cursor shape at magnifier setting. '
                                                                   'I-drag para ipuwesto ang cursor, i-tap ang '
                                                                   'on-screen drawing button, saka mag-pan para '
                                                                   'gumuhit. I-tap muli para huminto. Nananatili '
                                                                   'sa Gumuhit > Pagguhit ang brush at stroke '
                                                                   'setting. Ipinapakita ng Tingnan > Pinalaking '
                                                                   'preview ang cursor o drawing point sa '
                                                                   'adjustable magnification. May antialiasing at '
                                                                   'stroke smoothing din sa Mga setting sa '
                                                                   'pagguhit. May labing-isang dagdag na font; '
                                                                   'nasa Mga lisensiya ng font ang mga credit at '
                                                                   'buong tuntunin ng mga ito.\\n\\nPinapalitan '
                                                                   'ng File > Magbukas ng larawan ang canvas sa '
                                                                   'pamamagitan ng picker ng Android. Nasa '
                                                                   '«Gumuhit > Ipasok > Iba pang larawan» ang mga '
                                                                   'file sa device, Catrobat, Irasutoya at '
                                                                   'Openclipart. Pumili ng larawan mula sa '
                                                                   'device, o magbukas ng page ng artwork sa '
                                                                   'internet at i-tap ang «Gamitin ang larawan», '
                                                                   'para magdagdag ng larawan bilang floating '
                                                                   'selection. Itinatabi ng File > Tungkol, mga '
                                                                   'lisensiya at pagkilala > Mga credit ng '
                                                                   'larawan ang source link at abiso ng '
                                                                   'lisensiya. Ang mga larawang pasok sa memory '
                                                                   'limit ng device ay bino-load sa orihinal na '
                                                                   'resolution. Kung kailangan, ipinapakita ng '
                                                                   'resize-choice dialog ang sukat, pixel count '
                                                                   'at pagtataya sa memory, na may '
                                                                   'Pixels/Porsiyento sizing at opsyonal na '
                                                                   'aspect lock. Hindi nagbabago ang orihinal na '
                                                                   'file.\\n\\nBinubuksan ng File > Pagsamahin '
                                                                   'ang mga larawan ang hiwalay na workspace para '
                                                                   'sa hanggang 20 larawan. Ayusin ang mga '
                                                                   'thumbnail ayon sa pangalan ng file o oras. '
                                                                   'I-crop ang isang larawan o i-batch crop ang '
                                                                   'ilan. Pinapantay ng Parehong lapad / Parehong '
                                                                   'taas ang lahat ng na-load na larawan habang '
                                                                   'pinananatili ang aspect ratio. I-drag ang mga '
                                                                   'thumbnail o nakapuwestong larawan para ikabit '
                                                                   'sa kanan na pantay ang itaas, o sa ibaba na '
                                                                   'pantay ang kaliwang gilid. Inaalis ng Alisin '
                                                                   'sa puwesto ang napiling placement lamang at '
                                                                   'isinasara ang puwang. Ipakita lahat ay '
                                                                   'pagbabago lang sa zoom ng view. Ini-export ng '
                                                                   'I-save ang PNG ang pagsasama; inililipat ito '
                                                                   'ng I-edit sa Paint bilang edit na maaaring '
                                                                   'i-undo. Gumagamit ang app ng isang opaque '
                                                                   'image editor. Hiwalay na arrangement '
                                                                   'workspace ang Pagsasama ng '
                                                                   'larawan.\\n\\nKasama sa panel na «File > '
                                                                   'Tungkol, mga lisensiya at pagkilala» ang '
                                                                   'orihinal na copyright, mga credit ng '
                                                                   'asset/font, buong teksto ng lisensiya at '
                                                                   'kumpletong source ng bersiyong ito. Hiwalay '
                                                                   'na nase-scroll ang teksto ng lisensiya mula '
                                                                   'sa nakapirming Kopyahin lahat, Iba pang '
                                                                   'tuntunin at Tapos na mga button.',
                                                         'type': 'string'},
         'ui_the_assembly_exceeds_android_s_coordinate_range': {'attributes': {'name': 'ui_the_assembly_exceeds_android_s_coordinate_range'},
                                                                'target': 'Lumampas ang pagsasama sa coordinate '
                                                                          'range ng Android.',
                                                                'type': 'string'},
         'ui_the_assembly_needs_about_choose_a_smaller_output': {'attributes': {'name': 'ui_the_assembly_needs_about_choose_a_smaller_output'},
                                                                 'target': 'Kailangan ng pagsasama ng '
                                                                           'humigit-kumulang %1$s. Pumili ng mas '
                                                                           'maliit na laki ng output.',
                                                                 'type': 'string'},
         'ui_the_assembly_output_is_unavailable_reopen_image_assembly': {'attributes': {'name': 'ui_the_assembly_output_is_unavailable_reopen_image_assembly'},
                                                                         'target': 'Hindi available ang output ng '
                                                                                   'pagsasama. Buksan muli ang '
                                                                                   'Pagsamahin ang mga larawan at '
                                                                                   'subukan ulit.',
                                                                         'type': 'string'},
         'ui_the_attachment_image_is_missing': {'attributes': {'name': 'ui_the_attachment_image_is_missing'},
                                                'target': 'Wala ang nakakabit na larawan.',
                                                'type': 'string'},
         'ui_the_attachment_image_is_not_placed': {'attributes': {'name': 'ui_the_attachment_image_is_not_placed'},
                                                   'target': 'Hindi nakapuwesto ang nakakabit na larawan.',
                                                   'type': 'string'},
         'ui_the_first_image_starts_at_the_top_left': {'attributes': {'name': 'ui_the_first_image_starts_at_the_top_left'},
                                                       'target': 'Nagsisimula ang unang larawan sa kaliwang '
                                                                 'itaas.',
                                                       'type': 'string'},
         'ui_the_gallery_download_is_too_large': {'attributes': {'name': 'ui_the_gallery_download_is_too_large'},
                                                  'target': 'Masyadong malaki ang download mula sa gallery.',
                                                  'type': 'string'},
         'ui_the_gallery_image_is_unavailable': {'attributes': {'name': 'ui_the_gallery_image_is_unavailable'},
                                                 'target': 'Hindi available ang larawan sa gallery.',
                                                 'type': 'string'},
         'ui_the_gallery_redirected_outside_its_supported_hosts': {'attributes': {'name': 'ui_the_gallery_redirected_outside_its_supported_hosts'},
                                                                   'target': 'Nag-redirect ang gallery sa hindi '
                                                                             'sinusuportahang URL ng larawan.',
                                                                   'type': 'string'},
         'ui_the_image_could_not_be_downloaded': {'attributes': {'name': 'ui_the_image_could_not_be_downloaded'},
                                                  'target': 'Hindi ma-download ang larawan.',
                                                  'type': 'string'},
         'ui_the_images_cannot_fit_within_android_s_coordinate': {'attributes': {'name': 'ui_the_images_cannot_fit_within_android_s_coordinate'},
                                                                  'target': 'Hindi kasya ang mga larawan sa '
                                                                            'coordinate range ng Android. Pumili '
                                                                            'ng mas maliit na laki ng larawan.',
                                                                  'type': 'string'},
         'ui_the_normalized_image_dimensions_are_outside_android_s': {'attributes': {'name': 'ui_the_normalized_image_dimensions_are_outside_android_s'},
                                                                      'target': 'Nasa labas ng range ng Android '
                                                                                'ang normalized na sukat ng '
                                                                                'larawan.',
                                                                      'type': 'string'},
         'ui_the_online_gallery_could_not_be_loaded_check': {'attributes': {'name': 'ui_the_online_gallery_could_not_be_loaded_check'},
                                                             'target': 'Hindi ma-load ang online gallery. Tingnan '
                                                                       'ang koneksiyon at subukan muli.',
                                                             'type': 'string'},
         'ui_third_party_notices': {'attributes': {'name': 'ui_third_party_notices'},
                                    'target': 'Mga abiso ng third party',
                                    'type': 'string'},
         'ui_this_image_is_outside_the_supported_catrobat_gallery': {'attributes': {'name': 'ui_this_image_is_outside_the_supported_catrobat_gallery'},
                                                                     'target': 'Wala sa sinusuportahang Catrobat '
                                                                               'gallery ang larawang ito.',
                                                                     'type': 'string'},
         'ui_time_unavailable': {'attributes': {'name': 'ui_time_unavailable'},
                                 'target': 'Hindi available ang oras',
                                 'type': 'string'},
         'ui_toggle_toolbox': {'attributes': {'name': 'ui_toggle_toolbox'},
                               'target': 'I-toggle ang toolbox',
                               'type': 'string'},
         'ui_too_many_gallery_redirects': {'attributes': {'name': 'ui_too_many_gallery_redirects'},
                                           'target': 'Masyadong maraming redirect ng gallery.',
                                           'type': 'string'},
         'ui_tool_option': {'attributes': {'name': 'ui_tool_option'},
                            'target': 'Opsyon ng tool',
                            'type': 'string'},
         'ui_toolbox_and_tool_options_scroll_for_more': {'attributes': {'name': 'ui_toolbox_and_tool_options_scroll_for_more'},
                                                         'target': 'Toolbox at mga opsyon ng tool. Mag-scroll '
                                                                   'para sa higit pa.',
                                                         'type': 'string'},
         'ui_top23': {'attributes': {'name': 'ui_top23'}, 'target': 'Naka-align sa itaas', 'type': 'string'},
         'ui_trim_from_the_original_edges_drag_the_handles': {'attributes': {'name': 'ui_trim_from_the_original_edges_drag_the_handles'},
                                                              'target': 'Bawasan mula sa orihinal na mga gilid. '
                                                                        'I-drag ang mga handle o ilagay ang '
                                                                        'halaga sa ibaba. Hindi nagbabago ang '
                                                                        'source file.',
                                                              'type': 'string'},
         'ui_unplace': {'attributes': {'name': 'ui_unplace'}, 'target': 'Alisin sa puwesto', 'type': 'string'},
         'ui_vertical_hint23': {'attributes': {'name': 'ui_vertical_hint23'},
                                'target': 'Nagsisimula ng bagong column ang bagong linya. Pinananatili ng mga '
                                          'nakatagilid na salita ang mga script na magkakadugtong, kabilang ang '
                                          'Mongolian. Pinananatiling magkakasama ng mga tuwid na character ang '
                                          'combining mark at emoji sequence.',
                                'type': 'string'},
         'ui_vertical_letters23': {'attributes': {'name': 'ui_vertical_letters23'},
                                   'target': 'Mga letra sa vertical na teksto',
                                   'type': 'string'},
         'ui_vertical_lr23': {'attributes': {'name': 'ui_vertical_lr23'},
                              'target': 'Itaas pababa · mga column kaliwa pakanan',
                              'type': 'string'},
         'ui_vertical_mixed23': {'attributes': {'name': 'ui_vertical_mixed23'},
                                 'target': 'Awtomatiko · tuwid na CJK, nakatagilid na mga salita',
                                 'type': 'string'},
         'ui_vertical_rl23': {'attributes': {'name': 'ui_vertical_rl23'},
                              'target': 'Itaas pababa · mga column kanan pakaliwa',
                              'type': 'string'},
         'ui_vertical_sideways23': {'attributes': {'name': 'ui_vertical_sideways23'},
                                    'target': 'Nakatagilid · panatilihing magkakadugtong ang mga salita',
                                    'type': 'string'},
         'ui_vertical_upright23': {'attributes': {'name': 'ui_vertical_upright23'},
                                   'target': 'Tuwid · character kada character',
                                   'type': 'string'},
         'ui_webp_codec_licences': {'attributes': {'name': 'ui_webp_codec_licences'},
                                    'target': 'Mga lisensiya ng WebP codec',
                                    'type': 'string'},
         'ui_wheel': {'attributes': {'name': 'ui_wheel'}, 'target': 'Color wheel', 'type': 'string'},
         'ui_widths': {'attributes': {'name': 'ui_widths'}, 'target': 'Mga lapad', 'type': 'string'},
         'ui_you_can_add_more_images_select_fewer_files': {'attributes': {'name': 'ui_you_can_add_more_images_select_fewer_files'},
                                                           'target': 'Maaari ka pang magdagdag ng %1$s larawan. '
                                                                     'Pumili ng mas kaunting file.',
                                                           'type': 'string'}},
 'kn': {'gallery_copy_credit': {'attributes': {'name': 'gallery_copy_credit'},
                                'target': 'ನಕಲಿಸಿ',
                                'type': 'string'},
        'gallery_use_image': {'attributes': {'name': 'gallery_use_image'},
                              'target': 'Import image',
                              'type': 'string'},
        'ui_advanced': {'attributes': {'name': 'ui_advanced'}, 'target': '"ಸುಧಾರಿತ"', 'type': 'string'},
        'ui_horizontal23': {'attributes': {'name': 'ui_horizontal23'}, 'target': '"ಅಡ್ಡ"', 'type': 'string'},
        'ui_monospace': {'attributes': {'name': 'ui_monospace'}, 'target': 'Monospace', 'type': 'string'},
        'ui_sans_serif': {'attributes': {'name': 'ui_sans_serif'}, 'target': 'Sans Serif', 'type': 'string'},
        'ui_serif': {'attributes': {'name': 'ui_serif'}, 'target': 'Serif', 'type': 'string'},
        'ui_smooth_freehand_strokes': {'attributes': {'name': 'ui_smooth_freehand_strokes'},
                                       'target': 'Smoothing',
                                       'type': 'string'},
        'ui_smooth_pixel_edges_anti_aliasing': {'attributes': {'name': 'ui_smooth_pixel_edges_anti_aliasing'},
                                                'target': 'Antialiasing',
                                                'type': 'string'}},
 'ml-IN': {'gallery_copy_credit': {'attributes': {'name': 'gallery_copy_credit'},
                                   'target': 'പകര്\u200dപ്പ്\u200c',
                                   'type': 'string'},
           'gallery_use_image': {'attributes': {'name': 'gallery_use_image'},
                                 'target': 'Import image',
                                 'type': 'string'},
           'ui_monospace': {'attributes': {'name': 'ui_monospace'}, 'target': 'Monospace', 'type': 'string'},
           'ui_sans_serif': {'attributes': {'name': 'ui_sans_serif'}, 'target': 'Sans Serif', 'type': 'string'},
           'ui_serif': {'attributes': {'name': 'ui_serif'}, 'target': 'Serif', 'type': 'string'},
           'ui_smooth_freehand_strokes': {'attributes': {'name': 'ui_smooth_freehand_strokes'},
                                          'target': 'Smoothing',
                                          'type': 'string'},
           'ui_smooth_pixel_edges_anti_aliasing': {'attributes': {'name': 'ui_smooth_pixel_edges_anti_aliasing'},
                                                   'target': 'Antialiasing',
                                                   'type': 'string'},
           'ui_wheel': {'attributes': {'name': 'ui_wheel'}, 'target': '"ചക്രം"', 'type': 'string'}}}

ATTRIBUTE_EXCEPTIONS = {'fil': {'language20_device_default': {'formatted': 'false', 'name': 'language20_device_default'},
         'save20_title': {'formatted': 'false', 'name': 'save20_title'},
         'ui_100': {'formatted': 'false', 'name': 'ui_100'},
         'ui_actual_size_100': {'formatted': 'false', 'name': 'ui_actual_size_100'},
         'ui_add_colour26': {'formatted': 'false', 'name': 'ui_add_colour26'},
         'ui_background_colour': {'formatted': 'false', 'name': 'ui_background_colour'},
         'ui_bg': {'formatted': 'false', 'name': 'ui_bg'},
         'ui_bucket_fill': {'formatted': 'false', 'name': 'ui_bucket_fill'},
         'ui_canvas_bounds': {'formatted': 'false', 'name': 'ui_canvas_bounds'},
         'ui_canvas_size': {'formatted': 'false', 'name': 'ui_canvas_size'},
         'ui_category_insert': {'formatted': 'false', 'name': 'ui_category_insert'},
         'ui_category_selection': {'formatted': 'false', 'name': 'ui_category_selection'},
         'ui_clear_image': {'formatted': 'false', 'name': 'ui_clear_image'},
         'ui_colour_tab23': {'formatted': 'false', 'name': 'ui_colour_tab23'},
         'ui_crop_to_selection': {'formatted': 'false', 'name': 'ui_crop_to_selection'},
         'ui_delete_selection': {'formatted': 'false', 'name': 'ui_delete_selection'},
         'ui_draw26': {'formatted': 'false', 'name': 'ui_draw26'},
         'ui_drawing23': {'formatted': 'false', 'name': 'ui_drawing23'},
         'ui_edit_canvas33': {'formatted': 'false', 'name': 'ui_edit_canvas33'},
         'ui_edit_transform33': {'formatted': 'false', 'name': 'ui_edit_transform33'},
         'ui_eraser': {'formatted': 'false', 'name': 'ui_eraser'},
         'ui_export_as23': {'formatted': 'false', 'name': 'ui_export_as23'},
         'ui_export_recovery_copy': {'formatted': 'false', 'name': 'ui_export_recovery_copy'},
         'ui_eyedropper': {'formatted': 'false', 'name': 'ui_eyedropper'},
         'ui_fg': {'formatted': 'false', 'name': 'ui_fg'},
         'ui_fit_selection34': {'formatted': 'false', 'name': 'ui_fit_selection34'},
         'ui_flip_horizontal': {'formatted': 'false', 'name': 'ui_flip_horizontal'},
         'ui_flip_vertical': {'formatted': 'false', 'name': 'ui_flip_vertical'},
         'ui_foreground_colour': {'formatted': 'false', 'name': 'ui_foreground_colour'},
         'ui_from_device34': {'formatted': 'false', 'name': 'ui_from_device34'},
         'ui_hide_editor_controls': {'formatted': 'false', 'name': 'ui_hide_editor_controls'},
         'ui_insert_image_into_canvas': {'formatted': 'false', 'name': 'ui_insert_image_into_canvas'},
         'ui_invert_colours': {'formatted': 'false', 'name': 'ui_invert_colours'},
         'ui_languages23': {'formatted': 'false', 'name': 'ui_languages23'},
         'ui_line_spacing': {'formatted': 'false', 'name': 'ui_line_spacing'},
         'ui_load_image': {'formatted': 'false', 'name': 'ui_load_image'},
         'ui_magnification': {'formatted': 'false', 'name': 'ui_magnification'},
         'ui_menu_edit': {'formatted': 'false', 'name': 'ui_menu_edit'},
         'ui_menu_file': {'formatted': 'false', 'name': 'ui_menu_file'},
         'ui_menu_view': {'formatted': 'false', 'name': 'ui_menu_view'},
         'ui_navigate': {'formatted': 'false', 'name': 'ui_navigate'},
         'ui_new': {'formatted': 'false', 'name': 'ui_new'},
         'ui_original_size34': {'formatted': 'false', 'name': 'ui_original_size34'},
         'ui_other_images34': {'formatted': 'false', 'name': 'ui_other_images34'},
         'ui_quality': {'formatted': 'false', 'name': 'ui_quality'},
         'ui_reset_bw23': {'formatted': 'false', 'name': 'ui_reset_bw23'},
         'ui_resize_image': {'formatted': 'false', 'name': 'ui_resize_image'},
         'ui_rotate_180': {'formatted': 'false', 'name': 'ui_rotate_180'},
         'ui_rotate_90_clockwise': {'formatted': 'false', 'name': 'ui_rotate_90_clockwise'},
         'ui_save': {'formatted': 'false', 'name': 'ui_save'},
         'ui_save_and_share': {'formatted': 'false', 'name': 'ui_save_and_share'},
         'ui_select_all': {'formatted': 'false', 'name': 'ui_select_all'},
         'ui_share_explanation34': {'formatted': 'false', 'name': 'ui_share_explanation34'},
         'ui_show_editor_controls': {'formatted': 'false', 'name': 'ui_show_editor_controls'},
         'ui_swap23': {'formatted': 'false', 'name': 'ui_swap23'},
         'ui_use_50_300': {'formatted': 'false', 'name': 'ui_use_50_300'}},
 'kn': {'ui_100': {'formatted': 'false', 'name': 'ui_100'},
        'ui_actual_size_100': {'formatted': 'false', 'name': 'ui_actual_size_100'},
        'ui_fit_selection34': {'formatted': 'false', 'name': 'ui_fit_selection34'},
        'ui_from_device34': {'formatted': 'false', 'name': 'ui_from_device34'},
        'ui_history_unavailable34': {'formatted': 'false', 'name': 'ui_history_unavailable34'},
        'ui_line_spacing': {'formatted': 'false', 'name': 'ui_line_spacing'},
        'ui_magnification': {'formatted': 'false', 'name': 'ui_magnification'},
        'ui_original_size34': {'formatted': 'false', 'name': 'ui_original_size34'},
        'ui_other_images34': {'formatted': 'false', 'name': 'ui_other_images34'},
        'ui_paste_hint34': {'formatted': 'false', 'name': 'ui_paste_hint34'},
        'ui_quality': {'formatted': 'false', 'name': 'ui_quality'},
        'ui_share_explanation34': {'formatted': 'false', 'name': 'ui_share_explanation34'},
        'ui_use_50_300': {'formatted': 'false', 'name': 'ui_use_50_300'}},
 'ml-IN': {'ui_100': {'formatted': 'false', 'name': 'ui_100'},
           'ui_actual_size_100': {'formatted': 'false', 'name': 'ui_actual_size_100'},
           'ui_fit_selection34': {'formatted': 'false', 'name': 'ui_fit_selection34'},
           'ui_from_device34': {'formatted': 'false', 'name': 'ui_from_device34'},
           'ui_history_unavailable34': {'formatted': 'false', 'name': 'ui_history_unavailable34'},
           'ui_line_spacing': {'formatted': 'false', 'name': 'ui_line_spacing'},
           'ui_magnification': {'formatted': 'false', 'name': 'ui_magnification'},
           'ui_original_size34': {'formatted': 'false', 'name': 'ui_original_size34'},
           'ui_other_images34': {'formatted': 'false', 'name': 'ui_other_images34'},
           'ui_paste_hint34': {'formatted': 'false', 'name': 'ui_paste_hint34'},
           'ui_quality': {'formatted': 'false', 'name': 'ui_quality'},
           'ui_share_explanation34': {'formatted': 'false', 'name': 'ui_share_explanation34'},
           'ui_use_50_300': {'formatted': 'false', 'name': 'ui_use_50_300'}}}

EDIT_COUNTS = {'fil': 5, 'kn': 317, 'ml-IN': 333}

PRIORITY_STATUS = {'fil': {'string/colour_converter_unavailable': 'accept_current_bounded',
         'string/colour_invalid_metadata': 'accept_current_bounded',
         'string/colour_truncated_metadata': 'carry_prior_bounded',
         'string/colour_unsupported_icc_model': 'accept_current_bounded',
         'string/commons_svg_original_size_too_large': 'accept_current_bounded',
         'string/commons_svg_original_size_unavailable': 'carry_optional_current_unmodified',
         'string/formats22_animation_message': 'accept_current_bounded',
         'string/formats22_animation_poster': 'accept_current_bounded',
         'string/formats22_animation_still': 'accept_current_bounded',
         'string/formats22_animation_title': 'accept_current_bounded',
         'string/formats22_animation_unknown': 'accept_current_bounded',
         'string/formats22_ascii_description': 'accept_current_bounded',
         'string/formats22_derived_exported': 'hold_present_unchanged',
         'string/formats22_import_limit': 'accept_current_bounded',
         'string/formats22_open_still': 'accept_current_bounded',
         'string/formats22_pdf_raster_hint': 'accept_current_bounded',
         'string/gallery_credit_could_not_save': 'accept_current_bounded',
         'string/gallery_credit_too_large': 'carry_prior_bounded',
         'string/language20_app_language': 'accept_current_bounded',
         'string/language20_current': 'accept_current_bounded',
         'string/language20_device_default': 'accept_current_bounded',
         'string/language20_settings': 'accept_current_bounded',
         'string/language20_translation_note': 'accept_current_bounded',
         'string/legacy_credits_unreadable': 'accept_current_bounded',
         'string/save20_destination_error': 'accept_current_bounded',
         'string/save20_encoding_budget': 'accept_current_bounded',
         'string/save20_file_format': 'accept_current_bounded',
         'string/save20_file_name': 'accept_current_bounded',
         'string/save20_gif_description': 'accept_current_bounded',
         'string/save20_invalid_name': 'accept_current_bounded',
         'string/save20_lossy_quality_description': 'accept_current_bounded',
         'string/save20_title': 'accept_current_bounded',
         'string/save20_unsupported_image_colour': 'carry_prior_bounded',
         'string/ui_0f_0f_px_1f': 'accept_current_bounded',
         'string/ui_100': 'accept_current_bounded',
         'string/ui_1_px': 'accept_current_wording_only',
         'string/ui_1f_s': 'accept_current_bounded',
         'string/ui_a_separate_recovery_copy_has_been_kept_use': 'accept_current_bounded',
         'string/ui_actual_size_100': 'accept_current_wording_only',
         'string/ui_add_colour26': 'accept_current_bounded',
         'string/ui_add_text': 'accept_current_bounded',
         'string/ui_airbrush': 'accept_current_bounded',
         'string/ui_all': 'accept_current_bounded',
         'string/ui_an_assembly_source_image_is_missing': 'accept_current_bounded',
         'string/ui_android_blocked_the_file_picker': 'accept_current_bounded',
         'string/ui_android_could_not_decode_this_image': 'accept_current_bounded',
         'string/ui_android_could_not_find_a_file_picker_enable': 'accept_current_bounded',
         'string/ui_apply': 'accept_current_bounded',
         'string/ui_apply_bounds': 'accept_current_bounded',
         'string/ui_apply_crop': 'accept_current_bounded',
         'string/ui_assembly_saved': 'accept_current_bounded',
         'string/ui_assembly_source_memory_floor': 'carry_prior_bounded',
         'string/ui_autosave_failed_use_save': 'accept_current_bounded',
         'string/ui_autosave_image_encoding_failed': 'accept_current_bounded',
         'string/ui_autosave_is_paused_to_protect_that_draft_use': 'accept_current_bounded',
         'string/ui_autosave_metadata_is_missing': 'accept_current_bounded',
         'string/ui_autosave_paused_use_save': 'accept_current_bounded',
         'string/ui_autosave_pixels_are_missing': 'accept_current_bounded',
         'string/ui_autosave_pixels_could_not_be_read': 'accept_current_bounded',
         'string/ui_autosave_selection_encoding_failed': 'accept_current_bounded',
         'string/ui_autosaving_draft': 'accept_current_bounded',
         'string/ui_background_colour': 'accept_current_bounded',
         'string/ui_background_edit_colour': 'accept_current_bounded',
         'string/ui_basic_colours': 'accept_current_bounded',
         'string/ui_bg': 'accept_current_bounded',
         'string/ui_bold': 'accept_current_bounded',
         'string/ui_bottom': 'carry_prior_bounded',
         'string/ui_brush': 'accept_current_bounded',
         'string/ui_bucket_fill': 'accept_current_bounded',
         'string/ui_cancel': 'accept_current_bounded',
         'string/ui_cannot_create_the_undo_cache_free_some_device': 'accept_current_bounded',
         'string/ui_canvas_bounds': 'accept_current_bounded',
         'string/ui_canvas_size': 'accept_current_bounded',
         'string/ui_canvas_size_30460e': 'accept_current_bounded',
         'string/ui_canvas_zoom': 'accept_current_bounded',
         'string/ui_canvas_zoom_771f84': 'accept_current_bounded',
         'string/ui_category_brush': 'accept_current_wording_only',
         'string/ui_category_insert': 'accept_current_bounded',
         'string/ui_category_selection': 'accept_current_bounded',
         'string/ui_centred': 'accept_current_bounded',
         'string/ui_choose_a_smaller_output_copy_the_source_images': 'accept_current_bounded',
         'string/ui_choose_a_smaller_size': 'accept_current_bounded',
         'string/ui_choose_at_least_one_image': 'accept_current_bounded',
         'string/ui_choose_dimensions_no_larger_than_the_original': 'accept_current_bounded',
         'string/ui_choose_location': 'accept_current_bounded',
         'string/ui_clear_all': 'accept_current_bounded',
         'string/ui_clear_image': 'accept_current_bounded',
         'string/ui_codec_resize_memory_floor': 'accept_current_bounded',
         'string/ui_collapse_colour_palette': 'accept_current_wording_only',
         'string/ui_collapse_tool_category': 'accept_current_bounded',
         'string/ui_collapse_toolbox': 'accept_current_bounded',
         'string/ui_colour': 'accept_current_bounded',
         'string/ui_colour_palette_tap_for_foreground_hold_for_background': 'accept_current_bounded',
         'string/ui_colour_tab23': 'accept_current_bounded',
         'string/ui_colour_tap_foreground_hold_background': 'accept_current_bounded',
         'string/ui_commit_selection': 'accept_current_bounded',
         'string/ui_copy': 'accept_current_bounded',
         'string/ui_copy_all': 'accept_current_bounded',
         'string/ui_could_not_apply_the_crop': 'accept_current_bounded',
         'string/ui_could_not_complete_the_edit': 'accept_current_bounded',
         'string/ui_could_not_complete_the_operation': 'accept_current_bounded',
         'string/ui_could_not_export_the_recovery_copy': 'accept_current_bounded',
         'string/ui_could_not_open_image': 'accept_current_bounded',
         'string/ui_could_not_place_the_image': 'accept_current_bounded',
         'string/ui_could_not_prepare_the_image': 'accept_current_bounded',
         'string/ui_could_not_save_image': 'accept_current_bounded',
         'string/ui_could_not_save_the_assembly': 'accept_current_bounded',
         'string/ui_could_not_store_the_assembly': 'accept_current_bounded',
         'string/ui_crop': 'accept_current_bounded',
         'string/ui_crop_image': 'accept_current_bounded',
         'string/ui_crop_must_stay_inside_the_canvas': 'accept_current_bounded',
         'string/ui_crop_preview_drag_an_edge_or_corner_drag': 'carry_prior_bounded',
         'string/ui_crop_to_selection': 'accept_current_bounded',
         'string/ui_cut': 'accept_current_bounded',
         'string/ui_d_d_pixels_2f_mp_exceeds_the_current': 'accept_current_bounded',
         'string/ui_d_d_px_d_pixels_2f_mp': 'carry_optional_current_unmodified',
         'string/ui_delete_selection': 'accept_current_bounded',
         'string/ui_discard': 'accept_new_correction_wording_only',
         'string/ui_discard_changes23': 'accept_current_bounded',
         'string/ui_done': 'accept_current_bounded',
         'string/ui_draft_not_saved_yet': 'accept_current_bounded',
         'string/ui_draft_pending': 'accept_current_bounded',
         'string/ui_draft_restored': 'accept_current_bounded',
         'string/ui_draft_saved': 'accept_current_bounded',
         'string/ui_draw26': 'accept_current_bounded',
         'string/ui_draw_again': 'accept_new_correction',
         'string/ui_drawing23': 'accept_current_bounded',
         'string/ui_drawing_canvas_pinch_and_move_two_fingers_to': 'accept_current_bounded',
         'string/ui_drawing_settings': 'accept_current_bounded',
         'string/ui_drawing_settings_d900c6': 'accept_current_bounded',
         'string/ui_edit_background': 'accept_current_wording_only',
         'string/ui_edit_canvas33': 'carry_optional_current_unmodified',
         'string/ui_edit_colour26': 'accept_current_bounded',
         'string/ui_edit_foreground': 'accept_current_wording_only',
         'string/ui_edit_transform33': 'carry_prior_bounded',
         'string/ui_ellipse': 'accept_current_bounded',
         'string/ui_enter_a_number_from_to': 'accept_current_bounded',
         'string/ui_enter_a_positive_size': 'accept_current_bounded',
         'string/ui_enter_a_trim_amount_for_every_edge': 'accept_current_bounded',
         'string/ui_enter_a_whole_number_from_to': 'accept_current_bounded',
         'string/ui_enter_all_four_trim_amounts': 'accept_current_bounded',
         'string/ui_enter_positive_canvas_dimensions_within_android_s_coordinate': 'accept_current_bounded',
         'string/ui_enter_positive_dimensions': 'accept_current_bounded',
         'string/ui_enter_positive_dimensions_no_larger_than_the_original': 'accept_current_bounded',
         'string/ui_enter_positive_dimensions_that_resolve_to_at_least': 'accept_current_bounded',
         'string/ui_enter_positive_image_dimensions': 'accept_current_bounded',
         'string/ui_enter_valid_dimensions': 'accept_current_bounded',
         'string/ui_eraser': 'accept_current_bounded',
         'string/ui_expand_colour_palette': 'accept_current_wording_only',
         'string/ui_expand_tool_category': 'accept_current_bounded',
         'string/ui_expand_toolbox': 'accept_current_bounded',
         'string/ui_export_as23': 'accept_current_bounded',
         'string/ui_export_did_not_save23': 'accept_current_bounded',
         'string/ui_export_explanation23': 'accept_current_bounded',
         'string/ui_export_recovery_copy': 'accept_current_bounded',
         'string/ui_export_recovery_copy_144b8a': 'accept_current_bounded',
         'string/ui_eyedropper': 'accept_current_bounded',
         'string/ui_fg': 'accept_current_bounded',
         'string/ui_fit': 'accept_current_bounded',
         'string/ui_fit_entire_canvas_in_view': 'accept_current_bounded',
         'string/ui_fit_image': 'accept_current_wording_only',
         'string/ui_fit_selection34': 'accept_current_bounded',
         'string/ui_flip_horizontal': 'accept_current_bounded',
         'string/ui_flip_vertical': 'accept_current_bounded',
         'string/ui_font': 'accept_current_bounded',
         'string/ui_font_family': 'accept_current_bounded',
         'string/ui_foreground_background_colour_palette': 'hold_present_unchanged',
         'string/ui_foreground_colour': 'accept_current_bounded',
         'string/ui_foreground_edit_colour': 'accept_current_bounded',
         'string/ui_free_form_select': 'accept_current_bounded',
         'string/ui_from_device34': 'accept_current_bounded',
         'string/ui_full_text_copied': 'accept_current_bounded',
         'string/ui_height': 'accept_current_bounded',
         'string/ui_height_in': 'accept_current_bounded',
         'string/ui_heights': 'accept_current_wording_only',
         'string/ui_hex_rrggbb': 'accept_current_bounded',
         'string/ui_hide_editor_controls': 'accept_current_wording_only',
         'string/ui_higher_quality_usually_makes_a_larger_file_lossless': 'accept_current_bounded',
         'string/ui_history_unavailable34': 'accept_current_bounded',
         'string/ui_image': 'accept_current_bounded',
         'string/ui_insert': 'accept_current_wording_only',
         'string/ui_insert_image_into_canvas': 'accept_current_wording_only',
         'string/ui_invalid_autosave_metadata': 'accept_current_bounded',
         'string/ui_invalid_colour': 'accept_current_bounded',
         'string/ui_invalid_selection_outline': 'accept_current_bounded',
         'string/ui_invert_colours': 'accept_current_bounded',
         'string/ui_italic': 'accept_current_bounded',
         'string/ui_keep_editing23': 'accept_current_bounded',
         'string/ui_keeps_pixels_at_the_top_left_smaller_canvas': 'carry_prior_bounded',
         'string/ui_languages23': 'accept_current_bounded',
         'string/ui_left': 'carry_prior_bounded',
         'string/ui_left_aligned': 'accept_current_bounded',
         'string/ui_left_arrow_collapse': 'accept_current_wording_only',
         'string/ui_line': 'accept_current_bounded',
         'string/ui_line_spacing': 'accept_current_bounded',
         'string/ui_load_image': 'accept_current_bounded',
         'string/ui_lock_aspect_ratio': 'accept_current_bounded',
         'string/ui_lock_proportions': 'accept_current_bounded',
         'string/ui_magnification': 'accept_current_bounded',
         'string/ui_main23': 'accept_current_wording_only',
         'string/ui_menu': 'accept_current_wording_only',
         'string/ui_menu_colours': 'accept_current_wording_only',
         'string/ui_menu_edit': 'accept_current_bounded',
         'string/ui_menu_file': 'accept_current_bounded',
         'string/ui_menu_help': 'accept_current_bounded',
         'string/ui_menu_image': 'accept_current_bounded',
         'string/ui_menu_view': 'accept_current_bounded',
         'string/ui_navigate': 'accept_current_bounded',
         'string/ui_new': 'accept_current_bounded',
         'string/ui_new_colour': 'accept_current_wording_only',
         'string/ui_new_image': 'accept_current_bounded',
         'string/ui_no_readable_image_data': 'accept_current_bounded',
         'string/ui_no_resize_fits_decoder_memory': 'carry_prior_bounded',
         'string/ui_none': 'accept_current_bounded',
         'string/ui_not_enough_memory_for_this_operation_the_assembly': 'accept_current_bounded',
         'string/ui_not_enough_memory_to_finish_opening_this_image': 'accept_current_bounded',
         'string/ui_not_enough_memory_to_inspect_this_image': 'accept_current_bounded',
         'string/ui_not_enough_memory_to_save_in_this_format': 'accept_current_bounded',
         'string/ui_numeric_slider_value': 'accept_current_bounded',
         'string/ui_ok': 'accept_current_bounded',
         'string/ui_original_size34': 'accept_current_bounded',
         'string/ui_other_images34': 'accept_current_bounded',
         'string/ui_outline': 'accept_current_bounded',
         'string/ui_palette': 'accept_current_bounded',
         'string/ui_paste': 'accept_current_bounded',
         'string/ui_paste_hint34': 'accept_current_bounded',
         'string/ui_pencil': 'accept_current_bounded',
         'string/ui_percent': 'accept_current_bounded',
         'string/ui_percent_fd8671': 'accept_current_bounded',
         'string/ui_pinch_and_pan_mode': 'accept_current_wording_only',
         'string/ui_pixels': 'accept_current_bounded',
         'string/ui_pixels_6ec9c2': 'accept_current_bounded',
         'string/ui_place_text': 'accept_current_bounded',
         'string/ui_please_try_again': 'accept_current_bounded',
         'string/ui_please_wait_for_the_current_operation': 'accept_current_bounded',
         'string/ui_png_encoding_failed': 'accept_current_bounded',
         'string/ui_polygon': 'accept_current_bounded',
         'string/ui_preview': 'accept_current_bounded',
         'string/ui_previous_draft_kept_for_recovery': 'accept_current_bounded',
         'string/ui_px': 'accept_current_bounded',
         'string/ui_px_724eb3': 'accept_current_bounded',
         'string/ui_ready': 'accept_current_bounded',
         'string/ui_recovered_image': 'accept_current_bounded',
         'string/ui_recovery_copy_exported_extract_canvas_png_from_the': 'accept_current_bounded',
         'string/ui_rectangle': 'accept_current_bounded',
         'string/ui_rectangle_select': 'accept_current_bounded',
         'string/ui_redo': 'accept_current_bounded',
         'string/ui_remove': 'accept_current_bounded',
         'string/ui_reset_bw23': 'accept_current_bounded',
         'string/ui_reset_crop': 'accept_current_bounded',
         'string/ui_reset_to_black_white': 'accept_current_wording_only',
         'string/ui_resize_and_load': 'accept_current_bounded',
         'string/ui_resize_image': 'accept_current_bounded',
         'string/ui_resize_image_ab28be': 'accept_current_bounded',
         'string/ui_resize_large_image': 'accept_current_bounded',
         'string/ui_resize_the_copy': 'accept_current_bounded',
         'string/ui_right': 'carry_prior_bounded',
         'string/ui_right_aligned': 'accept_current_bounded',
         'string/ui_rotate': 'accept_current_bounded',
         'string/ui_rotate_180': 'accept_current_bounded',
         'string/ui_rotate_90_clockwise': 'accept_current_bounded',
         'string/ui_sampled_resize_memory_explanation': 'carry_prior_bounded',
         'string/ui_save': 'accept_current_bounded',
         'string/ui_save_a5d0d9': 'carry_optional_current_unmodified',
         'string/ui_save_and_share': 'accept_current_bounded',
         'string/ui_save_and_share_41edb4': 'accept_current_bounded',
         'string/ui_save_as': 'hold_present_unchanged',
         'string/ui_save_as_jpeg': 'hold_present_unchanged',
         'string/ui_save_as_jpeg_xl': 'hold_present_unchanged',
         'string/ui_save_as_png': 'hold_present_unchanged',
         'string/ui_save_explanation23': 'accept_current_bounded',
         'string/ui_save_png': 'accept_current_bounded',
         'string/ui_save_your_changes': 'accept_current_bounded',
         'string/ui_saved': 'accept_current_bounded',
         'string/ui_scales_the_image_unlock_the_ratio_to_stretch': 'accept_new_correction',
         'string/ui_select_all': 'accept_current_bounded',
         'string/ui_select_an_area': 'accept_current_bounded',
         'string/ui_select_an_area_first': 'accept_current_bounded',
         'string/ui_selected_colour23': 'accept_current_bounded',
         'string/ui_selection_dimensions_are_too_large': 'accept_current_bounded',
         'string/ui_share_explanation34': 'accept_current_bounded',
         'string/ui_share_saved_image': 'accept_current_bounded',
         'string/ui_show_all': 'accept_current_bounded',
         'string/ui_show_controls': 'accept_current_bounded',
         'string/ui_show_editor_controls': 'accept_current_wording_only',
         'string/ui_show_magnified_drawing_preview': 'accept_current_bounded',
         'string/ui_size_pixels': 'accept_current_bounded',
         'string/ui_size_px': 'accept_current_bounded',
         'string/ui_solid_fill': 'accept_new_correction',
         'string/ui_swap23': 'accept_current_bounded',
         'string/ui_swap_foreground_background': 'accept_current_wording_only',
         'string/ui_tap_an_image_first': 'accept_current_bounded',
         'string/ui_tap_canvas_to_type': 'accept_current_bounded',
         'string/ui_tap_to_type_a_number': 'accept_current_bounded',
         'string/ui_text': 'accept_current_bounded',
         'string/ui_text_alignment': 'accept_current_bounded',
         'string/ui_text_direction23': 'accept_current_bounded',
         'string/ui_the_crop_must_contain_at_least_one_pixel': 'accept_current_bounded',
         'string/ui_the_crop_must_stay_inside_the_image': 'accept_current_bounded',
         'string/ui_the_decoder_and_editing_buffers_need_about_the': 'accept_current_bounded',
         'string/ui_the_draft_is_saving_try_again_shortly': 'accept_current_bounded',
         'string/ui_the_encoder_did_not_finish': 'accept_current_bounded',
         'string/ui_the_full_image_and_working_buffers_exceed_the': 'carry_optional_current_unmodified',
         'string/ui_the_image_was_saved_but_android_could_not': 'accept_current_bounded',
         'string/ui_the_picker_returned_no_file_please_choose_the': 'accept_current_bounded',
         'string/ui_the_picker_returned_no_files': 'accept_current_bounded',
         'string/ui_the_previous_draft_could_not_be_moved_to': 'accept_current_bounded',
         'string/ui_the_previous_draft_could_not_be_preserved_separately': 'accept_current_bounded',
         'string/ui_the_previous_draft_could_not_be_restored': 'accept_current_bounded',
         'string/ui_the_previous_draft_needs_more_memory_to_reopen': 'accept_current_bounded',
         'string/ui_the_saved_assembly_could_not_be_opened': 'accept_current_bounded',
         'string/ui_the_selected_location_is_not_writable': 'accept_current_bounded',
         'string/ui_the_selected_provider_did_not_return_any_image': 'accept_current_bounded',
         'string/ui_the_trim_would_remove_the_entire_image': 'accept_current_bounded',
         'string/ui_the_undo_cache_is_damaged': 'accept_current_bounded',
         'string/ui_there_is_not_enough_memory_for_this_operation': 'accept_current_bounded',
         'string/ui_this_file_is_not_a_supported_image_use': 'accept_current_bounded',
         'string/ui_this_location_is_not_writable': 'accept_current_bounded',
         'string/ui_tolerance': 'accept_current_bounded',
         'string/ui_too_large_for_the_current_budget_reduce_the': 'accept_current_bounded',
         'string/ui_tool_categories': 'accept_current_wording_only',
         'string/ui_trim_amounts_must_be_zero_or_greater': 'accept_current_bounded',
         'string/ui_trim_amounts_must_fit_inside_each_image_use': 'accept_current_bounded',
         'string/ui_trim_expand_canvas_by_touch': 'accept_current_wording_only',
         'string/ui_try_a_different_file_or_location': 'accept_current_bounded',
         'string/ui_type_text': 'accept_current_bounded',
         'string/ui_underline': 'accept_current_bounded',
         'string/ui_undo': 'accept_current_bounded',
         'string/ui_unexpected_data_in_the_undo_cache': 'accept_current_bounded',
         'string/ui_untitled': 'accept_current_bounded',
         'string/ui_use_1_1024_pixels': 'accept_current_bounded',
         'string/ui_use_50_300': 'accept_current_bounded',
         'string/ui_use_a_positive_target_dimension': 'accept_current_bounded',
         'string/ui_use_colour': 'accept_current_bounded',
         'string/ui_use_rrggbb': 'accept_current_bounded',
         'string/ui_watercolor': 'accept_current_bounded',
         'string/ui_width': 'accept_current_bounded',
         'string/ui_working': 'accept_current_bounded',
         'string/ui_your_current_image_has_unsaved_changes': 'accept_current_bounded',
         'string/ui_zoom_in': 'accept_current_bounded',
         'string/ui_zoom_out': 'accept_current_bounded'},
 'kn': {'string/colour_converter_unavailable': 'accept_new_active',
        'string/colour_invalid_metadata': 'accept_new_active',
        'string/colour_truncated_metadata': 'accept_new_active',
        'string/colour_unsupported_icc_model': 'accept_new_active',
        'string/commons_svg_original_size_too_large': 'accept_new_active',
        'string/commons_svg_original_size_unavailable': 'accept_new_active',
        'string/formats22_animation_message': 'accept_new_active',
        'string/formats22_animation_poster': 'accept_new_active',
        'string/formats22_animation_still': 'accept_new_active',
        'string/formats22_animation_title': 'accept_new_active',
        'string/formats22_animation_unknown': 'accept_new_active',
        'string/formats22_ascii_description': 'accept_new_active',
        'string/formats22_derived_exported': 'hold_absent',
        'string/formats22_import_limit': 'accept_new_active',
        'string/formats22_open_still': 'accept_new_active',
        'string/formats22_pdf_raster_hint': 'accept_new_active',
        'string/gallery_credit_could_not_save': 'accept_new_active',
        'string/gallery_credit_too_large': 'accept_new_active',
        'string/language20_app_language': 'accept_new_active',
        'string/language20_current': 'accept_new_active',
        'string/language20_device_default': 'accept_new_active',
        'string/language20_settings': 'accept_current_bounded',
        'string/language20_translation_note': 'accept_new_active',
        'string/legacy_credits_unreadable': 'accept_new_active',
        'string/save20_destination_error': 'accept_new_active',
        'string/save20_encoding_budget': 'accept_new_active',
        'string/save20_file_format': 'accept_current_correction_active',
        'string/save20_file_name': 'accept_current_bounded',
        'string/save20_gif_description': 'accept_new_active',
        'string/save20_invalid_name': 'accept_new_active',
        'string/save20_lossy_quality_description': 'accept_new_active',
        'string/save20_title': 'accept_new_active',
        'string/save20_unsupported_image_colour': 'accept_new_active',
        'string/ui_0f_0f_px_1f': 'accept_new_active',
        'string/ui_100': 'accept_new_active',
        'string/ui_1_px': 'accept_new_wording_only',
        'string/ui_1f_s': 'accept_new_active',
        'string/ui_a_separate_recovery_copy_has_been_kept_use': 'accept_new_active',
        'string/ui_actual_size_100': 'accept_new_wording_only',
        'string/ui_add_colour26': 'accept_new_active',
        'string/ui_add_text': 'accept_new_active',
        'string/ui_airbrush': 'accept_current_correction_active',
        'string/ui_all': 'accept_new_active',
        'string/ui_an_assembly_source_image_is_missing': 'accept_new_active',
        'string/ui_android_blocked_the_file_picker': 'accept_new_active',
        'string/ui_android_could_not_decode_this_image': 'accept_new_active',
        'string/ui_android_could_not_find_a_file_picker_enable': 'accept_new_active',
        'string/ui_apply': 'accept_current_correction_active',
        'string/ui_apply_bounds': 'accept_new_active',
        'string/ui_apply_crop': 'accept_new_active',
        'string/ui_assembly_saved': 'accept_new_active',
        'string/ui_assembly_source_memory_floor': 'accept_new_active',
        'string/ui_autosave_failed_use_save': 'accept_new_active',
        'string/ui_autosave_image_encoding_failed': 'accept_new_active',
        'string/ui_autosave_is_paused_to_protect_that_draft_use': 'accept_new_active',
        'string/ui_autosave_metadata_is_missing': 'accept_new_active',
        'string/ui_autosave_paused_use_save': 'accept_new_active',
        'string/ui_autosave_pixels_are_missing': 'accept_new_active',
        'string/ui_autosave_pixels_could_not_be_read': 'accept_new_active',
        'string/ui_autosave_selection_encoding_failed': 'accept_new_active',
        'string/ui_autosaving_draft': 'accept_new_active',
        'string/ui_background_colour': 'accept_new_active',
        'string/ui_background_edit_colour': 'accept_new_active',
        'string/ui_basic_colours': 'accept_new_active',
        'string/ui_bg': 'accept_new_active',
        'string/ui_bold': 'accept_new_active',
        'string/ui_bottom': 'accept_new_active',
        'string/ui_brush': 'accept_current_correction_active',
        'string/ui_bucket_fill': 'accept_current_correction_active',
        'string/ui_cancel': 'accept_current_bounded',
        'string/ui_cannot_create_the_undo_cache_free_some_device': 'accept_new_active',
        'string/ui_canvas_bounds': 'accept_new_active',
        'string/ui_canvas_size': 'accept_current_bounded',
        'string/ui_canvas_size_30460e': 'accept_current_bounded',
        'string/ui_canvas_zoom': 'accept_new_active',
        'string/ui_canvas_zoom_771f84': 'accept_new_active',
        'string/ui_category_brush': 'accept_current_correction_wording_only',
        'string/ui_category_insert': 'accept_current_bounded',
        'string/ui_category_selection': 'accept_current_bounded',
        'string/ui_centred': 'accept_new_active',
        'string/ui_choose_a_smaller_output_copy_the_source_images': 'accept_new_active',
        'string/ui_choose_a_smaller_size': 'accept_new_active',
        'string/ui_choose_at_least_one_image': 'accept_new_active',
        'string/ui_choose_dimensions_no_larger_than_the_original': 'accept_new_active',
        'string/ui_choose_location': 'accept_new_active',
        'string/ui_clear_all': 'accept_new_active',
        'string/ui_clear_image': 'accept_new_active',
        'string/ui_codec_resize_memory_floor': 'accept_new_active',
        'string/ui_collapse_colour_palette': 'accept_new_wording_only',
        'string/ui_collapse_tool_category': 'accept_new_active',
        'string/ui_collapse_toolbox': 'accept_new_active',
        'string/ui_colour': 'accept_new_active',
        'string/ui_colour_palette_tap_for_foreground_hold_for_background': 'accept_new_active',
        'string/ui_colour_tab23': 'accept_new_active',
        'string/ui_colour_tap_foreground_hold_background': 'accept_new_active',
        'string/ui_commit_selection': 'accept_new_active',
        'string/ui_copy': 'accept_current_bounded',
        'string/ui_copy_all': 'accept_new_active',
        'string/ui_could_not_apply_the_crop': 'accept_new_active',
        'string/ui_could_not_complete_the_edit': 'accept_new_active',
        'string/ui_could_not_complete_the_operation': 'accept_new_active',
        'string/ui_could_not_export_the_recovery_copy': 'accept_new_active',
        'string/ui_could_not_open_image': 'accept_new_active',
        'string/ui_could_not_place_the_image': 'accept_new_active',
        'string/ui_could_not_prepare_the_image': 'accept_new_active',
        'string/ui_could_not_save_image': 'accept_new_active',
        'string/ui_could_not_save_the_assembly': 'accept_new_active',
        'string/ui_could_not_store_the_assembly': 'accept_new_active',
        'string/ui_crop': 'accept_new_active',
        'string/ui_crop_image': 'accept_new_active',
        'string/ui_crop_must_stay_inside_the_canvas': 'accept_new_active',
        'string/ui_crop_preview_drag_an_edge_or_corner_drag': 'accept_new_active',
        'string/ui_crop_to_selection': 'accept_new_active',
        'string/ui_cut': 'accept_current_bounded',
        'string/ui_d_d_pixels_2f_mp_exceeds_the_current': 'accept_new_active',
        'string/ui_d_d_px_d_pixels_2f_mp': 'accept_new_active',
        'string/ui_delete_selection': 'accept_new_active',
        'string/ui_discard': 'accept_current_correction_wording_only',
        'string/ui_discard_changes23': 'accept_current_bounded',
        'string/ui_done': 'accept_current_correction_active',
        'string/ui_draft_not_saved_yet': 'accept_new_active',
        'string/ui_draft_pending': 'accept_new_active',
        'string/ui_draft_restored': 'accept_new_active',
        'string/ui_draft_saved': 'accept_new_active',
        'string/ui_draw26': 'accept_new_active',
        'string/ui_draw_again': 'accept_new_active',
        'string/ui_drawing23': 'accept_new_active',
        'string/ui_drawing_canvas_pinch_and_move_two_fingers_to': 'accept_new_active',
        'string/ui_drawing_settings': 'accept_new_active',
        'string/ui_drawing_settings_d900c6': 'accept_new_active',
        'string/ui_edit_background': 'accept_current_wording_only',
        'string/ui_edit_canvas33': 'accept_new_active',
        'string/ui_edit_colour26': 'accept_new_active',
        'string/ui_edit_foreground': 'accept_current_wording_only',
        'string/ui_edit_transform33': 'accept_new_active',
        'string/ui_ellipse': 'accept_current_correction_active',
        'string/ui_enter_a_number_from_to': 'accept_new_active',
        'string/ui_enter_a_positive_size': 'accept_new_active',
        'string/ui_enter_a_trim_amount_for_every_edge': 'accept_new_active',
        'string/ui_enter_a_whole_number_from_to': 'accept_new_active',
        'string/ui_enter_all_four_trim_amounts': 'accept_new_active',
        'string/ui_enter_positive_canvas_dimensions_within_android_s_coordinate': 'accept_new_active',
        'string/ui_enter_positive_dimensions': 'accept_new_active',
        'string/ui_enter_positive_dimensions_no_larger_than_the_original': 'accept_new_active',
        'string/ui_enter_positive_dimensions_that_resolve_to_at_least': 'accept_new_active',
        'string/ui_enter_positive_image_dimensions': 'accept_new_active',
        'string/ui_enter_valid_dimensions': 'accept_new_active',
        'string/ui_eraser': 'accept_current_correction_active',
        'string/ui_expand_colour_palette': 'accept_new_wording_only',
        'string/ui_expand_tool_category': 'accept_new_active',
        'string/ui_expand_toolbox': 'accept_new_active',
        'string/ui_export_as23': 'accept_new_active',
        'string/ui_export_did_not_save23': 'accept_new_active',
        'string/ui_export_explanation23': 'accept_new_active',
        'string/ui_export_recovery_copy': 'accept_new_active',
        'string/ui_export_recovery_copy_144b8a': 'accept_new_active',
        'string/ui_eyedropper': 'accept_current_correction_active',
        'string/ui_fg': 'accept_new_active',
        'string/ui_fit': 'accept_new_active',
        'string/ui_fit_entire_canvas_in_view': 'accept_new_active',
        'string/ui_fit_image': 'accept_new_wording_only',
        'string/ui_fit_selection34': 'accept_new_active',
        'string/ui_flip_horizontal': 'accept_current_correction_active',
        'string/ui_flip_vertical': 'accept_current_correction_active',
        'string/ui_font': 'accept_new_active',
        'string/ui_font_family': 'accept_new_active',
        'string/ui_foreground_background_colour_palette': 'hold_absent',
        'string/ui_foreground_colour': 'accept_new_active',
        'string/ui_foreground_edit_colour': 'accept_new_active',
        'string/ui_free_form_select': 'accept_new_active',
        'string/ui_from_device34': 'accept_new_active',
        'string/ui_full_text_copied': 'accept_new_active',
        'string/ui_height': 'accept_new_active',
        'string/ui_height_in': 'accept_new_active',
        'string/ui_heights': 'accept_new_wording_only',
        'string/ui_hex_rrggbb': 'accept_new_active',
        'string/ui_hide_editor_controls': 'accept_new_wording_only',
        'string/ui_higher_quality_usually_makes_a_larger_file_lossless': 'accept_new_active',
        'string/ui_history_unavailable34': 'accept_new_active',
        'string/ui_image': 'accept_current_bounded',
        'string/ui_insert': 'accept_current_wording_only',
        'string/ui_insert_image_into_canvas': 'accept_new_wording_only',
        'string/ui_invalid_autosave_metadata': 'accept_new_active',
        'string/ui_invalid_colour': 'accept_new_active',
        'string/ui_invalid_selection_outline': 'accept_new_active',
        'string/ui_invert_colours': 'accept_new_active',
        'string/ui_italic': 'accept_new_active',
        'string/ui_keep_editing23': 'accept_current_correction_active',
        'string/ui_keeps_pixels_at_the_top_left_smaller_canvas': 'accept_new_active',
        'string/ui_languages23': 'accept_new_active',
        'string/ui_left': 'accept_new_active',
        'string/ui_left_aligned': 'accept_new_active',
        'string/ui_left_arrow_collapse': 'accept_new_wording_only',
        'string/ui_line': 'accept_current_correction_active',
        'string/ui_line_spacing': 'accept_new_active',
        'string/ui_load_image': 'accept_new_active',
        'string/ui_lock_aspect_ratio': 'accept_new_active',
        'string/ui_lock_proportions': 'accept_new_active',
        'string/ui_magnification': 'accept_new_active',
        'string/ui_main23': 'accept_new_wording_only',
        'string/ui_menu': 'accept_new_wording_only',
        'string/ui_menu_colours': 'accept_current_correction_wording_only',
        'string/ui_menu_edit': 'accept_new_active',
        'string/ui_menu_file': 'accept_new_active',
        'string/ui_menu_help': 'accept_current_correction_active',
        'string/ui_menu_image': 'accept_new_active',
        'string/ui_menu_view': 'accept_new_active',
        'string/ui_navigate': 'accept_new_active',
        'string/ui_new': 'accept_new_active',
        'string/ui_new_colour': 'accept_new_wording_only',
        'string/ui_new_image': 'accept_current_correction_active',
        'string/ui_no_readable_image_data': 'accept_new_active',
        'string/ui_no_resize_fits_decoder_memory': 'accept_new_active',
        'string/ui_none': 'accept_new_active',
        'string/ui_not_enough_memory_for_this_operation_the_assembly': 'accept_new_active',
        'string/ui_not_enough_memory_to_finish_opening_this_image': 'accept_new_active',
        'string/ui_not_enough_memory_to_inspect_this_image': 'accept_new_active',
        'string/ui_not_enough_memory_to_save_in_this_format': 'accept_new_active',
        'string/ui_numeric_slider_value': 'accept_new_active',
        'string/ui_ok': 'accept_current_bounded',
        'string/ui_original_size34': 'accept_new_active',
        'string/ui_other_images34': 'accept_new_active',
        'string/ui_outline': 'accept_current_correction_active',
        'string/ui_palette': 'accept_current_bounded',
        'string/ui_paste': 'accept_current_bounded',
        'string/ui_paste_hint34': 'accept_new_active',
        'string/ui_pencil': 'accept_current_bounded',
        'string/ui_percent': 'accept_new_active',
        'string/ui_percent_fd8671': 'accept_new_active',
        'string/ui_pinch_and_pan_mode': 'hold_absent',
        'string/ui_pixels': 'accept_current_bounded',
        'string/ui_pixels_6ec9c2': 'accept_current_bounded',
        'string/ui_place_text': 'accept_new_active',
        'string/ui_please_try_again': 'accept_new_active',
        'string/ui_please_wait_for_the_current_operation': 'accept_new_active',
        'string/ui_png_encoding_failed': 'accept_new_active',
        'string/ui_polygon': 'accept_new_active',
        'string/ui_preview': 'accept_current_bounded',
        'string/ui_previous_draft_kept_for_recovery': 'accept_new_active',
        'string/ui_px': 'accept_new_active',
        'string/ui_px_724eb3': 'accept_new_active',
        'string/ui_ready': 'accept_current_bounded',
        'string/ui_recovered_image': 'accept_new_active',
        'string/ui_recovery_copy_exported_extract_canvas_png_from_the': 'accept_new_active',
        'string/ui_rectangle': 'accept_current_bounded',
        'string/ui_rectangle_select': 'accept_current_bounded',
        'string/ui_redo': 'accept_current_correction_active',
        'string/ui_remove': 'accept_current_bounded',
        'string/ui_reset_bw23': 'accept_new_active',
        'string/ui_reset_crop': 'accept_new_active',
        'string/ui_reset_to_black_white': 'accept_new_wording_only',
        'string/ui_resize_and_load': 'accept_new_active',
        'string/ui_resize_image': 'accept_new_active',
        'string/ui_resize_image_ab28be': 'accept_new_active',
        'string/ui_resize_large_image': 'accept_new_active',
        'string/ui_resize_the_copy': 'accept_new_active',
        'string/ui_right': 'accept_new_active',
        'string/ui_right_aligned': 'accept_new_active',
        'string/ui_rotate': 'accept_current_bounded',
        'string/ui_rotate_180': 'accept_new_active',
        'string/ui_rotate_90_clockwise': 'accept_new_active',
        'string/ui_sampled_resize_memory_explanation': 'accept_new_active',
        'string/ui_save': 'accept_current_correction_active',
        'string/ui_save_a5d0d9': 'accept_current_correction_active',
        'string/ui_save_and_share': 'accept_new_active',
        'string/ui_save_and_share_41edb4': 'accept_new_active',
        'string/ui_save_as': 'hold_absent',
        'string/ui_save_as_jpeg': 'hold_absent',
        'string/ui_save_as_jpeg_xl': 'hold_absent',
        'string/ui_save_as_png': 'hold_absent',
        'string/ui_save_explanation23': 'accept_new_active',
        'string/ui_save_png': 'accept_new_active',
        'string/ui_save_your_changes': 'accept_current_correction_active',
        'string/ui_saved': 'accept_new_active',
        'string/ui_scales_the_image_unlock_the_ratio_to_stretch': 'accept_new_active',
        'string/ui_select_all': 'accept_current_bounded',
        'string/ui_select_an_area': 'accept_new_active',
        'string/ui_select_an_area_first': 'accept_new_active',
        'string/ui_selected_colour23': 'accept_new_active',
        'string/ui_selection_dimensions_are_too_large': 'accept_new_active',
        'string/ui_share_explanation34': 'accept_new_active',
        'string/ui_share_saved_image': 'accept_new_active',
        'string/ui_show_all': 'accept_new_active',
        'string/ui_show_controls': 'accept_new_active',
        'string/ui_show_editor_controls': 'accept_new_wording_only',
        'string/ui_show_magnified_drawing_preview': 'accept_new_active',
        'string/ui_size_pixels': 'accept_new_active',
        'string/ui_size_px': 'accept_new_active',
        'string/ui_solid_fill': 'accept_current_correction_active',
        'string/ui_swap23': 'accept_new_active',
        'string/ui_swap_foreground_background': 'accept_new_wording_only',
        'string/ui_tap_an_image_first': 'accept_new_active',
        'string/ui_tap_canvas_to_type': 'accept_new_active',
        'string/ui_tap_to_type_a_number': 'accept_new_active',
        'string/ui_text': 'accept_current_bounded',
        'string/ui_text_alignment': 'accept_new_active',
        'string/ui_text_direction23': 'accept_new_active',
        'string/ui_the_crop_must_contain_at_least_one_pixel': 'accept_new_active',
        'string/ui_the_crop_must_stay_inside_the_image': 'accept_new_active',
        'string/ui_the_decoder_and_editing_buffers_need_about_the': 'accept_new_active',
        'string/ui_the_draft_is_saving_try_again_shortly': 'accept_new_active',
        'string/ui_the_encoder_did_not_finish': 'accept_new_active',
        'string/ui_the_full_image_and_working_buffers_exceed_the': 'accept_new_active',
        'string/ui_the_image_was_saved_but_android_could_not': 'accept_new_active',
        'string/ui_the_picker_returned_no_file_please_choose_the': 'accept_new_active',
        'string/ui_the_picker_returned_no_files': 'accept_new_active',
        'string/ui_the_previous_draft_could_not_be_moved_to': 'accept_new_active',
        'string/ui_the_previous_draft_could_not_be_preserved_separately': 'accept_new_active',
        'string/ui_the_previous_draft_could_not_be_restored': 'accept_new_active',
        'string/ui_the_previous_draft_needs_more_memory_to_reopen': 'accept_new_active',
        'string/ui_the_saved_assembly_could_not_be_opened': 'accept_new_active',
        'string/ui_the_selected_location_is_not_writable': 'accept_new_active',
        'string/ui_the_selected_provider_did_not_return_any_image': 'accept_new_active',
        'string/ui_the_trim_would_remove_the_entire_image': 'accept_new_active',
        'string/ui_the_undo_cache_is_damaged': 'accept_new_active',
        'string/ui_there_is_not_enough_memory_for_this_operation': 'accept_new_active',
        'string/ui_this_file_is_not_a_supported_image_use': 'accept_new_active',
        'string/ui_this_location_is_not_writable': 'accept_new_active',
        'string/ui_tolerance': 'accept_new_active',
        'string/ui_too_large_for_the_current_budget_reduce_the': 'accept_new_active',
        'string/ui_tool_categories': 'accept_new_wording_only',
        'string/ui_trim_amounts_must_be_zero_or_greater': 'accept_new_active',
        'string/ui_trim_amounts_must_fit_inside_each_image_use': 'accept_new_active',
        'string/ui_trim_expand_canvas_by_touch': 'accept_new_wording_only',
        'string/ui_try_a_different_file_or_location': 'accept_new_active',
        'string/ui_type_text': 'accept_new_active',
        'string/ui_underline': 'accept_new_active',
        'string/ui_undo': 'accept_current_correction_active',
        'string/ui_unexpected_data_in_the_undo_cache': 'accept_new_active',
        'string/ui_untitled': 'accept_current_bounded',
        'string/ui_use_1_1024_pixels': 'accept_new_active',
        'string/ui_use_50_300': 'accept_new_active',
        'string/ui_use_a_positive_target_dimension': 'accept_new_active',
        'string/ui_use_colour': 'accept_new_active',
        'string/ui_use_rrggbb': 'accept_new_active',
        'string/ui_watercolor': 'accept_current_correction_active',
        'string/ui_width': 'accept_new_active',
        'string/ui_working': 'accept_new_active',
        'string/ui_your_current_image_has_unsaved_changes': 'accept_new_active',
        'string/ui_zoom_in': 'accept_current_bounded',
        'string/ui_zoom_out': 'accept_current_bounded'},
 'ml-IN': {'string/colour_converter_unavailable': 'accept_new_active',
           'string/colour_invalid_metadata': 'accept_new_active',
           'string/colour_truncated_metadata': 'accept_new_active',
           'string/colour_unsupported_icc_model': 'accept_new_active',
           'string/commons_svg_original_size_too_large': 'accept_new_active',
           'string/commons_svg_original_size_unavailable': 'accept_new_active',
           'string/formats22_animation_message': 'accept_new_active',
           'string/formats22_animation_poster': 'accept_new_active',
           'string/formats22_animation_still': 'accept_new_active',
           'string/formats22_animation_title': 'accept_new_active',
           'string/formats22_animation_unknown': 'accept_new_active',
           'string/formats22_ascii_description': 'accept_new_active',
           'string/formats22_derived_exported': 'hold_absent',
           'string/formats22_import_limit': 'accept_new_active',
           'string/formats22_open_still': 'accept_new_active',
           'string/formats22_pdf_raster_hint': 'accept_new_active',
           'string/gallery_credit_could_not_save': 'accept_new_active',
           'string/gallery_credit_too_large': 'accept_new_active',
           'string/language20_app_language': 'accept_current_correction_active',
           'string/language20_current': 'accept_new_active',
           'string/language20_device_default': 'accept_new_active',
           'string/language20_settings': 'accept_current_correction_active',
           'string/language20_translation_note': 'accept_new_active',
           'string/legacy_credits_unreadable': 'accept_new_active',
           'string/save20_destination_error': 'accept_new_active',
           'string/save20_encoding_budget': 'accept_new_active',
           'string/save20_file_format': 'accept_current_correction_active',
           'string/save20_file_name': 'accept_current_correction_active',
           'string/save20_gif_description': 'accept_new_active',
           'string/save20_invalid_name': 'accept_new_active',
           'string/save20_lossy_quality_description': 'accept_new_active',
           'string/save20_title': 'accept_new_active',
           'string/save20_unsupported_image_colour': 'accept_new_active',
           'string/ui_0f_0f_px_1f': 'accept_new_active',
           'string/ui_100': 'accept_new_active',
           'string/ui_1_px': 'accept_new_wording_only',
           'string/ui_1f_s': 'accept_new_active',
           'string/ui_a_separate_recovery_copy_has_been_kept_use': 'accept_new_active',
           'string/ui_actual_size_100': 'accept_new_wording_only',
           'string/ui_add_colour26': 'accept_new_active',
           'string/ui_add_text': 'accept_new_active',
           'string/ui_airbrush': 'accept_current_correction_active',
           'string/ui_all': 'accept_new_active',
           'string/ui_an_assembly_source_image_is_missing': 'accept_new_active',
           'string/ui_android_blocked_the_file_picker': 'accept_new_active',
           'string/ui_android_could_not_decode_this_image': 'accept_new_active',
           'string/ui_android_could_not_find_a_file_picker_enable': 'accept_new_active',
           'string/ui_apply': 'accept_current_correction_active',
           'string/ui_apply_bounds': 'accept_new_active',
           'string/ui_apply_crop': 'accept_new_active',
           'string/ui_assembly_saved': 'accept_new_active',
           'string/ui_assembly_source_memory_floor': 'accept_new_active',
           'string/ui_autosave_failed_use_save': 'accept_new_active',
           'string/ui_autosave_image_encoding_failed': 'accept_new_active',
           'string/ui_autosave_is_paused_to_protect_that_draft_use': 'accept_new_active',
           'string/ui_autosave_metadata_is_missing': 'accept_new_active',
           'string/ui_autosave_paused_use_save': 'accept_new_active',
           'string/ui_autosave_pixels_are_missing': 'accept_new_active',
           'string/ui_autosave_pixels_could_not_be_read': 'accept_new_active',
           'string/ui_autosave_selection_encoding_failed': 'accept_new_active',
           'string/ui_autosaving_draft': 'accept_new_active',
           'string/ui_background_colour': 'accept_new_active',
           'string/ui_background_edit_colour': 'accept_new_active',
           'string/ui_basic_colours': 'accept_new_active',
           'string/ui_bg': 'accept_new_active',
           'string/ui_bold': 'accept_new_active',
           'string/ui_bottom': 'accept_new_active',
           'string/ui_brush': 'accept_current_correction_active',
           'string/ui_bucket_fill': 'accept_current_correction_active',
           'string/ui_cancel': 'accept_current_bounded',
           'string/ui_cannot_create_the_undo_cache_free_some_device': 'accept_new_active',
           'string/ui_canvas_bounds': 'accept_new_active',
           'string/ui_canvas_size': 'accept_new_active',
           'string/ui_canvas_size_30460e': 'accept_new_active',
           'string/ui_canvas_zoom': 'accept_new_active',
           'string/ui_canvas_zoom_771f84': 'accept_new_active',
           'string/ui_category_brush': 'accept_current_correction_wording_only',
           'string/ui_category_insert': 'accept_new_active',
           'string/ui_category_selection': 'accept_new_active',
           'string/ui_centred': 'accept_new_active',
           'string/ui_choose_a_smaller_output_copy_the_source_images': 'accept_new_active',
           'string/ui_choose_a_smaller_size': 'accept_new_active',
           'string/ui_choose_at_least_one_image': 'accept_new_active',
           'string/ui_choose_dimensions_no_larger_than_the_original': 'accept_new_active',
           'string/ui_choose_location': 'accept_new_active',
           'string/ui_clear_all': 'accept_new_active',
           'string/ui_clear_image': 'accept_new_active',
           'string/ui_codec_resize_memory_floor': 'accept_new_active',
           'string/ui_collapse_colour_palette': 'accept_new_wording_only',
           'string/ui_collapse_tool_category': 'accept_new_active',
           'string/ui_collapse_toolbox': 'accept_new_active',
           'string/ui_colour': 'accept_new_active',
           'string/ui_colour_palette_tap_for_foreground_hold_for_background': 'accept_new_active',
           'string/ui_colour_tab23': 'accept_new_active',
           'string/ui_colour_tap_foreground_hold_background': 'accept_new_active',
           'string/ui_commit_selection': 'accept_new_active',
           'string/ui_copy': 'accept_current_bounded',
           'string/ui_copy_all': 'accept_new_active',
           'string/ui_could_not_apply_the_crop': 'accept_new_active',
           'string/ui_could_not_complete_the_edit': 'accept_new_active',
           'string/ui_could_not_complete_the_operation': 'accept_new_active',
           'string/ui_could_not_export_the_recovery_copy': 'accept_new_active',
           'string/ui_could_not_open_image': 'accept_new_active',
           'string/ui_could_not_place_the_image': 'accept_new_active',
           'string/ui_could_not_prepare_the_image': 'accept_new_active',
           'string/ui_could_not_save_image': 'accept_new_active',
           'string/ui_could_not_save_the_assembly': 'accept_new_active',
           'string/ui_could_not_store_the_assembly': 'accept_new_active',
           'string/ui_crop': 'accept_new_active',
           'string/ui_crop_image': 'accept_new_active',
           'string/ui_crop_must_stay_inside_the_canvas': 'accept_new_active',
           'string/ui_crop_preview_drag_an_edge_or_corner_drag': 'accept_new_active',
           'string/ui_crop_to_selection': 'accept_new_active',
           'string/ui_cut': 'accept_current_bounded',
           'string/ui_d_d_pixels_2f_mp_exceeds_the_current': 'accept_new_active',
           'string/ui_d_d_px_d_pixels_2f_mp': 'accept_new_active',
           'string/ui_delete_selection': 'accept_new_active',
           'string/ui_discard': 'accept_current_correction_wording_only',
           'string/ui_discard_changes23': 'accept_current_correction_active',
           'string/ui_done': 'accept_current_correction_active',
           'string/ui_draft_not_saved_yet': 'accept_new_active',
           'string/ui_draft_pending': 'accept_new_active',
           'string/ui_draft_restored': 'accept_new_active',
           'string/ui_draft_saved': 'accept_new_active',
           'string/ui_draw26': 'accept_new_active',
           'string/ui_draw_again': 'accept_new_active',
           'string/ui_drawing23': 'accept_new_active',
           'string/ui_drawing_canvas_pinch_and_move_two_fingers_to': 'accept_new_active',
           'string/ui_drawing_settings': 'accept_new_active',
           'string/ui_drawing_settings_d900c6': 'accept_new_active',
           'string/ui_edit_background': 'accept_current_correction_wording_only',
           'string/ui_edit_canvas33': 'accept_new_active',
           'string/ui_edit_colour26': 'accept_new_active',
           'string/ui_edit_foreground': 'accept_new_wording_only',
           'string/ui_edit_transform33': 'accept_new_active',
           'string/ui_ellipse': 'accept_current_correction_active',
           'string/ui_enter_a_number_from_to': 'accept_new_active',
           'string/ui_enter_a_positive_size': 'accept_new_active',
           'string/ui_enter_a_trim_amount_for_every_edge': 'accept_new_active',
           'string/ui_enter_a_whole_number_from_to': 'accept_new_active',
           'string/ui_enter_all_four_trim_amounts': 'accept_new_active',
           'string/ui_enter_positive_canvas_dimensions_within_android_s_coordinate': 'accept_new_active',
           'string/ui_enter_positive_dimensions': 'accept_new_active',
           'string/ui_enter_positive_dimensions_no_larger_than_the_original': 'accept_new_active',
           'string/ui_enter_positive_dimensions_that_resolve_to_at_least': 'accept_new_active',
           'string/ui_enter_positive_image_dimensions': 'accept_new_active',
           'string/ui_enter_valid_dimensions': 'accept_new_active',
           'string/ui_eraser': 'accept_current_correction_active',
           'string/ui_expand_colour_palette': 'accept_new_wording_only',
           'string/ui_expand_tool_category': 'accept_new_active',
           'string/ui_expand_toolbox': 'accept_new_active',
           'string/ui_export_as23': 'accept_new_active',
           'string/ui_export_did_not_save23': 'accept_new_active',
           'string/ui_export_explanation23': 'accept_new_active',
           'string/ui_export_recovery_copy': 'accept_new_active',
           'string/ui_export_recovery_copy_144b8a': 'accept_new_active',
           'string/ui_eyedropper': 'accept_current_correction_active',
           'string/ui_fg': 'accept_new_active',
           'string/ui_fit': 'accept_new_active',
           'string/ui_fit_entire_canvas_in_view': 'accept_new_active',
           'string/ui_fit_image': 'accept_new_wording_only',
           'string/ui_fit_selection34': 'accept_new_active',
           'string/ui_flip_horizontal': 'accept_current_correction_active',
           'string/ui_flip_vertical': 'accept_current_correction_active',
           'string/ui_font': 'accept_new_active',
           'string/ui_font_family': 'accept_new_active',
           'string/ui_foreground_background_colour_palette': 'hold_absent',
           'string/ui_foreground_colour': 'accept_new_active',
           'string/ui_foreground_edit_colour': 'accept_new_active',
           'string/ui_free_form_select': 'accept_new_active',
           'string/ui_from_device34': 'accept_new_active',
           'string/ui_full_text_copied': 'accept_new_active',
           'string/ui_height': 'accept_new_active',
           'string/ui_height_in': 'accept_new_active',
           'string/ui_heights': 'accept_new_wording_only',
           'string/ui_hex_rrggbb': 'accept_new_active',
           'string/ui_hide_editor_controls': 'accept_new_wording_only',
           'string/ui_higher_quality_usually_makes_a_larger_file_lossless': 'accept_new_active',
           'string/ui_history_unavailable34': 'accept_new_active',
           'string/ui_image': 'accept_current_bounded',
           'string/ui_insert': 'accept_new_wording_only',
           'string/ui_insert_image_into_canvas': 'accept_new_wording_only',
           'string/ui_invalid_autosave_metadata': 'accept_new_active',
           'string/ui_invalid_colour': 'accept_new_active',
           'string/ui_invalid_selection_outline': 'accept_new_active',
           'string/ui_invert_colours': 'accept_new_active',
           'string/ui_italic': 'accept_new_active',
           'string/ui_keep_editing23': 'accept_current_correction_active',
           'string/ui_keeps_pixels_at_the_top_left_smaller_canvas': 'accept_new_active',
           'string/ui_languages23': 'accept_current_bounded',
           'string/ui_left': 'accept_new_active',
           'string/ui_left_aligned': 'accept_new_active',
           'string/ui_left_arrow_collapse': 'accept_new_wording_only',
           'string/ui_line': 'accept_current_correction_active',
           'string/ui_line_spacing': 'accept_new_active',
           'string/ui_load_image': 'accept_new_active',
           'string/ui_lock_aspect_ratio': 'accept_new_active',
           'string/ui_lock_proportions': 'accept_new_active',
           'string/ui_magnification': 'accept_new_active',
           'string/ui_main23': 'accept_new_wording_only',
           'string/ui_menu': 'accept_new_wording_only',
           'string/ui_menu_colours': 'accept_current_correction_wording_only',
           'string/ui_menu_edit': 'accept_new_active',
           'string/ui_menu_file': 'accept_new_active',
           'string/ui_menu_help': 'accept_current_correction_active',
           'string/ui_menu_image': 'accept_new_active',
           'string/ui_menu_view': 'accept_new_active',
           'string/ui_navigate': 'accept_new_active',
           'string/ui_new': 'accept_new_active',
           'string/ui_new_colour': 'accept_new_wording_only',
           'string/ui_new_image': 'accept_current_correction_active',
           'string/ui_no_readable_image_data': 'accept_new_active',
           'string/ui_no_resize_fits_decoder_memory': 'accept_new_active',
           'string/ui_none': 'accept_new_active',
           'string/ui_not_enough_memory_for_this_operation_the_assembly': 'accept_new_active',
           'string/ui_not_enough_memory_to_finish_opening_this_image': 'accept_new_active',
           'string/ui_not_enough_memory_to_inspect_this_image': 'accept_new_active',
           'string/ui_not_enough_memory_to_save_in_this_format': 'accept_new_active',
           'string/ui_numeric_slider_value': 'accept_new_active',
           'string/ui_ok': 'accept_current_bounded',
           'string/ui_original_size34': 'accept_new_active',
           'string/ui_other_images34': 'accept_new_active',
           'string/ui_outline': 'accept_current_correction_active',
           'string/ui_palette': 'accept_new_active',
           'string/ui_paste': 'accept_current_bounded',
           'string/ui_paste_hint34': 'accept_new_active',
           'string/ui_pencil': 'accept_new_active',
           'string/ui_percent': 'accept_new_active',
           'string/ui_percent_fd8671': 'accept_new_active',
           'string/ui_pinch_and_pan_mode': 'hold_absent',
           'string/ui_pixels': 'accept_current_bounded',
           'string/ui_pixels_6ec9c2': 'accept_current_bounded',
           'string/ui_place_text': 'accept_new_active',
           'string/ui_please_try_again': 'accept_new_active',
           'string/ui_please_wait_for_the_current_operation': 'accept_new_active',
           'string/ui_png_encoding_failed': 'accept_new_active',
           'string/ui_polygon': 'accept_new_active',
           'string/ui_preview': 'accept_current_bounded',
           'string/ui_previous_draft_kept_for_recovery': 'accept_new_active',
           'string/ui_px': 'accept_new_active',
           'string/ui_px_724eb3': 'accept_new_active',
           'string/ui_ready': 'accept_current_bounded',
           'string/ui_recovered_image': 'accept_new_active',
           'string/ui_recovery_copy_exported_extract_canvas_png_from_the': 'accept_new_active',
           'string/ui_rectangle': 'accept_current_correction_active',
           'string/ui_rectangle_select': 'accept_new_active',
           'string/ui_redo': 'accept_current_correction_active',
           'string/ui_remove': 'accept_new_active',
           'string/ui_reset_bw23': 'accept_new_active',
           'string/ui_reset_crop': 'accept_new_active',
           'string/ui_reset_to_black_white': 'accept_new_wording_only',
           'string/ui_resize_and_load': 'accept_new_active',
           'string/ui_resize_image': 'accept_new_active',
           'string/ui_resize_image_ab28be': 'accept_new_active',
           'string/ui_resize_large_image': 'accept_new_active',
           'string/ui_resize_the_copy': 'accept_new_active',
           'string/ui_right': 'accept_new_active',
           'string/ui_right_aligned': 'accept_new_active',
           'string/ui_rotate': 'accept_new_active',
           'string/ui_rotate_180': 'accept_new_active',
           'string/ui_rotate_90_clockwise': 'accept_new_active',
           'string/ui_sampled_resize_memory_explanation': 'accept_new_active',
           'string/ui_save': 'accept_current_correction_active',
           'string/ui_save_a5d0d9': 'accept_current_correction_active',
           'string/ui_save_and_share': 'accept_new_active',
           'string/ui_save_and_share_41edb4': 'accept_new_active',
           'string/ui_save_as': 'hold_absent',
           'string/ui_save_as_jpeg': 'hold_absent',
           'string/ui_save_as_jpeg_xl': 'hold_absent',
           'string/ui_save_as_png': 'hold_absent',
           'string/ui_save_explanation23': 'accept_new_active',
           'string/ui_save_png': 'accept_new_active',
           'string/ui_save_your_changes': 'accept_current_correction_active',
           'string/ui_saved': 'accept_new_active',
           'string/ui_scales_the_image_unlock_the_ratio_to_stretch': 'accept_new_active',
           'string/ui_select_all': 'accept_current_bounded',
           'string/ui_select_an_area': 'accept_new_active',
           'string/ui_select_an_area_first': 'accept_new_active',
           'string/ui_selected_colour23': 'accept_new_active',
           'string/ui_selection_dimensions_are_too_large': 'accept_new_active',
           'string/ui_share_explanation34': 'accept_new_active',
           'string/ui_share_saved_image': 'accept_new_active',
           'string/ui_show_all': 'accept_new_active',
           'string/ui_show_controls': 'accept_new_active',
           'string/ui_show_editor_controls': 'accept_new_wording_only',
           'string/ui_show_magnified_drawing_preview': 'accept_new_active',
           'string/ui_size_pixels': 'accept_new_active',
           'string/ui_size_px': 'accept_new_active',
           'string/ui_solid_fill': 'accept_current_correction_active',
           'string/ui_swap23': 'accept_new_active',
           'string/ui_swap_foreground_background': 'accept_new_wording_only',
           'string/ui_tap_an_image_first': 'accept_new_active',
           'string/ui_tap_canvas_to_type': 'accept_new_active',
           'string/ui_tap_to_type_a_number': 'accept_new_active',
           'string/ui_text': 'accept_current_bounded',
           'string/ui_text_alignment': 'accept_new_active',
           'string/ui_text_direction23': 'accept_new_active',
           'string/ui_the_crop_must_contain_at_least_one_pixel': 'accept_new_active',
           'string/ui_the_crop_must_stay_inside_the_image': 'accept_new_active',
           'string/ui_the_decoder_and_editing_buffers_need_about_the': 'accept_new_active',
           'string/ui_the_draft_is_saving_try_again_shortly': 'accept_new_active',
           'string/ui_the_encoder_did_not_finish': 'accept_new_active',
           'string/ui_the_full_image_and_working_buffers_exceed_the': 'accept_new_active',
           'string/ui_the_image_was_saved_but_android_could_not': 'accept_new_active',
           'string/ui_the_picker_returned_no_file_please_choose_the': 'accept_new_active',
           'string/ui_the_picker_returned_no_files': 'accept_new_active',
           'string/ui_the_previous_draft_could_not_be_moved_to': 'accept_new_active',
           'string/ui_the_previous_draft_could_not_be_preserved_separately': 'accept_new_active',
           'string/ui_the_previous_draft_could_not_be_restored': 'accept_new_active',
           'string/ui_the_previous_draft_needs_more_memory_to_reopen': 'accept_new_active',
           'string/ui_the_saved_assembly_could_not_be_opened': 'accept_new_active',
           'string/ui_the_selected_location_is_not_writable': 'accept_new_active',
           'string/ui_the_selected_provider_did_not_return_any_image': 'accept_new_active',
           'string/ui_the_trim_would_remove_the_entire_image': 'accept_new_active',
           'string/ui_the_undo_cache_is_damaged': 'accept_new_active',
           'string/ui_there_is_not_enough_memory_for_this_operation': 'accept_new_active',
           'string/ui_this_file_is_not_a_supported_image_use': 'accept_new_active',
           'string/ui_this_location_is_not_writable': 'accept_new_active',
           'string/ui_tolerance': 'accept_new_active',
           'string/ui_too_large_for_the_current_budget_reduce_the': 'accept_new_active',
           'string/ui_tool_categories': 'accept_new_wording_only',
           'string/ui_trim_amounts_must_be_zero_or_greater': 'accept_new_active',
           'string/ui_trim_amounts_must_fit_inside_each_image_use': 'accept_new_active',
           'string/ui_trim_expand_canvas_by_touch': 'accept_new_wording_only',
           'string/ui_try_a_different_file_or_location': 'accept_new_active',
           'string/ui_type_text': 'accept_new_active',
           'string/ui_underline': 'accept_new_active',
           'string/ui_undo': 'accept_current_correction_active',
           'string/ui_unexpected_data_in_the_undo_cache': 'accept_new_active',
           'string/ui_untitled': 'accept_current_bounded',
           'string/ui_use_1_1024_pixels': 'accept_new_active',
           'string/ui_use_50_300': 'accept_new_active',
           'string/ui_use_a_positive_target_dimension': 'accept_new_active',
           'string/ui_use_colour': 'accept_new_active',
           'string/ui_use_rrggbb': 'accept_new_active',
           'string/ui_watercolor': 'accept_current_correction_active',
           'string/ui_width': 'accept_new_active',
           'string/ui_working': 'accept_new_active',
           'string/ui_your_current_image_has_unsaved_changes': 'accept_new_active',
           'string/ui_zoom_in': 'accept_current_bounded',
           'string/ui_zoom_out': 'accept_current_bounded'}}

WORDING_ONLY = {'fil': {'string/ui_1_px',
         'string/ui_actual_size_100',
         'string/ui_category_brush',
         'string/ui_collapse_colour_palette',
         'string/ui_discard',
         'string/ui_edit_background',
         'string/ui_edit_foreground',
         'string/ui_expand_colour_palette',
         'string/ui_fit_image',
         'string/ui_heights',
         'string/ui_hide_editor_controls',
         'string/ui_insert',
         'string/ui_insert_image_into_canvas',
         'string/ui_left_arrow_collapse',
         'string/ui_main23',
         'string/ui_menu',
         'string/ui_menu_colours',
         'string/ui_new_colour',
         'string/ui_pinch_and_pan_mode',
         'string/ui_reset_to_black_white',
         'string/ui_show_editor_controls',
         'string/ui_swap_foreground_background',
         'string/ui_tool_categories',
         'string/ui_trim_expand_canvas_by_touch'},
 'kn': {'string/ui_1_px',
        'string/ui_actual_size_100',
        'string/ui_category_brush',
        'string/ui_collapse_colour_palette',
        'string/ui_discard',
        'string/ui_edit_background',
        'string/ui_edit_foreground',
        'string/ui_expand_colour_palette',
        'string/ui_fit_image',
        'string/ui_heights',
        'string/ui_hide_editor_controls',
        'string/ui_insert',
        'string/ui_insert_image_into_canvas',
        'string/ui_left_arrow_collapse',
        'string/ui_main23',
        'string/ui_menu',
        'string/ui_menu_colours',
        'string/ui_new_colour',
        'string/ui_reset_to_black_white',
        'string/ui_show_editor_controls',
        'string/ui_swap_foreground_background',
        'string/ui_tool_categories',
        'string/ui_trim_expand_canvas_by_touch'},
 'ml-IN': {'string/ui_1_px',
           'string/ui_actual_size_100',
           'string/ui_category_brush',
           'string/ui_collapse_colour_palette',
           'string/ui_discard',
           'string/ui_edit_background',
           'string/ui_edit_foreground',
           'string/ui_expand_colour_palette',
           'string/ui_fit_image',
           'string/ui_heights',
           'string/ui_hide_editor_controls',
           'string/ui_insert',
           'string/ui_insert_image_into_canvas',
           'string/ui_left_arrow_collapse',
           'string/ui_main23',
           'string/ui_menu',
           'string/ui_menu_colours',
           'string/ui_new_colour',
           'string/ui_reset_to_black_white',
           'string/ui_show_editor_controls',
           'string/ui_swap_foreground_background',
           'string/ui_tool_categories',
           'string/ui_trim_expand_canvas_by_touch'}}


def priority_ids():
    manifest=json.loads((catalogues.DATA/'string-importance.json').read_text())
    return {key for tier in manifest['tiers'] if tier['id'] in ('P0','P1') for key in tier['keys']}


def require_shape(data):
    names={identity.split('/',1)[1] for identity in priority_ids()}
    if data.get('schema_version')!=1 or set(data.get('locales',{}))!=TAGS:raise ValueError('Exact schema/locale set differs')
    if set(data.get('sources',{}))!=names|DEPENDENCIES:raise ValueError('Complete shared English source set differs')
    for tag,locale in data['locales'].items():
        expected=names-HELD_ABSENT[tag]-set(HELD_PRESENT[tag])|DEPENDENCIES
        if locale.get('priority_status')!=PRIORITY_STATUS[tag]:raise ValueError('Exact341 dispositions differ')
        if set(locale.get('wording_only',[]))!=WORDING_ONLY[tag]:raise ValueError('Exact source-only context limits differ')
        if set(locale.get('held_absent',[]))!=HELD_ABSENT[tag]:raise ValueError('Exact absent hold set differs')
        if locale.get('held_present')!=HELD_PRESENT[tag]:raise ValueError('Exact held-present values/attributes differ')
        if set(locale.get('accepted',{}))!=expected:raise ValueError('Complete accepted typed target set differs')
        if set(locale.get('unchanged_accepted',[]))!=UNCHANGED[tag] or set(locale.get('changed',[]))!=expected-UNCHANGED[tag]:raise ValueError('Edited/retained partition differs')
        if locale.get('predecessors')!=PREDECESSORS[tag]:raise ValueError('Exact previous value/type/attribute binding differs')
        if locale.get('outside_review')!=OUTSIDE_REVIEW[tag]:raise ValueError('Unrelated prior values differ')
        if locale.get('target_attribute_exceptions')!=ATTRIBUTE_EXCEPTIONS[tag]:raise ValueError('Exact target attribute exceptions differ')
        if len(locale['changed'])!=EDIT_COUNTS[tag]:raise ValueError('Exact edited count differs')
        typed={('plurals' if k=='ui_crop_preview_images' else 'string')+'/'+k for k in expected}
        typed|={row['type']+'/'+k for k,row in OUTSIDE_REVIEW[tag].items()}
        typed|={row['type']+'/'+k for k,row in HELD_PRESENT[tag].items()}
        if set(locale.get('catalogue_identities',[]))!=typed or len(locale['catalogue_identities'])!=len(typed):raise ValueError('Exact catalogue typed union differs')
        for key,value in locale['accepted'].items():
            typ=data['sources'][key]['type']
            if typ=='string' and (not isinstance(value,str) or not value):raise ValueError('Missing complete string')
            if typ=='plurals' and (not isinstance(value,dict) or set(value)!=PLURAL_QUANTITIES[tag] or not all(value.values())):raise ValueError('Complete plural quantity set differs')
    if data['locales']['fil']['accepted']['ui_save_a5d0d9']!='@string/ui_save':raise ValueError('Filipino alias must remain exact')
    return data


def require_complete(root,key,source,target,attributes):
    nodes=root.findall(f"./{source['type']}[@name='{key}']")
    if len(nodes)!=1 or nodes[0].attrib!=attributes:raise ValueError('Typed resource identity/attributes differ')
    node=nodes[0]
    if source['type']=='string':
        if list(node) or node.text!=target:raise ValueError('Complete string differs')
        pairs=[(target,source['source'])]
    else:
        if any(n.tag!='item' or set(n.attrib)!={'quantity'} or list(n) for n in node):raise ValueError('Malformed plural children')
        values={n.get('quantity'):n.text for n in node}
        if len(values)!=len(node) or values!=target:raise ValueError('Complete plural differs')
        pairs=[(v,source['source'][q])for q,v in values.items()]
    for value,english in pairs:
        if Counter(FULL_FORMAT_TOKEN.findall(value))!=Counter(FULL_FORMAT_TOKEN.findall(english)) or value.count(r'\n')!=english.count(r'\n'):raise ValueError('Full format/newline contract differs')
        if FULL_FORMAT_TOKEN.sub('',value).count('%')!=FULL_FORMAT_TOKEN.sub('',english).count('%'):raise ValueError('Literal percent contract differs')


class KannadaMalayalamFilipinoPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=require_shape(fixture(NAME));cls.roots={tag:ET.parse(catalogues.catalogue_paths()[tag]).getroot()for tag in TAGS}
        cls.english=ET.parse(catalogues.RES/'values/strings.xml').getroot()

    def test_complete_341_identity_set_and_all_fifteen_atomic_dependencies(self):
        self.assertEqual(341,len(priority_ids()))
        for tag,locale in self.data['locales'].items():
            actual={e.tag+'/'+e.get('name')for e in self.roots[tag]}
            self.assertEqual(set(locale['catalogue_identities']),actual);self.assertEqual(len(actual),len(self.roots[tag]))
            self.assertEqual({'string/'+key for key in HELD_ABSENT[tag]},priority_ids()-actual)
            for key,target in locale['accepted'].items():
                with self.subTest(tag=tag,key=key):require_complete(self.roots[tag],key,self.data['sources'][key],target,locale['target_attribute_exceptions'].get(key,{'name':key}))

    def test_every_complete_english_value_and_attributes_remain_source_bound(self):
        for key,row in self.data['sources'].items():
            require_complete(self.english,key,row,row['source'],row['attributes'])

    def test_exact_changed_partition_and_predecessors_reject_laundering(self):
        for tag,locale in self.data['locales'].items():
            for mode in ('remove','extra','wrong-locale','move-edit','move-retained','missing-predecessor','forged-predecessor','wrong-attrs','hold-credit','context-credit','wording-limit','extra-catalogue','held-present'):
                bad=deepcopy(self.data);b=bad['locales'][tag]
                if mode=='remove':b['accepted'].pop(next(iter(b['accepted'])))
                elif mode=='extra':b['accepted']['invented']='unexpected'
                elif mode=='wrong-locale':bad['locales']['en']=bad['locales'].pop(tag)
                elif mode=='move-edit':k=b['changed'].pop();b['unchanged_accepted'].append(k)
                elif mode=='move-retained':k=b['unchanged_accepted'].pop();b['changed'].append(k)
                elif mode=='missing-predecessor':b['predecessors'].pop(next(iter(b['predecessors'])))
                elif mode=='forged-predecessor':b['predecessors'][next(iter(b['predecessors']))]['target']='forged'
                elif mode=='wrong-attrs':b['target_attribute_exceptions']['ui_quality']={'name':'ui_quality'}
                elif mode=='hold-credit':b['priority_status']['string/ui_save_as']='accept_new_active'
                elif mode=='context-credit':b['priority_status'][next(iter(WORDING_ONLY[tag]))]='accept_new_active'
                elif mode=='wording-limit':b['wording_only'].pop()
                elif mode=='extra-catalogue':b['catalogue_identities'].append('string/unreviewed_extra')
                else:
                    if not b['held_present']:continue
                    k=next(iter(b['held_present']));b['held_present'][k]['target']='changed held wording'
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_shape(bad)

    def test_each_complete_target_rejects_truncation_wrong_locale_and_format_drift(self):
        for tag,locale in self.data['locales'].items():
            for key,target in locale['accepted'].items():
                source=self.data['sources'][key];attrs=locale['target_attribute_exceptions'].get(key,{'name':key})
                for mode in ('truncate','wrong-locale','attribute'):
                    root=deepcopy(self.roots[tag]);n=root.find(f"./{source['type']}[@name='{key}']")
                    if mode=='attribute':n.set('translatable','false')
                    elif mode=='truncate':
                        if source['type']=='string':n.text=n.text[:-1]
                        else:n[0].text=n[0].text[:-1]
                    else:
                        other=next((self.data['locales'][t]['accepted'][key]for t in TAGS if t!=tag and key in self.data['locales'][t]['accepted'] and self.data['locales'][t]['accepted'][key]!=target),None)
                        if other is None:continue
                        if source['type']=='string':n.text=other
                        else:
                            for child in n:child.text=other.get(child.get('quantity'),next(iter(other.values())))
                    with self.subTest(tag=tag,key=key,mode=mode),self.assertRaises(ValueError):require_complete(root,key,source,target,attrs)

    def test_plural_missing_extra_duplicate_and_every_complete_child_corruption_reject(self):
        key='ui_crop_preview_images';source=self.data['sources'][key]
        for tag,locale in self.data['locales'].items():
            for quantity in PLURAL_QUANTITIES[tag]:
                for mode in ('remove','extra','duplicate','wrong-type','truncate','newline','attribute','markup'):
                    root=deepcopy(self.roots[tag]);n=root.find("./plurals[@name='ui_crop_preview_images']");child=n.find(f"./item[@quantity='{quantity}']")
                    if mode=='remove':n.remove(child)
                    elif mode=='extra':ET.SubElement(n,'item',quantity='many').text=child.text
                    elif mode=='duplicate':n.append(deepcopy(child))
                    elif mode=='wrong-type':child.text=child.text.replace('%3$d','%3$s')
                    elif mode=='truncate':child.text=child.text[:-1]
                    elif mode=='newline':child.text=child.text.replace(r'\n',' ')
                    elif mode=='attribute':child.set('formatted','false')
                    else:ET.SubElement(child,'b').text='markup'
                    with self.subTest(tag=tag,quantity=quantity,mode=mode),self.assertRaises(ValueError):require_complete(root,key,source,locale['accepted'][key],{'name':key})

    def test_unrelated_existing_values_and_all_exact_absent_holds_preserved(self):
        for tag,locale in self.data['locales'].items():
            root=self.roots[tag]
            for key,row in locale['outside_review'].items():
                source={'type':row['type'],'source':row['target']}
                require_complete(root,key,source,row['target'],row['attributes'])
            for key in HELD_ABSENT[tag]:self.assertEqual([],root.findall(f"./string[@name='{key}']"))
            for key,row in HELD_PRESENT[tag].items():require_complete(root,key,{'type':row['type'],'source':row['target']},row['target'],row['attributes'])

    def test_preserved_alias_and_complete_command_references_are_bound_to_controls(self):
        self.assertEqual(display('fil','ui_save'),display('fil','ui_save_a5d0d9'))
        for tag in TAGS:
            for key,commands in {
                'ui_autosave_is_paused_to_protect_that_draft_use':['ui_menu_file','ui_export_recovery_copy','save20_title','save20_file_format'],
                'ui_recovery_copy_exported_extract_canvas_png_from_the':['ui_menu_file','ui_load_image'],
                'ui_paste_hint34':['ui_draw26','ui_category_insert','ui_other_images34']}.items():
                for command in commands:
                    caption=display(tag,command)
                    # Exact retained Filipino sentence names this action without its dialog ellipsis.
                    if (tag,key,command)==('fil','ui_recovery_copy_exported_extract_canvas_png_from_the','ui_load_image'):
                        self.assertEqual('Magbukas ng larawan…',caption);caption=caption.removesuffix('…')
                    self.assertIn(caption,display(tag,key))

    def test_dimension_unit_and_crop_side_templates_use_actual_consumer_slots(self):
        source=(catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt').read_text()
        crop=(catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt').read_text()
        self.assertIn('R.string.ui_width_in',source);self.assertIn('R.string.ui_height_in',source)
        self.assertIn('R.string.ui_trim_in_percent',crop);self.assertIn('R.string.ui_trim_in_pixels',crop)
        self.assertIn('R.plurals.ui_crop_preview_images',crop)
        for tag in TAGS:
            self.assertEqual('%1$s',FULL_FORMAT_TOKEN.search(display(tag,'ui_width_in')).group())
            self.assertIn('canvas.png',display(tag,'ui_recovery_copy_exported_extract_canvas_png_from_the'))

    def test_complete_quality_and_animation_dependency_contracts(self):
        for tag in TAGS:
            self.assertIn('(%)',display(tag,'ui_quality'))
            self.assertEqual({'name':'ui_quality','formatted':'false'},current_row(tag,'ui_quality')['attributes'])
            self.assertEqual(['%1$d'],FULL_FORMAT_TOKEN.findall(display(tag,'formats22_at_least_frames')))
            self.assertEqual(Counter(['%1$s','%2$s']),Counter(FULL_FORMAT_TOKEN.findall(display(tag,'formats22_animation_message'))))
            self.assertEqual(['%1$s'],FULL_FORMAT_TOKEN.findall(display(tag,'ui_lossless_format')))

if __name__=='__main__':unittest.main()
