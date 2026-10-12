# Independent review: current-contract migration

## Result

Source/host-contract review passes. Both final frozen full host aggregates pass, with exact current identities independently reconciled against raw logs. No unresolved source blocker remains from this review. Android compilation and native execution of the revised positive-raster policy are **UNRUN locally** and require fresh exact-source CI. This does not claim release readiness, fluency, complete locale coverage or a clean historical run.

Reviewed candidate staged tree: `592a60877524c5c118695cb45a4d0d5cd257b25a` (1,061 leaves). Its temporary local baseline has exact tree `3dcc1a82f878ad7e0e708cff25ec8d493b88bbc6`, published as `04b128889a4ff9159f199d1737bd07d41e22162d`. The public successor head/run does not yet exist at this review stage. `source-binding.json` records one-time source provenance and removals; it is deliberately not a permanent application CI gate.

Final reviewed Flow SHA256: `ddbff57e3de0dadd7fdff7d59c3d1ae374996d32125fe43d89ffdaf4e616e39a`.
Current font-validator SHA256: `676fd2d6bee52c2e260660ff07441fb113de0261fd38b09ba40af522e060343c`.

## Executed checks

- **PASS:** 114 focused host methods normally, 16.692s, exit0; the same 114 under optimized Python, 14.029s, exit0. Modules: current font, cmap coverage, font disclosure, current localization, Help providers, current installed phase union, timeout budget, translations and font-builder input preservation.
- **PASS:** separate 38-method current-font suite, 2.375s, exit0.
- **PASS, writer execution independently inspected:** frozen ordinary full aggregate, all642 methods, 214.453s (215.013s wrapper), exit0, no skips/failures, unchanged240-second cap. Raw log SHA256 `f71109321b5e7ccff47ab5fe37e0b8ddd6213e61170ab9565fe58e34019c621b`. The optimized full aggregate also passes all642, 212.766s (214.158s wrapper), exit0, no skips/failures, unchanged240-second cap; raw log SHA256 `3942cab3ac18f97ddb603c5ae963b66474a304b09a9dba71bb3895e8d02cd263`. Independent current unittest discovery and raw verbose-status parsing reconcile exactly642 started/passed identities in both modes, including the warning-wrapped standalone `ok`. Deliberate failure JSON from negative controls does not alter those results.
- **PASS:** independent in-memory reproductions now reject all four original font/licence gaps: zero-length format4, nonexistent supplementary glyph with valid checksums/matching inventory, unrelated nonempty source notices, and consistently deleted OFL permissions/conditions. The unmodified asset passes.
- **PASS:** one-time parsed-data audit: 557 metadata/Copy-credit/SVG/Hungarian/Help values and 120 import messages remain the existing values. No language review was repeated. Defaults, exact scope, script controls and the 81 open fallbacks remain explicit.
- **PASS:** production, resources, fonts, build/workflow files and installed Android test sources are unchanged. The only Android/Kotlin source change is the JVM Flow test's explicit policy/diagnostic/control change. The retained font metadata and active release request/signing/notes inputs are byte-identical.
- **PASS:** final source/index consistency and `git diff --check`. The rename-aware diff records 13 additions, 16 modifications, one import-fixture move and 1,075 deletions. With rename detection disabled, this is 14 additions, 16 modifications and 1,076 deletions (1,106 path operations), including the moved fixture’s old path. Of these, 29 current non-verification inputs and the new verification index are added/modified. Historical file deletion is intentional and recoverable through the immutable baseline archive, rather than a future reconstruction duty.
- **UNRUN locally:** Kotlin compilation, changed native controls, new PNG/JSON outputs, APK build, installed execution and public successor-tree readback. The writer owns publication and exact remote-tree verification.

## Review findings and repairs

The initial draft had six meaningful gaps; all were reported before freeze and repaired:

1. Cmap coverage accepted a supplementary mapping to glyph65535 in a 740-glyph font. Every decoded glyph ID is now bounded by maxp, including non-fixture characters; glyph0 establishes no coverage.
2. Format4 declared length zero could read outside its subtable. Formats4/12 now validate headers, lengths, counts, segment/group ordering, Unicode scalar ranges, offsets and glyph endpoints before expansion. Retained coverage uses the same validated decoder. The OpenType [cmap](https://learn.microsoft.com/en-us/typography/opentype/spec/cmap) and [maxp](https://learn.microsoft.com/en-us/typography/opentype/spec/maxp) specifications support these bounds.
3. Nonempty but unrelated notices and consistently removed OFL terms could pass. Complete normalized canonical MIT/OFL paragraphs now form genuine licence inputs, with attribution and notice/aggregate checks. Mutations remove individual paragraphs and whole permission/condition blocks across all copies; whitespace reformatting remains allowed.
4. Removing HTTP/SVG contract families could leave a vacuous wording suite. Explicit expected families/keys, nonempty locale values and constraints now have deletion controls. Ordinary unrelated XML formatting/content edits remain allowed.
5. Phase coverage still froze old method totals. Tests now derive the SDK-eligible disjoint union from current source, keep explicit exclusions and operational deadlines, and admit a new ordinary method without historical-count editing.
6. Whole-glyph/mark mutations did not independently exercise opaque-loss rejection. A native one-sample clip now leaves its component present and triggers the separate opaque-loss guard. Existing edge-clipping controls additionally require changed actual pixels and newly missing ink beyond any intact difference.

`EARLY-FINDINGS.md`, initial input copies and reproduction receipts preserve the review sequence. `post-fix-stale-repro-partial.log` is explicitly a partial old probe run after repair: it already prints two correct rejections, then its obsolete expectation that coverage would return a set caused an exception. It is not a product regression. `font-gap-recheck.json` is the successful current independent reproduction.

## Meaningful coverage retained

Current parsed wording, syntax, placeholders, legal identifiers, Unicode controls, fallback scope, Hungarian label references, Help provider/caption boundaries and TIFF literal expectations remain. The compact import fixture preserves its prior assertions. Current resource/flow tests still exercise typed metadata errors, both user routes, provider details, thresholds, lifecycle and actual locale resolution. Production behavior, fonts and network timing did not change.

The migration removes recursive inverse adapters, full-source/XML endpoint pins, old-run inventory pins and tests demanding archived failed report files. The known04 strict-delegation defect is retired with its obsolete inverse layer; this is not another recursive adapter repair. Generic malformed transport, protocol, duplicate screenshot, source-bound per-run evidence and phase-completeness controls remain. Per-run source/APK authentication and pinned upstream font/licence provenance remain legitimate requirements; they are different from freezing ordinary source edits forever.

The one-time host identity map records 590 retained, 129 retired and 52 added identities (719→642). Independent AST comparison confirms the exact retired/added lists; direct AST totals omit 72 additional unittest-collected identities on both sides and are not presented as full discovery. The map is migration accounting, not a required future inventory. Retired Python source-fragment assertions do not imply removal of the corresponding real JVM/installed tests; those sources are preserved except for the reviewed Flow policy change.

## Raster policy assessment

The revised positive-frame policy matches the approved readable-content requirement. It preserves independent complete-layout reference allocation, every alpha>0/ARGB diagnostic, full text/accessibility/line/scroll/lifecycle checks and the existing strict mutation oracle. No font, translation, production geometry or numeric tolerance was changed.

Hard raster checks reject an empty/unsafe reference, allocation-edge contact, a wholly missing eight-connected ink component, or a completely missing opaque reference sample. Components are expressly not glyph segmentation. Partial marks/strokes, colour changes and shifted ink may still require materiality review even if those hard checks pass. Every nonzero exact comparison remains visible and marked review-required; a passing JUnit method alone does not dispose of it.

The separate native `A`/combining-acute controls remove actual draw regions through `Canvas.clipOutRect`, leaving the complete independent reference untouched. Whole-glyph, detached-mark and opaque-sample cases have defect-specific rejection checks at both scales. The original strict 72 mutations remain, strengthened against vacuous success when a baseline has a diagnostic fringe. Their compilation/execution remains a fresh-CI gate.

Current planned output is 189 ink triplets and 78 intentional rejected mutations, with four summaries, while original 112 UI pairs and 28 normal-landscape diagnostics remain. These are current-plan observations, not permanent source-count pins. See `CI-ACCEPTANCE.md` for exact audit steps.

The installed helper/decoder still has a separate zero-difference rule. Documentation now says so explicitly. Both installed Arabic routes passed on the prior04 source; that historical result is not a new migration run. A future fringe in an installed record requires severity review before adding production workarounds.

## Historical result remains unchanged

The frozen04 review is separately archived at commit `8a7dd2b59b491e8fc401072a9d8dd0d93f6aee17`, path `verification/commons-metadata-m04-natural-relayout-ci-2026-10-12`. Its exact manifest is SHA256 `7b17186e5f0f89869c676a229e50636bc958de4e5473ae46658387634a4aef8c`.

That run remains 891/892 JVM passed with the mixed-Arabic reset's strict guard failed, 155/181 ink frames and 60/72 completed mutations. Its two alpha7/alpha1 fringe losses were individually reviewed, with no demonstrated glyph/mark/line disappearance. Both installed suites passed, including the natural-update and complete Arabic raster checks. This migration neither rewrites that failure nor turns its missing controls into passes. A new run needs its own complete evidence and dispositions.
