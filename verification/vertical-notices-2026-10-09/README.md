# Vertical foreground notice feasibility, 9 October 2026

## Recovery and integration revision

The native results below are frozen at `3f8bb0f64cfad485a1e725223d3475d8d60f9e5b`.
The publication is based on newer `develop` commit
[`748a03d496b6b053f9dba1835a11f7d9748275f7`](https://github.com/c933103/AN-Paint/commit/748a03d496b6b053f9dba1835a11f7d9748275f7), preserving the later warning and Commons-gallery changes.
It does not claim the whole newer application is identical to the measured version.

All 42 files from the original diagnostic tree were recovered byte-for-byte and
verified against Git blob IDs. This 43-file publication retains 38 exact historical
artifacts, including every native probe, runner, raw measurement, image, dependency
inventory and original test log. This README, the package manifest, provenance and
evidence checker are newly authored recovery revisions. `integration-audit.json`
is new. A later, unpublished metadata revision could not be recovered and is not
being passed off as restored. See the [recovery and input audit](integration-audit.json)
for every original object/hash and the classification of each file.

The audit compared all 15 measured inputs. Nine are byte-identical, including the
three compiled production helpers, all three fonts, picker tags, the lifecycle test
and the filename validator. Five catalogues have four changed or added keys outside
the nine measured keys. `ClassicPaintActivity.kt` has gallery changes, while the
exact one-newline cursor caller used by the diagnostic is unchanged. Neither these
input checks nor the historical results are a new native run on the newer application.

Fresh recovery-time verification of the normal host Python suite at the integration
base passed 307 tests with no failures or skips. That result is separate from the
historical 304-test log and 32 native executions below. The unchanged workflow
excludes this verification-only PR from automatic Android rebuilding; a skipped
app workflow is not a passed app build.

## Decision and scope

Measured source: [`develop` at `3f8bb0f64cfad485a1e725223d3475d8d60f9e5b`](https://github.com/c933103/AN-Paint/commit/3f8bb0f64cfad485a1e725223d3475d8d60f9e5b), tree `2e4b4a5baa7ad9981c006100a6aec333b0d218d6`. All 497 materialized input files matched the remote tree before work; all existing files remain unchanged.

Keep production routing unchanged in this increment. This is an **opt-in diagnostic and measurement report**, not a vertical-notice implementation or a passing release claim.

The proposed full-width, direction-aligned vertical body fails the complete-message-fit gate for a short, valid save filename. The unchanged shared renderer treats an unsupported multi-emoji ZWJ cluster as one upright cell, while native shaping draws several separate glyphs across a wider span. Its reported logical bounds fit, but the existing foreground host clips some of the ink. The next implementation needs a measured ink-containment contract; one grapheme cannot be assumed to occupy one cell.

Ordinary fitting fixtures supplied useful positive evidence. An initial nominal-box overhang alone was **not** enough to establish clipping, because existing padding and direction-aware placement can contain it. The counterexample below is separately verified through the actual parent clipping path.

### Production behavior versus diagnostic behavior

| Evidence | What actually runs | What it establishes |
|---|---|---|
| All 140 picker routes | Unchanged `LocaleTypography.showMessage` in an attached activity | Two configured horizontal routes use foreground notices. The other 138, including all five vertical profiles, use system toasts |
| Native shaping sweep | Unchanged `VerticalText` with a configured-context TextView's actual 14sp paint; supplied safe rectangles | Shared renderer measurements and native pixels, not an attached notice for every sweep row |
| Attached-host clipping | Direct call to `LocaleNotification.show`, deliberately bypassing the route predicate; its original child is replaced by a test-only vertical drawing body | Whether the proposed body fits/clips inside the real Notice geometry. No production vertical route is enabled |
| IME/resize transitions | Direct helper call for the five vertical profiles, retaining the existing **horizontal** TextView | Existing host/node/timer/input behavior under a hypothetical expanded route. These profiles are not affected foreground routes today |
| Twelve selected lifecycle methods | Existing unmodified method bodies from `LocaleNotificationTest` | Focused existing horizontal foreground lifecycle/binding checks, with the resource-isolation limits below |

No application source, resources, translations, fonts, licences, native tooltip behavior, drawing-font policy, workflow or overlay has changed. Background/application contexts remain system-owned.

## Reproduced counterexample

Filename: `😀‍😀‍😀‍😀‍😀‍😀.png`

There are six U+1F600 characters joined by five U+200D characters, followed by `.png`. The diagnostic executes the current `ExportNames.valid` and `withExtension` implementation with `ImageFormat.PNG`; the name is accepted and preserved. The enum/validator fragment is extracted verbatim from `SaveOptionsDialog.kt`, with unused UI-label getters outside the execution scope. The actual save callback inserts the provider's display name into `ui_saved` and calls `showMessage`.

`VerticalText.clusters` retains this sequence as one cluster. `bounds` reserves one `paint.fontSpacing` cell for an upright cluster. `draw` shapes that cluster in a `StaticLayout`, which can produce six fallback glyphs. The renderer's private run layout, placement and rotation are not represented by an ink envelope in the current bounds API.

The diagnostic uses the existing 16dp outer margins, 16dp horizontal/12dp vertical body padding, 14sp text, exact configured face when present and normal TextView face otherwise. It tries a preferred 240dp column height, capped by available height, then full available height when width requires it. Vertical-LR is placed at the left reading edge; vertical-RL at the right. Both final nominal dimensions must fit before the proposed body is inserted.

For accepted candidates, an uncropped renderer reference is compared **pixel-for-pixel** with the real Notice's child-clipped native output. A guard assertion verifies that the reference itself is not cropped. Expected clipping is a recorded diagnostic finding, not a failed normal regression gate.

Representative images are diagnostic renderings with a white background, not screenshots of a shipped vertical-notice feature. The red rectangle in the reference marks the proposed body boundary. The paired image is drawn through the actual attached Notice.

- [API30, vertical-LR reference](images/api30-en-xv-reference.png) and [actual clipped parent output](images/api30-en-xv-clipped.png)
- [API35, vertical-RL reference](images/api35-lzh-reference.png) and [actual clipped parent output](images/api35-lzh-clipped.png)

The final frozen run completed all nine stages:

- API30: 560 attached-host cases, 390 nominal fits, 72 fitting cases with actual clipped ink
- API35: 560 attached-host cases, 420 nominal fits, 78 fitting cases with actual clipped ink
- Every clipping case is the joined-emoji filename. The other six fixture groups have 660 accepted layouts across both APIs with no body clipping
- 8,640 native shaping rows, 280 baseline route checks and 40 transition rows; 32 selected native test executions passed

At normal 14sp/mdpi in portrait, the en-XV counterexample reports only 16.40625×89.40625px against a 356×568px safe inner rectangle. Its ink starts 28px outside the 388px-wide body, and the real parent clips 372 painted pixels on both APIs.

See `summary.json` for the exact representative rows; complete TSVs are compressed losslessly in `data/`. `probes/check_evidence.py` verifies the published bytes, exact frozen or explicitly audited integration source hashes, complete historical stage results and summarized counts. It revalidates recorded evidence; it does not execute native tests.

## Insets, resizing and accessibility

The attached-window IME fixture supplies a visible bottom source to the real framework `InsetsController`, dispatches actual window insets, and verifies the calculated `rootWindowInsets` before using Notice geometry. It does not set Notice padding or replace its inset implementation. This is test-supplied window-manager state, not a real keyboard/IME animation or physical-device result.

The cached API30 Robolectric framework sets `persist.debug.new_insets=0`. That legacy mode reports IME visibility but omits its geometry. The diagnostic temporarily enables the framework's full mode 2 **after** the activity/dialog has been created, then restores the original mode before the next scene. Enabling it during window creation instead encounters a separate Robolectric window-metrics reflection limitation. Neither correction changes app code or weakens the required IME size assertion.

The transition diagnostic keeps the same existing horizontal TextView while showing/hiding the injected IME and resizing the window to 420×180px at mdpi. It checks unchanged full logical/accessibility text and live-region setting, no system-toast replay, touch pass-through, and an accessibility-recommended 8-second lifetime (survival beyond the ordinary short timeout and subsequent expiry). It does not implement a vertical-to-horizontal switch or certify exactly-once screen-reader speech.

With the exact current caller's single newline, the combined Mongolian and Manchu hints require 101px of complete horizontal text height, but only 92px remains after the tested shrink on both APIs. Retaining horizontal rendering therefore needs its own complete-layout check; it is not a universal overflow solution for a hypothetical expanded route. A separately named blank-paragraph stress fixture is retained only in the shaping sweep. These direct-helper results are **not current vertical-profile foreground defects**; current production routes those profiles to system toasts.

A later implementation can keep one logical node while reflowing a fitting measured layout. If an optional horizontal fallback is chosen, it also needs a full-layout fit check. If neither fits, dismissal without replay avoids deliberately creating a second announced surface but shortens availability. Switching an already-visible notice to a system toast can repeat speech: the toast owns its own accessibility event. The resize policy must be explicit; no claim of universal fit or guaranteed exactly-once TalkBack speech is made here.

## Verification and limits

Exact run totals, native pixel counts, source hashes and stage results are recorded in `summary.json`, `provenance.json`, `execution.json` and `data/`. The normal host Python suite passed all 304 tests with no failures or skips. Three runner-input checks also passed: occupied output, empty classpath component and modified dependency bytes were rejected before compiler execution. Its printed negative-fixture error payloads are expected test inputs, not Android failures.

The portable harness requires no cached application classes. It compiles the unchanged `LocaleTypography`, `LocaleNotification` and `VerticalText` sources against pinned framework/test JARs. It uses:

- A manifest-free Robolectric activity, native graphics, API30 and API35
- Exact repository font bytes attached as assets
- Existing catalogue XML strings and all 140 picker tags extracted into explicit fixture files; this does not establish AAPT/resource-linked application behavior
- A diagnostic-only `EditorColours` substitute (black ink/light gray container) because application resource initialization is intentionally absent
- Generated resource identifiers solely to compile three resource-bearing lifecycle methods and unused enum UI-label getters that are **not executed**; the twelve selected existing methods remain intact
- The Android framework JAR's annotations for isolated Kotlin compilation; this is not Gradle compilation, lint, a production APK, an instrumentation APK or emulator acceptance

Native font-scale conversion is actually exercised. In particular, API35's nonlinear conversion produces 18.8px/26px for 14sp at 1.3×/2× mdpi, whereas API30 produces approximately 18.2px/28px. A superseded initial linear-size sweep was not used as the final font-setting evidence.

The five measured profiles cover both column directions and all three null-configured-face cases. Joined words, long unbroken names, mixed scripts, supplementary characters, normal emoji sequences, the unsupported ZWJ counterexample and explicit paragraphs are retained unchanged. An oversized joined word is rejected by final height even if the nominal wrap target was smaller.

Not established: a production vertical route; real editor header/cursor/dialog interaction acceptance for such a route; API21/29 execution of these new diagnostics; physical-device fonts, real IME animation, TalkBack speech, arbitrary filename glyph coverage or universal message fit. Existing API boundaries and app behavior remain byte-for-byte unchanged.

The diagnostic files live only under `verification/`, which the existing Android workflow excludes from automatic app rebuilds. This is an evidence-only PR; no workflow is weakened and no failing app test is skipped. Fresh review should assess the evidence and scope, not treat this as app-build acceptance.

## Reproduce

For the original native run, check out the measured commit and use these unchanged
probe/runner files. For a new run on a newer checkout, keep its outputs separate and
record its own input hashes; do not overwrite or relabel the historical results.
Run `python verification/vertical-notices-2026-10-09/probes/check_evidence.py`
from the publication checkout for a fresh evidence-integrity check. To check the
same package against the frozen source instead, pass `--source-root /path/to/frozen-checkout`.
The checker accepts only the exact frozen bytes or exact integration bytes in the
audit and independently rechecks measured catalogue values and the cursor caller.
Its checks remain active under `python -O`. Add `--self-test` to run its isolated
normal/optimized positive and corruption-rejection tests; those tests change only
temporary copies and do not execute native tests.


Use Linux x86_64/OpenJDK21 (recorded build 21.0.12.1+1-1-deb13u1-Debian), Python3.12 and Kotlin compiler 1.9.24, Robolectric 4.14.1/JUnit4.13.2 and the exact dependency JARs listed in `dependencies.json`, including Maven coordinates and compiler/runtime/framework roles. Include the extracted AndroidX monitor/idling AAR class JARs. Place the two uninstrumented Android framework JARs in one directory. The runner requires a new/empty output directory, rejects directory/empty entries in supplied classpaths, and verifies dependency filenames and SHA-256 digests before compilation. This prevents cached application classes from silently satisfying missing inputs. The output status must say `completed`; prepared, interrupted, failed or partial stages are not accepted.

Run `probes/run.py --repo /path/to/AN-Paint --out /path/to/output --compiler-classpath "$KOTLIN_COMPILER_CP" --runtime-classpath "$ROBOLECTRIC_TEST_CP" --android-jars /path/to/framework-jars`.

Use `--suite measurement`, `host`, `transitions` or `lifecycle` for a focused rerun. Output includes raw TSVs, exact source/input hashes, stage exit codes, logs and PNGs. These diagnostics are opt-in and do not enter the normal Gradle test inventory.

## Next design questions

1. Define a shared measured layout or ink-envelope contract that accounts for fallback shaping, punctuation substitution, rotation and clusters wider than one cell. Keep measurement and drawing on the same representation; do not silently duplicate the renderer in a notice helper.
2. Preserve full logical/accessibility text while separating internal rendering lines. Evaluate direction independently from whether a configured face exists.
3. Use actual host insets/offsets and require complete ink containment before attaching a vertical notice; keep initial no-fit system-toast fallback.
4. Choose the post-exposure resize policy: measured reflow, an independently fitting horizontal option, then explicit dismissal if no layout fits, without a second app-owned surface or a restarted timer.
5. Only after that contract and policy are defined, implement the bounded foreground route and rerun resource-linked application, API-boundary, lifecycle, accessibility and device checks for its exact head.

### Primary platform references

- [MeasuredText.getBounds](https://developer.android.com/reference/android/graphics/text/MeasuredText): API29 building block for supplied shaping runs, not a drop-in bound for this renderer's private transformed layout
- [Layout](https://developer.android.com/reference/android/text/Layout): `computeDrawingBoundingBox` is available from API35
- [TextRunShaper](https://developer.android.com/reference/android/graphics/text/TextRunShaper): available from API31
- [Android14 nonlinear font scaling](https://developer.android.com/about/versions/14/features#non-linear-font-scaling)
- [API35 ToastPresenter source](https://android.googlesource.com/platform/prebuilts/fullsdk/sources/+/refs/heads/main/android-35/android/widget/ToastPresenter.java): system-toast accessibility event ownership
