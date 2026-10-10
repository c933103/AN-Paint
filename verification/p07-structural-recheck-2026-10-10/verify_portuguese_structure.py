from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import tempfile
import xml.etree.ElementTree as ET

import argparse
import io
import subprocess
import tarfile

CURRENT_TREE = "d9858229f98068bef9c6194c90d77610c5ecceec"
CURRENT_COMMIT = "80c14372b0504bc44f9f2809ad477247fdc8100b"
DEFAULT_REPOSITORY = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description="Read-only P07-004/005/006 structural recheck from named Git objects")
parser.add_argument("--history-repository", type=Path, default=DEFAULT_REPOSITORY)
parser.add_argument("--current-repository", type=Path, default=DEFAULT_REPOSITORY)
args = parser.parse_args()

def git(repository, *arguments):
    return subprocess.check_output(["git", "-C", str(repository), *arguments])

snapshots = tempfile.TemporaryDirectory()
CONTEXTS = {}
for label, revision, repository in (
    ("original", "730319aea40eb205d18c894c496e500d6f660ac6", args.history_repository),
    ("integration", "280df39de10004d74e1b7af8edc6e1265ab71477", args.history_repository),
    ("accepted_develop", CURRENT_TREE, args.current_repository),
):
    destination = Path(snapshots.name) / label
    destination.mkdir()
    archive = git(repository, "archive", revision, "Paintroid/src/main/res", "tools/translation_catalogues.py")
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(destination, filter="data")
    CONTEXTS[label] = (destination, revision)

EQUAL = [("values-b+pt+PT", "values-pt-rPT"), ("values-b+id", "values-in"),
         ("values-b+he+IL-v21", "values-iw-rIL-v21")]
DISTINCT = [("values-fr", "values-fr-night"), ("values-b+mn+Mong", "values-b+mn+Cyrl+MN"),
            ("values-en-rUS", "values-en-rGB")]
original_duplicate = git(args.history_repository, "show", "f709df3dfb91054a6411d9e545af644899979b6a:Paintroid/src/main/res/values-pt-rPT/strings.xml")
results = {}
for name, (source, revision) in CONTEXTS.items():
    spec = importlib.util.spec_from_file_location(name, source / "tools/translation_catalogues.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as directory:
        res = Path(directory) / "res"
        shutil.copytree(source / "Paintroid/src/main/res", res)
        module.RES = res
        picker = module.offered_tags()
        platform = [n.get("{http://schemas.android.com/apk/res/android}name")
                    for n in ET.parse(res / "xml/app_locales.xml").getroot()]
        names = ET.parse(res / "values/app_language_names.xml")
        array = lambda n: [x.text for x in names.findall(f".//string-array[@name='{n}']/item")]
        aliases = dict(zip(array("app_language_aliases"), array("app_language_alias_targets"), strict=True))
        paths = module.catalogue_paths()
        config = module.resource_configuration("values-pt-rPT")
        directories = [p.name for p in sorted(res.iterdir())
                       if (p / "strings.xml").exists() and module.resource_configuration(p.name) == config]
        assert directories == ["values-b+pt+PT"]
        assert paths["pt-PT"] == res / "values-b+pt+PT/strings.xml"
        assert picker.count("pt-PT") == platform.count("pt-PT") == 1
        assert picker.count("pt-BR") == platform.count("pt-BR") == 1
        assert "pt" not in picker and "pt" not in platform and aliases["pt"] == "pt-PT"
        assert not (res / "values-pt-rPT/strings.xml").exists()
        assert not (res / "values-pt/strings.xml").exists()
        assert module.validate_resource_directories() == []
        clean_all_errors = module.validate_all(require_complete=False)
        assert clean_all_errors == []
        for a, b in EQUAL:
            assert module.resource_configuration(a) == module.resource_configuration(b)
        for a, b in DISTINCT:
            assert module.resource_configuration(a) != module.resource_configuration(b)
        (res / "values-pt-rPT").mkdir()
        shutil.copyfile(paths["pt-PT"], res / "values-pt-rPT/strings.xml")
        errors = module.validate_all(require_complete=False)
        collision = "equivalent resource directories: values-b+pt+PT and values-pt-rPT"
        assert collision in errors and collision not in clean_all_errors
        assert sorted(x for x in errors if x != collision) == sorted(clean_all_errors)
        (res / "values-pt-rPT/strings.xml").write_bytes(original_duplicate)
        original_errors = module.validate_all(require_complete=False)
        assert collision in original_errors
        results[name] = {
            "revision": revision, "canonical_directory": directories[0],
            "canonical_file_sha256": hashlib.sha256(paths["pt-PT"].read_bytes()).hexdigest(),
            "validator_sha256": hashlib.sha256((source / "tools/translation_catalogues.py").read_bytes()).hexdigest(),
            "picker_pt_PT_count": picker.count("pt-PT"), "platform_pt_PT_count": platform.count("pt-PT"),
            "picker_pt_BR_count": picker.count("pt-BR"), "platform_pt_BR_count": platform.count("pt-BR"),
            "legacy_pt_alias": aliases["pt"], "legacy_or_ambiguous_strings_absent": True,
            "equivalent_pairs_checked": EQUAL, "distinct_pairs_checked": DISTINCT,
            "clean_global_validation_errors": clean_all_errors,
            "injected_canonical_pt_duplicate_rejected_by_validate_all": collision,
            "injected_original_reviewed_pt_duplicate_rejected_by_validate_all": collision,
            "original_reviewed_file_other_validation_errors": [x for x in original_errors if x != collision],
            "unrelated_errors_changed_by_negative_control": False,
            "negative_control_original_duplicate_sha256": hashlib.sha256(original_duplicate).hexdigest(),
        }
reviewed = "f709df3dfb91054a6411d9e545af644899979b6a"
legacy = "Paintroid/src/main/res/values-pt-rPT/strings.xml"
canonical = "Paintroid/src/main/res/values-b+pt+PT/strings.xml"
old = {path: git(args.history_repository, "show", f"{reviewed}:{path}") for path in (legacy, canonical)}
keys = lambda data: {n.get("name") for n in ET.fromstring(data) if n.get("name")}
shared = sorted(keys(old[legacy]) & keys(old[canonical]))
assert shared
removal = "614f54a5dccfe806f5d8f9fc50d9f722da2f8d93"
assert git(args.history_repository, "diff-tree", "--no-commit-id", "--name-status", "-r", removal).decode().strip() == "D\t" + legacy
results["historical_finding"] = {
    "reviewed_commit": reviewed, "both_equivalent_catalogues_present": True,
    "overlapping_resource_names": len(shared),
    "resource_names_sha256": hashlib.sha256("\n".join(shared).encode()).hexdigest(),
    "source_sha256": {path: hashlib.sha256(data).hexdigest() for path, data in old.items()},
    "removal_commit": removal, "removed_path": legacy,
    "current_commit": CURRENT_COMMIT, "current_tree": CURRENT_TREE,
    "review_url": "https://github.com/c933103/AN-Paint/pull/7#discussion_r4079350287",
}
results["accepted_develop"]["source_blob_manifest"] = {
    path: git(args.current_repository, "rev-parse", f"{CURRENT_TREE}:{path}").decode().strip()
    for path in (
        "Paintroid/src/main/res/values-b+pt+PT/strings.xml",
        "Paintroid/src/main/res/values/app_language_names.xml",
        "Paintroid/src/main/res/xml/app_locales.xml",
        "tools/translation_catalogues.py",
        "tools/test_translations.py",
    )
}
results["accepted_develop"]["resource_tree"] = git(
    args.current_repository, "rev-parse", f"{CURRENT_TREE}:Paintroid/src/main/res"
).decode().strip()
print(json.dumps(results, indent=2, ensure_ascii=False))
snapshots.cleanup()
