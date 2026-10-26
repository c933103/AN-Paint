# CA/RO P0 completion candidate verification

**All 110 frozen candidates pass source/data integrity checks**: 55 per locale in groups 28 + 16 + 11, against source `ce796879f4568a27b9d905a8e8db639dd0a93a30` and tree `f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c`.

This does not accept translations or implement source changes. Independent complete-value linguistic review is separate. The packet remains candidate-only.

## Results

- Reconstructed Git tree and all 1,376 raw tracked blobs agree; the current production inventory is 322 files.
- All 22 source bindings, 98 consumer windows and 150 inherited values per locale match; five explicit no-current-consumer holds remain absent per locale.
- Ordinary and Python `-O` output is byte-identical for all three receipts.
- 368 actual-packet mutations reject. This includes 26 refreshed-hash format mutations on the **two actual `formatted="false"` locale values**; those values contain no original format tokens.
- Separately labelled synthetic checks: 13 format-helper negatives plus one positive, and nine Git-tree/source-read negatives.
- The independent script uses Git's read-only `hash-object` CLI and ElementTree without importing the validator or its test helper.
- All 85 explicitly empty author-uncertainty lists are valid and preserved. Nonempty caveats, source notes and normalized original qualifications are preserved exactly. Preparation schema assumptions and their corrections are recorded separately, not reported as candidate defects.

## Reproduce

Use Python 3.9+ and Git. Set `SOURCE_ROOT` to a clean extraction/checkout of the pinned source, `TREE_FILE` to its full recursive Git tree JSON (not truncated), and `PACKET` to the candidate packet containing the corrected scope, foundations, correction ledger, six canonical candidate files and six original author-proposal JSONs. Input identities are in the packet and verification receipts.

```sh
python verify_candidates.py --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --packet "$PACKET" --out ordinary
python test_verifier.py --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --packet "$PACKET" --out ordinary
python independent_crosscheck.py --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --packet "$PACKET" --out ordinary
python -O verify_candidates.py --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --packet "$PACKET" --out optimized
python -O test_verifier.py --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --packet "$PACKET" --out optimized
python -O independent_crosscheck.py --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --packet "$PACKET" --out optimized
cmp ordinary/verification.json optimized/verification.json
cmp ordinary/mutation-controls.json optimized/mutation-controls.json
cmp ordinary/independent-crosscheck.json optimized/independent-crosscheck.json
```

The optional validator `--groups` argument emits an explicitly partial result and must not be reported as a full packet pass. Negative tests mutate only temporary packet/tree copies; the source corruption probe is an explicitly synthetic mocked read, not a changed source file. Structural scope probes explicitly rebind test-only expected metadata hashes to exercise source/context guards rather than merely a stale-checksum guard. There is no production bypass flag.

## Limits and provenance

No new native-human, physical-device, layout, runtime or whole-locale acceptance is claimed. Existing English composition labels and source routing remain unchanged; Valencian inheritance is distinct from direct CA/RO review. Five holds each, global 59/112, paired P1/frozen history, #56/#113/#159 and Help/archive/release pauses remain in place.

The earlier stale-label source notes are retained by the packet's correction history; current scope is `8dd3dd99b633bbec8254639797ddc81000ce4d8bfa9c037503663123587399d5`. No production candidate value was altered to satisfy validation.

`manifest.json` hashes all files in this verification directory except itself. Its external SHA-256 should be retained by the publishing record. JSON outputs and source text are unencoded, inspectable project evidence; no credentials, private links, unrelated data or execution-local paths are included.
