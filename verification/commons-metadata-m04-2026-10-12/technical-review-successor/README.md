# M04 final 59-value successor: independent technical review

Reviewed 12 October 2026. **PASS for the bounded source, host-contract and local font scope. No blocking defect found in that scope. Android compilation/runtime/rendering remain UNRUN and prevent an Android-verified or merge-ready conclusion.** No production edit, GitHub write, Work task or new translation review was performed by this reviewer.

## Exact inputs

- Base commit: `4231edaac45d89c52f51e2b77d0f94a1176ad88c`.
- Base tree: `c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1`.
- Exact accepted 59-value input SHA-256: `00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d`.
- Source-only manifest: `source-manifest.json`, SHA-256 `1b29a1008271a5086350b6b6d0ca781bccf79983d068b1017a3e8a143100eb95`.
- Whole reviewed checkout before this report is copied in: `reviewed-checkout-manifest.json`, SHA-256 `d98a1999399f59b3c14715d895e9ba435a54267252e8a252d477bc231174eb78`, 1,671 files. The separately published `verification/commons-metadata-m04-recovery-2026-10-12/` directory is explicitly excluded. This manifest binds the reviewed inputs; it is not the eventual Git tree after adding this report or further documentation.

The original 53-value review is retained as historical provisional evidence. Fresh portable checks use the real immutable base SHA, not the former temporary HEAD or vanished paths. All 116 frozen recovery files, including 14 old review artifacts, were independently hash-verified. The old failed completeness logs and conclusions were not rewritten.

## Production and preservation review

The two production-file deltas remain the previously reviewed minimal change: a message-less `QueryFailureException : IOException` replaces only the English-message exception raised by `root.has("error")`, and the shared UI mapper translates only that new typed condition. Top-level null/false/empty values still fail; unrelated nested error fields do not alter the trigger.

Both Copy credit and insertion invoke the mapper inside their alive-activity UI callbacks. Provider/framework details remain unmodified. HTTP handling, malformed JSON, M03 response-size handling, M05 ambiguity, M09 field limits, metadata fields, provider hosts/parameters, cache/document/clipboard behavior, lifecycle cleanup, timeouts and thresholds are unchanged. The old query test alone becomes its localized successor; other old test expectations remain exact.

Fresh direct comparisons with Git establish:

- Exactly 71 existing files differ: 60 single-entry catalogue additions, two production files, one prior Kotlin-test successor, font and inventory, and six narrow historical-test adapters.
- All 1,523 other baseline files and every baseline file mode are unchanged; exactly 12 expected new source/test/fixture files are present.
- All 205 separately protected paths and 561 baseline verification/fixture files are byte-identical. No historical hash, assertion threshold, method, workflow, provider rule or deadline was relaxed.
- The six adapter files are byte-identical to the original frozen proposal. They remove only exact hash-pinned M04 deltas before applying the unchanged historical oracles.
- Every original default-plus-53 catalogue file is byte-identical to the frozen partial checkpoint. Of its 77 source files, only five expected successor artifacts changed: catalogue pin/fixture, active decision path, expanded Kotlin value map and the added bo/ryu render profiles.

`scope-result.json` and `partial-successor-delta.json` record these checks. All new strict completeness gates remain active.

## Resources, Unicode and test-source coverage

All 60 explicit catalogue entries restore exactly to their immutable baseline after the one approved M04 addition is reversed. Their current values and the 59-entry Kotlin expectation map exactly match the accepted v4 input. All 140 offered tags have individual dispositions: 59 scoped values, 81 still-open fallback tags, zero unresolved scoped values. No other catalogue gained M04.

The Manchu value retains exactly three U+180E MONGOLIAN VOWEL SEPARATOR characters at zero-based positions 7, 18 and 27. The Traditional Mongolian value retains exactly three U+202F NARROW NO-BREAK SPACE characters at positions 7, 17 and 30. These values are preserved in canonical XML, the pinned scope and Kotlin expectations without normalization or removal. `scope-result.json` inventories controls and variation selectors; `unicode-and-render-source-check.json` independently binds the Kotlin map. This is source-level preservation, not a claim about AAPT output or Android shaping.

The flow-test source retains real WebView action routes, local fixture connections, query/error distinctions, stream/disconnect cleanup, both actions and successful retry, unchanged document/draft/cache/clipboard/result/temp-file behavior, UI-time localization, literal provider details, duplicate input and destruction during/after work. The repeated vertical action requires actual overflow, scrolls to the end, performs a second real request and checks restoration of reading start.

The only final change to that flow test adds bo and ryu to its existing profile list. All previous assertions are byte-preserved. Four normal/double-scale portrait/short-landscape configurations now cover 14 profiles and both actions, planning 112 captures. All six successor languages are included. Portrait whole-message fit, complete accessible text, zero ellipsis, short-landscape scroll reachability and vertical endpoints remain required. These tests have not run here: no captures or TalkBack/device-touch success are claimed.

## Fresh font verification and actual image inspection

The restored full Nom Na Tong v5.18 source independently matches SHA-256 `37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3`. The immutable base font is `4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05`; the candidate and fresh rebuild are both `6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006`, 276,500 bytes.

Independent binary/fontTools checks verify every old glyph order/ID, all 737 old outlines and horizontal metrics, all 735 old codepoint mappings in both cmap subtables, and every old global/name/licence table. Only U+3002, U+554F and U+8FFD are appended at glyph IDs 737–739. Their actual outlines and metrics exactly match the pinned source. The inventory changes only its font digest; the bundled MIT/OFL notice is byte-identical to baseline. This is licence-material preservation, not a new legal opinion.

Fresh builder output compares byte-for-byte equal with the asset. Fresh Pillow/FreeType rendering reproduces all 2,205 old-glyph mask/offset/advance comparisons at 24/48/96px. All are identical. The actual generated PNG was opened and inspected: additions and the candidate phrase are visible without tofu or image-edge clipping. 問 and 追 retain their recorded source/subset raster differences at 24px; all three source/subset masks match at 48/96px. Those differences are not hidden or treated as Android verification. Image SHA-256: `2410ed7956b6eb03b164f52ade923f3832d6f23f6c0fbebb85ecadf00b1d86f0`.

## Executed versus unrun checks

PASS, independently executed:

- Portable exact-scope, source-control and font audits; accepted values/source SHA pins; full baseline comparisons.
- 53 focused M04/M03/font/copy-credit/SVG/TIFF preservation methods, all pass.
- 32 translation-contract methods, all pass.
- Canonical catalogue structure; Python syntax compilation; `git diff --check`.
- Fresh font rebuild plus exact byte comparison; fresh raster generation and actual image inspection.

PASS, producer-run evidence independently inspected:

- Full host aggregate: 583 tests in 163.471 seconds, `OK`; producer reported exit 0. Summary is at lines 586/588 of `successor-all-host.log`. Later `success:false` JSON belongs to deliberate negative controls. This aggregate was not duplicated by this reviewer; its hash is in `observed-aggregate-result.json`.

UNRUN:

- Android/Kotlin compilation, AAPT/compiled-resource checks, Robolectric execution and 112 planned screenshots, lint, APK/native tests, installed-device behavior, screen-reader speech and actual Android shaping.
- No new Android attempt was made after recovery. The current environment receipt reports no SDK, Gradle command or adb. The older SDK-location failure remains historical evidence only.
- No global-language or native-speaker acceptance, merge or release decision is made. The 81 out-of-scope fallback tags remain open.

## Replay and publication

Run `bash run_review_checks.sh REPO ACCEPTED_VALUES FROZEN_PARTIAL FULL_SOURCE_FONT OUTPUT`. Inputs are explicit paths; the scripts themselves enforce immutable hashes. The wrapper performs host checks only, and fresh image inspection remains a separate human/model review action.

`DELIVERY-FILES.json` lists the report, portable scripts, manifests, logs and actual raster evidence to preserve. Temporary baseline/rebuilt TTF duplicates and Python caches are excluded. The existing base/candidate font bytes and pinned source suffice to reproduce them. Final remote-source equality, hosted Android CI, compiled-resource/source binding and actual Android image review remain required before broader technical acceptance.
