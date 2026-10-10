"""Exercise evidence replay validation in normal and optimized interpreters."""
from contextlib import ExitStack
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "verification/pr7-pr9-recheck-2026-10-10/verify_scope.py"
MODES = (("normal", (), None, 0), ("flag", ("-O",), None, 1),
         ("environment", (), "1", 1))
NEGATIVE_CASES = {
    "empty_guard": "PR7 positive guard: tests=0",
    "failed_guard": "PR7 positive guard: tests=1",
    "undetected_omission": "PR7 omission control:",
    "errored_omission": "fixture guard error",
    "missing_mutation_input": "PR7 mutation input missing:",
    "invalid_catalogue": "Catalogue en-001: ['fixture incomplete catalogue']",
    "unregistered_catalogue": "Catalogue registration en-001: count=0",
    "duplicate_registration": "Catalogue registration en-001: count=2",
    "invalid_directories": "Resource directories: ['fixture directory error']",
    "different_portuguese_configuration": "Portuguese resource configurations are not equivalent",
    "missing_portuguese_catalogue": "Portuguese canonical directories: []",
    "undetected_duplicate_directories": "Equivalent-directory negative control: []",
    "legacy_jeju_registration": "Jeju registration:",
    "changed_guard": "PR7 historical guard bytes differ",
    "removed_historical_key": "PR7 historical removed keys:",
    "changed_historical_element": "PR7 historical element differs:",
    "missing_historical_element": "PR7 historical element differs:",
    "wrong_historical_count": "Historical changed-element counts: [134, 97]",
    "wrong_android_count": "Archived Android suite results:",
    "failed_android_suite": "Archived Android suite results:",
    "missing_android_case": "Archived Android required case:",
    "failed_android_case": "Archived Android required case:",
    "changed_receipt": "Archived Android evidence mismatch: source_base",
}


def _load_verifier():
    spec = importlib.util.spec_from_file_location("scope_evidence_probe", VERIFIER)
    scope = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scope)
    return scope


def _probe(scenario):
    """Run the real entry point on a small complete, read-only fixture.

    Historical Git replies and catalogue inventory are local fixtures so these
    tests work in CI's shallow checkout. Real unittest guard execution, omission
    mutations, resource parsing, XML receipt validation and JSON emission run.
    Each negative case changes one prerequisite of the successful fixture.
    """
    scope = _load_verifier()
    translations = scope.translations
    with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
        root = Path(directory)
        res = root / "Paintroid/src/main/res"
        tools = root / "tools"
        tools.mkdir()
        paths = {}
        historical = {}
        modules = {}
        for pr, tag, folder, count in ((7, "en-001", "values-b+en+001", 135),
                                        (9, "jje", "values-b+jje", 97)):
            path = res / folder / "strings.xml"
            path.parent.mkdir(parents=True)
            tree = ET.Element("resources")
            ET.SubElement(tree, "string", name="required").text = "required value"
            for index in range(count - 1):
                ET.SubElement(tree, "string", name=f"key_{index}").text = str(index)
            historical[pr] = ET.tostring(tree)
            path.write_bytes(historical[pr])
            paths[tag] = path
            module = types.ModuleType(f"test_normalization_scope_pr{pr}")
            module.KEYS, module.SCOPE = {"required"}, (tag,)

            def guard(self, tag=tag):
                self.assertIn("required", translations.read_strings(res / "values/strings.xml"))
                self.assertIn("required", translations.read_strings(paths[tag]))

            module.GuardTest = type("GuardTest", (unittest.TestCase,), {"test_presence": guard})
            modules[module.__name__] = module
            (tools / f"test_normalization_scope_pr{pr}.py").write_text(f"fixture guard {pr}\n")
        for folder in ("values", "values-b+pt+PT"):
            path = res / folder / "strings.xml"
            path.parent.mkdir()
            path.write_text('<resources><string name="required">required value</string></resources>')
        paths["pt-PT"] = res / "values-b+pt+PT/strings.xml"
        (res / "values/app_language_names.xml").write_text(
            '<resources><string-array name="app_language_aliases"><item>cju</item></string-array>'
            '<string-array name="app_language_alias_targets"><item>jje</item></string-array></resources>')
        tags = ["en-001", "jje", "pt-PT"]
        if scenario == "unregistered_catalogue":
            tags.remove("en-001")
        elif scenario == "duplicate_registration":
            tags.append("en-001")
        elif scenario == "legacy_jeju_registration":
            tags.append("cju")
        elif scenario == "missing_portuguese_catalogue":
            paths.pop("pt-PT")
        elif scenario == "missing_mutation_input":
            (res / "values/strings.xml").write_text("<resources/>")
        elif scenario in ("changed_historical_element", "missing_historical_element"):
            tree = ET.fromstring(historical[7])
            if scenario == "changed_historical_element":
                tree[1].text = "changed"
            else:
                tree.remove(tree[1])
            paths["en-001"].write_bytes(ET.tostring(tree))
        elif scenario == "wrong_historical_count":
            tree = ET.fromstring(historical[7])
            tree.remove(tree[-1])
            historical[7] = ET.tostring(tree)

        def history_output(command):
            arguments = command[3:]
            if arguments[0] == "diff":
                pr = next(pr for pr, (_, head) in scope.HISTORY.items() if head == arguments[-1])
                return str(paths[modules[f"test_normalization_scope_pr{pr}"].SCOPE[0]].relative_to(root)).encode() + b"\n"
            if arguments[0] != "show":
                raise ValueError(f"Unexpected fixture Git command: {command}")
            ref, path = arguments[1].split(":", 1)
            if path.startswith("tools/"):
                return b"changed guard" if scenario == "changed_guard" else (root / path).read_bytes()
            for pr, (baseline, head) in scope.HISTORY.items():
                if ref == baseline:
                    if scenario == "removed_historical_key" and pr == 7:
                        return b'<resources><string name="removed">old</string></resources>'
                    return b"<resources/>"
                if ref == head:
                    return historical[pr]
            raise ValueError(f"Unexpected fixture historical ref: {ref}")

        stack.enter_context(patch.object(scope, "ROOT", root))
        stack.enter_context(patch.object(scope.sys, "argv", [str(VERIFIER)]))
        stack.enter_context(patch.object(translations, "RES", res))
        stack.enter_context(patch.object(translations, "catalogue_paths", return_value=paths))
        stack.enter_context(patch.object(translations, "offered_tags", return_value=tags))
        stack.enter_context(patch.object(translations, "default_resources", return_value=(
            {"language20_translation_note": "fixture note"}, {}, {"required"}, set())))
        catalogue_errors = ["fixture incomplete catalogue"] if scenario == "invalid_catalogue" else []
        stack.enter_context(patch.object(translations, "validate_catalogue", return_value=catalogue_errors))
        stack.enter_context(patch.object(scope.importlib, "import_module", side_effect=modules.__getitem__))
        stack.enter_context(patch.object(scope.subprocess, "check_output", side_effect=history_output))
        if scenario in ("empty_guard", "failed_guard", "undetected_omission", "errored_omission", "missing_mutation_input"):
            actual_guard_result = scope.guard_result
            calls = 0

            def guard_result(module):
                nonlocal calls
                calls += 1
                result = unittest.TestResult()
                result.testsRun = 0 if scenario == "empty_guard" else 1
                if scenario == "failed_guard":
                    result.failures.append(("fixture", "fixture positive guard failure"))
                elif scenario == "errored_omission" and calls > 1:
                    result.errors.append(("fixture", "fixture guard error"))
                elif scenario == "missing_mutation_input" and calls > 1:
                    return actual_guard_result(module)
                return result

            stack.enter_context(patch.object(scope, "guard_result", side_effect=guard_result))
        if scenario in ("invalid_directories", "undetected_duplicate_directories"):
            errors = ["fixture directory error"] if scenario == "invalid_directories" else []
            stack.enter_context(patch.object(translations, "validate_resource_directories", return_value=errors))
        if scenario == "different_portuguese_configuration":
            original_configuration = translations.resource_configuration
            stack.enter_context(patch.object(translations, "resource_configuration", side_effect=lambda folder:
                "different" if folder == "values-pt-rPT" else original_configuration(folder)))
        if scenario in ("wrong_android_count", "failed_android_suite", "missing_android_case", "failed_android_case", "changed_receipt"):
            validate_receipt = scope.validate_base_android_receipt

            def android_receipt(receipt, xml_bytes):
                if scenario == "changed_receipt":
                    receipt["source_base"] = "changed"
                tree = validate_receipt(receipt, xml_bytes)
                if scenario == "wrong_android_count":
                    tree.set("tests", "18")
                elif scenario == "failed_android_suite":
                    tree.set("failures", "1")
                else:
                    case = next(case for case in tree.findall("testcase") if case.get("name") ==
                                "regionalLabelsLegacyMigrationsAndStarterChoicesUseTheirCatalogues")
                    if scenario == "missing_android_case":
                        tree.remove(case)
                    else:
                        ET.SubElement(case, "failure", message="fixture failure")
                return tree

            stack.enter_context(patch.object(scope, "validate_base_android_receipt", side_effect=android_receipt))
        print(f"optimization={sys.flags.optimize}", file=sys.stderr)
        scope.main()


class EvidenceValidationModeTest(unittest.TestCase):
    def run_probe(self, scenario, flags, optimize):
        environment = os.environ.copy()
        environment.pop("PYTHONOPTIMIZE", None)
        if optimize is not None:
            environment["PYTHONOPTIMIZE"] = optimize
        return subprocess.run([sys.executable, *flags, str(Path(__file__).resolve()), "--probe", scenario],
                              env=environment, text=True, capture_output=True, timeout=30)

    def test_complete_fixture_emits_evidence_in_every_mode(self):
        for mode, flags, optimize, level in MODES:
            with self.subTest(mode=mode):
                result = self.run_probe("valid", flags, optimize)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(f"optimization={level}", result.stderr)
                evidence = json.loads(result.stdout)
                self.assertEqual([135, 97], [evidence["historical_resource_deltas"][pr]["changed_elements"] for pr in ("7", "9")])
                self.assertTrue(evidence["base_android_unit_evidence"]["receipt_and_xml_binding_validated"])
                for guard in evidence["guards"].values():
                    self.assertEqual(2, len(guard["missing_key_negative_controls"]))
                    self.assertTrue(all(control["detected"] for control in guard["missing_key_negative_controls"]))

    def test_invalid_evidence_fails_without_emitting_json_in_every_mode(self):
        for mode, flags, optimize, level in MODES:
            for scenario, diagnostic in NEGATIVE_CASES.items():
                with self.subTest(mode=mode, scenario=scenario):
                    result = self.run_probe(scenario, flags, optimize)
                    self.assertNotEqual(0, result.returncode)
                    self.assertEqual("", result.stdout)
                    self.assertIn(f"optimization={level}", result.stderr)
                    self.assertIn("ValueError:", result.stderr)
                    self.assertIn(diagnostic, result.stderr)

    def test_receipt_regressions_pass_in_every_mode(self):
        for mode, flags, optimize, level in MODES:
            with self.subTest(mode=mode):
                environment = os.environ.copy()
                environment.pop("PYTHONOPTIMIZE", None)
                if optimize is not None:
                    environment["PYTHONOPTIMIZE"] = optimize
                result = subprocess.run([sys.executable, *flags, "-m", "unittest", "discover", "-s", "tools",
                                         "-p", "test_pr7_pr9_evidence_receipt.py"], cwd=ROOT, env=environment,
                                        text=True, capture_output=True, timeout=30)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("Ran 3 tests", result.stderr)
                self.assertIn("OK", result.stderr)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--probe":
        _probe(sys.argv[2])
    else:
        unittest.main()
