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
rows/footers, credit-editor live rotation and normal Advanced Colour. Real device
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
are retained in `minimal-successor/`. Current exact-head Android compilation,
runtime and installed results remain pending; host checks alone do not accept
UI behavior.

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
