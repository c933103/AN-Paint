# Reviewed vertical reachability proposal: durable source/mock evidence

This archive preserves the first unpublished proposal, both independent-review
findings, the corrected exact-source proposal, and actual host-test output.
It is an evidence-only addition to reviewed tree
`186de374ffce6dabd549a5b7982b5344f9724fec`; it changes no reviewed source bytes.

- Parent: [PR18](https://github.com/c933103/AN-Paint/pull/18), exact code head
  `66c39ca345ef7bc8c5fe1da8ce64cb872c3a0e88`.
- Distinct [unresolved reachability checklist](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6093775811).
- [Project board PR39](https://github.com/c933103/AN-Paint/pull/39) and
  [live project board](https://github.com/c933103/AN-Paint/blob/docs/project-kanban-2026-10-10/docs/PROJECT_KANBAN.md).
- [Accepted earlier capture-state evidence](https://github.com/c933103/AN-Paint/tree/5f16192207161dd828bf9f37becb7eda9f205365/verification/installed-vertical-matrix-2026-10-10/repair-api35-66c39ca)
  is preserved separately and is not retroactively revalidated.

The first patch/tree remain retained as a superseded, unexecuted proposal. Its
source/mock tests did not catch an equal-value Cancel precondition and undefined
false-visibility rectangle handling. Revision 2 corrects both, as documented in
`review-report.md` and `revision-2-fixes.patch`.

Revision 2 passed 389 local host tests in 55.218 seconds and 389 independent host
tests in 55.167 seconds, with zero skips. Its 28 targeted host checks, shell syntax
and diff checks passed. These are source/mock checks only. Host geometry fixture
contracts do not execute Android/Kotlin. The local compile attempt was blocked
before compilation by an unavailable Gradle distribution and network failure.

Android compilation, installed fake-View negatives, real native controls and the
unchanged 180-second phase budget remain unverified at this publication. Existing
API35 CI will report separately against the exact published source/evidence tree.
No broad usability, linguistic, all-glyph, API30, physical-device or merge/release
acceptance follows from this review. Independent source review is not a fresh
Codex review result; the known quota limitation was not retried.

Every retained file is hashed in `files.json`. No signing keys, credentials,
private cross-project findings or expiring artifact-download URLs are included.
