# Priority-cohort maintenance consolidation — 2026-10-31

Source `f74981bb4cb9be1ac69d6f448b9790e3951435c3`, tree `2b542e654d0555456d8ca18d8eeb204552b99d99`, parent actual develop `f3d617d0ec83dcab20d9fd5287272207c17c8d51`.

Exactly 41 existing files: seven Python current-row readers, 32 Kotlin locale-lifecycle wrappers, two existing shared supports. +158/-646, net 488 lines removed. No production, fixture, test identity, workflow, deadline or new-file change. Maintenance reduction only; no runtime speedup claimed.

## Preservation

`preservation.json` identifies the exact scope and 387 existing JVM test methods. All Python wrapper/import substitutions reverse to the same original AST; all Kotlin method replacements reverse to byte-identical caller files. The shared lifecycle is identical after removing only whitespace/comments. Existing locale lists, alias handling, decoders, setup/teardown, complete test bodies and diagnostics are unchanged. The 32 original classes contain 3,219 assertion/require/check callsites; the moved lifecycle assertion remains executed for every locale. No duplicate body is claimed to be a duplicate behavior requirement.

The verification script is included as a temporary audit recipe. Its input originals are obtainable from the exact parent commit; its hardcoded local paths are receipt context, not shipped project code. All historical fixture and production blobs remain byte-identical.

`remote-tree.json` records comparison of all 1,643 remote leaves, content SHAs and executable modes against the reviewed checkout. No synthetic local commit parent is used for publication.

## Verification boundaries

The focused normal-Python invocation passed all 107 existing identities in ten direct consumer modules, zero skips, exit0, 353.677s unittest / 354.639s wall. Raw output, exact identities, exit code and duration are recorded separately. No duplicate optimized/full local aggregate is run. Local Android SDK/compiler is absent; real Android/JVM compilation and existing standard CI are required on this exact source. Root independently inspected shared lifecycle/state restoration and Python call-time dependency semantics with no finding; that static review does not replace compilation.

No release, linguistic certification, installed-UI acceptance or whole-project cleanup completion is claimed. Swedish PR249 is separate and untouched.

PR: https://github.com/c933103/AN-Paint/pull/250
Exact-head review request: https://github.com/c933103/AN-Paint/pull/250#issuecomment-6543041739
Required CI: https://github.com/c933103/AN-Paint/actions/runs/41198859959 (pending when this receipt was saved).
