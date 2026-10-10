# AN Paint 0.0.38 publication preparation

This is a preparation bundle, not a release, signed build, successful postmerge
run, or localization-completion claim. It does not modify the source checkout or
contact GitHub. It contains no key, credential, private backup, actual signed
APK, or signing patch. The release source is the verified merge commit below; its fresh postmerge
artifacts and completed test outcomes remain pending.

Inspected candidate: PR #43 head `0c782ef533f246ee5b6676451e09c51a00e4ae61`,
exact staged tree `83f46e5d4772e98610bd6eb6fcc5a3964d19cd84`. The local checkout's
HEAD is a temporary integration commit, not the publication identity.
Parent-confirmed actual merge commit:
`2c1bd8622eb6c57444eee8f816194b309fff136e`, with accepted tree
`83f46e5d4772e98610bd6eb6fcc5a3964d19cd84`. Target develop push run:
[38095872353](https://github.com/c933103/AN-Paint/actions/runs/38095872353),
in progress at preparation time. Its final artifact hashes and fresh test
outcomes are still unknown and are intentionally not invented.

The existing `verification/releases/request.json` still refers to 0.0.32 and
must not be reused unchanged. Its two obsolete selectors describe superseded
behavior, not passing current assertions; see the explicit reconciliation below.

## Deliverables

- `0.0.38-notes.template.md`: source-grounded changes, including accepted PR #34
  and PR #43, bounded localization/physical-device limitations, and required
  final-value placeholders. Never publish this template as finalized notes.
- `prepare_release_metadata.py`: deterministic, offline preparation helper.
- `test_prepare_release_metadata.py`: synthetic negative/positive contracts,
  explicitly not executed Android test evidence.
- `metadata-tests.log`: 28 preparation contracts passed.
- `parent-metadata-tests.log`: independent parent replay of all 28 preparation
  contracts passed after reading the helper; metadata preparation remains
  supplementary to the strict final-run artifact verifier.
- `publisher-contract-tests.log`: 12 existing repository publisher, public-patch,
  and release-selection tests passed.
- `pr43-parser-rehearsal.json`: real PR43 host-report parser rehearsal, 804 cases
  in 85 suites. It is not a postmerge release result.

## Gates owned by the parent

1. PR43 exact-head evidence reconciliation, review and merge are complete as
   reported by the parent. Retain their evidence separately from fresh postmerge
   release results.
2. The accepted merge is `2c1bd8622eb6c57444eee8f816194b309fff136e`, with
   verified subject starting `Release `, selecting release plus API30/API35.
   Verify all later inputs against that actual merge commit and remote tree. Do not reuse PR head SHA,
   synthetic PR merge SHA, temporary local HEAD, or a guessed future commit.
3. Require the exact commit's successful `.github/workflows/android.yml` push
   on `develop`. Jobs must include successful build, regression/lint, API30,
   API35 and exact-script generation. A workflow_dispatch or successful PR run
   is not accepted by the existing publisher.
4. Download artifacts from that exact run into a fresh directory. Record
   artifact IDs, run/head binding and ZIP hashes before extraction. Verify
   `build-info.json` identifies that same commit/run and `release` variant.
   Artifact availability alone is insufficient. Preserve raw reports durably.
5. Re-run existing strict build/source, regression, generation and device
   evidence validation using the actual new source/run. The already-prepared
   `verify_ci.py` in the parent PR43 evidence directory has candidate constants
   for HEAD, TREE, TESTED_MERGE and RUN_ID; update those in a separate final-run
   copy. For a develop push, the generator commit must equal the actual released
   commit, not a PR synthetic merge. Retain current source inventory checks,
   protocol replay, source-digest bindings, SDK-aware partitioning, restart
   boundary logs, Korean/viewport oracles, transport and screenshot/reachability
   validation. This metadata helper does not replace those deeper checks or
   visual review.
6. Parent privately signs the exact CI APK using the already-available original
   upgrade key. Recheck signature/certificate, package `paint.anpaint.android`,
   version `0.0.38`, code `95`, release/nondebuggable state, all four native ABIs,
   16 KB alignment, unchanged non-signature payload and embedded source hash.
   Produce only the existing public signing/alignment patch for repository use.
7. Run this helper with the actual identity and public patch. It fails closed
   before creating an output directory. Review final notes, request and receipt.
   The helper validates the public patch's input/output identities, not its
   signing bytes; the parent's APK verification and publisher remain mandatory.
8. Add final notes, public signing patch and request together to the authorized
   publication commit, with the request change last/atomic so its workflow never
   sees incomplete metadata. Preserve repository visibility. Do not include
   credentials, key files, private backups or unrelated data.
9. Watch the publication workflow through its terminal result. Verify v0.0.38
   points at the actual release source commit, is public/non-draft/latest, and
   its APK, corresponding source, verification JSON and checksums have the
   expected hashes. Verify downloadable bytes, not only asset names. Reconcile
   an existing partial draft/assets before retrying; the publisher's `release
   create` is not itself idempotent. Never delete a release or overwrite assets
   merely to bypass an uncertain failure.

## Input layout and invocation

Use a new EVIDENCE directory populated only from the exact postmerge run:

```
EVIDENCE/
  regression/Paintroid/build/test-results/testReleaseUnitTest/TEST-*.xml
  regression/app/build/reports/lint-results-release.xml
  emulator30/  # extracted emulator-api-30-COMMIT artifact root
  emulator35/  # extracted emulator-api-35-COMMIT artifact root
```

The emulator roots retain native and ordinary reports, separate gallery-draft
reports, two vertical shards, and API35 seed/verify phases with each original
summary JSON, JUnit XML and instrumentation log. Copying only old `TEST-app.xml`
would omit real executed tests and is rejected. Do not put replays or historical
reports under those roots: duplicate or stale XML/summary inventories fail.

```
python3 prepare_release_metadata.py \
  --source EXACT_SOURCE_CHECKOUT \
  --evidence-root EVIDENCE \
  --workflow workflow.json --jobs jobs.json --build-info build-info.json \
  --commit ACTUAL_MERGE_SHA --run-id ACTUAL_SUCCESSFUL_DEVELOP_RUN_ID \
  --signed-apk-sha256 ACTUAL_VERIFIED_SIGNED_APK_HASH \
  --public-signing-patch 0.0.38-signing.json \
  --legacy-request EXACT_SOURCE_CHECKOUT/verification/releases/request.json \
  --output NEW_FINAL_METADATA_DIRECTORY
```

`workflow.json` and `jobs.json` are unmodified GitHub API responses. Retain all
jobs (pagination must not truncate them). The helper uses the checked source's
actual publisher `verify_jobs` and phase/source parsers. Output:
`request.json`, `metadata-validation.json`, and completed `0.0.38-notes.md`.
It emits every actual current passing JVM and device test as a feature check,
with its observed report path and newly computed SHA-256. This is compatible
with the existing publisher, which copies this object without schema limits.
The existing publisher does not independently read/validate `feature_checks`.

The historical `jpeg_xl_application_pixels_per_save` annotation is not copied
blindly. The current test still uses 257 × 193 pixels, but the actual fresh test
identities and reports are sufficient; the new request avoids inherited
non-result annotations.

## Explicit historical-selector reconciliation

The old cursor `movingAndTappingNeverToggleInkAndCancelRollsBack` is superseded
by current off-cursor positioning, cursor-tap toggling, and cancelled tap/drag
checks. The old unfiltered-at-every-scale
`canvasDisplayDoesNotBlendNeighbouringPixelsWhenZoomedInOrOut` is superseded
by reduced-preview filtering, source-pixel preservation, one-pixel-stroke
visibility and crisp-magnification/cache-refresh checks. These are documented
behavior changes, not aliases. The helper requires all six current checks and
records the two old identities separately in its validation receipt; it never
claims either old test passed. Any other disappeared historical selector fails.

## Validation commands

```
ANPAINT_SOURCE=EXACT_SOURCE_CHECKOUT python3 -m unittest -v test_prepare_release_metadata
PYTHONPATH=EXACT_SOURCE_CHECKOUT/tools python3 -m unittest -v \
  test_release_verification test_ci_release_selection test_apk_release_patch
```

Preparation tests use deterministic synthetic protocol/JUnit fixtures and a
synthetic release identity. None of those values is a release request. The real
PR43 rehearsal only exercises current host report parsing and historical
selector reconciliation. No postmerge source/run/artifact hash is guessed.
