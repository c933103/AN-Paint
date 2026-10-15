#!/usr/bin/env python3
"""Validate the published entry-count data, without running application code.

Run from any directory with: python validate_entry_review.py
Optionally pass a directory containing the four current JSON data files.
This validates internal receipt/count/state/identity consistency. It does not
fetch source, certify translations, or run Android tests.
"""
import json
import sys
from pathlib import Path

def expected_state(receipt):
    changed = any(
        receipt["reviewed_" + kind + "_sha256"] != receipt["current_" + kind + "_sha256"]
        for kind in ("english", "localized")
    )
    return "needs_rereview" if changed or receipt.get("finding_status") == "open" else "reviewed_current"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def historical_partial_link_valid(partial, complete):
    """Allow preserved partial evidence only with an exact complete-review successor."""
    link = partial.get("superseded_by_complete_review", {})
    return (
        partial.get("partial_review_is_historical") is True
        and complete.get("review_scope", "").startswith("complete_")
        and link.get("cohort") == complete.get("cohort") != partial.get("cohort")
        and bool(link.get("source"))
        and link["source"] == complete.get("source")
        and all(
            link.get(kind + "_sha256")
            == partial.get("reviewed_" + kind + "_sha256")
            == complete.get("reviewed_" + kind + "_sha256")
            for kind in ("english", "localized")
        )
    )

def validate(directory):
    read = lambda name: json.loads((directory / name).read_text(encoding="utf-8"))
    receipts = read("entry-review-receipts.json")
    counts = read("entry-review-counts.json")
    identities = read("source-identities.json")
    validation = read("validation.json")
    revision = counts["source_revision"]
    require(all(x["source_revision"] == revision for x in (receipts, identities, validation)), "Source revisions disagree")
    keys = set(identities["resource_keys"])
    require(len(keys) == len(identities["resource_keys"]) == counts["denominator"]["total"], "Invalid source-key denominator")
    rows = counts["languages"]
    require(len({x["tag"] for x in rows}) == len(rows), "Duplicate language identity")
    by_tag = {x["tag"]: x for x in rows}
    pairs = {}
    for item in receipts["receipts"]:
        pair = (item["tag"], item["key"])
        require(pair not in pairs, "Duplicate active pair: " + str(pair))
        require(item["tag"] in by_tag and item["key"] in keys, "Unknown active identity/key")
        require(item["cohort"] in receipts["cohorts"], "Unknown cohort")
        require(item["state"] == expected_state(item), "Incorrect current/open classification: " + str(pair))
        pairs[pair] = item
    totals = {key: 0 for key in ("present", "reviewed_current", "needs_rereview", "unreviewed_or_unknown", "missing")}
    statuses = {}
    full = partial = empty = test_receipts = 0
    for row in rows:
        require(row["total"] == len(keys), "Row denominator differs")
        for state in ("reviewed_current", "needs_rereview"):
            expected = sorted(key for (tag, key), item in pairs.items() if tag == row["tag"] and item["state"] == state)
            require(expected == row[state + "_keys"], "Wrong key membership: " + row["tag"])
            require(len(expected) == row[state], "Wrong receipt count")
        require(all(isinstance(row[k], int) and row[k] >= 0 for k in totals), "Negative/noninteger count")
        require(row["present"] == row["reviewed_current"] + row["needs_rereview"] + row["unreviewed_or_unknown"], "Present partition mismatch")
        require(row["present"] + row["missing"] == row["total"], "Missing partition mismatch")
        for key in totals:
            totals[key] += row[key]
        statuses[row["language_status"]] = statuses.get(row["language_status"], 0) + 1
        if row["present"] == len(keys):
            full += 1
        elif row["present"]:
            partial += 1
        else:
            empty += 1
        if row["kind"] == "test_mode":
            test_receipts += row["reviewed_current"]
    summary = counts["summary"]
    require(all(summary[k] == value for k, value in totals.items()), "Aggregate mismatch")
    require(summary["total"] == len(rows) * len(keys), "Total denominator mismatch")
    require(summary["language_status_counts"] == statuses, "Status mismatch")
    require((summary["full_catalogues"], summary["partial_nonempty_catalogues"], summary["empty_catalogues"]) == (full, partial, empty), "Coverage mismatch")
    require(summary["test_mode_current_convention_receipts"] == test_receipts, "Test-mode mismatch")
    for item in receipts.get("partial_reviews", []):
        require(item["state"] == "partial_review_not_counted", "Unexpected partial state")
        complete = pairs.get((item["tag"], item["key"]))
        require(complete is None or historical_partial_link_valid(item, complete), "Partial evidence overlaps without an exact complete-review successor")
        require(item["tag"] in by_tag and item["key"] in keys, "Unknown partial identity/key")
    control = {"reviewed_english_sha256": "a", "current_english_sha256": "a", "reviewed_localized_sha256": "b", "current_localized_sha256": "b"}
    require(expected_state(control) == "reviewed_current", "Matching-hash control failed")
    require(expected_state(dict(control, finding_status="open")) == "needs_rereview", "Equal-hash open finding incorrectly accepted")
    require(expected_state(dict(control, current_localized_sha256="changed")) == "needs_rereview", "Changed-value control failed")
    require(expected_state(dict(control, current_localized_sha256="changed", finding_status="open")) == "needs_rereview", "Changed open control failed")
    partial_control = {"cohort": "partial", "reviewed_english_sha256": "a", "reviewed_localized_sha256": "b"}
    complete_control = dict(control, cohort="complete", source="receipt", review_scope="complete_linguistic")
    require(not historical_partial_link_valid(partial_control, complete_control), "Unmarked partial overlap incorrectly accepted")
    linked = dict(partial_control, partial_review_is_historical=True, superseded_by_complete_review={"cohort": "complete", "source": "receipt", "english_sha256": "a", "localized_sha256": "b"})
    require(historical_partial_link_valid(linked, complete_control), "Exact historical partial successor rejected")
    require(not historical_partial_link_valid(linked, dict(complete_control, reviewed_localized_sha256="changed")), "Mismatched historical partial hash accepted")
    require(not historical_partial_link_valid(linked, dict(complete_control, review_scope="delta_only")), "Partial successor accepted as complete")
    return {"source_revision": revision, "languages": len(rows), "entries": len(keys), "active_pairs": len(pairs), **totals}

if __name__ == "__main__":
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    print(json.dumps(validate(directory), indent=2))
