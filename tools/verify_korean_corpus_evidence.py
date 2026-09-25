#!/usr/bin/env python3
"""Verify reviewed occurrence coordinates against the external, pinned corpus.

This is an evidence checker, not a translation or script-conversion generator.
The large corpus is deliberately not bundled with AN Paint. See
translations/KOREAN_SCRIPT_REVIEW.md for its URL, scope, and licensing.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
GONGU_SHA256 = "b689360119c1fc68c2dbcfdabc27589997e2a54a988051739c1644634db1785c"
ANNOTATION = re.compile(r"([가-힣]{2,8})[（(]([\u3400-\u9fff\uf900-\ufaff]{2,8})[)）]")


def read_tsv(name):
    with (ROOT / "translations" / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    if digest.hexdigest() != GONGU_SHA256:
        raise ValueError("Corpus hash differs from the reviewed pinned snapshot")

    review = read_tsv("KOREAN_CORPUS_OCCURRENCES.tsv")
    app_pairs = {(row["hangul"], row["hanja"])
                 for row in read_tsv("KOREAN_HANJA_REVIEW.tsv")}
    wanted = {row["record_id"] for row in review}
    records = {}
    matched_pairs = set()
    occurrences = 0
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            if record["id"] in wanted:
                if record["id"] in records:
                    raise ValueError(f"Duplicate record: {record['id']}")
                records[record["id"]] = line_number, record
            if record.get("language") not in ("Korean", "Modern Korean", "Early Modern Korean"):
                continue
            for match in ANNOTATION.finditer(record["text"]):
                if len(match[1]) != len(match[2]):
                    continue
                occurrences += 1
                pair = match[1], unicodedata.normalize("NFKC", match[2])
                if pair in app_pairs:
                    matched_pairs.add(pair)

    for row in review:
        line_number, record = records[row["record_id"]]
        assert line_number == int(row["jsonl_line"]), row
        span = record["text"][int(row["text_start"]):int(row["text_end"])]
        assert span == row["published_span"], row
        match = ANNOTATION.fullmatch(span)
        assert match and match[1] == row["hangul"], row
        assert unicodedata.normalize("NFKC", match[2]) == row["hanja"], row
        assert (row["hangul"], row["hanja"]) in app_pairs, row
        assert record["url"] == row["source_url"], row
        assert record["copyright_status"] == "Public Domain", row
        assert row["status"] in ("accepted_occurrence", "rejected_ui_sense"), row

    accepted = sum(row["status"] == "accepted_occurrence" for row in review)
    print(f"Verified {len(review)} source spans in {len(records)} records: "
          f"{accepted} accepted occurrences, {len(review) - accepted} rejected UI senses")
    print(f"Extraction: {occurrences} annotated occurrences; "
          f"{len(matched_pairs)}/{len(app_pairs)} app pairs found before contextual review")
    print("Coordinates verified; semantic decisions remain the recorded human-readable review.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gongu_jsonl", type=Path, help="Downloaded pinned gongu.jsonl")
    verify(parser.parse_args().gongu_jsonl)
