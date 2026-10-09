# PR19 post-merge checks: original attempt, 9 October 2026

The automatic [push workflow 37922913129](https://github.com/c933103/AN-Paint/actions/runs/37922913129) tested actual merge commit `2fc36a811a6c04d02760bb1da4d62af71653503a`, tree `3ac89e305f168a12f55bcf1c2ca898229e8e41a6` (identical to the reviewed/tested PR head).

- Production and instrumentation APK build succeeded.
- All 93 API35 installed cases passed again: 74 native/import + 17 ordinary app + accepted-credit restart seed/verify. Ordinary app took 152.915 seconds, about 27.1 seconds inside the unchanged 180-second limit. The pre-merge observation was 164.552 seconds, about 15.4 seconds inside. Neither measurement proves repeat-run stability.
- Regression attempt 1 **failed**: its existing 12-minute `Run local checks` step timed out during lint analysis. All 675 available JUnit cases passed with no failures/errors/skips, but no completed lint report was present. CI host summary was 315 total, including two unnamed skips. Do not label this attempt as a complete regression/lint pass.
- One diagnosed failed-job-only retry was requested with unchanged source/deadlines. Successful build/emulator jobs were not re-requested. A later successful attempt does not erase this original timeout.
- The downloaded emulator/regression ZIPs matched official artifact SHA-256 digests recorded in `provenance.json`. Only focused reports, derived JUnit totals/hashes and the original timeout excerpt are preserved here; full ZIPs/APKs are not copied.
- The post-merge logcat file ends in boot output and contains no gallery test tag. Its hash/extent are recorded in `logcat-capture-limits.json`. The three installed gallery cases passed their assertions, but this capture supplies no new lifecycle/proxy trace. The complete 153-line pre-merge trace for the identical tree remains in `verification/gallery-routing-runtime-2026-10-09`.

No physical-device, API30, live-provider, linguistic or universal-network-isolation claim is added. No timeout, test partition, inventory, production code or CI workflow was weakened. Retry outcome is recorded below and in `final-receipt.json`.

## Failed-job retry outcome

Attempt 2, [job 113800736562](https://github.com/c933103/AN-Paint/actions/runs/37922913129/job/113800736562), failed during dependency resolution: `repo.maven.apache.org` returned HTTP 403 for existing Robolectric and lint transitive dependency POMs. It produced no JVM/lint reports and uploaded no new regression artifact. The original failure excerpt and exact dependencies are preserved separately. The cause of the server 403 is not established.

Further retries pause at this dependency-access blocker. No repository mirror, credential, source, timeout or CI architecture change was made. The completed pre-merge regression/lint result remains valid for the identical source tree, but the post-merge workflow is still failed. Its separate APK and 93-case installed results remain passed. Physical/API30 gaps and the tighter pre-merge 15.4-second ordinary-app margin remain explicit.

Read-only diagnosis checked the [official status](https://status.maven.org/) and [403 guidance](https://central.sonatype.org/faq/403-error-central/): no reported general outage, and no specific rationale in the CI response. The concurrent AN29 combined run uses unchanged dependency/workflow declarations; its regression result was still pending at diagnosis time. This is an upstream HTTP response, not a tool-policy denial or user refusal. See `dependency-access-diagnosis.json`.

## Successful comparison and supersession

[AN29 combined regression job 113800831714](https://github.com/c933103/AN-Paint/actions/runs/37924730965/job/113800831714) succeeded at 11:49:02 UTC with unchanged dependency/workflow declarations and the same restored dependency-cache key. This supports successful same-configuration resolution/execution; it does not reveal individual cache/network responses or establish the original 403 cause. It justified one further unchanged failed-job retry.

Attempt 3 was then cancelled at 11:56:29 UTC, shortly after AN29 merged into develop (`8a75b825131f0b24c55a40a3636e9e70792037a8`, 11:55:55) and [successor run 37926785579](https://github.com/c933103/AN-Paint/actions/runs/37926785579) started (11:55:58). The existing workflow groups by branch ref and cancels in-progress runs. That supports supersession as the explanation; the log itself only states cancellation. It supplies no completed regression/lint result and is neither a test failure nor user refusal.

Do not rerun the superseded PR19 merge and compete with current develop. The newer combined source is being verified by the existing AN29 run owner. Pre-merge exact-tree success, both completed reviews, two independent 93-case installed passes, original timeout/403 and subsequent cancellation remain distinctly recorded.
