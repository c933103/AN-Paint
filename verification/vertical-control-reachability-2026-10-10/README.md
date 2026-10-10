# Native vertical Save reachability: proposed probe

Status: **unexecuted Android test proposal**. No production defect, completed
reachability verification or broad usability acceptance is claimed.

Base: `66c39ca345ef7bc8c5fe1da8ce64cb872c3a0e88`, tree
`a90cdf84be34e6a08ab7a9d25b46cdce2f71b776`.

The source snapshot was independently compared with the remote tree: all 1,341
existing path/blob/mode identities matched before changes. PR18 and its accepted
[evidence-only continuation](https://github.com/c933103/AN-Paint/tree/5f16192207161dd828bf9f37becb7eda9f205365/verification/installed-vertical-matrix-2026-10-10/repair-api35-66c39ca)
remain untouched. Work concerns the distinct unresolved
[control-reachability checklist](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6093775811).

## Why this probe

The original helper accepts a target when its center and a minimum 32dp tap area
are visible. JPEG selection exposes a `NumericSlider` with range 1–100 and a native
100dp-wide SeekBar, inside a 176dp quality column. The accepted test captured that
state but did not change native progress or establish full thumb/end visibility.
Actual Manchu landscape pixels clip the thumb; Literary Chinese / vertical emoji
portrait pixels show partial columns. Scrolling might resolve these observations,
so clipping alone is not classified as a defect.

## Frozen intended coverage

- All four vertical locales, portrait and landscape, through the real native Save flow.
- Native horizontal reveal of the complete quality widget/readout/SeekBar/thumb,
  filename field/preview, JPEG explanation, and dialog actions. Record geometry
  and scroll offsets before and after gestures.
- Native thumb movement to 1 and 100, each from a different value; verify progress,
  display, complete thumb bounds, filename, all canvas pixels and selected tool.
- Original Cancel/reopen/Back flow unchanged; cancelled quality cannot persist.
- Native Choose location on a fresh JPEG form, with one intercepted/cancelled
  document-provider request. Check actual callback quality and request filename/MIME.
- Eight JSON receipts and 64 new rendered frames in a separate evidence subdirectory;
  existing 32-state captures and their validator remain independently required.
- Existing source inventory, collector deadlines, phase budgets and all prior
  assertions remain. No source-production edit or settings/credential change.

## Review and execution gates

1. Root/source review of the complete frozen diff and host checks.
2. Publish only to a separate draft test branch based on this exact head, after
   review. Compare remote tree, including modes and any removals, before CI.
3. Compile and run the existing current-platform API35 workflow. A failed new
   assertion or deadline is retained as failure, not retried without diagnosis.
4. Verify exact source/run/merge-tree/artifact binding, all XML and raw logs,
   receipt checks and actual pixels. The preexisting 180-second phase had 121.531
   seconds on the accepted run; the additional probe duration is unknown until run.
5. Classify native reachability per locale/orientation and control. If an assertion
   fails, determine whether it is a reproducible production limitation or a probe
   problem before proposing any production change. No broad UI redesign.

Local host/source checks cannot substitute for Kotlin compilation, installed
native input, a measured runtime budget or independent visual review. Local
compilation was attempted but the Gradle 8.13 distribution was unavailable and
its download failed with `java.net.SocketException: Network is unreachable`.
No Android compile or runtime pass is claimed.

Coordinate review reference: the Android platform's
[AbsSeekBar implementation](https://android.googlesource.com/platform/frameworks/base/+/master/core/java/android/widget/AbsSeekBar.java)
positions the drawable using left padding minus thumb offset and applies RTL
mirroring in touch tracking. The probe observes the installed drawable bounds and
verifies the resulting native value; source review is not runtime certification.

## Independent review corrections, revision 2

The initial unpublished proposal is preserved at candidate tree
`8a45b54bbbb975d4d7331d8a6ceb62b85eadbffc`, patch SHA-256
`4296f8a6ae8a9d6d576161eea5b54e70396866def2c7783acb0fd0b2b220e01b`.
Independent review identified two test-oracle gaps:

1. Portrait confirmation persisted quality 1. The landscape endpoint sequence
   could finish at 1, making its Cancel draft indistinguishable from remembered
   quality. Revision 2 performs another real endpoint gesture when necessary,
   asserts distinct values immediately before Cancel and stores both values.
   The receipt verifier and a focused negative reject that exact equal-value
   landscape precondition, including when the screenshot state reports 1.
2. Both geometry helpers returned Android's undefined output rectangle when
   `getGlobalVisibleRect` returned false. Revision 2 returns a fresh empty Rect
   in both helpers. Both installed negative fixtures deliberately write a
   nonempty rectangle before returning false. Host source/fixture contracts
   reject removal of either guard; they do not substitute for installed execution.

The Android 15 contract explicitly leaves the output undefined on a false result:
[View.getGlobalVisibleRect](https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-15.0.0_r1/core/java/android/view/View.java).

One pre-existing helper line is deliberately hardened. The claim that every
original line is unchanged is therefore withdrawn for revision 2. All original
assertions and thresholds remain, and production source, workflow and phase
budgets are unchanged. No prior screenshot or accepted evidence is overwritten
or retroactively revalidated. The original 32-state capture evidence remains a
bounded claim about its exact old source, independently of this proposed probe.

The additional native drag and 64-frame probe duration remain unmeasured inside
the unchanged 180-second phase. A timeout stays failed. A drag-specific failure
also does not prove that every native endpoint tap route is inaccessible.
