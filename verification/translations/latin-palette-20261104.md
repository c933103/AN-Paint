# Latin saved palette and recent colours

Base: `c0dc6a2da211ebfcf6737a8f7c5f8c00f9278e8f` on `review/nv-bottom-2038-20261103`.

## Scope and review

Twenty missing Latin strings cover custom/saved palette actions, selected/stored/empty palette slots and recent-colour accessibility captions. Independent language/context review accepted all twenty unchanged. Existing terms for palette, colour, saving, editing, foreground and background are retained. All 381 previous typed resources remain unchanged; the additions give 401 typed resources.

`AdvancedColourDialog.kt` uses custom-colour labels, empty-slot descriptions, the saved heading, add feedback and full-palette replacement selection. `ClassicPaintActivity.kt` uses saved-palette controls, background/edit/remove actions and recent-colour descriptions. Recent colours retain tap-for-foreground and hold-for-background behavior. The active colour is the replacement being supplied, not the item to alter. The retained stored-slot instruction quotes the exact stem of its replacement caption.

The six retained `colour20` slot resources are translated from their source without claiming that they are currently routed to the live editor confirmation button. No direct static call found is not proof of an unused resource. Nothing is removed or rerouted.

## Checks

- 78 existing host tests passed: translation catalogues, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through, and open-review recovery.
- All 171 offered options pass existing structural validation.
- 40 Java formatter cases passed across the English and Latin templates, including uppercase six-digit hexadecimal output.
- Source attributes, XML/Android escaping, ordered typed arguments, `%2$06X` width/case, newline escapes and numeric literals are preserved.
- Latin direct priority presence: P0 94/94, P1 249/249, P2 58/305 (previously 38/305), P3 0/71. Remaining priority keys: 318.
- 1,252 materialized source files were checked against expected Git objects and modes; the other 206 non-tree entries remain in the base tree. Publication uses an exact-parent non-force lease, full remote tree comparison and changed-file readback.

## Limits

This is bounded independent AI language/context and host structural review, not whole-catalogue linguistic acceptance or native-speaker certification. Technical Latin is a modern adaptation. No Android build, AAPT, installed layout, device, accessibility, runtime or CI acceptance is claimed. No runtime routing changes, deletions, release, merge or issue-tracker updates are included. Canonical XML owns the text; no permanent language-approval mirror or per-language wording test was added.
