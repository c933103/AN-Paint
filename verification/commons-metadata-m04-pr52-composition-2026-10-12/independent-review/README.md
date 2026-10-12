# Independent review: PR52-first M04 composition

Reviewed 12 October 2026. **PASS for the exact combined source, host contracts and local font scope. No blocking defect found for bounded source publication. Android compilation, compiled resources, runtime and actual app rendering remain UNRUN; this is not a merge-ready or Android-verified conclusion.**

The reviewer made no production edits, GitHub writes, translation changes or new language decisions. Earlier standalone M04 review results remain bound to their old checkpoint and were not reused as combined acceptance.

## Source identity and scope

- PR52 parent: `71f4d288669858e7975ec4c094b7f47a9a1ff145`, tree `815e265af5387111dcdaef66efac5d2091bbb56d`.
- Standalone M04 checkpoint: `045004bb23ef762f1731982f7a0152fef0fc5507`, tree `892e09280be9d668862ae5efada0ada163cc6bdb`.
- Shared develop input: `4231edaac45d89c52f51e2b77d0f94a1176ad88c`, tree `c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1`.
- Frozen writer manifest, 91 changed/new source paths: SHA-256 `d23ba36229197b1a2d90849f6cc89a53d7c156de2707756456c088201c2591bc`.
- Complete source patch: SHA-256 `d29ba081d5c98af5128c3654da7277cb87fcc6ca8378764cfece5eec413faa90`. A fresh Git diff was independently reproduced and matched these bytes exactly.
- Independent whole-source manifest, 1,080 non-verification files: `reviewed-source-manifest.json`, SHA-256 `b02ad5fdcf6c687c11a27f56bc4614549f812dabcd537db47c1cda84a6f19827`.
- Independent full reviewed checkout manifest, 1,922 files before adding this review: `reviewed-checkout-manifest.json`, SHA-256 `61b12b0e1ad480a75dc2c58a8a245441619e699aaf65ac98637a526a42831f11`.

The independent manifests bind these reviewed inputs, not the eventual Git tree after this report or later evidence-only additions. Publication must recheck the actual selected base and remote tree. Root retains merge authority.

## Exact preservation findings

`audit_composition.py` independently reads both immutable Git endpoints. It does not accept the new fixture's claimed original hashes without comparing its restored bytes with Git.

- Every PR52 leaf is accounted for: **1,729 byte-identical paths, 75 exact text reversals and one exact binary/font reversal = 1,805 leaves**. Existing modes are preserved; no baseline path is deleted.
- Exactly 76 PR52 files change and 15 expected source/test/tool/fixture files are added. The 91-path inventory matches actual checked-out bytes, lengths and Git blob IDs; no unexpected source path is present.
- All **751 historical PR52 fixture/evidence files** and **653 historical M04 fixture/evidence files** match their respective immutable commits. These producer-specific counts overlap and must not be added as distinct files.
- All 94 explicitly immutable M04 inputs are checked directly against the standalone commit. All original M02/M03/C05/composition/M04 fixtures, pins, manifests, old reports and failed evidence remain untouched.
- All seven M04 inverse endpoints restore exact standalone bytes. The three PR52 changes intersecting M04's original 205-path manifest are correctly handled: `.github/workflows/android.yml`, `CommonsHelpProviderTranslationTest.kt`, and `GalleryControlReachabilityTest.kt`. Their actual PR52 bytes remain in the application/test tree; the unchanged historical manifest is evaluated through strictly pinned inverse projections.
- The old preservation adapters were manually reviewed. Changes add only exact input projections and the explicitly bound two-new-Kotlin-test inventory. The original source hashes, assertions, count thresholds and negative controls remain required.
- The fragment-only production projection intentionally does not validate an entire file by itself. Its callers retain original full-file endpoints, and the new combined contracts independently enforce current full-file hashes. Extra unrelated content is retained through the fragment reversal and fails those complete-file checks.
- All 24 C05/M02/M03/M04 resource-reversal orders are exercised across all 60 catalogues, totaling 1,440 endpoint checks. Missing, duplicated, corrupted, unrelated and expanded deltas or changed fixture pins fail the required guards, including under optimized Python.

The full PR52 UI/layout implementation, its HTTP behavior, tests, workflow, SDK partitions, test-runner source and timing values are unchanged by M04. Neither PR51 nor the stopped PR53 producer is present among the added source paths or altered baseline behavior.

## Production and Kotlin-test review

The production result was independently reconstructed from PR52 using only the intended M04 edits, and it equals the candidate byte-for-byte:

1. `CommonsAttribution.kt` adds a message-less `QueryFailureException : IOException` and changes only the exception raised by the unchanged `root.has("error")` condition.
2. `MediaGalleryActivity.kt` adds one QueryFailureException branch to PR52's existing HTTP/response-limit mapper, preserving its position, comment and untyped fallback.

PR52's typed `HttpException(status)`, HTTP-before-body precedence, ASCII status formatting and both alive-activity callbacks are intact. Response limits, field/JSON validation, provider hosts/parameters/content, document/cache/clipboard behavior, cleanup, cancellation and timeouts remain unchanged. Top-level null/false/empty error values keep the same trigger; nested unrelated error data remains unrelated. Provider error fields are not attached to the M04 exception or displayed by that branch.

`CommonsCopyCreditErrorTest.kt` contains the exact standalone M04 query-case successor together with PR52's exact mixed-script Korean HTTP oracle. Every other prior expectation restores exactly.

The new M04 flow test differs from its standalone checkpoint by exactly one catch clause: it now requires `CommonsAttribution.HttpException`, status 503 and null message. The narrow catch itself excludes the separate QueryFailureException class; body-not-read, closure/disconnection and active-reference assertions remain. All other methods and assertions are byte-identical, including both actions, retries, provider literals, state/draft preservation, cancellation/destruction and repeated vertical reading-start restoration.

The M04 translation test is byte-identical to its standalone checkpoint. All 112 planned normal/double-scale portrait/short-landscape capture states and the six successor-language profiles remain required. No Kotlin/Android execution or screenshot success is inferred from reviewing their source.

## Fixed values and script controls

The exact accepted 59-value input remains SHA-256 `00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d`. Every new resource value matches it, and removing only the one immutable M04 line from each of the 60 catalogues restores its exact PR52 file, including Hungarian C05 wording and M02 HTTP strings. All 140 individual dispositions remain preserved, with 81 open fallback tags and zero unresolved scoped values.

Manchu retains three U+180E characters at zero-based positions 7, 18 and 27. Traditional Mongolian retains three U+202F characters at positions 7, 17 and 30. XML, fixtures and unchanged Kotlin expectations retain their exact sequences. No normalization or new linguistic judgment was introduced. Compiled-resource retention and Android shaping are still unrun.

## Fresh font and actual raster review

PR52 font/inventory/licence bytes were independently compared with the shared develop base and are identical. The current font exactly matches the M04 checkpoint:

- Base font SHA-256: `4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05`.
- Restored full Nom Na Tong v5.18 source: `37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3`.
- Candidate and fresh rebuild: `6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006`, 276,500 bytes.

Fresh independent font checks verify all 737 old outlines, IDs/order and metrics, all 735 old mappings in both cmap subtables, unchanged global/name/licence tables and the exact additive U+3002/U+554F/U+8FFD source glyphs. Inventory changes only the asset digest; the bundled MIT/OFL notice is unchanged. This is preservation of licence material, not a new legal opinion.

The preservation-only builder was rerun against the full pinned source and its output is byte-identical to the candidate. Fresh local rendering compares 2,205 old-glyph masks/offsets/advances at 24/48/96px, all identical. The actual newly generated PNG was opened and inspected: the additions and phrase are visible without tofu or image-edge clipping. At 24px 問/追 retain the honestly recorded source/subset differences; all three masks match at 48/96px. Image SHA-256: `2410ed7956b6eb03b164f52ade923f3832d6f23f6c0fbebb85ecadf00b1d86f0`. These are current local FreeType results, not Android render results.

## Executed results and remaining gates

Independently executed PASS:

- Exact immutable-tree/source/fixture/projection audit, including both reconstructed production files, strict inventory and fresh source diff.
- **89 focused methods**, 9.864 seconds, including all nine new composition contracts.
- **32 translation-contract methods**, 2.884 seconds.
- **Nine composition methods under `python -O`**, 3.907 seconds, including corruption/scope-expansion guards.
- Catalogue structure, Python syntax checks and `git diff --check`.
- Fresh font audit, exact rebuild comparison, raster generation and actual image inspection.

Writer-executed results independently read and hash-verified:

- **660/660 full host methods**, 184.672 seconds; raw unittest summary at `all-host.log` lines 665/667. Writer reports exit 0. Subsequent `success:false` instrumentation JSON is deliberate negative-control output.
- **89/89 writer focused methods**, 10.695 seconds.
- **89/89 writer optimized focused methods**, 9.217 seconds.

The aggregate and full optimized run were not redundantly executed by the reviewer. `observed-writer-checks.json` records their exact log hashes and evidence boundary.

UNRUN for the composition:

- Kotlin/Android compilation, AAPT/compiled-resource binding, the expected JVM inventory (producer reports 890 identities), all 112 M04 app-render captures, lint, APK/native tests, installed-device checks and actual Android/TalkBack behavior.
- The current environment receipt reports no SDK, Gradle command or adb. Previous standalone or PR52 device results do not establish combined success.
- No global-language/native-speaker acceptance, merge or release decision is made.

After publication, fresh actual-base hosted checks and source/APK/resource binding remain required. Rendered-image claims require opening the actual combined-run captures. Host passes do not waive those gates or authorize changing their thresholds.

## Portable artifacts

`bash run_review_checks.sh COMPOSED_REPO M04_CHECKPOINT_REPO FULL_SOURCE_FONT OUTPUT` replays the main host-only review. The Git repositories must contain the named immutable commits. Use ordinary Python for the independent assertion-based audit; project optimized guards have their separate recorded test. Image inspection remains a separate action.

`DELIVERY-FILES.json` lists the report, scripts, immutable/current manifests, results, logs and actual raster file. Temporary duplicate baseline/rebuilt TTFs and Python caches are excluded. Existing repository assets and the pinned source reproduce those duplicates.
