# Zhuang resize and memory notices

Base: `2d97ae246a9d31ae3e945a5e14b335e19b41e4bb` on `review/nv-bottom-2038-20261103`.

Adds five missing resources: three P0 entries for the large-image resize question, operation memory failure and assembly memory failure with retained sources; two P1 entries for the Resize image menu command and dialog title. All 112 previous typed resources and attributes remain unchanged. No implementation, English resource, other locale or font changes.

## Independent review and meaning

The five complete values received independent source-supported linguistic and current-consumer review at moderate compositional confidence. Earlier packets were nominations, not approval. The dimensions wording uses an explicit picture noun and asks about a user-selected action. Menu and dialog captions differ only by the menu ellipsis. They refer to whole-image resampling, not zoom or canvas-edge resizing.

The general memory warning was revised. Its old conditional could describe a hypothetical future shortage rather than the failure being reported. The accepted version keeps original dimensions as the diagnostic scope and uses an occurrence-specific negative for no automatic resizing applied. A stronger proposed account of what resolution the operation actually used was rejected: the same error handler also handles manual resize/new-image failures. The translation preserves the English scope without claiming that every failure allocated an original-size target.

RAM means working memory, not disk storage. The assembly warning says the source files used for the image group remain present. It does not promise unchanged layout, metadata, pixels, undo state, every transient import, a new backup or a successful retry.

Current consumers checked: `ImageResizeDialog.kt`, `ClassicPaintActivity.kt`, `PaintDocument.kt` and `AssemblyActivity.kt`. The two memory warnings follow observed `OutOfMemoryError` paths; estimated-budget exceptions and copy/loading explanations are separate. The Resize image command passes the stretch/resampling path to the dimensions dialog and `PaintDocument.resize`. These are source checks, not Android dialog execution.

Evidence includes [physical dimensions and image enlargement](https://www.guangximinzubao.cn/zw/f_282583/377720.html), [picture reference and questions](https://www.guangximinzubao.cn/szbzw/html/2018-06/20/content_26157.htm), [occurrence-specific negation](https://www.guangximinzubao.cn/zw/f/637638.html), [original modifiers](https://www.guangximinzubao.cn/szbzw/html/2021-09/29/content_41823.htm) and [temporal still-existence/use-purpose descriptions](https://www.guangximinzubao.cn/zw/y/377700.html). Authored technical extensions remain distinct from attested whole software sentences. No native-speaker or PDF-raster certification is claimed.

Unreviewed copy/loading/estimated-memory text and previously held sharing/animation warnings remain English fallback. This batch does not resolve those separate obligations.

## Verification

- 82 affected host tests pass: localization structure, current formatting/legal boundaries, help/recovery routes, priority accounting, memory-warning source distinctions and number-input wiring. This is an affected subset, not the full repository suite.
- All 171 offered language options and the priority manifest pass structural validation.
- Ten English/Zhuang Java resource-template checks pass. Five unique missing-only additions preserve source attributes, formatting and Android/XML escaping. The exact accepted values, menu ellipsis and unchanged held-key absences were verified.
- All 1,252 materialized base files match the freshly fetched remote tree's Git blob hashes and executable modes. Its 238 unmaterialized non-tree entries remain unchanged.
- Direct presence becomes P0 59/94, P1 58/249, P2 0/305 and P3 0/71: 117 typed resources total. P0 gaps fall from 38 to 35 and P1 gaps from 193 to 191. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, device/layout test, hosted CI, native-speaker certification, merge or release is claimed. Publication uses an exact expected parent and non-force lease, followed by full remote-tree and changed-file verification. Canonical Android XML owns current wording; no permanent sentence mirror or per-batch test package is added.
