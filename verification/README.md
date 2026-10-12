# Verification records

Routine CI tests current behavior and compact product fixtures. Historical raw
logs, captures, source snapshots, inverse adapters and one-time preservation
checks live outside the active application tree.

## Immutable archive

The complete pre-migration checkout, including every removed verification file,
is preserved at commit
[04b128889a4ff9159f199d1737bd07d41e22162d](https://github.com/c933103/AN-Paint/tree/04b128889a4ff9159f199d1737bd07d41e22162d),
reachable through `archive/pr55-before-evidence-migration-20261012`.
The [old handoff](https://github.com/c933103/AN-Paint/blob/04b128889a4ff9159f199d1737bd07d41e22162d/HANDOFF.md)
and [old CI history](https://github.com/c933103/AN-Paint/blob/04b128889a4ff9159f199d1737bd07d41e22162d/CI.md)
retain their original claims and limits; archiving them grants no new acceptance.

Distinct PR55 failure checkpoints:
- [Original advance-guard failure](https://github.com/c933103/AN-Paint/tree/946e5378cf3f75a8047dc42a46a3b3dbe62c9327/verification/commons-metadata-m04-pr55-initial-ci-2026-10-12).
- [Ainu diagnostic advance/painted-ink mismatch](https://github.com/c933103/AN-Paint/tree/746d41107b8251d2b288a62931da5c1e80810b08/verification/commons-metadata-m04-pr55-diagnostic-ci-2026-10-12).
- [Arabic strict-ink failure](https://github.com/c933103/AN-Paint/tree/04b128889a4ff9159f199d1737bd07d41e22162d/verification/commons-metadata-m04-glyph-bounds-2026-10-12/failed-painted-ink-run).
- [Compiler failure and installed same-height failure](https://github.com/c933103/AN-Paint/tree/94b91c4eb04d856853e29bdf7c90c61d52405bff/verification/commons-metadata-m04-glyph-bounds-ci-2026-10-12).
- [Natural-relayout authoring review](https://github.com/c933103/AN-Paint/tree/82bd9bc0e8e4c7a47784fa157a22e2bd9b52c72c/verification/commons-metadata-m04-status-remeasure-2026-10-12).

[Full immutable04 CI review, raw receipts and pixel disposition](https://github.com/c933103/AN-Paint/tree/8a7dd2b59b491e8fc401072a9d8dd0d93f6aee17/verification/commons-metadata-m04-natural-relayout-ci-2026-10-12).

The subsequent [04 source run](https://github.com/c933103/AN-Paint/actions/runs/38269993000)
executed 892 JVM identities: 891 passed; the mixed-paragraph Arabic reset failed
its exact-alpha guard. All 112 original render pairs passed. Its 155/181 ink
triplets and 60/72 mutation controls are incomplete, not a complete pass. The
reviewed difference consists of two antialias fringe samples (alpha 7 and 1),
with no demonstrated glyph, mark or line loss; this is a specific disposition,
not a universal pixel tolerance. API30's 95 and API35's 104 scheduled installed
methods passed, including both Arabic natural-update/full-raster checks.

## Language-option evidence

The accepted language-option records remain reachable at immutable develop
[484d1b31](https://github.com/c933103/AN-Paint/tree/484d1b31cb113c88351e6d0dbdaa0d503e5dd834):
- [Six-option registration and review](https://github.com/c933103/AN-Paint/tree/484d1b31cb113c88351e6d0dbdaa0d503e5dd834/verification/language-options-2026-10-12).
- [Twenty-one concrete identities and principal-variety decision](https://github.com/c933103/AN-Paint/tree/484d1b31cb113c88351e6d0dbdaa0d503e5dd834/verification/language-options-second-2026-10-12).
- [Superseded unpublished 162-choice candidate](https://github.com/c933103/AN-Paint/tree/484d1b31cb113c88351e6d0dbdaa0d503e5dd834/verification/language-options-superseded-162-2026-10-12).
These records do not certify translated UI or current runtime behavior. The
compact identity/status fixtures and explicit 59-scoped/108-fallback contract
remain active; routine CI does not require the historical files.

## Files intentionally retained here

- `legacy-font-metadata.json`: licensing/provenance input cited by the packaged
  asset notices and font licence review.
- `releases/request.json` and its selected version's signing patch/notes:
  operational inputs to the separately authorized release publisher. The patch
  contains public signatures and copy ranges, never the private signing key.

New raw evidence belongs in CI artifacts or a dedicated evidence ref, with a
short exact-source summary linked from the relevant PR. Normal CI must not
fetch or reconstruct the historical archive.
