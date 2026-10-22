"""Polish priority draft regression contracts; independent linguistic review is separate."""
from collections import Counter
from copy import deepcopy
import json
import hashlib
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string
import translation_catalogues as catalogues
# The two memory translations remain pending review against the corrected source.
from memory_warning_source_review import current_source_expectation

KEYS = set('''
colour_converter_unavailable
colour_invalid_metadata
colour_truncated_metadata
colour_unsupported_icc_model
commons_svg_original_size_too_large
commons_svg_original_size_unavailable
formats22_animation_message
formats22_animation_poster
formats22_animation_still
formats22_animation_title
formats22_animation_unknown
formats22_ascii_description
formats22_at_least_frames
formats22_derived_exported
formats22_import_limit
formats22_open_still
formats22_pdf_raster_hint
gallery_credit_could_not_save
gallery_credit_too_large
language20_current
language20_translation_note
legacy_credits_unreadable
save20_destination_error
save20_encoding_budget
save20_file_format
save20_gif_description
save20_invalid_name
save20_lossy_quality_description
save20_unsupported_image_colour
ui_0f_0f_px_1f
ui_100
ui_1_px
ui_1f_s
ui_a_separate_recovery_copy_has_been_kept_use
ui_actual_size_100
ui_add_text
ui_all
ui_an_assembly_source_image_is_missing
ui_android_blocked_the_file_picker
ui_android_could_not_decode_this_image
ui_android_could_not_find_a_file_picker_enable
ui_apply_bounds
ui_apply_crop
ui_assembly_saved
ui_assembly_source_memory_floor
ui_autosave_failed_use_save
ui_autosave_image_encoding_failed
ui_autosave_is_paused_to_protect_that_draft_use
ui_autosave_metadata_is_missing
ui_autosave_paused_use_save
ui_autosave_pixels_are_missing
ui_autosave_pixels_could_not_be_read
ui_autosave_selection_encoding_failed
ui_autosaving_draft
ui_background_colour
ui_background_edit_colour
ui_basic_colours
ui_cannot_create_the_undo_cache_free_some_device
ui_canvas_zoom
ui_canvas_zoom_771f84
ui_choose_a_smaller_output_copy_the_source_images
ui_choose_a_smaller_size
ui_choose_at_least_one_image
ui_choose_dimensions_no_larger_than_the_original
ui_choose_location
ui_clear_all
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
ui_could_not_export_the_recovery_copy
ui_could_not_open_image
ui_could_not_place_the_image
ui_could_not_prepare_the_image
ui_could_not_save_image
ui_could_not_save_the_assembly
ui_could_not_store_the_assembly
ui_crop
ui_crop_must_stay_inside_the_canvas
ui_crop_preview_drag_an_edge_or_corner_drag
ui_d_d_pixels_2f_mp_exceeds_the_current
ui_d_d_px_d_pixels_2f_mp
ui_draft_not_saved_yet
ui_draft_pending
ui_draft_restored
ui_draft_saved
ui_draw_again
ui_drawing_canvas_pinch_and_move_two_fingers_to
ui_drawing_settings
ui_drawing_settings_d900c6
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
ui_export_did_not_save23
ui_export_explanation23
ui_export_recovery_copy_144b8a
ui_font_family
ui_foreground_background_colour_palette
ui_foreground_colour
ui_foreground_edit_colour
ui_full_text_copied
ui_height
ui_height_in
ui_heights
ui_hex_rrggbb
ui_higher_quality_usually_makes_a_larger_file_lossless
ui_history_unavailable34
ui_invalid_autosave_metadata
ui_invalid_colour
ui_invalid_selection_outline
ui_keep_editing23
ui_keeps_pixels_at_the_top_left_smaller_canvas
ui_left_arrow_collapse
ui_line_spacing
ui_lock_aspect_ratio
ui_lock_proportions
ui_magnification
ui_menu
ui_new_colour
ui_no_readable_image_data
ui_no_resize_fits_decoder_memory
ui_none
ui_not_enough_memory_for_this_operation_the_assembly
ui_not_enough_memory_to_finish_opening_this_image
ui_not_enough_memory_to_inspect_this_image
ui_not_enough_memory_to_save_in_this_format
ui_numeric_slider_value
ui_paste_hint34
ui_percent
ui_percent_fd8671
ui_pinch_and_pan_mode
ui_pixels
ui_pixels_6ec9c2
ui_place_text
ui_please_try_again
ui_please_wait_for_the_current_operation
ui_png_encoding_failed
ui_previous_draft_kept_for_recovery
ui_px
ui_px_724eb3
ui_recovered_image
ui_recovery_copy_exported_extract_canvas_png_from_the
ui_reset_crop
ui_reset_to_black_white
ui_resize_and_load
ui_resize_large_image
ui_resize_the_copy
ui_sampled_resize_memory_explanation
ui_save_and_share_41edb4
ui_save_as
ui_save_as_jpeg
ui_save_as_jpeg_xl
ui_save_as_png
ui_save_explanation23
ui_save_png
ui_saved
ui_scales_the_image_unlock_the_ratio_to_stretch
ui_select_an_area
ui_select_an_area_first
ui_selected_colour23
ui_selection_dimensions_are_too_large
ui_share_explanation34
ui_share_saved_image
ui_show_all
ui_show_controls
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
ui_the_draft_is_saving_try_again_shortly
ui_the_encoder_did_not_finish
ui_the_full_image_and_working_buffers_exceed_the
ui_the_image_was_saved_but_android_could_not
ui_the_picker_returned_no_file_please_choose_the
ui_the_picker_returned_no_files
ui_the_previous_draft_could_not_be_moved_to
ui_the_previous_draft_could_not_be_preserved_separately
ui_the_previous_draft_could_not_be_restored
ui_the_previous_draft_needs_more_memory_to_reopen
ui_the_saved_assembly_could_not_be_opened
ui_the_selected_location_is_not_writable
ui_the_selected_provider_did_not_return_any_image
ui_the_trim_would_remove_the_entire_image
ui_the_undo_cache_is_damaged
ui_there_is_not_enough_memory_for_this_operation
ui_this_file_is_not_a_supported_image_use
ui_this_location_is_not_writable
ui_tolerance
ui_too_large_for_the_current_budget_reduce_the
ui_tool_categories
ui_trim_amounts_must_be_zero_or_greater
ui_trim_amounts_must_fit_inside_each_image_use
ui_trim_expand_canvas_by_touch
ui_try_a_different_file_or_location
ui_type_text
ui_unexpected_data_in_the_undo_cache
ui_use_1_1024_pixels
ui_use_50_300
ui_use_a_positive_target_dimension
ui_use_colour
ui_use_rrggbb
ui_width
ui_width_in
ui_working
ui_your_current_image_has_unsaved_changes
'''.split())
TAGS = {'default', 'pl'}
FIXTURE = 'polish_priority_draft_wording.json'
MEMORY = 'ui_d_d_pixels_2f_mp_exceeds_the_current'


REVIEW_BINDING = {'archive_url': 'https://github.com/c933103/AN-Paint/blob/399d7ab1ec6fd197c9824518b470a6d8a0086df9/priority-review-packets.zip',
 'archive_sha256': 'ade1e4eca35692f70dae7691ea14cebc17da0e353fa9fb9a0b4eee17eea45c7a',
 'priority_receipt_member': 'pl/independent-final-receipt.json',
 'priority_receipt_original_sha256': '4ca6d1c3f66390caf784169479d86eefabf7228f2d1b96a581a39cc21db91560',
 'p2_receipt_member': 'pl/independent-p2-companions.json',
 'p2_receipt_original_sha256': '5a23b58693a6025c1aa27281f49ac48c6f758587029c4b99bfc7815277469141',
 'reviewed_values_sha256': '9dcdf42b73f07ac14e29e9ed2b0da0b937f90d41b258fb7b04d47a92bfb7fe29',
 'digest_format': 'SHA-256 of UTF-8 JSON values with sorted keys, ensure_ascii=False and compact '
                  'comma/colon separators',
 'context_unverified_keys': ['formats22_derived_exported',
                             'ui_1_px',
                             'ui_actual_size_100',
                             'ui_collapse_colour_palette',
                             'ui_expand_colour_palette',
                             'ui_foreground_background_colour_palette',
                             'ui_heights',
                             'ui_left_arrow_collapse',
                             'ui_menu',
                             'ui_new_colour',
                             'ui_pinch_and_pan_mode',
                             'ui_reset_to_black_white',
                             'ui_save_as',
                             'ui_save_as_jpeg',
                             'ui_save_as_jpeg_xl',
                             'ui_save_as_png',
                             'ui_tool_categories',
                             'ui_trim_expand_canvas_by_touch']}


def require_review_binding(data):
    """Bind the complete expected pairs to immutable review evidence, not source-file hashes."""
    if data.get('review_binding') != REVIEW_BINDING:
        raise ValueError('Independent review binding differs')
    payload = json.dumps(data['values'], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    if hashlib.sha256(payload.encode()).hexdigest() != REVIEW_BINDING['reviewed_values_sha256']:
        raise ValueError('Complete reviewed pair set differs')


def require_family(data):
    if data.get('schema_version') != 1 or set(data.get('values', {})) != KEYS:
        raise ValueError('Polish draft message inventory differs')
    if set(data.get('constraints', {})) != KEYS:
        raise ValueError('Polish draft constraints are incomplete')
    for key in KEYS:
        if set(data['values'][key]) != TAGS or set(data['constraints'][key]) != TAGS:
            raise ValueError('Polish draft locale inventory differs: ' + key)
        for tag in TAGS:
            if not isinstance(data['values'][key][tag], str) or not data['values'][key][tag]:
                raise ValueError('Empty Polish draft wording: ' + key)
            if set(data['constraints'][key][tag]) != {'attributes', 'formatted', 'placeholders'}:
                raise ValueError('Polish draft constraint fields differ: ' + key)
    require_review_binding(data)
    return data


def display(value):
    """Only strip the ordinary complete Android quotation wrapper used by these inputs."""
    return value[1:-1] if value.startswith('"') and value.endswith('"') else value


class PolishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_family(fixture(FIXTURE))
        cls.xml = {
            tag: (catalogues.RES / directory / 'strings.xml').read_text(encoding='utf-8')
            for tag, directory in [('default', 'values'), ('pl', 'values-pl')]
        }
        cls.nodes = {tag: {n.get('name'): n for n in ET.fromstring(xml) if n.tag == 'string'}
                     for tag, xml in cls.xml.items()}
        cls.strings = {tag: {key: ''.join(node.itertext()) for key, node in nodes.items()}
                       for tag, nodes in cls.nodes.items()}

    def test_complete_wording_attributes_and_typed_placeholders(self):
        for key in KEYS:
            for tag in TAGS:
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, current_source_expectation(key, tag, self.data['values'][key][tag]),
                                   self.data['constraints'][key][tag])
            self.assertEqual(catalogues.placeholders(self.data['values'][key]['default']),
                             catalogues.placeholders(self.data['values'][key]['pl']), key)

    def test_fixture_rejects_missing_key_locale_wording_and_constraints(self):
        for key in KEYS:
            for mutation in ('key', 'locale', 'empty', 'constraint'):
                data = deepcopy(self.data)
                if mutation == 'key':
                    del data['values'][key]
                elif mutation == 'locale':
                    del data['values'][key]['pl']
                elif mutation == 'empty':
                    data['values'][key]['pl'] = ''
                else:
                    del data['constraints'][key]['pl']
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_family(data)

    def test_changed_missing_duplicate_or_markup_messages_are_rejected(self):
        for key in KEYS:
            for mutation in ('truncate', 'changed', 'missing', 'duplicate', 'markup', 'attribute'):
                root = ET.fromstring(self.xml['pl'])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'truncate':
                    node.text = node.text[:-1]
                elif mutation == 'changed':
                    node.text = 'zmiana ' + node.text
                elif mutation == 'missing':
                    root.remove(node)
                elif mutation == 'duplicate':
                    root.append(deepcopy(node))
                elif mutation == 'markup':
                    child = ET.SubElement(node, 'b')
                    child.text, node.text = node.text, None
                else:
                    node.set('translatable', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key,
                                   self.data['values'][key]['pl'], self.data['constraints'][key]['pl'])

    def test_independent_binding_and_complete_delta_inventory_cannot_be_dropped(self):
        self.assertEqual(231, len(KEYS))
        self.assertEqual('independent_static_review_with_holds', self.data['review_status'])
        self.assertEqual(18, len(self.data['review_binding']['context_unverified_keys']))
        for mutation in ('missing-binding', 'changed-receipt', 'changed-pair', 'removed-hold'):
            data = deepcopy(self.data)
            if mutation == 'missing-binding': del data['review_binding']
            elif mutation == 'changed-receipt': data['review_binding']['priority_receipt_member'] = 'other.json'
            elif mutation == 'removed-hold': data['review_binding']['context_unverified_keys'].pop()
            else: data['values']['ui_assembly_source_memory_floor']['pl'] += ' zmiana'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_family(data)

    def test_assembly_memory_floor_preserves_every_complete_remedy_clause(self):
        key = 'ui_assembly_source_memory_floor'
        clauses = (
            'Obraz źródłowy wymaga więcej pamięci do dekodowania, niż jest obecnie dostępne, nawet dla bardzo małego obrazu wynikowego.',
            'Zmniejszenie wymiarów kompozycji nie rozwiąże tego problemu.',
            'Zamknij inne dokumenty lub przygotuj mniejszy obraz źródłowy przed ponowną próbą.',
            'Kompozycja pozostaje bez zmian.',
        )
        expected = ' '.join(clauses)
        self.assertEqual(expected, self.strings['pl'][key])
        for clause in clauses:
            root = ET.fromstring(self.xml['pl'])
            root.find(f"./string[@name='{key}']").text = expected.replace(clause, '')
            with self.subTest(clause=clause), self.assertRaises(ValueError):
                require_string(ET.tostring(root, encoding='unicode'), key,
                               self.data['values'][key]['pl'], self.data['constraints'][key]['pl'])

    def test_placeholder_type_precision_loss_and_unescaped_apostrophes_are_rejected(self):
        expected = self.strings['pl'][MEMORY]
        for value in (expected.replace('%1$d', '%1$s'), expected.replace('%3$.2f', '%3$f'),
                      expected.replace('%4$.2f', ''), expected + " '"):
            root = ET.fromstring(self.xml['pl'])
            root.find(f"./string[@name='{MEMORY}']").text = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                require_string(ET.tostring(root, encoding='unicode'), MEMORY, value,
                               self.data['constraints'][MEMORY]['pl'])

    def test_priority_inventory_present_and_catalogue_syntax_valid(self):
        # Completeness is only the current manifest's priority subset, not all Polish strings.
        manifest = json.loads((catalogues.ROOT / 'translations/string-importance.json').read_text())
        priority = {key.split('/', 1)[1] for tier in manifest['tiers'] if tier['id'] in {'P0', 'P1'}
                    for key in tier['keys']}
        self.assertFalse(priority - self.strings['pl'].keys())
        self.assertEqual([], catalogues.validate_catalogue('pl', require_complete=False))
        root = ET.fromstring(self.xml['pl'])
        identities = [(node.tag, node.get('name')) for node in root]
        self.assertEqual(len(identities), len(set(identities)))
        for node in root.findall('string'):
            value = ''.join(node.itertext())
            with self.subTest(key=node.get('name')):
                self.assertEqual([], catalogues.android_string_errors(value))
                self.assertEqual([], catalogues.format_string_errors(value, node.get('formatted') != 'false'))
                key = node.get('name')
                if not value.startswith('@string/'):
                    self.assertEqual(catalogues.placeholders(self.strings['default'][key]),
                                     catalogues.placeholders(value))

    def test_dimension_units_compose_in_locative_both_axes(self):
        strings = self.strings['pl']
        self.assertEqual('piksele', display(strings['ui_pixels']))
        self.assertEqual('Procenty', strings['ui_percent'])
        for key, label in (('ui_width_in', 'Szerokość'), ('ui_height_in', 'Wysokość')):
            for unit_key, unit in (('ui_pixels_6ec9c2', 'pikselach'), ('ui_percent_fd8671', 'procentach')):
                with self.subTest(key=key, unit=unit):
                    self.assertEqual(f'{label} w {unit}',
                                     strings[key].replace('%1$s', display(strings[unit_key])))

    def test_animation_count_composes_without_numeral_agreement_or_english_fallback(self):
        strings = self.strings['pl']
        for count in (2, 5, 21, 22, 100):
            for value in (str(count), strings['formats22_at_least_frames'].replace('%1$d', str(count))):
                composed = strings['formats22_animation_message'].replace('%1$s', 'GIF').replace('%2$s', value)
                self.assertEqual(f'Liczba klatek w tym pliku GIF: {value}. '
                                 'AN Paint edytuje obrazy nieruchome i nie zachowuje animacji.', composed)
        self.assertIn('zamiast klatek animacji', strings['formats22_animation_poster'])
        self.assertIn('tylko pierwsza klatka', strings['formats22_animation_still'])
        self.assertIn('nie zachowa żadnej animacji', strings['formats22_animation_unknown'])

    def test_dynamic_tool_gender_is_avoided_by_named_head(self):
        strings = self.strings['pl']
        for key, action in (('ui_expand_tool_category', 'Rozwiń'), ('ui_collapse_tool_category', 'Zwiń')):
            for tool_key in ('ui_brush', 'ui_eraser', 'ui_rectangle_select'):
                tool = display(strings[tool_key])
                value = strings[key].replace('%1$s', strings['ui_drawing23']).replace('%2$s', tool)
                self.assertEqual(f'Narzędzia rysowania. Wybrane narzędzie: {tool}. {action} narzędzia i opcje', value)

    def test_safety_choices_alias_and_preserved_uncertain_values(self):
        strings = self.strings['pl']
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual(('Zapisz', 'Odrzuć zmiany', 'Kontynuuj edycję'),
                         tuple(strings[k] for k in ('ui_save', 'ui_discard_changes23', 'ui_keep_editing23')))
        for key, expected in {'ui_discard': 'Odrzuć zmiany', 'ui_fit_image': '"Cały obraz w\u00a0oknie"',
                              'ui_main23': 'Główne', 'ui_swap_foreground_background': '"Zamień kolory"'}.items():
            self.assertEqual(expected, strings[key])
        self.assertEqual(('Pierwszy plan', 'Tło'), (strings['ui_fg'], strings['ui_bg']))

    def test_memory_recovery_and_original_file_guarantees_are_complete(self):
        strings = self.strings['pl']
        for clause in ('%1$d × %2$d px (%3$.2f MP)', '%4$.2f MP.',
                       'przechowuje cały obraz w pamięci', 'przekształcenia oraz zaznaczenia',
                       'Ten limit zależy od dostępnej pamięci.',
                       'przed przydzieleniem pamięci na zbyt dużą bitmapę',
                       'Nie zastosowano automatycznej zmiany rozmiaru.'):
            self.assertIn(clause, strings[MEMORY])
        self.assertIn('Oryginalny plik pozostanie bez zmian.', strings['ui_the_full_image_and_working_buffers_exceed_the'])
        self.assertIn('jako kopia odzyskiwania', strings['ui_history_unavailable34'])
        self.assertIn('aby chronić tę wersję roboczą', strings['ui_autosave_is_paused_to_protect_that_draft_use'])
        self.assertIn('canvas.png', strings['ui_a_separate_recovery_copy_has_been_kept_use'])
        self.assertIn('ZIP', strings['ui_a_separate_recovery_copy_has_been_kept_use'])
        self.assertIn('Bieżące miejsce zapisu pozostanie bez zmian.', strings['ui_share_explanation34'])

    def test_route_labels_and_pan_zoom_distinctions_match(self):
        strings = self.strings['pl']
        route = ' → '.join(strings[key] for key in ('ui_draw26', 'ui_category_insert', 'ui_other_images34'))
        self.assertIn(route, strings['ui_paste_hint34'])
        canvas = strings['ui_drawing_canvas_pinch_and_move_two_fingers_to']
        self.assertIn('Zbliżaj lub rozsuwaj dwa palce', canvas)
        self.assertIn(f'Tryb „{strings["ui_navigate"]}”', canvas)
        self.assertIn('jednym palcem', canvas)
        self.assertEqual('Jednolite wypełnienie', strings['ui_solid_fill'])
        self.assertNotEqual(strings['ui_outline'], strings['ui_solid_fill'])


if __name__ == '__main__':
    unittest.main()
