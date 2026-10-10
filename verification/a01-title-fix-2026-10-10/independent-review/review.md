# A01 uncertain-animation title: independent frozen-candidate review

## Result

No actionable source-correctness defect found in the scoped change. The one production expression fixes the contradictory title for scanner results with fewer than two proven frames. **This is source/host approval only. Kotlin compilation and Android dialog execution remain a verification blocker, not a pass.** Do not close A01 as runtime-verified from this review.

## Exact scope and integrity

- Base commit: `80c14372b0504bc44f9f2809ad477247fdc8100b`
- Base tree, independently reconstructed: `d9858229f98068bef9c6194c90d77610c5ecceec`
- Candidate tree, independently reconstructed: `5d7ce333311c452cd7587fd871cdf45d6b6a72ca`
- 1,290 base files; 1,292 candidate files. Exactly 1,289 base files unchanged, one existing file changed, two tests added, no removals. Candidate Git index matches materialized bytes and modes.
- Recreated base-to-candidate diff matches supplied candidate.patch byte-for-byte: SHA-256 `0c772308be8ead4235d58a7267a76dc67d580c81c421279b541b5e1076012c7d`.
- Exact-tree `git diff --check` passes. Unstaged tracked diff is empty after review.
- All three candidate blob/SHA-256 identities match the author's manifest; see `integrity.json`.

Files:

1. `Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt`
   - Blob `d8d34518377f84c564cb508e4fa4f40d50f9b1d4`
   - SHA-256 `86169c732b8a5520b3f95b82f010ec6ef8d22ef1422cf86df3b5303822d6be69`
2. `Paintroid/src/test/java/org/catrobat/paintroid/local/ImportSelectionTitleTest.kt`
   - Blob `c795c04d42b96074663217c1372805d316f52e5d`
   - SHA-256 `4208f7a35235877e71cabd745b62cac319c1c479a5e11d0c3e823b78dfffc085`
3. `tools/test_animation_warning_title.py`
   - Blob `95d31ca878abe6b7fc9653414ddfeb4e34d1a512`
   - SHA-256 `67a5faf079f326b06b602034553b50c6ac3a1b016511610a79160ae68fc939f3`

## Source semantics

`ImportSelection.kt:89-96` now uses the same `frameCount < 2` threshold for both the uncertain body and neutral title. It uses the existing localized action resource `formats22_open_still`; no new English hardcoding or catalogue key is introduced.

- Zero/one proven frame: scanner result can be non-null at its work limit, so this is uncertainty, not evidence of a static image. The new title describes the permitted action without claiming confirmed animation.
- Two or more proven frames: exact and lower-bound counts retain `formats22_animation_title`. An incomplete scan with two proven frames is still confirmed multiple-frame content; the title correctly does not depend on `frameCountExact`.
- Exact counts continue to use the number; incomplete counts use `formats22_at_least_frames`.
- APNG confirmed-frame messages retain the separate-poster versus first-animation-frame resource choice. Unknown APNG results retain only the uncertainty body regardless of poster state.
- Null probes, including ordinary single-frame and malformed/unsupported containers, continue directly to `finishSelection(0)`; the scanner remains a warning hint rather than a decoder/validator.
- Positive action, Cancel, on-cancel, staged-file ownership, disposal, page chooser and every decoder are unchanged byte-for-byte outside the title expression.
- Existing localized keys are used through `ui`. English and pt-BR title wording is checked independently; missing Welsh keys still have default resources available. No catalogue changed. This does not certify other locales' semantics or rendering.

## Independently executed checks

1. `python3 -m unittest discover -s tools -p 'test_animation*py' -v`: **16 passed** (11 production Java scanner tests and 5 source/resource guards).
2. `python3 -m unittest discover -s tools -p 'test_translations.py' -v`: **32 passed**.
3. Five negative controls in temporary source copies: **all rejected with the intended assertion failure and no execution error**. Variants: original unconditional animated title; incorrect `<=2`; always-neutral; incorrect `<1`; and neutral whenever the count is inexact. These are source-wiring mutations, not executed Kotlin/Android mutations.
4. `scan_extra_states.py`: **25 fixture probes passed against independently compiled production AnimationMetadata.java**. These include all ten author's Kotlin-constant/equivalent-cap inputs plus:
   - Exact-two boundaries for GIF, WebP, APNG with and without separate poster.
   - APNG and WebP lower-bound 0/1/2 states, including APNG separate-poster state.
   - Malformed GIF and unknown-container null results.
   Kotlin constants were read directly from candidate source; cap bytes were constructed equivalently in Python. No Kotlin helper, dialog or image decoding was executed by this check.
5. Exact tree/blob integrity and patch checks described above pass.

Host logs: `animation-host-tests.log`, `translation-host-tests.log`, `negative-controls.json`, `scanner-extra-results.json`.

## Regression-test review and limits

The nine new Robolectric methods target the production scanner -> ImportSelection -> dialog path rather than a duplicate title function. Their title expectations are independent literals in English and pt-BR. They cover zero/one-frame uncertainty, exact GIF/WebP, the lower-bound-two boundary, APNG poster/non-poster, Welsh default fallback, ordinary still-image bypass, positive approval/ownership, Cancel and dialog cancellation, and disposal after approval before queued selection finishes.

These assertions are appropriately aimed at the reported regression: the original title would conflict with the uncertain English/pt-BR expectations; an always-neutral title would conflict with the confirmed cases; an off-by-one threshold would conflict with the two-frame lower-bound case. **This is a static assessment of their ability to fail, not observed Robolectric mutation testing.**

Coverage qualifications:

- All nine new methods and the existing ImportSelectionFlowTest remain uncompiled/unrun on this candidate. Existing flow tests are therefore not current-head runtime evidence.
- Body expectations mostly call the same resource keys as production. They guard route/composition, not independent translation accuracy.
- The Python title guard matches the intended source expression. It is useful for wiring regressions, not a Kotlin compiler or UI executor.
- New runtime cases do not cover uncertain WebP/APNG, exact-two counts, malformed-file error UI, vertical/RTL layouts, Activity recreation, real Back-key dispatch, or repeated positive-button clicks. The extra host probes establish scanner states only. These are residual coverage limits, not identified defects in this one-line change.
- First-image assertions establish `pageIndex == 0`, ownership and one callback following one click; they do not inspect decoded pixel content. Calling `drain` twice is not a repeated-click test.

## Verified execution blocker and next gate

The author's exact focused Gradle command stopped in Gradle wrapper bootstrap while requesting Gradle 8.13, with `java.net.SocketException: Network is unreachable`, before any Gradle task or Kotlin compilation. I inspected the log and the cache: only zero-byte `.zip.part`/`.zip.lck` files exist for that distribution. In this workspace PATH has Java but no Gradle, Kotlin compiler, javac executable or adb; JDK 21 is installed, and ANDROID_HOME/ANDROID_SDK_ROOT are unset. Java's bundled compiler module is available and was used successfully for the host scanner checks. No working Android toolchain was established.

Do not describe this as failing Kotlin tests: those stages never ran. The next verification gate is a permitted Android/JDK/Gradle environment running the new and existing focused Robolectric classes, followed by relevant Android build/runtime and rendered checks under the project's normal policy. No new Work task, remote upload, CI dispatch, production edit or publication was performed by this review. F01 and broader localization acceptance are outside this review and remain unchanged.
