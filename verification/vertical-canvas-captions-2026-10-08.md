# Vertical canvas caption propagation

Base: [`develop` at 46b9e93ece6b2730733fabf0db5009de846ee322](https://github.com/c933103/AN-Paint/commit/46b9e93ece6b2730733fabf0db5009de846ee322), whose tree exactly matches accepted PR #22.

## Bounded finding and applicability

The [first cross-language engineering inventory](cross-language-engineering-propagation-2026-10-08.md) identified two canvas captions that received the bundled UI font but still called horizontal `Canvas.drawText` in a vertical UI:

- `AssemblyCanvas`: the empty-workspace instruction.
- `PaintCanvas`: the selection rotation caption.

This change propagates the existing shared shaping/layout renderer into those two surfaces. It applies to every current vertical picker profile: `mn-Mong`, `mnc-Mong`, `lzh-Hant`, `en-XV`, and `qaa-Zsye-XV`. The predicate is script/direction based, not a five-tag whitelist, so other Mong-script locales follow the same established direction policy. The other 135 picker tags retain the existing horizontal path, including horizontal RTL languages, Cyrillic Mongolian, Nôm and Wu.

No text is translated or introduced. Existing resource keys, catalogue conventions, glyph clusters, font assets, licensing, UI/drawing-font roles and explicit font selections remain unchanged. This is not completion of vertical assembly UI, all-language localization acceptance, or linguistic validation.

## Implementation boundaries

[`VerticalCanvasCaption`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalCanvasCaption.kt) copies the supplied UI paint, normalizes only the copy's alignment to LEFT, wraps through `VerticalText.wrapLabel`, measures the returned text, and draws it through `VerticalText.draw` with MIXED orientation. The original paint is not changed. This avoids passing AssemblyCanvas's CENTER-aligned horizontal paint into the top-left vertical layout contract.

The assembly instruction keeps its existing `16*density` text size. Vertical text is wrapped against viewport height with a 16dp inset and its measured box is centered before the canvas's document pan/zoom transform. Horizontal drawing keeps the original baseline, paint and `drawText` call.

The rotation caption keeps its existing `11*scaledDensity` screen size and UI typeface. For vertical text, measurement occurs in **viewport pixels**. Inside the existing image-coordinate canvas, a saved translation to the grip and reciprocal scale establish a local screen-pixel frame only for the caption. A zoom of `1e-9` therefore does not create enormous inverse-zoom `StaticLayout` font metrics. The canvas transform is restored before other handles are drawn.

Placement uses the existing ruler/scrollbar viewport, with a 4dp caption inset and 10dp grip gap. Vertical-LR prefers the right side and vertical-RL the left side, placing the first reading column nearest the grip when that side fits. The opposite side is tried before a containment clamp. The grip is never moved to accommodate the label. `rotationHandle` and `hitSelection` are byte-identical to the base.

## Overflow and coverage limits

A wrapping height is a target, not a guaranteed bound: joined Mongolian/Manchu words are preserved. The actual wrapped box is measured. A box too large for the viewport keeps its text, shaping and existing viewport clipping; it is centered rather than split into arbitrary clusters, silently truncated or shrunk to tiny text. Narrow-view containment can overlap a grip. Extreme-size/ink-overhang visual design is not declared solved.

The existing horizontal/RTL drawing calls are retained. No selection geometry, interaction radius, rotation/resize behavior, document pixels, history, save state or assembly placement behavior is changed. Framework tooltip typography, modern vertical feedback and the surrounding AssemblyActivity control rows remain separate open gaps. PRs #19 and #20 are not incorporated or duplicated.

## Regression evidence

- All **302 local host tests passed** with no failures/errors/skips. Four new source guards cover propagation, horizontal call preservation, pixel-scale font measurement and side placement. Source guards are not visual runtime evidence.
- Six locally executed isolated native helper cases passed: three test methods on each of API30/API35. They use the new helper, the unchanged shared vertical renderer and real Robolectric native Canvas. Cases cover copied alignment and renderer pixel equivalence, canvas restoration, edge/tiny viewport placement, and identical screen-size output from `1e-9` through `32` zoom. These do not exercise application resource linking or actual app Views.
- Three isolated native mutation controls are rejected: restoring the source paint's CENTER alignment, reversing the preferred side, and omitting canvas restoration. Two source mutation controls reject the original horizontal-only call sites and inverse-zoom vertical font metrics.
- The three production files and both new test files receive an isolated Kotlin type-consistency check against cached base/framework dependencies. Full resource linking, the full Android build and lint are separate CI outcomes. Existing `scaledDensity`/framework deprecation warnings are not silently called warning-free compilation.

[`VerticalCanvasCaptionTest`](../Paintroid/src/test/java/org/catrobat/paintroid/local/VerticalCanvasCaptionTest.kt) adds six API35 native View tests. It updates both `AppLanguage` and `PaintApplication.currentResources`, then restores the prior state. Independent references use the shared renderer without calling the new caption helper:

1. All five vertical assembly captions in portrait and shallow landscape; compare actual pixels and reject the old horizontal rendering, including viewport independence from pan/zoom.
2. Unchanged horizontal pixels for `en-001`, `ar`, `vi-Hani`, and `wuu-Hans`, in both caption surfaces.
3. Assembly empty, unplaced, selected, placed and cleared states.
4. Every vertical rotation profile at Fit, while preserving document and selection state.
5. Both vertical directions at center/left/right/top/bottom viewport scenes with different zoom/grid states.
6. A controlled `1e-9` viewport-scale fixture on a real 4×4 document, without allocating an enormous source bitmap. It checks the numerical rendering path, not ordinary UI reachability or huge-document handling.

Tests preserve nonempty undo/redo stacks, source/selection pixels, grip/clamping formulas and handle-hit identities. Actual/expected failure PNGs and representative successful native-render samples are written to the normal CI preview artifact directory. The six helper executions are separate from these six resource-linked View methods.

Exact-head build, full test, lint, emulator and Codex outcomes are recorded in the pull request. A successful helper probe or source check must not be presented as successful full View execution, physical-device smoothness, accessibility acceptance, or universal glyph/linguistic validation.
