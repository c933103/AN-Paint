#!/usr/bin/env python3
"""Validate the saved PR35 cohort; no Android execution or speech certification."""
from pathlib import Path
import hashlib
import json
import struct
import zipfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    manifest = json.loads((HERE / "artifact-manifest.json").read_text())
    summary = json.loads((HERE / "summary.json").read_text())
    archive = HERE / "characterization-evidence.zip"
    require(hashlib.sha256(archive.read_bytes()).hexdigest() == manifest["zip_sha256"], "ZIP hash")
    entries = {f["path"]: f for f in manifest["files"]}
    require(len(entries) == len(manifest["files"]) == 115, "Entry inventory")
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, "ZIP CRC")
        require(set(z.namelist()) == set(entries) and len(z.namelist()) == 115, "ZIP paths")
        data = {}
        for name, f in entries.items():
            require(not name.startswith("/") and ".." not in Path(name).parts, "Unsafe path")
            b = z.read(name)
            require(len(b) == f["bytes"] and hashlib.sha256(b).hexdigest() == f["sha256"], name)
            data[name] = b
        cases = ET.fromstring(data["VerticalNoticeResizeCharacterizationTest.xml"])
        require(cases.get("tests") == "8" and all(cases.get(k) == "0" for k in ["failures", "errors", "skipped"]), "New JUnit status")
        require(len(cases.findall("testcase")) == 8, "New JUnit inventory")
        inventory = json.loads(data["jvm-inventory.json"])
        require(len(inventory) == 737 == len({(r["class"], r["name"]) for r in inventory}), "Full JUnit inventory")
        require(not ET.fromstring(data["lint-results-debug.xml"]).findall("issue"), "Lint")
        total = 0
        for name in data:
            if name.startswith("device/") and name.endswith("summary.json"):
                record = json.loads(data[name])
                require(record["success"] and all(not record[k] for k in ["missing", "unexpected", "errors"]), name)
                require(record["expected_tests"] == record["completed_tests"] == len(record["cases"]), name)
                require(all(c["status"] == "passed" for c in record["cases"]), name)
                total += record["completed_tests"]
        require(total == 94, "Installed inventory")
        tags = ["mn-Mong", "mnc-Mong", "lzh-Hant", "en-XV", "qaa-Zsye-XV"]
        expected = {f"characterization/api{api}-{tag}-{edge}-shrink124-{part}.png"
                    for api in [30, 35] for tag in tags for edge in ["false", "true"]
                    for part in ["reference", "parent"]}
        expected |= {f"characterization/api{api}-{tag}-{kind}-{part}.png"
                     for api in [30, 35] for tag in tags
                     for kind in ["unsupported-zwj", "ordinary-emoji", "joined-word"]
                     for part in ["reference", "parent"]}
        require(expected == {n for n in data if n.endswith(".png")} and len(expected) == 100, "PNG matrix")
        for name in expected:
            b = data[name]
            require(b.startswith(b"\x89PNG\r\n\x1a\n") and b[12:16] == b"IHDR", name)
            width, height = struct.unpack(">II", b[16:24])
            require(width > 0 and height > 0, name)
        for api in [30, 35]:
            reports = {kind: json.loads(data[f"characterization/api{api}-{kind}.json"])
                       for kind in ["routes", "transitions", "events", "ink"]}
            for kind, report in reports.items():
                require(report["completed"] and report["build_commit"] == summary["tested_merge"]
                        and str(report["run_id"]) == str(summary["run_id"]), kind)
            for kind, count in [("routes", 10), ("transitions", 80), ("ink", 15)]:
                require(len(reports[kind]["rows"]) == count, kind)
            for row in reports["routes"]["rows"]:
                require(row["route"] == "system-toast" and row["resource_locale"] == row["locale"], "Route")
            transitions = reports["transitions"]["rows"]
            for tag in tags:
                for edge in [False, True]:
                    rows = [r for r in transitions if r["locale"] == tag and r["edge_to_edge"] == edge]
                    require([r["phase"] for r in rows] == ["initial", "ime", "restored", "shrink180", "shrink124", "expand", "same-layout", "expired"], "Phases")
                    require(len({r["node_identity"] for r in rows[:-1]}) == 1 and len({r["logical_text"] for r in rows[:-1]}) == 1, "Node/text")
                    require(rows[-1]["at_ms"] == 8001 and rows[-1]["toast_count"] == 0, "Expiry")
            nofit = [r for r in transitions if r.get("complete_layout_fits") is False]
            require(len(nofit) == 4 and all(r["body_height"] == 92 and r["complete_horizontal_height"] == 101 and r["phase"] == "shrink124" for r in nofit), "No-fit")
            for row in transitions + reports["ink"]["rows"]:
                if "pixels" in row:
                    pixels = row["pixels"]
                    require(pixels["parent_reference_pixel_equal"] and pixels["reference_guard_clear"] and pixels["reference_ink_pixels"] > 0, "Pixel controls")
                    require(pixels["reference_ink_pixels"] - pixels["clipped_ink_pixels"] == pixels["visible_ink_pixels"], "Pixel counts")
            for row in reports["ink"]["rows"]:
                require((row["pixels"]["clipped_ink_pixels"] > 0) == (row["kind"] == "unsupported-zwj"), "Ink cohort")
            events = reports["events"]["rows"]
            controls = [r for r in events if r["record_kind"] == "observer-controls"]
            require(len(controls) == 2 and all(r["explicit_announcement_observed"] and r["real_text_mutation_observed"] for r in controls), "Observer controls")
            requests = [r for r in events if r["record_kind"] == "event_request"]
            require(not any(r["event_type"] == 16384 and r["phase"] != "explicit-positive-control" for r in requests), "Unexpected announcement")
            require(not any(r["phase"] in ["same-layout", "shrink", "expand", "quiet-control"] for r in requests), "Geometry observation")
            same = [r for r in requests if r["phase"] == "same-text-assignment"]
            require(len(same) == (2 if api == 30 else 0), "Same-text API distinction")
    print("Verified saved PR35 evidence: 115 entries, 100 PNGs, 8 new/737 total JVM cases, lint 0, 94 existing installed cases. No Android rerun.")


if __name__ == "__main__":
    main()
