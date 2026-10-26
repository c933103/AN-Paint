# Catalan/Romanian P0 completion — independent reviewed values

**All 110 complete values have bounded independent AI linguistic/source-static outcomes:** Catalan 53 unchanged accepts + two exact revisions; Romanian 54 unchanged + one revision; no new holds. The three revisions clarify failed recovery moves and a destination-replacement error shared by encoding and decoding.

Source is pinned to `ce796879f4568a27b9d905a8e8db639dd0a93a30`, tree `f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c`. Exact per-value final strings, hashes, reviewer receipts and source bindings are in `approved-manifest.json` and `review/`. Each locale reviewer independently checked 55 values, 150 inherited pairs, 22 source bindings / 98 windows and all 1,376 source blobs. Both provide 13 static composition examples; these are not executed runtime cases.

Original author pending-review phrases are retained verbatim as historical proposal provenance. Current explicit independent verdicts and final strings are authoritative for this bounded review; the original semantic caveats remain applicable. Whole-value acceptance does not certify all dynamic English reasons, mixed labels, parent-language inheritance, native-human correctness, layout or physical devices.

The three exact revisions were reconciled with production source: AutosaveStore throws on missing source or failed move to a separate ZIP; neither negative wording promises preservation. TextImageCodec.replace serves decoding as well as Base64/ASCII encoding, so Catalan uses “fitxer resultant” without narrowing its meaning.

## Implementation boundary

`reconcile_and_apply.py` verifies manifest and receipt hashes, exact candidate/source joins, all complete-value hashes/attrs/tokens and missing-only scope, then emits the reviewed XML and test fixture. Run it against a clean pinned source with `--packet` pointing to r01-candidates/packet, `--review` to this review directory, `--base-source` to that source, `--output` to an implementation copy, and `--receipt` to the resulting manifest. This produces only two resource changes and one fixture; host/JVM tests and current-only warning resolver integration are separate source-PR work.

All 300 inherited values and attributes stay unchanged. The resulting local resource counts are 205 each, P0 87/92, with five no-current-consumer holds per locale still absent. Those are structural counts, not whole-language acceptance. No direct Valencian value is added; inherited routing remains separate. The paired 120-entry/60-tag warning oracle, P1/frozen evidence, global 59/112, PR56 never-merge, PR113/159, Help callback/archive identity and release pauses are unchanged.

This records reviews and reproducible application only. Source PR publication, exact-head Codex, required CI and actual postmerge verification are subsequent evidence; this record claims none of those gates passed. No release.
