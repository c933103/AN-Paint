# PR87 gallery redirect diagnostic candidate

## Finding and scope

PR87 remains an open, intentional documentation-only draft. Current source at
`b765b8b2396d9b4c05f7272fa982d115ce18469a` still rejects any failed
`IllustrationSource.allowsDownload` predicate in
`MediaGalleryActivity.kt:325` with a host-only explanation. The predicate also
checks HTTPS, user information, port, image path and extension. A controlled
same-host destination such as
`https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Example.png/320px-Example.png`
is safely rejected yet falsely described as leaving supported hosts.

This is source-supported diagnosis, not an executed Android reproduction or a
claim about a real provider. Search found no competing implementation. No hold
on a separate fix was found; the tracker itself must remain open/draft until its
acceptance gates are established.

## Candidate

Default English is now “The gallery redirected to an unsupported image URL.”
All 59 existing locale definitions are updated in the same candidate. The legacy
resource key is preserved, with one explanatory default-resource comment. The
112 selectable fallback locales and all translation progress counts are unchanged.

Production Kotlin, URL policies, redirect handling/limits, cancellation, temporary
file ownership and result state are byte-for-byte unchanged. No destination URL
or query value is inserted into the corrected diagnostic.

Ten new Robolectric test methods (API30 and API35 declarations) cover the actual
WebView selection -> asynchronous downloader -> status/result path with substituted
connections: same-host thumbnail/archive rejection in English/French/Japanese;
off-host, scheme, port, user-info and extension rejection; retry and allowed
relative redirect; five/six-redirect boundary; cancellation after a redirect; and
all 171 compiled locale resolutions. No live-provider request is part of the tests.
These JVM tests are authored and independently source-reviewed, not executed here.
The source review tightened the cancellation gate to avoid timeout-driven false
positives and made actual-loop status assertions independent of production's
selected resource value.

## Language review

All 60 complete values have a first translation pass and separate full-value
source-context review. Seven modifier-scope improvements were cross-reviewed:
Ainu Kana/Latin, Dzongkha, Mongolian Cyrillic/traditional, Manchu and Okinawan.
The Ainu context gloss was corrected from “request” to “page/sheet.” Final counts
are 39 high, 15 medium and 6 low confidence. The six low-confidence entries are
Ainu Kana/Latin, Dzongkha, traditional Mongolian, Manchu and Okinawan. Specialist
idiom/grammar uncertainty remains; no native-speaker certification is claimed.
All corrected script values use code points already present in their catalogues.

`final-language-coverage.json` is the reconciled complete review receipt. Original
candidate and independent/cross-review files are retained for traceability and
must not be mistaken for the final values where a correction exists.

## Deliverables

- `implementation.patch`: 64 changed/new files, no removals.
- `publication-files.json`: complete UTF-8 payloads anchored to the stated base,
  with Git blob SHA, SHA256 and executable mode.
- `changed-files.json`: exhaustive compact file inventory.
- `resource-delta.json`: exact baseline old -> final message values for 60 files.
- `reconcile-resource-delta.py`: temporary, guarded key-only integration helper.
- `test-source-review.txt`: independent test/fixture source review and limits.
- `final-language-coverage.json`: authoritative combined language receipt.
- `patch-verification.json`: exact reconstruction of all 1,146 final files/modes.
- `integration-rehearsal.json`: unrelated PR102 resource values remain intact.
- `test-results.json`: final executed test counts and unrun stages.

Application-file inventory: 60 existing strings.xml files plus
`GalleryRedirectTest.kt`, `tools/test_gallery_redirect_wording.py`,
`tools/fixtures/current_localization/gallery_redirect_current_wording.json`,
and `docs/GALLERY_REDIRECT_DIAGNOSTIC.md`.

## Important integration constraint

This final packet already includes merged PR102 as its baseline. PR102 changes a
different key in the same 60 resource files, and its messages and synchronization
fix are retained. If develop advances again, materialize and verify fresh target
files, apply only the key delta/helper, and review the resulting remote tree/lease.
Do not overwrite newer unrelated resource changes with stale whole-file payloads.
Both an isolated rehearsal and the actual fresh-base reconciliation preserved all
unrelated XML content. No existing PR102 workspace or branch was modified.

Keep bulky test/review evidence outside the application tree on the project's
appropriate evidence ref. No publication, review request, workflow trigger or
tracker edit was performed for this task.

## Validation limits

The initial temporary baseline was matched against all 1,139 original blobs.
After PR102 merged, the candidate was reconciled key-only onto fresh develop
`b765b8b2396d9b4c05f7272fa982d115ce18469a`, verifying all 1,142 base blobs
and modes. Patch reconstruction verifies all 1,146 final files/modes; all 1,082
unaffected original blobs remain unchanged. PR102’s complete merged test file,
including its onShow-idle synchronization, is preserved byte-for-byte.
The final negative control rejects all 60 original host-only resource values.
See `test-results.json` for final focused/aggregate executions and logs.

Kotlin/Robolectric, Android compilation/lint/native build/APK, Gradle generated
resources, emulator, installed-device rendering and live-provider stages are
unrun. No Gradle/Kotlin/adb/sdkmanager executable or configured Android SDK is
available; the only known Gradle8.13 cache contains incomplete download marker
files. The installed Java is 21, while the project documents JDK17. No prohibited
live dependency download or Work-side task was attempted. Exact-source hosted
CI/review remains required before claiming runtime acceptance or closing PR87.

## Retained aggregate-run failures

An initial serialized complete host run passed 725 tests before the seven
word-order refinements. The first post-review normal/optimized aggregates were
run concurrently and both failed existing 10-second subprocess gates in
`ComposedDriverTest.test_both_clis_require_composed_reports_and_clear_all_receipts_in_optimized_modes`
(one error in normal, two in optimized). All timed-out verifier/test sources
match the baseline exactly. Resource contention is the working explanation,
not a demonstrated product defect. The failure logs remain `host-final.log` and
`host-final-optimized.log`; original limits/assertions are unchanged. The isolated
method and sequential complete-rerun outcomes are recorded in `test-results.json`.

Fresh-base validation also retained a working-directory setup error: the first
focused invocation kept the renamed old-source inode as its shell directory and
could not import the newly merged empty-credit test module. It made no production
change. Rerunning in the resolved fresh-source directory passed all 47 focused
tests. The setup-failure log is retained as focused-rebase-cwd-error.log.

## Final executed results on b765-based candidate

- Focused redirect/empty-credit/resource/font checks: 47 passed, 4.061 seconds.
- Full host suite, sequential normal run: 729 passed, 168.336 seconds.
- Full host suite, sequential optimized run: 729 passed, 178.237 seconds.
- Fresh-baseline negative control: all 60 old values rejected.
- Patch reconstruction: all 1,146 final files and executable modes match.
- Fresh-base preservation: all 60 PR102 empty-credit values and the exact merged
  CommonsCreditFlowTest, including its onShow idle, remain intact.

The existing subprocess limits and assertions were never changed. Prior failed
parallel runs and the corrected working-directory setup error remain retained.
No Android runtime result is implied by these host/source/resource passes.
