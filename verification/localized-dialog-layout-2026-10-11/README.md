# Localized About and notice layout repair

## Scope and reproductions

Independent base: develop `691f8870649a1d21d1441f4e3d0e795660b23e9a`, tree
`040a35f40a6e8e143c6a9b2121e804f0704dd5d1`. Production translations, legal assets,
C05 wording and M02 source are unchanged. The project kanban's AN-W04-DIALOG card
and draft PR49 track the ordinary UI work; repository Issues remain disabled.

Actual C05 pixels from [run38102363951](https://github.com/c933103/AN-Paint/actions/runs/38102363951)
show API30/35 notice headings with223–522px text in fixed104px (52dp) viewports at2×,
About-title ellipsis, and clipped Copy all/Other terms captions. Done fits.
[Successor evidence](https://github.com/c933103/AN-Paint/tree/3c871305f7a84767dd2909afd11598e754e27b4c/verification/hungarian-attribution-c05-2026-10-11/acceptance-38104574988)
shows all six selected Hungarian About rows fit, and editor Copy/Save labels are
readable after real ancestor rectangle reveal. Copy's remaining6px/1px clipping
is lower padding. Earlier broad row-clipping/inaccessible-editor claims are
withdrawn; these are not demonstrated defects.

## Current minimal implementation

- Only About explicitly uses `setScrollableTitle`: a multiline title with a
  scrollable viewport capped at22% of screen height. Native AlertController
  continues to own the list, adapter, buttons, body and window sizing.
- Every other horizontal EditorDialogBuilder call retains its original native
  layout. No horizontal remount, adapter replacement, custom-container unwrap,
  button reparenting or fixed window width remains.
- LegalInfo notice titles and footers use intrinsic text with independent
  scrollable viewports capped at25%/35% of the actual available dialog height.
  The body retains the remaining space. Action captions wrap into full-width
  rows when a single row cannot fit; native listeners and verbatim body remain.
- Vertical About behavior is unchanged. Vertical notice headings/actions keep
  natural columns inside direction-aware horizontal scroll containers.
- No translation is shortened to hide a fit problem.

## Validation plan and limits

`applicability.json` enumerates default plus142 locale catalogues and140 picker
languages. It establishes source applicability and direct overrides, not Android
fallback equivalence, runtime acceptance of every language or linguistic review.

`LocalizedDialogLayoutTest` covers API30/35 Robolectric NATIVE,15 representative
horizontal locales at2× in320×640/640×320, en/hu at1×, and five vertical profiles.
Text oracles require intrinsic fit, no ellipsis and each line's actual ancestor
rectangle reveal. Pointer activation uses root-dispatched touchscreen DOWN/UP;
scroll tests use paced DOWN/MOVE/UP and verify settling, clipboard sentinel and
absence of a secondary dialog before the independent Done tap. Read-only pointer
traces retain hit position, attachment and list state; no handler is synthesized.
Actual production rows replace the rejected artificial long-title-as-menu-row
fixture. Long C05 wording remains title-only test input.

Retained About tests preserve the native list/adapter; native credit-editor
regression preserves field identity, draft, selection and exactly-once callbacks
across configuration changes. Robolectric's documented display-resize callback
updates its otherwise stale window frame; no child is directly enlarged.
Normal Advanced Colour regressions retain its finite holder/inner scroller and
fixed controls. The identical diagnostic class on temporary baseline draft PR50
and this candidate records1×/2× short-landscape colour geometry without treating
capture completion as fit acceptance.

Focused installed API35 instrumentation separately checks actual About→notice
rows/footers and credit-editor live rotation. Advanced Colour is separately
characterized as a known limitation, with its positive gate preserved. Real device
input, bounded system font transitions with restoration, screenshots and exact
source-bound receipts are required. They are emulator observations, not physical
hardware, accessibility-service, full-language or native-language acceptance.
Current minimal-source local checks pass556/556 host cases (147.928s), plus the
transport's7 cases under Python -O. After the final bounded foreground-focus
wait was added to the installed fixture, its57 related host checks pass again
(35.923s; `focus-guard-host.log`). The initial full host attempt's sole failure
was the preserved historical whole-file Commons guard: a new exact before/after
hash endpoint now permits only the single About-title presentation call, then
reconstructs and verifies the original bytes. That failure and both endpoints
are retained in `minimal-successor/`. The minimal head `386078641e8793058573f328ce6c2805216893b9` compiled and passed
832 JVM cases (including24 focused dialog cases), with no failures/errors/skips
and lint green in run38107965583. Its installed run failed before the three new
fixture bodies at the exporter cache-path preflight; existing74 native,16 ordinary,
3 gallery and4 vertical methods passed, while restart was correctly withheld.
The ordinary runner took131.244s (instrumentation inner timer129.652s), which
does not establish timing for the unexecuted fixtures. Ten representative original
PNG states were inspected, with readable captions in final revealed states;
per-line reveal is not simultaneous whole-title visibility. See
`minimal-ci-38107965583/receipt.json` for exact identities and inspection limits.
The next batched successor below still requires fresh Android execution.

## Rejected historical iterations

Initial head `447a5d944a2f053dfb659075220aa966deb5a384` failed Kotlin compilation
(missing test-runner import and vertical-bounds spacing argument). Its compiler
excerpt and earlier host-contract failure are retained. Rect arguments are now
copied because Android mutates requestRectangleOnScreen inputs.

The broad horizontal-shell successor `470943f8319a5cb66ad6c4413d5ff431c2e02552`,
tree `378f8737ec7ffbf70570a47985d09f1a882a46a6`, compiled in
[run38105079757](https://github.com/c933103/AN-Paint/actions/runs/38105079757).
It failed8/20 new JVM cases (824 total,8 failures,0 errors/skips) and one installed
API35 Other-images chooser test. Restart phases were correctly withheld and the
exact installed union failed. Resource generation, build and lint passed.
Code review also identified an introduced Advanced Colour holder constraint
regression. That broad approach is rejected and removed, rather than declared
repaired. All old native captures/XML remain historical evidence.

The old pointer-callback failures were not proved to be harness-only. Paced
uptime-consistent events, bounded fling settling, and explicit diagnostic traces
improve the new oracle without accepting the old result. The old rotation test
changed resources but left the model's window frame at portrait dimensions.
Its source limitation is corrected separately from actual installed rotation.

## Batched rotation and fixture successor

Exact-head Code review found that the newly used vertical notice rails inherited
a first-layout-only reading start. Only those two rails now use
`ResponsiveDialogColumns`: retain the distance from the reading start when the
content/viewport range changes, clamp shorter ranges, and leave same-range native
scrolling alone. A focused descendant takes precedence over a touch-reader offset.
The global ColumnScrollView and unrelated dialogs remain unchanged. New API30/35
model tests cover both reading directions, untouched start, intentional offsets,
content/viewport/fitting transitions, deferred native input focus, and a still-open
notice's landscape→portrait→landscape callbacks, with dismissal unregistering its
width callback. This does not establish TalkBack or installed vertical rotation.

The installed collector now canonicalizes only Android's trusted app-cache root.
The private container, exact method directory and bounded regular evidence files
remain independently confined and reject symlinks; cleanup validates a flat
inventory before deleting it. The previous failure and original three failed
method summaries are retained. No layout assertion, method, budget, source-binding
check or native input requirement is weakened. All562 final-source host checks pass (146.765s), including the five new
cache-path contracts and the scoped rail contract. Twelve targeted transport/path
host tests also pass in normal and optimized Python. These host results belonged to `df214fee4f106c4365325412b4f9d3c8530232d5`;
its actual Android failures are recorded below, not superseded by a host pass.


## Run 38109511511 and bounded fixture/phase successor

Head `df214fee4f106c4365325412b4f9d3c8530232d5`, tree
`856fc693af0dfd265acb0f2c9221e91c09d30a6c`, failed
[run38109511511](https://github.com/c933103/AN-Paint/actions/runs/38109511511).
Of 836 JVM cases, 834 passed and two synthetic width/offset cases failed (one per
API). A bare View inside HorizontalScrollView had no intrinsic/minimum width:
its layout-parameter width was ignored under UNSPECIFIED measurement, so the
intended overflow was absent. The successor sets that synthetic minimum width and
asserts measured content width, exact range, real overflow and the immediately
applied offset before resizing. Production is unchanged by this correction. The
real retained notice tests already passed on both APIs, retaining offsets 0/47
for both directions through both rotations in all 16 original JSON records.

All three installed fixture bodies ran and failed. The About clipboard sentinel
created a SystemUI preview that physically covered the Copy-all tap. Credit Copy
passed its clipboard and callback checks, then its SystemUI preview intercepted
the gesture lane used to reveal Done. Actual before-restoration screenshots and
original receipts support these diagnoses. The successor natively dismisses the
system preview with the established bounded UiDevice helper, checks that its
input window disappeared, then retains all original positive clipboard,
reachability and callback-count assertions. It does not disable system features
or invoke app action handlers directly.

The third failure is a genuine zero editor viewport in Advanced Colour on the
installed API35 640×320, 1× fixture. Its implementation and native builder path
are byte-identical to develop after reversing only the unrelated About title
opt-in; the pinned `advanced_colour_pr49_scope.json` guard verifies that exact
scope. This establishes source non-regression, not an untouched-baseline installed
reproduction. The latter remains pending in a separate corrective task. The
original full test source and positive method are preserved byte-for-byte in
`colour-separate-scope/`, with exact provenance and future positive acceptance
requirements. PR49's explicitly renamed diagnostic records collapsed geometry,
requires the narrow measured limitation and native Cancel exactly once without
committing. A passing characterization must never be described as usable/fixed
colour or positive viewport acceptance.

The existing 97 installed methods passed, but restart was correctly withheld and
the overall run remains failed. The 19-case ordinary report took 175.068 seconds
(inner instrumentation 173.304); there was no timeout. The early-failed bodies
used 25.016, 10.629 and 9.370 seconds, so the complete successful flow still has no
measured margin. The new exact three-method dialog phase has a documented
300-second budget; ordinary remains 180 seconds. The full disjoint union is still
mandatory. See `CI.md` for controlled 43/53-minute outer-budget arithmetic. These
successor changes still need fresh Kotlin, model and installed execution.

Historical originals remain immutable. The rejected broad approach is archived at
[dca91abd](https://github.com/c933103/AN-Paint/tree/dca91abd7f3fba09e4cd4f7a87817918b5f07b5f/verification/localized-dialog-layout-2026-10-11/rejected-38105079757).
The untouched baseline's model diagnostic and failed-workflow/99-passed-installed
split are archived at
[9901fbbe](https://github.com/c933103/AN-Paint/tree/9901fbbe2d6d645749a71579217bdfac7cac56b5/verification/advanced-colour-baseline-2026-10-11/run-38105969602);
its temporary diagnostic PR50 is closed without merging.

The initial successor host run retained 28 error/subtest outcomes because two
older synthetic source fixtures lacked the now-required three-method dialog
inventory. They now include the exact API35-only class and matching report/union
counts, while API30 suppression and every negative corruption check remain. One
intermediate run had already loaded the old explicit union assertion; its failure
is retained too. The verifier was not relaxed to accept incomplete inventories.

Final successor host validation passes all 573 cases in 165.076 seconds. The 38
selected matrix/transport/budget/source-scope cases also pass under Python -O.
The strict fake-ADB wrapper checks both exact method selection and refusal of
missing, extra, skipped or truncated reports for gallery and dialog phases.
These host passes do not establish Kotlin compilation or new installed outcomes.
