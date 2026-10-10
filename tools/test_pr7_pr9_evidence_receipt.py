"""Reject relabelled or substituted archived localization-recheck XML."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

EVIDENCE = Path(__file__).resolve().parents[1] / "verification/pr7-pr9-recheck-2026-10-10"
SPEC = importlib.util.spec_from_file_location("pr7_pr9_scope_evidence", EVIDENCE / "verify_scope.py")
SCOPE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCOPE)


class EvidenceReceiptTest(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((EVIDENCE / "ci-receipt.json").read_text())
        self.xml = (EVIDENCE / "AppLanguageTest-eab2820.xml").read_bytes()

    def test_recorded_xml_and_fixed_artifact_identity_match(self):
        root = SCOPE.validate_base_android_receipt(self.receipt, self.xml)
        self.assertEqual("19", root.get("tests"))
        self.assertEqual("0", root.get("failures"))

    def test_stale_or_edited_receipt_fields_are_rejected(self):
        fields = ("source_base", "run_url", "artifact.id", "artifact.digest",
                  "artifact.workflow_run.id", "artifact.workflow_run.head_sha",
                  "artifact.workflow_run.repository_id", "artifact.workflow_run.head_repository_id",
                  "xml_binding.file", "xml_binding.archive_member",
                  "xml_binding.archive_sha256", "xml_binding.sha256")
        for field in fields:
            with self.subTest(field=field):
                receipt = copy.deepcopy(self.receipt)
                target = receipt
                parts = field.split(".")
                for part in parts[:-1]:
                    target = target[part]
                target[parts[-1]] = "stale-or-substituted"
                with self.assertRaises(ValueError):
                    SCOPE.validate_base_android_receipt(receipt, self.xml)

    def test_substituted_xml_fails_even_when_its_receipt_hash_is_changed(self):
        changed = self.xml + b"\n"
        with self.assertRaises(ValueError):
            SCOPE.validate_base_android_receipt(self.receipt, changed)
        receipt = copy.deepcopy(self.receipt)
        receipt["xml_binding"]["sha256"] = hashlib.sha256(changed).hexdigest()
        with self.assertRaises(ValueError):
            SCOPE.validate_base_android_receipt(receipt, changed)


if __name__ == "__main__":
    unittest.main()
