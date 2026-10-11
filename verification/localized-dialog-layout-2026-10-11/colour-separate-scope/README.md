# Separate Advanced Colour corrective gate

The original positive test is preserved here, not credited as passing. Its full
source was fetched directly from the pinned GitHub commit recorded in
`source-identity.json`. The method excerpt retains its exact original bytes,
including indentation and its closing newline (the following inter-method blank
separator is outside the excerpt). The full source supplies its helper
implementations and records the unchanged positive requirements.

## Why this case moved

Run [38109511511](https://github.com/c933103/AN-Paint/actions/runs/38109511511)
executed the installed API35 case on a measured 640 × 320 screen at 1× font scale.
It failed waiting for a positive Advanced Colour editor viewport. The retained
failure screenshot shows the title, tabs, saved palette and native action buttons
but no usable editor area. The original receipt did not emit inner/holder geometry
before that wait, so it does not prove an exact zero-height measurement by itself.

PR49 changes the About title and legal-notice layout. Its horizontal colour body
and native dialog path are required to stay baseline-identical by a separate,
pinned production-source guard. Their original positive test failure remains an
open corrective item. Source equality is not an untouched-baseline installed test:
that comparison is still pending.

The explicitly renamed PR49 case,
`unchangedAdvancedColourReportsShortLandscapeLimitation`, captures holder, editor,
content, fixed-control and native-dialog geometry before asserting the observed
zero viewport. It then requires a real visible Cancel tap, exactly one close and
no colour commit. Its two images are explicitly named `colour-limitation` and
`colour-cancelled`. A passing characterization proves neither usability nor repair.
Both its receipt and collector keep `positive_viewport_accepted=false` and
`untouched_baseline_installed=pending`.

## Separate positive acceptance requirements

1. Replay the archived positive method unchanged against untouched baseline app
   source at the original API35, 640 × 320, 1× configuration. Carry over only the
   test harness needed to install/run that exact method; record all harness/source
   identities and do not alter colour production code before this comparison.
2. Diagnose the actual measured native title/action/custom-body allocation. Retain
   the original failing evidence and new bounds, layout parameters and screenshots.
3. For any separately authorized colour repair, require positive finite holder and
   editor dimensions, real content overflow and an actual native swipe that changes
   the internal editor scroll position.
4. Require complete visible bounds for the Advanced tab, custom-colour controls and
   Add action before and after the internal swipe. Their positions must stay fixed.
5. Require an actual reachable Cancel tap, one close callback and no colour commit.
   Preserve draft/value behavior and test repeated opening/dismissal as appropriate.
6. Do not substitute this negative characterization, screenshot creation, clipping
   suppression, ignored tests or increased wait time for the positive assertions.
   Restore a positive installed acceptance identity when the separate repair is
   ready. Large-text (2×) short-landscape coverage remains diagnostic until separately
   established; it cannot be inferred from 1×.

The original export hash, workflow run, checked-out merge/base identities, full
source hash and method hash are recorded in `source-identity.json`. Original failed
exports remain diagnostic evidence; this directory does not relabel them as green.
