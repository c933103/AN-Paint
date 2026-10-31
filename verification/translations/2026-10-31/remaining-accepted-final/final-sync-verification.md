# Final synchronized candidate: verification in progress

PR247 final head 3ae863e4f5b8ce5b7d22214b2037d8fc1e7560be, tree ed35501ba4428259614234fa91e505e804607891, actual develop parent c120c378ee1edc54193b6358b8a1cc5d59d05559. Exactly 737 additions and two existing replacements. This supersedes temporary-parent readiness assumptions, not immutable historical acceptance receipts.

Provisional run https://github.com/c933103/AN-Paint/actions/runs/41179275329 on b1348dc completed: five non-regression jobs and lint passed. Python ran 2081 tests: five failures, two skips. JVM ran 1960: one failure. Regression artifact 13034958827 was downloaded; SHA256 94d7748dcdf4cc31e13b033779f10640507637511a7ba8cdf8946065f47991de matched GitHub. Its included all-739 compiled test XML passes with zero skips. This does not validate subsequent helper changes.

Diagnosed failures preserved, not erased:
- test_memory_warning_successors historical absent-value guard compared None to accepted ang decoder/non assembly/shn decoder warnings. Exactly those three pairs join the qualified-successor branch, retaining old None, English source, exact target and forged-predecessor rejection. Frozen historical fixtures unchanged.
- test_swedish_extended_wording historical held_missing included palette. Retain old fixture; require exact accepted successor and subtract only its identity from current missing set. Main remains held.
- test_tajik_option_jvm_successor asserted Yucatec Brush absent. Exact Brush and Save successors now bind; all other fallback keys remain checked.
- BretonAsturianOccitanPriorityWordingTest expected old English palette fallback, got exact accepted Breton. Test retains frozen historical null hold and explicit default/US distinction; checks exact later successor instead. No resource values changed.
- Independent schema hardening requires exact integer1 before caching, including negative bool/float/string/container/null/missing controls. Exact-byte reread, content invalidation, loader mocking and mutation isolation remain checked.

Final focused checks: memory/schema22 and Swedish/Tajik11 pass normal and optimized. Full final suites started 08:03 UTC, with isolated temporary paths and frozen-source manifest. Fresh hosted run https://github.com/c933103/AN-Paint/actions/runs/41182876027 and exact-head Codex request https://github.com/c933103/AN-Paint/pull/247#issuecomment-6540913924 pending. Not ready to merge; no release.

Earlier post-memory diagnostic ran776 tests and found the same Swedish/Yucatec stale guards. Modules were imported before their fixes; this diagnostic is not final evidence. Only newly started full frozen suites count for final validation.

