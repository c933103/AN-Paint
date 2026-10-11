# Exact localized-dialog / C05 / M02 composition

This candidate composes three independently accepted increments over settled
develop `691f8870649a1d21d1441f4e3d0e795660b23e9a`. Standalone successes do not
establish composed-source acceptance. The producer branches remain unchanged;
this work does not authorize a merge, release, or ready-for-review transition.

## Pinned inputs and precise scope

- Shared dialog PR49: `d7f1a95835704d2b263866895babaffa9a16b49e`, tree
  `32957329aef7dc966d4a138c24c1a9292deb1de5` (1,589 leaves).
- Hungarian C05 PR48: `826eeaa9f4c2960eca3958ae63d673e4d87fe05a`, tree
  `f0b4b757e265ec5b176d9b7431533ae74080deaa` (1,586 leaves).
- Metadata M02 PR47: `a8074c5c4f3b76767f479c6716d823e61ab06aed`, tree
  `b93546e32cf5ae300eaf09ee64813606f22fd4a0` (1,525 leaves).

The live remote input trees were compared by every path, mode and Git blob hash
with the available producer snapshots before composition. All matched exactly.
The first two snapshots derive from current develop; M02 derives from the earlier
release source. Only M02's 87-path increment is imported, preserving current
develop's later release-publisher changes. No producer checkout is edited.

The exact producer union changes 251 paths from current develop: 66 production
paths (six Kotlin files and 60 catalogues), 12 JVM/installed test source paths,
26 host-tool/fixture/CI/documentation paths, and 147 inherited evidence paths.
The final diff also contains the new composition contract, its pinned fixture,
and the evidence in this directory. No production logic beyond the accepted
producer union is added.

Only two producer paths overlap: `values-hu/strings.xml` and the historical
`tools/test_commons_copy_credit_errors.py` guard. The Hungarian merge consists
of exactly the original C05 17 replacements and M02's one new
`commons_metadata_http_error` entry. The guard preserves all three narrow
reversals. The existing C05 and M02 host endpoint tests each additionally apply
the other producer's unchanged strict reversal before checking their original
whole-file endpoint. Neither historical fixture is replaced or expanded.

The C05 fixture remains SHA256
`2dc109760b76f0c6b32c56a14d2bcb95c7cafa3b897b74dc514b43e51ac02ee8`.
The M02 resource fixture remains SHA256
`a2358aca0d192313bc554269f2f2a03fc0dc07267f4e5f735920a01a86b5249a`.
The composed Hungarian catalogue is SHA256
`5be4b70114f805ca95e150da47446631455c6257775f0856a8265d5d338a6f24`.

## Reversible composition and inherited gates

`tools/test_localized_dialog_composition.py` proves that C05 and M02 resource
reversals commute across all 60 M02 catalogues and recover each original pinned
pre-M02 hash. The Hungarian path also restores both C05 whole-file endpoints.
The About and M02 producer source reversals commute and recover the historical
C04 semantic-file hashes. The original C04 whole-file guard still rejects
unrelated resource changes, missing/duplicated/corrupted M02 lines, and every
existing C05/F01/C023 negative control. C03, format, source and legal-text
endpoints remain authoritative.

The new pinned union fixture binds all 247 nonconflicting inherited changed paths
and all 116 Kotlin JVM/installed test source files to their original producer
bytes. Thus every inherited method, assertion, case/profile, interaction and
evidence export is retained. The exact SDK-aware app partition is unchanged:
API35 has 16 ordinary + 3 gallery + 5 dialog + 4 vertical + seed + verify = 30
app methods, plus 74 native methods; API30 completes 15 + 3 + 4 = 22 app methods
and 73 native methods, with six explicit SDK suppressions and two separate
restart exclusions. Exclusions are not passes.

All five dialog cases retain 45-second interaction limits, the dialog phase
retains 300 seconds, ordinary retains 180 seconds, and the execution/job caps
remain 43/53 minutes. The accepted PR49 workflow, runner, partition verifier,
timeout-budget contract and documentation are byte-identical here. This is a
configured cancellation model, not a universal liveness proof.

PR51 Advanced Colour remains separate. PR49's explicit baseline-limitation
diagnostic is retained byte-for-byte and makes no positive usability claim.

## Local checks and retained failed attempts

- `initial-guard-conflict.json`: lossless original merge-conflict content/hash in the C04 semantic
  guard, resolved by preserving both producers' strict reversals.
- `initial-focused-host.log`: original two expected whole-file endpoint failures
  before composition reversals, plus two misspelled test-module invocation
  errors. No failed result is relabeled a pass.
- `initial-xml-tail-oracle-failure.log`: the new XML value-comparison oracle
  initially included ElementTree tail whitespace, so insertion of M02's line
  appeared to change the preceding C04 value. The corrected semantic comparison
  uses attributes/text; the independent whole-file hashes still bind all bytes.
- `focused-host.log`: 53 focused historical/dialog checks pass.
- `composition-host.log`: seven exact-union and commuting-reversal checks pass.
- `optimized-host.log`: all 60 focused/composition checks pass under Python -O.
- `all-host.log`: 608/608 fresh aggregate host checks pass in 159.361 seconds,
  with no failures, errors or skips. Printed failed-protocol samples are intentional
  negative-control outputs, not accepted runtime receipts.

This environment has Java but no installed Gradle, Android SDK, or ADB. The
retained PR49 local bootstrap log documents the unavailable Gradle download.
No local Android compilation, JVM, installed, capture or APK pass is claimed.

## Required fresh composed-source acceptance

After independent source review and draft publication, obtain fresh exact-tree
Code review and normal CI. Inspect original JVM XML, installed raw logs/reports,
all source-bound dialog exports and actual PNGs, compiled Hungarian C05 values
and M02's one-entry coexistence, and corresponding-source/APK identity. C05's
real Hungarian About/notice and credit routes and M02's two action paths remain
in the JVM suite; PR49's installed French notices and Hungarian credit routes
remain in the device suite. Do not infer installed Hungarian notice coverage
from the JVM rendering. Model geometry, linguistic quality, physical devices,
TalkBack and all-language acceptance remain distinct, unestablished claims.

Standalone source receipts remain historical inputs:
[PR49](https://github.com/c933103/AN-Paint/tree/a37797d5f7efc9ad5841a3ba37aac6554bac8210/verification/localized-dialog-layout-2026-10-11/acceptance-38116209866),
[C05](https://github.com/c933103/AN-Paint/tree/3c871305f7a84767dd2909afd11598e754e27b4c/verification/hungarian-attribution-c05-2026-10-11/acceptance-38104574988),
and [M02](https://github.com/c933103/AN-Paint/tree/6d2e99a71597bb54386216eb116995aca739d806/verification/commons-metadata-m02-2026-10-11/acceptance-38099501387).
The held historical archive part166 is unrelated and is not used or retransmitted.
