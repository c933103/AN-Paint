# Zhuang animation import notices

Base: `ec03790f20714ddd5a6abc03d3109ff67394421d` on `review/nv-bottom-2038-20261103`.

This batch adds five missing P0 resources: the animated-image title, Open still image action, frame-count notice, first-frame import notice and separate-PNG-default-image notice. All 107 previous typed resources and attributes remain unchanged. No implementation, English resource, other locale or font changes.

## Meaning and current consumers

The new wording receives independent full-value linguistic and semantic review against `ImportSelection.kt` and `AnimationMetadata.java`. Earlier research packets were nominations, not approvals. The accepted scope is bounded authored composition with moderate confidence, not native-speaker certification or restoration of withdrawn historical conclusions.

The dialog distinguishes images with known multiple frames from containers whose bounded scan cannot confirm animation. Its count argument remains a String that may contain an exact number or an English lower-bound phrase. The positive button imports index zero; cancellation does not import. PNG with a separate default image follows a distinct branch from importing an animation's first frame. Quoted saving instructions use the current Zhuang Save caption, `Cunz`.

The count clause was revised to identify pictures contained in the animated image, rather than a generic picture count that could include PNG's separate default image. The poster clause was scoped to this animation, rather than a general refusal to open animated images. Still-image output is described as an image saved by AN Paint that does not move, without claiming that a save already succeeded or that the original file was changed.

Picture/nonmoving descriptions and the saved-image relative clause are functional compositions. They are not claimed to be published technical animation terminology. The unknown-animation warning remains English fallback: its old draft described not knowing an exact generic picture count, which does not preserve the inability to confirm multiple animation frames. A proposed animated-versus-static alternative was also withheld because repeated frames need not visibly move. The lower-bound count label likewise remains English fallback; its placement in the composed numeral slot needs separate review. Full localization of every dialog is not claimed.

Language evidence includes [the picture-classifier example](https://www.guangximinzubao.cn/szbzw/html/2018-06/20/content_26157.htm), [official ordinal and negative-modifier terminology](https://www.guangximinzubao.cn/sy/gg/383691.html), [descriptive nonmovement in a Zhuang linguistic example](https://www.scholink.org/ojs/index.php/sll/article/download/35742/8656) and [digital-picture usage](https://www.guangximinzubao.cn/szbzw/page/21/2023-11/08/08/2023110808_pdf.pdf). Direct/indexed textual support and authored extensions are distinguished; no PDF-raster certification is claimed.

## Verification

- 90 affected host tests pass, including the production Java animation scanner's container, exact-count, lower-bound, poster/default and uncertainty cases, plus localization structure, formatting and priority checks. This is not the full repository suite or an Android dialog execution.
- All 171 offered language options and the priority manifest pass structural validation.
- Ten English/Zhuang Java resource-template checks pass. Missing-only unique additions retain canonical source attributes, indexed argument types/order, literals and valid Android/XML escaping.
- All 1,252 materialized base files match the freshly fetched remote tree's Git blob hashes and executable modes. Its 237 unmaterialized non-tree entries remain unchanged.

Direct presence becomes P0 56/94, P1 56/249, P2 0/305 and P3 0/71: 112 typed resources total. P0 gaps decrease from 43 to 38. These are presence counts, not whole-catalogue linguistic acceptance.

No Android build, AAPT, device/layout test, hosted CI, native-speaker certification, merge or release is claimed. Publication uses an exact expected parent and non-force lease, followed by full remote-tree and changed-file verification. Canonical Android XML owns current wording; no permanent sentence mirror or per-batch test package is added.
