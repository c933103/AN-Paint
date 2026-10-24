#!/usr/bin/env python3
"""Read-only integrity checks. This is not an application test."""

import hashlib
import json
from pathlib import Path
import unicodedata
import xml.etree.ElementTree as ET


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


here = Path(__file__).resolve().parent
input_dir = here.parent / "amharic-held-proportions-resolution-20261024"
input_seal = "d113853881663749a9b02859739b1c320dae3bbbec5fd80295d3426ee67d5b35"
assert sha((input_dir / "MANIFEST.json").read_bytes()) == input_seal
assert (here / "input-MANIFEST.json").read_bytes() == (input_dir / "MANIFEST.json").read_bytes()
input_manifest = json.loads((input_dir / "MANIFEST.json").read_text())
assert len(input_manifest["files"]) == 49
for filename, expected in input_manifest["files"].items():
    assert sha((input_dir / filename).read_bytes()) == expected, filename

bindings = json.loads((input_dir / "source-bindings.json").read_text())
assert len(bindings) == 16
for filename, binding in bindings.items():
    data = (input_dir / binding["local_complete_copy"]).read_bytes()
    assert sha(data) == binding["sha256"], filename
    assert git_blob(data) == binding["git_blob"], filename

original = (input_dir / "original-held-rows.json").read_bytes()
assert (here / "prior-held-records.json").read_bytes() == original
old_rows = {r["key"]: r for r in json.loads(original)}
result = json.loads((here / "adjudicated-values.json").read_text())
rows = result["decisions"]
assert result["input_manifest_sha256"] == input_seal
expected = {
    "string/ui_same_width": ("release_with_revision", "እኩል ስፋት"),
    "string/ui_same_height": ("release_with_revision", "እኩል ቁመት"),
    "string/ui_lock_proportions": ("release_unchanged", "ተመጣጣኝነት መጠበቂያ"),
}
assert len(rows) == len(expected) == len({r["key"] for r in rows})
resource = ET.parse(here / "adjudicated-values.xml").getroot()
assert len(resource) == 3
source = ET.parse(input_dir / "source/Paintroid/src/main/res/values/strings.xml").getroot()
target = ET.parse(input_dir / "source/Paintroid/src/main/res/values-b+am/strings.xml").getroot()
for row in rows:
    key = row["key"]
    name = key.split("/", 1)[1]
    assert (row["decision"], row["adjudicated_value"]) == expected[key]
    assert row["prior_decision"] == old_rows[key]["exact_held_decision_and_requirements"]
    assert row["adjudicated_value"] == unicodedata.normalize("NFC", row["adjudicated_value"])
    assert sha(row["adjudicated_value"].encode()) == row["display_value_utf8_sha256"]
    assert row["adjudicated_XML_text"] == '"' + row["adjudicated_value"] + '"'
    assert sha(row["adjudicated_XML_text"].encode()) == row["adjudicated_XML_text_sha256"]
    assert sha(row["adjudicated_XML_element"].encode()) == row["adjudicated_XML_element_sha256"]
    assert resource.find(f"string[@name='{name}']").text == row["adjudicated_XML_text"]
    english = source.find(f"string[@name='{name}']").text
    assert english == row["english"]
    assert sha(english.encode()) == row["source_English_sha256"]
    assert target.find(f"string[@name='{name}']") is None
    assert row["english_change_required"] is False
    assert row["native_review"] is False
    assert row["runtime_verified"] is False
    assert row["rendering_verified"] is False

manifest = json.loads((here / "MANIFEST.json").read_text())
assert manifest["input_manifest_sha256"] == input_seal
for filename, expected_hash in manifest["files"].items():
    assert sha((here / filename).read_bytes()) == expected_hash, filename
for line in (here / "SHA256SUMS").read_text().splitlines():
    expected_hash, filename = line.split("  ", 1)
    assert sha((here / filename).read_bytes()) == expected_hash, filename

print(json.dumps({
    "verified": True,
    "input_payload_files": 49,
    "project_blob_bindings": 16,
    "output_payload_files": len(manifest["files"]),
    "review_seal_sha256": sha((here / "MANIFEST.json").read_bytes()),
    "decisions": {row["key"]: row["decision"] for row in rows},
    "originals_unchanged": True,
    "app_tests_run": False,
    "implemented": 0,
}, ensure_ascii=False, indent=2))
