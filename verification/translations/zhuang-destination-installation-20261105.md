# Zhuang destination-installation failure

Base: `dea73e0b2307e63f57eb7f1b522e28b9884c3599` on `review/nv-bottom-2038-20261103`.

Adds the missing P0 `save20_destination_error` notice. All 123 existing typed resources, their attributes and the preceding file bytes are preserved. No implementation, default English, other locale, font or test-framework changes.

## Independent wording and consumer review

The previously unaccepted nomination was reviewed afresh and retained. Its functional meaning is “AN Paint cannot move the new file to this location.” This is a bounded file-installation diagnostic, not a claim of insufficient memory, a successful save, an existing old destination, or a retained temporary copy.

Current `BitmapFileCodec`, `DibCodec`, `IcoCodec` and `TextImageCodec` all emit this resource when moving a completely written temporary file to its target fails. The text codec helper also serves Base64 image import and Base64/ASCII exports, so the authored file wording applies beyond saving the current canvas. The completed write precedes the attempted move, and each path removes its temporary file in cleanup. The translation deliberately makes no promise about recovering the new file or preserving old destination contents.

Fresh primary evidence supports the transitive movement construction and destination goal: [moving books to a doorway](https://www.guangximinzubao.cn/szbzw/page/21/2024-05/29/05/2024052905_pdf.pdf) and [moving bee colonies to another location](https://www.guangximinzubao.cn/zw/f/382446.html). [An explicit actor with negative ability and an overt object](https://www.guangximinzubao.cn/szbzw/html/2025-08/27/content_54391.htm) supports the negative construction. [An individual document](https://www.guangximinzubao.cn/szbzw/html/2015-03/04/content_12240.htm) supports the noun/classifier combination. The book passage was inspected as indexed primary PDF text after direct access failed; the other pages were read directly. No PDF-raster verification is claimed.

The complete software sentence is authored composition, not an attested quotation. Extending ordinary movement to a file operation is judged appropriate at moderate confidence. The current catalogue already uses the same file noun and contextual location expression in write failures. Native-human approval is not treated as a publication gate; this review does not claim native-speaker certification.

## Verification

- 77 affected host tests passed in 9.829 seconds: current localization contracts, general resources, formatting boundaries, priority accounting and existing help/save-export checks. This is not the full repository suite.
- Structural validation passed for all 171 offered catalogues and the priority manifest. The single addition is unique and missing-only, preserves source attributes and has no format arguments. Android/XML escaping checks passed.
- Two English/Zhuang Java resource-template checks passed. These are host checks, not Android rendering.
- Current-source checks confirmed all four destination-failure callers, write-before-move order, cleanup and the shared text helper's import/export scope. No runtime file-failure test was executed.
- All 1,252 materialized base files matched the freshly fetched remote tree's Git hashes and executable modes; its 241 unmaterialized non-tree entries are preserved by the base tree.
- Zhuang direct presence becomes P0 66/94, P1 58/249, P2 0/305 and P3 0/71: 124 typed resources. P0 gaps decrease from 29 to 28. Across 171 options, direct gaps become P0 165, P1 1,433, P2 30,129 and P3 7,481; 46 options have all 719 tracked resources. Presence does not establish whole-catalogue translation quality.

No Android build, AAPT, installed/device/layout/accessibility test, hosted CI, merge or release is claimed. Longer export and memory warnings remain unchanged. Publication uses the exact expected parent and a non-force branch lease, with full remote-tree and changed-file verification. Canonical XML owns the wording; no permanent sentence mirror or per-batch test package is added.
