"""Regression tests for complete, independent AN Paint string-priority coverage."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import string_importance as importance
import translation_catalogues as catalogues


class StringImportanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = importance.load_manifest()
        cls.source = importance.default_resource_keys()

    def test_all_live_translatable_resources_are_classified_once(self):
        self.assertEqual([], importance.validate(self.manifest, self.source))
        self.assertEqual(self.source, importance.resource_keys(importance.ROOT / importance.SOURCE))
        keys = [k for tier in self.manifest["tiers"] for k in tier["keys"]]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(self.source, set(keys))
        self.assertEqual(list(importance.tier_counts(self.manifest)), list(importance.TIERS))

    def test_critical_notices_and_core_commands_have_deliberate_priorities(self):
        assigned = {key: tier["id"] for tier in self.manifest["tiers"] for key in tier["keys"]}
        for key in (
            "string/ui_save", "string/ui_save_your_changes", "string/ui_autosave_failed_use_save",
            "string/ui_share_explanation34",
            "string/ui_sampled_resize_memory_explanation",
            "string/formats22_ascii_description", "string/formats22_pdf_raster_hint", "string/save20_lossy_quality_description",
            "string/ui_higher_quality_usually_makes_a_larger_file_lossless",
            "string/save20_gif_description",
            "string/save20_unsupported_image_colour",
            "string/ui_the_image_was_saved_but_android_could_not",
            "string/ui_export_did_not_save23", "string/ui_keep_editing23", "string/save20_destination_error",
            "string/formats22_animation_message", "string/ui_the_previous_draft_could_not_be_restored",
        ):
            self.assertEqual("P0", assigned[key], key)
        for key in (
            "string/ui_menu_file", "string/ui_pencil", "string/ui_undo", "string/ui_rectangle_select",
            "string/ui_zoom_in", "string/language20_app_language", "string/ui_category_brush",
        ):
            self.assertEqual("P1", assigned[key], key)
        for key in ("string/ui_image_assembly", "string/formats22_tiff_compression", "plurals/ui_crop_preview_images"):
            self.assertEqual("P2", assigned[key], key)
        for key in ("string/ui_the_arrow_on_the_left_directly_below_the", "string/ui_help23"):
            self.assertEqual("P3", assigned[key], key)

    def test_optional_help_and_lossless_reference_have_lower_priority(self):
        assigned = {key: tier["id"] for tier in self.manifest["tiers"] for key in tier["keys"]}
        # These are deliberate contextual decisions, not a length/name heuristic.
        for key in (
            "string/ui_add_up_to_20_images_with_android_s",
            "string/ui_the_arrow_on_the_left_directly_below_the", "string/ui_help23",
            "string/ui_cursor_help29", "string/ui_cursor_help31",
            "string/ui_cursor_marker_help31", "string/ui_pixel_grid_help33",
            "string/formats22_tiff_description", "string/save20_bmp_description",
            "string/formats22_dib_description", "string/formats22_base64_description",
        ):
            self.assertEqual("P3", assigned[key], key)
        source = catalogues.read_strings(importance.ROOT / importance.SOURCE)
        self.assertEqual("@string/ui_cursor_help31", source["ui_cursor_help29"])

    def test_actionable_and_accessible_instructions_are_not_demoted_as_prose(self):
        assigned = {key: tier["id"] for tier in self.manifest["tiers"] for key in tier["keys"]}
        for key in (
            "string/ui_drawing_canvas_pinch_and_move_two_fingers_to",
            "string/ui_fit_entire_canvas_in_view", "string/ui_paste_hint34",
            "string/language20_translation_note",
        ):
            self.assertEqual("P1", assigned[key], key)
        for key in (
            "string/ui_image_assembly_workspace_drag_placed_images_or_drop",
            "string/ui_image_shown_in_crop_preview",
            "string/ui_image_thumbnails_and_filenames_scroll_horizontally_for_more",
            "string/ui_px_drag_an_image_to_move_hold_a",
            "string/ui_cursor_tap_hint37", "string/ui_cursor_pan_draw32",
            "string/ui_cursor_pan_move32", "plurals/ui_crop_preview_images",
            "string/ui_normalize_width_intro", "string/ui_normalize_height_intro",
            "string/ui_normalize_width_info", "string/ui_normalize_height_info",
            "string/commons_check_file_licence", "string/gallery_credit_edit_hint",
            "string/ui_trim_from_the_original_edges_drag_the_handles",
        ):
            self.assertEqual("P2", assigned[key], key)
        for key in (
            "string/ui_a_separate_recovery_copy_has_been_kept_use",
            "string/ui_autosave_is_paused_to_protect_that_draft_use",
            "string/ui_sampled_resize_memory_explanation",
            "string/ui_assembly_source_memory_floor",
            "string/ui_keeps_pixels_at_the_top_left_smaller_canvas",
            "string/ui_your_current_image_has_unsaved_changes", "string/ui_discard_changes23",
            "string/ui_save_explanation23", "string/ui_export_explanation23",
            "string/save20_lossy_quality_description", "string/save20_gif_description",
            "string/formats22_pdf_raster_hint", "string/formats22_ascii_description",
        ):
            self.assertEqual("P0", assigned[key], key)

    def test_inline_teaching_is_not_automatically_an_operational_label(self):
        assigned = {key: tier["id"] for tier in self.manifest["tiers"] for key in tier["keys"]}
        for key in (
            "string/ui_corners_and_edges_resize_round_handle_rotates",
            "string/ui_pinch_to_zoom_drag_to_pan",
            "string/ui_drag_out_to_expand_in_to_trim_drag",
            "string/ui_vertical_hint23", "string/ui_pencil_crisp_adjustable_strokes",
            "string/ui_hold_a_thumbnail_and_drag_it_here_or",
            "string/ui_drag_placed_images_to_move_them_hold_and",
            "string/ui_shows_the_whole_assembly_image_and_output_sizes",
        ):
            self.assertEqual("P3", assigned[key], key)

    def test_commons_import_failures_have_deliberate_specialist_error_priority(self):
        assigned = {key: tier["id"] for tier in self.manifest["tiers"] for key in tier["keys"]}
        # These block a specialist import/credit operation; no drawing data is silently changed.
        # Keep them with the existing typed Commons failures, not optional reference prose.
        for key in (
            "string/commons_metadata_not_file_page",
            "string/commons_metadata_ambiguous_file",
            "string/commons_metadata_unavailable",
            "string/commons_metadata_original_mismatch",
            "string/commons_metadata_invalid_page",
            "string/commons_metadata_field_too_large",
            "string/commons_metadata_cache_failed",
            "string/commons_download_original_mismatch",
            "string/commons_svg_png_encode_failed",
            "string/commons_metadata_http_error",
            "string/commons_metadata_query_failed",
            "string/commons_metadata_response_too_large",
        ):
            self.assertEqual("P2", assigned[key], key)

    def test_new_source_resource_must_not_silently_enter_a_default_tier(self):
        errors = importance.validate(self.manifest, self.source | {"string/new_important_warning"})
        self.assertTrue(any("unclassified" in e and "string/new_important_warning" in e for e in errors))

    def test_deleted_resource_must_not_remain_in_manifest(self):
        errors = importance.validate(self.manifest, self.source - {"string/ui_pencil"})
        self.assertTrue(any("unknown/nontranslatable" in e and "string/ui_pencil" in e for e in errors))

    def test_duplicate_assignments_and_out_of_order_keys_fail(self):
        duplicate = copy.deepcopy(self.manifest)
        duplicate["tiers"][3]["keys"].append("string/ui_save")
        duplicate["tiers"][3]["keys"].sort()
        self.assertTrue(any("assigned to both" in e for e in importance.validate(duplicate, self.source)))
        unsorted = copy.deepcopy(self.manifest)
        unsorted["tiers"][0]["keys"].reverse()
        self.assertTrue(any("alphabetically sorted" in e
                            for e in importance.validate(unsorted, self.source)))

    def test_wrong_schema_or_tier_order_fails(self):
        changed = copy.deepcopy(self.manifest)
        changed["tiers"][0]["id"] = "P9"
        self.assertTrue(any("expected id" in e for e in importance.validate(changed, self.source)))
        changed = copy.deepcopy(self.manifest)
        changed["schema_version"] = 1
        self.assertTrue(any("schema_version" in e for e in importance.validate(changed, self.source)))

    def test_plural_array_and_nontranslatable_filters(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "strings.xml"
            path.write_text(
                '<?xml version="1.0" encoding="utf-8"?>'
                '<resources><string name="yes">Yes</string>'
                '<plurals name="count"><item quantity="other">%d items</item></plurals>'
                '<string-array name="choices"><item>A</item></string-array>'
                '<string-array name="ids" translatable="false"><item>alpha</item></string-array>'
                '<string name="fixed" translatable="false">x</string></resources>',
                encoding="utf-8",
            )
            self.assertEqual({"string/yes", "plurals/count", "string-array/choices"},
                             importance.resource_keys(path))

    def test_nontranslatable_locale_entries_are_directly_present(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "strings.xml"
            path.write_text(
                '<resources><string name="label" translatable="false">Label</string>'
                '<plurals name="count" translatable="false">'
                '<item quantity="other">%d items</item></plurals>'
                '<string-array name="choices" translatable="false"><item>A</item></string-array>'
                '<string name="unclassified">Extra</string></resources>', encoding="utf-8",
            )
            manifest = {"tiers": [{"id": "P0", "keys": [
                "string/label", "plurals/count", "string-array/choices", "string/absent"]}]}
            self.assertEqual({"string/unclassified"}, importance.resource_keys(path))
            with patch.object(catalogues, "offered_tags", return_value=["test"]), \
                    patch.object(catalogues, "catalogue_paths", return_value={"test": path}):
                self.assertEqual(
                    {"P0": {"present": 3, "missing": 1, "total": 4,
                            "missing_keys": ["string/absent"]}},
                    importance.locale_coverage(manifest, "test", include_missing=True),
                )

    def test_same_name_types_are_classified_and_reported_independently(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "values").mkdir()
            (root / "values" / "strings.xml").write_text(
                '<resources><string name="status">Status</string>'
                '<plurals name="status"><item quantity="other">%d</item></plurals>'
                '<string name="fixed" translatable="false">Fixed</string></resources>',
                encoding="utf-8",
            )
            (root / "values" / "arrays.xml").write_text(
                '<resources><string-array name="status"><item>A</item></string-array>'
                '<string name="help">Help</string></resources>', encoding="utf-8",
            )
            locale = root / "locale.xml"
            locale.write_text(
                '<resources><string name="status">Status</string>'
                '<string-array name="status" translatable="false"><item>A</item></string-array>'
                '</resources>', encoding="utf-8",
            )
            manifest = copy.deepcopy(self.manifest)
            for tier, key in zip(manifest["tiers"], (
                    "string/status", "plurals/status", "string-array/status", "string/help")):
                tier["keys"] = [key]
            with patch.object(catalogues, "RES", root), \
                    patch.object(catalogues, "offered_tags", return_value=["test"]), \
                    patch.object(catalogues, "catalogue_paths", return_value={"test": locale}):
                self.assertEqual({"string/status", "plurals/status", "string-array/status", "string/help"},
                                 importance.default_resource_keys())
                self.assertEqual([], importance.validate(manifest))
                self.assertEqual(
                    {"P0": {"present": 1, "missing": 0, "total": 1, "missing_keys": []},
                     "P1": {"present": 0, "missing": 1, "total": 1, "missing_keys": ["plurals/status"]},
                     "P2": {"present": 1, "missing": 0, "total": 1, "missing_keys": []},
                     "P3": {"present": 0, "missing": 1, "total": 1, "missing_keys": ["string/help"]}},
                    importance.locale_coverage(manifest, "test", include_missing=True),
                )

    def test_duplicate_typed_resources_fail_within_and_across_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "values").mkdir()
            path = root / "values" / "strings.xml"
            path.write_text('<resources><string name="same">A</string>'
                            '<string name="same" translatable="false">B</string></resources>',
                            encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate resource string/same"):
                importance.resource_identities(path, translatable_only=False)
            path.write_text('<resources><string name="same">A</string></resources>', encoding="utf-8")
            (root / "values" / "extra.xml").write_text(
                '<resources><string name="same">B</string></resources>', encoding="utf-8")
            with patch.object(catalogues, "RES", root), \
                    self.assertRaisesRegex(ValueError, "duplicate default resource string/same"):
                importance.default_resource_keys()

    def test_bare_unknown_and_malformed_resource_identities_fail(self):
        for key in ("ui_save", "drawable/ui_save", "string/", "string/ui/save"):
            with self.subTest(key=key):
                manifest = copy.deepcopy(self.manifest)
                manifest["tiers"][0]["keys"].append(key)
                manifest["tiers"][0]["keys"].sort()
                self.assertTrue(any("invalid resource key" in e for e in importance.validate(manifest)))

    def test_direct_coverage_bounds_and_language_fallback_distinction(self):
        tags = catalogues.offered_tags()
        self.assertTrue(tags)
        for tag in tags:
            coverage = importance.locale_coverage(self.manifest, tag)
            self.assertEqual(list(importance.TIERS), list(coverage))
            present = importance.resource_keys(catalogues.catalogue_paths()[tag],
                                               translatable_only=False)
            # Repartitioning tiers must not change the source denominator or
            # any locale's total direct presence/missing count.
            self.assertEqual(len(self.source), sum(row["total"] for row in coverage.values()))
            self.assertEqual(len(self.source & present),
                             sum(row["present"] for row in coverage.values()))
            self.assertEqual(len(self.source - present),
                             sum(row["missing"] for row in coverage.values()))
            for row in coverage.values():
                self.assertEqual(row["total"], row["present"] + row["missing"])
                self.assertGreaterEqual(row["missing"], 0)
                self.assertGreaterEqual(row["present"], 0)
        with self.assertRaises(ValueError):
            importance.locale_coverage(self.manifest, "invalid-no-such-locale")
        # Key presence, even in a full catalogue, is not translation or review status.

    def test_machine_readable_cli(self):
        out = subprocess.run(
            [sys.executable, str(importance.ROOT / "tools/string_importance.py"), "--json"],
            capture_output=True, text=True, check=True, timeout=30,
        )
        data = json.loads(out.stdout)
        self.assertEqual(len(self.source), data["source_entries"])
        self.assertEqual(importance.tier_counts(self.manifest), data["tier_counts"])


if __name__ == "__main__":
    unittest.main()
