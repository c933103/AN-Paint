# PR19 post-merge checks: original attempt, 9 October 2026

The automatic [push workflow 37922913129](https://github.com/c933103/AN-Paint/actions/runs/37922913129) tested actual merge commit `2fc36a811a6c04d02760bb1da4d62af71653503a`, tree `3ac89e305f168a12f55bcf1c2ca898229e8e41a6` (identical to the reviewed/tested PR head).

- Production and instrumentation APK build succeeded.
- All 93 API35 installed cases passed again: 74 native/import + 17 ordinary app + accepted-credit restart seed/verify. Ordinary app took 152.915 seconds, about 27.1 seconds inside the unchanged 180-second limit. The pre-merge observation was 164.552 seconds, about 15.4 seconds inside. Neither measurement proves repeat-run stability.
- Regression attempt 1 **failed**: its existing 12-minute `Run local checks` step timed out during lint analysis. All 675 available JUnit cases passed with no failures/errors/skips, but no completed lint report was present. CI host summary was 315 total, including two unnamed skips. Do not label this attempt as a complete regression/lint pass.
- One diagnosed failed-job-only retry was requested with unchanged source/deadlines. Successful build/emulator jobs were not re-requested. A later successful attempt does not erase this original timeout.
- The downloaded emulator/regression ZIPs matched official artifact SHA-256 digests recorded in `provenance.json`. Only focused reports, derived JUnit totals/hashes and the original timeout excerpt are preserved here; full ZIPs/APKs are not copied.
- The post-merge logcat file ends in boot output and contains no gallery test tag. Its hash/extent are recorded in `logcat-capture-limits.json`. The three installed gallery cases passed their assertions, but this capture supplies no new lifecycle/proxy trace. The complete 153-line pre-merge trace for the identical tree remains in `verification/gallery-routing-runtime-2026-10-09`.

No physical-device, API30, live-provider, linguistic or universal-network-isolation claim is added. No timeout, test partition, inventory, production code or CI workflow was weakened. Retry outcome is recorded separately after it finishes.
