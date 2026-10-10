#!/usr/bin/env python3
"""Reproduce bounded structural evidence, not translation acceptance.

Run from a checkout with the two guard files. Historical comparisons also need
the named PR commit objects, either in this checkout or --history-repository.
The script reads files/Git and mocks catalogue reads; it does not edit resources.
"""
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import translation_catalogues as translations

BASE = "eab28203893ffba45f14a7f96df6d19cf4d19d3b"
BASE_TREE = "537185be479023d1567ab583d808ffaa7a4d3db8"
BASE_RUN_ID = 38013637833
BASE_ARTIFACT_ID = 11654898336
BASE_ARTIFACT_SHA256 = "8834a80a9d7fb6bb34ad66cefe662e04d3daf6262183bd70679d4229bca0a21a"
BASE_XML_SHA256 = "5897e328b0fb2ed082fbae2036f68e713bba5c8b13a7d54ad665a34bc3670853"
BASE_XML_MEMBER = "Paintroid/build/test-results/testReleaseUnitTest/TEST-org.catrobat.paintroid.local.AppLanguageTest.xml"
HISTORY = {
    7: ("b528c9d2a1eeb950143386154cedfcd38c4350af", "730319aea40eb205d18c894c496e500d6f660ac6"),
    9: ("97e511dc63f1b2011300ce49fd1582b4de23ce3d", "a0afe1cfed363b65c3880c9875034b0460f811a2"),
}


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def require_evidence(condition, detail):
    """Keep evidence validation active with -O and PYTHONOPTIMIZE."""
    if not condition:
        raise ValueError(f"Scope evidence validation failed: {detail}")


def guard_result(module):
    result = unittest.TestResult()
    unittest.defaultTestLoader.loadTestsFromModule(module).run(result)
    return result


def validate_base_android_receipt(receipt, xml_bytes):
    """Bind the archived XML to the fixed, independently downloaded CI receipt.

    This is an offline integrity check of recorded evidence. It does not fetch
    GitHub or claim that metadata supplied by an arbitrary receipt is authentic.
    Both the artifact identity/digest and the extracted XML digest are pinned to
    the archive checked during this recheck, so editing both the XML and receipt
    hash cannot silently relabel replacement XML as exact-base evidence.
    """
    artifact = receipt["artifact"]
    workflow = artifact["workflow_run"]
    binding = receipt["xml_binding"]
    expected = {
        "source_base": (receipt["source_base"], BASE),
        "run_url": (receipt["run_url"], f"https://github.com/c933103/AN-Paint/actions/runs/{BASE_RUN_ID}"),
        "artifact.id": (artifact["id"], BASE_ARTIFACT_ID),
        "artifact.digest": (artifact["digest"], "sha256:" + BASE_ARTIFACT_SHA256),
        "artifact.workflow_run.id": (workflow["id"], BASE_RUN_ID),
        "artifact.workflow_run.repository_id": (workflow["repository_id"], 1362702425),
        "artifact.workflow_run.head_repository_id": (workflow["head_repository_id"], 1362702425),
        "artifact.workflow_run.head_sha": (workflow["head_sha"], BASE),
        "xml_binding.file": (binding["file"], "AppLanguageTest-eab2820.xml"),
        "xml_binding.archive_member": (binding["archive_member"], BASE_XML_MEMBER),
        "xml_binding.archive_sha256": (binding["archive_sha256"], BASE_ARTIFACT_SHA256),
        "xml_binding.sha256": (binding["sha256"], BASE_XML_SHA256),
        "XML bytes": (sha256(xml_bytes), binding["sha256"]),
    }
    for field, (actual, required) in expected.items():
        if actual != required:
            raise ValueError(f"Archived Android evidence mismatch: {field}")
    return ET.fromstring(xml_bytes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history-repository", type=Path, default=ROOT)
    args = parser.parse_args()
    out = {"recorded_source_base": BASE, "recorded_source_base_tree": BASE_TREE,
           "replay_target": "Current checkout files; recorded base is provenance, not an assertion that a later replay is the same tree",
           "scope": "Structural and preservation checks only; all acceptance/reset rows remain open",
           "guards": {}, "catalogues": {}, "historical_resource_deltas": {}}
    paths = translations.catalogue_paths()
    tags = translations.offered_tags()
    all_defaults, all_plurals, source_keys, plural_keys = translations.default_resources()
    out["source_counts"] = {"translatable_strings": len(source_keys), "translatable_plurals": len(plural_keys)}
    for pr in HISTORY:
        module = importlib.import_module(f"test_normalization_scope_pr{pr}")
        result = guard_result(module)
        require_evidence(result.testsRun == 1 and result.wasSuccessful(),
                         f"PR{pr} positive guard: tests={result.testsRun}, "
                         f"failures={result.failures}, errors={result.errors}")
        original_read = translations.read_strings
        mutations = []
        targets = {"default": translations.RES / "values/strings.xml", **{tag: paths[tag] for tag in module.SCOPE}}
        for tag, target in targets.items():
            for key in sorted(module.KEYS):
                def damaged_read(path, target=target, key=key):
                    values = original_read(path)
                    if path == target:
                        require_evidence(key in values,
                                         f"PR{pr} mutation input missing: tag={tag}, key={key}")
                        values.pop(key)
                    return values
                with patch.object(translations, "read_strings", damaged_read):
                    negative = guard_result(module)
                require_evidence(len(negative.failures) == 1 and not negative.errors,
                                 f"PR{pr} omission control: tag={tag}, key={key}, "
                                 f"failures={negative.failures}, errors={negative.errors}")
                mutations.append({"tag": tag, "missing_key": key, "detected": True})
        out["guards"][str(pr)] = {"positive_tests": result.testsRun,
            "sha256": sha256((ROOT / f"tools/test_normalization_scope_pr{pr}.py").read_bytes()),
            "missing_key_negative_controls": mutations}
        for tag in module.SCOPE:
            values = translations.read_strings(paths[tag])
            plurals = translations.read_plurals(paths[tag])
            errors = translations.validate_catalogue(tag, require_complete=True)
            require_evidence(not errors, f"Catalogue {tag}: {errors}")
            require_evidence(tags.count(tag) == 1,
                             f"Catalogue registration {tag}: count={tags.count(tag)}")
            out["catalogues"][tag] = {"path": str(paths[tag].relative_to(ROOT)),
                "sha256": sha256(paths[tag].read_bytes()), "registered_once": True,
                "string_count": len(values), "plural_count": len(plurals),
                "missing_translatable_strings": sorted(source_keys - values.keys()),
                "missing_translatable_plurals": sorted(plural_keys - plurals.keys()),
                "validation_errors": errors}

    directory_errors = translations.validate_resource_directories()
    require_evidence(not directory_errors, f"Resource directories: {directory_errors}")
    pt_config = translations.resource_configuration("values-pt-rPT")
    require_evidence(pt_config == translations.resource_configuration("values-b+pt+PT"),
                     "Portuguese resource configurations are not equivalent")
    matches = [p.parent.name for p in paths.values() if translations.resource_configuration(p.parent.name) == pt_config]
    require_evidence(matches == ["values-b+pt+PT"],
                     f"Portuguese canonical directories: {matches}")
    with tempfile.TemporaryDirectory() as directory:
        fake_res = Path(directory)
        for folder in ("values-pt-rPT", "values-b+pt+PT"):
            (fake_res / folder).mkdir()
            (fake_res / folder / "strings.xml").write_text('<resources><string name="x">x</string></resources>')
        with patch.object(translations, "RES", fake_res):
            duplicate_errors = translations.validate_resource_directories()
        require_evidence(len(duplicate_errors) == 1 and "equivalent resource directories" in duplicate_errors[0],
                         f"Equivalent-directory negative control: {duplicate_errors}")
    out["portuguese_configuration"] = {"canonical_directories": matches, "equivalent_duplicate_fixture_rejected": True,
        "fixture_error": duplicate_errors[0]}
    names = ET.parse(translations.RES / "values/app_language_names.xml")
    def array(name):
        return [n.text for n in names.findall(f".//string-array[@name='{name}']/item")]
    aliases = dict(zip(array("app_language_aliases"), array("app_language_alias_targets"), strict=True))
    require_evidence(tags.count("jje") == 1 and "cju" not in tags and aliases.get("cju") == "jje",
                     f"Jeju registration: jje count={tags.count('jje')}, "
                     f"cju registered={'cju' in tags}, alias={aliases.get('cju')}")
    out["jeju_registration"] = {"jje_registration_count": tags.count("jje"), "cju_registered": "cju" in tags,
                                 "legacy_alias": {"cju": aliases["cju"]}}
    out["default_language_note"] = all_defaults["language20_translation_note"]

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(args.history_repository), *arguments])
    def elements(data):
        return {e.get("name"): ET.tostring(e, encoding="unicode").strip() for e in ET.fromstring(data) if e.get("name")}
    for pr, (baseline, head) in HISTORY.items():
        rows = []
        original_guard = git("show", f"{head}:tools/test_normalization_scope_pr{pr}.py")
        require_evidence(original_guard == (ROOT / f"tools/test_normalization_scope_pr{pr}.py").read_bytes(),
                         f"PR{pr} historical guard bytes differ")
        for path in git("diff", "--name-only", baseline, head).decode().splitlines():
            if "/res/values" not in path or not path.endswith("/strings.xml"):
                continue
            old, proposed = (elements(git("show", f"{ref}:{path}")) for ref in (baseline, head))
            current = elements((ROOT / path).read_bytes())
            require_evidence(not old.keys() - proposed.keys(),
                             f"PR{pr} historical removed keys: path={path}, "
                             f"keys={sorted(old.keys() - proposed.keys())}")
            for key, value in proposed.items():
                if old.get(key) == value:
                    continue
                require_evidence(current.get(key) == value,
                                 f"PR{pr} historical element differs: path={path}, key={key}")
                rows.append({"path": path, "key": key, "proposed_sha256": sha256(value.encode()),
                             "current_sha256": sha256(current[key].encode()), "equal": True})
        out["historical_resource_deltas"][str(pr)] = {"baseline": baseline, "head": head,
            "guard_byte_identical": True, "changed_elements": len(rows), "rows": rows}
    changed_counts = [out["historical_resource_deltas"][str(pr)]["changed_elements"] for pr in (7, 9)]
    require_evidence(changed_counts == [135, 97], f"Historical changed-element counts: {changed_counts}")

    receipt = json.loads(Path(__file__).with_name("ci-receipt.json").read_text())
    xml_bytes = Path(__file__).with_name("AppLanguageTest-eab2820.xml").read_bytes()
    xml = validate_base_android_receipt(receipt, xml_bytes)
    require_evidence(xml.get("tests") == "19" and all(xml.get(k) == "0" for k in ("skipped", "failures", "errors")),
                     f"Archived Android suite results: {xml.attrib}")
    required = ("regionalLabelsLegacyMigrationsAndStarterChoicesUseTheirCatalogues", "manchuPickerUsesItsOwnJoinedVerticalAutonym")
    for name in required:
        cases = [n for n in xml.findall("testcase") if n.get("name") == name]
        require_evidence(len(cases) == 1 and not list(cases[0]),
                         f"Archived Android required case: {name}, matches={len(cases)}")
    out["base_android_unit_evidence"] = {"head": receipt["artifact"]["workflow_run"]["head_sha"],
        "artifact_id": receipt["artifact"]["id"], "receipt_and_xml_binding_validated": True,
        "tests": 19, "failures": 0, "errors": 0, "skipped": 0,
        "inspected_cases": list(required), "xml_sha256": sha256(xml_bytes),
        "note": "Executed on source base eab2820; not a fresh candidate CI run or an installed-device matrix"}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
