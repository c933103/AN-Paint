# Android build and test workflow

## Working policy

Keep the application tree focused on code, meaningful tests, compact current
product fixtures, licence inputs and current instructions. Historical raw logs,
images, source inventories and one-time preservation audits belong in CI
artifacts or an immutable evidence ref linked from [the archive index](verification/README.md).
Normal CI does not reconstruct old source snapshots or require inverse adapters.
Current source/test discovery and per-run APK/source binding remain required.

Localization status remains scoped: earlier withdrawn review conclusions are
not restored by this migration. The compact 59-locale wording fixtures preserve
current regression expectations and explicitly retain the 112 open fallbacks;
matching them does not certify fluency or complete linguistic review.

## What runs

- Code push to `develop` or a PR targeting any branch: independent host/JVM/lint,
  universal APK/corresponding source, exact-script generation and API35 jobs.
- Workflow dispatch `device_tests`: `current` (API35), `full` (API30+35), or `none`
  (explicitly not run). Release selects full coverage.
- PR label `ci:full-android` selects API30+35 on its next normal source event.
  `ci:release-android` additionally selects release-configured host/APK/tests.
  Label changes alone do not trigger or cancel a run.
- A develop commit subject starting `Release `, or manual `build_type: release`,
  selects the release variant and API30+35. CI release configuration uses the
  temporary CI key, not the private upgrade key, and does not publish a release.
- Markdown/historical-verification-only changes do not automatically rebuild.

Test APKs compile once after delivery artifacts are available. Device jobs use
those prebuilt binaries through `adb shell am instrument -w -r`, without Gradle
or native-codec rebuilds. SDK-aware source discovery determines the expected
identities and explicit exclusions; never freeze a past test count as a source
oracle. API30 omits SDK-ineligible tests and the explicitly API35 restart pair.
API35 includes ordinary, gallery-draft, dialog, two vertical shards, two position
shards and the external force-stop seed/verify phases. A missing or excluded test is not a pass.

The exact-script job tests clean debug/release resource merges, release-first,
producer-before-consumer order, identical generated XML, an unchanged up-to-date
run, input-change regeneration and stale-output removal in a disposable worktree.
Both the mixed-script Korean and emoji-English mirrors are checked independently.
Only `:Paintroid:bundleCorrespondingSource` is excluded there; the normal build
verifies that native-source/bundling graph. Production translations are not edited.

## Local commands

Run relevant focused tests first, then the current host suite:

```sh
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 -O -m unittest discover -s tools -p 'test_*.py'
```

Use the repository Gradle wrapper with the installed SDK/toolchain for
`:Paintroid:testDebugUnitTest`, lint and APK compilation. The workflow is the
canonical command/variant source. If Android tools are absent locally, report
compile/native/device stages as unrun and use the exact-source hosted results.
Focused checks do not turn an incomplete aggregate into a pass.

## Deadlines and evidence

- Regression job: 22 minutes; Python contracts: 4 minutes; build job: 45 minutes;
  universal assembly: 30 minutes; emulator jobs: 53 minutes, including a 43-minute execution step.
- SDK install: 5 minutes; device discovery: 60 seconds; boot/service readiness:
  shared 120 seconds, each transient probe at most 10 seconds within that budget.
  Main and each test APK installation: 60 seconds; runner discovery: 15 seconds.
- Native and ordinary app phases: 180 seconds each; gallery-draft: 90 seconds;
  API35 dialog phase: 300 seconds; each vertical shard: 180 seconds; seed and
  verify: 60 seconds each. Core app ceilings total 630 seconds on API30 and 1,050 seconds on API35.
  Including native gives 810 / 1,230 seconds before setup/collection.
- Separate position job: two 180-second invocations, a 16-minute execution step,
  6-minute image step and 26-minute job cap. Its controlled path is 270 seconds
  startup + 360 instrumentation + 180 preparation + 10 capture tails + 20 failure
  recovery + 36 cleanup = 876 seconds; a 60-second processing allowance rounds
  up to 16 minutes. These are cancellation budgets, not proven runtime bounds.
  Across both jobs, app ceilings total 990 / 1,410 seconds on API30 / API35.
- The current 43-minute step includes separately bounded setup, processing and
  cleanup allowances. Inner deadlines and failure behavior must not be relaxed
  to obtain green results. Test/installation failures are not automatically retried.

The runner retains live raw output, JUnit XML and summaries, including partial
failures. Success requires the final protocol plus every selected identity,
without unexpected, missing, ignored, failed or aborted methods. A zero ADB exit
alone is insufficient. Artifact upload runs even on failure, but cancellation
can leave partial evidence. Keep passed, failed, timed out and unrun distinct.
Actions artifacts expire after 14 days; preserve needed final evidence on a
separate durable ref before expiration. Never include keys, credentials or
unrelated private data.

## How to conclude work

Publish the concrete reviewed change and report the exact asynchronous run.
Continue useful work while it runs. Development delivery requires a built APK,
matching source and correct signature, with pending checks clearly stated.
A verified release requires its complete exact-source gates. Inspect a failure
before retrying; use the affected scope, not a repeated full matrix by default.

## Localized dialog evidence and separate phase

Twelve installed dialog method/class pairs run in the `app-dialog` report: four
current notice/credit cases, three Korean attribution/crop consumer cases, three normal-font colour cases and two 2× short-landscape preview-rail cases. Source discovery
still requires every SDK-eligible app identity, without duplication or omission.
The colour cases replace the old zero-height limitation characterization; its
original failed positive and measured negative results remain historical evidence,
not claims about the repaired source. See [PR51's accepted bounded baseline](https://github.com/c933103/AN-Paint/pull/51).

The dialog 300-second cancellation cap and each 45-second interaction limit stay
unchanged. Twelve individual maxima exceed that aggregate cap; fresh actual combined
execution must fit, and a timeout remains a failure. Neither historical timings
nor synthetic transport fixtures prove the combined runtime. The new 2× cases cover English/Hungarian caption and preview-rail reachability
only. Large-font IME/footer, physical-device and TalkBack coverage remain separate
limits; C05 large-font ancestor visibility is still open.

The three Korean cases select `ko-KP`, `ko-KR` and `ko-Kore-KR` through the real
picker and require their public/platform/resource identities. They open the
actual image-credit editor from the About row with a synthetic document credit,
then the production crop dialog with synthetic pixels and placed/linked image
metadata. Exact complete title/Copy text, accessible text and native layout-line
coverage are bound to source-checked fixtures. Four screenshots per case show
the attribution title, Copy control and conditional crop status for one/two
selected images after a real text-watcher margin update and native checkbox tap.
Native Back/Cancel must preserve the fixture credit and never apply the crop.
Copy is displayed and measured, not executed in these Korean cases; assembly
movement, the assembly toolbar launch route, expanded fonts, full catalogues,
pixel-level glyph clipping and native-language acceptance are not claimed.
No provider is opened and no user image is read. Existing immutable Mongolian,
PR56 and Hakka holds and historical evidence remain unchanged. New test code is
not installed evidence until its exact-source API35 run and captures are checked.

The dialog collector checks a bounded native-screenshot PNG profile: noninterlaced
RGB8/RGBA8, with IHDR, optional single sRGB/sBIT before consecutive IDAT chunks,
and final IEND. It checks CRCs, small metadata fields, size limits and the exact
zlib/scanline envelope. Other encodings or chunks fail as **unsupported profile**;
this is not a general PNG decoder or conformance claim. UiDevice promises PNG,
not this exact encoding, so a future producer change needs explicit review.
The current API30/API35 capture corpus fits this profile. Actual images still
need standard-decoder and visual/input review; source/hash checks alone cannot
establish rendered correctness. No new image-decoder dependency is installed.

## Historical composed cancellation budgets

Older budgets, timings, raw captures and source-preservation checks are in the
[immutable pre-migration CI history](https://github.com/c933103/AN-Paint/blob/04b128889a4ff9159f199d1737bd07d41e22162d/CI.md).
They do not set current caps. Current workflow and phase-budget tests are authoritative.

## Rendering requirements and diagnostics

Hard requirements include full text and UTF-16 line coverage, no ellipsis,
accessible text, reachable controls/scroll endpoints, and correct natural
same-height status updates. Native capture must use a complete independently
bounded reference, with unsupported drawing state and unsafe allocation rejected.
Keep unmasked exact ARGB/alpha comparisons and genuine native overflow/clipping
controls. A completely missing ink component or opaque stroke sample is a hard
failure; components are not glyph segmentation. Other pixel differences require
explicit review, including partial marks/strokes. A reviewed antialias fringe is
not a universal tolerance, and a diagnostic difference is never labelled exact-pixel pass.
The proportional positive-frame policy currently applies to the M04 JVM captures.
The two installed Arabic helper/decoder profiles retain their exact zero-difference
gate; both passed in the archived04 run. A future installed fringe difference
still needs explicit severity review before adding a production workaround.
Installed software-raster evidence is not a hardware screenshot or network-route proof.

## Locale UI font inventory check

The Nôm asset is a subset for catalogue and picker text, so it has the
`ui_only` role and is excluded from the drawing-font selector.
Default Nôm text still uses its glyph coverage, while an explicit drawing font
keeps the user's selected face. Complete Mongolian remains a drawing choice.
Font regressions compare selectable entries with the inventory's drawing roles
instead of freezing catalogue size. The Android test additionally opens, hashes
and loads every declared asset, including UI-only subsets; hiding a subset from
the selector does not remove its font-load coverage.


AN Paint Nom UI is a renamed subset of Nom Na Tong (MIT) and Gothic Nguyen
(SIL OFL 1.1), distributed under SIL OFL 1.1 with the original MIT notice retained.
AN Paint Wu Fallback is a glyph-only subset of Nom Na Tong under MIT.
Keep actual asset/notice/inventory consistency, bundled cmap coverage, current
glyph metrics and upstream input provenance. Historical binary reconstruction
is an archived one-time check, not a normal CI dependency.

API30–33 font-setting synchronization uses bounded shell work and a private
virtual-display acknowledgement. Under normal FIFO ordering this orders relevant
ATMS messages; a synchronization barrier prevents a portable queue-drain guarantee.
Do not describe it as a universal synchronization proof.

## Cache and corresponding-source rules

Cache downloaded dependencies, pinned native source trees and content-checked
ccache objects only. Compiler identity/content, flags, preprocessed inputs and
strict headers remain checked; direct/depend modes are disabled, sloppiness empty.
Do not restore Java/Kotlin classes, APKs, linked libraries or CMake build output.
Build corresponding source from the same checkout and required pinned native
inputs, retaining licences, font attribution and build scripts. Verify the
embedded source ZIP equals the separately delivered ZIP and matches current source.

## Release publication

The separate publisher consumes `verification/releases/request.json`, its
selected version's public signing patch and release notes. Preserve these
operational inputs during evidence cleanup. Private upgrade signing happens
outside GitHub; never publish the key or private backup. Publication requires
successful exact-develop regression/build/API30/API35 jobs, release manifest,
existing certificate, unchanged non-signature payload, four ABIs, 16KB alignment
and matching embedded source. A normal PR update does not authorize a release.

## Android 5.0 and 7.0 compatibility

`.github/workflows/android-legacy.yml` is manual-only (`workflow_dispatch`).
Choose API21, API24 or both and x86, x86_64 or both. It builds one universal debug
APK and reuses strict SDK-aware native/app inventory checks. SDK-ineligible app
phases are explicitly NOT RUN; no fake empty passing report is produced. This
workflow does not expand ordinary API35/full API30+35 or implicit release gates.
Emulator results do not establish physical ARM-device or vendor-picker coverage.

## Exact-position dialog coverage

Seven installed `AssemblyPositionDeviceTest` methods are source-discovered in
two explicit position shards on API30/API35: Ainu Kana/Latin, Manchu, Tibetan,
Dzongkha, Jeju and Nôm. They exercise the actual production position dialog
with explicit locale/image-metadata fixtures, full caption and accessibility
text, line/vertical-column extent and native scroll reachability in portrait
and landscape. Native focus/input, invalid-value rejection, Apply, saved-project
reload, Cancel and Back are separate assertions. Manchu must mount the
left-to-right vertical shell and retain its complete vertical caption spans.

The ordinary 180-second phase cap remains unchanged. The seven position methods
run once in a separate emulator job: Ainu Kana/Latin + Manchu (three), and
Tibetan/Dzongkha + Jeju + Nôm (four), each capped at 180 seconds. Each method keeps
its 45-second interaction bound. Native Back dismisses a previous field's IME
before revealing/tapping the next field; view clipping alone does not account
for keyboard occlusion. Native focus/input and all persistence assertions remain.
Caption reveal visits the same 64dp tiles column-first, avoiding a repeated
horizontal sweep for every row of a wide vertical caption. Host checks execute
the device helper and compare the exact tile set/area with the former row order;
their scroll model is not an Android runtime measurement. Timeout diagnostics
distinguish the shared 45-second budget from the individual 8-second wait bound.
Neither deadline nor any text/input/persistence assertion is relaxed.

Core and position jobs use the same API selection and prebuilt artifacts. Their
partial receipts cannot stand in for the complete union. The final `Emulator API`
gate requires both jobs to succeed, identical checkout/run/variant,
main/test APK and corresponding-source hashes, and the exact disjoint source-bound
app report union. Exact-identity groups from earlier attempts of the same run may
be reused; both positive attempt numbers are recorded and cannot be in the future.
Missing/failed/duplicate methods, wrong selectors/deadlines,
stale artifacts and SDK mismatches fail closed. All 45 declared methods remain
required according to their existing SDK rules (30 selected on API30; 45 on API35).
Count/selector contracts and synthetic receipts do not prove Android execution
or runtime. These
checks cover native layout boxes and input, not pixel-level glyph clipping,
linguistic acceptance, picker/import/export, forced IME visibility, enlarged-font
layouts, physical devices or all catalogue languages. The production dialog is
opened as a fixture; the assembly toolbar launch route retains its separate JVM
coverage. The existing glyph/font checks remain complementary.

## Selecting artifacts after a partial retry

The final emulator gate resolves each exact core/position artifact name to an
explicit ID before download. It paginates current-run artifacts and jobs, requires
the latest matching job to have succeeded, and requires exactly one nonexpired
artifact created/updated inside that job's recorded start/end interval. Repository,
run, workflow head, exact checkout in the name, SDK and positive/nonfuture attempt
identities must match. Duplicate names from earlier attempts are retained; numeric
artifact IDs and API list order are not chronological selection rules. Ambiguous
or incomplete metadata fails closed.

On a partial rerun, GitHub may carry a successful earlier job into the current
attempt's job metadata with its original execution interval. That interval selects
the existing successful core artifact, while the rerun position job selects its
new artifact. The unchanged composer still checks complete successful inventories,
exact prebuilt/source hashes and each artifact's declared original attempt. The
selection receipt does not replace those content checks. PR workflow head and
synthetic merge checkout are distinct identities and are checked separately.

Only the final composition job receives read-only Actions metadata permission;
no write permission or persistent credential is added. The selector has a one-minute
step cap inside the unchanged eight-minute composition-job cap. Existing device,
interaction, setup, report and composition deadlines remain unchanged.

The pinned download action re-lists with `latest: true` even for explicit IDs; its
SDK filters duplicate names by highest ID. The final gate therefore uses the
runner's existing GitHub CLI to GET each selected REST artifact ID directly, then
checks the selected SHA-256 before safe report extraction. Each transfer has a
90-second deadline; the two-transfer step is capped at four minutes within the
unchanged eight-minute job. Report archives are limited to 128 MiB compressed,
512 MiB expanded and 10,000 members. Unsafe paths, symlinks, duplicate members,
unsupported encodings and attempts to overwrite existing evidence are rejected.
No downloaded artifact can replace the saved selection receipt. The normal
content/inventory composer still runs after extraction.
