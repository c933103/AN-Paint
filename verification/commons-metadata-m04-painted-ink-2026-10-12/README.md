# M04 horizontal painted-ink oracle successor

## Evidence for the change

The [immutable diagnostic checkpoint](https://github.com/c933103/AN-Paint/tree/746d41107b8251d2b288a62931da5c1e80810b08/verification/commons-metadata-m04-pr55-diagnostic-ci-2026-10-12)
retains run `38244193872`, public diagnostic head
`dc46abc2add7984358565a88fe65c5278212dcf6`, source tree
`4ff7f479ffc73964fa8756b6c7e3202f624ad0f1`, and synthetic merge
`56e7891852a2da201bf10ad99c486e659da2e6c5`.

All 890 JVM identities executed: 889 passed and the original short-landscape
horizontal advance proxy failed for Ainu Kana COPY at 640×320 dp, font scale 1.
The first line's right advance is 1233.043 pixels for a 1232-pixel layout. The
old width-plus-one condition therefore fails. Independently recomputed native
pixels occupy x=3 through x=1231 inclusive, with zero painted pixels outside the
layout and no expanded-canvas edge contact. The actual root crop agrees with
the complete text raster composited onto its background within one color level;
that forensic compositing difference is **not** a new acceptance tolerance.
Raw PNG/JSON/XML and the independent comparison are copied unchanged under
`historical-diagnostic/`, with source and file hashes in
`historical-failure-binding.json`. The original failed guard and both failed
source checkpoints remain recoverable byte-for-byte through their frozen history.

This evidence supports replacing an advance-based proxy for visible clipping.
It does not establish a production text-layout, font or translation defect.

## Two distinct failed checkpoints remain explicit

1. Original PR55 run [38239121942](https://github.com/c933103/AN-Paint/actions/runs/38239121942),
   head `b95c9a682c77f5dfa9b9a1f4eacabd9d9a03265a`, tree
   `d80218496e45bbefcaa378d40e5cd9846b7988ee`, synthetic merge
   `14b1fdf8e02ebe6f765d63906f05c7e808524b76`: 890 executed, one failed,
   85 of 112 successful capture pairs. Failure occurred before its pixels and
   metrics could be retained. Its original XML and receipt remain in the
   unchanged prior diagnostic evidence directory.
2. Diagnostic successor run [38244193872](https://github.com/c933103/AN-Paint/actions/runs/38244193872),
   head `dc46abc2add7984358565a88fe65c5278212dcf6`, tree
   `4ff7f479ffc73964fa8756b6c7e3202f624ad0f1`: the same 890 identities and
   failed Ainu advance proxy, with 111 successful pairs and all 28 diagnostic
   profiles. This is the measured native-ink evidence supporting the new oracle.

Neither failed checkpoint is relabeled as a pass. Their unchanged 890-identity
inventories remain historical; the new successor has its own 892-identity gate.

## Exact acceptance scope

Only M04's **short-landscape horizontal** line-width assertion is replaced.
Portrait uses its unchanged original fixture. Vertical languages keep their
original completeness, column reachability and reading-start checks. The two
vertical emoji diagnostics have a single nonzero-alpha pixel outside logical
layout width and were never covered by the old horizontal guard; this successor
does not reinterpret those routes or silently apply horizontal policy to them.

Production code, all wording and fonts, accessibility/full-message checks,
ellipses, measured height, scroll/parent reachability, complete locale coverage,
workflow behavior and timeouts remain unchanged. The original advance values
and width-plus-one result remain recorded as diagnostics.

## Strict full-reference oracle

The helper is restricted, with fail-closed assertions, to the existing plain
API35 horizontal status view. It rejects unsupported spans, nonnormal alignment,
shifted-overhang mode, background/foreground/compound drawables, transformations,
selection, self-scroll, non-TOP gravity, shadows and paint effects/decorations.
It does not alter the view or paint to satisfy these preconditions.

The actual `TextView` first draws to its own transparent native bitmap, retaining
its native clipping. A separate native `Layout` draw provides the complete
reference. Text identity, contiguous UTF-16 line ranges and no ellipses are
asserted. The origin comes from compound left padding and the view baseline
minus the first layout baseline, with the TOP origin explicitly checked.

Reference allocation uses a **copy** of API35 actual glyph bounds, unioned with
all line extents and the full layout rectangle, rounded outward. Copying matters:
`BoringLayout` may return cached bounds. A two-pixel allocation border does not
relax acceptance. Nonfinite or oversized allocations fail, as does any nonzero
pixel touching the allocation edge. Geometry-based allocation also covers glyphs
wholly beyond the old fixed diagnostic margin.

Every nonzero-alpha reference pixel is scanned, including marks outside nominal
line boxes. No horizontal overflow pixel is accepted. Full-reference ink outside
the actual view fails. The entire actual-view ARGB bitmap must equal the mapped
complete reference exactly: no alpha threshold, color/position tolerance, ignored
border, or comparison restricted to an already-clipped crop. The original parent
visibility and scroll assertions remain additional requirements.

API evidence: [`Layout.computeDrawingBoundingBox()`](https://developer.android.com/reference/android/text/Layout#computeDrawingBoundingBox())
is available from API35 and measures actual glyph geometry rather than relying on
line metrics. The [Android 35 source](https://android.googlesource.com/platform/prebuilts/fullsdk/sources/+/refs/heads/androidx-constraintlayout-release/android-35/android/text/Layout.java)
shows its per-line glyph-bound calculation. The repository's unchanged compile
SDK is 35 and this test class already runs only SDK35. New Kotlin compilation
and runtime behavior still require the successor's hosted build.

## Native negative controls

Two explicit new JVM methods cover font scales 1 and 2. Each tests English Latin,
combining Ainu Kana, Tibetan, Arabic RTL, Japanese Han/Kana and the bundled Nôm
font through a real local-fixture Commons COPY action. Every intact view must
pass first. Six real native draw mutations then must be rejected:

- Shift painted text across the left boundary
- Shift it across the right boundary
- Shift it wholly left of the view
- Shift it wholly right of the view
- Clip the first spatially painted edge-glyph column
- Clip the last spatially painted edge-glyph column

Clipping changes only the actual native Canvas; its complete reference must
remain byte-identical to the intact reference. Translation must retain every
reference ink pixel, including wholly off-view glyphs. Controls assert nonzero
lost/overflowing ink and the **specific** intended rejection, so an unrelated
precondition failure cannot pass a negative test. Logical RTL direction is
recorded rather than equated with a spatial edge. Native bounds, view/layout/line
geometry, key paint properties, text and accessibility remain unchanged after
each mutant.

Expected evidence includes 12 intact control profiles and 72 rejected native
mutations, split across the two font-scale receipts. Together with 36 live
horizontal landscape frames, this is 120 PNG pairs/JSON records plus two control
summaries. Current outcome metadata explicitly marks the old advance booleans
as diagnostic only; a painted-ink pass never claims that the old proxy passed. The fresh JVM inventory is
892 identities: all previous 890 plus exactly these two methods. Old inventories
are not rewritten. Native positive and negative evidence remains unrun locally;
source contracts alone are not proof that these controls executed.

## Provenance, validation and next gate

The new SHA-256-pinned successor fixture enumerates exactly three changed files:
the flow test and two historical diagnostic adapters. Historical projections
restore the diagnostic and pre-diagnostic source endpoints exactly. The new live
source checks reject removed, old-restored, corrupted, duplicated or unrelated
successor content. All historical fixtures and evidence remain unchanged.

Host checks and their exact source hashes are recorded in
`local-verification.json`. Fresh hosted compilation must prove the API calls
compile, real views meet every fail-closed precondition, intact native canvases
match exactly, and all 72 draw mutations trigger their intended failures. Inspect
all 892 JUnit identities and new native evidence before accepting the repair.
No hosted result from an earlier source is substituted for that gate.
