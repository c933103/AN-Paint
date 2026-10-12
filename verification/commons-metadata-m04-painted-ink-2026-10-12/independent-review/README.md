# Independent painted-ink successor source review

## Result

**PASS for the bounded source/design and portable host checks below. Native acceptance is UNRUN locally and remains required.** No remaining source blocker was found in the reviewed frozen six-file successor. This does not turn either prior failed JVM run green or establish that the new Kotlin helper compiles or passes.

The change is justified by the retained actual diagnostic pixels: the Ainu Kana normal-landscape COPY first-line advance exceeded width+1 by about 0.043 pixels, while the complete observed painted ink remained inside the content width. The underlying Android advance behavior is not diagnosed as a production defect. No production, wording, font, provider, threshold, timing, workflow or prior HTTP semantics change is included here.

## Exact binding and preservation

Baseline: diagnostic tree `4ff7f479ffc73964fa8756b6c7e3202f624ad0f1` (PR55 head `dc46abc2add7984358565a88fe65c5278212dcf6`). The independently reviewed flow SHA is `44651d7001dcc01ba37a7c7ff0b650785fa9b4204f4bcc75e6fcabd7e67e8816`; new successor fixture SHA is `3e7fb249d1334ee1bb9b0ecbe647a9a34b83452e248e772854a40e7721a9efdf`.

`audit_ink_source.py` read every actual immutable Git blob and working file. All 1,975 baseline leaves and executable modes were checked: 1,972 are byte-identical, and exactly three changed files reverse to their actual immutable baseline blobs. Those files are the flow test and two historical diagnostic adapters. There are exactly three new source files: a pinned inverse fixture, its helper and seven host contracts. All existing production, catalogues, fonts/licences, historical manifests, fixtures and evidence remain byte-identical. All 16 old flow methods remain; exactly two explicit native-control methods are added. The new explicit JVM inventory contains the frozen 890 identities plus those two, without deletion, duplication or rewriting the old inventory.

`reviewed-source-manifest.json` binds all six source paths plus the new inventory and historical failure-copy receipt. `reviewed-three-file.diff` is the exact existing-file delta. `source-scope-result.json` contains actual endpoint hashes and new-evidence inventory. Final publication head/merge/tree/run bindings are deliberately not guessed here.

## Oracle assessment

Only the short-landscape horizontal advance assertion changes. The old advance formula remains in diagnostic output. Portrait assertions, the vertical route, full message/accessibility checks, UTF-16 line coverage, ellipsis checks, measured height, parent visibility, scrolling and restored reading-start checks remain enforced. The pinned successor projections recover the old failed assertion and both earlier source endpoints exactly. New live-source checks reject rollback, missing/duplicated/corrupted edits and unrelated changes; historical tests receive the exact recovered historical bytes rather than silently repinned fixtures.

The complete native Layout reference is independent of the actual TextView's clipped bitmap. Reference allocation uses actual glyph bounds plus all line extents and layout bounds, rounded outward with an allocation border. The helper guards its plain horizontal API35 scope and fails on unsupported drawing features, nonfinite/oversized geometry or edge contact. It scans all nonzero-alpha reference pixels, including marks outside nominal line boxes, and requires strict containment plus exact whole-view ARGB equality. There is no raised allowance, alpha cutoff, ignored border or color tolerance. Actual placement is derived from padding/baseline and checked TOP/zero-scroll geometry.

The six native controls per locale/scale cover boundary crossing, wholly displaced text and genuine first/last spatial ink clipping. Intact views must pass first; mutants must retain reference ink, actually overflow/remove ink, and fail for the specifically intended reason. Clipped references must equal the intact complete reference. Six script profiles at both scales cover Latin, combining Ainu, Tibetan, RTL Arabic, Japanese and bundled Nôm. Their execution and pixel receipts remain an essential unrun gate, not a fact proved by source tokens.

## Review correction resolved

The initial candidate offset the RectF returned by `computeDrawingBoundingBox()` directly. A native `BoringLayout` can return cached bounds, so that could mutate layout state during controls. The reviewed candidate copies the RectF before offsetting and verifies cached bounds, view/layout/line geometry, key paint state, text and accessibility remain unchanged after each mutant. Outcome metadata also now explicitly describes the current painted-ink oracle and leaves the original advance booleans diagnostic. These were resolved before the final frozen aggregate, not waived.

## Executed checks

- Independent full baseline byte/mode inventory and exact reverse-endpoint audit: PASS.
- New painted-ink + historical diagnostic + PR52/M04 composition host contracts: 22/22 PASS normally, 22/22 PASS with Python `-O`.
- Additional localized-dialog stacked projection contracts: 7/7 PASS normally.
- Writer's final full aggregate: 673/673 in 222.535 seconds, OK and saved PROCESS_EXIT_CODE=0. Catalogue structure also passed with saved exit 0; optimized focused contracts report 39/39. Exact log hashes and the final source binding are in `observed-writer-checks.json`. These are inspected writer evidence, not an independently repeated full suite. Later error JSON in the full log comes from deliberate negative controls, not a failed aggregate.

Reproduce from any equivalent checkout containing the immutable baseline Git tree:

```
python3 audit_ink_source.py --repo /path/to/checkout --output source-scope-result.json
cd /path/to/checkout
PYTHONPATH=tools python3 -m unittest -v tools.test_commons_metadata_m04_painted_ink tools.test_commons_metadata_m04_diagnostic tools.test_commons_metadata_m04_composition
PYTHONPATH=tools python3 -O -m unittest -v tools.test_commons_metadata_m04_painted_ink tools.test_commons_metadata_m04_diagnostic tools.test_commons_metadata_m04_composition
PYTHONPATH=tools python3 -m unittest -v tools.test_localized_dialog_composition
```

## API and runtime limits

The [official Layout API](https://developer.android.com/reference/android/text/Layout#computeDrawingBoundingBox()) exposes actual-glyph drawing bounds from API35. The inspected [Android35 source](https://android.googlesource.com/platform/prebuilts/fullsdk/sources/+/refs/heads/androidx-constraintlayout-release/android-35/android/text/Layout.java), blob `c674968bba8a7b3ffc854167b46db36385e461ab`, computes line glyph bounds, includes baselines and handles RTL placement. Its width-bounds getter supports the candidate's explicit overhang-mode guard. This validates the chosen API contract within the restricted scope, not the runtime implementation's correctness for every script.

There is no local Android SDK, Gradle, adb or Kotlin compiler. Local Kotlin compilation, native graphics execution, actual positive/control images, API35 installed tests and successor CI are UNRUN. No universal rendering/shaping guarantee follows from a shared native Layout reference; the oracle tests clipping/placement preservation, while inherited text/resource/font tests and inspected real render pixels cover their separate claims. The finite reference relies on API35's glyph-bound contract and fail-closed scope restrictions, not an arbitrary finite margin alone.

`HOSTED-ACCEPTANCE.md` requires fresh exact-source 892/892 JVM identities, all 112 success pairs, 28 diagnostic profiles, 120 paired ink frames (48 positive, 72 negative), two native control summaries, raw pixel/count recomputation, compiled resource/script controls, packaged font/source equality and separate device/delivery results. The old frozen 890/111 artifact checker must not be rebound.
