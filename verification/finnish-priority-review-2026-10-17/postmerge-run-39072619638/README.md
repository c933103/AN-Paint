# Finnish PR126 postmerge verification

[Natural develop run 39072619638](https://github.com/c933103/AN-Paint/actions/runs/39072619638), attempt 1, completed successfully on 17 October 2026. All six jobs passed without a retry or repair.

## Merge and runtime identity

PR126 merged as `a9d32f8368c2d2e7fbeecfe1a1b8f9100ae7b6dc`. Its parents are develop `b6a99b41c4390ca6a412e3a1938eb913c59509fb` and the reviewed application head `69fe1495d4468fc028cf1bc30bdac35e70e6cdf0`. The merge tree is `c723db3d5e2c3202ea24c021f6a3e3574e840a83`, exactly the tree reviewed and tested in the passing PR run.

The natural push run, exact-script report and composed API35 identity name this actual develop merge. Core and position reports both use attempt 1, the same build variant, APK/source hashes and source-test inventory. The final gate validates the complete disjoint union.

## Verified results

- Hosted Python: 918 tests passed in 189.915 seconds.
- JVM: 1,113 tests across 118 XML reports, zero failures, errors or skips.
- All four Finnish consumer methods passed in 0.251 seconds: actual language-picker title/fallback/Cancel, singular/grouped pixel counts, repeated dimension-unit switching and all three encoder-failure consumers with pixel preservation and successful PNG control.
- Android lint: zero reported issues. Exact-script resource generation: nine successful probes.
- Universal APK and corresponding-source job passed.
- API35: 74 native tests and the complete 45-method app union passed, including all seven position methods, with no missing, duplicate or excluded methods.

[Summary](summary.json), [Finnish JUnit XML](FinnishPriorityWordingTest.xml), [postmerge packet](postmerge-receipt.zip) and [checksum](packet.sha256). The packet retains terminal metadata, all six job logs, all 118 JVM JUnit reports, lint/phase logs, original exact-script artifacts and source-bound native/app instrumentation receipts. Downloaded artifact archive hashes were verified before extraction. Screenshots and the complete 84 MB regression archive are not duplicated; their original artifact metadata remains preserved.

## Continuing limits

The complete [341-entry source-based linguistic review](https://github.com/c933103/AN-Paint/blob/c2d1bdd3fd1f4f37f640f2fe3b38d031d25543a8/verification/finnish-priority-review-2026-10-17/README.md) and [initial PR runtime evidence](https://github.com/c933103/AN-Paint/blob/d63b49654fd7c65017553012edb3263170678926/verification/finnish-priority-review-2026-10-17/hosted-run-39070781922/README.md) remain immutable. All nine uncertainty holds, 31 wording-only judgments, 375 unreviewed canonical entries, PR56 upload hold and other project holds remain unchanged. The separately counted P2 width correction does not expand the 341-entry review.

Finnish consumer tests are JVM/Robolectric evidence, not installed Finnish layout or TalkBack acceptance. The general API35 suite does not certify a whole catalogue or native-language fluency. This is not a release, private upgrade-signing, physical-device or API30 verification. APK/source hashes are the hosted composed identity receipt; no separate local signature or embedded-source reinspection is claimed.

The initial local optimized-run failure and accidentally overwritten raw-log disclosure remain in the original packet. The natural postmerge run needed no weakened assertions, workflow changes, retries or repairs.

This additive evidence update preserves every one of the 1,214 existing source/evidence leaves and their modes unchanged and adds only five files in this directory. No evidence is inserted into the application branch.
