"""Complete current typed scope, retained/held boundaries and consumer compositions."""
from collections import Counter
from copy import deepcopy
import json,re,unittest,xml.etree.ElementTree as ET
from unittest.mock import patch
from current_localization_contracts import fixture, residual_rows, require_residual_or_previous
from test_danish_norwegian_p0_wording import FULL_FORMAT_TOKEN
import translation_catalogues as catalogues
from moroccan_arabic_mongolian_toki_pona_priority_expectations import NAME,TAGS,current_row,display,_display,require_fixture_binding
DEPENDENCIES={'formats22_at_least_frames',
 'save20_dither',
 'ui_an_paint_image_assembly',
 'ui_an_paint_image_assembly_20_images_placed',
 'ui_arrow',
 'ui_crop_preview_images',
 'ui_curve',
 'ui_heart',
 'ui_image_assembly',
 'ui_image_shown_in_crop_preview',
 'ui_lossless_format',
 'ui_quality',
 'ui_rounded_rectangle',
 'ui_star',
 'ui_top',
 'ui_trim_in_percent',
 'ui_trim_in_pixels',
 'ui_width_in'}
HOLDS={'ary': {'formats22_derived_exported': None,
         'ui_bg': None,
         'ui_fg': None,
         'ui_fit_image': None,
         'ui_foreground_background_colour_palette': None,
         'ui_main23': None,
         'ui_pinch_and_pan_mode': None,
         'ui_save_as': None,
         'ui_save_as_jpeg': None,
         'ui_save_as_jpeg_xl': None,
         'ui_save_as_png': None},
 'mn-Cyrl-MN': {'formats22_derived_exported': {'attributes': {'name': 'formats22_derived_exported'},
                                               'target': '%1$s экспортоллоо. Бүтэн зурагт хадгалаагүй өөрчлөлт хэвээр '
                                                         'байна; солихоос өмнө бүтэн зургийн хуулбарыг хадгална уу.',
                                               'type': 'string'},
                'ui_bg': {'attributes': {'name': 'ui_bg'}, 'target': 'Дэвсгэр', 'type': 'string'},
                'ui_fg': {'attributes': {'name': 'ui_fg'}, 'target': 'Үндсэн', 'type': 'string'},
                'ui_fit_image': {'attributes': {'name': 'ui_fit_image'}, 'target': 'Зургийг багтаах', 'type': 'string'},
                'ui_foreground_background_colour_palette': {'attributes': {'name': 'ui_foreground_background_colour_palette'},
                                                            'target': 'Үндсэн %1$s, дэвсгэр %2$s. %3$s өнгөний самбар.',
                                                            'type': 'string'},
                'ui_main23': {'attributes': {'name': 'ui_main23'}, 'target': 'Үндсэн', 'type': 'string'},
                'ui_pinch_and_pan_mode': {'attributes': {'name': 'ui_pinch_and_pan_mode'},
                                          'target': 'Чимхэж томруулах ба шилжүүлэх горим',
                                          'type': 'string'},
                'ui_save_as': {'attributes': {'name': 'ui_save_as'},
                               'target': '%1$s болгон хадгалах',
                               'type': 'string'},
                'ui_save_as_jpeg': {'attributes': {'name': 'ui_save_as_jpeg'},
                                    'target': 'JPEG болгон хадгалах…',
                                    'type': 'string'},
                'ui_save_as_jpeg_xl': {'attributes': {'name': 'ui_save_as_jpeg_xl'},
                                       'target': 'JPEG XL болгон хадгалах…',
                                       'type': 'string'},
                'ui_save_as_png': {'attributes': {'name': 'ui_save_as_png'},
                                   'target': 'PNG болгон хадгалах…',
                                   'type': 'string'}},
 'tok': {'formats22_derived_exported': None,
         'ui_bg': None,
         'ui_fg': None,
         'ui_fit_image': None,
         'ui_foreground_background_colour_palette': None,
         'ui_main23': None,
         'ui_pinch_and_pan_mode': None,
         'ui_save_as': None,
         'ui_save_as_jpeg': None,
         'ui_save_as_jpeg_xl': None,
         'ui_save_as_png': None}}
PRIORITY_STATUS={'ary': {'string/colour_converter_unavailable': 'accept_edit',
         'string/colour_invalid_metadata': 'accept_edit',
         'string/colour_truncated_metadata': 'accept_edit',
         'string/colour_unsupported_icc_model': 'accept_edit',
         'string/commons_svg_original_size_too_large': 'accept_edit',
         'string/commons_svg_original_size_unavailable': 'accept_edit',
         'string/formats22_animation_message': 'accept_edit',
         'string/formats22_animation_poster': 'accept_edit',
         'string/formats22_animation_still': 'accept_edit',
         'string/formats22_animation_title': 'accept_edit',
         'string/formats22_animation_unknown': 'accept_edit',
         'string/formats22_ascii_description': 'accept_edit',
         'string/formats22_derived_exported': 'hold_absent',
         'string/formats22_import_limit': 'accept_edit',
         'string/formats22_open_still': 'accept_edit',
         'string/formats22_pdf_raster_hint': 'accept_edit',
         'string/gallery_credit_could_not_save': 'accept_edit',
         'string/gallery_credit_too_large': 'accept_edit',
         'string/language20_app_language': 'accept_edit',
         'string/language20_current': 'accept_edit',
         'string/language20_device_default': 'accept_edit',
         'string/language20_settings': 'accept_edit',
         'string/language20_translation_note': 'accept_edit',
         'string/legacy_credits_unreadable': 'accept_edit',
         'string/save20_destination_error': 'accept_edit',
         'string/save20_encoding_budget': 'accept_edit',
         'string/save20_file_format': 'accept_edit',
         'string/save20_file_name': 'accept_edit',
         'string/save20_gif_description': 'accept_edit',
         'string/save20_invalid_name': 'accept_edit',
         'string/save20_lossy_quality_description': 'accept_edit',
         'string/save20_title': 'accept_edit',
         'string/save20_unsupported_image_colour': 'accept_edit',
         'string/ui_0f_0f_px_1f': 'accept_edit',
         'string/ui_100': 'accept_edit',
         'string/ui_1_px': 'accept_edit_wording_or_route_limited',
         'string/ui_1f_s': 'accept_edit',
         'string/ui_a_separate_recovery_copy_has_been_kept_use': 'accept_edit',
         'string/ui_actual_size_100': 'accept_edit_wording_or_route_limited',
         'string/ui_add_colour26': 'accept_edit',
         'string/ui_add_text': 'accept_edit',
         'string/ui_airbrush': 'accept_edit',
         'string/ui_all': 'accept_edit',
         'string/ui_an_assembly_source_image_is_missing': 'accept_edit',
         'string/ui_android_blocked_the_file_picker': 'accept_edit',
         'string/ui_android_could_not_decode_this_image': 'accept_edit',
         'string/ui_android_could_not_find_a_file_picker_enable': 'accept_edit',
         'string/ui_apply': 'accept_edit',
         'string/ui_apply_bounds': 'accept_edit',
         'string/ui_apply_crop': 'accept_edit',
         'string/ui_assembly_saved': 'accept_edit',
         'string/ui_assembly_source_memory_floor': 'accept_edit',
         'string/ui_autosave_failed_use_save': 'accept_edit',
         'string/ui_autosave_image_encoding_failed': 'accept_edit',
         'string/ui_autosave_is_paused_to_protect_that_draft_use': 'accept_edit',
         'string/ui_autosave_metadata_is_missing': 'accept_edit',
         'string/ui_autosave_paused_use_save': 'accept_edit',
         'string/ui_autosave_pixels_are_missing': 'accept_edit',
         'string/ui_autosave_pixels_could_not_be_read': 'accept_edit',
         'string/ui_autosave_selection_encoding_failed': 'accept_edit',
         'string/ui_autosaving_draft': 'accept_edit',
         'string/ui_background_colour': 'accept_edit',
         'string/ui_background_edit_colour': 'accept_edit',
         'string/ui_basic_colours': 'accept_edit',
         'string/ui_bg': 'hold_absent',
         'string/ui_bold': 'accept_edit',
         'string/ui_bottom': 'accept_edit',
         'string/ui_brush': 'accept_edit',
         'string/ui_bucket_fill': 'accept_edit',
         'string/ui_cancel': 'accept_edit',
         'string/ui_cannot_create_the_undo_cache_free_some_device': 'accept_edit',
         'string/ui_canvas_bounds': 'accept_edit',
         'string/ui_canvas_size': 'accept_edit',
         'string/ui_canvas_size_30460e': 'accept_edit',
         'string/ui_canvas_zoom': 'accept_edit',
         'string/ui_canvas_zoom_771f84': 'accept_edit',
         'string/ui_category_brush': 'accept_edit_wording_or_route_limited',
         'string/ui_category_insert': 'accept_edit',
         'string/ui_category_selection': 'accept_edit',
         'string/ui_centred': 'accept_edit',
         'string/ui_choose_a_smaller_output_copy_the_source_images': 'accept_edit',
         'string/ui_choose_a_smaller_size': 'accept_edit',
         'string/ui_choose_at_least_one_image': 'accept_edit',
         'string/ui_choose_dimensions_no_larger_than_the_original': 'accept_edit',
         'string/ui_choose_location': 'accept_edit',
         'string/ui_clear_all': 'accept_edit',
         'string/ui_clear_image': 'accept_edit',
         'string/ui_codec_resize_memory_floor': 'accept_edit',
         'string/ui_collapse_colour_palette': 'accept_edit_wording_or_route_limited',
         'string/ui_collapse_tool_category': 'accept_edit',
         'string/ui_collapse_toolbox': 'accept_edit',
         'string/ui_colour': 'accept_edit',
         'string/ui_colour_palette_tap_for_foreground_hold_for_background': 'accept_edit',
         'string/ui_colour_tab23': 'accept_edit',
         'string/ui_colour_tap_foreground_hold_background': 'accept_edit',
         'string/ui_commit_selection': 'accept_edit',
         'string/ui_copy': 'accept_edit',
         'string/ui_copy_all': 'accept_edit',
         'string/ui_could_not_apply_the_crop': 'accept_edit',
         'string/ui_could_not_complete_the_edit': 'accept_edit',
         'string/ui_could_not_complete_the_operation': 'accept_edit',
         'string/ui_could_not_export_the_recovery_copy': 'accept_edit',
         'string/ui_could_not_open_image': 'accept_edit',
         'string/ui_could_not_place_the_image': 'accept_edit',
         'string/ui_could_not_prepare_the_image': 'accept_edit',
         'string/ui_could_not_save_image': 'accept_edit',
         'string/ui_could_not_save_the_assembly': 'accept_edit',
         'string/ui_could_not_store_the_assembly': 'accept_edit',
         'string/ui_crop': 'accept_edit',
         'string/ui_crop_image': 'accept_edit',
         'string/ui_crop_must_stay_inside_the_canvas': 'accept_edit',
         'string/ui_crop_preview_drag_an_edge_or_corner_drag': 'accept_edit',
         'string/ui_crop_to_selection': 'accept_edit',
         'string/ui_cut': 'accept_edit',
         'string/ui_d_d_pixels_2f_mp_exceeds_the_current': 'accept_edit',
         'string/ui_d_d_px_d_pixels_2f_mp': 'accept_edit',
         'string/ui_delete_selection': 'accept_edit',
         'string/ui_discard': 'accept_edit_wording_or_route_limited',
         'string/ui_discard_changes23': 'accept_edit',
         'string/ui_done': 'accept_edit',
         'string/ui_draft_not_saved_yet': 'accept_edit',
         'string/ui_draft_pending': 'accept_edit',
         'string/ui_draft_restored': 'accept_edit',
         'string/ui_draft_saved': 'accept_edit',
         'string/ui_draw26': 'accept_edit',
         'string/ui_draw_again': 'accept_edit',
         'string/ui_drawing23': 'accept_edit',
         'string/ui_drawing_canvas_pinch_and_move_two_fingers_to': 'accept_edit',
         'string/ui_drawing_settings': 'accept_edit',
         'string/ui_drawing_settings_d900c6': 'accept_edit',
         'string/ui_edit_background': 'accept_edit_wording_or_route_limited',
         'string/ui_edit_canvas33': 'accept_edit',
         'string/ui_edit_colour26': 'accept_edit',
         'string/ui_edit_foreground': 'accept_edit_wording_or_route_limited',
         'string/ui_edit_transform33': 'accept_edit',
         'string/ui_ellipse': 'accept_edit',
         'string/ui_enter_a_number_from_to': 'accept_edit',
         'string/ui_enter_a_positive_size': 'accept_edit',
         'string/ui_enter_a_trim_amount_for_every_edge': 'accept_edit',
         'string/ui_enter_a_whole_number_from_to': 'accept_edit',
         'string/ui_enter_all_four_trim_amounts': 'accept_edit',
         'string/ui_enter_positive_canvas_dimensions_within_android_s_coordinate': 'accept_edit',
         'string/ui_enter_positive_dimensions': 'accept_edit',
         'string/ui_enter_positive_dimensions_no_larger_than_the_original': 'accept_edit',
         'string/ui_enter_positive_dimensions_that_resolve_to_at_least': 'accept_edit',
         'string/ui_enter_positive_image_dimensions': 'accept_edit',
         'string/ui_enter_valid_dimensions': 'accept_edit',
         'string/ui_eraser': 'accept_edit',
         'string/ui_expand_colour_palette': 'accept_edit_wording_or_route_limited',
         'string/ui_expand_tool_category': 'accept_edit',
         'string/ui_expand_toolbox': 'accept_edit',
         'string/ui_export_as23': 'accept_edit',
         'string/ui_export_did_not_save23': 'accept_edit',
         'string/ui_export_explanation23': 'accept_edit',
         'string/ui_export_recovery_copy': 'accept_edit',
         'string/ui_export_recovery_copy_144b8a': 'accept_edit',
         'string/ui_eyedropper': 'accept_edit',
         'string/ui_fg': 'hold_absent',
         'string/ui_fit': 'accept_edit',
         'string/ui_fit_entire_canvas_in_view': 'accept_edit',
         'string/ui_fit_image': 'hold_absent',
         'string/ui_fit_selection34': 'accept_edit',
         'string/ui_flip_horizontal': 'accept_edit',
         'string/ui_flip_vertical': 'accept_edit',
         'string/ui_font': 'accept_edit',
         'string/ui_font_family': 'accept_edit',
         'string/ui_foreground_background_colour_palette': 'hold_absent',
         'string/ui_foreground_colour': 'accept_edit',
         'string/ui_foreground_edit_colour': 'accept_edit',
         'string/ui_free_form_select': 'accept_edit',
         'string/ui_from_device34': 'accept_edit',
         'string/ui_full_text_copied': 'accept_edit',
         'string/ui_height': 'accept_edit',
         'string/ui_height_in': 'accept_edit',
         'string/ui_heights': 'accept_edit_wording_or_route_limited',
         'string/ui_hex_rrggbb': 'accept_edit',
         'string/ui_hide_editor_controls': 'accept_edit_wording_or_route_limited',
         'string/ui_higher_quality_usually_makes_a_larger_file_lossless': 'accept_edit',
         'string/ui_history_unavailable34': 'accept_edit',
         'string/ui_image': 'accept_edit',
         'string/ui_insert': 'accept_edit_wording_or_route_limited',
         'string/ui_insert_image_into_canvas': 'accept_edit_wording_or_route_limited',
         'string/ui_invalid_autosave_metadata': 'accept_edit',
         'string/ui_invalid_colour': 'accept_edit',
         'string/ui_invalid_selection_outline': 'accept_edit',
         'string/ui_invert_colours': 'accept_edit',
         'string/ui_italic': 'accept_edit',
         'string/ui_keep_editing23': 'accept_edit',
         'string/ui_keeps_pixels_at_the_top_left_smaller_canvas': 'accept_edit',
         'string/ui_languages23': 'accept_edit',
         'string/ui_left': 'accept_edit',
         'string/ui_left_aligned': 'accept_edit',
         'string/ui_left_arrow_collapse': 'accept_edit_wording_or_route_limited',
         'string/ui_line': 'accept_edit',
         'string/ui_line_spacing': 'accept_edit',
         'string/ui_load_image': 'accept_edit',
         'string/ui_lock_aspect_ratio': 'accept_edit',
         'string/ui_lock_proportions': 'accept_edit',
         'string/ui_magnification': 'accept_edit',
         'string/ui_main23': 'hold_absent',
         'string/ui_menu': 'accept_edit_wording_or_route_limited',
         'string/ui_menu_colours': 'accept_edit_wording_or_route_limited',
         'string/ui_menu_edit': 'accept_edit',
         'string/ui_menu_file': 'accept_edit',
         'string/ui_menu_help': 'accept_edit',
         'string/ui_menu_image': 'accept_edit',
         'string/ui_menu_view': 'accept_edit',
         'string/ui_navigate': 'accept_edit',
         'string/ui_new': 'accept_edit',
         'string/ui_new_colour': 'accept_edit_wording_or_route_limited',
         'string/ui_new_image': 'accept_edit',
         'string/ui_no_readable_image_data': 'accept_edit',
         'string/ui_no_resize_fits_decoder_memory': 'accept_edit',
         'string/ui_none': 'accept_edit',
         'string/ui_not_enough_memory_for_this_operation_the_assembly': 'accept_edit',
         'string/ui_not_enough_memory_to_finish_opening_this_image': 'accept_edit',
         'string/ui_not_enough_memory_to_inspect_this_image': 'accept_edit',
         'string/ui_not_enough_memory_to_save_in_this_format': 'accept_edit',
         'string/ui_numeric_slider_value': 'accept_edit',
         'string/ui_ok': 'accept_edit',
         'string/ui_original_size34': 'accept_edit',
         'string/ui_other_images34': 'accept_edit',
         'string/ui_outline': 'accept_edit',
         'string/ui_palette': 'accept_edit',
         'string/ui_paste': 'accept_edit',
         'string/ui_paste_hint34': 'accept_edit',
         'string/ui_pencil': 'accept_edit',
         'string/ui_percent': 'accept_edit',
         'string/ui_percent_fd8671': 'accept_edit',
         'string/ui_pinch_and_pan_mode': 'hold_absent',
         'string/ui_pixels': 'accept_edit',
         'string/ui_pixels_6ec9c2': 'accept_edit',
         'string/ui_place_text': 'accept_edit',
         'string/ui_please_try_again': 'accept_edit',
         'string/ui_please_wait_for_the_current_operation': 'accept_edit',
         'string/ui_png_encoding_failed': 'accept_edit',
         'string/ui_polygon': 'accept_edit',
         'string/ui_preview': 'accept_edit',
         'string/ui_previous_draft_kept_for_recovery': 'accept_edit',
         'string/ui_px': 'accept_edit',
         'string/ui_px_724eb3': 'accept_edit',
         'string/ui_ready': 'accept_edit',
         'string/ui_recovered_image': 'accept_edit',
         'string/ui_recovery_copy_exported_extract_canvas_png_from_the': 'accept_edit',
         'string/ui_rectangle': 'accept_edit',
         'string/ui_rectangle_select': 'accept_edit',
         'string/ui_redo': 'accept_edit',
         'string/ui_remove': 'accept_edit',
         'string/ui_reset_bw23': 'accept_edit',
         'string/ui_reset_crop': 'accept_edit',
         'string/ui_reset_to_black_white': 'accept_edit_wording_or_route_limited',
         'string/ui_resize_and_load': 'accept_edit',
         'string/ui_resize_image': 'accept_edit',
         'string/ui_resize_image_ab28be': 'accept_edit',
         'string/ui_resize_large_image': 'accept_edit',
         'string/ui_resize_the_copy': 'accept_edit',
         'string/ui_right': 'accept_edit',
         'string/ui_right_aligned': 'accept_edit',
         'string/ui_rotate': 'accept_edit',
         'string/ui_rotate_180': 'accept_edit',
         'string/ui_rotate_90_clockwise': 'accept_edit',
         'string/ui_sampled_resize_memory_explanation': 'accept_edit',
         'string/ui_save': 'accept_edit',
         'string/ui_save_a5d0d9': 'accept_edit',
         'string/ui_save_and_share': 'accept_edit',
         'string/ui_save_and_share_41edb4': 'accept_edit',
         'string/ui_save_as': 'hold_absent',
         'string/ui_save_as_jpeg': 'hold_absent',
         'string/ui_save_as_jpeg_xl': 'hold_absent',
         'string/ui_save_as_png': 'hold_absent',
         'string/ui_save_explanation23': 'accept_edit',
         'string/ui_save_png': 'accept_edit',
         'string/ui_save_your_changes': 'accept_edit',
         'string/ui_saved': 'accept_edit',
         'string/ui_scales_the_image_unlock_the_ratio_to_stretch': 'accept_edit',
         'string/ui_select_all': 'accept_edit',
         'string/ui_select_an_area': 'accept_edit',
         'string/ui_select_an_area_first': 'accept_edit',
         'string/ui_selected_colour23': 'accept_edit',
         'string/ui_selection_dimensions_are_too_large': 'accept_edit',
         'string/ui_share_explanation34': 'accept_edit',
         'string/ui_share_saved_image': 'accept_edit',
         'string/ui_show_all': 'accept_edit',
         'string/ui_show_controls': 'accept_edit',
         'string/ui_show_editor_controls': 'accept_edit_wording_or_route_limited',
         'string/ui_show_magnified_drawing_preview': 'accept_edit',
         'string/ui_size_pixels': 'accept_edit',
         'string/ui_size_px': 'accept_edit',
         'string/ui_solid_fill': 'accept_edit',
         'string/ui_swap23': 'accept_edit',
         'string/ui_swap_foreground_background': 'accept_edit_wording_or_route_limited',
         'string/ui_tap_an_image_first': 'accept_edit',
         'string/ui_tap_canvas_to_type': 'accept_edit',
         'string/ui_tap_to_type_a_number': 'accept_edit',
         'string/ui_text': 'accept_edit',
         'string/ui_text_alignment': 'accept_edit',
         'string/ui_text_direction23': 'accept_edit',
         'string/ui_the_crop_must_contain_at_least_one_pixel': 'accept_edit',
         'string/ui_the_crop_must_stay_inside_the_image': 'accept_edit',
         'string/ui_the_decoder_and_editing_buffers_need_about_the': 'accept_edit',
         'string/ui_the_draft_is_saving_try_again_shortly': 'accept_edit',
         'string/ui_the_encoder_did_not_finish': 'accept_edit',
         'string/ui_the_full_image_and_working_buffers_exceed_the': 'accept_edit',
         'string/ui_the_image_was_saved_but_android_could_not': 'accept_edit',
         'string/ui_the_picker_returned_no_file_please_choose_the': 'accept_edit',
         'string/ui_the_picker_returned_no_files': 'accept_edit',
         'string/ui_the_previous_draft_could_not_be_moved_to': 'accept_edit',
         'string/ui_the_previous_draft_could_not_be_preserved_separately': 'accept_edit',
         'string/ui_the_previous_draft_could_not_be_restored': 'accept_edit',
         'string/ui_the_previous_draft_needs_more_memory_to_reopen': 'accept_edit',
         'string/ui_the_saved_assembly_could_not_be_opened': 'accept_edit',
         'string/ui_the_selected_location_is_not_writable': 'accept_edit',
         'string/ui_the_selected_provider_did_not_return_any_image': 'accept_edit',
         'string/ui_the_trim_would_remove_the_entire_image': 'accept_edit',
         'string/ui_the_undo_cache_is_damaged': 'accept_edit',
         'string/ui_there_is_not_enough_memory_for_this_operation': 'accept_edit',
         'string/ui_this_file_is_not_a_supported_image_use': 'accept_edit',
         'string/ui_this_location_is_not_writable': 'accept_edit',
         'string/ui_tolerance': 'accept_edit',
         'string/ui_too_large_for_the_current_budget_reduce_the': 'accept_edit',
         'string/ui_tool_categories': 'accept_edit_wording_or_route_limited',
         'string/ui_trim_amounts_must_be_zero_or_greater': 'accept_edit',
         'string/ui_trim_amounts_must_fit_inside_each_image_use': 'accept_edit',
         'string/ui_trim_expand_canvas_by_touch': 'accept_edit_wording_or_route_limited',
         'string/ui_try_a_different_file_or_location': 'accept_edit',
         'string/ui_type_text': 'accept_edit',
         'string/ui_underline': 'accept_edit',
         'string/ui_undo': 'accept_edit',
         'string/ui_unexpected_data_in_the_undo_cache': 'accept_edit',
         'string/ui_untitled': 'accept_edit',
         'string/ui_use_1_1024_pixels': 'accept_edit',
         'string/ui_use_50_300': 'accept_edit',
         'string/ui_use_a_positive_target_dimension': 'accept_edit',
         'string/ui_use_colour': 'accept_edit',
         'string/ui_use_rrggbb': 'accept_edit',
         'string/ui_watercolor': 'accept_edit',
         'string/ui_width': 'accept_edit',
         'string/ui_working': 'accept_edit',
         'string/ui_your_current_image_has_unsaved_changes': 'accept_edit',
         'string/ui_zoom_in': 'accept_edit',
         'string/ui_zoom_out': 'accept_edit'},
 'mn-Cyrl-MN': {'string/colour_converter_unavailable': 'accept_retained',
                'string/colour_invalid_metadata': 'accept_retained',
                'string/colour_truncated_metadata': 'accept_retained',
                'string/colour_unsupported_icc_model': 'accept_retained',
                'string/commons_svg_original_size_too_large': 'accept_retained',
                'string/commons_svg_original_size_unavailable': 'accept_retained',
                'string/formats22_animation_message': 'accept_retained',
                'string/formats22_animation_poster': 'accept_retained',
                'string/formats22_animation_still': 'accept_retained',
                'string/formats22_animation_title': 'accept_retained',
                'string/formats22_animation_unknown': 'accept_retained',
                'string/formats22_ascii_description': 'accept_retained',
                'string/formats22_derived_exported': 'hold_existing',
                'string/formats22_import_limit': 'accept_retained',
                'string/formats22_open_still': 'accept_retained',
                'string/formats22_pdf_raster_hint': 'accept_retained',
                'string/gallery_credit_could_not_save': 'accept_edit',
                'string/gallery_credit_too_large': 'accept_edit',
                'string/language20_app_language': 'accept_retained',
                'string/language20_current': 'accept_retained',
                'string/language20_device_default': 'accept_edit',
                'string/language20_settings': 'accept_retained',
                'string/language20_translation_note': 'accept_retained',
                'string/legacy_credits_unreadable': 'accept_edit',
                'string/save20_destination_error': 'accept_retained',
                'string/save20_encoding_budget': 'accept_retained',
                'string/save20_file_format': 'accept_retained',
                'string/save20_file_name': 'accept_retained',
                'string/save20_gif_description': 'accept_retained',
                'string/save20_invalid_name': 'accept_retained',
                'string/save20_lossy_quality_description': 'accept_retained',
                'string/save20_title': 'accept_retained',
                'string/save20_unsupported_image_colour': 'accept_retained',
                'string/ui_0f_0f_px_1f': 'accept_retained',
                'string/ui_100': 'accept_retained',
                'string/ui_1_px': 'accept_retained_wording_or_route_limited',
                'string/ui_1f_s': 'accept_retained',
                'string/ui_a_separate_recovery_copy_has_been_kept_use': 'accept_retained',
                'string/ui_actual_size_100': 'accept_retained_wording_or_route_limited',
                'string/ui_add_colour26': 'accept_retained',
                'string/ui_add_text': 'accept_retained',
                'string/ui_airbrush': 'accept_retained',
                'string/ui_all': 'accept_retained',
                'string/ui_an_assembly_source_image_is_missing': 'accept_retained',
                'string/ui_android_blocked_the_file_picker': 'accept_retained',
                'string/ui_android_could_not_decode_this_image': 'accept_retained',
                'string/ui_android_could_not_find_a_file_picker_enable': 'accept_retained',
                'string/ui_apply': 'accept_retained',
                'string/ui_apply_bounds': 'accept_retained',
                'string/ui_apply_crop': 'accept_retained',
                'string/ui_assembly_saved': 'accept_retained',
                'string/ui_assembly_source_memory_floor': 'accept_retained',
                'string/ui_autosave_failed_use_save': 'accept_retained',
                'string/ui_autosave_image_encoding_failed': 'accept_retained',
                'string/ui_autosave_is_paused_to_protect_that_draft_use': 'accept_retained',
                'string/ui_autosave_metadata_is_missing': 'accept_retained',
                'string/ui_autosave_paused_use_save': 'accept_retained',
                'string/ui_autosave_pixels_are_missing': 'accept_retained',
                'string/ui_autosave_pixels_could_not_be_read': 'accept_retained',
                'string/ui_autosave_selection_encoding_failed': 'accept_retained',
                'string/ui_autosaving_draft': 'accept_retained',
                'string/ui_background_colour': 'accept_retained',
                'string/ui_background_edit_colour': 'accept_retained',
                'string/ui_basic_colours': 'accept_retained',
                'string/ui_bg': 'hold_existing',
                'string/ui_bold': 'accept_retained',
                'string/ui_bottom': 'accept_retained',
                'string/ui_brush': 'accept_retained',
                'string/ui_bucket_fill': 'accept_retained',
                'string/ui_cancel': 'accept_retained',
                'string/ui_cannot_create_the_undo_cache_free_some_device': 'accept_retained',
                'string/ui_canvas_bounds': 'accept_retained',
                'string/ui_canvas_size': 'accept_retained',
                'string/ui_canvas_size_30460e': 'accept_retained',
                'string/ui_canvas_zoom': 'accept_retained',
                'string/ui_canvas_zoom_771f84': 'accept_retained',
                'string/ui_category_brush': 'accept_retained_wording_or_route_limited',
                'string/ui_category_insert': 'accept_retained',
                'string/ui_category_selection': 'accept_retained',
                'string/ui_centred': 'accept_retained',
                'string/ui_choose_a_smaller_output_copy_the_source_images': 'accept_retained',
                'string/ui_choose_a_smaller_size': 'accept_retained',
                'string/ui_choose_at_least_one_image': 'accept_retained',
                'string/ui_choose_dimensions_no_larger_than_the_original': 'accept_retained',
                'string/ui_choose_location': 'accept_edit',
                'string/ui_clear_all': 'accept_retained',
                'string/ui_clear_image': 'accept_retained',
                'string/ui_codec_resize_memory_floor': 'accept_retained',
                'string/ui_collapse_colour_palette': 'accept_retained_wording_or_route_limited',
                'string/ui_collapse_tool_category': 'accept_edit',
                'string/ui_collapse_toolbox': 'accept_retained',
                'string/ui_colour': 'accept_retained',
                'string/ui_colour_palette_tap_for_foreground_hold_for_background': 'accept_retained',
                'string/ui_colour_tab23': 'accept_retained',
                'string/ui_colour_tap_foreground_hold_background': 'accept_retained',
                'string/ui_commit_selection': 'accept_retained',
                'string/ui_copy': 'accept_retained',
                'string/ui_copy_all': 'accept_retained',
                'string/ui_could_not_apply_the_crop': 'accept_retained',
                'string/ui_could_not_complete_the_edit': 'accept_retained',
                'string/ui_could_not_complete_the_operation': 'accept_retained',
                'string/ui_could_not_export_the_recovery_copy': 'accept_retained',
                'string/ui_could_not_open_image': 'accept_retained',
                'string/ui_could_not_place_the_image': 'accept_retained',
                'string/ui_could_not_prepare_the_image': 'accept_retained',
                'string/ui_could_not_save_image': 'accept_retained',
                'string/ui_could_not_save_the_assembly': 'accept_retained',
                'string/ui_could_not_store_the_assembly': 'accept_retained',
                'string/ui_crop': 'accept_retained',
                'string/ui_crop_image': 'accept_retained',
                'string/ui_crop_must_stay_inside_the_canvas': 'accept_retained',
                'string/ui_crop_preview_drag_an_edge_or_corner_drag': 'accept_retained',
                'string/ui_crop_to_selection': 'accept_retained',
                'string/ui_cut': 'accept_retained',
                'string/ui_d_d_pixels_2f_mp_exceeds_the_current': 'accept_retained',
                'string/ui_d_d_px_d_pixels_2f_mp': 'accept_retained',
                'string/ui_delete_selection': 'accept_retained',
                'string/ui_discard': 'accept_retained_wording_or_route_limited',
                'string/ui_discard_changes23': 'accept_retained',
                'string/ui_done': 'accept_retained',
                'string/ui_draft_not_saved_yet': 'accept_retained',
                'string/ui_draft_pending': 'accept_retained',
                'string/ui_draft_restored': 'accept_retained',
                'string/ui_draft_saved': 'accept_retained',
                'string/ui_draw26': 'accept_retained',
                'string/ui_draw_again': 'accept_retained',
                'string/ui_drawing23': 'accept_retained',
                'string/ui_drawing_canvas_pinch_and_move_two_fingers_to': 'accept_retained',
                'string/ui_drawing_settings': 'accept_retained',
                'string/ui_drawing_settings_d900c6': 'accept_retained',
                'string/ui_edit_background': 'accept_retained_wording_or_route_limited',
                'string/ui_edit_canvas33': 'accept_retained',
                'string/ui_edit_colour26': 'accept_retained',
                'string/ui_edit_foreground': 'accept_retained_wording_or_route_limited',
                'string/ui_edit_transform33': 'accept_retained',
                'string/ui_ellipse': 'accept_retained',
                'string/ui_enter_a_number_from_to': 'accept_retained',
                'string/ui_enter_a_positive_size': 'accept_retained',
                'string/ui_enter_a_trim_amount_for_every_edge': 'accept_retained',
                'string/ui_enter_a_whole_number_from_to': 'accept_retained',
                'string/ui_enter_all_four_trim_amounts': 'accept_retained',
                'string/ui_enter_positive_canvas_dimensions_within_android_s_coordinate': 'accept_retained',
                'string/ui_enter_positive_dimensions': 'accept_retained',
                'string/ui_enter_positive_dimensions_no_larger_than_the_original': 'accept_retained',
                'string/ui_enter_positive_dimensions_that_resolve_to_at_least': 'accept_retained',
                'string/ui_enter_positive_image_dimensions': 'accept_retained',
                'string/ui_enter_valid_dimensions': 'accept_retained',
                'string/ui_eraser': 'accept_retained',
                'string/ui_expand_colour_palette': 'accept_retained_wording_or_route_limited',
                'string/ui_expand_tool_category': 'accept_retained',
                'string/ui_expand_toolbox': 'accept_retained',
                'string/ui_export_as23': 'accept_retained',
                'string/ui_export_did_not_save23': 'accept_retained',
                'string/ui_export_explanation23': 'accept_retained',
                'string/ui_export_recovery_copy': 'accept_retained',
                'string/ui_export_recovery_copy_144b8a': 'accept_retained',
                'string/ui_eyedropper': 'accept_retained',
                'string/ui_fg': 'hold_existing',
                'string/ui_fit': 'accept_retained',
                'string/ui_fit_entire_canvas_in_view': 'accept_retained',
                'string/ui_fit_image': 'hold_existing',
                'string/ui_fit_selection34': 'accept_retained',
                'string/ui_flip_horizontal': 'accept_retained',
                'string/ui_flip_vertical': 'accept_retained',
                'string/ui_font': 'accept_retained',
                'string/ui_font_family': 'accept_retained',
                'string/ui_foreground_background_colour_palette': 'hold_existing',
                'string/ui_foreground_colour': 'accept_retained',
                'string/ui_foreground_edit_colour': 'accept_retained',
                'string/ui_free_form_select': 'accept_retained',
                'string/ui_from_device34': 'accept_retained',
                'string/ui_full_text_copied': 'accept_retained',
                'string/ui_height': 'accept_retained',
                'string/ui_height_in': 'accept_retained',
                'string/ui_heights': 'accept_retained_wording_or_route_limited',
                'string/ui_hex_rrggbb': 'accept_retained',
                'string/ui_hide_editor_controls': 'accept_retained_wording_or_route_limited',
                'string/ui_higher_quality_usually_makes_a_larger_file_lossless': 'accept_retained',
                'string/ui_history_unavailable34': 'accept_retained',
                'string/ui_image': 'accept_retained',
                'string/ui_insert': 'accept_retained_wording_or_route_limited',
                'string/ui_insert_image_into_canvas': 'accept_retained_wording_or_route_limited',
                'string/ui_invalid_autosave_metadata': 'accept_retained',
                'string/ui_invalid_colour': 'accept_retained',
                'string/ui_invalid_selection_outline': 'accept_retained',
                'string/ui_invert_colours': 'accept_retained',
                'string/ui_italic': 'accept_retained',
                'string/ui_keep_editing23': 'accept_retained',
                'string/ui_keeps_pixels_at_the_top_left_smaller_canvas': 'accept_retained',
                'string/ui_languages23': 'accept_retained',
                'string/ui_left': 'accept_retained',
                'string/ui_left_aligned': 'accept_retained',
                'string/ui_left_arrow_collapse': 'accept_retained_wording_or_route_limited',
                'string/ui_line': 'accept_retained',
                'string/ui_line_spacing': 'accept_retained',
                'string/ui_load_image': 'accept_edit',
                'string/ui_lock_aspect_ratio': 'accept_retained',
                'string/ui_lock_proportions': 'accept_retained',
                'string/ui_magnification': 'accept_retained',
                'string/ui_main23': 'hold_existing',
                'string/ui_menu': 'accept_retained_wording_or_route_limited',
                'string/ui_menu_colours': 'accept_retained_wording_or_route_limited',
                'string/ui_menu_edit': 'accept_retained',
                'string/ui_menu_file': 'accept_retained',
                'string/ui_menu_help': 'accept_retained',
                'string/ui_menu_image': 'accept_retained',
                'string/ui_menu_view': 'accept_retained',
                'string/ui_navigate': 'accept_retained',
                'string/ui_new': 'accept_edit',
                'string/ui_new_colour': 'accept_retained_wording_or_route_limited',
                'string/ui_new_image': 'accept_retained',
                'string/ui_no_readable_image_data': 'accept_retained',
                'string/ui_no_resize_fits_decoder_memory': 'accept_retained',
                'string/ui_none': 'accept_retained',
                'string/ui_not_enough_memory_for_this_operation_the_assembly': 'accept_retained',
                'string/ui_not_enough_memory_to_finish_opening_this_image': 'accept_retained',
                'string/ui_not_enough_memory_to_inspect_this_image': 'accept_retained',
                'string/ui_not_enough_memory_to_save_in_this_format': 'accept_retained',
                'string/ui_numeric_slider_value': 'accept_retained',
                'string/ui_ok': 'accept_retained',
                'string/ui_original_size34': 'accept_retained',
                'string/ui_other_images34': 'accept_retained',
                'string/ui_outline': 'accept_retained',
                'string/ui_palette': 'accept_retained',
                'string/ui_paste': 'accept_retained',
                'string/ui_paste_hint34': 'accept_retained',
                'string/ui_pencil': 'accept_retained',
                'string/ui_percent': 'accept_retained',
                'string/ui_percent_fd8671': 'accept_retained',
                'string/ui_pinch_and_pan_mode': 'hold_existing',
                'string/ui_pixels': 'accept_retained',
                'string/ui_pixels_6ec9c2': 'accept_retained',
                'string/ui_place_text': 'accept_retained',
                'string/ui_please_try_again': 'accept_retained',
                'string/ui_please_wait_for_the_current_operation': 'accept_retained',
                'string/ui_png_encoding_failed': 'accept_retained',
                'string/ui_polygon': 'accept_retained',
                'string/ui_preview': 'accept_retained',
                'string/ui_previous_draft_kept_for_recovery': 'accept_retained',
                'string/ui_px': 'accept_retained',
                'string/ui_px_724eb3': 'accept_retained',
                'string/ui_ready': 'accept_retained',
                'string/ui_recovered_image': 'accept_retained',
                'string/ui_recovery_copy_exported_extract_canvas_png_from_the': 'accept_retained',
                'string/ui_rectangle': 'accept_retained',
                'string/ui_rectangle_select': 'accept_retained',
                'string/ui_redo': 'accept_retained',
                'string/ui_remove': 'accept_retained',
                'string/ui_reset_bw23': 'accept_retained',
                'string/ui_reset_crop': 'accept_retained',
                'string/ui_reset_to_black_white': 'accept_retained_wording_or_route_limited',
                'string/ui_resize_and_load': 'accept_retained',
                'string/ui_resize_image': 'accept_retained',
                'string/ui_resize_image_ab28be': 'accept_retained',
                'string/ui_resize_large_image': 'accept_retained',
                'string/ui_resize_the_copy': 'accept_retained',
                'string/ui_right': 'accept_retained',
                'string/ui_right_aligned': 'accept_retained',
                'string/ui_rotate': 'accept_retained',
                'string/ui_rotate_180': 'accept_retained',
                'string/ui_rotate_90_clockwise': 'accept_retained',
                'string/ui_sampled_resize_memory_explanation': 'accept_retained',
                'string/ui_save': 'accept_retained',
                'string/ui_save_a5d0d9': 'accept_edit',
                'string/ui_save_and_share': 'accept_retained',
                'string/ui_save_and_share_41edb4': 'accept_retained',
                'string/ui_save_as': 'hold_existing',
                'string/ui_save_as_jpeg': 'hold_existing',
                'string/ui_save_as_jpeg_xl': 'hold_existing',
                'string/ui_save_as_png': 'hold_existing',
                'string/ui_save_explanation23': 'accept_retained',
                'string/ui_save_png': 'accept_retained',
                'string/ui_save_your_changes': 'accept_retained',
                'string/ui_saved': 'accept_retained',
                'string/ui_scales_the_image_unlock_the_ratio_to_stretch': 'accept_retained',
                'string/ui_select_all': 'accept_retained',
                'string/ui_select_an_area': 'accept_retained',
                'string/ui_select_an_area_first': 'accept_retained',
                'string/ui_selected_colour23': 'accept_retained',
                'string/ui_selection_dimensions_are_too_large': 'accept_retained',
                'string/ui_share_explanation34': 'accept_retained',
                'string/ui_share_saved_image': 'accept_retained',
                'string/ui_show_all': 'accept_retained',
                'string/ui_show_controls': 'accept_retained',
                'string/ui_show_editor_controls': 'accept_retained_wording_or_route_limited',
                'string/ui_show_magnified_drawing_preview': 'accept_retained',
                'string/ui_size_pixels': 'accept_retained',
                'string/ui_size_px': 'accept_retained',
                'string/ui_solid_fill': 'accept_retained',
                'string/ui_swap23': 'accept_retained',
                'string/ui_swap_foreground_background': 'accept_retained_wording_or_route_limited',
                'string/ui_tap_an_image_first': 'accept_retained',
                'string/ui_tap_canvas_to_type': 'accept_retained',
                'string/ui_tap_to_type_a_number': 'accept_retained',
                'string/ui_text': 'accept_retained',
                'string/ui_text_alignment': 'accept_retained',
                'string/ui_text_direction23': 'accept_retained',
                'string/ui_the_crop_must_contain_at_least_one_pixel': 'accept_retained',
                'string/ui_the_crop_must_stay_inside_the_image': 'accept_retained',
                'string/ui_the_decoder_and_editing_buffers_need_about_the': 'accept_retained',
                'string/ui_the_draft_is_saving_try_again_shortly': 'accept_retained',
                'string/ui_the_encoder_did_not_finish': 'accept_retained',
                'string/ui_the_full_image_and_working_buffers_exceed_the': 'accept_retained',
                'string/ui_the_image_was_saved_but_android_could_not': 'accept_retained',
                'string/ui_the_picker_returned_no_file_please_choose_the': 'accept_retained',
                'string/ui_the_picker_returned_no_files': 'accept_retained',
                'string/ui_the_previous_draft_could_not_be_moved_to': 'accept_retained',
                'string/ui_the_previous_draft_could_not_be_preserved_separately': 'accept_retained',
                'string/ui_the_previous_draft_could_not_be_restored': 'accept_retained',
                'string/ui_the_previous_draft_needs_more_memory_to_reopen': 'accept_retained',
                'string/ui_the_saved_assembly_could_not_be_opened': 'accept_retained',
                'string/ui_the_selected_location_is_not_writable': 'accept_retained',
                'string/ui_the_selected_provider_did_not_return_any_image': 'accept_retained',
                'string/ui_the_trim_would_remove_the_entire_image': 'accept_retained',
                'string/ui_the_undo_cache_is_damaged': 'accept_retained',
                'string/ui_there_is_not_enough_memory_for_this_operation': 'accept_retained',
                'string/ui_this_file_is_not_a_supported_image_use': 'accept_retained',
                'string/ui_this_location_is_not_writable': 'accept_retained',
                'string/ui_tolerance': 'accept_retained',
                'string/ui_too_large_for_the_current_budget_reduce_the': 'accept_retained',
                'string/ui_tool_categories': 'accept_retained_wording_or_route_limited',
                'string/ui_trim_amounts_must_be_zero_or_greater': 'accept_retained',
                'string/ui_trim_amounts_must_fit_inside_each_image_use': 'accept_retained',
                'string/ui_trim_expand_canvas_by_touch': 'accept_retained_wording_or_route_limited',
                'string/ui_try_a_different_file_or_location': 'accept_retained',
                'string/ui_type_text': 'accept_retained',
                'string/ui_underline': 'accept_retained',
                'string/ui_undo': 'accept_retained',
                'string/ui_unexpected_data_in_the_undo_cache': 'accept_retained',
                'string/ui_untitled': 'accept_retained',
                'string/ui_use_1_1024_pixels': 'accept_retained',
                'string/ui_use_50_300': 'accept_retained',
                'string/ui_use_a_positive_target_dimension': 'accept_retained',
                'string/ui_use_colour': 'accept_retained',
                'string/ui_use_rrggbb': 'accept_retained',
                'string/ui_watercolor': 'accept_retained',
                'string/ui_width': 'accept_retained',
                'string/ui_working': 'accept_retained',
                'string/ui_your_current_image_has_unsaved_changes': 'accept_retained',
                'string/ui_zoom_in': 'accept_retained',
                'string/ui_zoom_out': 'accept_retained'},
 'tok': {'string/colour_converter_unavailable': 'accept_edit',
         'string/colour_invalid_metadata': 'accept_edit',
         'string/colour_truncated_metadata': 'accept_edit',
         'string/colour_unsupported_icc_model': 'accept_edit',
         'string/commons_svg_original_size_too_large': 'accept_edit',
         'string/commons_svg_original_size_unavailable': 'accept_edit',
         'string/formats22_animation_message': 'accept_edit',
         'string/formats22_animation_poster': 'accept_edit',
         'string/formats22_animation_still': 'accept_edit',
         'string/formats22_animation_title': 'accept_edit',
         'string/formats22_animation_unknown': 'accept_edit',
         'string/formats22_ascii_description': 'accept_edit',
         'string/formats22_derived_exported': 'hold_absent',
         'string/formats22_import_limit': 'accept_edit',
         'string/formats22_open_still': 'accept_edit',
         'string/formats22_pdf_raster_hint': 'accept_edit',
         'string/gallery_credit_could_not_save': 'accept_edit',
         'string/gallery_credit_too_large': 'accept_edit',
         'string/language20_app_language': 'accept_edit',
         'string/language20_current': 'accept_edit',
         'string/language20_device_default': 'accept_edit',
         'string/language20_settings': 'accept_edit',
         'string/language20_translation_note': 'accept_edit',
         'string/legacy_credits_unreadable': 'accept_edit',
         'string/save20_destination_error': 'accept_edit',
         'string/save20_encoding_budget': 'accept_edit',
         'string/save20_file_format': 'accept_edit',
         'string/save20_file_name': 'accept_edit',
         'string/save20_gif_description': 'accept_edit',
         'string/save20_invalid_name': 'accept_edit',
         'string/save20_lossy_quality_description': 'accept_edit',
         'string/save20_title': 'accept_edit',
         'string/save20_unsupported_image_colour': 'accept_edit',
         'string/ui_0f_0f_px_1f': 'accept_edit',
         'string/ui_100': 'accept_edit',
         'string/ui_1_px': 'accept_edit_wording_or_route_limited',
         'string/ui_1f_s': 'accept_edit',
         'string/ui_a_separate_recovery_copy_has_been_kept_use': 'accept_edit',
         'string/ui_actual_size_100': 'accept_edit_wording_or_route_limited',
         'string/ui_add_colour26': 'accept_edit',
         'string/ui_add_text': 'accept_edit',
         'string/ui_airbrush': 'accept_edit',
         'string/ui_all': 'accept_edit',
         'string/ui_an_assembly_source_image_is_missing': 'accept_edit',
         'string/ui_android_blocked_the_file_picker': 'accept_edit',
         'string/ui_android_could_not_decode_this_image': 'accept_edit',
         'string/ui_android_could_not_find_a_file_picker_enable': 'accept_edit',
         'string/ui_apply': 'accept_edit',
         'string/ui_apply_bounds': 'accept_edit',
         'string/ui_apply_crop': 'accept_edit',
         'string/ui_assembly_saved': 'accept_edit',
         'string/ui_assembly_source_memory_floor': 'accept_edit',
         'string/ui_autosave_failed_use_save': 'accept_edit',
         'string/ui_autosave_image_encoding_failed': 'accept_edit',
         'string/ui_autosave_is_paused_to_protect_that_draft_use': 'accept_edit',
         'string/ui_autosave_metadata_is_missing': 'accept_edit',
         'string/ui_autosave_paused_use_save': 'accept_edit',
         'string/ui_autosave_pixels_are_missing': 'accept_edit',
         'string/ui_autosave_pixels_could_not_be_read': 'accept_edit',
         'string/ui_autosave_selection_encoding_failed': 'accept_edit',
         'string/ui_autosaving_draft': 'accept_edit',
         'string/ui_background_colour': 'accept_edit',
         'string/ui_background_edit_colour': 'accept_edit',
         'string/ui_basic_colours': 'accept_edit',
         'string/ui_bg': 'hold_absent',
         'string/ui_bold': 'accept_edit',
         'string/ui_bottom': 'accept_edit',
         'string/ui_brush': 'accept_edit',
         'string/ui_bucket_fill': 'accept_edit',
         'string/ui_cancel': 'accept_edit',
         'string/ui_cannot_create_the_undo_cache_free_some_device': 'accept_edit',
         'string/ui_canvas_bounds': 'accept_edit',
         'string/ui_canvas_size': 'accept_edit',
         'string/ui_canvas_size_30460e': 'accept_edit',
         'string/ui_canvas_zoom': 'accept_edit',
         'string/ui_canvas_zoom_771f84': 'accept_edit',
         'string/ui_category_brush': 'accept_edit_wording_or_route_limited',
         'string/ui_category_insert': 'accept_edit',
         'string/ui_category_selection': 'accept_edit',
         'string/ui_centred': 'accept_edit',
         'string/ui_choose_a_smaller_output_copy_the_source_images': 'accept_edit',
         'string/ui_choose_a_smaller_size': 'accept_edit',
         'string/ui_choose_at_least_one_image': 'accept_edit',
         'string/ui_choose_dimensions_no_larger_than_the_original': 'accept_edit',
         'string/ui_choose_location': 'accept_edit',
         'string/ui_clear_all': 'accept_edit',
         'string/ui_clear_image': 'accept_edit',
         'string/ui_codec_resize_memory_floor': 'accept_edit',
         'string/ui_collapse_colour_palette': 'accept_edit_wording_or_route_limited',
         'string/ui_collapse_tool_category': 'accept_edit',
         'string/ui_collapse_toolbox': 'accept_edit',
         'string/ui_colour': 'accept_edit',
         'string/ui_colour_palette_tap_for_foreground_hold_for_background': 'accept_edit',
         'string/ui_colour_tab23': 'accept_edit',
         'string/ui_colour_tap_foreground_hold_background': 'accept_edit',
         'string/ui_commit_selection': 'accept_edit',
         'string/ui_copy': 'accept_edit',
         'string/ui_copy_all': 'accept_edit',
         'string/ui_could_not_apply_the_crop': 'accept_edit',
         'string/ui_could_not_complete_the_edit': 'accept_edit',
         'string/ui_could_not_complete_the_operation': 'accept_edit',
         'string/ui_could_not_export_the_recovery_copy': 'accept_edit',
         'string/ui_could_not_open_image': 'accept_edit',
         'string/ui_could_not_place_the_image': 'accept_edit',
         'string/ui_could_not_prepare_the_image': 'accept_edit',
         'string/ui_could_not_save_image': 'accept_edit',
         'string/ui_could_not_save_the_assembly': 'accept_edit',
         'string/ui_could_not_store_the_assembly': 'accept_edit',
         'string/ui_crop': 'accept_edit',
         'string/ui_crop_image': 'accept_edit',
         'string/ui_crop_must_stay_inside_the_canvas': 'accept_edit',
         'string/ui_crop_preview_drag_an_edge_or_corner_drag': 'accept_edit',
         'string/ui_crop_to_selection': 'accept_edit',
         'string/ui_cut': 'accept_edit',
         'string/ui_d_d_pixels_2f_mp_exceeds_the_current': 'accept_edit',
         'string/ui_d_d_px_d_pixels_2f_mp': 'accept_edit',
         'string/ui_delete_selection': 'accept_edit',
         'string/ui_discard': 'accept_edit_wording_or_route_limited',
         'string/ui_discard_changes23': 'accept_edit',
         'string/ui_done': 'accept_edit',
         'string/ui_draft_not_saved_yet': 'accept_edit',
         'string/ui_draft_pending': 'accept_edit',
         'string/ui_draft_restored': 'accept_edit',
         'string/ui_draft_saved': 'accept_edit',
         'string/ui_draw26': 'accept_edit',
         'string/ui_draw_again': 'accept_edit',
         'string/ui_drawing23': 'accept_edit',
         'string/ui_drawing_canvas_pinch_and_move_two_fingers_to': 'accept_edit',
         'string/ui_drawing_settings': 'accept_edit',
         'string/ui_drawing_settings_d900c6': 'accept_edit',
         'string/ui_edit_background': 'accept_edit_wording_or_route_limited',
         'string/ui_edit_canvas33': 'accept_edit',
         'string/ui_edit_colour26': 'accept_edit',
         'string/ui_edit_foreground': 'accept_edit_wording_or_route_limited',
         'string/ui_edit_transform33': 'accept_edit',
         'string/ui_ellipse': 'accept_edit',
         'string/ui_enter_a_number_from_to': 'accept_edit',
         'string/ui_enter_a_positive_size': 'accept_edit',
         'string/ui_enter_a_trim_amount_for_every_edge': 'accept_edit',
         'string/ui_enter_a_whole_number_from_to': 'accept_edit',
         'string/ui_enter_all_four_trim_amounts': 'accept_edit',
         'string/ui_enter_positive_canvas_dimensions_within_android_s_coordinate': 'accept_edit',
         'string/ui_enter_positive_dimensions': 'accept_edit',
         'string/ui_enter_positive_dimensions_no_larger_than_the_original': 'accept_edit',
         'string/ui_enter_positive_dimensions_that_resolve_to_at_least': 'accept_edit',
         'string/ui_enter_positive_image_dimensions': 'accept_edit',
         'string/ui_enter_valid_dimensions': 'accept_edit',
         'string/ui_eraser': 'accept_edit',
         'string/ui_expand_colour_palette': 'accept_edit_wording_or_route_limited',
         'string/ui_expand_tool_category': 'accept_edit',
         'string/ui_expand_toolbox': 'accept_edit',
         'string/ui_export_as23': 'accept_edit',
         'string/ui_export_did_not_save23': 'accept_edit',
         'string/ui_export_explanation23': 'accept_edit',
         'string/ui_export_recovery_copy': 'accept_edit',
         'string/ui_export_recovery_copy_144b8a': 'accept_edit',
         'string/ui_eyedropper': 'accept_edit',
         'string/ui_fg': 'hold_absent',
         'string/ui_fit': 'accept_edit',
         'string/ui_fit_entire_canvas_in_view': 'accept_edit',
         'string/ui_fit_image': 'hold_absent',
         'string/ui_fit_selection34': 'accept_edit',
         'string/ui_flip_horizontal': 'accept_edit',
         'string/ui_flip_vertical': 'accept_edit',
         'string/ui_font': 'accept_edit',
         'string/ui_font_family': 'accept_edit',
         'string/ui_foreground_background_colour_palette': 'hold_absent',
         'string/ui_foreground_colour': 'accept_edit',
         'string/ui_foreground_edit_colour': 'accept_edit',
         'string/ui_free_form_select': 'accept_edit',
         'string/ui_from_device34': 'accept_edit',
         'string/ui_full_text_copied': 'accept_edit',
         'string/ui_height': 'accept_edit',
         'string/ui_height_in': 'accept_edit',
         'string/ui_heights': 'accept_edit_wording_or_route_limited',
         'string/ui_hex_rrggbb': 'accept_edit',
         'string/ui_hide_editor_controls': 'accept_edit_wording_or_route_limited',
         'string/ui_higher_quality_usually_makes_a_larger_file_lossless': 'accept_edit',
         'string/ui_history_unavailable34': 'accept_edit',
         'string/ui_image': 'accept_edit',
         'string/ui_insert': 'accept_edit_wording_or_route_limited',
         'string/ui_insert_image_into_canvas': 'accept_edit_wording_or_route_limited',
         'string/ui_invalid_autosave_metadata': 'accept_edit',
         'string/ui_invalid_colour': 'accept_edit',
         'string/ui_invalid_selection_outline': 'accept_edit',
         'string/ui_invert_colours': 'accept_edit',
         'string/ui_italic': 'accept_edit',
         'string/ui_keep_editing23': 'accept_edit',
         'string/ui_keeps_pixels_at_the_top_left_smaller_canvas': 'accept_edit',
         'string/ui_languages23': 'accept_edit',
         'string/ui_left': 'accept_edit',
         'string/ui_left_aligned': 'accept_edit',
         'string/ui_left_arrow_collapse': 'accept_edit_wording_or_route_limited',
         'string/ui_line': 'accept_edit',
         'string/ui_line_spacing': 'accept_edit',
         'string/ui_load_image': 'accept_edit',
         'string/ui_lock_aspect_ratio': 'accept_edit',
         'string/ui_lock_proportions': 'accept_edit',
         'string/ui_magnification': 'accept_edit',
         'string/ui_main23': 'hold_absent',
         'string/ui_menu': 'accept_edit_wording_or_route_limited',
         'string/ui_menu_colours': 'accept_edit_wording_or_route_limited',
         'string/ui_menu_edit': 'accept_retained',
         'string/ui_menu_file': 'accept_edit',
         'string/ui_menu_help': 'accept_edit',
         'string/ui_menu_image': 'accept_edit',
         'string/ui_menu_view': 'accept_edit',
         'string/ui_navigate': 'accept_edit',
         'string/ui_new': 'accept_edit',
         'string/ui_new_colour': 'accept_edit_wording_or_route_limited',
         'string/ui_new_image': 'accept_edit',
         'string/ui_no_readable_image_data': 'accept_edit',
         'string/ui_no_resize_fits_decoder_memory': 'accept_edit',
         'string/ui_none': 'accept_edit',
         'string/ui_not_enough_memory_for_this_operation_the_assembly': 'accept_edit',
         'string/ui_not_enough_memory_to_finish_opening_this_image': 'accept_edit',
         'string/ui_not_enough_memory_to_inspect_this_image': 'accept_edit',
         'string/ui_not_enough_memory_to_save_in_this_format': 'accept_edit',
         'string/ui_numeric_slider_value': 'accept_edit',
         'string/ui_ok': 'accept_retained',
         'string/ui_original_size34': 'accept_edit',
         'string/ui_other_images34': 'accept_edit',
         'string/ui_outline': 'accept_edit',
         'string/ui_palette': 'accept_edit',
         'string/ui_paste': 'accept_edit',
         'string/ui_paste_hint34': 'accept_edit',
         'string/ui_pencil': 'accept_edit',
         'string/ui_percent': 'accept_edit',
         'string/ui_percent_fd8671': 'accept_edit',
         'string/ui_pinch_and_pan_mode': 'hold_absent',
         'string/ui_pixels': 'accept_edit',
         'string/ui_pixels_6ec9c2': 'accept_edit',
         'string/ui_place_text': 'accept_edit',
         'string/ui_please_try_again': 'accept_edit',
         'string/ui_please_wait_for_the_current_operation': 'accept_edit',
         'string/ui_png_encoding_failed': 'accept_edit',
         'string/ui_polygon': 'accept_edit',
         'string/ui_preview': 'accept_edit',
         'string/ui_previous_draft_kept_for_recovery': 'accept_edit',
         'string/ui_px': 'accept_edit',
         'string/ui_px_724eb3': 'accept_edit',
         'string/ui_ready': 'accept_edit',
         'string/ui_recovered_image': 'accept_edit',
         'string/ui_recovery_copy_exported_extract_canvas_png_from_the': 'accept_edit',
         'string/ui_rectangle': 'accept_edit',
         'string/ui_rectangle_select': 'accept_edit',
         'string/ui_redo': 'accept_edit',
         'string/ui_remove': 'accept_edit',
         'string/ui_reset_bw23': 'accept_edit',
         'string/ui_reset_crop': 'accept_edit',
         'string/ui_reset_to_black_white': 'accept_edit_wording_or_route_limited',
         'string/ui_resize_and_load': 'accept_edit',
         'string/ui_resize_image': 'accept_edit',
         'string/ui_resize_image_ab28be': 'accept_edit',
         'string/ui_resize_large_image': 'accept_edit',
         'string/ui_resize_the_copy': 'accept_edit',
         'string/ui_right': 'accept_edit',
         'string/ui_right_aligned': 'accept_edit',
         'string/ui_rotate': 'accept_edit',
         'string/ui_rotate_180': 'accept_edit',
         'string/ui_rotate_90_clockwise': 'accept_edit',
         'string/ui_sampled_resize_memory_explanation': 'accept_edit',
         'string/ui_save': 'accept_retained',
         'string/ui_save_a5d0d9': 'accept_edit',
         'string/ui_save_and_share': 'accept_edit',
         'string/ui_save_and_share_41edb4': 'accept_edit',
         'string/ui_save_as': 'hold_absent',
         'string/ui_save_as_jpeg': 'hold_absent',
         'string/ui_save_as_jpeg_xl': 'hold_absent',
         'string/ui_save_as_png': 'hold_absent',
         'string/ui_save_explanation23': 'accept_edit',
         'string/ui_save_png': 'accept_edit',
         'string/ui_save_your_changes': 'accept_edit',
         'string/ui_saved': 'accept_edit',
         'string/ui_scales_the_image_unlock_the_ratio_to_stretch': 'accept_edit',
         'string/ui_select_all': 'accept_edit',
         'string/ui_select_an_area': 'accept_edit',
         'string/ui_select_an_area_first': 'accept_edit',
         'string/ui_selected_colour23': 'accept_edit',
         'string/ui_selection_dimensions_are_too_large': 'accept_edit',
         'string/ui_share_explanation34': 'accept_edit',
         'string/ui_share_saved_image': 'accept_edit',
         'string/ui_show_all': 'accept_edit',
         'string/ui_show_controls': 'accept_edit',
         'string/ui_show_editor_controls': 'accept_edit_wording_or_route_limited',
         'string/ui_show_magnified_drawing_preview': 'accept_edit',
         'string/ui_size_pixels': 'accept_edit',
         'string/ui_size_px': 'accept_edit',
         'string/ui_solid_fill': 'accept_edit',
         'string/ui_swap23': 'accept_edit',
         'string/ui_swap_foreground_background': 'accept_edit_wording_or_route_limited',
         'string/ui_tap_an_image_first': 'accept_edit',
         'string/ui_tap_canvas_to_type': 'accept_edit',
         'string/ui_tap_to_type_a_number': 'accept_edit',
         'string/ui_text': 'accept_edit',
         'string/ui_text_alignment': 'accept_edit',
         'string/ui_text_direction23': 'accept_edit',
         'string/ui_the_crop_must_contain_at_least_one_pixel': 'accept_edit',
         'string/ui_the_crop_must_stay_inside_the_image': 'accept_edit',
         'string/ui_the_decoder_and_editing_buffers_need_about_the': 'accept_edit',
         'string/ui_the_draft_is_saving_try_again_shortly': 'accept_edit',
         'string/ui_the_encoder_did_not_finish': 'accept_edit',
         'string/ui_the_full_image_and_working_buffers_exceed_the': 'accept_edit',
         'string/ui_the_image_was_saved_but_android_could_not': 'accept_edit',
         'string/ui_the_picker_returned_no_file_please_choose_the': 'accept_edit',
         'string/ui_the_picker_returned_no_files': 'accept_edit',
         'string/ui_the_previous_draft_could_not_be_moved_to': 'accept_edit',
         'string/ui_the_previous_draft_could_not_be_preserved_separately': 'accept_edit',
         'string/ui_the_previous_draft_could_not_be_restored': 'accept_edit',
         'string/ui_the_previous_draft_needs_more_memory_to_reopen': 'accept_edit',
         'string/ui_the_saved_assembly_could_not_be_opened': 'accept_edit',
         'string/ui_the_selected_location_is_not_writable': 'accept_edit',
         'string/ui_the_selected_provider_did_not_return_any_image': 'accept_edit',
         'string/ui_the_trim_would_remove_the_entire_image': 'accept_edit',
         'string/ui_the_undo_cache_is_damaged': 'accept_edit',
         'string/ui_there_is_not_enough_memory_for_this_operation': 'accept_edit',
         'string/ui_this_file_is_not_a_supported_image_use': 'accept_edit',
         'string/ui_this_location_is_not_writable': 'accept_edit',
         'string/ui_tolerance': 'accept_edit',
         'string/ui_too_large_for_the_current_budget_reduce_the': 'accept_edit',
         'string/ui_tool_categories': 'accept_edit_wording_or_route_limited',
         'string/ui_trim_amounts_must_be_zero_or_greater': 'accept_edit',
         'string/ui_trim_amounts_must_fit_inside_each_image_use': 'accept_edit',
         'string/ui_trim_expand_canvas_by_touch': 'accept_edit_wording_or_route_limited',
         'string/ui_try_a_different_file_or_location': 'accept_edit',
         'string/ui_type_text': 'accept_edit',
         'string/ui_underline': 'accept_edit',
         'string/ui_undo': 'accept_edit',
         'string/ui_unexpected_data_in_the_undo_cache': 'accept_edit',
         'string/ui_untitled': 'accept_edit',
         'string/ui_use_1_1024_pixels': 'accept_edit',
         'string/ui_use_50_300': 'accept_edit',
         'string/ui_use_a_positive_target_dimension': 'accept_edit',
         'string/ui_use_colour': 'accept_edit',
         'string/ui_use_rrggbb': 'accept_edit',
         'string/ui_watercolor': 'accept_edit',
         'string/ui_width': 'accept_edit',
         'string/ui_working': 'accept_edit',
         'string/ui_your_current_image_has_unsaved_changes': 'accept_edit',
         'string/ui_zoom_in': 'accept_edit',
         'string/ui_zoom_out': 'accept_edit'}}
PREDECESSORS={'ary': {},
 'mn-Cyrl-MN': {'colour_converter_unavailable': {'attributes': {'name': 'colour_converter_unavailable'},
                                                 'target': 'Зургийн өнгө хөрвүүлэгчийг эхлүүлж чадсангүй. Зургийг '
                                                           'импортлоогүй.',
                                                 'type': 'string'},
                'colour_invalid_metadata': {'attributes': {'name': 'colour_invalid_metadata'},
                                            'target': 'Зургийн өнгөний мета өгөгдөл буруу эсвэл дэмжигдээгүй.',
                                            'type': 'string'},
                'colour_truncated_metadata': {'attributes': {'name': 'colour_truncated_metadata'},
                                              'target': 'Зургийн өгөгдөл өнгөний мета өгөгдлийн дунд тасарсан.',
                                              'type': 'string'},
                'colour_unsupported_icc_model': {'attributes': {'name': 'colour_unsupported_icc_model'},
                                                 'target': 'Энэ зураг зургийн декодер хөрвүүлж чадахгүй ICC өнгөний '
                                                           'загвар ашиглаж байна. Эхлээд өнгө удирддаг апп-аар RGB '
                                                           'хуулбар экспортлоно уу.',
                                                 'type': 'string'},
                'commons_svg_original_size_too_large': {'attributes': {'name': 'commons_svg_original_size_too_large'},
                                                        'target': 'SVG-ийн анхны хэмжээ Android-ийн bitmap-ийн '
                                                                  'хэмжээсийн хязгаараас давсан. Хэмжээг өөрчлөөгүй.',
                                                        'type': 'string'},
                'commons_svg_original_size_unavailable': {'attributes': {'name': 'commons_svg_original_size_unavailable'},
                                                          'target': 'SVG файлд ашиглаж болох анхны хэмжээг заагаагүй '
                                                                    'байна. Зургийн талбарт үндэслэсэн хэмжээг '
                                                                    'орлуулан ашиглаагүй.',
                                                          'type': 'string'},
                'formats22_animation_message': {'attributes': {'name': 'formats22_animation_message'},
                                                'target': 'Энэ %1$s нь %2$s кадр агуулна. AN Paint хөдөлгөөнгүй зураг '
                                                          'засварладаг бөгөөд анимацийг хадгалдаггүй.',
                                                'type': 'string'},
                'formats22_animation_poster': {'attributes': {'name': 'formats22_animation_poster'},
                                               'target': 'Энэ PNG тусдаа үндсэн зурагтай. Анимэйшний кадруудын оронд '
                                                         'тэр зургийг импортлоно. Хадгалах үед хөдөлгөөнгүй зураг '
                                                         'үүснэ.',
                                               'type': 'string'},
                'formats22_animation_still': {'attributes': {'name': 'formats22_animation_still'},
                                              'target': 'Зөвхөн эхний кадрыг импортлоно. Хадгалах үед хөдөлгөөнгүй '
                                                        'зураг үүснэ.',
                                              'type': 'string'},
                'formats22_animation_title': {'attributes': {'name': 'formats22_animation_title'},
                                              'target': 'Хөдөлгөөнт зураг',
                                              'type': 'string'},
                'formats22_animation_unknown': {'attributes': {'name': 'formats22_animation_unknown'},
                                                'target': 'Энэ %1$s нь олон кадр агуулж байгаа эсэхийг батлахад хэт '
                                                          'төвөгтэй байна. AN Paint зөвхөн хөдөлгөөнгүй зургийг нээж, '
                                                          'анимацийг хадгалахгүй.',
                                                'type': 'string'},
                'formats22_ascii_description': {'attributes': {'name': 'formats22_ascii_description'},
                                                'target': 'Гэрэл ба бараан тэмдэгт ашиглан энгийн текст бичнэ. Ижил '
                                                          'өргөнтэй фонтоор харна уу. Энэ нь зөвхөн дүрслэл тул анхны '
                                                          'зураг болгон дахин нээж болохгүй.',
                                                'type': 'string'},
                'formats22_at_least_frames': {'attributes': {'name': 'formats22_at_least_frames'},
                                              'target': 'дор хаяж %1$d',
                                              'type': 'string'},
                'formats22_derived_exported': {'attributes': {'name': 'formats22_derived_exported'},
                                               'target': '%1$s экспортоллоо. Бүтэн зурагт хадгалаагүй өөрчлөлт хэвээр '
                                                         'байна; солихоос өмнө бүтэн зургийн хуулбарыг хадгална уу.',
                                               'type': 'string'},
                'formats22_import_limit': {'attributes': {'name': 'formats22_import_limit'},
                                           'target': 'Энэ файл 512 MiB импортын хязгаараас давсан. Жижиг файл сонгоно '
                                                     'уу.',
                                           'type': 'string'},
                'formats22_open_still': {'attributes': {'name': 'formats22_open_still'},
                                         'target': 'Хөдөлгөөнгүй зураг нээх',
                                         'type': 'string'},
                'formats22_pdf_raster_hint': {'attributes': {'name': 'formats22_pdf_raster_hint'},
                                              'target': 'PDF хуудсыг 144 dpi-аар дүрслэнэ. Текст ба вектор объект '
                                                        'пиксел болно.',
                                              'type': 'string'},
                'gallery_credit_could_not_save': {'attributes': {'name': 'gallery_credit_could_not_save'},
                                                  'target': 'Зургийн эх сурвалжийн мэдээллийг хадгалж эсвэл сэргээж '
                                                            'чадсангүй. Өмнө хадгалсан мэдээллийг хэвээр үлдээлээ. '
                                                            'Дахин оролдоно уу.',
                                                  'type': 'string'},
                'gallery_credit_too_large': {'attributes': {'name': 'gallery_credit_too_large'},
                                             'target': 'Эх сурвалжийн энэ мэдээлэл нь зургийг сэргээх боломжгүй болтол '
                                                       'томруулна. Таны өмнөх зураг болон эх сурвалжийн мэдээллийг '
                                                       'хэвээр үлдээлээ.',
                                             'type': 'string'},
                'language20_app_language': {'attributes': {'name': 'language20_app_language'},
                                            'target': 'Аппын хэл',
                                            'type': 'string'},
                'language20_current': {'attributes': {'name': 'language20_current'},
                                       'target': 'Аппын хэл: %1$s',
                                       'type': 'string'},
                'language20_device_default': {'attributes': {'name': 'language20_device_default'},
                                              'target': 'Төхөөрөмжийн хэл',
                                              'type': 'string'},
                'language20_settings': {'attributes': {'name': 'language20_settings'},
                                        'target': 'Тохиргоо',
                                        'type': 'string'},
                'language20_translation_note': {'attributes': {'name': 'language20_translation_note'},
                                                'target': 'Аппын хэл\\n\\nОрчуулгыг AN Paint-ийн хэлний нөөцөд '
                                                          'хадгалж, шинэчилдэг. Шинэ эсвэл орчуулагдаагүй текст '
                                                          'англиар харагдана.',
                                                'type': 'string'},
                'legacy_credits_unreadable': {'attributes': {'name': 'legacy_credits_unreadable'},
                                              'target': 'Хадгалсан эх сурвалжийн мэдээллийн заримыг уншиж чадсангүй. '
                                                        'Хадгалсан хуулбаруудыг нь хэвээр үлдээлээ.',
                                              'type': 'string'},
                'save20_destination_error': {'attributes': {'name': 'save20_destination_error'},
                                             'target': 'Дууссан зураг зорилтот файлаа сольж чадсангүй.',
                                             'type': 'string'},
                'save20_dither': {'attributes': {'name': 'save20_dither'},
                                  'target': 'Өнгийг дизерлэх',
                                  'type': 'string'},
                'save20_encoding_budget': {'attributes': {'name': 'save20_encoding_budget'},
                                           'target': 'Зураг болон кодлох буферууд экспортын санах ойн хязгаараас '
                                                     'давсан.',
                                           'type': 'string'},
                'save20_file_format': {'attributes': {'name': 'save20_file_format'},
                                       'target': 'Файлын формат',
                                       'type': 'string'},
                'save20_file_name': {'attributes': {'name': 'save20_file_name'},
                                     'target': 'Файлын нэр',
                                     'type': 'string'},
                'save20_gif_description': {'attributes': {'name': 'save20_gif_description'},
                                           'target': 'Хөдөлгөөнгүй зураг, 256 хүртэл өнгө. Дизерлэх нь өнгөний '
                                                     'шилжилтийг жигд харагдуулна. Хөдөлгөөнт GIF-ийн эхний кадр '
                                                     'нээгдэнэ.',
                                           'type': 'string'},
                'save20_invalid_name': {'attributes': {'name': 'save20_invalid_name'},
                                        'target': 'Ташуу зураас эсвэл удирдлагын тэмдэггүй файлын нэр оруулна уу.',
                                        'type': 'string'},
                'save20_lossy_quality_description': {'attributes': {'name': 'save20_lossy_quality_description'},
                                                     'target': 'Өндөр чанар илүү их нарийвчлал хадгалж, ихэвчлэн том '
                                                               'файл үүсгэнэ.',
                                                     'type': 'string'},
                'save20_title': {'attributes': {'name': 'save20_title'},
                                 'target': 'Өөрөөр хадгалах…',
                                 'type': 'string'},
                'save20_unsupported_image_colour': {'attributes': {'name': 'save20_unsupported_image_colour'},
                                                    'target': 'Энэ зураг нь AN Paint одоогоор хөрвүүлж чадахгүй '
                                                              'өнгөний профайл ашиглаж байна. Импортлохоос өмнө өнгө '
                                                              'удирддаг засварлагчаар sRGB PNG болгон хөрвүүлнэ үү.',
                                                    'type': 'string'},
                'ui_0f_0f_px_1f': {'attributes': {'name': 'ui_0f_0f_px_1f'},
                                   'target': '%1$.0f × %2$.0f px\\n%3$.1f°',
                                   'type': 'string'},
                'ui_100': {'attributes': {'formatted': 'false', 'name': 'ui_100'}, 'target': '100%', 'type': 'string'},
                'ui_1_px': {'attributes': {'name': 'ui_1_px'}, 'target': '1 px', 'type': 'string'},
                'ui_1f_s': {'attributes': {'name': 'ui_1f_s'}, 'target': '%1$.1f %2$s', 'type': 'string'},
                'ui_a_separate_recovery_copy_has_been_kept_use': {'attributes': {'name': 'ui_a_separate_recovery_copy_has_been_kept_use'},
                                                                  'target': '%1$s Тусдаа сэргээх хуулбар хадгалагдсан. '
                                                                            'ZIP файлыг хадгалахын тулд Файл > Сэргээх '
                                                                            'хуулбар экспортлох командыг ашиглана уу. '
                                                                            'Шаардлагатай бол түүнээс canvas.png '
                                                                            'файлыг гаргаж аваад зураг болгон нээж '
                                                                            'ердийн хэмжээ өөрчлөх тохиргоог ашиглана '
                                                                            'уу.',
                                                                  'type': 'string'},
                'ui_actual_size_100': {'attributes': {'formatted': 'false', 'name': 'ui_actual_size_100'},
                                       'target': 'Бодит хэмжээ (100%)',
                                       'type': 'string'},
                'ui_add_colour26': {'attributes': {'name': 'ui_add_colour26'},
                                    'target': 'Өнгө нэмэх',
                                    'type': 'string'},
                'ui_add_text': {'attributes': {'name': 'ui_add_text'}, 'target': 'Текст нэмэх', 'type': 'string'},
                'ui_airbrush': {'attributes': {'name': 'ui_airbrush'}, 'target': 'Шүршигч', 'type': 'string'},
                'ui_all': {'attributes': {'name': 'ui_all'}, 'target': 'Бүгд', 'type': 'string'},
                'ui_an_assembly_source_image_is_missing': {'attributes': {'name': 'ui_an_assembly_source_image_is_missing'},
                                                           'target': 'Эвлүүлгийн эх зураг алга.',
                                                           'type': 'string'},
                'ui_an_paint_image_assembly': {'attributes': {'name': 'ui_an_paint_image_assembly'},
                                               'target': 'AN Paint · Зураг эвлүүлэх',
                                               'type': 'string'},
                'ui_an_paint_image_assembly_20_images_placed': {'attributes': {'name': 'ui_an_paint_image_assembly_20_images_placed'},
                                                                'target': 'AN Paint · Зураг эвлүүлэх\\n%1$s/20 зураг · '
                                                                          '%2$s байрлуулсан',
                                                                'type': 'string'},
                'ui_android_blocked_the_file_picker': {'attributes': {'name': 'ui_android_blocked_the_file_picker'},
                                                       'target': 'Android файл сонгогчийг хориглосон: %1$s',
                                                       'type': 'string'},
                'ui_android_could_not_decode_this_image': {'attributes': {'name': 'ui_android_could_not_decode_this_image'},
                                                           'target': 'Android энэ зургийг тайлж чадсангүй.',
                                                           'type': 'string'},
                'ui_android_could_not_find_a_file_picker_enable': {'attributes': {'name': 'ui_android_could_not_find_a_file_picker_enable'},
                                                                   'target': 'Android файл сонгогч олсонгүй. '
                                                                             'Android-ын тохиргоонд Files эсвэл '
                                                                             'Documents аппыг идэвхжүүлээд дахин '
                                                                             'оролдоно уу.',
                                                                   'type': 'string'},
                'ui_apply': {'attributes': {'name': 'ui_apply'}, 'target': 'Хэрэглэх', 'type': 'string'},
                'ui_apply_bounds': {'attributes': {'name': 'ui_apply_bounds'},
                                    'target': 'Хүрээг хэрэглэх',
                                    'type': 'string'},
                'ui_apply_crop': {'attributes': {'name': 'ui_apply_crop'},
                                  'target': 'Тайралтыг хэрэглэх',
                                  'type': 'string'},
                'ui_arrow': {'attributes': {'name': 'ui_arrow'}, 'target': 'Сум', 'type': 'string'},
                'ui_assembly_saved': {'attributes': {'name': 'ui_assembly_saved'},
                                      'target': 'Эвлүүлгийг хадгаллаа',
                                      'type': 'string'},
                'ui_assembly_source_memory_floor': {'attributes': {'name': 'ui_assembly_source_memory_floor'},
                                                    'target': 'Тооцоолсноор, гаралтын хэмжээг хамгийн бага болгосон ч '
                                                              'энэ эвлүүлэг одоогийн ажлын санах ойд хуваарилсан '
                                                              'хэмжээнээс хэтэрнэ. Одоогийн хязгаарын хүрээнд зөвхөн '
                                                              'эвлүүлгийн хэмжээг багасгах нь хангалтгүй. Дахин '
                                                              'оролдохоос өмнө бусад баримтыг хаана уу эсвэл илүү '
                                                              'жижиг эх зураг бэлтгэнэ үү. Таны эвлүүлэг '
                                                              'өөрчлөгдөөгүй.',
                                                    'type': 'string'},
                'ui_autosave_failed_use_save': {'attributes': {'name': 'ui_autosave_failed_use_save'},
                                                'target': 'Автоматаар хадгалах амжилтгүй · «Хадгалах»-ыг ашиглана уу',
                                                'type': 'string'},
                'ui_autosave_image_encoding_failed': {'attributes': {'name': 'ui_autosave_image_encoding_failed'},
                                                      'target': 'Автоматаар хадгалах зургийн кодчилол амжилтгүй.',
                                                      'type': 'string'},
                'ui_autosave_is_paused_to_protect_that_draft_use': {'attributes': {'name': 'ui_autosave_is_paused_to_protect_that_draft_use'},
                                                                    'target': '%1$s Тэр нооргийг хамгаалахын тулд '
                                                                              'автоматаар хадгалах түр зогссон. Үүнийг '
                                                                              'хадгалахын тулд “Файл → Сэргээх хуулбар '
                                                                              'экспортлох…”, одоогийн ажлыг хадгалахын '
                                                                              'тулд “Файл → Өөрөөр хадгалах…” (Файлын '
                                                                              'формат: PNG / JPEG) ашиглана уу.',
                                                                    'type': 'string'},
                'ui_autosave_metadata_is_missing': {'attributes': {'name': 'ui_autosave_metadata_is_missing'},
                                                    'target': 'Автоматаар хадгалсан мета өгөгдөл алга.',
                                                    'type': 'string'},
                'ui_autosave_paused_use_save': {'attributes': {'name': 'ui_autosave_paused_use_save'},
                                                'target': 'Автоматаар хадгалах түр зогссон · «Хадгалах»-ыг ашиглана уу',
                                                'type': 'string'},
                'ui_autosave_pixels_are_missing': {'attributes': {'name': 'ui_autosave_pixels_are_missing'},
                                                   'target': 'Автоматаар хадгалсан пикселийн өгөгдөл алга.',
                                                   'type': 'string'},
                'ui_autosave_pixels_could_not_be_read': {'attributes': {'name': 'ui_autosave_pixels_could_not_be_read'},
                                                         'target': 'Автоматаар хадгалсан пикселийн өгөгдлийг уншиж '
                                                                   'чадсангүй.',
                                                         'type': 'string'},
                'ui_autosave_selection_encoding_failed': {'attributes': {'name': 'ui_autosave_selection_encoding_failed'},
                                                          'target': 'Автоматаар хадгалах сонголтын кодчилол амжилтгүй.',
                                                          'type': 'string'},
                'ui_autosaving_draft': {'attributes': {'name': 'ui_autosaving_draft'},
                                        'target': 'Нооргийг автоматаар хадгалж байна…',
                                        'type': 'string'},
                'ui_background_colour': {'attributes': {'name': 'ui_background_colour'},
                                         'target': 'Дэвсгэр өнгө',
                                         'type': 'string'},
                'ui_background_edit_colour': {'attributes': {'name': 'ui_background_edit_colour'},
                                              'target': 'Дэвсгэр %1$s. Өнгө засах.',
                                              'type': 'string'},
                'ui_basic_colours': {'attributes': {'name': 'ui_basic_colours'},
                                     'target': 'Үндсэн өнгөнүүд',
                                     'type': 'string'},
                'ui_bg': {'attributes': {'name': 'ui_bg'}, 'target': 'Дэвсгэр', 'type': 'string'},
                'ui_bold': {'attributes': {'name': 'ui_bold'}, 'target': 'Бүдүүн', 'type': 'string'},
                'ui_bottom': {'attributes': {'name': 'ui_bottom'}, 'target': 'Доод', 'type': 'string'},
                'ui_brush': {'attributes': {'name': 'ui_brush'}, 'target': 'Бийр', 'type': 'string'},
                'ui_bucket_fill': {'attributes': {'name': 'ui_bucket_fill'},
                                   'target': 'Өнгөөр дүүргэх',
                                   'type': 'string'},
                'ui_cancel': {'attributes': {'name': 'ui_cancel'}, 'target': 'Цуцлах', 'type': 'string'},
                'ui_cannot_create_the_undo_cache_free_some_device': {'attributes': {'name': 'ui_cannot_create_the_undo_cache_free_some_device'},
                                                                     'target': 'Буцаах кэш үүсгэж чадсангүй. '
                                                                               'Төхөөрөмжийн хадгалах сангаас зай '
                                                                               'чөлөөлөөд дахин оролдоно уу.',
                                                                     'type': 'string'},
                'ui_canvas_bounds': {'attributes': {'name': 'ui_canvas_bounds'},
                                     'target': 'Зургийн хүрээ',
                                     'type': 'string'},
                'ui_canvas_size': {'attributes': {'name': 'ui_canvas_size'},
                                   'target': 'Зургийн талбарын хэмжээ…',
                                   'type': 'string'},
                'ui_canvas_size_30460e': {'attributes': {'name': 'ui_canvas_size_30460e'},
                                          'target': 'Зургийн хэмжээ',
                                          'type': 'string'},
                'ui_canvas_zoom': {'attributes': {'name': 'ui_canvas_zoom'},
                                   'target': 'Зургийн томруулалт',
                                   'type': 'string'},
                'ui_canvas_zoom_771f84': {'attributes': {'name': 'ui_canvas_zoom_771f84'},
                                          'target': 'Зургийн томруулалт %1$s',
                                          'type': 'string'},
                'ui_category_brush': {'attributes': {'name': 'ui_category_brush'}, 'target': 'Бийр', 'type': 'string'},
                'ui_category_insert': {'attributes': {'name': 'ui_category_insert'},
                                       'target': 'Оруулах',
                                       'type': 'string'},
                'ui_category_selection': {'attributes': {'name': 'ui_category_selection'},
                                          'target': 'Сонголт',
                                          'type': 'string'},
                'ui_centred': {'attributes': {'name': 'ui_centred'}, 'target': 'Төвд', 'type': 'string'},
                'ui_choose_a_smaller_output_copy_the_source_images': {'attributes': {'name': 'ui_choose_a_smaller_output_copy_the_source_images'},
                                                                      'target': 'Жижиг гаралтын хуулбар сонгоно уу. Эх '
                                                                                'зургууд болон тайралтын тохиргоо '
                                                                                'анхны нягтаршилтайгаа үлдэнэ.',
                                                                      'type': 'string'},
                'ui_choose_a_smaller_size': {'attributes': {'name': 'ui_choose_a_smaller_size'},
                                             'target': 'Жижиг хэмжээ сонгоно уу.',
                                             'type': 'string'},
                'ui_choose_at_least_one_image': {'attributes': {'name': 'ui_choose_at_least_one_image'},
                                                 'target': 'Дор хаяж нэг зураг сонгоно уу.',
                                                 'type': 'string'},
                'ui_choose_dimensions_no_larger_than_the_original': {'attributes': {'name': 'ui_choose_dimensions_no_larger_than_the_original'},
                                                                     'target': 'Анхны хэмжээнээс хэтрэхгүй хэмжээс '
                                                                               'сонгоно уу.',
                                                                     'type': 'string'},
                'ui_choose_location': {'attributes': {'name': 'ui_choose_location'},
                                       'target': 'Байршил сонгох',
                                       'type': 'string'},
                'ui_clear_all': {'attributes': {'name': 'ui_clear_all'}, 'target': 'Бүгдийг арилгах', 'type': 'string'},
                'ui_clear_image': {'attributes': {'name': 'ui_clear_image'},
                                   'target': 'Зургийг цэвэрлэх',
                                   'type': 'string'},
                'ui_codec_resize_memory_floor': {'attributes': {'name': 'ui_codec_resize_memory_floor'},
                                                 'target': 'Энэ формат хэмжээг өөрчлөхөөс өмнө эх зураг эсвэл эх '
                                                           'хавтангуудыг тайлах ёстой. Жижиг гаралт ч боломжит санах '
                                                           'ойгоос давж болно.',
                                                 'type': 'string'},
                'ui_collapse_colour_palette': {'attributes': {'name': 'ui_collapse_colour_palette'},
                                               'target': 'Өнгөний самбарыг хумих',
                                               'type': 'string'},
                'ui_collapse_tool_category': {'attributes': {'name': 'ui_collapse_tool_category'},
                                              'target': '%1$s: %2$s сонгосон. Хэрэгсэл ба сонголтыг хумьж',
                                              'type': 'string'},
                'ui_collapse_toolbox': {'attributes': {'name': 'ui_collapse_toolbox'},
                                        'target': 'Багажны самбарыг хумих',
                                        'type': 'string'},
                'ui_colour': {'attributes': {'name': 'ui_colour'}, 'target': 'Өнгө %1$s', 'type': 'string'},
                'ui_colour_palette_tap_for_foreground_hold_for_background': {'attributes': {'name': 'ui_colour_palette_tap_for_foreground_hold_for_background'},
                                                                             'target': 'Өнгөний самбар. Товшвол үндсэн '
                                                                                       'өнгө, удаан дарвал дэвсгэр '
                                                                                       'өнгө болно. Бусад өнгийг '
                                                                                       'харахын тулд гүйлгэнэ үү.',
                                                                             'type': 'string'},
                'ui_colour_tab23': {'attributes': {'name': 'ui_colour_tab23'}, 'target': 'Өнгө', 'type': 'string'},
                'ui_colour_tap_foreground_hold_background': {'attributes': {'name': 'ui_colour_tap_foreground_hold_background'},
                                                             'target': 'Өнгө #%1$s. Товшвол үндсэн, удаан дарвал '
                                                                       'дэвсгэр өнгө.',
                                                             'type': 'string'},
                'ui_commit_selection': {'attributes': {'name': 'ui_commit_selection'},
                                        'target': 'Сонголтыг батлах',
                                        'type': 'string'},
                'ui_copy': {'attributes': {'name': 'ui_copy'}, 'target': 'Хуулах', 'type': 'string'},
                'ui_copy_all': {'attributes': {'name': 'ui_copy_all'}, 'target': 'Бүгдийг хуулах', 'type': 'string'},
                'ui_could_not_apply_the_crop': {'attributes': {'name': 'ui_could_not_apply_the_crop'},
                                                'target': 'Тайралтыг хэрэглэж чадсангүй.',
                                                'type': 'string'},
                'ui_could_not_complete_the_edit': {'attributes': {'name': 'ui_could_not_complete_the_edit'},
                                                   'target': 'Засварыг дуусгаж чадсангүй. %1$s',
                                                   'type': 'string'},
                'ui_could_not_complete_the_operation': {'attributes': {'name': 'ui_could_not_complete_the_operation'},
                                                        'target': 'Үйлдлийг дуусгаж чадсангүй.',
                                                        'type': 'string'},
                'ui_could_not_export_the_recovery_copy': {'attributes': {'name': 'ui_could_not_export_the_recovery_copy'},
                                                          'target': 'Сэргээх хуулбарыг экспортолж чадсангүй',
                                                          'type': 'string'},
                'ui_could_not_open_image': {'attributes': {'name': 'ui_could_not_open_image'},
                                            'target': 'Зургийг нээж чадсангүй',
                                            'type': 'string'},
                'ui_could_not_place_the_image': {'attributes': {'name': 'ui_could_not_place_the_image'},
                                                 'target': 'Зургийг байрлуулж чадсангүй.',
                                                 'type': 'string'},
                'ui_could_not_prepare_the_image': {'attributes': {'name': 'ui_could_not_prepare_the_image'},
                                                   'target': 'Зургийг бэлтгэж чадсангүй.',
                                                   'type': 'string'},
                'ui_could_not_save_image': {'attributes': {'name': 'ui_could_not_save_image'},
                                            'target': 'Зургийг хадгалж чадсангүй',
                                            'type': 'string'},
                'ui_could_not_save_the_assembly': {'attributes': {'name': 'ui_could_not_save_the_assembly'},
                                                   'target': 'Эвлүүлгийг хадгалж чадсангүй: %1$s',
                                                   'type': 'string'},
                'ui_could_not_store_the_assembly': {'attributes': {'name': 'ui_could_not_store_the_assembly'},
                                                    'target': 'Эвлүүлгийг хадгалж чадсангүй.',
                                                    'type': 'string'},
                'ui_crop': {'attributes': {'name': 'ui_crop'}, 'target': '%1$s тайрах', 'type': 'string'},
                'ui_crop_image': {'attributes': {'name': 'ui_crop_image'}, 'target': 'Зураг тайрах', 'type': 'string'},
                'ui_crop_must_stay_inside_the_canvas': {'attributes': {'name': 'ui_crop_must_stay_inside_the_canvas'},
                                                        'target': 'Тайралт зургийн талбар дотор байх ёстой.',
                                                        'type': 'string'},
                'ui_crop_preview_drag_an_edge_or_corner_drag': {'attributes': {'name': 'ui_crop_preview_drag_an_edge_or_corner_drag'},
                                                                'target': 'Тайралтын урьдчилсан харагдац. Ирмэг эсвэл '
                                                                          'буланг чирж хэмжээг өөрчилнө; дотрыг нь '
                                                                          'чирж тайралтыг хөдөлгөнө.',
                                                                'type': 'string'},
                'ui_crop_preview_images': {'attributes': {'name': 'ui_crop_preview_images'},
                                           'target': {'other': 'Урьдчилсан харагдац: %1$d × %2$d px\\n%3$d зурагт '
                                                               'хэрэглэнэ. Байрлуулсан зургийг тайрахад холбогдсон '
                                                               'зургуудын байрлал мөн шинэчлэгдэнэ.'},
                                           'type': 'plurals'},
                'ui_crop_to_selection': {'attributes': {'name': 'ui_crop_to_selection'},
                                         'target': 'Сонголтоор тайрах',
                                         'type': 'string'},
                'ui_curve': {'attributes': {'name': 'ui_curve'}, 'target': 'Муруй', 'type': 'string'},
                'ui_cut': {'attributes': {'name': 'ui_cut'}, 'target': 'Таслах', 'type': 'string'},
                'ui_d_d_pixels_2f_mp_exceeds_the_current': {'attributes': {'name': 'ui_d_d_pixels_2f_mp_exceeds_the_current'},
                                                            'target': '%1$d × %2$d пиксел (%3$.2f MP) нь одоогийн '
                                                                      '%4$.2f MP аюулгүй засварлах хязгаараас давсан. '
                                                                      'AN Paint бүх зургийг санах ойд хадгалж, '
                                                                      'хувиргалт болон сонголтод нэмэлт зай нөөцөлдөг. '
                                                                      'Энэ хязгаар нь боломжит санах ойгоор тогтоно. '
                                                                      'Хэт том bitmap үүсгэхээс өмнө үйлдлийг '
                                                                      'зогсоосон. Автоматаар хэмжээ өөрчлөөгүй.',
                                                            'type': 'string'},
                'ui_d_d_px_d_pixels_2f_mp': {'attributes': {'name': 'ui_d_d_px_d_pixels_2f_mp'},
                                             'target': '%1$d × %2$d px · %3$,d пиксел (%4$.2f MP)',
                                             'type': 'string'},
                'ui_delete_selection': {'attributes': {'name': 'ui_delete_selection'},
                                        'target': 'Сонголтыг устгах',
                                        'type': 'string'},
                'ui_discard': {'attributes': {'name': 'ui_discard'}, 'target': 'Өөрчлөлтийг хаях', 'type': 'string'},
                'ui_discard_changes23': {'attributes': {'name': 'ui_discard_changes23'},
                                         'target': 'Өөрчлөлтийг хаях',
                                         'type': 'string'},
                'ui_done': {'attributes': {'name': 'ui_done'}, 'target': 'Дуусгах', 'type': 'string'},
                'ui_draft_not_saved_yet': {'attributes': {'name': 'ui_draft_not_saved_yet'},
                                           'target': 'Ноорог хараахан хадгалагдаагүй',
                                           'type': 'string'},
                'ui_draft_pending': {'attributes': {'name': 'ui_draft_pending'},
                                     'target': 'Ноорог хадгалахыг хүлээж байна',
                                     'type': 'string'},
                'ui_draft_restored': {'attributes': {'name': 'ui_draft_restored'},
                                      'target': 'Нооргийг сэргээв',
                                      'type': 'string'},
                'ui_draft_saved': {'attributes': {'name': 'ui_draft_saved'},
                                   'target': 'Нооргийг хадгаллаа',
                                   'type': 'string'},
                'ui_draw26': {'attributes': {'name': 'ui_draw26'}, 'target': '@string/ui_drawing23', 'type': 'string'},
                'ui_draw_again': {'attributes': {'name': 'ui_draw_again'}, 'target': 'Дахин зурах', 'type': 'string'},
                'ui_drawing23': {'attributes': {'name': 'ui_drawing23'}, 'target': 'Зурах', 'type': 'string'},
                'ui_drawing_canvas_pinch_and_move_two_fingers_to': {'attributes': {'name': 'ui_drawing_canvas_pinch_and_move_two_fingers_to'},
                                                                    'target': 'Зургийн талбар. Хоёр хуруугаар чимхэж, '
                                                                              'хөдөлгөж томруулан шилжүүлнэ. '
                                                                              '«Шилжүүлэх» горимд нэг хуруугаар ч '
                                                                              'шилжүүлж болно.',
                                                                    'type': 'string'},
                'ui_drawing_settings': {'attributes': {'name': 'ui_drawing_settings'},
                                        'target': 'Зурах тохиргоо…',
                                        'type': 'string'},
                'ui_drawing_settings_d900c6': {'attributes': {'name': 'ui_drawing_settings_d900c6'},
                                               'target': 'Зурах тохиргоо',
                                               'type': 'string'},
                'ui_edit_background': {'attributes': {'name': 'ui_edit_background'},
                                       'target': 'Дэвсгэрийг засах…',
                                       'type': 'string'},
                'ui_edit_canvas33': {'attributes': {'name': 'ui_edit_canvas33'},
                                     'target': 'Зургийн талбар',
                                     'type': 'string'},
                'ui_edit_colour26': {'attributes': {'name': 'ui_edit_colour26'},
                                     'target': 'Өнгө засах',
                                     'type': 'string'},
                'ui_edit_foreground': {'attributes': {'name': 'ui_edit_foreground'},
                                       'target': 'Үндсэн өнгийг засах…',
                                       'type': 'string'},
                'ui_edit_transform33': {'attributes': {'name': 'ui_edit_transform33'},
                                        'target': 'Тольдох / Эргүүлэх',
                                        'type': 'string'},
                'ui_ellipse': {'attributes': {'name': 'ui_ellipse'}, 'target': 'Зууван', 'type': 'string'},
                'ui_enter_a_number_from_to': {'attributes': {'name': 'ui_enter_a_number_from_to'},
                                              'target': '%1$s–%2$s хооронд тоо оруулна уу.',
                                              'type': 'string'},
                'ui_enter_a_positive_size': {'attributes': {'name': 'ui_enter_a_positive_size'},
                                             'target': '0-ээс их хэмжээ оруулна уу.',
                                             'type': 'string'},
                'ui_enter_a_trim_amount_for_every_edge': {'attributes': {'name': 'ui_enter_a_trim_amount_for_every_edge'},
                                                          'target': 'Ирмэг бүрийн тайрах хэмжээг оруулна уу.',
                                                          'type': 'string'},
                'ui_enter_a_whole_number_from_to': {'attributes': {'name': 'ui_enter_a_whole_number_from_to'},
                                                    'target': '%1$s–%2$s хооронд бүхэл тоо оруулна уу.',
                                                    'type': 'string'},
                'ui_enter_all_four_trim_amounts': {'attributes': {'name': 'ui_enter_all_four_trim_amounts'},
                                                   'target': 'Дөрвөн ирмэгийн бүх тайрах хэмжээг оруулна уу.',
                                                   'type': 'string'},
                'ui_enter_positive_canvas_dimensions_within_android_s_coordinate': {'attributes': {'name': 'ui_enter_positive_canvas_dimensions_within_android_s_coordinate'},
                                                                                    'target': 'Android-ын координатын '
                                                                                              'хязгаарт багтах, 0-ээс '
                                                                                              'их зургийн хэмжээс '
                                                                                              'оруулна уу.',
                                                                                    'type': 'string'},
                'ui_enter_positive_dimensions': {'attributes': {'name': 'ui_enter_positive_dimensions'},
                                                 'target': '0-ээс их хэмжээс оруулна уу.',
                                                 'type': 'string'},
                'ui_enter_positive_dimensions_no_larger_than_the_original': {'attributes': {'name': 'ui_enter_positive_dimensions_no_larger_than_the_original'},
                                                                             'target': 'Анхны хэмжээнээс хэтрэхгүй, '
                                                                                       '0-ээс их хэмжээс оруулна уу.',
                                                                             'type': 'string'},
                'ui_enter_positive_dimensions_that_resolve_to_at_least': {'attributes': {'name': 'ui_enter_positive_dimensions_that_resolve_to_at_least'},
                                                                          'target': 'Дор хаяж 1 пиксел болох 0-ээс их '
                                                                                    'хэмжээс оруулна уу.',
                                                                          'type': 'string'},
                'ui_enter_positive_image_dimensions': {'attributes': {'name': 'ui_enter_positive_image_dimensions'},
                                                       'target': '0-ээс их зургийн хэмжээс оруулна уу.',
                                                       'type': 'string'},
                'ui_enter_valid_dimensions': {'attributes': {'name': 'ui_enter_valid_dimensions'},
                                              'target': 'Зөв хэмжээс оруулна уу.',
                                              'type': 'string'},
                'ui_eraser': {'attributes': {'name': 'ui_eraser'}, 'target': 'Баллуур', 'type': 'string'},
                'ui_expand_colour_palette': {'attributes': {'name': 'ui_expand_colour_palette'},
                                             'target': 'Өнгөний самбарыг дэлгэх',
                                             'type': 'string'},
                'ui_expand_tool_category': {'attributes': {'name': 'ui_expand_tool_category'},
                                            'target': '%1$s: %2$s сонгосон. Хэрэгсэл ба сонголтыг дэлгэх',
                                            'type': 'string'},
                'ui_expand_toolbox': {'attributes': {'name': 'ui_expand_toolbox'},
                                      'target': 'Багажны самбарыг дэлгэх',
                                      'type': 'string'},
                'ui_export_as23': {'attributes': {'name': 'ui_export_as23'}, 'target': 'Экспортлох…', 'type': 'string'},
                'ui_export_did_not_save23': {'attributes': {'name': 'ui_export_did_not_save23'},
                                             'target': 'Экспорт үүссэн. Үргэлжлүүлэхээс өмнө одоогийн зургийг '
                                                       '«Хадгалах» эсвэл «Өөрөөр хадгалах»-аар хадгална уу.',
                                             'type': 'string'},
                'ui_export_explanation23': {'attributes': {'name': 'ui_export_explanation23'},
                                            'target': 'Дүрс, Base64 текст эсвэл ASCII арт экспортлоно. Экспортлох нь '
                                                      'одоогийн зураг болон түүний «Хадгалах» байршлыг өөрчлөхгүй.',
                                            'type': 'string'},
                'ui_export_recovery_copy': {'attributes': {'name': 'ui_export_recovery_copy'},
                                            'target': 'Сэргээх хуулбар экспортлох…',
                                            'type': 'string'},
                'ui_export_recovery_copy_144b8a': {'attributes': {'name': 'ui_export_recovery_copy_144b8a'},
                                                   'target': 'Сэргээх хуулбар экспортлох',
                                                   'type': 'string'},
                'ui_eyedropper': {'attributes': {'name': 'ui_eyedropper'}, 'target': 'Өнгө авах', 'type': 'string'},
                'ui_fg': {'attributes': {'name': 'ui_fg'}, 'target': 'Үндсэн', 'type': 'string'},
                'ui_fit': {'attributes': {'name': 'ui_fit'}, 'target': 'Багтаах', 'type': 'string'},
                'ui_fit_entire_canvas_in_view': {'attributes': {'name': 'ui_fit_entire_canvas_in_view'},
                                                 'target': 'Зургийн талбарыг бүхэлд нь багтаах',
                                                 'type': 'string'},
                'ui_fit_image': {'attributes': {'name': 'ui_fit_image'}, 'target': 'Зургийг багтаах', 'type': 'string'},
                'ui_fit_selection34': {'attributes': {'name': 'ui_fit_selection34'},
                                       'target': 'Зургийг талбарт багтаах',
                                       'type': 'string'},
                'ui_flip_horizontal': {'attributes': {'name': 'ui_flip_horizontal'},
                                       'target': 'Хэвтээгээр тольдох',
                                       'type': 'string'},
                'ui_flip_vertical': {'attributes': {'name': 'ui_flip_vertical'},
                                     'target': 'Босоогоор тольдох',
                                     'type': 'string'},
                'ui_font': {'attributes': {'name': 'ui_font'}, 'target': 'Фонт', 'type': 'string'},
                'ui_font_family': {'attributes': {'name': 'ui_font_family'},
                                   'target': 'Фонтын бүлэг',
                                   'type': 'string'},
                'ui_foreground_background_colour_palette': {'attributes': {'name': 'ui_foreground_background_colour_palette'},
                                                            'target': 'Үндсэн %1$s, дэвсгэр %2$s. %3$s өнгөний самбар.',
                                                            'type': 'string'},
                'ui_foreground_colour': {'attributes': {'name': 'ui_foreground_colour'},
                                         'target': 'Үндсэн өнгө',
                                         'type': 'string'},
                'ui_foreground_edit_colour': {'attributes': {'name': 'ui_foreground_edit_colour'},
                                              'target': 'Үндсэн %1$s. Өнгө засах.',
                                              'type': 'string'},
                'ui_free_form_select': {'attributes': {'name': 'ui_free_form_select'},
                                        'target': 'Чөлөөт хэлбэрээр сонгох',
                                        'type': 'string'},
                'ui_from_device34': {'attributes': {'name': 'ui_from_device34'},
                                     'target': 'Төхөөрөмжөөс…',
                                     'type': 'string'},
                'ui_full_text_copied': {'attributes': {'name': 'ui_full_text_copied'},
                                        'target': 'Бүх текстийг хууллаа',
                                        'type': 'string'},
                'ui_heart': {'attributes': {'name': 'ui_heart'}, 'target': 'Зүрх', 'type': 'string'},
                'ui_height': {'attributes': {'name': 'ui_height'}, 'target': 'Өндөр (%1$s)', 'type': 'string'},
                'ui_height_in': {'attributes': {'name': 'ui_height_in'}, 'target': 'Өндөр (%1$s)', 'type': 'string'},
                'ui_heights': {'attributes': {'name': 'ui_heights'}, 'target': 'Өндрүүд', 'type': 'string'},
                'ui_hex_rrggbb': {'attributes': {'name': 'ui_hex_rrggbb'}, 'target': 'Hex #RRGGBB', 'type': 'string'},
                'ui_hide_editor_controls': {'attributes': {'name': 'ui_hide_editor_controls'},
                                            'target': 'Засварлагчийн удирдлагыг нуух',
                                            'type': 'string'},
                'ui_higher_quality_usually_makes_a_larger_file_lossless': {'attributes': {'name': 'ui_higher_quality_usually_makes_a_larger_file_lossless'},
                                                                           'target': 'Өндөр чанар нь ихэвчлэн том файл '
                                                                                     'үүсгэнэ. Алдагдалгүй горим бүх '
                                                                                     'өнгөний утгыг хадгална.',
                                                                           'type': 'string'},
                'ui_history_unavailable34': {'attributes': {'name': 'ui_history_unavailable34'},
                                             'target': 'Зургийн талбарыг сэргээсэн боловч буцаах түүхийг уншиж '
                                                       'чадсангүй. Анхны нооргийг сэргээх хуулбар болгон хадгалсан.',
                                             'type': 'string'},
                'ui_image': {'attributes': {'name': 'ui_image'}, 'target': 'Зураг', 'type': 'string'},
                'ui_image_assembly': {'attributes': {'name': 'ui_image_assembly'},
                                      'target': 'Зураг эвлүүлэх…',
                                      'type': 'string'},
                'ui_image_shown_in_crop_preview': {'attributes': {'name': 'ui_image_shown_in_crop_preview'},
                                                   'target': 'Тайралтын урьдчилсан харагдацад үзүүлж буй зураг',
                                                   'type': 'string'},
                'ui_insert': {'attributes': {'name': 'ui_insert'}, 'target': 'Оруулах', 'type': 'string'},
                'ui_insert_image_into_canvas': {'attributes': {'name': 'ui_insert_image_into_canvas'},
                                                'target': 'Зургийг зургийн талбарт оруулах…',
                                                'type': 'string'},
                'ui_invalid_autosave_metadata': {'attributes': {'name': 'ui_invalid_autosave_metadata'},
                                                 'target': 'Автоматаар хадгалсан мета өгөгдөл буруу.',
                                                 'type': 'string'},
                'ui_invalid_colour': {'attributes': {'name': 'ui_invalid_colour'},
                                      'target': 'Буруу өнгө',
                                      'type': 'string'},
                'ui_invalid_selection_outline': {'attributes': {'name': 'ui_invalid_selection_outline'},
                                                 'target': 'Сонголтын хүрээ буруу.',
                                                 'type': 'string'},
                'ui_invert_colours': {'attributes': {'name': 'ui_invert_colours'},
                                      'target': 'Өнгийг урвуулах',
                                      'type': 'string'},
                'ui_italic': {'attributes': {'name': 'ui_italic'}, 'target': 'Налуу', 'type': 'string'},
                'ui_keep_editing23': {'attributes': {'name': 'ui_keep_editing23'},
                                      'target': 'Үргэлжлүүлэн засах',
                                      'type': 'string'},
                'ui_keeps_pixels_at_the_top_left_smaller_canvas': {'attributes': {'name': 'ui_keeps_pixels_at_the_top_left_smaller_canvas'},
                                                                   'target': 'Зүүн дээд талын пикселүүдийг хадгална. '
                                                                             'Зургийн талбарыг жижигрүүлэхэд '
                                                                             'баруун/доод ирмэгээс гадуурх пикселүүд '
                                                                             'хаягдана; «Буцаах» нь тэдгээрийг '
                                                                             'сэргээнэ.',
                                                                   'type': 'string'},
                'ui_languages23': {'attributes': {'name': 'ui_languages23'}, 'target': 'Хэл', 'type': 'string'},
                'ui_left': {'attributes': {'name': 'ui_left'}, 'target': 'Зүүн', 'type': 'string'},
                'ui_left_aligned': {'attributes': {'name': 'ui_left_aligned'},
                                    'target': 'Зүүн зэрэгцүүлсэн',
                                    'type': 'string'},
                'ui_left_arrow_collapse': {'attributes': {'name': 'ui_left_arrow_collapse'},
                                           'target': 'Зүүн сум: хумих',
                                           'type': 'string'},
                'ui_line': {'attributes': {'name': 'ui_line'}, 'target': 'Шулуун', 'type': 'string'},
                'ui_line_spacing': {'attributes': {'formatted': 'false', 'name': 'ui_line_spacing'},
                                    'target': 'Мөр хоорондын зай (%)',
                                    'type': 'string'},
                'ui_load_image': {'attributes': {'name': 'ui_load_image'}, 'target': 'Зураг нээх', 'type': 'string'},
                'ui_lock_aspect_ratio': {'attributes': {'name': 'ui_lock_aspect_ratio'},
                                         'target': 'Харьцааг түгжих',
                                         'type': 'string'},
                'ui_lock_proportions': {'attributes': {'name': 'ui_lock_proportions'},
                                        'target': 'Харьцааг түгжих',
                                        'type': 'string'},
                'ui_lossless_format': {'attributes': {'name': 'ui_lossless_format'},
                                       'target': '%1$s алдагдалгүй',
                                       'type': 'string'},
                'ui_magnification': {'attributes': {'formatted': 'false', 'name': 'ui_magnification'},
                                     'target': 'Томруулалт (%)',
                                     'type': 'string'},
                'ui_main23': {'attributes': {'name': 'ui_main23'}, 'target': 'Үндсэн', 'type': 'string'},
                'ui_menu': {'attributes': {'name': 'ui_menu'}, 'target': 'Цэс', 'type': 'string'},
                'ui_menu_colours': {'attributes': {'name': 'ui_menu_colours'}, 'target': 'Өнгө', 'type': 'string'},
                'ui_menu_edit': {'attributes': {'name': 'ui_menu_edit'}, 'target': 'Засах', 'type': 'string'},
                'ui_menu_file': {'attributes': {'name': 'ui_menu_file'}, 'target': 'Файл', 'type': 'string'},
                'ui_menu_help': {'attributes': {'name': 'ui_menu_help'}, 'target': 'Тусламж', 'type': 'string'},
                'ui_menu_image': {'attributes': {'name': 'ui_menu_image'}, 'target': 'Зураг', 'type': 'string'},
                'ui_menu_view': {'attributes': {'name': 'ui_menu_view'}, 'target': 'Харах', 'type': 'string'},
                'ui_navigate': {'attributes': {'name': 'ui_navigate'}, 'target': 'Шилжүүлэх', 'type': 'string'},
                'ui_new': {'attributes': {'name': 'ui_new'}, 'target': 'Шинэ', 'type': 'string'},
                'ui_new_colour': {'attributes': {'name': 'ui_new_colour'}, 'target': 'Шинэ өнгө', 'type': 'string'},
                'ui_new_image': {'attributes': {'name': 'ui_new_image'}, 'target': 'Шинэ зураг', 'type': 'string'},
                'ui_no_readable_image_data': {'attributes': {'name': 'ui_no_readable_image_data'},
                                              'target': 'Уншигдах зургийн өгөгдөл алга.',
                                              'type': 'string'},
                'ui_no_resize_fits_decoder_memory': {'attributes': {'name': 'ui_no_resize_fits_decoder_memory'},
                                                     'target': 'Гаралтын хэмжээг хамгийн бага болгосон ч энэ зургийг '
                                                               'одоогийн санах ойн хязгаарт багтаан засварлахаар '
                                                               'ачаалах боломжгүй. Цуцлаад илүү жижиг эх зураг '
                                                               'ашиглана уу.',
                                                     'type': 'string'},
                'ui_none': {'attributes': {'name': 'ui_none'}, 'target': 'Байхгүй', 'type': 'string'},
                'ui_not_enough_memory_for_this_operation_the_assembly': {'attributes': {'name': 'ui_not_enough_memory_for_this_operation_the_assembly'},
                                                                         'target': 'Энэ үйлдэлд санах ой хүрэлцэхгүй. '
                                                                                   'Эвлүүлгийн эх файлууд '
                                                                                   'хадгалагдана.',
                                                                         'type': 'string'},
                'ui_not_enough_memory_to_finish_opening_this_image': {'attributes': {'name': 'ui_not_enough_memory_to_finish_opening_this_image'},
                                                                      'target': 'Энэ зургийг нээж дуусгахад санах ой '
                                                                                'хүрэлцэхгүй',
                                                                      'type': 'string'},
                'ui_not_enough_memory_to_inspect_this_image': {'attributes': {'name': 'ui_not_enough_memory_to_inspect_this_image'},
                                                               'target': 'Энэ зургийг шалгахад санах ой хүрэлцэхгүй',
                                                               'type': 'string'},
                'ui_not_enough_memory_to_save_in_this_format': {'attributes': {'name': 'ui_not_enough_memory_to_save_in_this_format'},
                                                                'target': 'Энэ форматаар хадгалахад санах ой '
                                                                          'хүрэлцэхгүй. PNG ашиглаж үзнэ үү',
                                                                'type': 'string'},
                'ui_numeric_slider_value': {'attributes': {'name': 'ui_numeric_slider_value'},
                                            'target': '%1$s: %2$d',
                                            'type': 'string'},
                'ui_ok': {'attributes': {'name': 'ui_ok'}, 'target': 'ОК', 'type': 'string'},
                'ui_original_size34': {'attributes': {'name': 'ui_original_size34'},
                                       'target': 'Анхны хэмжээ',
                                       'type': 'string'},
                'ui_other_images34': {'attributes': {'name': 'ui_other_images34'},
                                      'target': 'Бусад зураг',
                                      'type': 'string'},
                'ui_outline': {'attributes': {'name': 'ui_outline'}, 'target': 'Хүрээ', 'type': 'string'},
                'ui_palette': {'attributes': {'name': 'ui_palette'}, 'target': 'Өнгөний самбар', 'type': 'string'},
                'ui_paste': {'attributes': {'name': 'ui_paste'}, 'target': 'Буулгах', 'type': 'string'},
                'ui_paste_hint34': {'attributes': {'name': 'ui_paste_hint34'},
                                    'target': 'Талбайг хуулж эсвэл Зурах → Оруулах → Бусад зураг командыг ашиглана уу.',
                                    'type': 'string'},
                'ui_pencil': {'attributes': {'name': 'ui_pencil'}, 'target': 'Харандаа', 'type': 'string'},
                'ui_percent': {'attributes': {'name': 'ui_percent'}, 'target': 'Хувь', 'type': 'string'},
                'ui_percent_fd8671': {'attributes': {'name': 'ui_percent_fd8671'}, 'target': 'хувь', 'type': 'string'},
                'ui_pinch_and_pan_mode': {'attributes': {'name': 'ui_pinch_and_pan_mode'},
                                          'target': 'Чимхэж томруулах ба шилжүүлэх горим',
                                          'type': 'string'},
                'ui_pixels': {'attributes': {'name': 'ui_pixels'}, 'target': 'Пиксел', 'type': 'string'},
                'ui_pixels_6ec9c2': {'attributes': {'name': 'ui_pixels_6ec9c2'}, 'target': 'пиксел', 'type': 'string'},
                'ui_place_text': {'attributes': {'name': 'ui_place_text'},
                                  'target': 'Текст байрлуулах',
                                  'type': 'string'},
                'ui_please_try_again': {'attributes': {'name': 'ui_please_try_again'},
                                        'target': 'Дахин оролдоно уу.',
                                        'type': 'string'},
                'ui_please_wait_for_the_current_operation': {'attributes': {'name': 'ui_please_wait_for_the_current_operation'},
                                                             'target': 'Одоогийн үйлдэл дуусахыг хүлээнэ үү.',
                                                             'type': 'string'},
                'ui_png_encoding_failed': {'attributes': {'name': 'ui_png_encoding_failed'},
                                           'target': 'PNG кодчилол амжилтгүй.',
                                           'type': 'string'},
                'ui_polygon': {'attributes': {'name': 'ui_polygon'}, 'target': 'Олон өнцөгт', 'type': 'string'},
                'ui_preview': {'attributes': {'name': 'ui_preview'}, 'target': 'Урьдчилан харах', 'type': 'string'},
                'ui_previous_draft_kept_for_recovery': {'attributes': {'name': 'ui_previous_draft_kept_for_recovery'},
                                                        'target': 'Өмнөх нооргийг сэргээх зорилгоор хадгаллаа',
                                                        'type': 'string'},
                'ui_px': {'attributes': {'name': 'ui_px'},
                          'target': '%1$s · %2$s\\n%3$s × %4$s px · %5$s',
                          'type': 'string'},
                'ui_px_724eb3': {'attributes': {'name': 'ui_px_724eb3'}, 'target': '%1$s × %2$s px', 'type': 'string'},
                'ui_quality': {'attributes': {'formatted': 'false', 'name': 'ui_quality'},
                               'target': 'Чанар (%)',
                               'type': 'string'},
                'ui_ready': {'attributes': {'name': 'ui_ready'}, 'target': 'Бэлэн', 'type': 'string'},
                'ui_recovered_image': {'attributes': {'name': 'ui_recovered_image'},
                                       'target': 'Сэргээсэн зураг',
                                       'type': 'string'},
                'ui_recovery_copy_exported_extract_canvas_png_from_the': {'attributes': {'name': 'ui_recovery_copy_exported_extract_canvas_png_from_the'},
                                                                          'target': 'Сэргээх хуулбарыг экспортоллоо. '
                                                                                    'ZIP-ээс canvas.png файлыг гаргаж '
                                                                                    'аваад Файл > Зураг нээх командаар '
                                                                                    'нээнэ үү. ZIP дотор мөн ноорогийн '
                                                                                    'тохиргоо болон хөвөгч сонголт '
                                                                                    'байвал хадгалагдсан.',
                                                                          'type': 'string'},
                'ui_rectangle': {'attributes': {'name': 'ui_rectangle'}, 'target': 'Тэгш өнцөгт', 'type': 'string'},
                'ui_rectangle_select': {'attributes': {'name': 'ui_rectangle_select'},
                                        'target': 'Тэгш өнцөгтөөр сонгох',
                                        'type': 'string'},
                'ui_redo': {'attributes': {'name': 'ui_redo'}, 'target': 'Дахин хийх', 'type': 'string'},
                'ui_remove': {'attributes': {'name': 'ui_remove'}, 'target': 'Устгах', 'type': 'string'},
                'ui_reset_bw23': {'attributes': {'name': 'ui_reset_bw23'},
                                  'target': 'Хар, цагаан болгох',
                                  'type': 'string'},
                'ui_reset_crop': {'attributes': {'name': 'ui_reset_crop'},
                                  'target': 'Тайралтыг сэргээх',
                                  'type': 'string'},
                'ui_reset_to_black_white': {'attributes': {'name': 'ui_reset_to_black_white'},
                                            'target': 'Хар / цагаан болгох',
                                            'type': 'string'},
                'ui_resize_and_load': {'attributes': {'name': 'ui_resize_and_load'},
                                       'target': 'Хэмжээг өөрчилж нээх',
                                       'type': 'string'},
                'ui_resize_image': {'attributes': {'name': 'ui_resize_image'},
                                    'target': 'Зургийн хэмжээг өөрчлөх…',
                                    'type': 'string'},
                'ui_resize_image_ab28be': {'attributes': {'name': 'ui_resize_image_ab28be'},
                                           'target': 'Зургийн хэмжээг өөрчлөх',
                                           'type': 'string'},
                'ui_resize_large_image': {'attributes': {'name': 'ui_resize_large_image'},
                                          'target': 'Том зургийн хэмжээг өөрчлөх үү?',
                                          'type': 'string'},
                'ui_resize_the_copy': {'attributes': {'name': 'ui_resize_the_copy'},
                                       'target': 'Хуулбарын хэмжээг өөрчлөх',
                                       'type': 'string'},
                'ui_right': {'attributes': {'name': 'ui_right'}, 'target': 'Баруун', 'type': 'string'},
                'ui_right_aligned': {'attributes': {'name': 'ui_right_aligned'},
                                     'target': 'Баруун зэрэгцүүлсэн',
                                     'type': 'string'},
                'ui_rotate': {'attributes': {'name': 'ui_rotate'}, 'target': 'Эргүүлэх', 'type': 'string'},
                'ui_rotate_180': {'attributes': {'name': 'ui_rotate_180'}, 'target': '180° эргүүлэх', 'type': 'string'},
                'ui_rotate_90_clockwise': {'attributes': {'name': 'ui_rotate_90_clockwise'},
                                           'target': 'Цагийн зүүний дагуу 90° эргүүлэх',
                                           'type': 'string'},
                'ui_rounded_rectangle': {'attributes': {'name': 'ui_rounded_rectangle'},
                                         'target': 'Дугуй булант тэгш өнцөгт',
                                         'type': 'string'},
                'ui_sampled_resize_memory_explanation': {'attributes': {'name': 'ui_sampled_resize_memory_explanation'},
                                                         'target': 'Тооцоонд одоогийн зургийн талбар, санах ойд '
                                                                   'хуулсан зураг, дээжлэн тайлах болон засварлах '
                                                                   'буфер орно. Бодит хэрэглээ өөр байж болно. Жижиг '
                                                                   'хуулбар нь нарийвчлал алддаг. Эх файл '
                                                                   'өөрчлөгдөхгүй.',
                                                         'type': 'string'},
                'ui_save': {'attributes': {'name': 'ui_save'}, 'target': 'Хадгалах', 'type': 'string'},
                'ui_save_a5d0d9': {'attributes': {'name': 'ui_save_a5d0d9'}, 'target': 'Хадгалах', 'type': 'string'},
                'ui_save_and_share': {'attributes': {'name': 'ui_save_and_share'},
                                      'target': 'Хадгалж хуваалцах…',
                                      'type': 'string'},
                'ui_save_and_share_41edb4': {'attributes': {'name': 'ui_save_and_share_41edb4'},
                                             'target': 'Хадгалж хуваалцах',
                                             'type': 'string'},
                'ui_save_as': {'attributes': {'name': 'ui_save_as'},
                               'target': '%1$s болгон хадгалах',
                               'type': 'string'},
                'ui_save_as_jpeg': {'attributes': {'name': 'ui_save_as_jpeg'},
                                    'target': 'JPEG болгон хадгалах…',
                                    'type': 'string'},
                'ui_save_as_jpeg_xl': {'attributes': {'name': 'ui_save_as_jpeg_xl'},
                                       'target': 'JPEG XL болгон хадгалах…',
                                       'type': 'string'},
                'ui_save_as_png': {'attributes': {'name': 'ui_save_as_png'},
                                   'target': 'PNG болгон хадгалах…',
                                   'type': 'string'},
                'ui_save_explanation23': {'attributes': {'name': 'ui_save_explanation23'},
                                          'target': 'Зургийн формат болон шахалтын тохиргоог сонгоно. «Хадгалах» нь '
                                                    'энэ файлын нэр, байршил, формат, тохиргоог дахин ашиглана.',
                                          'type': 'string'},
                'ui_save_png': {'attributes': {'name': 'ui_save_png'}, 'target': 'PNG хадгалах', 'type': 'string'},
                'ui_save_your_changes': {'attributes': {'name': 'ui_save_your_changes'},
                                         'target': 'Өөрчлөлтөө хадгалах уу?',
                                         'type': 'string'},
                'ui_saved': {'attributes': {'name': 'ui_saved'}, 'target': '%1$s хадгаллаа', 'type': 'string'},
                'ui_scales_the_image_unlock_the_ratio_to_stretch': {'attributes': {'name': 'ui_scales_the_image_unlock_the_ratio_to_stretch'},
                                                                    'target': 'Зургийг хэмжээгээр нь өөрчилнө. Өргөн '
                                                                              'ба өндрийг тусад нь сунгахын тулд '
                                                                              'харьцааны түгжээг тайлна.',
                                                                    'type': 'string'},
                'ui_select_all': {'attributes': {'name': 'ui_select_all'},
                                  'target': 'Бүгдийг сонгох',
                                  'type': 'string'},
                'ui_select_an_area': {'attributes': {'name': 'ui_select_an_area'},
                                      'target': 'Талбай сонгох',
                                      'type': 'string'},
                'ui_select_an_area_first': {'attributes': {'name': 'ui_select_an_area_first'},
                                            'target': 'Эхлээд талбай сонгоно уу.',
                                            'type': 'string'},
                'ui_selected_colour23': {'attributes': {'name': 'ui_selected_colour23'},
                                         'target': 'Сонгосон өнгө',
                                         'type': 'string'},
                'ui_selection_dimensions_are_too_large': {'attributes': {'name': 'ui_selection_dimensions_are_too_large'},
                                                          'target': 'Сонголтын хэмжээ хэт том байна.',
                                                          'type': 'string'},
                'ui_share_explanation34': {'attributes': {'name': 'ui_share_explanation34'},
                                           'target': 'Сонгосон байршилдаа хуулбар хадгалаад, дараа нь хуваалцах апп '
                                                     'сонгоно. Одоогийн «Хадгалах» байршил өөрчлөгдөхгүй.',
                                           'type': 'string'},
                'ui_share_saved_image': {'attributes': {'name': 'ui_share_saved_image'},
                                         'target': 'Хадгалсан зургийг хуваалцах',
                                         'type': 'string'},
                'ui_show_all': {'attributes': {'name': 'ui_show_all'}, 'target': 'Бүгдийг харуулах', 'type': 'string'},
                'ui_show_controls': {'attributes': {'name': 'ui_show_controls'},
                                     'target': 'Удирдлагыг харуулах',
                                     'type': 'string'},
                'ui_show_editor_controls': {'attributes': {'name': 'ui_show_editor_controls'},
                                            'target': 'Засварлагчийн удирдлагыг харуулах',
                                            'type': 'string'},
                'ui_show_magnified_drawing_preview': {'attributes': {'name': 'ui_show_magnified_drawing_preview'},
                                                      'target': 'Томруулсан зургийн урьдчилсан харагдацыг үзүүлэх',
                                                      'type': 'string'},
                'ui_size_pixels': {'attributes': {'name': 'ui_size_pixels'},
                                   'target': 'Хэмжээ (пиксел)',
                                   'type': 'string'},
                'ui_size_px': {'attributes': {'name': 'ui_size_px'}, 'target': 'Хэмжээ (px)', 'type': 'string'},
                'ui_solid_fill': {'attributes': {'name': 'ui_solid_fill'}, 'target': 'Дүүргэлт', 'type': 'string'},
                'ui_star': {'attributes': {'name': 'ui_star'}, 'target': 'Од', 'type': 'string'},
                'ui_swap23': {'attributes': {'name': 'ui_swap23'}, 'target': 'Өнгө солих', 'type': 'string'},
                'ui_swap_foreground_background': {'attributes': {'name': 'ui_swap_foreground_background'},
                                                  'target': 'Үндсэн / дэвсгэр өнгийг солих',
                                                  'type': 'string'},
                'ui_tap_an_image_first': {'attributes': {'name': 'ui_tap_an_image_first'},
                                          'target': 'Эхлээд зураг товшино уу.',
                                          'type': 'string'},
                'ui_tap_canvas_to_type': {'attributes': {'name': 'ui_tap_canvas_to_type'},
                                          'target': 'Текст оруулахын тулд\\nзургийн талбарыг товшино',
                                          'type': 'string'},
                'ui_tap_to_type_a_number': {'attributes': {'name': 'ui_tap_to_type_a_number'},
                                            'target': '%1$s: %2$s. Тоо оруулахын тулд товшино.',
                                            'type': 'string'},
                'ui_text': {'attributes': {'name': 'ui_text'}, 'target': 'Текст', 'type': 'string'},
                'ui_text_alignment': {'attributes': {'name': 'ui_text_alignment'},
                                      'target': 'Текст зэрэгцүүлэх',
                                      'type': 'string'},
                'ui_text_direction23': {'attributes': {'name': 'ui_text_direction23'},
                                        'target': 'Текстийн чиглэл',
                                        'type': 'string'},
                'ui_the_crop_must_contain_at_least_one_pixel': {'attributes': {'name': 'ui_the_crop_must_contain_at_least_one_pixel'},
                                                                'target': 'Тайралт дор хаяж нэг пиксел агуулсан байх '
                                                                          'ёстой.',
                                                                'type': 'string'},
                'ui_the_crop_must_stay_inside_the_image': {'attributes': {'name': 'ui_the_crop_must_stay_inside_the_image'},
                                                           'target': 'Тайралт зураг дотор байх ёстой.',
                                                           'type': 'string'},
                'ui_the_decoder_and_editing_buffers_need_about_the': {'attributes': {'name': 'ui_the_decoder_and_editing_buffers_need_about_the'},
                                                                      'target': 'Декодер болон засварлах буферт '
                                                                                'ойролцоогоор %1$s хэрэгтэй; одоогийн '
                                                                                'аюулгүй засварлах хязгаар %2$s. Жижиг '
                                                                                'хуулбар сонгоно уу.',
                                                                      'type': 'string'},
                'ui_the_draft_is_saving_try_again_shortly': {'attributes': {'name': 'ui_the_draft_is_saving_try_again_shortly'},
                                                             'target': 'Нооргийг хадгалж байна. Түр хүлээгээд дахин '
                                                                       'оролдоно уу.',
                                                             'type': 'string'},
                'ui_the_encoder_did_not_finish': {'attributes': {'name': 'ui_the_encoder_did_not_finish'},
                                                  'target': 'Кодлогч ажиллагаагаа дуусгасангүй.',
                                                  'type': 'string'},
                'ui_the_full_image_and_working_buffers_exceed_the': {'attributes': {'name': 'ui_the_full_image_and_working_buffers_exceed_the'},
                                                                     'target': 'Бүтэн зураг болон ажлын буферууд '
                                                                               'одоогийн аюулгүй хязгаараас давсан, '
                                                                               'эсвэл Android шаардлагатай санах ойг '
                                                                               'хуваарилж чадсангүй. Засахын тулд '
                                                                               'хуулбарын хэмжээг багасгана уу. Таны '
                                                                               'эх файл өөрчлөгдөхгүй.',
                                                                     'type': 'string'},
                'ui_the_image_was_saved_but_android_could_not': {'attributes': {'name': 'ui_the_image_was_saved_but_android_could_not'},
                                                                 'target': 'Зургийг хадгалсан боловч Android хуваалцах '
                                                                           'цонхыг нээж чадсангүй: %1$s',
                                                                 'type': 'string'},
                'ui_the_picker_returned_no_file_please_choose_the': {'attributes': {'name': 'ui_the_picker_returned_no_file_please_choose_the'},
                                                                     'target': 'Файл сонгогч файл буцаасангүй. Файлыг '
                                                                               'дахин сонгоно уу.',
                                                                     'type': 'string'},
                'ui_the_picker_returned_no_files': {'attributes': {'name': 'ui_the_picker_returned_no_files'},
                                                    'target': 'Файл сонгогч ямар ч файл буцаасангүй.',
                                                    'type': 'string'},
                'ui_the_previous_draft_could_not_be_moved_to': {'attributes': {'name': 'ui_the_previous_draft_could_not_be_moved_to'},
                                                                'target': 'Өмнөх нооргийг сэргээх хуулбар руу шилжүүлж '
                                                                          'чадсангүй.',
                                                                'type': 'string'},
                'ui_the_previous_draft_could_not_be_preserved_separately': {'attributes': {'name': 'ui_the_previous_draft_could_not_be_preserved_separately'},
                                                                            'target': 'Өмнөх нооргийг тусад нь хадгалж '
                                                                                      'чадсангүй.',
                                                                            'type': 'string'},
                'ui_the_previous_draft_could_not_be_restored': {'attributes': {'name': 'ui_the_previous_draft_could_not_be_restored'},
                                                                'target': 'Өмнөх нооргийг сэргээж чадсангүй.',
                                                                'type': 'string'},
                'ui_the_previous_draft_needs_more_memory_to_reopen': {'attributes': {'name': 'ui_the_previous_draft_needs_more_memory_to_reopen'},
                                                                      'target': 'Өмнөх нооргийг дахин нээхэд илүү их '
                                                                                'санах ой хэрэгтэй.',
                                                                      'type': 'string'},
                'ui_the_saved_assembly_could_not_be_opened': {'attributes': {'name': 'ui_the_saved_assembly_could_not_be_opened'},
                                                              'target': 'Хадгалсан эвлүүлгийг нээж чадсангүй: %1$s',
                                                              'type': 'string'},
                'ui_the_selected_location_is_not_writable': {'attributes': {'name': 'ui_the_selected_location_is_not_writable'},
                                                             'target': 'Сонгосон байршилд бичих боломжгүй.',
                                                             'type': 'string'},
                'ui_the_selected_provider_did_not_return_any_image': {'attributes': {'name': 'ui_the_selected_provider_did_not_return_any_image'},
                                                                      'target': 'Сонгосон үйлчилгээ үзүүлэгч ямар ч '
                                                                                'зургийн өгөгдөл буцаасангүй.',
                                                                      'type': 'string'},
                'ui_the_trim_would_remove_the_entire_image': {'attributes': {'name': 'ui_the_trim_would_remove_the_entire_image'},
                                                              'target': 'Энэ тайралт бүх зургийг арилгана.',
                                                              'type': 'string'},
                'ui_the_undo_cache_is_damaged': {'attributes': {'name': 'ui_the_undo_cache_is_damaged'},
                                                 'target': 'Буцаах кэш гэмтсэн.',
                                                 'type': 'string'},
                'ui_there_is_not_enough_memory_for_this_operation': {'attributes': {'name': 'ui_there_is_not_enough_memory_for_this_operation'},
                                                                     'target': 'Энэ үйлдлийг анхны нягтаршилаар хийхэд '
                                                                               'санах ой хүрэлцэхгүй. Автоматаар '
                                                                               'хэмжээ өөрчлөөгүй.',
                                                                     'type': 'string'},
                'ui_this_file_is_not_a_supported_image_use': {'attributes': {'name': 'ui_this_file_is_not_a_supported_image_use'},
                                                              'target': 'Энэ файл дэмжигдсэн зураг биш. PNG, JPEG, '
                                                                        'JPEG XL, WebP, HEIC, AVIF, BMP, GIF, DIB, '
                                                                        'TIFF, ICO, PDF эсвэл Base64 зургийн текст '
                                                                        'ашиглана уу.',
                                                              'type': 'string'},
                'ui_this_location_is_not_writable': {'attributes': {'name': 'ui_this_location_is_not_writable'},
                                                     'target': 'Энэ байршилд бичих боломжгүй.',
                                                     'type': 'string'},
                'ui_tolerance': {'attributes': {'name': 'ui_tolerance'}, 'target': 'Хүлцэл', 'type': 'string'},
                'ui_too_large_for_the_current_budget_reduce_the': {'attributes': {'name': 'ui_too_large_for_the_current_budget_reduce_the'},
                                                                   'target': 'Одоогийн хязгаарт хэт том байна. '
                                                                             'Хэмжээсийг багасгах эсвэл цуцлаад санах '
                                                                             'ой чөлөөлнө үү.',
                                                                   'type': 'string'},
                'ui_tool_categories': {'attributes': {'name': 'ui_tool_categories'},
                                       'target': 'Багажны ангиллууд. Бусад хэрэгслийг харахын тулд гүйлгэнэ',
                                       'type': 'string'},
                'ui_top': {'attributes': {'name': 'ui_top'}, 'target': 'Дээд', 'type': 'string'},
                'ui_trim_amounts_must_be_zero_or_greater': {'attributes': {'name': 'ui_trim_amounts_must_be_zero_or_greater'},
                                                            'target': 'Тайрах хэмжээ 0 эсвэл түүнээс их байх ёстой.',
                                                            'type': 'string'},
                'ui_trim_amounts_must_fit_inside_each_image_use': {'attributes': {'name': 'ui_trim_amounts_must_fit_inside_each_image_use'},
                                                                   'target': 'Тайрах хэмжээ зураг бүрийн дотор багтах '
                                                                             'ёстой; бүхэл пиксел эсвэл хувь ашиглана '
                                                                             'уу.',
                                                                   'type': 'string'},
                'ui_trim_expand_canvas_by_touch': {'attributes': {'name': 'ui_trim_expand_canvas_by_touch'},
                                                   'target': 'Зургийн талбарыг хүрэлтээр тайрах / өргөтгөх…',
                                                   'type': 'string'},
                'ui_trim_in_percent': {'attributes': {'name': 'ui_trim_in_percent'},
                                       'target': '%1$s тайралт, хувиар',
                                       'type': 'string'},
                'ui_trim_in_pixels': {'attributes': {'name': 'ui_trim_in_pixels'},
                                      'target': '%1$s тайралт, пикселээр',
                                      'type': 'string'},
                'ui_try_a_different_file_or_location': {'attributes': {'name': 'ui_try_a_different_file_or_location'},
                                                        'target': 'Өөр файл эсвэл байршил ашиглаж үзнэ үү.',
                                                        'type': 'string'},
                'ui_type_text': {'attributes': {'name': 'ui_type_text'}, 'target': 'Текст бичих', 'type': 'string'},
                'ui_underline': {'attributes': {'name': 'ui_underline'}, 'target': 'Доогуур зураас', 'type': 'string'},
                'ui_undo': {'attributes': {'name': 'ui_undo'}, 'target': 'Буцаах', 'type': 'string'},
                'ui_unexpected_data_in_the_undo_cache': {'attributes': {'name': 'ui_unexpected_data_in_the_undo_cache'},
                                                         'target': 'Буцаах кэшэд санаандгүй өгөгдөл байна.',
                                                         'type': 'string'},
                'ui_untitled': {'attributes': {'name': 'ui_untitled'}, 'target': 'Нэргүй', 'type': 'string'},
                'ui_use_1_1024_pixels': {'attributes': {'name': 'ui_use_1_1024_pixels'},
                                         'target': '1–1024 пиксел ашиглана уу.',
                                         'type': 'string'},
                'ui_use_50_300': {'attributes': {'formatted': 'false', 'name': 'ui_use_50_300'},
                                  'target': '50–300% ашиглана уу.',
                                  'type': 'string'},
                'ui_use_a_positive_target_dimension': {'attributes': {'name': 'ui_use_a_positive_target_dimension'},
                                                       'target': '0-ээс их зорилтот хэмжээс ашиглана уу.',
                                                       'type': 'string'},
                'ui_use_colour': {'attributes': {'name': 'ui_use_colour'},
                                  'target': 'Өнгийг хэрэглэх',
                                  'type': 'string'},
                'ui_use_rrggbb': {'attributes': {'name': 'ui_use_rrggbb'},
                                  'target': '#RRGGBB ашиглах',
                                  'type': 'string'},
                'ui_watercolor': {'attributes': {'name': 'ui_watercolor'}, 'target': 'Усан будаг', 'type': 'string'},
                'ui_width': {'attributes': {'name': 'ui_width'}, 'target': 'Өргөн (%1$s)', 'type': 'string'},
                'ui_width_in': {'attributes': {'name': 'ui_width_in'}, 'target': 'Өргөн (%1$s)', 'type': 'string'},
                'ui_working': {'attributes': {'name': 'ui_working'}, 'target': 'Ажиллаж байна…', 'type': 'string'},
                'ui_your_current_image_has_unsaved_changes': {'attributes': {'name': 'ui_your_current_image_has_unsaved_changes'},
                                                              'target': 'Одоогийн зурагт хадгалаагүй өөрчлөлт байна.',
                                                              'type': 'string'},
                'ui_zoom_in': {'attributes': {'name': 'ui_zoom_in'}, 'target': 'Томруулах', 'type': 'string'},
                'ui_zoom_out': {'attributes': {'name': 'ui_zoom_out'}, 'target': 'Жижигрүүлэх', 'type': 'string'}},
 'tok': {'ui_cancel': {'attributes': {'name': 'ui_cancel'}, 'target': '"o pali ala"', 'type': 'string'},
         'ui_done': {'attributes': {'name': 'ui_done'}, 'target': '"mi pini"', 'type': 'string'},
         'ui_menu_edit': {'attributes': {'name': 'ui_menu_edit'}, 'target': '"o ante"', 'type': 'string'},
         'ui_menu_help': {'attributes': {'name': 'ui_menu_help'}, 'target': '"sona pali"', 'type': 'string'},
         'ui_ok': {'attributes': {'name': 'ui_ok'}, 'target': '"pona"', 'type': 'string'},
         'ui_save': {'attributes': {'name': 'ui_save'}, 'target': '"o awen sona"', 'type': 'string'},
         'ui_save_a5d0d9': {'attributes': {'name': 'ui_save_a5d0d9'}, 'target': '@string/ui_save', 'type': 'string'},
         'ui_undo': {'attributes': {'name': 'ui_undo'}, 'target': '"o weka"', 'type': 'string'}}}
OUTSIDE_REVIEW={'ary': {},
 'mn-Cyrl-MN': {'colour20_custom_selected_slot': {'attributes': {'name': 'colour20_custom_selected_slot'},
                                                  'target': 'Өөрийн өнгө · %1$d-р нүдийг сонгов',
                                                  'type': 'string'},
                'colour20_empty_slot': {'attributes': {'name': 'colour20_empty_slot'},
                                        'target': 'Хоосон нүд %1$d. Одоогийн өнгийг хаана хадгалахаа сонгохын тулд '
                                                  'товшино.',
                                        'type': 'string'},
                'colour20_replace_slot': {'attributes': {'name': 'colour20_replace_slot'},
                                          'target': '%1$d-р нүдийг солих',
                                          'type': 'string'},
                'colour20_save_slot': {'attributes': {'name': 'colour20_save_slot'},
                                       'target': '%1$d-р нүдэд хадгалах',
                                       'type': 'string'},
                'colour20_saved_slot': {'attributes': {'name': 'colour20_saved_slot'},
                                        'target': 'Өнгийг %1$d-р нүдэд хадгаллаа',
                                        'type': 'string'},
                'colour20_stored_slot': {'attributes': {'name': 'colour20_stored_slot'},
                                         'target': '%1$d-р нүд · %2$s. Ашиглахын тулд товшино; өнгийг тохируулаад '
                                                   '«Солих»-ыг дарж өөрчлөлтийг хадгална.',
                                         'type': 'string'},
                'commons_blank_maps': {'attributes': {'name': 'commons_blank_maps'},
                                       'target': 'Wikimedia Commons · Хоосон газрын зураг…',
                                       'type': 'string'},
                'commons_check_file_licence': {'attributes': {'name': 'commons_check_file_licence'},
                                               'target': 'Газрын зураг бүрийн Commons дахь файлын хуудаснаас зохиогч, '
                                                         'лиценз болон зохиогчийг хэрхэн дурдах шаардлагыг шалгана уу. '
                                                         'Өөрчлөлтийг үүсмэл бүтээл гэж үзэж болно.',
                                               'type': 'string'},
                'commons_credit_copy_failed': {'attributes': {'name': 'commons_credit_copy_failed'},
                                               'target': 'Зургийн эх сурвалжийн мэдээллийг хуулж чадсангүй.',
                                               'type': 'string'},
                'commons_credit_copy_failed_reason': {'attributes': {'name': 'commons_credit_copy_failed_reason'},
                                                      'target': 'Зургийн эх сурвалжийн мэдээллийг хуулж чадсангүй: '
                                                                '%1$s',
                                                      'type': 'string'},
                'commons_credit_copy_out_of_memory': {'attributes': {'name': 'commons_credit_copy_out_of_memory'},
                                                      'target': 'Зургийн эх сурвалжийн мэдээллийг хуулахад санах ой '
                                                                'хүрэлцэхгүй.',
                                                      'type': 'string'},
                'commons_download_original_mismatch': {'attributes': {'name': 'commons_download_original_mismatch'},
                                                       'target': 'Commons-оос татах хүсэлтийг өөр эх файл руу '
                                                                 'чиглүүлсэн.',
                                                       'type': 'string'},
                'commons_import_raster_changes': {'attributes': {'name': 'commons_import_raster_changes'},
                                                  'target': 'AN Paint: background=#FFFFFF (тунгалаг байдлыг харгалзан '
                                                            'нэгтгэх).',
                                                  'type': 'string'},
                'commons_import_svg_changes': {'attributes': {'name': 'commons_import_svg_changes'},
                                               'target': 'AN Paint: SVG → PNG; анхны хэмжээ; antiAlias=false; '
                                                         'strokeDashArray=none; background=#FFFFFF.',
                                               'type': 'string'},
                'commons_metadata_ambiguous_file': {'attributes': {'name': 'commons_metadata_ambiguous_file'},
                                                    'target': 'Commons-ийн мета өгөгдөл аль ч файлтай таарахгүй эсвэл '
                                                              'нэгээс олон файлтай таарч байна',
                                                    'type': 'string'},
                'commons_metadata_cache_failed': {'attributes': {'name': 'commons_metadata_cache_failed'},
                                                  'target': 'Commons-оос авсан зохиогч, лицензийн мэдээллийг хадгалж '
                                                            'чадсангүй',
                                                  'type': 'string'},
                'commons_metadata_field_too_large': {'attributes': {'name': 'commons_metadata_field_too_large'},
                                                     'target': 'Commons-ийн зохиогч, лицензийн мэдээллийн талбар дахь '
                                                               'боловсруулаагүй бичвэрийн урт зөвшөөрөгдсөн хязгаараас '
                                                               'хэтэрсэн',
                                                     'type': 'string'},
                'commons_metadata_http_error': {'attributes': {'name': 'commons_metadata_http_error'},
                                                'target': 'Commons-ийн мета өгөгдөл: HTTP %1$s',
                                                'type': 'string'},
                'commons_metadata_invalid_page': {'attributes': {'name': 'commons_metadata_invalid_page'},
                                                  'target': 'Commons дахь зохиогч, лицензийн мэдээллийн хуудас '
                                                            'хүчингүй',
                                                  'type': 'string'},
                'commons_metadata_not_file_page': {'attributes': {'name': 'commons_metadata_not_file_page'},
                                                   'target': 'Энэ нь Commons дахь файлын хуудас биш',
                                                   'type': 'string'},
                'commons_metadata_original_mismatch': {'attributes': {'name': 'commons_metadata_original_mismatch'},
                                                       'target': 'Commons-оос авсан зохиогч, лицензийн мэдээлэл '
                                                                 'сонгосон эх файлтай тохирохгүй байна',
                                                       'type': 'string'},
                'commons_metadata_query_failed': {'attributes': {'name': 'commons_metadata_query_failed'},
                                                  'target': 'Commons-ын мета өгөгдлийн хүсэлт амжилтгүй боллоо.',
                                                  'type': 'string'},
                'commons_metadata_response_too_large': {'attributes': {'name': 'commons_metadata_response_too_large'},
                                                        'target': 'Commons-ийн мета өгөгдлийн хариуны хэмжээ '
                                                                  'хязгаараас хэтэрсэн.',
                                                        'type': 'string'},
                'commons_metadata_unavailable': {'attributes': {'name': 'commons_metadata_unavailable'},
                                                 'target': 'Commons дахь файлын мета өгөгдлийг авах боломжгүй',
                                                 'type': 'string'},
                'commons_svg_png_encode_failed': {'attributes': {'name': 'commons_svg_png_encode_failed'},
                                                  'target': 'Хоосон газрын зургийг PNG хэлбэрээр кодчилж чадсангүй',
                                                  'type': 'string'},
                'commons_svg_too_large': {'attributes': {'name': 'commons_svg_too_large'},
                                          'target': 'SVG > 32 MiB',
                                          'type': 'string'},
                'formats22_ascii_columns': {'attributes': {'name': 'formats22_ascii_columns'},
                                            'target': 'Өргөн (тэмдэгт)',
                                            'type': 'string'},
                'formats22_ascii_invert': {'attributes': {'name': 'formats22_ascii_invert'},
                                           'target': 'Гэрэл ба бараан тэмдэгтүүдийг урвуулах',
                                           'type': 'string'},
                'formats22_ascii_label': {'attributes': {'name': 'formats22_ascii_label'},
                                          'target': 'ASCII арт',
                                          'type': 'string'},
                'formats22_base64_description': {'attributes': {'name': 'formats22_base64_description'},
                                                 'target': 'Алдагдалгүй PNG-г data:image/png;base64, гэж эхэлсэн '
                                                           'Base64 текст болгон хадгална. Энэ текст файлыг дахин нээж '
                                                           'зургийг сэргээж болно. Base64 нь дотроо агуулсан PNG-ээс '
                                                           'том байна.',
                                                 'type': 'string'},
                'formats22_base64_label': {'attributes': {'name': 'formats22_base64_label'},
                                           'target': 'Base64 текст',
                                           'type': 'string'},
                'formats22_dib_description': {'attributes': {'name': 'formats22_dib_description'},
                                              'target': 'Шахаагүй 24-бит Windows DIB хадгална. Хүлээн авагч апп BMP '
                                                        'файлын толгой шаардвал BMP ашиглана.',
                                              'type': 'string'},
                'formats22_dib_size_limit': {'attributes': {'name': 'formats22_dib_size_limit'},
                                             'target': 'Зураг DIB файлын хэмжээнээс хэтэрсэн.',
                                             'type': 'string'},
                'formats22_ico_decode_budget': {'attributes': {'name': 'formats22_ico_decode_budget'},
                                                'target': 'Энэ дүрсийг тайлахад боломжит зургийн санах ойн хязгаараас '
                                                          'их санах ой хэрэгтэй.',
                                                'type': 'string'},
                'formats22_ico_description': {'attributes': {'name': 'formats22_ico_description'},
                                              'target': 'Сонгосон хэмжээнд (16–256 пиксел) PNG шахалттай нэг дүрс '
                                                        'хадгална. Таны зураг харьцаагаа хадгалж, тунгалаг дөрвөлжний '
                                                        'төвд байрлана.',
                                              'type': 'string'},
                'formats22_ico_dimensions_error': {'attributes': {'name': 'formats22_ico_dimensions_error'},
                                                   'target': 'Дүрсний зургийн хэмжээ түүний лавлах бичлэгтэй '
                                                             'тохирохгүй.',
                                                   'type': 'string'},
                'formats22_ico_invalid_size': {'attributes': {'name': 'formats22_ico_invalid_size'},
                                               'target': '16, 24, 32, 48, 64, 128 эсвэл 256 пиксел дүрсний хэмжээ '
                                                         'сонгоно уу.',
                                               'type': 'string'},
                'formats22_ico_size': {'attributes': {'name': 'formats22_ico_size'},
                                       'target': 'Дүрсний хэмжээ',
                                       'type': 'string'},
                'formats22_loading_page': {'attributes': {'name': 'formats22_loading_page'},
                                           'target': '%1$d / %2$d-р хуудас · Урьдчилсан харагдацыг ачаалж байна…',
                                           'type': 'string'},
                'formats22_next_page': {'attributes': {'name': 'formats22_next_page'},
                                        'target': 'Дараагийн хуудас',
                                        'type': 'string'},
                'formats22_open_page': {'attributes': {'name': 'formats22_open_page'},
                                        'target': 'Хуудас нээх',
                                        'type': 'string'},
                'formats22_page_description': {'attributes': {'name': 'formats22_page_description'},
                                               'target': '%1$s · %2$s\\n%3$d хуудас. Зураг болгон засах нэг хуудсыг '
                                                         'сонгоно уу.',
                                               'type': 'string'},
                'formats22_page_dimensions': {'attributes': {'name': 'formats22_page_dimensions'},
                                              'target': '%1$d / %2$d-р хуудас · %3$d × %4$d пиксел',
                                              'type': 'string'},
                'formats22_page_number': {'attributes': {'name': 'formats22_page_number'},
                                          'target': 'Хуудасны дугаар',
                                          'type': 'string'},
                'formats22_page_preview': {'attributes': {'name': 'formats22_page_preview'},
                                           'target': 'Сонгосон хуудасны урьдчилсан харагдац',
                                           'type': 'string'},
                'formats22_page_range': {'attributes': {'name': 'formats22_page_range'},
                                         'target': '1-ээс %1$d хүртэл хуудасны дугаар оруулна уу.',
                                         'type': 'string'},
                'formats22_pdf_crop': {'attributes': {'name': 'formats22_pdf_crop'},
                                       'target': 'PDF тайралт нь сонгосон хуудасны доторх хоосон биш тэгш өнцөгт байх '
                                                 'ёстой.',
                                       'type': 'string'},
                'formats22_pdf_dimensions': {'attributes': {'name': 'formats22_pdf_dimensions'},
                                             'target': 'PDF хуудасны хэмжээ буруу эсвэл импортлоход хэт том.',
                                             'type': 'string'},
                'formats22_pdf_encrypted': {'attributes': {'name': 'formats22_pdf_encrypted'},
                                            'target': 'PDF нууц үг шаарддаг эсвэл дэмжигдээгүй шифрлэлт ашиглаж байна. '
                                                      'Импортлохоос өмнө хамгаалалтгүй хуулбар хадгална уу.',
                                            'type': 'string'},
                'formats22_pdf_file_size': {'attributes': {'name': 'formats22_pdf_file_size'},
                                            'target': 'PDF нь хоосон биш бөгөөд 512 MiB-аас ихгүй файл байх ёстой.',
                                            'type': 'string'},
                'formats22_pdf_invalid': {'attributes': {'name': 'formats22_pdf_invalid'},
                                          'target': 'PDF-г уншиж чадсангүй. Файл гэмтсэн эсвэл энэ Android хувилбарын '
                                                    'дэмждэггүй боломж ашигласан байж болно.',
                                          'type': 'string'},
                'formats22_pdf_memory': {'attributes': {'name': 'formats22_pdf_memory'},
                                         'target': 'PDF дүрслэхэд боломжит зургийн санах ойн хязгаараас их санах ой '
                                                   'хэрэгтэй.',
                                         'type': 'string'},
                'formats22_pdf_page_count': {'attributes': {'name': 'formats22_pdf_page_count'},
                                             'target': 'PDF нь 1-ээс %1$d хүртэл хуудастай байх ёстой.',
                                             'type': 'string'},
                'formats22_pdf_page_index': {'attributes': {'name': 'formats22_pdf_page_index'},
                                             'target': 'Сонгосон PDF хуудас хүчингүй болсон. Энэ баримтаас хуудсыг '
                                                       'дахин сонгоно уу.',
                                             'type': 'string'},
                'formats22_preview_memory': {'attributes': {'name': 'formats22_preview_memory'},
                                             'target': 'Энэ урьдчилсан харагдацад санах ой хүрэлцэхгүй. Хуудсыг нээх '
                                                       'үед боломжтой бол жижиг хэмжээ сонгох санал гарна.',
                                             'type': 'string'},
                'formats22_preview_unavailable': {'attributes': {'name': 'formats22_preview_unavailable'},
                                                  'target': 'Урьдчилсан харагдац боломжгүй: %1$s',
                                                  'type': 'string'},
                'formats22_previous_page': {'attributes': {'name': 'formats22_previous_page'},
                                            'target': 'Өмнөх хуудас',
                                            'type': 'string'},
                'formats22_select_page': {'attributes': {'name': 'formats22_select_page'},
                                          'target': 'Хуудас сонгох',
                                          'type': 'string'},
                'formats22_text_not_image': {'attributes': {'name': 'formats22_text_not_image'},
                                             'target': 'Base64 текст дэмжигдсэн зураг агуулаагүй.',
                                             'type': 'string'},
                'formats22_tiff_compression': {'attributes': {'name': 'formats22_tiff_compression'},
                                               'target': 'Алдагдалгүй шахалт (Deflate)',
                                               'type': 'string'},
                'formats22_tiff_description': {'attributes': {'name': 'formats22_tiff_description'},
                                               'target': 'Нэг RGB хуудсыг хадгална. Шахалт нь пикселийг өөрчлөхгүйгээр '
                                                         'файлын хэмжээг багасгаж магадгүй; шахалтгүй TIFF хадгалахын '
                                                         'тулд унтраана.',
                                               'type': 'string'},
                'gallery_copy_credit': {'attributes': {'name': 'gallery_copy_credit'},
                                        'target': 'Эх сурвалжийн мэдээллийг хуулах',
                                        'type': 'string'},
                'gallery_credit_copied': {'attributes': {'name': 'gallery_credit_copied'},
                                          'target': 'Эх сурвалжийн мэдээллийг хууллаа',
                                          'type': 'string'},
                'gallery_credit_edit_hint': {'attributes': {'name': 'gallery_credit_edit_hint'},
                                             'target': 'Нийтлэхээс өмнө нэрлэсэн бүтээгч болон зохиогчийн эрхийн '
                                                       'мэдэгдлийг хадгалж, хийсэн өөрчлөлтийн тайлбарыг нэмнэ үү. '
                                                       'Нийтэлсэн зурагт байхгүй эх сурвалжуудыг устгана уу. Доорх '
                                                       'текстийг засварлаж болно.',
                                             'type': 'string'},
                'gallery_credit_gallery': {'attributes': {'name': 'gallery_credit_gallery'},
                                           'target': 'Галерей: %1$s',
                                           'type': 'string'},
                'gallery_credit_licence': {'attributes': {'name': 'gallery_credit_licence'},
                                           'target': 'Catrobat-ын эх бүтээл: CC BY-SA 4.0 — %1$s',
                                           'type': 'string'},
                'gallery_credit_publisher': {'attributes': {'name': 'gallery_credit_publisher'},
                                             'target': 'Нийтлэгч: Catrobat project',
                                             'type': 'string'},
                'gallery_credit_saved': {'attributes': {'name': 'gallery_credit_saved'},
                                         'target': 'Эх сурвалжийн текстийг хадгаллаа',
                                         'type': 'string'},
                'gallery_credit_source': {'attributes': {'name': 'gallery_credit_source'},
                                          'target': 'Эх сурвалж: %1$s',
                                          'type': 'string'},
                'gallery_credit_title': {'attributes': {'name': 'gallery_credit_title'},
                                         'target': 'Бүтээл: %1$s',
                                         'type': 'string'},
                'gallery_description': {'attributes': {'name': 'gallery_description'},
                                        'target': 'Шууд оруулахын тулд «Зургийг ашиглах»-ыг товшино. Зургийн хажуугийн '
                                                  '«Эх сурвалжийн мэдээллийг хуулах» нь нийтлэхэд хэрэглэх бүтээлийн '
                                                  'нэр, нийтлэгч, эх сурвалж, лицензийг хуулна. Catrobat-ын өөрийн '
                                                  'бүтээл CC BY-SA 4.0 лицензтэй; тусад нь нэрлэсэн бүтээгчид, '
                                                  'зохиогчийн эрх болон бусад эх сурвалжийн мэдэгдлийг хадгална уу. '
                                                  'Хийсэн өөрчлөлтөө тайлбарлаж, хувиргасан бүтээлээ CC BY-SA 4.0 '
                                                  'эсвэл нийцтэй лицензээр хуваалцана уу. «Эх сурвалжийн мэдээллийг '
                                                  'засах» нь эдгээр дэлгэрэнгүйг нэмэх боломж олгоно; оруулсан эх '
                                                  'сурвалжууд Файл → Тухай, лиценз ба талархал → Зургийн талархал '
                                                  'хэсэгт хадгалагдана.',
                                        'type': 'string'},
                'gallery_edit_credits': {'attributes': {'name': 'gallery_edit_credits'},
                                         'target': 'Эх сурвалжийн мэдээллийг засах',
                                         'type': 'string'},
                'gallery_external_link_no_handler': {'attributes': {'name': 'gallery_external_link_no_handler'},
                                                     'target': 'Android энэ холбоосыг нээх апп олсонгүй.',
                                                     'type': 'string'},
                'gallery_image_component_unavailable': {'attributes': {'name': 'gallery_image_component_unavailable'},
                                                        'target': 'Зураг боловсруулахад шаардлагатай бүрэлдэхүүн '
                                                                  'хэсгийг ашиглах боломжгүй байна. Зургийг '
                                                                  'импортлоогүй.',
                                                        'type': 'string'},
                'gallery_use_image': {'attributes': {'name': 'gallery_use_image'},
                                      'target': 'Зургийг ашиглах',
                                      'type': 'string'},
                'legacy_credits_add': {'attributes': {'name': 'legacy_credits_add'},
                                       'target': 'Сонгосон эх сурвалжийн мэдээллийг энэ зурагт нэмэх',
                                       'type': 'string'},
                'legacy_credits_added': {'attributes': {'name': 'legacy_credits_added'},
                                         'target': 'Эх сурвалжийн мэдээллийг энэ зурагт нэмлээ.',
                                         'type': 'string'},
                'legacy_credits_existing': {'attributes': {'name': 'legacy_credits_existing'},
                                            'target': 'Энэ зурагт тухайн эх сурвалжийн мэдээлэл аль хэдийн байна. '
                                                      'Текстийг нь хэвээр үлдээлээ.',
                                            'type': 'string'},
                'legacy_credits_hint': {'attributes': {'name': 'legacy_credits_hint'},
                                        'target': 'Энэ эх сурвалжийн мэдээллийг өмнө нь хадгалсан бөгөөд өөр зурагт '
                                                  'хамаарах байж болно. Энэ зурагт мэдээллийг нь нэмэх эх сурвалжийг '
                                                  'сонгоно уу, эсвэл бүтэн текстийг нь файл болгон хадгална уу.',
                                        'type': 'string'},
                'legacy_credits_save_text': {'attributes': {'name': 'legacy_credits_save_text'},
                                             'target': 'Сонгосон эх сурвалжийн мэдээллийг текст болгон хадгалах',
                                             'type': 'string'},
                'legacy_credits_title': {'attributes': {'name': 'legacy_credits_title'},
                                         'target': 'Өмнө хадгалсан эх сурвалжийн мэдээлэл',
                                         'type': 'string'},
                'save20_bmp_description': {'attributes': {'name': 'save20_bmp_description'},
                                           'target': 'Шахаагүй 24-бит RGB; өнгө яг хадгалагдана, файл том байна.',
                                           'type': 'string'},
                'save20_bmp_size_limit': {'attributes': {'name': 'save20_bmp_size_limit'},
                                          'target': 'Зураг BMP файлын хэмжээнээс хэтэрсэн.',
                                          'type': 'string'},
                'save20_gif_size_limit': {'attributes': {'name': 'save20_gif_size_limit'},
                                          'target': 'GIF-ийн тал бүр 65,535 пикселээс их байж болохгүй.',
                                          'type': 'string'},
                'save20_unsupported_tagged_colour': {'attributes': {'name': 'save20_unsupported_tagged_colour'},
                                                     'target': 'Энэ BMP эсвэл GIF нь AN Paint одоогоор хөрвүүлж '
                                                               'чадахгүй өнгөний профайл ашиглаж байна. Импортлохоос '
                                                               'өмнө өнгө удирддаг засварлагчаар sRGB PNG болгон '
                                                               'хөрвүүлнэ үү.',
                                                     'type': 'string'},
                'ui_aa_bb_0123': {'attributes': {'name': 'ui_aa_bb_0123'},
                                  'target': 'Aa Bb 0123 · あいう',
                                  'type': 'string'},
                'ui_about_copyright': {'attributes': {'name': 'ui_about_copyright'},
                                       'target': 'Тухай ба зохиогчийн эрх',
                                       'type': 'string'},
                'ui_about_copyright_licence': {'attributes': {'name': 'ui_about_copyright_licence'},
                                               'target': 'Тухай, зохиогчийн эрх ба лиценз',
                                               'type': 'string'},
                'ui_about_credits23': {'attributes': {'name': 'ui_about_credits23'},
                                       'target': 'Тухай, лиценз ба талархал',
                                       'type': 'string'},
                'ui_add_active23': {'attributes': {'name': 'ui_add_active23'},
                                    'target': 'Одоогийн өнгийг нэмэх',
                                    'type': 'string'},
                'ui_add_images': {'attributes': {'name': 'ui_add_images'}, 'target': 'Зураг нэмэх', 'type': 'string'},
                'ui_add_images_first': {'attributes': {'name': 'ui_add_images_first'},
                                        'target': 'Эхлээд зураг нэмнэ үү.',
                                        'type': 'string'},
                'ui_add_images_then_drag_a_thumbnail_here': {'attributes': {'name': 'ui_add_images_then_drag_a_thumbnail_here'},
                                                             'target': 'Зураг нэмээд, дараа нь өнгөц зургийг энд чирнэ '
                                                                       'үү',
                                                             'type': 'string'},
                'ui_add_palette23': {'attributes': {'name': 'ui_add_palette23'},
                                     'target': 'Өнгөний самбарт нэмэх',
                                     'type': 'string'},
                'ui_add_to_custom_colours': {'attributes': {'name': 'ui_add_to_custom_colours'},
                                             'target': 'Өөрийн өнгөнд нэмэх',
                                             'type': 'string'},
                'ui_add_up_to_20_images_with_android_s': {'attributes': {'name': 'ui_add_up_to_20_images_with_android_s'},
                                                          'target': 'Android-ын файл сонгогчоор 20 хүртэл зураг нэмнэ. '
                                                                    'Доод тавиурт өнгөц зураг, файлын нэр, тайралт '
                                                                    'болон «Ижил өргөн» эсвэл «Ижил өндөр» тохируулгын '
                                                                    'дараах зургийн хэмжээ, мөн үйлчилгээ үзүүлэгчээс '
                                                                    'өгсөн тохиолдолд файлын өөрчлөгдсөн хугацаа '
                                                                    'харагдана. Файлын нэр эсвэл өөрчлөгдсөн '
                                                                    'хугацаагаар эрэмбэлж болно; эрэмбэлэхэд '
                                                                    'байрлуулсан зургуудын байрлал '
                                                                    'өөрчлөгдөхгүй.\\n\\nӨнгөц зургийг товшиж сонгоно. '
                                                                    '«Зураг тайрах» нь тухайн зургийг тайрна; «Бөөнөөр '
                                                                    'тайрах» нь сонгосон зургуудын ирмэгээс пикселээр '
                                                                    'эсвэл хувиар заасан хэмжээгээр тайрна. Тайрах '
                                                                    'бариулыг чирэх эсвэл хэмжээг тоогоор оруулна. '
                                                                    '«Тайралтыг сэргээх» нь анхны ирмэгүүдийг '
                                                                    'сэргээнэ. Тайрах нь эх зургийг өөрчлөхгүй бөгөөд '
                                                                    'тайралтыг буцааж болно.\\n\\nӨнгөц зургийг удаан '
                                                                    'дарж, эсвэл ажлын талбарт байгаа зургийг чирээд '
                                                                    'тодруулсан ирмэг дээр тавина. Хагас тунгалаг '
                                                                    'урьдчилсан харагдац нь ирмэгт залгаж байрлуулахад '
                                                                    'гарах үр дүнг яг таг харуулна. Баруун талд '
                                                                    'залгахад дээд ирмэгүүд, доод талд залгахад зүүн '
                                                                    'ирмэгүүд зэрэгцэнэ. Мөн өнгөц зургийг товшоод '
                                                                    'дараа нь + тэмдэгтэй байг товшиж болно. Ирмэгт '
                                                                    'залгаж байрлуулах үед эхний зураг координатын '
                                                                    'эхлэл цэгээс эхэлнэ. Залгаж байрлуулсан зургууд '
                                                                    'нь залгасан суурь зургийг нь тайрахад шилжиж '
                                                                    'болно. Ирмэгт залгаж байрлуулах үед зураг '
                                                                    'давхцахыг зөвшөөрөхгүй.\\n\\nЗургийг сонгоод «Яг '
                                                                    'таг байрлал»-аар зүүн дээд булангийн X/Y '
                                                                    'координатыг тэгээс эхлэх бүхэл пикселээр '
                                                                    'тохируулна. Бусад зургийн байрлал өөрчлөгдөхгүй '
                                                                    'бөгөөд зургуудыг давхцуулж болно.\\n\\n«Ижил '
                                                                    'өргөн» болон «Ижил өндөр» нь зураг бүрийн өргөн, '
                                                                    'өндрийн харьцааг хадгалж, бүх оролтын зургийн '
                                                                    'өргөн эсвэл өндрийг ижил болгоно. Пиксел, хувь, '
                                                                    '«Хамгийн бага» эсвэл «Хамгийн их»-ийг сонгоно. '
                                                                    '«Анхны хэмжээг сэргээх» нь хэмжээг ижилсүүлсэн '
                                                                    'тохируулгыг цуцалж, тайралтыг хэвээр '
                                                                    'үлдээнэ.\\n\\n«Байрлалаас гаргах» нь зөвхөн '
                                                                    'сонгосон зургийг тавиурт буцаана. Бусад зураг '
                                                                    'байрлуулсан хэвээр үлдэнэ; залгаж байрлуулсан '
                                                                    'зургууд сул зайг нөхөхөөр шилжиж болно. «Устгах» '
                                                                    'нь зөвхөн тухайн оролтын зургийг устгана. '
                                                                    '«Буцаах» болон «Дахин хийх»-ээр эдгээр '
                                                                    'өөрчлөлтийг буцааж, дахин хийж болно. Байрлуулсан '
                                                                    'зургийг чирж дахин байрлуулна; хоосон зайг '
                                                                    'чирэхэд харагдац шилжинэ. Хоёр хуруугаар чимхэх '
                                                                    'хөдөлгөөнөөр харагдацыг томруулж, жижигрүүлнэ. '
                                                                    '«Бүгдийг харуулах» нь бүх эвлүүлгийг багтаан '
                                                                    'харуулахаар харагдацын томруулалтыг тохируулна; '
                                                                    'гаралтын хэмжээг огт өөрчлөхгүй.\\n\\n«PNG '
                                                                    'хадгалах» нь эвлүүлсэн зургийг шууд хадгална. '
                                                                    '«Paint-д засах» нь эвлүүлсэн зургийг үндсэн '
                                                                    'засварлагч руу шилжүүлж, одоогийн зургийг буцааж '
                                                                    'болох үйлдлээр солино. Гаралт санах ойн '
                                                                    'хязгаараас давбал жижиг хэмжээтэй гаралтын '
                                                                    'хуулбар сонгох боломж санал болгосон тохиолдолд '
                                                                    'түүнийг сонгоно. Маш жижиг гаралт ч хязгаараас '
                                                                    'давбал апп хэмжээ сонгогчийн оронд санах ойн '
                                                                    'анхааруулга харуулна. Эх зургийн файлууд '
                                                                    'өөрчлөгдөхгүй. Одоогийн эвлүүлгийг төхөөрөмжид '
                                                                    'хадгалж, буцаж ороход дахин нээнэ.\\n\\nЭнэ '
                                                                    'горимд үндсэн засварлагчийн «Файл > Тухай, лиценз '
                                                                    'ба талархал» самбарт харуулсан Catrobat/AGPL '
                                                                    'болон ашигласан материалын талаарх талархлын '
                                                                    'мэдээллийг мөн ашиглана.',
                                                          'type': 'string'},
                'ui_added_palette23': {'attributes': {'name': 'ui_added_palette23'},
                                       'target': 'Өнгө нэмэгдлээ',
                                       'type': 'string'},
                'ui_advanced': {'attributes': {'name': 'ui_advanced'}, 'target': 'Нарийвчилсан', 'type': 'string'},
                'ui_agpl_licence': {'attributes': {'name': 'ui_agpl_licence'},
                                    'target': 'AGPL лиценз',
                                    'type': 'string'},
                'ui_an_assembly_can_contain_up_to_20_images': {'attributes': {'name': 'ui_an_assembly_can_contain_up_to_20_images'},
                                                               'target': 'Нэг эвлүүлэгт 20 хүртэл зураг байж болно. '
                                                                         'Өөр зураг нэмэхийн тулд нэг зургийг устгана '
                                                                         'уу.',
                                                               'type': 'string'},
                'ui_an_assembly_can_contain_up_to_20_images_86d995': {'attributes': {'name': 'ui_an_assembly_can_contain_up_to_20_images_86d995'},
                                                                      'target': 'Нэг эвлүүлэгт 20 хүртэл зураг байж '
                                                                                'болно.',
                                                                      'type': 'string'},
                'ui_an_image_cannot_attach_to_itself_or_one': {'attributes': {'name': 'ui_an_image_cannot_attach_to_itself_or_one'},
                                                               'target': 'Зургийг өөрт нь эсвэл өөрт нь холбогдсон '
                                                                         'зурагт холбож болохгүй.',
                                                               'type': 'string'},
                'ui_an_paint_assembly_image': {'attributes': {'name': 'ui_an_paint_assembly_image'},
                                               'target': 'AN Paint эвлүүлсэн зураг',
                                               'type': 'string'},
                'ui_an_paint_image': {'attributes': {'name': 'ui_an_paint_image'},
                                      'target': 'AN Paint зураг',
                                      'type': 'string'},
                'ui_apply_to_all': {'attributes': {'name': 'ui_apply_to_all'},
                                    'target': 'Бүгдэд хэрэглэх',
                                    'type': 'string'},
                'ui_apply_to_these_images': {'attributes': {'name': 'ui_apply_to_these_images'},
                                             'target': 'Эдгээр зурагт хэрэглэх',
                                             'type': 'string'},
                'ui_assembly_decoded_output_estimated_editing_render_memory_at': {'attributes': {'name': 'ui_assembly_decoded_output_estimated_editing_render_memory_at'},
                                                                                  'target': 'Эвлүүлэг: %1$s\\nТайлсан '
                                                                                            'гаралт: %2$s\\nАнхны '
                                                                                            'хэмжээнд засах/дүрслэхэд '
                                                                                            'шаардагдах санах ойн '
                                                                                            'тооцоо: %3$s',
                                                                                  'type': 'string'},
                'ui_assembly_exact_position': {'attributes': {'name': 'ui_assembly_exact_position'},
                                               'target': 'Яг таг байрлал',
                                               'type': 'string'},
                'ui_assembly_output_size': {'attributes': {'name': 'ui_assembly_output_size'},
                                            'target': 'Эвлүүлгийн гаралтын хэмжээ',
                                            'type': 'string'},
                'ui_assembly_png': {'attributes': {'name': 'ui_assembly_png'},
                                    'target': 'Эвлүүлэг.png',
                                    'type': 'string'},
                'ui_assembly_position_help': {'attributes': {'name': 'ui_assembly_position_help'},
                                              'target': 'Энэ зургийн зүүн дээд булангийн байрлалыг гаралтын зургийн '
                                                        'талбарт тохируулна. X ба Y нь тэгээс эхлэх бүхэл пикселийн '
                                                        'тоо юм. Бусад зураг одоогийн байрлалаа хадгална. Энд '
                                                        'давхцуулахыг зөвшөөрнө; сүүлд импортолсон зураг өмнөх '
                                                        'зургуудын дээр зурагдана. Талбар байрлуулсан бүх зургийг '
                                                        'багтаахаар тэлнэ. Тайралт болон хэмжээ өөрчлөгдөхгүй.',
                                              'type': 'string'},
                'ui_assembly_position_nonnegative': {'attributes': {'name': 'ui_assembly_position_nonnegative'},
                                                     'target': 'X ба Y нь 0-ээс 2147483647 хүртэлх бүхэл тоо байх '
                                                               'ёстой.',
                                                     'type': 'string'},
                'ui_assembly_target_x': {'attributes': {'name': 'ui_assembly_target_x'},
                                         'target': 'X байрлал (зүүн захаас пикселээр)',
                                         'type': 'string'},
                'ui_assembly_target_y': {'attributes': {'name': 'ui_assembly_target_y'},
                                         'target': 'Y байрлал (дээд захаас пикселээр)',
                                         'type': 'string'},
                'ui_assembly_unknown_image': {'attributes': {'name': 'ui_assembly_unknown_image'},
                                              'target': 'Сонгосон зураг энэ эвлүүлэгт байхаа больсон.',
                                              'type': 'string'},
                'ui_batch_crop': {'attributes': {'name': 'ui_batch_crop'},
                                  'target': 'Бөөнөөр тайрах',
                                  'type': 'string'},
                'ui_batch_crop_images': {'attributes': {'name': 'ui_batch_crop_images'},
                                         'target': 'Зургуудыг бөөнөөр тайрах',
                                         'type': 'string'},
                'ui_bottom23': {'attributes': {'name': 'ui_bottom23'},
                                'target': 'Доод талд зэрэгцүүлэх',
                                'type': 'string'},
                'ui_by_pixels_hold_and_drag_to_place': {'attributes': {'name': 'ui_by_pixels_hold_and_drag_to_place'},
                                                        'target': '%1$s. %2$s. %3$s × %4$s пиксел. Байрлуулахын тулд '
                                                                  'удаан дарж чирнэ үү.',
                                                        'type': 'string'},
                'ui_calligraphy': {'attributes': {'name': 'ui_calligraphy'}, 'target': 'Уран бичлэг', 'type': 'string'},
                'ui_casual': {'attributes': {'name': 'ui_casual'}, 'target': 'Энгийн', 'type': 'string'},
                'ui_catrobat_online_gallery_artwork_by_its_credited_creators': {'attributes': {'name': 'ui_catrobat_online_gallery_artwork_by_its_credited_creators'},
                                                                                'target': 'Catrobat онлайн галерей · '
                                                                                          'бүтээлийн зохиогчдыг '
                                                                                          'талархлын мэдээлэлд дурдсан',
                                                                                'type': 'string'},
                'ui_catrobat_s_own_artwork_uses_cc_by_sa': {'attributes': {'name': 'ui_catrobat_s_own_artwork_uses_cc_by_sa'},
                                                            'target': 'Catrobat-ын өөрийн бүтээл CC BY-SA 4.0 '
                                                                      'лицензтэй. Бүтээгчийн нэрийг хадгалж, '
                                                                      'өөрчлөлтийг ижил лицензээр хуваалцана уу. '
                                                                      'Нэмэлт талархлын шаардлага байгаа эсэхийг эх '
                                                                      'хуудсаас шалгана уу. Эх URL нь Файл > Тухай, '
                                                                      'лиценз ба талархал > Зургийн талархал хэсэгт '
                                                                      'хадгалагдана.',
                                                            'type': 'string'},
                'ui_catrobat_sticker_gallery': {'attributes': {'name': 'ui_catrobat_sticker_gallery'},
                                                'target': 'Catrobat наалтны галерей…',
                                                'type': 'string'},
                'ui_close_polygon': {'attributes': {'name': 'ui_close_polygon'},
                                     'target': 'Олон өнцөгтийг хаах',
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
                                 'target': '%2$s дахь нийтлэг %1$s',
                                 'type': 'string'},
                'ui_common_in_pixels': {'attributes': {'name': 'ui_common_in_pixels'},
                                        'target': 'Пикселээрх нийтлэг %1$s',
                                        'type': 'string'},
                'ui_copper': {'attributes': {'name': 'ui_copper'}, 'target': 'Зэс', 'type': 'string'},
                'ui_copy_an_area_or_use_file_insert_image': {'attributes': {'name': 'ui_copy_an_area_or_use_file_insert_image'},
                                                             'target': 'Талбайг хуулж эсвэл Зурах → Оруулах → Бусад '
                                                                       'зураг командыг ашиглана уу.',
                                                             'type': 'string'},
                'ui_copy_decoded_image_at_this_size_estimated_loading': {'attributes': {'name': 'ui_copy_decoded_image_at_this_size_estimated_loading'},
                                                                         'target': 'Хуулбар: %1$s\\nЭнэ хэмжээнд '
                                                                                   'тайлсан зураг: '
                                                                                   '%2$s\\nАчаалах/засах санах ойн '
                                                                                   'тооцоо: %3$s\\n',
                                                                         'type': 'string'},
                'ui_corners_and_edges_resize_round_handle_rotates': {'attributes': {'name': 'ui_corners_and_edges_resize_round_handle_rotates'},
                                                                     'target': 'Булан ба ирмэгээр хэмжээг өөрчилнө. '
                                                                               'Дугуй бариулаар эргүүлнэ.',
                                                                     'type': 'string'},
                'ui_could_not_create_the_assembly': {'attributes': {'name': 'ui_could_not_create_the_assembly'},
                                                     'target': 'Эвлүүлэг үүсгэж чадсангүй: %1$s',
                                                     'type': 'string'},
                'ui_could_not_decode_the_cropped_region_of': {'attributes': {'name': 'ui_could_not_decode_the_cropped_region_of'},
                                                              'target': '%1$s-ийн тайрсан хэсгийг тайлж чадсангүй.',
                                                              'type': 'string'},
                'ui_could_not_export_source_code': {'attributes': {'name': 'ui_could_not_export_source_code'},
                                                    'target': 'Эх кодыг экспортолж чадсангүй',
                                                    'type': 'string'},
                'ui_could_not_load_gallery_image': {'attributes': {'name': 'ui_could_not_load_gallery_image'},
                                                    'target': 'Галерейн зургийг ачаалж чадсангүй: %1$s',
                                                    'type': 'string'},
                'ui_create_output': {'attributes': {'name': 'ui_create_output'},
                                     'target': 'Гаралт үүсгэх',
                                     'type': 'string'},
                'ui_creator_on_source34': {'attributes': {'name': 'ui_creator_on_source34'},
                                           'target': 'Оруулсан хүний мэдээллийг эх хуудсаас харна уу.',
                                           'type': 'string'},
                'ui_credits_terms': {'attributes': {'name': 'ui_credits_terms'},
                                     'target': 'Талархал ба нөхцөл',
                                     'type': 'string'},
                'ui_cropped_thumbnail': {'attributes': {'name': 'ui_cropped_thumbnail'},
                                         'target': 'Тайрсан өнгөц зураг: %1$s',
                                         'type': 'string'},
                'ui_current_safe_budget_2f_mp': {'attributes': {'name': 'ui_current_safe_budget_2f_mp'},
                                                 'target': 'Одоогийн аюулгүй хязгаар: %1$.2f MP.',
                                                 'type': 'string'},
                'ui_current_safe_editing_budget_s_up_to_2f': {'attributes': {'name': 'ui_current_safe_editing_budget_s_up_to_2f'},
                                                              'target': 'Одоогийн аюулгүй засварлах хязгаар: %1$s · '
                                                                        'декодерын нэмэлт хэрэглээнээс өмнө %2$.2f MP '
                                                                        'хүртэл',
                                                              'type': 'string'},
                'ui_cursive': {'attributes': {'name': 'ui_cursive'}, 'target': 'Бичмэл', 'type': 'string'},
                'ui_cursor_drawing32': {'attributes': {'name': 'ui_cursor_drawing32'},
                                        'target': 'Курсороор зурах',
                                        'type': 'string'},
                'ui_cursor_help29': {'attributes': {'name': 'ui_cursor_help29'},
                                     'target': '@string/ui_cursor_help31',
                                     'type': 'string'},
                'ui_cursor_help31': {'attributes': {'name': 'ui_cursor_help31'},
                                     'target': 'Курсорыг байрлуулахын тулд чирнэ. Дэлгэц дээрх зурах товчийг товшоод, '
                                               'дараа нь харагдацыг шилжүүлж зурна. Дахин товшиж зогсооно. Бийр ба '
                                               'мөрийн тохиргоог Зурах → Зурах хэсгээс сонгоно.',
                                     'type': 'string'},
                'ui_cursor_ink30': {'attributes': {'name': 'ui_cursor_ink30'},
                                    'target': 'Курсороор зурах',
                                    'type': 'string'},
                'ui_cursor_marker_help31': {'attributes': {'name': 'ui_cursor_marker_help31'},
                                            'target': 'Зурж буй бийрийн хэмжээг өөрчлөхгүйгээр зөвхөн курсорын '
                                                      'тэмдэглэгээг томруулна.',
                                            'type': 'string'},
                'ui_cursor_marker_size31': {'attributes': {'formatted': 'false', 'name': 'ui_cursor_marker_size31'},
                                            'target': 'Курсорын тэмдэглэгээний хэмжээ (%)',
                                            'type': 'string'},
                'ui_cursor_pan_draw32': {'attributes': {'name': 'ui_cursor_pan_draw32'},
                                         'target': 'Харагдацыг шилжүүлж зурж эхэлнэ. Дахин товшиж зогсооно.',
                                         'type': 'string'},
                'ui_cursor_pan_move32': {'attributes': {'name': 'ui_cursor_pan_move32'},
                                         'target': 'Харагдацыг шилжүүлж курсорыг байрлуулна. Зурж эхлэхийн тулд зурах '
                                                   'товчийг товшино.',
                                         'type': 'string'},
                'ui_cursor_position26': {'attributes': {'name': 'ui_cursor_position26'},
                                         'target': 'x: %1$d, y: %2$d',
                                         'type': 'string'},
                'ui_cursor_settings31': {'attributes': {'name': 'ui_cursor_settings31'},
                                         'target': 'Курсороор зурах тохиргоо…',
                                         'type': 'string'},
                'ui_cursor_shape31': {'attributes': {'name': 'ui_cursor_shape31'},
                                      'target': 'Курсорын хэлбэр',
                                      'type': 'string'},
                'ui_cursor_start31': {'attributes': {'name': 'ui_cursor_start31'},
                                      'target': 'Зурж эхлэх',
                                      'type': 'string'},
                'ui_cursor_stop31': {'attributes': {'name': 'ui_cursor_stop31'},
                                     'target': 'Зурахаа зогсоох',
                                     'type': 'string'},
                'ui_cursor_tap_hint37': {'attributes': {'name': 'ui_cursor_tap_hint37'},
                                         'target': 'Зурж эхлэх эсвэл зогсоохын тулд курсорыг товшино.',
                                         'type': 'string'},
                'ui_custom_colour': {'attributes': {'name': 'ui_custom_colour'},
                                     'target': 'Өөрийн өнгө %1$s',
                                     'type': 'string'},
                'ui_custom_colours_hold_a_swatch_to_replace_it': {'attributes': {'name': 'ui_custom_colours_hold_a_swatch_to_replace_it'},
                                                                  'target': 'Өөрийн өнгөнүүд · өнгийн дээжийг удаан '
                                                                            'дарж солино',
                                                                  'type': 'string'},
                'ui_disable_cursor_drawing': {'attributes': {'name': 'ui_disable_cursor_drawing'},
                                              'target': 'Курсороор зурахыг идэвхгүй болгох',
                                              'type': 'string'},
                'ui_disable_cursor_drawing33': {'attributes': {'name': 'ui_disable_cursor_drawing33'},
                                                'target': 'Курсороор зурахыг идэвхгүй болгох',
                                                'type': 'string'},
                'ui_downloading_image': {'attributes': {'name': 'ui_downloading_image'},
                                         'target': 'Зураг татаж байна…',
                                         'type': 'string'},
                'ui_drag_a_line_then_drag_twice_to_set': {'attributes': {'name': 'ui_drag_a_line_then_drag_twice_to_set'},
                                                          'target': 'Эхлээд шулуун чирж зурна, дараа нь хоёр удаа чирж '
                                                                    'хоёр нугалааг тогтооно. «Муруйг дуусгах» нь '
                                                                    'тухайн үеийн хэлбэрийг шууд батална.',
                                                          'type': 'string'},
                'ui_drag_a_selection_drag_inside_to_move_square': {'attributes': {'name': 'ui_drag_a_selection_drag_inside_to_move_square'},
                                                                   'target': 'Сонголтыг чирж үүсгэнэ. Дотор нь чирж '
                                                                             'зөөнө, дөрвөлжин булан эсвэл ирмэгийн '
                                                                             'бариулаар хэмжээг өөрчилнө, дугуй '
                                                                             'бариулаар эргүүлнэ. «Харьцааг түгжих» нь '
                                                                             'хэлбэрийг хадгална.',
                                                                   'type': 'string'},
                'ui_drag_across_the_ellipse_s_bounding_box': {'attributes': {'name': 'ui_drag_across_the_ellipse_s_bounding_box'},
                                                              'target': 'Зуувангийн хүрээний эсрэг булангуудын хооронд '
                                                                        'чирнэ.',
                                                              'type': 'string'},
                'ui_drag_between_opposite_corners_choose_outline_or_fill': {'attributes': {'name': 'ui_drag_between_opposite_corners_choose_outline_or_fill'},
                                                                            'target': 'Эсрэг булангуудын хооронд '
                                                                                      'чирнэ. Доороос хүрээ эсвэл '
                                                                                      'дүүргэлтийг сонгоно.',
                                                                            'type': 'string'},
                'ui_drag_between_opposite_corners_to_draw_a_five': {'attributes': {'name': 'ui_drag_between_opposite_corners_to_draw_a_five'},
                                                                    'target': 'Эсрэг булангуудын хооронд чирж таван '
                                                                              'хошуут од зурна. Хүрээ эсвэл дүүргэлт '
                                                                              'сонгоно.',
                                                                    'type': 'string'},
                'ui_drag_between_opposite_corners_to_draw_a_heart': {'attributes': {'name': 'ui_drag_between_opposite_corners_to_draw_a_heart'},
                                                                     'target': 'Эсрэг булангуудын хооронд чирж зүрх '
                                                                               'зурна. Хүрээ эсвэл дүүргэлт сонгоно.',
                                                                     'type': 'string'},
                'ui_drag_from_the_start_to_the_end_of': {'attributes': {'name': 'ui_drag_from_the_start_to_the_end_of'},
                                                         'target': 'Шугамын эхлэлээс төгсгөл хүртэл чирнэ.',
                                                         'type': 'string'},
                'ui_drag_from_the_tail_towards_the_arrowhead_choose': {'attributes': {'name': 'ui_drag_from_the_tail_towards_the_arrowhead_choose'},
                                                                       'target': 'Сумны сүүлээс үзүүр рүү чирнэ. Хүрээ '
                                                                                 'эсвэл дүүргэлт сонгоно.',
                                                                       'type': 'string'},
                'ui_drag_out_to_expand_in_to_trim_drag': {'attributes': {'name': 'ui_drag_out_to_expand_in_to_trim_drag'},
                                                          'target': 'Гадагш чирж томруулна, дотогш чирж тайрна. Дотор '
                                                                    'нь чирж хүрээг зөөнө. Илүү зай харахын тулд хоёр '
                                                                    'хуруугаар чимхэх эсвэл «Багтаах»-ыг ашиглана. '
                                                                    'Шинэ зайг BG өнгөөр дүүргэнэ.',
                                                          'type': 'string'},
                'ui_drag_placed_images_to_move_them_hold_and': {'attributes': {'name': 'ui_drag_placed_images_to_move_them_hold_and'},
                                                                'target': 'Байрлуулсан зургийг чирж зөөнө. Өнгөц '
                                                                          'зургийг удаан дарж чирээд нэмнэ.',
                                                                'type': 'string'},
                'ui_drag_to_erase_with_the_background_colour': {'attributes': {'name': 'ui_drag_to_erase_with_the_background_colour'},
                                                                'target': 'Дэвсгэр өнгөөр арилгахын тулд чирнэ.',
                                                                'type': 'string'},
                'ui_drag_to_pan_without_drawing_pinch_with_two': {'attributes': {'name': 'ui_drag_to_pan_without_drawing_pinch_with_two'},
                                                                  'target': 'Зурахгүйгээр харагдацыг шилжүүлэхийн тулд '
                                                                            'чирнэ. Хоёр хуруугаар чимхэж томруулж, '
                                                                            'шилжүүлнэ. Хоёр хурууны навигаци зургийн '
                                                                            'хэрэгслүүд дээр ч ажиллана.',
                                                                  'type': 'string'},
                'ui_draw_a_crisp_one_pixel_line': {'attributes': {'name': 'ui_draw_a_crisp_one_pixel_line'},
                                                   'target': 'Тод ирмэгтэй шугам зурна. Өргөнийг 1–100 пикселээр '
                                                             'тохируулна.',
                                                   'type': 'string'},
                'ui_draw_around_an_area_drag_inside_to_move': {'attributes': {'name': 'ui_draw_around_an_area_drag_inside_to_move'},
                                                               'target': 'Талбайг тойруулж зурна. Дотор нь чирж зөөнө, '
                                                                         'дөрвөлжин булан эсвэл ирмэгийн бариулаар '
                                                                         'хэмжээг өөрчилнө, дугуй бариулаар эргүүлнэ. '
                                                                         '«Сонголтыг батлах» нь засварыг хэрэглэнэ.',
                                                               'type': 'string'},
                'ui_draw_soft_watercolor_strokes_strength_controls_how_strongly': {'attributes': {'name': 'ui_draw_soft_watercolor_strokes_strength_controls_how_strongly'},
                                                                                   'target': 'Зөөлөн усан будгийн мөр '
                                                                                             'зурна. «Хүч» нь өнгө '
                                                                                             'зургийн талбарт хэр '
                                                                                             'хүчтэй уусахыг '
                                                                                             'тохируулна.',
                                                                                   'type': 'string'},
                'ui_draw_with_the_selected_brush_tip_and_size': {'attributes': {'name': 'ui_draw_with_the_selected_brush_tip_and_size'},
                                                                 'target': 'Сонгосон бийрийн үзүүр ба хэмжээгээр '
                                                                           'зурна.',
                                                                 'type': 'string'},
                'ui_drop_at_a_highlighted_edge_right_top_aligned': {'attributes': {'name': 'ui_drop_at_a_highlighted_edge_right_top_aligned'},
                                                                    'target': 'Тодруулсан ирмэг дээр тавина: баруун '
                                                                              'талд бол дээд ирмэг, доод талд бол зүүн '
                                                                              'ирмэг таарна.',
                                                                    'type': 'string'},
                'ui_each_px_px_percent_is_relative_to_the': {'attributes': {'name': 'ui_each_px_px_percent_is_relative_to_the'},
                                                             'target': '%1$s бүр: %2$s px\\n%3$s: %4$s–%5$s px\\nХувь '
                                                                       'нь одоогийн хамгийн их %6$s буюу %7$s px-д '
                                                                       'харьцуулагдана. Байрлуулсан зургууд зай '
                                                                       'гаргахын тулд дахин байрлана.',
                                                             'type': 'string'},
                'ui_edit_in_paint': {'attributes': {'name': 'ui_edit_in_paint'},
                                     'target': 'Paint-д засах',
                                     'type': 'string'},
                'ui_edit_palette23': {'attributes': {'name': 'ui_edit_palette23'},
                                      'target': 'Өнгөний самбар засах',
                                      'type': 'string'},
                'ui_empty_palette26': {'attributes': {'name': 'ui_empty_palette26'},
                                       'target': 'Өнгөний самбарын хоосон нүд %1$d — өнгө нэмэх',
                                       'type': 'string'},
                'ui_enable_android_s_files_or_documents_app_then': {'attributes': {'name': 'ui_enable_android_s_files_or_documents_app_then'},
                                                                    'target': 'Android-ын Files эсвэл Documents аппыг '
                                                                              'идэвхжүүлээд дахин оролдоно уу.',
                                                                    'type': 'string'},
                'ui_enable_cursor_drawing': {'attributes': {'name': 'ui_enable_cursor_drawing'},
                                             'target': 'Курсороор зурахыг идэвхжүүлэх',
                                             'type': 'string'},
                'ui_estimated_memory_current_working_budget': {'attributes': {'name': 'ui_estimated_memory_current_working_budget'},
                                                               'target': 'Тооцоолсон санах ой: %1$s\\nОдоогийн ажлын '
                                                                         'хязгаар: %2$s\\n',
                                                               'type': 'string'},
                'ui_estimates_include_the_current_canvas_and_clipboard_sampled': {'attributes': {'name': 'ui_estimates_include_the_current_canvas_and_clipboard_sampled'},
                                                                                  'target': 'Тооцоонд одоогийн зургийн '
                                                                                            'талбар, санах ойд хуулсан '
                                                                                            'зураг, дээжлэн тайлах '
                                                                                            'болон засварлах буфер '
                                                                                            'орно. Бодит хэрэглээ өөр '
                                                                                            'байж болно. Жижиг хуулбар '
                                                                                            'нь нарийвчлал алддаг. '
                                                                                            'Импорт хийхдээ сонгосон '
                                                                                            'тунгалаг бус дэвсгэрийг '
                                                                                            'хэрэглэнэ; эх файл '
                                                                                            'өөрчлөгдөхгүй.',
                                                                                  'type': 'string'},
                'ui_export_this_version_s_source_code': {'attributes': {'name': 'ui_export_this_version_s_source_code'},
                                                         'target': 'Энэ хувилбарын эх кодыг экспортлох…',
                                                         'type': 'string'},
                'ui_filename_a_z': {'attributes': {'name': 'ui_filename_a_z'},
                                    'target': 'Файлын нэр A–Z',
                                    'type': 'string'},
                'ui_filename_z_a': {'attributes': {'name': 'ui_filename_z_a'},
                                    'target': 'Файлын нэр Z–A',
                                    'type': 'string'},
                'ui_fill_line': {'attributes': {'name': 'ui_fill_line'},
                                 'target': 'Дүүргэлт + шугам',
                                 'type': 'string'},
                'ui_fill_text_box_with_bg_colour': {'attributes': {'name': 'ui_fill_text_box_with_bg_colour'},
                                                    'target': 'Текстийн хайрцгийг BG өнгөөр дүүргэх',
                                                    'type': 'string'},
                'ui_finish_curve': {'attributes': {'name': 'ui_finish_curve'},
                                    'target': 'Муруйг дуусгах',
                                    'type': 'string'},
                'ui_finish_polygon': {'attributes': {'name': 'ui_finish_polygon'},
                                      'target': 'Олон өнцөгтийг дуусгах',
                                      'type': 'string'},
                'ui_fits_the_current_budget': {'attributes': {'name': 'ui_fits_the_current_budget'},
                                               'target': 'Одоогийн хязгаарт багтана.',
                                               'type': 'string'},
                'ui_font_licences': {'attributes': {'name': 'ui_font_licences'},
                                     'target': 'Фонтын лицензүүд',
                                     'type': 'string'},
                'ui_fullscreen33': {'attributes': {'name': 'ui_fullscreen33'},
                                    'target': 'Бүтэн дэлгэц',
                                    'type': 'string'},
                'ui_gallery_artwork_catrobat_and_its_credited_creators_cc': {'attributes': {'name': 'ui_gallery_artwork_catrobat_and_its_credited_creators_cc'},
                                                                             'target': 'Галерейн бүтээл: Catrobat '
                                                                                       'болон талархлын мэдээлэлд нэр '
                                                                                       'дурдсан бүтээгчид. Эх сурвалж '
                                                                                       'өөр нөхцөл заагаагүй бол CC '
                                                                                       'BY-SA 4.0. Өөрчилсөн бүтээл '
                                                                                       'хуваалцахдаа эх бүтээлийн '
                                                                                       'талархлыг хадгалж, хийсэн '
                                                                                       'өөрчлөлтөө тайлбарлана '
                                                                                       'уу.\\n\\n',
                                                                             'type': 'string'},
                'ui_gallery_back34': {'attributes': {'name': 'ui_gallery_back34'}, 'target': 'Буцах', 'type': 'string'},
                'ui_gallery_image': {'attributes': {'name': 'ui_gallery_image'},
                                     'target': 'Галерейн зураг',
                                     'type': 'string'},
                'ui_gallery_unsupported34': {'attributes': {'name': 'ui_gallery_unsupported34'},
                                             'target': 'Энэ зураг сонгосон зургийн эх сурвалжийн хүрээнээс гадуур '
                                                       'байна.',
                                             'type': 'string'},
                'ui_gimp_translations31': {'attributes': {'name': 'ui_gimp_translations31'},
                                           'target': 'Орчуулгын талархал ба лицензүүд',
                                           'type': 'string'},
                'ui_give_all_images_the_same_each_image_keeps': {'attributes': {'name': 'ui_give_all_images_the_same_each_image_keeps'},
                                                                 'target': 'Бүх %1$s зургийн %2$s-ийг ижил болгоно. '
                                                                           'Зураг бүр өөрийн харьцааг хадгална. Эх '
                                                                           'файлууд болон тайралтын тохиргоо '
                                                                           'өөрчлөгдөхгүй.',
                                                                 'type': 'string'},
                'ui_gnu_affero_general_public_license': {'attributes': {'name': 'ui_gnu_affero_general_public_license'},
                                                         'target': 'GNU Affero General Public License',
                                                         'type': 'string'},
                'ui_gnu_agpl_licence': {'attributes': {'name': 'ui_gnu_agpl_licence'},
                                        'target': 'GNU AGPL лиценз',
                                        'type': 'string'},
                'ui_gold': {'attributes': {'name': 'ui_gold'}, 'target': 'Алтлаг', 'type': 'string'},
                'ui_heic_avif_codec_licences': {'attributes': {'name': 'ui_heic_avif_codec_licences'},
                                                'target': 'HEIC ба AVIF кодекын лицензүүд',
                                                'type': 'string'},
                'ui_help23': {'attributes': {'name': 'ui_help23'},
                              'target': 'Тухайн удирдлагыг харахын тулд таб сонгоно. «Харах» нь «Шилжүүлэх»-ээс '
                                        'эхэлнэ; «Зурах» дотор «Зурах», «Сонголт», «Оруулах» байна. «Шилжүүлэх» нь '
                                        'зурахгүйгээр харагдацыг хөдөлгөнө; хоёр хуруугаар чимхэж томруулна. Табын '
                                        'хажуугийн сум самбарыг хумьж/дэлгэнэ. Бүх хэрэгсэл нэртэй. «Засах» нь '
                                        'сонголт, зургийн хүрээ, хэмжээс эсвэл зургийг өөрчилнө. «Өнгө» нь үндсэн '
                                        'болон дэвсгэр өнгийг сонгоно; «Өнгө солих» нь хоёрыг сольж, «Хар, цагаан '
                                        'болгох» нь анхны утгад буцаана. Өнгө сонгогч сонголтыг шууд урьдчилан '
                                        'харуулна. «Өнгийг хэрэглэх» батална; «Цуцлах» нь өмнөх өнгийг сэргээнэ. «Өнгө '
                                        'нэмэх» эсвэл хоосон хадгалсан нүдийг товшиж өнгө сонгон хадгална. Хадгалсан '
                                        'өнгийг удаан дарж засах эсвэл устгана. «Нарийвчилсан» нь «Хар, цагаан '
                                        'болгох»-ын хажууд дэлгэрэнгүй засварлагч нээнэ. Пикселийн тор зураг-пикселийн '
                                        'шугамтай; курсороор зурахад томруулалтын хажууд x/y координат шууд харагдана. '
                                        '«Өөрөөр хадгалах» нь зургийн формат, шахалтын тохиргоо, байршлыг сонгоно; '
                                        '«Хадгалах» нь тэр тохиргоо, байршлыг дахин ашиглана. «Экспортлох…» нь ICO, '
                                        'ASCII арт эсвэл Base64 текст үүсгэх боловч зургийг хадгалсан гэж '
                                        'тэмдэглэхгүй. «Хадгалж хуваалцах» нь хуулбар хадгалаад Android-ын хуваалцах '
                                        'цонхыг нээнэ; одоогийн «Хадгалах» байршлыг хэвээр үлдээнэ. Зурах > Оруулах > '
                                        'Бусад зураг хэсэгт төхөөрөмжийн файл, Catrobat, Irasutoya, Openclipart, '
                                        '«Wikimedia Commons · Хоосон газрын зураг…» байна. Оруулсан зураг сонгогдсон '
                                        'хэвээр үлдэж, зургийн талбараас гадуур байсан ч бариул нь харагдана. «Зургийг '
                                        'талбарт багтаах» нь байрлуулалтын хэмжээг өөрчилнө; «Анхны хэмжээ» нь эх '
                                        'хэмжээсийг сэргээнэ. Аппыг дахин нээхэд автоматаар хадгалах нь ноорог болон '
                                        'буцаах/дахин хийх хоёр түүхийг сэргээнэ. «Файл» дотор мөн зураг эвлүүлэх, '
                                        'Хэрэглэх заавар, Тухай, лиценз ба талархал байна. «Текст оруулах» нь хэвтээ '
                                        'болон босоо бичлэгийг дэмжинэ.',
                              'type': 'string'},
                'ui_hide_pixel_grid_800': {'attributes': {'formatted': 'false', 'name': 'ui_hide_pixel_grid_800'},
                                           'target': 'Пикселийн торыг нуух (800%+)',
                                           'type': 'string'},
                'ui_hold_a_thumbnail_and_drag_it_here_or': {'attributes': {'name': 'ui_hold_a_thumbnail_and_drag_it_here_or'},
                                                            'target': 'Өнгөц зургийг удаан дарж энд чирнэ, эсвэл '
                                                                      'товшоод ажлын талбарыг товшино.',
                                                            'type': 'string'},
                'ui_hold_or_drag_to_spray_colour': {'attributes': {'name': 'ui_hold_or_drag_to_spray_colour'},
                                                    'target': 'Өнгө цацахын тулд удаан дарах эсвэл чирнэ.',
                                                    'type': 'string'},
                'ui_honeycomb': {'attributes': {'name': 'ui_honeycomb'}, 'target': 'Зөгийн үүр', 'type': 'string'},
                'ui_honeycomb_colour_06x': {'attributes': {'name': 'ui_honeycomb_colour_06x'},
                                            'target': 'Зөгийн үүрний өнгө #%1$06X',
                                            'type': 'string'},
                'ui_honeycomb_colour_swatches_with_a_greyscale_row': {'attributes': {'name': 'ui_honeycomb_colour_swatches_with_a_greyscale_row'},
                                                                      'target': 'Саарал шатлалын мөртэй зөгийн үүр '
                                                                                'хэлбэрийн өнгийн дээжүүд',
                                                                      'type': 'string'},
                'ui_horizontal23': {'attributes': {'name': 'ui_horizontal23'}, 'target': 'Хэвтээ', 'type': 'string'},
                'ui_how_to_use': {'attributes': {'name': 'ui_how_to_use'},
                                  'target': 'Хэрэглэх заавар',
                                  'type': 'string'},
                'ui_hue_and_saturation_spectrum_lightness_slider_on_the': {'attributes': {'name': 'ui_hue_and_saturation_spectrum_lightness_slider_on_the'},
                                                                           'target': 'Өнгөний ая ба ханалтын спектр; '
                                                                                     'баруун талд гэрэлтүүлгийн '
                                                                                     'гулсуур',
                                                                           'type': 'string'},
                'ui_hue_and_saturation_wheel_value_slider_on_the': {'attributes': {'name': 'ui_hue_and_saturation_wheel_value_slider_on_the'},
                                                                    'target': 'Өнгөний ая ба ханалтын дугуй; баруун '
                                                                              'талд утгын гулсуур',
                                                                    'type': 'string'},
                'ui_icon_licences': {'attributes': {'name': 'ui_icon_licences'},
                                     'target': 'Дүрсний лицензүүд',
                                     'type': 'string'},
                'ui_icon_licences_kde_breeze': {'attributes': {'name': 'ui_icon_licences_kde_breeze'},
                                                'target': 'Дүрсний лицензүүд — KDE Breeze',
                                                'type': 'string'},
                'ui_icons_artwork': {'attributes': {'name': 'ui_icons_artwork'},
                                     'target': 'Дүрс ба зураглал',
                                     'type': 'string'},
                'ui_icons_fonts_artwork_credits': {'attributes': {'name': 'ui_icons_fonts_artwork_credits'},
                                                   'target': 'Дүрс, фонт ба зураглалын талархал',
                                                   'type': 'string'},
                'ui_image_assembly_workspace_drag_placed_images_or_drop': {'attributes': {'name': 'ui_image_assembly_workspace_drag_placed_images_or_drop'},
                                                                           'target': 'Зураг эвлүүлэх ажлын талбар. '
                                                                                     'Байрлуулсан зургуудыг чирэх '
                                                                                     'эсвэл өнгөц зургийг баруун/доод '
                                                                                     'бай дээр тавьж наалдуулна. Хоёр '
                                                                                     'хуруугаар чимхэж томруулна; '
                                                                                     'хоосон зайг чирж харагдацыг '
                                                                                     'шилжүүлнэ.',
                                                                           'type': 'string'},
                'ui_image_codec_licences': {'attributes': {'name': 'ui_image_codec_licences'},
                                            'target': 'Зургийн кодекын лицензүүд',
                                            'type': 'string'},
                'ui_image_credits': {'attributes': {'name': 'ui_image_credits'},
                                     'target': 'Зургийн талархал',
                                     'type': 'string'},
                'ui_image_placed_drag_it_to_move_or_hold': {'attributes': {'name': 'ui_image_placed_drag_it_to_move_or_hold'},
                                                            'target': 'Зургийг байрлууллаа. Зөөхийн тулд чирнэ, эсвэл '
                                                                      'өөр өнгөц зургийг удаан дарж чирнэ.',
                                                            'type': 'string'},
                'ui_image_thumbnails_and_filenames_scroll_horizontally_for_more': {'attributes': {'name': 'ui_image_thumbnails_and_filenames_scroll_horizontally_for_more'},
                                                                                   'target': 'Зургийн өнгөц зураг ба '
                                                                                             'файлын нэрс. Илүүг '
                                                                                             'харахын тулд хэвтээгээр '
                                                                                             'гүйлгэнэ.',
                                                                                   'type': 'string'},
                'ui_insert_gallery_image': {'attributes': {'name': 'ui_insert_gallery_image'},
                                            'target': 'Галерейн зураг оруулах уу?',
                                            'type': 'string'},
                'ui_invalid_image_attachments': {'attributes': {'name': 'ui_invalid_image_attachments'},
                                                 'target': 'Зургийн холболтын өгөгдөл буруу.',
                                                 'type': 'string'},
                'ui_irasutoya_credit34': {'attributes': {'name': 'ui_irasutoya_credit34'},
                                          'target': 'Зохиогчийн эрх бүтээгчид хадгалагдана. Хэрэглээ Irasutoya-гийн '
                                                    'нөхцөлд захирагдана; энэ нь Creative Commons лиценз биш.',
                                          'type': 'string'},
                'ui_irasutoya_help34': {'attributes': {'name': 'ui_irasutoya_help34'},
                                        'target': 'Бүтээлийн хуудсыг нээгээд «Зургийг ашиглах»-ыг товшино. Англи эсвэл '
                                                  'япон хэлээр хайж болно; бүтээлийн нэр ба сайтын текст япон хэлээр '
                                                  'хэвээр байна. Үнэгүй хэрэглээнд Irasutoya-гийн нөхцөл үйлчилнэ: '
                                                  'арилжааны загварт 21 ба түүнээс олон материал ашиглавал төлбөр '
                                                  'шаардлагатай. Тусгай хамтын ажиллагааны материал өөр нөхцөлтэй байж '
                                                  'болно. Эх хуудас ба талархал Файл → Тухай, лиценз ба талархал → '
                                                  'Зургийн талархал хэсэгт хадгалагдана.',
                                        'type': 'string'},
                'ui_jpeg_xl_codec_licences': {'attributes': {'name': 'ui_jpeg_xl_codec_licences'},
                                              'target': 'JPEG XL кодекын лицензүүд',
                                              'type': 'string'},
                'ui_largest': {'attributes': {'name': 'ui_largest'}, 'target': 'Хамгийн их', 'type': 'string'},
                'ui_lossless_jpeg_xl': {'attributes': {'name': 'ui_lossless_jpeg_xl'},
                                        'target': 'Алдагдалгүй JPEG XL',
                                        'type': 'string'},
                'ui_magnified_preview': {'attributes': {'name': 'ui_magnified_preview'},
                                         'target': 'Томруулсан урьдчилсан харагдац…',
                                         'type': 'string'},
                'ui_magnified_preview_ea9209': {'attributes': {'name': 'ui_magnified_preview_ea9209'},
                                                'target': 'Томруулсан урьдчилсан харагдац',
                                                'type': 'string'},
                'ui_magnifier33': {'attributes': {'name': 'ui_magnifier33'},
                                   'target': 'Томруулдаг шил',
                                   'type': 'string'},
                'ui_modified_newest_first': {'attributes': {'name': 'ui_modified_newest_first'},
                                             'target': 'Өөрчлөгдсөн: шинээрээ эхэнд',
                                             'type': 'string'},
                'ui_modified_oldest_first': {'attributes': {'name': 'ui_modified_oldest_first'},
                                             'target': 'Өөрчлөгдсөн: хуучнаараа эхэнд',
                                             'type': 'string'},
                'ui_monospace': {'attributes': {'name': 'ui_monospace'}, 'target': 'Ижил өргөнтэй', 'type': 'string'},
                'ui_no_attachment_fits_within_the_current_coordinate_range': {'attributes': {'name': 'ui_no_attachment_fits_within_the_current_coordinate_range'},
                                                                              'target': 'Одоогийн координатын мужид '
                                                                                        'багтах холболтын байрлал '
                                                                                        'алга. Жижиг зургийн хэмжээ '
                                                                                        'хэрэглэнэ үү.',
                                                                              'type': 'string'},
                'ui_no_gallery_images_have_been_inserted': {'attributes': {'name': 'ui_no_gallery_images_have_been_inserted'},
                                                            'target': 'Зургийн эх сурвалжийн текст байхгүй байна.',
                                                            'type': 'string'},
                'ui_normalize_height_info': {'attributes': {'name': 'ui_normalize_height_info'},
                                             'target': 'Зураг бүрийн өндөр: %1$d px\\nӨргөн: %2$d–%3$d px\\nХувийг '
                                                       'одоогийн хамгийн их өндөр болох %4$d px-ээс тооцно. '
                                                       'Байрлуулсан зургууд зай гаргахын тулд дахин байрлана.',
                                             'type': 'string'},
                'ui_normalize_height_input_percent': {'attributes': {'name': 'ui_normalize_height_input_percent'},
                                                      'target': 'Ижил өндөр, %1$d px-ээс тооцсон хувиар',
                                                      'type': 'string'},
                'ui_normalize_height_intro': {'attributes': {'name': 'ui_normalize_height_intro'},
                                              'target': 'Бүх зургийн өндрийг ижил болгоно. Зургийн тоо: %1$d. Зураг '
                                                        'бүр өөрийн өргөн ба өндрийн харьцааг хадгална. Эх файлууд '
                                                        'болон тайралтын тохиргоо өөрчлөгдөхгүй.',
                                              'type': 'string'},
                'ui_normalize_width_info': {'attributes': {'name': 'ui_normalize_width_info'},
                                            'target': 'Зураг бүрийн өргөн: %1$d px\\nӨндөр: %2$d–%3$d px\\nХувийг '
                                                      'одоогийн хамгийн их өргөн болох %4$d px-ээс тооцно. Байрлуулсан '
                                                      'зургууд зай гаргахын тулд дахин байрлана.',
                                            'type': 'string'},
                'ui_normalize_width_input_percent': {'attributes': {'name': 'ui_normalize_width_input_percent'},
                                                     'target': 'Ижил өргөн, %1$d px-ээс тооцсон хувиар',
                                                     'type': 'string'},
                'ui_normalize_width_intro': {'attributes': {'name': 'ui_normalize_width_intro'},
                                             'target': 'Бүх зургийн өргөнийг ижил болгоно. Зургийн тоо: %1$d. Зураг '
                                                       'бүр өөрийн өргөн ба өндрийн харьцааг хадгална. Эх файлууд '
                                                       'болон тайралтын тохиргоо өөрчлөгдөхгүй.',
                                             'type': 'string'},
                'ui_not_enough_memory_to_inspect_the_gallery_image': {'attributes': {'name': 'ui_not_enough_memory_to_inspect_the_gallery_image'},
                                                                      'target': 'Галерейн зургийг шалгахад санах ой '
                                                                                'хүрэлцэхгүй.',
                                                                      'type': 'string'},
                'ui_not_placed': {'attributes': {'name': 'ui_not_placed'}, 'target': 'Байрлуулаагүй', 'type': 'string'},
                'ui_open_artwork34': {'attributes': {'name': 'ui_open_artwork34'},
                                      'target': 'Эхлээд бүтээлийн хуудсыг нээгээд «Зургийг ашиглах»-ыг товшино.',
                                      'type': 'string'},
                'ui_open_source_credits_and_notices': {'attributes': {'name': 'ui_open_source_credits_and_notices'},
                                                       'target': 'Нээлттэй эхийн талархал ба мэдэгдлүүд',
                                                       'type': 'string'},
                'ui_openclipart_help34': {'attributes': {'name': 'ui_openclipart_help34'},
                                          'target': 'Бүтээлийн хуудсыг нээгээд Large PNG таталтын хажуугийн «Зургийг '
                                                    'ашиглах»-ыг товшино. Openclipart бүтээлээ CC0 лицензээр '
                                                    'нийтэлдэг. Эх хуудас ба лиценз Файл → Тухай, лиценз ба талархал → '
                                                    'Зургийн талархал хэсэгт хадгалагдана.',
                                          'type': 'string'},
                'ui_original_decoded_image_rgba_4_bytes_pixel_estimated': {'attributes': {'name': 'ui_original_decoded_image_rgba_4_bytes_pixel_estimated'},
                                                                           'target': 'Анхны зураг: %1$s\\nТайлсан '
                                                                                     'зураг: %2$s (RGBA, пиксел бүрт 4 '
                                                                                     'байт)\\nХэмжээ өөрчлөхгүй үеийн '
                                                                                     'засварлах санах ойн тооцоо: %3$s',
                                                                           'type': 'string'},
                'ui_other_terms': {'attributes': {'name': 'ui_other_terms'},
                                   'target': 'Бусад нөхцөл',
                                   'type': 'string'},
                'ui_pale_violet': {'attributes': {'name': 'ui_pale_violet'},
                                   'target': 'Цайвар ягаан-хөх',
                                   'type': 'string'},
                'ui_pencil_crisp_adjustable_strokes': {'attributes': {'name': 'ui_pencil_crisp_adjustable_strokes'},
                                                       'target': 'Харандаа сонгосон ямар ч өргөнд тод ирмэгийг '
                                                                 'хадгална.',
                                                       'type': 'string'},
                'ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing': {'attributes': {'name': 'ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing'},
                                                                           'target': 'Харандаа сонгосон ямар ч өргөнд '
                                                                                     'тод ирмэгийг хадгална.',
                                                                           'type': 'string'},
                'ui_percent_of_pixels': {'attributes': {'name': 'ui_percent_of_pixels'},
                                         'target': '%1$s пикселийн хувь',
                                         'type': 'string'},
                'ui_pinch_to_zoom_drag_to_pan': {'attributes': {'name': 'ui_pinch_to_zoom_drag_to_pan'},
                                                 'target': 'Чимхэж томруулна. Чирж шилжүүлнэ.',
                                                 'type': 'string'},
                'ui_pixel_grid33': {'attributes': {'name': 'ui_pixel_grid33'},
                                    'target': 'Пикселийн тор',
                                    'type': 'string'},
                'ui_pixel_grid_help33': {'attributes': {'formatted': 'false', 'name': 'ui_pixel_grid_help33'},
                                         'target': '800% болон түүнээс их томруулалт дээр пикселийн тор харагдана. '
                                                   'Шугамууд байрлалыг зургийн пикселээр харуулна.',
                                         'type': 'string'},
                'ui_place_at_least_one_image_in_the_workspace': {'attributes': {'name': 'ui_place_at_least_one_image_in_the_workspace'},
                                                                 'target': 'Эхлээд ажлын талбарт дор хаяж нэг зураг '
                                                                           'байрлуулна уу.',
                                                                 'type': 'string'},
                'ui_placed': {'attributes': {'name': 'ui_placed'}, 'target': 'Байрлуулсан', 'type': 'string'},
                'ui_preview_memory_error': {'attributes': {'name': 'ui_preview_memory_error'},
                                            'target': '%1$s: урьдчилсан харагдацад санах ой хүрэлцэхгүй.',
                                            'type': 'string'},
                'ui_px_drag_an_image_to_move_hold_a': {'attributes': {'name': 'ui_px_drag_an_image_to_move_hold_a'},
                                                       'target': '%1$s × %2$s px · зургийг чирж зөөнө; өнгөц зургийг '
                                                                 'удаан дарж нэмнэ.',
                                                       'type': 'string'},
                'ui_radius_px': {'attributes': {'name': 'ui_radius_px'}, 'target': 'Радиус (px)', 'type': 'string'},
                'ui_recent_colour_d_06x_tap_foreground_hold_background': {'attributes': {'name': 'ui_recent_colour_d_06x_tap_foreground_hold_background'},
                                                                          'target': 'Сүүлийн өнгө %1$d: #%2$06X. '
                                                                                    'Товшвол үндсэн, удаан дарвал '
                                                                                    'дэвсгэр өнгө.',
                                                                          'type': 'string'},
                'ui_recent_colour_empty': {'attributes': {'name': 'ui_recent_colour_empty'},
                                           'target': 'Сүүлийн өнгө %1$s: хоосон',
                                           'type': 'string'},
                'ui_remove_palette23': {'attributes': {'name': 'ui_remove_palette23'},
                                        'target': 'Өнгө хасах',
                                        'type': 'string'},
                'ui_rendering_images': {'attributes': {'name': 'ui_rendering_images'},
                                        'target': '%1$s / %2$s зургийг дүрсэлж байна…',
                                        'type': 'string'},
                'ui_replace_palette23': {'attributes': {'name': 'ui_replace_palette23'},
                                         'target': 'Өнгөний самбар дүүрсэн — солих өнгөө сонгоно уу',
                                         'type': 'string'},
                'ui_replace_with_active23': {'attributes': {'name': 'ui_replace_with_active23'},
                                             'target': 'Одоогийн өнгөөр солих',
                                             'type': 'string'},
                'ui_restore_original_sizes': {'attributes': {'name': 'ui_restore_original_sizes'},
                                              'target': 'Анхны хэмжээг сэргээх',
                                              'type': 'string'},
                'ui_right_arrow_expand': {'attributes': {'name': 'ui_right_arrow_expand'},
                                          'target': 'Баруун сум: дэлгэх',
                                          'type': 'string'},
                'ui_round': {'attributes': {'name': 'ui_round'}, 'target': 'Дугуй', 'type': 'string'},
                'ui_same': {'attributes': {'name': 'ui_same'}, 'target': 'Ижил %1$s', 'type': 'string'},
                'ui_same_height': {'attributes': {'name': 'ui_same_height'}, 'target': 'Ижил өндөр', 'type': 'string'},
                'ui_same_width': {'attributes': {'name': 'ui_same_width'}, 'target': 'Ижил өргөн', 'type': 'string'},
                'ui_sans_condensed': {'attributes': {'name': 'ui_sans_condensed'},
                                      'target': 'Нарийн санс-сериф',
                                      'type': 'string'},
                'ui_sans_light': {'attributes': {'name': 'ui_sans_light'},
                                  'target': 'Хөнгөн санс-сериф',
                                  'type': 'string'},
                'ui_sans_medium': {'attributes': {'name': 'ui_sans_medium'},
                                   'target': 'Дунд санс-сериф',
                                   'type': 'string'},
                'ui_sans_serif': {'attributes': {'name': 'ui_sans_serif'}, 'target': 'Санс-сериф', 'type': 'string'},
                'ui_sans_thin': {'attributes': {'name': 'ui_sans_thin'},
                                 'target': 'Нимгэн санс-сериф',
                                 'type': 'string'},
                'ui_save_as_avif': {'attributes': {'name': 'ui_save_as_avif'},
                                    'target': 'AVIF болгон хадгалах…',
                                    'type': 'string'},
                'ui_save_as_heic': {'attributes': {'name': 'ui_save_as_heic'},
                                    'target': 'HEIC болгон хадгалах…',
                                    'type': 'string'},
                'ui_save_as_webp': {'attributes': {'name': 'ui_save_as_webp'},
                                    'target': 'WebP болгон хадгалах…',
                                    'type': 'string'},
                'ui_saved_palette23': {'attributes': {'name': 'ui_saved_palette23'},
                                       'target': 'Хадгалсан өнгөний самбар',
                                       'type': 'string'},
                'ui_search34': {'attributes': {'name': 'ui_search34'}, 'target': 'Хайх', 'type': 'string'},
                'ui_search_english34': {'attributes': {'name': 'ui_search_english34'},
                                        'target': 'Англи эсвэл япон хэлээр хайх',
                                        'type': 'string'},
                'ui_serif': {'attributes': {'name': 'ui_serif'}, 'target': 'Сериф', 'type': 'string'},
                'ui_set_radius_px_then_drag_between_opposite_corners': {'attributes': {'name': 'ui_set_radius_px_then_drag_between_opposite_corners'},
                                                                        'target': '«Радиус (px)»-ыг тохируулж, дараа '
                                                                                  'нь эсрэг булангуудын хооронд чирнэ. '
                                                                                  'Радиус нь тэгш өнцөгтийн богино '
                                                                                  'талын хагасаас ихгүй байна.',
                                                                        'type': 'string'},
                'ui_show_pixel_grid_800': {'attributes': {'formatted': 'false', 'name': 'ui_show_pixel_grid_800'},
                                           'target': 'Пикселийн торыг харуулах (800%+)',
                                           'type': 'string'},
                'ui_shows_the_whole_assembly_image_and_output_sizes': {'attributes': {'name': 'ui_shows_the_whole_assembly_image_and_output_sizes'},
                                                                       'target': 'Эвлүүлгийг бүхэлд нь харуулна. '
                                                                                 'Зургийн болон гаралтын хэмжээ '
                                                                                 'өөрчлөгдөхгүй.',
                                                                       'type': 'string'},
                'ui_silver': {'attributes': {'name': 'ui_silver'}, 'target': 'Мөнгөлөг', 'type': 'string'},
                'ui_smallest': {'attributes': {'name': 'ui_smallest'}, 'target': 'Хамгийн бага', 'type': 'string'},
                'ui_smooth_freehand_strokes': {'attributes': {'name': 'ui_smooth_freehand_strokes'},
                                               'target': 'Чөлөөт гарын зураасыг жигдлэх',
                                               'type': 'string'},
                'ui_smooth_pixel_edges_anti_aliasing': {'attributes': {'name': 'ui_smooth_pixel_edges_anti_aliasing'},
                                                        'target': 'Пикселийн ирмэгийг жигдлэх (anti-aliasing)',
                                                        'type': 'string'},
                'ui_some_previews_could_not_be_decoded_you_can': {'attributes': {'name': 'ui_some_previews_could_not_be_decoded_you_can'},
                                                                  'target': 'Зарим урьдчилсан харагдацыг тайлж '
                                                                            'чадсангүй. Тэдгээр зургийг устгах эсвэл '
                                                                            'эвлүүлгийг хадгалж үзэж болно.',
                                                                  'type': 'string'},
                'ui_sort_images_by_filename_or_modification_time': {'attributes': {'name': 'ui_sort_images_by_filename_or_modification_time'},
                                                                    'target': 'Зургуудыг файлын нэр эсвэл өөрчлөгдсөн '
                                                                              'хугацаагаар эрэмбэлэх',
                                                                    'type': 'string'},
                'ui_sort_tray': {'attributes': {'name': 'ui_sort_tray'},
                                 'target': 'Тавиурыг эрэмбэлэх',
                                 'type': 'string'},
                'ui_source_code_exported_including_build_scripts_and_licence': {'attributes': {'name': 'ui_source_code_exported_including_build_scripts_and_licence'},
                                                                                'target': 'Эх кодыг build скрипт болон '
                                                                                          'лицензийн мэдэгдлүүдийн '
                                                                                          'хамт экспортоллоо.',
                                                                                'type': 'string'},
                'ui_spectrum': {'attributes': {'name': 'ui_spectrum'}, 'target': 'Спектр', 'type': 'string'},
                'ui_spray_radius_px': {'attributes': {'name': 'ui_spray_radius_px'},
                                       'target': 'Шүрших радиус (px)',
                                       'type': 'string'},
                'ui_square': {'attributes': {'name': 'ui_square'}, 'target': 'Дөрвөлжин', 'type': 'string'},
                'ui_strength': {'attributes': {'formatted': 'false', 'name': 'ui_strength'},
                                'target': 'Хүч (%)',
                                'type': 'string'},
                'ui_strikethrough': {'attributes': {'name': 'ui_strikethrough'},
                                     'target': 'Дундуур зураас',
                                     'type': 'string'},
                'ui_tap_a_pixel': {'attributes': {'name': 'ui_tap_a_pixel'},
                                   'target': 'Пиксел товших',
                                   'type': 'string'},
                'ui_tap_an_enclosed_area_adjust_tolerance_for_similar': {'attributes': {'name': 'ui_tap_an_enclosed_area_adjust_tolerance_for_similar'},
                                                                         'target': 'Хаалттай талбайг товшино. Төстэй '
                                                                                   'өнгийг хамруулахын тулд хүлцлийг '
                                                                                   'тохируулна.',
                                                                         'type': 'string'},
                'ui_tap_an_image_thumbnail_first': {'attributes': {'name': 'ui_tap_an_image_thumbnail_first'},
                                                    'target': 'Эхлээд зургийн өнгөц зургийг товшино уу.',
                                                    'type': 'string'},
                'ui_tap_the_canvas_to_place_text_and_choose': {'attributes': {'name': 'ui_tap_the_canvas_to_place_text_and_choose'},
                                                               'target': 'Текст байрлуулахын тулд зургийн талбарыг '
                                                                         'товшоод фонт, хэмжээг сонгоно.',
                                                               'type': 'string'},
                'ui_tap_the_image_to_sample_the_foreground_colour': {'attributes': {'name': 'ui_tap_the_image_to_sample_the_foreground_colour'},
                                                                     'target': 'Үндсэн өнгө авахын тулд зургийг '
                                                                               'товшино.',
                                                                     'type': 'string'},
                'ui_tap_vertices_then_double_tap_the_last_vertex': {'attributes': {'name': 'ui_tap_vertices_then_double_tap_the_last_vertex'},
                                                                    'target': 'Оройнуудыг товшоод, сүүлийн оройг '
                                                                              'давхар товшиж олон өнцөгтийг хаана. '
                                                                              '«Олон өнцөгтийг дуусгах» мөн ажиллана. '
                                                                              'Холбогдсон нээлттэй шугамууд зурахын '
                                                                              'тулд «Олон өнцөгтийг хаах»-ыг унтраана.',
                                                                    'type': 'string'},
                'ui_that_arrangement_overlaps_another_image_use_a_different': {'attributes': {'name': 'ui_that_arrangement_overlaps_another_image_use_a_different'},
                                                                               'target': 'Энэ байрлал өөр зурагтай '
                                                                                         'давхцаж байна. Өөр ирмэг '
                                                                                         'ашиглах эсвэл эхлээд '
                                                                                         'холбогдсон зургуудыг '
                                                                                         'байрлалаас гаргана уу.',
                                                                               'type': 'string'},
                'ui_the_arrow_on_the_left_directly_below_the': {'attributes': {'formatted': 'false',
                                                                               'name': 'ui_the_arrow_on_the_left_directly_below_the'},
                                                                'target': 'Хэрэгслийн мөрний яг доорх зүүн талын сум '
                                                                          'хэрэгслүүдийг хумьж эсвэл сэргээнэ: дээш '
                                                                          'сум нь хумьж, доош сум нь дэлгэнэ. Босоо '
                                                                          'дэлгэц дээр хэрэгслийн зурвас дээд мөрний '
                                                                          'доор хэвтээгээр байрлана; бусад хэрэгсэлд '
                                                                          'хүрэхийн тулд хажуу тийш шударна. Хэвтээ '
                                                                          'дэлгэц дээр зүүн талд босоогоор үлдэнэ. '
                                                                          '«Бийр» бүлэгт Харандаа, Бийр, Усан будаг, '
                                                                          'Шүршигч байна. «Сонголт» бүлэгт тэгш өнцөгт '
                                                                          'болон чөлөөт хэлбэрийн сонголтууд байна. '
                                                                          '«Оруулах» бүлэгт шугам, дүрс, текст байна. '
                                                                          'Ангиллыг товшиход босоо дэлгэц дээр '
                                                                          'зурвасын доор, хэвтээ дэлгэц дээр баруун '
                                                                          'талд хэрэгсэл ба тохиргоо нь дэлгэгдэнэ. '
                                                                          'Дахин товшвол хумьж, сумны чиглэл '
                                                                          'өөрчлөгдөнө. Ангилал бүр хамгийн сүүлд '
                                                                          'ашигласан хэрэгслээ санана. Нэмэлт тохиргоо '
                                                                          'болон засварын удирдлагыг харахын тулд '
                                                                          'хязгаартай сонголтын самбарыг гүйлгэнэ. Энэ '
                                                                          'байрлалын анхны нээлтэд хоёр самбар хоёулаа '
                                                                          'дэлгэгдсэн байна; дараагийн сонголтууд '
                                                                          'хадгалагдана. Хэвтээ дэлгэц дээр дээд '
                                                                          'удирдлагууд нэг мөрөнд багтаж, файлын нэр '
                                                                          'голд байрлана. Талархал ба нөхцөл: «Файл → '
                                                                          'Тухай, лиценз ба талархал».\\n\\nFG/BG '
                                                                          'өнгөний заалт зүүн доод талд, өнгөний '
                                                                          'самбарын хажууд тогтмол үлдэнэ. Өнгөний '
                                                                          'самбар яг баруун талдаа ижил мөрөнд '
                                                                          'нээгдэнэ. Сум нь самбарын баруун ирмэгт '
                                                                          'байна: зүүн сум хумьж, баруун сум дэлгэнэ. '
                                                                          'Хумьсан үед нэмэлт өнгийн дээжүүд л '
                                                                          'нуугдаж, FG/BG заалт хөдөлдөггүй. Өнгөний '
                                                                          'хайрцгийг товшиход ч самбар '
                                                                          'нээгдэж/хаагдана. Дээжийг товшвол үндсэн, '
                                                                          'удаан дарвал дэвсгэр өнгө болно. FG/BG '
                                                                          'цэсээр Өнгөний самбар, Зөгийн үүр, '
                                                                          'Нарийвчилсан хэсгийг нээнэ. «Нарийвчилсан» '
                                                                          'хэсэгт спектр, өнгөний дугуй, RGB, HSV, HSL '
                                                                          'болон зургаан оронт hex удирдлага байна. '
                                                                          'Хамгийн баруун дөрвөн нүд нь сүүлийн '
                                                                          'өнгөнүүдийг хадгална; товшвол үндсэн, удаан '
                                                                          'дарвал дэвсгэр өнгө. Өөрийн өнгөнүүд анх '
                                                                          'Цайвар ягаан-хөх #5B67FF, Алтлаг #FFD700, '
                                                                          'Мөнгөлөг #C0C0C0, Зэс #B87333 байна. Өөрийн '
                                                                          'өнгийн дээжийг удаан дарж солино. Үндсэн '
                                                                          'засварлагч тунгалаг бус өнгө ашиглана; '
                                                                          'тунгалаг хэсэгтэй импортын зургийг одоогийн '
                                                                          'BG өнгөн дээр байрлуулна. Эх файлууд '
                                                                          'өөрчлөгдөхгүй.\\n\\n«Шилжүүлэх» нь хуучин '
                                                                          'томруулдаг шилний хэрэгслийг орлоно: нэг '
                                                                          'хуруугаар чирж шилжүүлнэ, хоёр хуруугаар '
                                                                          'чимхэж томруулан шилжүүлнэ. «Шилжүүлэх»-ийг '
                                                                          'дахин эсвэл «Дахин зурах»-ыг товшиж зурах '
                                                                          'горимд буцна. Зургийн хэрэгсэл дээр ч хоёр '
                                                                          'хуруугаар мөр үлдээхгүй шилжүүлж болно. '
                                                                          'Баруун доод гулсуурт 100%-ийн төв шугам '
                                                                          'байна. Томруулах/жижигрүүлэх товч нь нэг '
                                                                          'алхам 100%-ийг давах бол эхлээд 100%-д '
                                                                          'зогсоно; дахин дарвал үргэлжилнэ. Хажуугийн '
                                                                          '«Багтаах» товч зургийн талбарыг харагдацад '
                                                                          'багтааж төвлөрүүлнэ. «Харах» цэсэнд 100% '
                                                                          'болон пикселийн тор мөн '
                                                                          'бий.\\n\\nАвтоматаар хадгалах нь засвар '
                                                                          'богино хугацаанд зогссоны дараа болон '
                                                                          'апп-аас гарахад одоогийн нооргийг бичнэ. '
                                                                          'Төлөвт «Нооргийг хадгаллаа» эсвэл '
                                                                          'автоматаар хадгалах алдаа харагдана. Дахин '
                                                                          'нээхэд ноорог, файлын нэр, хэрэгслийн '
                                                                          'тохиргоо, хөвөгч сонголт, дуусаагүй дүрсийг '
                                                                          'сэргээнэ. Автоматаар хадгалах нь хувийн '
                                                                          'ажлын ноорог хадгална. «Файл» нь PNG, чанар '
                                                                          'тохируулдаг JPEG ба HEIC, мөн алдагдалгүй '
                                                                          'эсвэл алдагдалтай JPEG XL, WebP, AVIF санал '
                                                                          'болгоно. «Хадгалж хуваалцах» нь Android-ын '
                                                                          'хуваалцах цонхыг нээхээс өмнө файлыг бичнэ. '
                                                                          '«Экспортлох» нь сонгосон байршилд хадгална; '
                                                                          'файлын нэрний од нь экспортолсон файлд '
                                                                          'хадгалаагүй өөрчлөлт байгааг илтгэнэ. '
                                                                          'Автоматаар хадгалах нь эх зургийг хэзээ ч '
                                                                          'дарж бичихгүй.\\n\\nСонголт: тэгш өнцөгт '
                                                                          'эсвэл чөлөөт хэлбэрийн хүрээ зурна. Дотор '
                                                                          'нь чирж зөөнө, дөрвөлжин булан эсвэл '
                                                                          'ирмэгийн дунд бариулаар хэмжээг өөрчилнө, '
                                                                          'дугуй «Эргүүлэх» бариулаар эргүүлнэ. '
                                                                          '«Харьцааг түгжих» анхнаасаа асаалттай; '
                                                                          'унтраавал өргөн ба өндрийг тусад нь '
                                                                          'сунгана. Ирмэгийн бариул сонгосон талын '
                                                                          'дагуу хэмжээг өөрчилнө. Чөлөөт сонголт нь '
                                                                          'эргүүлсний дараа болон автоматаар хадгалсны '
                                                                          'дараа ч хувиргалтын хүрээн дотор сонгосон '
                                                                          'хэлбэрээ хадгална. Хэмжээс ба өнцөг '
                                                                          'хажуугийн самбарт харагдана. «Сонголтыг '
                                                                          'батлах» нь үр дүнг нэг буцааж болох '
                                                                          'сонголтын засвар болгон хэрэглэнэ; '
                                                                          'автоматаар хадгалах нь дуусаагүй '
                                                                          'хувиргалтыг хадгална. Хуулах, Таслах, '
                                                                          'Сонголтоор тайрах нь хувиргасан зургийг '
                                                                          'ашиглана. «Бүгдийг сонгох» нь засварын '
                                                                          'дүрсний хоёр дахь мөрөнд байна, гадаад гар '
                                                                          'дээр Ctrl+A ажиллана. Таслах/Хуулах болон '
                                                                          'Буулгах/Бүгдийг сонгох нь «Хэрэглэх '
                                                                          'заавар»-ын доор хоёр мөр үүсгэнэ. Сонголтын '
                                                                          'маск сонгосон хэлбэрийг хадгална; баримт '
                                                                          'өөрөө тунгалаг бус хэвээр.\\n\\nЗургийн '
                                                                          'хүрээ: бариулыг дотогш чирж тайрна, гадагш '
                                                                          'чирж аль ч талд өргөтгөнө, дараа нь «Хүрээг '
                                                                          'хэрэглэх»-ийг дарна. Шинэ зайг BG өнгөөр '
                                                                          'дүүргэнэ; одоо байгаа пикселүүдийн хэмжээ '
                                                                          'өөрчлөгдөхгүй. «Цуцлах» ба «Буцаах» '
                                                                          'боломжтой. Зургийн хэмжээ, Зургийн талбарын '
                                                                          'хэмжээ, Шинэ зураг нь пиксел эсвэл хувиар '
                                                                          'утга авч, харьцааг түгжих '
                                                                          'сонголттой.\\n\\nМуруй: шугам зураад хоёр '
                                                                          'удаа чирж нугална. Олон өнцөгт: оройнуудыг '
                                                                          'товшоод сүүлийн оройг давхар товших эсвэл '
                                                                          '«Олон өнцөгтийг дуусгах»-ыг ашиглана. '
                                                                          'Холбогдсон нээлттэй шугам зурахын тулд '
                                                                          '«Олон өнцөгтийг хаах»-ыг унтраана. Дугуй '
                                                                          'булант тэгш өнцөгт: гулсуураар «Радиус '
                                                                          '(px)»-ыг тохируулна; радиус нь дүрсний '
                                                                          'богино талын хагасаас ихгүй. Текст: зургийн '
                                                                          'талбарыг товшоод өөрийн хэв маягаар '
                                                                          'харагдах фонтыг сонгон шууд урьдчилсан '
                                                                          'харагдацыг ашиглана. Хэмжээ, бүдүүн, налуу, '
                                                                          'доогуур зураас, дундуур зураас, '
                                                                          'зэрэгцүүлэлт, мөр хоорондын зай, BG өнгийн '
                                                                          'текстийн хайрцгийг тохируулж болно. Усан '
                                                                          'будаг нь «Бийр» ангилалд Бийр ба Шүршигчийн '
                                                                          'хажууд байна; илүү зөөлөн мөрийн хувьд '
                                                                          'хүчийг тохируулна. Харандаа, бийр, '
                                                                          'хэрэгслийн хэмжээний гулсуур 100 пиксел '
                                                                          'хүртэл. Харандаа 1 пикселээс эхэлж өөрийн '
                                                                          'өргөнийг санана. Нарийн утга оруулахын тулд '
                                                                          'харагдах тоог товшино. Зүрх, Од, Сум нь '
                                                                          'бусад дүрстэй адил хүрээ/дүүргэлтийн '
                                                                          'сонголттой. Харах > Курсороор зурах хэсэгт '
                                                                          'идэвхжүүлэх унтраалга, курсорын хэлбэр, '
                                                                          'томруулдаг шилний тохиргоо байна. Курсорыг '
                                                                          'байрлуулахын тулд чирээд, дэлгэц дээрх '
                                                                          'зурах товчийг товшиж, дараа нь шилжүүлж '
                                                                          'зурна. Дахин товшиж зогсооно. Бийр ба '
                                                                          'мөрийн тохиргоо Зурах > Зурах хэсэгт '
                                                                          'хэвээр. Харах > Томруулсан урьдчилсан '
                                                                          'харагдац нь курсор эсвэл зурах цэгийг '
                                                                          'тохируулж болох томруулалтаар үзүүлнэ. '
                                                                          '«Зурах тохиргоо» нь anti-aliasing болон мөр '
                                                                          'жигдлэх тохиргоотой. 11 нэмэлт фонт '
                                                                          'багтсан; «Фонтын лицензүүд» хэсэгт талархал '
                                                                          'ба бүрэн нөхцөл байна.\\n\\nФайл > Зураг '
                                                                          'нээх нь Android-ын сонгогчоор зургийн '
                                                                          'талбарыг солино. «Зурах → Оруулах → Бусад '
                                                                          'зураг» хэсэгт төхөөрөмжийн файл, Catrobat, '
                                                                          'Irasutoya, Openclipart байна. Төхөөрөмжөөс '
                                                                          'зураг сонгох эсвэл онлайн зургийн хуудсыг '
                                                                          'нээгээд «Зургийг ашиглах» товчийг товшиж '
                                                                          'зургийг хөвөгч сонголт болгон нэмнэ. Файл > '
                                                                          'Тухай, лиценз ба талархал > Зургийн '
                                                                          'талархал хэсэг эх холбоос ба лицензийн '
                                                                          'мэдэгдлийг хадгална. Төхөөрөмжийн санах ойн '
                                                                          'хязгаарт багтсан зураг анхны нягтаршилаар '
                                                                          'нээгдэнэ. Шаардлагатай үед хэмжээ сонгох '
                                                                          'цонх нь хэмжээс, пикселийн тоо, санах ойн '
                                                                          'тооцоог харуулж, Пиксел/Хувь болон харьцаа '
                                                                          'түгжих сонголт өгнө. Эх файл '
                                                                          'өөрчлөгдөхгүй.\\n\\n«Файл» > Зураг эвлүүлэх '
                                                                          'нь 20 хүртэл зурагтай тусдаа ажлын талбар '
                                                                          'нээнэ. Өнгөц зургуудыг файлын нэр эсвэл '
                                                                          'хугацаагаар эрэмбэлнэ. Нэг зураг тайрах '
                                                                          'эсвэл хэд хэдийг бөөнөөр тайрна. «Ижил '
                                                                          'өргөн / Ижил өндөр» нь харьцааг хадгалан '
                                                                          'бүх ачаалсан зургийн хэмжээг ижилсүүлнэ. '
                                                                          'Өнгөц зураг эсвэл байрлуулсан зургийг чирж '
                                                                          'залгана: баруун талд залгахад дээд '
                                                                          'ирмэгүүд, доод талд залгахад зүүн ирмэгүүд '
                                                                          'зэрэгцэнэ. «Байрлалаас гаргах» нь зөвхөн '
                                                                          'сонгосон байрлалыг арилгаж, завсрыг нөхнө. '
                                                                          '«Бүгдийг харуулах» нь зөвхөн харагдацын '
                                                                          'томруулалтыг өөрчилнө. «PNG хадгалах» нь '
                                                                          'эвлүүлгийг экспортолно; «Paint-д засах» нь '
                                                                          'үндсэн засварлагч руу буцааж болох засвар '
                                                                          'болгон шилжүүлнэ. Апп нэг тунгалаг бус '
                                                                          'зураг засварлагч ашиглана. «Зураг эвлүүлэх» '
                                                                          'нь тусдаа байрлуулалтын ажлын '
                                                                          'талбар.\\n\\n«Файл → Тухай, лиценз ба '
                                                                          'талархал» хэсэгт анхны зохиогчийн эрх, '
                                                                          'хөрөнгө/фонтын талархал, лицензийн бүрэн '
                                                                          'текст, энэ хувилбарын бүрэн эх код бий. '
                                                                          'Лицензийн текст нь тогтмол байрлах «Бүгдийг '
                                                                          'хуулах», «Бусад нөхцөл», «Дуусгах» товчоос '
                                                                          'тусдаа гүйлгэнэ.',
                                                                'type': 'string'},
                'ui_the_assembly_exceeds_android_s_coordinate_range': {'attributes': {'name': 'ui_the_assembly_exceeds_android_s_coordinate_range'},
                                                                       'target': 'Эвлүүлэг Android-ын координатын '
                                                                                 'мужаас хэтэрсэн.',
                                                                       'type': 'string'},
                'ui_the_assembly_needs_about_choose_a_smaller_output': {'attributes': {'name': 'ui_the_assembly_needs_about_choose_a_smaller_output'},
                                                                        'target': 'Эвлүүлэгт ойролцоогоор %1$s '
                                                                                  'хэрэгтэй. Жижиг гаралтын хэмжээ '
                                                                                  'сонгоно уу.',
                                                                        'type': 'string'},
                'ui_the_assembly_output_is_unavailable_reopen_image_assembly': {'attributes': {'name': 'ui_the_assembly_output_is_unavailable_reopen_image_assembly'},
                                                                                'target': 'Эвлүүлгийн гаралт боломжгүй '
                                                                                          'байна. «Зураг эвлүүлэх»-ийг '
                                                                                          'дахин нээгээд оролдоно уу.',
                                                                                'type': 'string'},
                'ui_the_attachment_image_is_missing': {'attributes': {'name': 'ui_the_attachment_image_is_missing'},
                                                       'target': 'Холбосон зураг алга.',
                                                       'type': 'string'},
                'ui_the_attachment_image_is_not_placed': {'attributes': {'name': 'ui_the_attachment_image_is_not_placed'},
                                                          'target': 'Холбосон зураг байрлуулаагүй.',
                                                          'type': 'string'},
                'ui_the_first_image_starts_at_the_top_left': {'attributes': {'name': 'ui_the_first_image_starts_at_the_top_left'},
                                                              'target': 'Эхний зураг зүүн дээд булангаас эхэлнэ.',
                                                              'type': 'string'},
                'ui_the_gallery_download_is_too_large': {'attributes': {'name': 'ui_the_gallery_download_is_too_large'},
                                                         'target': 'Галерейн таталт хэт том байна.',
                                                         'type': 'string'},
                'ui_the_gallery_image_is_unavailable': {'attributes': {'name': 'ui_the_gallery_image_is_unavailable'},
                                                        'target': 'Галерейн зураг боломжгүй байна.',
                                                        'type': 'string'},
                'ui_the_gallery_redirected_outside_its_supported_hosts': {'attributes': {'name': 'ui_the_gallery_redirected_outside_its_supported_hosts'},
                                                                          'target': 'Галерей зургийн дэмжигддэггүй URL '
                                                                                    'руу дахин чиглүүлсэн.',
                                                                          'type': 'string'},
                'ui_the_image_could_not_be_downloaded': {'attributes': {'name': 'ui_the_image_could_not_be_downloaded'},
                                                         'target': 'Зургийг татаж чадсангүй.',
                                                         'type': 'string'},
                'ui_the_images_cannot_fit_within_android_s_coordinate': {'attributes': {'name': 'ui_the_images_cannot_fit_within_android_s_coordinate'},
                                                                         'target': 'Зургууд Android-ын координатын '
                                                                                   'мужид багтахгүй. Жижиг зургийн '
                                                                                   'хэмжээ сонгоно уу.',
                                                                         'type': 'string'},
                'ui_the_normalized_image_dimensions_are_outside_android_s': {'attributes': {'name': 'ui_the_normalized_image_dimensions_are_outside_android_s'},
                                                                             'target': 'Ижилсүүлсэн зургийн хэмжээс '
                                                                                       'Android-ын мужийн гадна байна.',
                                                                             'type': 'string'},
                'ui_the_online_gallery_could_not_be_loaded_check': {'attributes': {'name': 'ui_the_online_gallery_could_not_be_loaded_check'},
                                                                    'target': 'Онлайн галерейг ачаалж чадсангүй. '
                                                                              'Холболтоо шалгаад дахин оролдоно уу.',
                                                                    'type': 'string'},
                'ui_third_party_notices': {'attributes': {'name': 'ui_third_party_notices'},
                                           'target': 'Гуравдагч талын мэдэгдлүүд',
                                           'type': 'string'},
                'ui_this_image_is_outside_the_supported_catrobat_gallery': {'attributes': {'name': 'ui_this_image_is_outside_the_supported_catrobat_gallery'},
                                                                            'target': 'Энэ зураг дэмжигдсэн Catrobat '
                                                                                      'галерейн хүрээнээс гадуур '
                                                                                      'байна.',
                                                                            'type': 'string'},
                'ui_time_unavailable': {'attributes': {'name': 'ui_time_unavailable'},
                                        'target': 'Хугацааны мэдээлэл байхгүй',
                                        'type': 'string'},
                'ui_toggle_toolbox': {'attributes': {'name': 'ui_toggle_toolbox'},
                                      'target': 'Багажны самбарыг нээх/хаах',
                                      'type': 'string'},
                'ui_too_many_gallery_redirects': {'attributes': {'name': 'ui_too_many_gallery_redirects'},
                                                  'target': 'Галерейн дахин чиглүүлэлт хэт олон байна.',
                                                  'type': 'string'},
                'ui_tool_option': {'attributes': {'name': 'ui_tool_option'},
                                   'target': 'Багажны сонголт',
                                   'type': 'string'},
                'ui_toolbox_and_tool_options_scroll_for_more': {'attributes': {'name': 'ui_toolbox_and_tool_options_scroll_for_more'},
                                                                'target': 'Багажны самбар ба багажны сонголтууд. Илүүг '
                                                                          'харахын тулд гүйлгэнэ.',
                                                                'type': 'string'},
                'ui_top23': {'attributes': {'name': 'ui_top23'}, 'target': 'Дээд талд зэрэгцүүлэх', 'type': 'string'},
                'ui_trim_from_the_original_edges_drag_the_handles': {'attributes': {'name': 'ui_trim_from_the_original_edges_drag_the_handles'},
                                                                     'target': 'Анхны ирмэгээс тайрна. Бариулыг чирэх '
                                                                               'эсвэл доор утга оруулна. Эх файлууд '
                                                                               'өөрчлөгдөхгүй.',
                                                                     'type': 'string'},
                'ui_unplace': {'attributes': {'name': 'ui_unplace'}, 'target': 'Байрлалаас гаргах', 'type': 'string'},
                'ui_vertical_hint23': {'attributes': {'name': 'ui_vertical_hint23'},
                                       'target': 'Шинэ мөр бүр шинэ багана эхлүүлнэ. Хажуу тийш эргэсэн үгс монгол '
                                                 'бичиг зэрэг холбогддог бичгийн холбоосыг хадгална. Босоо тэмдэгтүүд '
                                                 'нийлмэл тэмдэг болон emoji дарааллыг салгахгүй.',
                                       'type': 'string'},
                'ui_vertical_letters23': {'attributes': {'name': 'ui_vertical_letters23'},
                                          'target': 'Босоо текстийн үсэг',
                                          'type': 'string'},
                'ui_vertical_lr23': {'attributes': {'name': 'ui_vertical_lr23'},
                                     'target': 'Босоо, багана зүүнээс баруун',
                                     'type': 'string'},
                'ui_vertical_mixed23': {'attributes': {'name': 'ui_vertical_mixed23'},
                                        'target': 'Автомат · CJK босоо, үгс хажуу тийш',
                                        'type': 'string'},
                'ui_vertical_rl23': {'attributes': {'name': 'ui_vertical_rl23'},
                                     'target': 'Босоо, багана баруунаас зүүн',
                                     'type': 'string'},
                'ui_vertical_sideways23': {'attributes': {'name': 'ui_vertical_sideways23'},
                                           'target': 'Хажуу тийш · үгсийн холбоосыг хадгалах',
                                           'type': 'string'},
                'ui_vertical_upright23': {'attributes': {'name': 'ui_vertical_upright23'},
                                          'target': 'Босоо · тэмдэгт бүрээр',
                                          'type': 'string'},
                'ui_webp_codec_licences': {'attributes': {'name': 'ui_webp_codec_licences'},
                                           'target': 'WebP кодекын лицензүүд',
                                           'type': 'string'},
                'ui_wheel': {'attributes': {'name': 'ui_wheel'}, 'target': 'Өнгөний дугуй', 'type': 'string'},
                'ui_widths': {'attributes': {'name': 'ui_widths'}, 'target': 'Өргөнүүд', 'type': 'string'},
                'ui_you_can_add_more_images_select_fewer_files': {'attributes': {'name': 'ui_you_can_add_more_images_select_fewer_files'},
                                                                  'target': 'Та %1$s зураг нэмж болно. Цөөн файл '
                                                                            'сонгоно уу.',
                                                                  'type': 'string'}},
 'tok': {'ui_search34': {'attributes': {'name': 'ui_search34'}, 'target': '"o alasa"', 'type': 'string'}}}
ATTRIBUTE_EXCEPTIONS={'ary': {'ui_100': {'formatted': 'false', 'name': 'ui_100'},
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
 'mn-Cyrl-MN': {'ui_100': {'formatted': 'false', 'name': 'ui_100'},
                'ui_actual_size_100': {'formatted': 'false', 'name': 'ui_actual_size_100'},
                'ui_line_spacing': {'formatted': 'false', 'name': 'ui_line_spacing'},
                'ui_magnification': {'formatted': 'false', 'name': 'ui_magnification'},
                'ui_quality': {'formatted': 'false', 'name': 'ui_quality'},
                'ui_use_50_300': {'formatted': 'false', 'name': 'ui_use_50_300'}},
 'tok': {'ui_100': {'formatted': 'false', 'name': 'ui_100'},
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
WORDING_ONLY={'ary': {'string/formats22_derived_exported',
         'string/ui_1_px',
         'string/ui_actual_size_100',
         'string/ui_category_brush',
         'string/ui_collapse_colour_palette',
         'string/ui_discard',
         'string/ui_edit_background',
         'string/ui_edit_foreground',
         'string/ui_expand_colour_palette',
         'string/ui_fit_image',
         'string/ui_foreground_background_colour_palette',
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
         'string/ui_save_as',
         'string/ui_save_as_jpeg',
         'string/ui_save_as_jpeg_xl',
         'string/ui_save_as_png',
         'string/ui_show_editor_controls',
         'string/ui_swap_foreground_background',
         'string/ui_tool_categories',
         'string/ui_trim_expand_canvas_by_touch'},
 'mn-Cyrl-MN': {'string/formats22_derived_exported',
                'string/ui_1_px',
                'string/ui_actual_size_100',
                'string/ui_category_brush',
                'string/ui_collapse_colour_palette',
                'string/ui_discard',
                'string/ui_edit_background',
                'string/ui_edit_foreground',
                'string/ui_expand_colour_palette',
                'string/ui_fit_image',
                'string/ui_foreground_background_colour_palette',
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
                'string/ui_save_as',
                'string/ui_save_as_jpeg',
                'string/ui_save_as_jpeg_xl',
                'string/ui_save_as_png',
                'string/ui_show_editor_controls',
                'string/ui_swap_foreground_background',
                'string/ui_tool_categories',
                'string/ui_trim_expand_canvas_by_touch'},
 'tok': {'string/formats22_derived_exported',
         'string/ui_1_px',
         'string/ui_actual_size_100',
         'string/ui_category_brush',
         'string/ui_collapse_colour_palette',
         'string/ui_discard',
         'string/ui_edit_background',
         'string/ui_edit_foreground',
         'string/ui_expand_colour_palette',
         'string/ui_fit_image',
         'string/ui_foreground_background_colour_palette',
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
         'string/ui_save_as',
         'string/ui_save_as_jpeg',
         'string/ui_save_as_jpeg_xl',
         'string/ui_save_as_png',
         'string/ui_show_editor_controls',
         'string/ui_swap_foreground_background',
         'string/ui_tool_categories',
         'string/ui_trim_expand_canvas_by_touch'}}
UNCHANGED={'ary': set(),
 'mn-Cyrl-MN': {'colour_converter_unavailable',
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
                'language20_app_language',
                'language20_current',
                'language20_settings',
                'language20_translation_note',
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
                'ui_an_paint_image_assembly',
                'ui_an_paint_image_assembly_20_images_placed',
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
                'ui_clear_all',
                'ui_clear_image',
                'ui_codec_resize_memory_floor',
                'ui_collapse_colour_palette',
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
                'ui_discard',
                'ui_discard_changes23',
                'ui_done',
                'ui_draft_not_saved_yet',
                'ui_draft_pending',
                'ui_draft_restored',
                'ui_draft_saved',
                'ui_draw26',
                'ui_draw_again',
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
                'ui_fit',
                'ui_fit_entire_canvas_in_view',
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
                'ui_image_assembly',
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
                'ui_lock_aspect_ratio',
                'ui_lock_proportions',
                'ui_lossless_format',
                'ui_magnification',
                'ui_menu',
                'ui_menu_colours',
                'ui_menu_edit',
                'ui_menu_file',
                'ui_menu_help',
                'ui_menu_image',
                'ui_menu_view',
                'ui_navigate',
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
                'ui_save_and_share',
                'ui_save_and_share_41edb4',
                'ui_save_explanation23',
                'ui_save_png',
                'ui_save_your_changes',
                'ui_saved',
                'ui_scales_the_image_unlock_the_ratio_to_stretch',
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
                'ui_solid_fill',
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
 'tok': {'ui_ok', 'ui_save', 'ui_menu_edit'}}
EDIT_COUNTS={'ary': 348, 'mn-Cyrl-MN': 10, 'tok': 345}
PLURAL_QUANTITIES={'ary': {'other'}, 'mn-Cyrl-MN': {'other', 'one'}, 'tok': {'other'}}
DITHER_PAIRS={'ary': ('توزيع نقط ملوّنة',
         'صورة ثابتة، حتى لـ 256 لون. توزيع نقط ملوّنة كيخلّي الانتقال بين الألوان أنعم. ملفات GIF المتحركة كيتحلّو '
         'باللقطة اللولة ديالهم.'),
 'mn-Cyrl-MN': ('Өнгийг дизерлэх',
                'Хөдөлгөөнгүй зураг, 256 хүртэл өнгө. Дизерлэх нь өнгөний шилжилтийг жигд харагдуулна. Хөдөлгөөнт '
                'GIF-ийн эхний кадр нээгдэнэ.'),
 'tok': ('o pana e leko kule lili',
         'sitelen li tawa ala, li jo e kule 256 anu lili. pana pi leko kule lili li pona e ante kule. lipu GIF tawa la '
         'ilo li open e sitelen nanpa wan.')}

def priority_ids():
    return {k for t in json.loads((catalogues.DATA/'string-importance.json').read_text())['tiers'] if t['id']in('P0','P1')for k in t['keys']}
def newlines(value):
    return re.findall(r'(\\+)n',value)
def require_complete(root,key,source,target,attrs):
    found=root.findall(f"./{source['type']}[@name='{key}']")
    if len(found)!=1 or found[0].attrib!=attrs:raise ValueError('Exact typed identity/attributes differ')
    n=found[0]
    if (n.tail or '').strip():raise ValueError('Non-whitespace resource tail')
    if source['type']=='string':
        if list(n) or n.text!=target:raise ValueError('Full target differs')
        pairs=[(target,source['source'])]
    else:
        if (n.text or '').strip() or any((i.tail or '').strip()for i in n):raise ValueError('Non-whitespace plural container/tail')
        if any(i.tag!='item' or set(i.attrib)!={'quantity'} or list(i)for i in n):raise ValueError('Malformed plural')
        values={i.get('quantity'):i.text for i in n}
        if len(values)!=len(n) or values!=target:raise ValueError('Complete plural differs')
        pairs=[(v,source['source'].get(q,source['source']['other']))for q,v in values.items()]
    for target,english in pairs:
        if attrs.get('formatted')=='false':
            if target.count('%')!=english.count('%'):raise ValueError('Literal percent differs')
            continue
        if Counter(FULL_FORMAT_TOKEN.findall(target))!=Counter(FULL_FORMAT_TOKEN.findall(english)):raise ValueError('Full placeholder contract differs')
        if newlines(target)!=newlines(english):raise ValueError('Exact raw newline escape contract differs')
        if FULL_FORMAT_TOKEN.sub('',target).count('%')!=FULL_FORMAT_TOKEN.sub('',english).count('%'):raise ValueError('Literal percent differs')

def require_shape(data):
    require_fixture_binding(data)
    names={x.split('/',1)[1]for x in priority_ids()}
    if data.get('schema_version')!=1 or set(data.get('locales',{}))!=TAGS:raise ValueError('Schema/locale scope differs')
    if set(data.get('sources',{}))!=names|DEPENDENCIES:raise ValueError('Full source identity set differs')
    for tag,loc in data['locales'].items():
        expected=names-set(HOLDS[tag])|DEPENDENCIES
        if set(loc.get('accepted',{}))!=expected:raise ValueError('Full accepted identity set differs')
        for field,constant in [('priority_status',PRIORITY_STATUS),('predecessors',PREDECESSORS),('outside_review',OUTSIDE_REVIEW),('held',HOLDS),('target_attribute_exceptions',ATTRIBUTE_EXCEPTIONS)]:
            if loc.get(field)!=constant[tag]:raise ValueError('Exact '+field+' binding differs')
        if set(loc.get('wording_only',[]))!=WORDING_ONLY[tag]:raise ValueError('Context credit boundary differs')
        if set(loc.get('unchanged_accepted',[]))!=UNCHANGED[tag] or set(loc.get('changed',[]))!=expected-UNCHANGED[tag] or len(loc['changed'])!=EDIT_COUNTS[tag]:raise ValueError('Changed/retained partition differs')
        typed={data['sources'][k]['type']+'/'+k for k in expected}|{v['type']+'/'+k for k,v in OUTSIDE_REVIEW[tag].items()}|{v['type']+'/'+k for k,v in HOLDS[tag].items()if v is not None}
        if set(loc.get('catalogue_identities',[]))!=typed or len(loc['catalogue_identities'])!=len(typed):raise ValueError('Catalogue union differs')
        for key,value in loc['accepted'].items():
            if data['sources'][key]['type']=='string':
                if not isinstance(value,str) or not value:raise ValueError('Missing complete string')
                if value.startswith('@string/') and (tag,key,value)!=('mn-Cyrl-MN','ui_draw26','@string/ui_drawing23'):raise ValueError('Unexpected alias')
            elif not isinstance(value,dict) or set(value)!=PLURAL_QUANTITIES[tag] or not all(isinstance(v,str)and v for v in value.values()):raise ValueError('Complete plural quantity set differs')
    return data

def require_current(data,roots,english):
    require_shape(data)
    for key,source in data['sources'].items():require_complete(english,key,source,source['source'],source['attributes'])
    for tag,loc in data['locales'].items():
        root=roots[tag]
        if root.tag!='resources' or root.attrib or (root.text or '').strip():raise ValueError('Malformed catalogue root')
        successors={key:row for (locale,key),row in residual_rows().items() if locale==tag}
        identities=set(loc['catalogue_identities'])|{'string/'+key for key in successors}
        if len(root)!=len(identities) or {e.tag+'/'+e.get('name')for e in root}!=identities:raise ValueError('Actual exact catalogue differs')
        for key,target in loc['accepted'].items():
            if key in successors:
                row=successors[key]
                if row['previous_target']!=target or row['source']!=data['sources'][key]['source']:raise ValueError('Exact existing successor binding differs')
                require_residual_or_previous(root,tag,key,target)
                require_complete(root,key,data['sources'][key],row['target'],row['attributes'])
            else:require_complete(root,key,data['sources'][key],target,loc['target_attribute_exceptions'].get(key,{'name':key}))
        for key,previous in loc['held'].items():
            if previous is None:
                require_residual_or_previous(root,tag,key)
                if key in successors:require_complete(root,key,data['sources'][key],successors[key]['target'],successors[key]['attributes'])
            else:require_complete(root,key,{'type':previous['type'],'source':previous['target']},previous['target'],previous['attributes'])
        for key,row in loc['outside_review'].items():require_complete(root,key,{'type':row['type'],'source':row['target']},row['target'],row['attributes'])
    return data

class MoroccanArabicMongolianTokiPonaPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roots={t:ET.parse(catalogues.catalogue_paths()[t]).getroot()for t in TAGS};cls.english=ET.parse(catalogues.RES/'values/strings.xml').getroot();cls.data=require_current(fixture(NAME),cls.roots,cls.english)
    def test_complete_341_and_18_atomic_typed_scope(self):
        self.assertEqual(341,len(priority_ids()));self.assertEqual(18,len(DEPENDENCIES));require_current(self.data,self.roots,self.english)
    def test_all_accepted_fixture_and_catalogue_full_values_reject_corruption(self):
        for tag,loc in self.data['locales'].items():
            for key,value in loc['accepted'].items():
                for field in ('catalogue','fixture'):
                    src=self.data['sources'][key];attrs=loc['target_attribute_exceptions'].get(key,{'name':key})
                    root=deepcopy(self.roots[tag]);target=deepcopy(value)
                    if field=='fixture':
                        target=value+'X' if isinstance(value,str)else dict(value,other=value['other']+'X')
                    else:
                        n=root.find(f"./{src['type']}[@name='{key}']")
                        if isinstance(value,str):n.text=n.text[:-1]
                        else:n[0].text=n[0].text[:-1]
                    with self.subTest(tag=tag,key=key,field=field),self.assertRaises(ValueError):require_complete(root,key,src,target,attrs)
    def test_whitespace_outside_exact_string_and_plural_text_rejects_smuggling(self):
        for tag in TAGS:
            for mode in ('string-tail','plural-text','plural-child-tail','root-text','root-attribute'):
                roots=deepcopy(self.roots);root=roots[tag]
                if mode=='string-tail':root.find("./string[@name='ui_save']").tail='forged'
                elif mode=='plural-text':root.find("./plurals[@name='ui_crop_preview_images']").text='forged'
                elif mode=='plural-child-tail':root.find("./plurals[@name='ui_crop_preview_images']")[0].tail='forged'
                elif mode=='root-text':root.text='forged'
                else:root.set('formatted','false')
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_current(self.data,roots,self.english)
    def test_coordinated_fixture_catalogue_and_each_full_fixture_field_tamper_rejected(self):
        for tag in TAGS:
            data=deepcopy(self.data);roots=deepcopy(self.roots);key='ui_save'
            data['locales'][tag]['accepted'][key]+=' forged';roots[tag].find(f"./string[@name='{key}']").text=data['locales'][tag]['accepted'][key]
            with self.subTest(tag=tag),self.assertRaises(ValueError):require_current(data,roots,self.english)
            with patch('moroccan_arabic_mongolian_toki_pona_priority_expectations.fixture',return_value=data),self.assertRaises(ValueError):current_row(tag,key)
        def leaves(value,path=()):
            if isinstance(value,dict):
                for k,v in value.items():yield from leaves(v,path+(k,))
            elif isinstance(value,list):
                for i,v in enumerate(value):yield from leaves(v,path+(i,))
            else:yield path,value
        # Check all source, target, predecessor, attributes, partitions and context-credit leaves.
        for path,value in leaves(self.data):
            data=deepcopy(self.data);parent=data
            for key in path[:-1]:parent=parent[key]
            parent[path[-1]]=str(value)+' forged'
            with self.subTest(path=path),self.assertRaises(ValueError):require_fixture_binding(data)
    def test_complete_sources_and_attributes_reject_drift(self):
        for key,row in self.data['sources'].items():
            for mode in ('value','attributes'):
                root=deepcopy(self.english);n=root.find(f"./{row['type']}[@name='{key}']")
                if mode=='attributes':n.set('translatable','false')
                elif row['type']=='string':n.text=n.text+'X'
                else:n[0].text=n[0].text+'X'
                with self.subTest(key=key,mode=mode),self.assertRaises(ValueError):require_complete(root,key,row,row['source'],row['attributes'])
    def test_every_target_rejects_attributes_and_cross_locale_substitution(self):
        for tag,loc in self.data['locales'].items():
            for key,target in loc['accepted'].items():
                src=self.data['sources'][key];attrs=loc['target_attribute_exceptions'].get(key,{'name':key})
                for mode in ('attributes','cross-locale'):
                    root=deepcopy(self.roots[tag]);n=root.find(f"./{src['type']}[@name='{key}']")
                    if mode=='attributes':n.set('translatable','false')
                    else:
                        other=next((d['accepted'][key]for t,d in self.data['locales'].items()if t!=tag and key in d['accepted']and d['accepted'][key]!=target),None)
                        if other is None:continue
                        if src['type']=='string':n.text=other
                        else:
                            for child in n:child.text=other.get(child.get('quantity'),other['other'])
                    with self.subTest(tag=tag,key=key,mode=mode),self.assertRaises(ValueError):require_complete(root,key,src,target,attrs)
    def test_all_plural_quantities_require_full_fields_tokens_newlines_and_attributes(self):
        k='ui_crop_preview_images';source=self.data['sources'][k]
        for tag,loc in self.data['locales'].items():
            for q in loc['accepted'][k]:
                for mode in ('missing','duplicate','extra','format','newline','attributes','markup','truncated'):
                    root=deepcopy(self.roots[tag]);n=root.find(f"./plurals[@name='{k}']");c=n.find(f"./item[@quantity='{q}']")
                    if mode=='missing':n.remove(c)
                    elif mode=='duplicate':n.append(deepcopy(c))
                    elif mode=='extra':ET.SubElement(n,'item',quantity='zero').text=c.text
                    elif mode=='format':c.text=c.text.replace('%3$d','%3$s')
                    elif mode=='newline':c.text=c.text.replace('\\n','\\\\n')
                    elif mode=='attributes':c.set('formatted','false')
                    elif mode=='markup':ET.SubElement(c,'b').text='x'
                    else:c.text=c.text[:-1]
                    with self.subTest(tag=tag,q=q,mode=mode),self.assertRaises(ValueError):require_complete(root,k,source,loc['accepted'][k],{'name':k})
    def test_predecessor_hold_scope_and_context_laundering_rejected(self):
        for tag in TAGS:
            for mode in ('source-identity','locale','predecessor','hold','edited','retained','attrs','wording','priority','outside','catalogue'):
                b=deepcopy(self.data);loc=b['locales'][tag]
                if mode=='source-identity':b['sources']['invented']={'type':'string','source':'x','attributes':{'name':'invented'}}
                elif mode=='locale':b['locales']['en']=b['locales'].pop(tag)
                elif mode=='predecessor':
                    if loc['predecessors']:loc['predecessors'].pop(next(iter(loc['predecessors'])))
                    else:loc['predecessors']['invented']={'type':'string','target':'forged','attributes':{'name':'invented'}}
                elif mode=='hold':loc['held']['invented']=None
                elif mode=='edited':loc['changed'].pop()
                elif mode=='retained':
                    if loc['unchanged_accepted']:loc['unchanged_accepted'].pop()
                    else:loc['unchanged_accepted'].append('ui_save')
                elif mode=='attrs':loc['target_attribute_exceptions']['ui_quality']={'name':'ui_quality'}
                elif mode=='wording':loc['wording_only'].pop()
                elif mode=='priority':loc['priority_status'][next(iter(loc['priority_status']))]='invented'
                elif mode=='outside':loc['outside_review']['invented']={'type':'string','target':'x','attributes':{'name':'invented'}}
                else:loc['catalogue_identities'].append('string/invented')
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_shape(b)
    def test_save_ellipsis_is_distinct_and_not_an_arbitrary_reference(self):
        for tag in TAGS:
            self.assertEqual(display(tag,'ui_save')+'…',display(tag,'ui_save_a5d0d9'))
            self.assertFalse(current_row(tag,'ui_save_a5d0d9')['target'].startswith('@'))
    def test_complete_routes_and_atomic_labels_match(self):
        for tag in TAGS:
            for key,commands in {'ui_autosave_is_paused_to_protect_that_draft_use':['ui_menu_file','ui_export_recovery_copy','save20_title','save20_file_format'],'ui_recovery_copy_exported_extract_canvas_png_from_the':['ui_menu_file','ui_load_image'],'ui_paste_hint34':['ui_draw26','ui_category_insert','ui_other_images34']}.items():
                for command in commands:self.assertIn(display(tag,command).removesuffix('…'),display(tag,key))
            self.assertEqual(DITHER_PAIRS[tag],(display(tag,'save20_dither'),display(tag,'save20_gif_description')))
            self.assertIn('(%)',display(tag,'ui_quality'))
            self.assertEqual({'name':'ui_quality','formatted':'false'},current_row(tag,'ui_quality')['attributes'])
            self.assertEqual(['%1$d'],FULL_FORMAT_TOKEN.findall(display(tag,'formats22_at_least_frames')))
            self.assertEqual(Counter(['%1$s','%2$s']),Counter(FULL_FORMAT_TOKEN.findall(display(tag,'formats22_animation_message'))))
            self.assertEqual(['%1$s'],FULL_FORMAT_TOKEN.findall(display(tag,'ui_lossless_format')))
    def test_exact_dimension_crop_and_category_consumers_stay_bound(self):
        p=catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        for name,terms in {'DimensionControls.kt':['R.string.ui_width_in','R.string.ui_height_in'],'ImageCropDialog.kt':['R.string.ui_trim_in_percent','R.string.ui_trim_in_pixels','R.plurals.ui_crop_preview_images'],'ToolCategoryButton.kt':['R.string.ui_category_insert']}.items():
            text=(p/name).read_text()
            for term in terms:self.assertIn(term,text)
if __name__=='__main__':unittest.main()
