# Finnish PR126 initial hosted verification

[Run 39070781922](https://github.com/c933103/AN-Paint/actions/runs/39070781922), attempt 1, completed successfully on 17 October 2026. All six jobs passed. This adds terminal runtime evidence to the immutable [full 341-entry review](https://github.com/c933103/AN-Paint/blob/c2d1bdd3fd1f4f37f640f2fe3b38d031d25543a8/verification/finnish-priority-review-2026-10-17/README.md).

## Exact source binding

- Application head: `69fe1495d4468fc028cf1bc30bdac35e70e6cdf0`.
- Actual PR merge checkout: `4daf64866b621af8adbe618d135cdd5ca0902cfd`, whose parents are develop `b6a99b41c4390ca6a412e3a1938eb913c59509fb` and the application head.
- Both application and tested merge have the identical reviewed tree `c723db3d5e2c3202ea24c021f6a3e3574e840a83`.
- Initial checks ran while the PR was draft. Parent coordination marked it ready only after terminal success; Codex/security review and merge remain the parent's separate gates.

## Actual results

- Hosted Python contracts: 918 passed in 207.619 seconds.
- JVM regression: 1,113 tests in 118 XML reports, zero failures, errors or skips.
- All four new Finnish consumer methods passed in 0.334 seconds: actual picker title/fallback/Cancel, singular and grouped pixel counts, repeated dimension-unit switching, and all three real encoder failure consumers with source preservation and successful PNG control.
- Android lint: zero reported issues.
- Exact-script resource generation: nine probes passed.
- Universal APK and corresponding-source job passed.
- API35 native suite: 74 tests passed. Complete source-bound app union: 45 methods passed, including both position shards, with no missing/duplicate methods or exclusions. Core and position identity receipts use attempt 1, the same merge checkout, variant and APK/source hashes.

[Summary](summary.json), [original Finnish JUnit XML](FinnishPriorityWordingTest.xml), [runtime packet](hosted-receipt.zip) and [packet checksum](packet.sha256). The packet preserves six raw job logs, all 118 JVM JUnit reports, original resource-graph artifacts, terminal run/job/artifact metadata, lint/phase logs, native/app instrumentation receipts and exact tested merge metadata. Artifact archive hashes were checked before extraction. The larger original artifacts remain linked in their metadata; screenshots and complete 84 MB regression archive are not duplicated in this packet.

## Limits and preservation

These four Finnish tests use JVM/Robolectric actual consumers; they do not establish installed Finnish layout, TalkBack, native-speaker certification or whole-catalogue linguistic acceptance. General API35 success does not remove the nine Finnish uncertainty holds, the 31 wording-only judgments, the 375 unreviewed canonical entries or existing project holds. API30, physical devices and private upgrade signing are outside this run. APK/source hashes here are the hosted composed identity receipt, not a separate local signature or embedded-source reinspection.

The earlier local optimized run's five ICO-fixture failures and accidentally overwritten raw-log disclosure remain unchanged in the first evidence packet. No checks were weakened and no application/workflow changes or retries were needed for this first hosted run.

This is an additive evidence update: all 1,209 pre-existing source/evidence leaves and their modes are retained unchanged. Only this hosted-run subdirectory is added. The application PR remains four files; no evidence is inserted into its source tree.
