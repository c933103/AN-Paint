# Shared localized-dialog layout repair

## Scope and reproduction

Independent base: develop `691f8870649a1d21d1441f4e3d0e795660b23e9a`, tree
`040a35f40a6e8e143c6a9b2121e804f0704dd5d1`. No production resource/translation,
legal asset, M02 or C05 source change is included.

Actual original C05 pixels were inspected from [run 38102363951](https://github.com/c933103/AN-Paint/actions/runs/38102363951), source
`d8132ede62bf50a0bd972588703bc6a86222e7f0`. At 320 dp portrait width and 2× text,
API30/API35 notice headings have 223–522 px text layouts inside a fixed 104 px
(52 dp) viewport. About headings and long native list rows ellipsize. Existing
Copy all / Other terms captions clip; Done fits. Editor Copy/Save are outside
the original capture; that initial visibility alone does **not** prove they are
unreachable. The original captures remain C05 evidence, not accepted post-fix
results. One C05 proposed long heading is test input only.

Repository Issues are disabled (GitHub returned 410 on the ordinary issue
creation attempt). The project kanban and separate draft PR track this repair;
repository settings are unchanged.

## Implementation

- Shared horizontal dialogs retain their actual ListView, adapter item IDs/types,
  selection and native Button objects/callbacks, including Save validation.
- Intrinsic-height titles and wrapping menu rows have no line cap or ellipsis.
- The title and action regions scroll independently and use at most 25% / 35%
  of the actual bounded dialog height. The central body retains the remaining
  space; a long title cannot consume the entire body or hide the footer.
- Buttons use a row if every natural caption fits; otherwise full-width rows.
  The footer is a scrollable viewport, not truncated text. Normal wide-screen
  short actions stay together while legal-body scrolling leaves them fixed.
- Notices share those bounded regions. Vertical notice headings/actions use
  reading-direction-aware column scroll views with intrinsic column sizes.
- No action is replaced with a synthetic callback and no translations are
  shortened. Cancel, Back, clipboard bodies and edit/save callbacks are retained.

## Applicability and tests

`applicability.json` enumerates the default plus all 142 canonical locale
catalogues, including all 140 picker languages and non-picker catalogues. Every
language uses the same shared layout code. Direct-source overrides and defaults
are listed per key; that inventory is not an emulation of Android's fallback
resolution and does not certify rendered fit or linguistic accuracy.

`LocalizedDialogLayoutTest` exercises mounted production dialogs with API30/35
Robolectric NATIVE rendering. Fifteen representative horizontal locales cover
Latin expansion, RTL Arabic/Hebrew, Indic, Thai, CJK, exact-script Korean,
Cyrillic Mongolian and bundled Nôm/Wu typography, at 2× in 320×640 portrait and
640×320 landscape. English/Hungarian also run at 1×. Five vertical script/fixture
profiles exercise notice bounds and column-edge reveal at 2× landscape.

Assertions require full intrinsic text, zero ellipsis, each horizontal line's
actual ancestor-mediated scroll reveal, then root-dispatched DOWN/UP pointer
activation. They exercise real ListView rows, notice Copy/Other terms/Done,
cancelled secondary chooser, repeated Back dismissal, and GalleryCredits
Copy/Save/Done/reopen/unsaved Back. Tests do not call performClick/performItemClick
or assign larger test-only child dimensions to bypass visibility failures.
Screenshots and geometry JSON are emitted under the normal regression artifact.

All 549 local host tests pass with no skips; the three focused contracts also
pass under Python -O. The first host attempt failed one inherited source-fragment
expectation that encoded the former vertical-only mount. Its successor explicitly
requires the horizontal/vertical branch while retaining every title/message,
typography and vertical action assertion; the original failure is retained.
Android compilation/runtime is blocked by
the missing Gradle 8.13 distribution and unavailable download route. Exact-head
CI results, captures and Code review are pending publication. No new native
emulator dialog-specific assertion, accessibility-service, physical-device,
native-language or complete-all-language runtime acceptance is claimed. Normal
installed regression checks are a separate CI gate, not evidence that every
localized dialog was visually reviewed.

## First source-review follow-through

Independent review found a missing RobolectricTestRunner import in the new test
class, before runtime acceptance. Initial CI also reports a missing explicit
vertical-bounds spacing argument; the successor supplies the unchanged 1f
spacing. The exact failed compiler excerpt is retained. The batched successor adds it and drains
200 ms of the real main-looper pressed-state delay after dispatched pointer
UP; ListView's callback is not invoked directly. The three strict focused host
contracts pass again. The original failed source evidence is unchanged.

Further independent review identified two concrete defects before acceptance:
`requestRectangleOnScreen` mutates its Rect argument, so the test now passes a
copy and keeps its local-coordinate oracle unchanged; the fixed horizontal
window width also needed a lifecycle-safe resize callback on configuration
change. The responsive root now handles that callback without replacing the
field or intercepting existing dismissal listeners.

The successor additionally tests real DOWN/MOVE/UP scrolling in title/footer
regions, exactly-once action/save/cancel callbacks, a rejected save that must
not dismiss, outside cancellation, and retained-editor configuration dispatch
with draft and callback preservation. The latter is a framework-callback
simulation in Robolectric, not installed-device rotation acceptance. Fresh
source CI must establish compilation and runtime outcomes; earlier host results
alone do not accept these changes.
