#!/usr/bin/env python3
"""Validate saved post-merge PR35 evidence with the Python standard library.

This does not execute Android, authenticate GitHub provenance, certify speech,
or replace the original full JUnit XML, final run/job receipts or visual review.
Inventory fingerprints pin names from the premerge cohort's identical tree;
they do not import its results or timings into this distinct execution.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import math
import struct
import xml.etree.ElementTree as ET
import zipfile
import zlib

RUN = 37978574286
MERGE = "7e8a0d2377693a35cd9392f2082ef88548a6f67f"
TREE = "7d4245411d699a3cf59018ce8c6d4cb87940dc60"
SOURCE = "768959d1aa580ed88beb26abf99db597cf998f5d"
TAGS = ["mn-Mong", "mnc-Mong", "lzh-Hant", "en-XV", "qaa-Zsye-XV"]
KINDS = ["routes", "transitions", "events", "ink"]
PHASES = ["initial", "ime", "restored", "shrink180", "shrink124", "expand", "same-layout", "expired"]
CLASS = "org.catrobat.paintroid.local.VerticalNoticeResizeCharacterizationTest"
METHODS = [
    "currentRendererNominalFitIsNotAnInkContainmentOracle",
    "accessibilityObserverSeesControlsAndSeparatesInitialContentFromGeometryEvents",
    "unchangedHorizontalDirectHelperKeepsNodeTextAndDeadlineAcrossRepeatedGeometryChanges",
    "compiledAppResourcesKeepFiveVerticalProfilesOnSystemToasts",
]
JVM_NAMES = "b4bbf28a9095e6d36aebc25bc5be7a7d08490e568e74ebd8c0b217e0576f5f51"
DEVICE = {
    "Paintroid/androidTest-results/summary.json": (74, "af66d92ec794d5d61f0ec301eec5e4b01b55fea6e1b1906e252be1279034e501"),
    "app/accepted-credit-restart/seed/summary.json": (1, "98c178ea29a669dd2ac966c2ea1857a3d021282dc5e5f4747632d78364ddd9d2"),
    "app/accepted-credit-restart/verify/summary.json": (1, "0ddcd1a0d4725d1dc6c5c9d0ef4e090c19663bb0d002c0c8b0e2441dee56fe8b"),
    "app/androidTest-results/summary.json": (18, "63331fd28640a913cedced49037b9ad2d0cb4304dbe95ea7c99909787cf39d9e"),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def bad_constant(value):
    raise ValueError("Non-finite JSON: " + value)


def read_json(data):
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=bad_constant)


def fingerprint(names):
    return hashlib.sha256(json.dumps(sorted(names), ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def finite_nonnegative(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def png_ink(data, name):
    """Decode this fixture's 8-bit RGBA, noninterlaced PNG and count alpha ink."""
    require(data[:8] == b"\x89PNG\r\n\x1a\n", name + ": signature")
    offset, chunks, compressed = 8, [], bytearray()
    while offset < len(data):
        require(offset + 12 <= len(data), name + ": truncated chunk")
        length, kind = struct.unpack(">I4s", data[offset:offset + 8])
        require(offset + 12 + length <= len(data), name + ": truncated payload")
        payload = data[offset + 8:offset + 8 + length]
        crc = struct.unpack(">I", data[offset + 8 + length:offset + 12 + length])[0]
        require(zlib.crc32(kind + payload) & 0xffffffff == crc, name + ": chunk CRC")
        chunks.append((kind, payload))
        if kind == b"IDAT":
            compressed.extend(payload)
        offset += length + 12
        if kind == b"IEND":
            require(length == 0 and offset == len(data), name + ": end")
            break
    require(chunks and chunks[0][0] == b"IHDR" and len(chunks[0][1]) == 13, name + ": IHDR")
    require(sum(k == b"IHDR" for k, _ in chunks) == 1 and chunks[-1][0] == b"IEND", name + ": structure")
    width, height, depth, color, comp, filtering, interlace = struct.unpack(">IIBBBBB", chunks[0][1])
    require(0 < width <= 4096 and 0 < height <= 4096, name + ": dimensions")
    require((depth, color, comp, filtering, interlace) == (8, 6, 0, 0, 0), name + ": expected RGBA encoding")
    require(compressed, name + ": missing IDAT")
    stream = zlib.decompressobj()
    expected_size = height * (1 + 4 * width)
    raw = stream.decompress(bytes(compressed), expected_size + 1)
    require(stream.eof and not stream.unused_data and not stream.unconsumed_tail
            and len(raw) == expected_size, name + ": compressed scanlines")
    stride, previous, ink = width * 4, bytearray(width * 4), 0
    for y in range(height):
        pos = y * (stride + 1)
        mode, current = raw[pos], bytearray(raw[pos + 1:pos + 1 + stride])
        require(mode in range(5), name + ": filter")
        for x in range(stride):
            a, b, c = (current[x - 4] if x >= 4 else 0), previous[x], (previous[x - 4] if x >= 4 else 0)
            if mode == 0:
                prediction = 0
            elif mode == 1:
                prediction = a
            elif mode == 2:
                prediction = b
            elif mode == 3:
                prediction = (a + b) // 2
            else:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                prediction = a if pa <= pb and pa <= pc else b if pb <= pc else c
            current[x] = (current[x] + prediction) & 255
        ink += sum(alpha != 0 for alpha in current[3::4])
        previous = current
    require(ink > 0, name + ": empty image")
    return ink


def pixel_controls(row):
    p = row["pixels"]
    require(p["parent_reference_pixel_equal"] is True and p["reference_guard_clear"] is True, "Pixel controls")
    require(all(type(p[k]) is int and p[k] >= 0 for k in ["reference_ink_pixels", "visible_ink_pixels", "clipped_ink_pixels"]), "Pixel types")
    require(p["reference_ink_pixels"] > 0 and p["reference_ink_pixels"] - p["clipped_ink_pixels"] == p["visible_ink_pixels"], "Pixel arithmetic")
    return p


def verify(here):
    manifest = read_json((here / "artifact-manifest.json").read_bytes())
    summary = read_json((here / "summary.json").read_bytes())
    for key, value in {"schema": 1, "pr": 35, "source_head": SOURCE, "tested_merge": MERGE,
                       "tested_tree": TREE, "run_id": RUN, "run_attempt": 1}.items():
        require(summary[key] == value, "Pinned cohort: " + key)
    require(summary["cohort"] == "post-merge push run; independent execution from premerge run 37974245255", "Cohort description")
    require(manifest["schema"] == 1, "Manifest schema")
    archive = here / "characterization-evidence.zip"
    require(hashlib.sha256(archive.read_bytes()).hexdigest() == manifest["zip_sha256"], "ZIP hash")
    pngs = {f"characterization/api{api}-{tag}-{edge}-shrink124-{part}.png"
            for api in [30, 35] for tag in TAGS for edge in ["false", "true"] for part in ["reference", "parent"]}
    pngs |= {f"characterization/api{api}-{tag}-{kind}-{part}.png"
             for api in [30, 35] for tag in TAGS for kind in ["unsupported-zwj", "ordinary-emoji", "joined-word"]
             for part in ["reference", "parent"]}
    reports = {f"characterization/api{api}-{kind}.json" for api in [30, 35] for kind in KINDS}
    expected = pngs | reports | {"device/" + path for path in DEVICE} | {
        "VerticalNoticeResizeCharacterizationTest.xml", "lint-results-debug.xml", "jvm-inventory.json"}
    require(len(pngs) == 100 and len(reports) == 8 and len(expected) == 115, "Internal expected inventory")
    entries = {item["path"]: item for item in manifest["files"]}
    require(len(entries) == len(manifest["files"]) == 115 and set(entries) == expected, "Exact manifest inventory")
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, "ZIP CRC")
        require(len(z.namelist()) == 115 and set(z.namelist()) == expected, "Exact ZIP inventory")
        data = {}
        for name, item in entries.items():
            require(not name.startswith("/") and ".." not in PurePosixPath(name).parts and "\\" not in name, "Unsafe path")
            content = z.read(name)
            require(len(content) == item["bytes"] and hashlib.sha256(content).hexdigest() == item["sha256"], name + ": hash/size")
            require(item["provenance"] == ("derived inventory" if name == "jvm-inventory.json" else "original CI bytes"), name + ": provenance label")
            data[name] = content
    decoded = {name: png_ink(data[name], name) for name in sorted(pngs)}
    cases = ET.fromstring(data["VerticalNoticeResizeCharacterizationTest.xml"])
    require(cases.tag == "testsuite" and cases.get("name") == CLASS, "New JUnit class")
    require(cases.get("tests") == "8" and all(cases.get(k) == "0" for k in ["failures", "errors", "skipped"]), "New JUnit status")
    rows = cases.findall("testcase")
    names = [(row.get("classname"), row.get("name")) for row in rows]
    require(len(rows) == 8 and set(names) == {(CLASS, method + suffix) for method in METHODS for suffix in ["", "[30]"]}, "Exact eight new cases")
    require(all(not any(row.find(k) is not None for k in ["failure", "error", "skipped"]) for row in rows), "New individual case status")
    inventory = read_json(data["jvm-inventory.json"])
    keys = [(row["class"], row["name"]) for row in inventory]
    require(len(keys) == len(set(keys)) == 737 and fingerprint(keys) == JVM_NAMES, "Exact unique full JUnit inventory")
    require(all(finite_nonnegative(row["seconds"]) for row in inventory), "JUnit times")
    indexed = {(row["class"], row["name"]): row for row in inventory}
    require(all(indexed[(row.get("classname"), row.get("name"))]["seconds"] == float(row.get("time")) for row in rows), "JUnit/inventory times")
    require(summary["new_case_seconds"] == float(cases.get("time")) and finite_nonnegative(summary["new_case_seconds"]), "Summary JUnit time")
    lint = ET.fromstring(data["lint-results-debug.xml"])
    require(lint.tag == "issues" and not lint.findall(".//issue"), "Lint")
    for key, value in {"jvm_tests": 737, "jvm_failures": 0, "jvm_errors": 0, "jvm_skipped": 0,
                       "new_cases": 8, "lint_issues": 0, "installed_api35_tests": 94}.items():
        require(summary[key] == value, "Summary count: " + key)
    partitions, device_names = [], []
    for path, (count, digest) in sorted(DEVICE.items()):
        record = read_json(data["device/" + path])
        require(record["success"] is True and all(record[k] == [] for k in ["missing", "unexpected", "errors"]), path + ": outcome")
        require(record["returncode"] == 0 and record["timed_out"] is False, path + ": process")
        require(record["expected_tests"] == record["completed_tests"] == len(record["cases"]) == count, path + ": count")
        require(all(row["status"] == "passed" for row in record["cases"]), path + ": status")
        keys = [(row["classname"], row["name"]) for row in record["cases"]]
        require(len(keys) == len(set(keys)) and fingerprint(keys) == digest, path + ": exact inventory")
        device_names.extend(keys)
        require(finite_nonnegative(record["elapsed_seconds"]), path + ": time")
        partitions.append({"path": path, "tests": count, "elapsed_seconds": record["elapsed_seconds"]})
    require(len(device_names) == len(set(device_names)) == 94, "Unique installed inventory")
    require(summary["device_partitions"] == partitions, "Partition summary")
    require(set(summary["new_characterization"]) == {"30", "35"}, "Summary APIs")
    for api in [30, 35]:
        records = {kind: read_json(data[f"characterization/api{api}-{kind}.json"]) for kind in KINDS}
        for kind, record in records.items():
            require(record["schema"] == 1 and record["completed"] is True and record["build_commit"] == MERGE
                    and str(record["run_id"]) == str(RUN) and record["production_vertical_route"] is False, kind + ": metadata")
            require(record["evidence_kind"] == "Compiled-resource Robolectric NATIVE characterization; not installed execution or TalkBack speech", kind + ": scope")
            require(all(row["api"] == api and row["locale"] in TAGS for row in record["rows"]), kind + ": API/locale")
        routes = records["routes"]["rows"]
        require(len(routes) == 10 and {(r["locale"], r["kind"]) for r in routes}
                == {(tag, kind) for tag in TAGS for kind in ["combined", "joined-emoji-save"]}, "Exact route matrix")
        route_map = {(r["locale"], r["kind"]): r for r in routes}
        for row in routes:
            require(row["route"] == "system-toast" and row["resource_locale"] == row["locale"], "Route/resource")
            require(row["direction"] == ("VERTICAL_RL" if row["locale"] in ["lzh-Hant", "qaa-Zsye-XV"] else "VERTICAL_LR"), "Direction")
            require(row["configured_face"] == ("fonts/notosansmongolian.ttf" if row["locale"] in ["mn-Mong", "mnc-Mong"] else None), "Configured face")
            require(isinstance(row["text"], str) and row["text"], "Logical route text")
        transitions = records["transitions"]["rows"]
        require(len(transitions) == 80, "Transition count")
        for tag in TAGS:
            for edge in [False, True]:
                group = [r for r in transitions if r["locale"] == tag and r["edge_to_edge"] is edge]
                require([r["phase"] for r in group] == PHASES, "Exact phases")
                require(all(r["original_expiry_ms"] == 8000 for r in group), "Unchanged deadline")
                require(len({r["node_identity"] for r in group[:-1]}) == 1 and len({r["notice_identity"] for r in group[:-1]}) == 1, "Stable node/notice")
                require(all(r["logical_text"] == route_map[(tag, "combined")]["text"] for r in group[:-1]), "Stable logical text")
                require(group[-1]["at_ms"] == 8001 and group[-1]["toast_count"] == 0, "Expiry/no replay")
                times = [r["at_ms"] for r in group]
                require(all(type(t) is int and t >= 0 for t in times) and times == sorted(times) and times[-2] < 8000, "Phase times")
                for row in group[:-1]:
                    require(row["last_line_end"] == len(row["logical_text"].encode("utf-16-le")) // 2, "Complete logical layout")
                    require(row["complete_layout_fits"] is (row["complete_horizontal_height"] <= row["body_height"]), "Fit arithmetic")
                    p = pixel_controls(row)
                    if row["phase"] == "shrink124":
                        stem = f"characterization/api{api}-{tag}-{str(edge).lower()}-shrink124"
                        require(decoded[stem + "-reference.png"] == p["reference_ink_pixels"]
                                and decoded[stem + "-parent.png"] == p["visible_ink_pixels"], "Horizontal PNG/count agreement")
        nofit = [r for r in transitions if r.get("complete_layout_fits") is False]
        require(len(nofit) == 4 and {(r["locale"], r["edge_to_edge"]) for r in nofit}
                == {(tag, edge) for tag in ["mn-Mong", "mnc-Mong"] for edge in [False, True]}, "Exact no-fit matrix")
        require(all(r["phase"] == "shrink124" and r["body_height"] == 92 and r["complete_horizontal_height"] == 101
                    and r["pixels"]["clipped_ink_pixels"] > 0 for r in nofit), "No-fit/lost ink")
        ink = records["ink"]["rows"]
        require(len(ink) == 15 and {(r["locale"], r["kind"]) for r in ink}
                == {(tag, kind) for tag in TAGS for kind in ["unsupported-zwj", "ordinary-emoji", "joined-word"]}, "Exact ink matrix")
        for row in ink:
            p = pixel_controls(row)
            require(row["nominal_fits"] is True and math.ceil(row["nominal_width"]) <= row["safe_width"]
                    and math.ceil(row["nominal_height"]) <= row["safe_height"], "Nominal fit")
            require(row["scope"] == "test-only vertical drawing child through unchanged Notice", "Ink scope")
            require((p["clipped_ink_pixels"] > 0) == (row["kind"] == "unsupported-zwj"), "Ink/ordinary controls")
            stem = f"characterization/api{api}-{row['locale']}-{row['kind']}"
            require(decoded[stem + "-reference.png"] == p["reference_ink_pixels"]
                    and decoded[stem + "-parent.png"] == p["visible_ink_pixels"], "Vertical PNG/count agreement")
            if row["kind"] == "unsupported-zwj":
                require(row["logical_text"] == route_map[(row["locale"], "joined-emoji-save")]["text"], "Saved logical text")
        events = records["events"]["rows"]
        require(all(r["record_kind"] in ["observer-controls", "event_request"] for r in events), "Event record kinds")
        controls = [r for r in events if r["record_kind"] == "observer-controls"]
        requests = [r for r in events if r["record_kind"] == "event_request"]
        require(len(controls) == 2 and {r["locale"] for r in controls} == {"mn-Mong", "lzh-Hant"}, "Observer matrix")
        require(len(events) == (10 if api == 30 else 8), "Bounded event row count")
        require(not any(r["phase"] in ["same-layout", "shrink", "expand", "quiet-control"] for r in requests), "Geometry/quiet observation")
        require(not any(r["event_type"] == 16384 and r["phase"] != "explicit-positive-control" for r in requests), "Unexpected announcement")
        require(all(r["locale"] in ["mn-Mong", "lzh-Hant"] for r in requests), "Event request locales")
        for control in controls:
            tag = control["locale"]
            group = [r for r in requests if r["locale"] == tag]
            require(len(group) == (4 if api == 30 else 3)
                    and all(r["phase"] in ["explicit-positive-control", "same-text-assignment",
                                          "changed-text-positive-control"] for r in group), "Per-locale bounded event matrix")
            require(control["explicit_announcement_observed"] is True and control["real_text_mutation_observed"] is True
                    and control["toast_count"] == 0 and control["event_count"] == len(group), "Observer summary")
            require(len({r["source_identity"] for r in group}) == 1
                    and all(type(r["source_identity"]) is int and r["source_tag"] == "locale_notification_text" for r in group), "Event source")
            positive = [r for r in group if r["phase"] == "explicit-positive-control"]
            require(len(positive) == 1 and positive[0]["event_type"] == 16384
                    and "notice-observer-positive-" + tag in positive[0]["event_text"]
                    and positive[0]["source_logical_text"] == route_map[(tag, "combined")]["text"], "Announcement payload/source")
            changed = [r for r in group if r["phase"] == "changed-text-positive-control"]
            require(len(changed) == 2 and all(r["source_logical_text"] == route_map[(tag, "combined")]["text"]
                                   + "\nobserver replacement" for r in changed), "Changed-text payload")
            require(any(r["event_type"] == 16 or r["event_type"] == 2048 and r["content_change_types"] & 2 for r in changed), "Text-change event control")
            same = [r for r in group if r["phase"] == "same-text-assignment"]
            require(len(same) == (1 if api == 30 else 0), "Per-locale same-text API distinction")
            require(all(r["event_type"] == 2048 and r["content_change_types"] & 2
                        and r["source_logical_text"] == route_map[(tag, "combined")]["text"] for r in same), "Same-text event type/payload")
        derived = {
            "routes": 10, "transition_rows": 80, "event_rows": len(events), "pixel_rows": 15, "pngs": 50,
            "horizontal_no_fit": [{k: r[k] for k in ["locale", "edge_to_edge", "phase", "body_height", "complete_horizontal_height"]}
                                  | {"clipped_ink_pixels": r["pixels"]["clipped_ink_pixels"]} for r in nofit],
            "joined_emoji_clipped_ink": {r["locale"]: r["pixels"]["clipped_ink_pixels"] for r in ink if r["kind"] == "unsupported-zwj"},
            "ordinary_controls_no_clip": 10, "same_text_content_change_requests": 2 if api == 30 else 0,
            "geometry_only_requests": 0, "observer_control_summaries": controls,
        }
        require(summary["new_characterization"][str(api)] == derived, "Derived characterization summary")
    print("Verified saved post-merge cohort 37978574286: exact 115 entries, 8 JSON, 100 decoded nonempty RGBA PNGs with report-matched ink counts, 8 new/737 unique JVM inventory, lint 0, 94 existing installed cases. No Android rerun or GitHub-provenance certification.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    verify(parser.parse_args().directory)
