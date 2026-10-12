> SUPERSEDED PRE-PROJECTION-REPAIR REVIEW. Three real failures in historical composition/M02/M03 contracts were subsequently found in both full timeout logs. The focused 89+89 results and byte-scope checks below were accurate but incomplete, and do not accept that candidate. These hashes apply only to the earlier 11-file source snapshot.

# Independent glyph-bounds successor source review

**Disposition: PASS for bounded source, preservation and host-review checks. Android compilation, native rendering and installed repair acceptance remain UNRUN. No remaining source-publication blocker identified; root owns publication/readiness/merge.**

This review applies only to the 11 files pinned by `reviewed-source-manifest.json`, SHA256 `1b4f2c2b16cff9f88a8b856e6ab4c7de53039b6670d6305bf550ab1d97d85770`. The writer's source manifest is `40d3afd8abe7320bafbc198c0773360a123033ce36dd001487e8f7de0e223a85`. The immutable predecessor is head `e7855e04a1a4647a1fae3a14937df0c17c3f4d79`, tree `8752ed99c9350235da46fac1b4a188ca89296889`, failed run `38250189049`. No successor commit, tree or hosted run is asserted by this source report.

## Results

- **PASS:** all 2,008 predecessor leaves checked directly against their immutable Git blobs and executable bits. Exactly 2,002 are unchanged. Six changed files restore and replay byte-exactly in both directions through the pinned successor edits. Five new source/test/tool files are explicitly enumerated. All previous fixtures, verification records, fonts, licences, resources, catalogues, workflows and deadlines remain byte-identical.
- **PASS:** reviewer independently ran 89 focused methods normally (6.510s) and with `python -O` (7.387s), both process exit 0. These cover the new source and transport contracts, old painted-ink/diagnostic/composition oracles and runner adversarial controls. Negative-control `success:false` JSON after the unittest summary is expected test output, not a failed aggregate.
- **PASS:** independent byte-scope and evidence-inventory audits in normal and optimized Python. All 11 source pins remained unchanged after the checks.
- **PASS:** exact 892 inherited JVM identities, 104 expected API35 installed identities (74 library + 30 app; ordinary app partition 16), 181 planned ink triplets, four summaries and all 72 intended native mutant identities independently reconciled. These are expectations, not execution results.
- **PASS:** all 39 frozen failed-run review deliverables and their original manifest match exactly. Prior failed checkpoints remain failed. The new PNG decoder independently agrees with Pillow on all six selected historical native PNGs and recomputes the same three Arabic two-pixel failures. This checks decoder interoperability, not current repair efficacy.
- **UNRUN locally:** Kotlin/APK/test-APK compilation, Android lint, 892 JVM/native outcomes, 112 root captures, 28 diagnostics, 181 strict raster pairs, installed API35 receipts and both installed Arabic raster reports. No SDK/Gradle/adb/kotlinc is available. Fresh hosted results are required.

Writer full-suite evidence is recorded separately in `observed-writer-checks.json` when its frozen run completes; it is not represented as a reviewer-executed full aggregate.

## Technical assessment

The only production change selects a private status subclass on API35+ horizontal gallery routes. It enables bounds-based width calculation, explicitly disables global overhang shift, and uses one complete-message standard leading-margin span to reserve measured logical-start ink. The inset is absolute rather than cumulatively added, resets with the new message or width/paint/padding/direction signature, and allows at most three extra native measures under a 2em work bound. Plain text, accessibility string, font choice, provider behavior, timing and vertical/API30 routes are preserved.

Exact Android15 source supports this unshifted origin model. It also shows that the glyph-box API omits paragraph-margin positioning; the oracle therefore conservatively expands reference allocation by the exact known uniform span margin. This does not widen accepted content bounds. Every nonzero-alpha pixel is still checked, and whole-view ARGB equality is exact. The strict acceptance function is byte-identical to the predecessor. Complete text/UTF-16 lines, no ellipsis, accessibility, unsupported-feature rejection, view/layout flag agreement, parent reachability and existing vertical checks remain required.

Native controls preserve all six script groups at both scales and all 72 real canvas mutants. Added controls cover a separate original-plain Arabic before-view, no-growth remeasurement, narrower width, changed text size, mixed paragraph directions, a new short status and restoration. Their successful execution is still outstanding. The bounded algorithm is not claimed to fix arbitrary provider text, every font or every Android35+ framework revision.

The installed extension preserves the French/Mongolian checks and adds actual Arabic scale2 landscape status-view raster comparisons for both exact messages. It injects status text directly; it is not a network-failure route or hardware screenshot. Its bounded final-result transport cannot generate test status codes or manufacture success. The decoder verifies exact source-derived ordinary-app identities, strict JSON/base64/PNG structure, full images and zero-tolerance pixels. Both records, exact installed source/APK binding and the whole 104-identity audit are required.

## Review corrections resolved before freeze

1. Removed an inaccessible cross-module call to Paintroid's internal VerticalText from app/androidTest, replacing it with explicit public Arabic/profile checks.
2. Guarded the API35 subclass call in showStatus with an explicit SDK branch to avoid an older-API/lint hazard.
3. Closed decoder acceptance of a self-consistent test subset by deriving the ordinary-app identities from source bytes; a producer-only subset control now rejects it.

Earlier discussion also prevented treating the width setter alone as an established RTL repair and prevented additive use of a margin-omitting glyph box. See `SEMANTICS-REVIEW.md` and `primary-source-index.json` for the primary sources, exact upstream hashes and framework/Robolectric limitations.

## Reproduce

From the reviewed checkout, with `REVIEW` pointing to this report directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python "$REVIEW/audit_glyph_bounds_source.py" --repo . \
  --reviewed-manifest "$REVIEW/reviewed-source-manifest.json" \
  --manifest-sha256 1b4f2c2b16cff9f88a8b856e6ab4c7de53039b6670d6305bf550ab1d97d85770 \
  --output /tmp/glyph-source-result.json
PYTHONDONTWRITEBYTECODE=1 python "$REVIEW/audit_evidence_inputs.py" --repo . --output /tmp/glyph-inputs-result.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tools python -m unittest -v \
  test_commons_metadata_m04_glyph_bounds test_installed_glyph_ink_evidence \
  test_commons_metadata_m04_painted_ink test_commons_metadata_m04_diagnostic \
  test_commons_metadata_m04_composition test_run_android_instrumentation
```

Repeat those commands with `python -O`. To independently compare the new decoder with Pillow on the retained failed-run PNGs:

```sh
PYTHONDONTWRITEBYTECODE=1 python "$REVIEW/crosscheck_png_decoder.py" --repo . \
  --prior-evidence verification/commons-metadata-m04-glyph-bounds-2026-10-12/failed-painted-ink-run/observed-ink \
  --output /tmp/glyph-old-png-crosscheck.json
```

`HOSTED-ACCEPTANCE.md` gives the fresh exact-source/JUnit/raster/resource/installed gates. Signing, corresponding source and installability remain separate delivery checks. Root must bind any future artifact review to the actual newly published head, merge, tree and run without changing the frozen prior checkers.
