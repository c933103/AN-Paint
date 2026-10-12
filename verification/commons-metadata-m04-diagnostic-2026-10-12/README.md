# PR55 normal-landscape failure: diagnostic successor

This checkpoint improves failure evidence. It is **not a production repair** and
has no local Android execution or acceptance claim.

## Preserved failure

- Public PR55 head: `b95c9a682c77f5dfa9b9a1f4eacabd9d9a03265a`.
- Exact reviewed/failed source tree: `d80218496e45bbefcaa378d40e5cd9846b7988ee`.
- Run [38239121942](https://github.com/c933103/AN-Paint/actions/runs/38239121942)
  tested synthetic merge `14b1fdf8e02ebe6f765d63906f05c7e808524b76`, whose tree
  matches that reviewed source. The PR52 parent remains
  `71f4d288669858e7975ec4c094b7f47a9a1ff145`.
- Exact JVM inventory: 890 executed, 889 passed, one failed; no missing, extra,
  duplicate or skipped identity. The failed XML is retained unchanged here.
- Failure: `CommonsMetadataQueryFailureFlowTest.shortLandscapeM04RetainsFullAccessibleTextAtNormalScale`,
  original source line 398. The condition was and remains
  `layout.getLineLeft(line)>=-1f && layout.getLineRight(line)<=layout.width+1f`.
- The first failing profile is inferred from the source loop and artifact boundary:
  `ain-Kana`, COPY, 640×320 dp, font scale 1.0. Only preceding `en-GB` has the
  normal-landscape capture. All 28 profiles in each of the other three rendering
  methods completed, leaving 85 of the planned 112 PNG/JSON pairs.

The original failing profile had no saved line metrics or pixels because its
capture followed the assertion. Successful Ainu normal-portrait and double-scale
landscape pixels show the same complete text; they do not establish the geometry
of the failed normal-landscape case. The root cause remains unestablished.
Nothing here labels it a fixture error, glyph clipping, or a platform line-breaking
bug without the required measurements.

## Narrow source change

The existing flow test keeps all 16 methods, with the complete JVM inventory
remaining **890**. No production file, translation, font, expected localized
string, old threshold, completeness gate, deadline or workflow is changed.

For each of the 28 normal-landscape profiles, before the geometry assertions, the
successor records under `build/reports/commons-metadata-m04-diagnostic/`:

1. The real root-window native-rendered PNG.
2. The same native `Layout` drawn on a transparent expanded canvas, without
   changing production text, typography, dimensions or break strategy.
3. Per-line text ranges, left/right/max/width advances, line boxes, ellipses,
   the original guard result, and observed ink bounds/outside-layout pixels.
4. View/content/layout/window geometry, actual resource and text locales,
   text size, scale, break strategy, hyphenation and parent scroll positions.
5. Edge-contact flags on the finite expanded raster. A touched outer edge can
   mean that the diagnostic canvas itself clips ink. Per-line ink counts cover
   the native line boxes only; the retained pixels remain necessary evidence.

Each profile still runs the unchanged assertions. An `AssertionError` is collected
only after its metadata action finished and the ordinary `withGallery` cleanup
ran. Setup/in-flight failure remains fail-fast. Later safe profiles are attempted
once; the original failed action is never retried. The method fails after the loop
if **any** profile failed. `normal-landscape-outcomes.json` records the attempted
completed profiles and failures; original JUnit remains authoritative.

The original success-capture path stays distinct from diagnostics. Its vertical
capture now performs the layout requested by `resetToReadingStart()` and asserts
the resulting reading-start scroll position before drawing; its JSON records
`status_parent_scroll_x`. The old endpoint-reachability assertions remain. This
corrects an observed evidence-ordering issue: the old reset only requested layout,
so its success PNG could still depict the endpoint viewport. It does not establish
a production regression.

## Immutable source evidence and host checks

`tools/fixtures/commons_metadata_m04_diagnostic_successor_scope.json` is a new,
SHA-256-pinned successor fixture. It enumerates exactly the changed flow test and
three host adapters, with exact before/after hashes and reversible fragments.
It restores failed PR55 bytes before the existing PR52/M04 projections run.
No historical fixture or historical 890-identity inventory is rewritten.

The original source-union check still requires the same exact Kotlin path union.
Existing historical mutation checks operate on the restored original endpoint;
the new diagnostic mutation checks separately reject missing, duplicated,
corrupted, restored-old or unrelated successor content. Neither layer is bypassed.

`expected-jvm-identities.json` is a fresh successor inventory, with the same 890
identities and the changed flow-source hash. It adds or removes no runtime test.
Host/source tests validate provenance and controls only. They cannot establish
Kotlin compilation, native shaping/layout, or Android acceptance.

## Next evidence needed

Publish this explicit diagnostic successor, verify the remote tree, and inspect
its exact-source JVM results and retained diagnostics. Compare actual native line
advance bounds, painted ink, content width and parent geometry before choosing the
smallest defensible repair. Preserve the failed run even if a later successor
passes. Do not change strings, fonts, thresholds or deadlines merely to obtain
green CI. Installed-device results are a separate outcome.

## Local validation history

An initial aggregate was started before diagnostic authoring was frozen. Updating
the successor fixture and raster suffix while that process held imported older
constants invalidated its results: 261 stale fixture-pin failures and one stale
raster-suffix failure. The entire failed log is retained as
`in-progress-source-change-all-host.log`; it is superseded, never treated as a pass.
A fresh aggregate on frozen source completed all 666 tests (660 existing plus six
new diagnostic contracts) with no failures. Focused optimized-Python contracts and
catalogue structural validation also pass; see `local-verification.json` and logs
for exact results. Android compilation and execution remain unrun locally.

## Publication evidence boundary

The [complete first-run evidence checkpoint](https://github.com/c933103/AN-Paint/tree/946e5378cf3f75a8047dc42a46a3b3dbe62c9327/verification/commons-metadata-m04-pr55-initial-ci-2026-10-12) preserves all336 evidence files including all85 available captures. It is a failed checkpoint, not superseded into a pass.

[Independent diagnostic source review](independent-review/README.md) finds no blocking source issue. Its seven-file source manifest SHA256 is `d3501be64d05907c00f45ef2feca60d42df480b7122866bce1108457a1c2e3ec`. It independently passes22 normal and22 optimized contracts and binds the writer's frozen full666-test result.

All inherited standalone and PR52-composition reports remain historical and byte-identical. Their old full-host results do not verify this diagnostic successor. This directory and its fresh source manifest, projection checks and logs describe the changed test instrumentation; a new hosted run must establish compilation and actual output. The temporary checkout's local baseline commit is not a substitute public commit: GitHub independently binds public PR55 `b95c9a682c77f5dfa9b9a1f4eacabd9d9a03265a` to the exact immutable `d80218496e45bbefcaa378d40e5cd9846b7988ee` base tree.
