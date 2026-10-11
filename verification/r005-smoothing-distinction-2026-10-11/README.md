# R-005: stroke smoothing versus pixel-edge antialiasing

Date: 11 October 2026. **New bounded completion of R-005 only.**

The two controls have distinct meanings and independent source bindings: smoothing
changes the freehand path geometry, while antialiasing changes how eligible geometry
is rasterized. The retained Malay objects, `sapuan bebas` and `tepi piksel (antialias)`,
preserve that distinction. No production edit is required for this row.

This is a fresh source/API and model linguistic review. It is not Kotlin execution,
installed Android rendering verification, native-speaker certification, full Malay
wording acceptance, or completion of R2/PR3/the localization reset.

## Original question and recovered scope

The canonical row asks: **“R2: recheck the distinction between stroke smoothing and
pixel-edge antialiasing.”** Its originating [R2 requirement at the rejected report's
pinned version](https://github.com/c933103/AN-Paint/blob/e51ab25c0/verification/localization-reconciliation-2026-09-28.md#L44)
requires the two Malay controls to retain that distinction while wording is corrected
in the original and integration copies. This earlier report defines the claim being
rechecked; it is not evidence that the claim is true.

The original 22 September locale instruction, its subsequent locale-thread tail,
and the 28 September rejection/reset were read again. The relevant original thread's
reader returned its final 23 September message with `next_cursor=null`,
`truncated=false`, and no omitted message content. The requested work concerns
Tagalog, Cebuano, Malay and Indonesian; the historical completion assertion is
withdrawn. The reset explicitly requires each item to be independently rechecked.
This retrieval does not claim recovery of all eight other discussions or close R1.

Current [PR3](https://github.com/c933103/AN-Paint/pull/3) and
[PR15](https://github.com/c933103/AN-Paint/pull/15) descriptions and their full returned
comment timelines were read. PR3's 6 October report supplies the later retained
`Licinkan` correction. Its old behavioral explanation was treated as a lead and
independently checked below. Neither PR discussion adds a runtime or native-speaker
certification requirement specifically to R-005. Both original PRs are now merged;
their historical draft wording does not describe their current state.

## Pinned source and current candidate comparison

The five source snapshots are:

| Snapshot | Exact ref |
| --- | --- |
| Current develop | `691f8870649a1d21d1441f4e3d0e795660b23e9a` |
| Accepted bounded composition, draft PR52 | `2755e30573d6ea2c071a128b6fa2940fc675af1a` |
| Accepted bounded colour repair, draft PR51 | `512360bffef3abb393557bce29a30217b03c5ecc` |
| Original PR3 source head | `b0f916377353f1c8102ad08c4faf132af4c83a2f` |
| Canonical integration/register branch before this report | `32d196a8fa1cd085646ae3f81722ac8d317daa49` |

For each snapshot, full `ClassicPaintActivity.kt`, `PaintCanvas.kt`, `PaintDocument.kt`,
English XML and Malay XML were fetched through the repository connector. All 25
full-content Git blob hashes were independently recomputed. [Source manifest](source-manifest.json)
contains exact refs, paths, URLs, blob hashes, SHA-256 hashes and byte lengths.

The three complete relevant methods and both exact labels are identical across all
five snapshots, even though surrounding files differ. The source remains retained;
PR51 and PR52 remain draft and unmerged. The current candidates are compared
individually, not represented as an already accepted combined tree.

## Independent source and API findings

1. [Drawing-settings bindings](https://github.com/c933103/AN-Paint/blob/691f8870649a1d21d1441f4e3d0e795660b23e9a/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1543-L1562)
   give the first checkbox only `document.strokeSmoothing` and the second only
   `document.antialiasing`. Both fields default independently to false. The checkbox
   callback applies the corresponding value, invalidates the canvas and schedules
   autosave; it does not turn the other option on.
2. [The freehand stroke implementation](https://github.com/c933103/AN-Paint/blob/691f8870649a1d21d1441f4e3d0e795660b23e9a/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L506-L523)
   obtains its Paint separately, then selects a quadratic curve from the previous
   smoothed point through the current sample to the next midpoint. This selection
   reads `strokeSmoothing`, not `antialiasing`. Android's [Path.quadTo
   documentation](https://developer.android.com/reference/android/graphics/Path#quadTo(float,%20float,%20float,%20float))
   independently confirms that this is a geometric quadratic Bezier operation.
3. [Paint construction](https://github.com/c933103/AN-Paint/blob/691f8870649a1d21d1441f4e3d0e795660b23e9a/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L247-L258)
   explicitly sets `isAntiAlias = tool != PaintTool.PENCIL && antialiasing`.
   It does not consult `strokeSmoothing`. Android's [Paint.setAntiAlias
   documentation](https://developer.android.com/reference/android/graphics/Paint#setAntiAlias(boolean))
   identifies antialiasing with rendered-edge smoothing, distinct from constructing
   the path geometry. It does not mean blurring/resizing the complete bitmap.
4. The earlier shorthand needs its actual exceptions: Pencil bypasses both effects;
   finishing segments and identical-point samples bypass quadratic interpolation;
   and the flat-brush path (`brushTip == 2` for Brush) takes precedence over the
   interpolation branch. The flat-brush strokes can still use antialiasing. Thus
   neither checkbox promises interpolation for every tool or every stroke segment.

For an ordinary, moving non-finishing round Brush stroke, the four combinations are:

| Stroke smoothing | Antialiasing | Source-selected operation |
| --- | --- | --- |
| Off | Off | Straight segment; antialias flag false |
| On | Off | Quadratic segment; antialias flag false |
| Off | On | Straight segment; antialias flag true |
| On | On | Quadratic segment; antialias flag true |

## Meaning of the retained labels

English: `Smooth freehand strokes` / `Smooth pixel edges (anti-aliasing)`.

Malay: `Licinkan sapuan bebas` / `Licinkan tepi piksel (antialias)`.

The model's contextual reading is that the first targets the drawn strokes and
the second targets pixel edges, with the technical antialias qualifier making the
second operation explicit. The labels therefore do not collapse or swap the two
operations. [DBP's melicinkan entry](https://prpm.dbp.gov.my/Cari1?d=175768&keyword=melicinkan)
supports the smoothing sense, and [DBP's tepi entry](https://prpm.dbp.gov.my/Cari1?d=243192&keyword=tepi)
supports the outer-edge/boundary sense. Both pages were retrieved in this recheck.
These lexical sources corroborate the distinction; they do not approve either full
application label. Search also returned DBP stroke/antialias material, but failed
full-page retrievals of those additional entries are not treated as complete primary
source inspections. No native-speaker or exhaustive-corpus requirement is invented.

Full grammatical/idiomatic adequacy of each label remains under R-003 and R-004.
Those rows are not closed by this contrastive meaning check.

## New executable checks and their limits

[recheck_r005.py](recheck_r005.py) verifies all full-source hashes, extracts the actual
binding/painting methods, checks each key's unique concrete XML value, and evaluates
the source's restricted boolean expressions across 128 combinations per snapshot:
Pencil, Brush, Watercolor and Eraser; smoothing on/off; antialiasing on/off;
flat/ordinary tip; finishing/non-finishing; identical/different points.

**640 source-expression model cases passed across five snapshots.** Four causal
negative controls were rejected: cross-wiring the checkbox, driving antialiasing
from smoothing, removing the Pencil antialias exception, and driving path geometry
from antialiasing. The normal and `python -O` results are byte-identical.

- [Exact extracted methods and results](results.json)
- [Shared 128-case branch table](branch-truth-table.json)
- [Execution output](verification.log)
- [Structured row disposition](disposition.json)

The initial probe failed because its condition-extraction regex greedily included
the `drawPoint` call after an inline condition. Only the extractor was corrected to
stop at the first closing parenthesis; production code and every expected outcome
were unchanged. The original failed outcome is retained here rather than presented
as a production failure.

These are source-contract/Python-expression checks, not execution of Kotlin or
Android Canvas. The existing `ViewportAndVerticalTextTest` source asserts Brush
antialiasing false then true, but this recheck neither reruns it nor counts a historic
CI pass as proof of the new distinction check. No Android workflow is triggered for
this evidence-only change. Pixel output, touch interactions, UI clipping, TalkBack,
full autosave recovery and cross-platform rasterization are not tested here.

## Disposition and remaining work

R-005 is complete for its individual control-meaning/source-behavior distinction.
No source repair was found necessary for that question. This is a new bounded
finding, not restoration of any rejected broad claim.

R-003, R-004, R-006, R-016, PR3-wide semantic/structural coverage and the other register
rows retain their own requirements and statuses. No companion evidence row is closed.
The canonical total becomes **475 = 3 completed structural rows + 1 completed
semantic/source distinction row + 471 pending rows**.

Track the remaining work through the [canonical register](../localization-recheck-register.md)
and [AN-W02 project kanban](https://github.com/c933103/AN-Paint/blob/docs/project-kanban-2026-10-10/docs/PROJECT_KANBAN.md).
