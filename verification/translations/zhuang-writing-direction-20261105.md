# Zhuang writing direction

Base: `6a341af73a5f39932389330e02d66c8dd33110e7` on `review/nv-bottom-2038-20261103`.

Adds the P1 writing-direction label (`ui_text_direction23`) and its three P2 choices (`ui_horizontal23`, `ui_vertical_rl23`, `ui_vertical_lr23`). All 192 earlier typed resources and attributes remain unchanged. Only Zhuang XML and this report change.

## Wording and evidence

Independent review supports all four entries. The title describes writing direction. The horizontal option does not impose left-to-right order. The two vertical descriptions separate top-to-bottom layout from the order in which vertical lines are placed. Confidence is moderate overall, with narrower confidence in the complete vertical typography phrases: their component meanings are supported, but the full compositions are not attested UI terminology.

- [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): direction at F.htm 23/29; horizontal at V.htm 10/19; arranging/placing at B.htm 13/80; row/rank and line classifier at H.htm 19/45; above at G.htm 91/110, below at L.htm 1/49, right at G.htm 79/110 and left at S.htm 51/52. The line word is not independently established here as a specialized typographic column term. Its vertical meaning comes from the preceding top-to-bottom clause. The mirror warns of incomplete proofreading.
- [Guangxi Minzu Bao, 10 September 2025](https://www.guangximinzubao.cn/szbzw/html/2025-09/10/content_54482.htm), paragraph beginning “Mizgven bouhmonz,” corroborates the modern spelling of the direction noun. [Classroom account, 3 December 2025](https://www.guangximinzubao.cn/szbzw/html/2025-12/03/content_55130.htm), paragraph beginning “Gij daiz gyausiz,” corroborates writing characters alongside reading and drawing. Both pages were directly readable; neither establishes the complete software labels.

## Actual consumers and checks

`TextStyleDialog` uses the whole direction resource for its visible label and accessibility description. The three whole option resources map, in order, to `HORIZONTAL`, `VERTICAL_RL` and `VERTICAL_LR`. Selection updates the preview and is carried into committed `TextSettings`; glyph orientation is a separate control. Preview and placed document text use the shared `VerticalText` renderer.

Horizontal rendering uses Android `StaticLayout` shaping, not forced left-to-right text. In vertical modes, newline-separated lines form columns: LR increases the column x position and RL decreases it. Runs advance downward, while sideways words retain shaping and rotate 90 degrees. Therefore the top-to-bottom description concerns column layout, not a guarantee about every logical character's direction within bidirectional sideways runs. This change does not alter rendering.

- 61 host tests pass in 10.223 seconds: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest validate. Eight English/Zhuang Java literal render checks pass.
- Missing-only XML checks preserve all earlier values, source attributes, placeholders, newlines, literal requirements, escaping and prefix bytes. Temporary token-aware checks cover the actual resource bindings, enum order, preview/commit propagation, separate orientation control and renderer branches. These are static checks, not executed Android typography.
- All 1,252 materialized base files match fresh Git hashes and executable modes; 264 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full-tree and exact changed-file verification.

Zhuang direct presence is now 196 resources: P0 68/94, P1 125/249, P2 3/305 and P3 0/71. Global gaps are P0 163, P1 1,366, P2 30,126 and P3 7,481; 46 options contain all tracked resources. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed dropdown layout or clipping, complex-script rendering, cancellation, accessibility, merge or release is claimed. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
