# Reviewed native-drag observation proposal and fixture correction

[PR41](https://github.com/c933103/AN-Paint/pull/41) · [parent PR18](https://github.com/c933103/AN-Paint/pull/18) · [board PR39](https://github.com/c933103/AN-Paint/pull/39)

The combined executable/test source tree is `e92d6da029405fcfd9751b91411d0a550299427f`,
based on tested PR41 head `7549abdcc9a65945ec18bbab6a25d54b4ce0bce8`.
Combined patch SHA-256: `bc96fd29748602ceec3a48b28714a8ff99e2f8620206f24d689d9676d3e7620a`.

Independent focused source review accepted the observation-only proposal tree
`f07a03eb38b86e7a3ecc78fed273b678d935da1b` (patch SHA-256
`64503e77767cc03d34f79598c60ecd8766c49c019edcd86e3712ef4cab854854`).
Ten focused host contracts passed independently in0.034seconds. The temporary
listener always returns false, preserves the production SeekBar change listener,
and removes itself and its scroll observer in finally. Production sources had
no touch listener to restore; this verified-null assumption is explicit.
All three accepted proposal files are byte-identical in the combined tree.

A separately reviewed two-file test-fixture correction preserves already-detected
request-budget exceptions during shutdown. Its patch SHA-256 is
`4e567cdac53320345cc75719be2bf6062eacaeeddaf7d6aa3bb0e914eed95836`.
Four deterministic regressions passed independently in0.799seconds. The same
harness against the original fixture produced the three expected missing-error
failures and retained a passing idle-shutdown case. This is test-fixture error
reporting; no production fail-open behavior was established.

The final combined source passed one complete host run:396 tests, no failures,
errors or skips,56.135seconds, exit0. Targeted suites and source/shell checks also
passed. The earlier391/392 diagnostic result is retained as a prior failure;
it is not silently replaced. `host-results.json` and `source-manifest.json`
record bounded outcomes and exact hashes without reproducing broad logs.
The source manifest preserves the frozen prepublication record.

The earlier [failed API35 evidence](https://github.com/c933103/AN-Paint/tree/69a36a16d3d5e03473607333e1fc0974fc16831a/verification/vertical-control-reachability-2026-10-10/api35-attempt-1)
remains unchanged:four portrait endpoint failures, landscape and later actions
unexecuted. New observation instrumentation does not award a pass to a failed
drag. No production, workflow, gesture, existing assertion or deadline changes are part
of this proposal. Actual compilation/event delivery/runtime evidence for the
combined source must come from its new existing CI run.

These are independent source/mock checks, not a new provider review
or a clean review claim. The three files in this directory are the only extra
publication-evidence paths beyond the exact tested combined source tree.
