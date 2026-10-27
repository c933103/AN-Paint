# Exact-head local validation and source readback

PR [188](https://github.com/c933103/AN-Paint/pull/188), head `ad6373256e918c0579bdb320c23bc19518aed65f`, tree `8e2b7586b62e65bc8afaf007751b9cb3d2d91c92`.

- Final ordinary host suite: **1,491 passed**, 197.565 seconds, exit 0.
- Final optimized host suite: **1,491 passed**, 191.981 seconds, exit 0.
- Focused new guards: 9 passed in each mode; existing Spanish successor suite: 11 passed in each mode. Independent focused checks and final source/fixture readback are archived separately.
- All 1,405 remote source/test file blobs and modes match the intended tree: six changed paths, three additions, no removals. Twenty exact reviewed XML edits, 707 untouched entries in each changed catalogue, all 717 Hungarian entries unchanged, all 83 historical fixtures unchanged.

## Preserved earlier stages

The 16-value stage passed 1,490 ordinary and optimized tests. The initial 20-value ordinary stage **failed**: 1,490 tests, one error and one failure. Both were the old Spanish memory-warning expectation (`píxeles`) after the independently accepted `px` successor. A finite one-key source/predecessor/attribute-bound projection preserves the historical fixture and rejects unrelated changes. Its 1,491-test normal/optimized reruns passed. Final extra-key/wrong-locale guard cases were then separately run in the final source suites above. None of these earlier stages is relabelled or substituted for final-source results.

The archive retains every local stage log/exit code and both independent readback checkpoints. Only local workspace directory prefixes are sanitized; manifest hashes distinguish original and public bytes. Synthetic negative-example output printed by passing host tests remains verbatim.

## Review and remaining gates

Read the [complete review](../complete-review/README.md) together with the mandatory [provenance/hold addendum](../provenance-addendum/README.md). The final accounting keeps seven PT holds, nine ES holds and seven HU holds; prior reported and already-applied values receive no novel-pair credit.

[Hosted run 40480384625](https://github.com/c933103/AN-Paint/actions/runs/40480384625) is in progress at publication. Exact-head Codex review was requested. Android JVM compilation/execution, lint, APK/corresponding source and API35 are not run locally because the toolchain is absent; required hosted gates remain pending. No release, API30, physical-device, whole-language or native-speaker acceptance is inferred.
