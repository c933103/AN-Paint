# PR114 concurrent-head reconciliation

Source head: `511f9607c7889a5acd2e6f79dc96e484cb37bf5a`, a direct child of
`e434c5e779183a017ca9153e688dc77a79a0fc39`. Source tree:
`2c1b18bdf7ef64e828e56b60a7cd96b4bb7f85e5`. The hosted synthetic merge
`cad21eca7f8146d159b0a93d4c7fdf1fc75e2632` has that identical tree.
All 1,182 source blobs and executable modes were independently compared.

This receipt records read-only reconciliation of the concurrent change. Earlier
e434 evidence remains historical and immutable. No source/ref change was made
by this reconciliation; proposed follow-up corrections are not part of 511.

## Exact-head outcomes

[Hosted run 39017556055](https://github.com/c933103/AN-Paint/actions/runs/39017556055)
passed APK/corresponding-source build, clean/incremental resource generation,
both API35 device groups and their aggregate. Python contracts, native preparation
and Android lint also passed. Exact-head Codex code review found no major issues;
the security receipt remains stale at `db076197`.

The regression job failed its unchanged 12-minute JVM-step deadline. Its artifact
contains 110 suites and 1,099 cases with zero failures, errors or skips. The phase
completed successfully after 720.907 seconds, but this does not turn the failed
workflow deadline into a pass. The actual Test task took 9m32.14s; compilation,
resource preparation and Gradle setup consumed the remaining roughly 149 seconds.
The prior e434 overrun similarly conflated preparation with test execution.
Both failed outcomes are retained. A separately bounded preparation phase is
being reviewed while preserving the 12-minute full-test step and 22-minute job cap.

The artifact includes 25 LocaleTextBoundary cases, 11 formatter cases, 4 prefix
cases and 4 native SDK33 caption-safety cases, all passed. Native/installed checks
do not establish every device, font, OS or caller-memory limit. In particular,
the new caption test did not execute the API21–27 Paint comparison branch.

## Independent compatibility checks

- 12 generator/boundary-policy tests and 15 pure formatter/prefix tests passed.
- 48,421 current XML rows plus 23,632 nullable comparisons: zero mismatches/errors.
- 50,550 AAPT-decoded rows across 145 configurations plus 24,820 nullable comparisons:
 zero mismatches/errors. All 205 aliases resolved without a missing exact-config target.
- The sole resource edit is Japanese `ui_trim_in_percent`, restoring the displayed
 percent symbol with the valid `%%` template encoding. The 18 Ainu/Manchu values
 remain unchanged. Source English and other locale catalogues remain unchanged.
- Independent caption review found no concrete regression: 6,000 seeded Unicode
 cluster/run comparisons, four long reconstruction controls and 37,500 modeled
 wrapping comparisons passed. The model is explicitly not native shaping proof.

A qualified source-discovery defect was
[reported with a reproducer](https://github.com/c933103/AN-Paint/pull/114#issuecomment-6231852162):
an explicit generated source root beneath a nonconventional build directory was
silently pruned. Current configured production paths are covered. The proposed
two-file repair has separate local review/tests and is not yet applied to 511.

## Retained evidence

`review-511-evidence.zip` contains actual stdout/stderr, source identities,
commands, independent helper/model sources, catalogue summaries, selected hosted
JUnit XML, phase logs and Gradle profiles. `review-511-evidence-manifest.json`
records each member hash and the archive hash. The full hosted archive is
artifact 12094924734, SHA256
`91d573a069d0a5d563830e9611cf67e471c1b00158bbe1c38d2a0cda0fb7d773`.
Large captures and dependency binaries are not duplicated here.

This is bounded runtime/resource compatibility evidence, not linguistic
certification or a universal crash-proof guarantee. XML/build rejection and
remaining platform/native/device limits remain separate.
