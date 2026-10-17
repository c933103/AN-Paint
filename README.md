# PR117: diagnose and repair two asynchronous test-ordering failures

The original failed run is preserved, not retried or relabelled:
https://github.com/c933103/AN-Paint/actions/runs/39046719952

Its synthetic merge `2116b091a087bb5e44d1f8f531d6584372dc6c0d` has tree
`3ac7a0abe119504abbde70537bd6d4a2fcc46d3d`, identical to source head
`30413454eaa1c1599c15a0a42a4110d8d1976514`.

## Position-device failure and repair

The Ainu Latin method failed the existing eight-second native Cancel dismissal
wait. Its final field tap requested the keyboard asynchronously; `hideIme()`
sampled hidden insets before that show completed. The IME then reported shown
before the Cancel coordinates were injected. No native Back/hide occurred between
them. Same-run Ainu Kana shows the successful comparison: show, native Back,
hidden, Cancel, window removal. All seven methods have four field-triggered
shows; the six passing methods have four Back hides, failed Latin only three.

The evidence strongly supports IME occlusion/input synchronization as the cause.
The actual recipient of the failed touch is not logged; no captured Cancel
ACTION_DOWN/UP is claimed. Production uses the native negative button without a
custom listener. The repair changes test synchronization only: require the
explicitly tapped field and window to be focused with its naturally shown IME
visible before typing; retain native Back hiding; require a focused window and
hidden IME immediately before tap-coordinate capture. No force-show/hide,
programmatic click replacement, action retry, inventory relaxation or deadline
extension is introduced. The existing eight-second wait, 45-second interaction
budget, exact identities, complete text checks and persistence checks remain.

This is the controlled CI soft-keyboard path. It deliberately fails a device
configuration that suppresses the keyboard; physical/hardware-keyboard variants
and an exact-source API30 execution are not certified.

## Portuguese crop-consumer test failure and repair

The same run completed 1,093 JVM tests with one failure. The new pt-BR crop test
clicked before Android's queued OnShow callback installed the production Apply
validator. Its exact Portuguese error assertion consequently found the unchanged
zero-selection preview; the XML also reports unexecuted main-looper runnables.
The repair drains the show callback before any button clicks, keeps the complete
Portuguese validation expectation, and drains/explicitly verifies real Cancel
dismissal. Production crop logic and all eight pt-BR wording corrections remain
unchanged. The same failed run passed all six ImageDisplayLocaleTest methods and
all fifteen SizingAndTrimTest methods; those successes do not make its aggregate
successful.

The original position ZIP and hash are preserved verbatim. All 112 JUnit XML
suites and the JVM job log are retained, including the failure and queued-callback
exception. The 83.96 MB regression artifact's unrelated generated captures are
not duplicated; its exact digest and extraction inventory are recorded.

## Composition and validation

The candidate composes current develop `8c08554995f4d07be1b47736746ab2d0771e810e`,
preserving the exact three-file Greek change from PR118. The delta from 30413454
is three Greek files plus three test repairs; the numeric production repair and
all wording changes are byte-identical to that prior head.

See source-publication.json for the final source head, complete remote-tree
comparison and branch lease. See test-summary.json for final local results.
The host synchronization contract is a source-order/guard check, not an Android
execution. Original-code and four mutation rejections remain separately labelled.
The supplemental direct Kotlin compilation covers the changed JVM test against
previously built dependencies; it is not a full Gradle/device run. New installed
repair verification requires fresh exact-source hosted results.

Prior evidence is preserved separately:
- Original 341-entry review: https://github.com/c933103/AN-Paint/tree/fb0c77cb5964df034989c692d39f952d76a73e01
- Numeric repair: https://github.com/c933103/AN-Paint/tree/f9da527b0b37b52e852470e95c19118f2b95e397

The three pt-BR holds and earlier receipts remain. This packet does not certify
whole-language quality, every app numeric display, runtime layout, native-speaker
acceptance, or any unexecuted device/configuration.
