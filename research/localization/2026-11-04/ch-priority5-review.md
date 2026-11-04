# Chamorro: five reviewed priority additions

Base: `c2d1e61025f50327e329b8cbe62adc5fd60386b3`.

Five P1 entries are added to the canonical XML after independent contextual review. The prior 333 entries remain unchanged. This is not native-speaker certification.

## Review decisions

- `ui_fg`: accept_as_compact_role_cue. Drawing is a functional shorthand, not a literal translation of foreground. In the paired colour-control context it is reasonable. ColourStatusButton has 132dp width and 123dp text budget at 11dp, then scales down; six letters plus hex appears conservative, but actual font rendering was not tested.
- `ui_bg`: hold_semantic_ambiguity. Brin means canvas and omits eraser and shape-interior roles. The full accessibility description is correct but does not resolve the abbreviated visual label for sighted users. Do not certify this as an equivalent of BG without a terminology decision. Literal front/back alternatives are not established UI terms either, so no speculative replacement is applied.
- `ui_fit_image`: accept_wording_only. Consistent with existing view-fit wording. No live call in supplied files, so this is not evidence of runtime semantics or coverage.
- `ui_fit_selection34`: accept_caller_semantics. fitSelectionToCanvas scales floating geometry proportionally to the canvas, centers it, and resets rotation to zero while keeping original pixels. The caller also invokes paintCanvas.fit. Wording distinguishes image placement from view magnification; label need not enumerate centering and rotation reset.
- `ui_from_device34`: hold_terminology_ambiguity. Primary dictionary defines ramienta as tool, with carpenter and hand-tool examples, not an electronic device. Existing locale uses it for software tools. This may be understood as From this tool instead of from the phone/tablet. Picker semantics are otherwise correct and do not justify saying only local files.
- `ui_pinch_and_pan_mode`: revised_accept_wording_only. Added i mostra after mineddung so resizing clearly affects the view, not image data. No live caller found in supplied files; keep that coverage limitation separate from wording review.
- `ui_drawing_canvas_pinch_and_move_two_fingers_to`: revised_accept_caller_semantics. Reordered shrink/enlarge to match near/far finger order, avoiding a possible inverse-gesture reading. Code uses span ratio for zoom and midpoint movement for pan; Navigate remains one-finger pan. Exact existing Navigate label retained. Primary teaching material attests dos na kålulot, but full sentence has no native-speaker review.
- `ui_watercolor`: hold_medium_ambiguity. Pintura is attested as paint/dye, so this is not the erroneous color of water. However paint with water is broader than the watercolor art medium and could include generic water-based paint. No established watercolor term was found; absence of a search hit is not proof none exists. Keep as a candidate pending a medium-specific wording decision.

## Caller evidence

Source links are pinned to the integration base:

- [ColourStatusButton.kt](https://github.com/c933103/AN-Paint/blob/c2d1e61025f50327e329b8cbe62adc5fd60386b3/Paintroid/src/main/java/org/catrobat/paintroid/classic/ColourStatusButton.kt#L45-L74): the short foreground caption shares space with a hex code, uses 11dp text and scales down; the accessibility descriptions remain unchanged. [ClassicPaintActivity.kt](https://github.com/c933103/AN-Paint/blob/c2d1e61025f50327e329b8cbe62adc5fd60386b3/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L417-L420) allocates 132×88dp. No rendered measurement is claimed.
- [Selection caller](https://github.com/c933103/AN-Paint/blob/c2d1e61025f50327e329b8cbe62adc5fd60386b3/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L755-L756) and [implementation](https://github.com/c933103/AN-Paint/blob/c2d1e61025f50327e329b8cbe62adc5fd60386b3/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L405-L413): proportional floating-image placement, centred on canvas with rotation reset, source pixels preserved. Distinct from viewport fit.
- [Two-pointer gestures](https://github.com/c933103/AN-Paint/blob/c2d1e61025f50327e329b8cbe62adc5fd60386b3/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L653) use span for zoom and midpoint motion for pan. [One-finger navigation](https://github.com/c933103/AN-Paint/blob/c2d1e61025f50327e329b8cbe62adc5fd60386b3/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L739) depends on Navigate. The accessibility text quotes the existing navigation label exactly.

No live references to ui_fit_image or ui_pinch_and_pan_mode were found in the five inspected exact-base editor files (ClassicPaintActivity, PaintCanvas, PaintDocument, ColourStatusButton, UiText). Their acceptance is wording-only, not a whole-tree absence assertion or live-route certification.

## Narrow lexical references

- [Guam early-learning material, page 34](https://www.guamehdi.org/wp-content/uploads/2016/12/2010-Hugando-Playbook-English.pdf) attests dos na kålulot.
- [Revised dictionary, R](https://natibunmarianas.org/r/) identifies ramienta as tool and ramenta as hand tool; this does not resolve the device wording.
- [Revised dictionary, P](https://natibunmarianas.org/p/) identifies pintura as paint/dye, not specifically the watercolour art medium.

## Validation and limits

Focused checks passed XML parsing, missing-only unique additions, exact reviewed values, preservation of existing nodes and bytes, source attributes, placeholder parity, Android escaping, format syntax, exact navigation quotation and deferred-key absence. Escaping/format checks use the helper fetched at the exact base. These are focused checks, not the full repository aggregate.

Direct coverage is now P0 92/92 and P1 246/249; BG, From device and Watercolor remain missing. Full catalogue coverage is 338/717. Coverage is not linguistic acceptance. No Android build, hosted CI, native-speaker certification or device/font rendering was run. Canonical XML owns wording; this report does not freeze translations.
