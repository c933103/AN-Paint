"""Regression tests for complete, independent AN Paint string-priority coverage."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import string_importance as importance
import translation_catalogues as catalogues


class StringImportanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = importance.load_manifest()
        cls.source = importance.default_resource_names()

    def test_all_live_translatable_resources_are_classified_once(self):
        self.assertEqual([], importance.validate(self.manifest, self.source))
        self.assertEqual(self.source, importance.resource_names(importance.ROOT / importance.SOURCE))
        keys = [k for tier in self.manifest["tiers"] for k in tier["keys"]]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(self.source, set(keys))
        self.assertEqual(list(importance.tier_counts(self.manifest)), list(importance.TIERS))

    def test_critical_notices_and_core_commands_have_deliberate_priorities(self):
        assigned = {key: tier["id"] for tier in self.manifest["tiers"] for key in tier["keys"]}
        for key in (
            "ui_save", "ui_save_your_changes", "ui_autosave_failed_use_save",
            "ui_export_did_not_save23", "ui_keep_editing23", "save20_destination_error",
            "formats22_animation_message", "ui_the_previous_draft_could_not_be_restored",
        ):
            self.assertEqual("P0", assigned[key], key)
        for key in (
            "ui_menu_file", "ui_pencil", "ui_undo", "ui_rectangle_select",
            "ui_zoom_in", "language20_app_language", "ui_category_brush",
        ):
            self.assertEqual("P1", assigned[key], key)
        for key in ("ui_image_assembly", "formats22_tiff_description", "ui_crop_preview_images"):
            self.assertEqual("P2", assigned[key], key)
        for key in ("ui_the_arrow_on_the_left_directly_below_the", "ui_help23"):
            self.assertEqual("P3", assigned[key], key)

    def test_new_source_resource_must_not_silently_enter_a_default_tier(self):
        errors = importance.validate(self.manifest, self.source | {"new_important_warning"})
        self.assertTrue(any("unclassified" in e and "new_important_warning" in e for e in errors))

    def test_deleted_resource_must_not_remain_in_manifest(self):
        errors = importance.validate(self.manifest, self.source - {"ui_pencil"})
        self.assertTrue(any("unknown/nontranslatable" in e and "ui_pencil" in e for e in errors))

    def test_duplicate_assignments_and_out_of_order_keys_fail(self):
        duplicate = copy.deepcopy(self.manifest)
        duplicate["tiers"][3]["keys"].append("ui_save")
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
        changed["schema_version"] = 2
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
            self.assertEqual({"yes", "count", "choices"}, importance.resource_names(path))

    def test_direct_coverage_bounds_and_language_fallback_distinction(self):
        tags = catalogues.offered_tags()
        self.assertTrue(tags)
        for tag in tags:
            coverage = importance.locale_coverage(self.manifest, tag)
            self.assertEqual(list(importance.TIERS), list(coverage))
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
