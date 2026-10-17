# Esperanto merged-develop verification

The natural push [run 39065698813](https://github.com/c933103/AN-Paint/actions/runs/39065698813) for merge `9bff0abd8f7bc04facbb556908b3a6f578c7346f` completed successfully on attempt 1. All six jobs passed. The merge and reviewed PR124 head have identical tree `5f0fab23aadd6cc6ecec4233e2fc7a88f7784b24`. Develop still pointed to this merge when the terminal result was checked. No retry, source fix or gate change was necessary.

## Recorded results

- All three `EsperantoPriorityWordingTest` consumers passed: count-neutral dimension labels, bounded crop validation, and the actual crop-dialog invalid/reset/apply flow. Zero failures/errors/skips.
- All 1,107 JVM cases in 116 XML suites passed, zero failures/errors/skips. Lint XML contains zero issues.
- Hosted Python: 905 tests, two skips, no failures. The non-verbose output does not identify the skipped cases; this does not replace the separately preserved fully executed local suites.
- API35: exact source-bound 45-method app union, and 74 expected/completed native cases passed with no missing/unexpected/errors. Core and position identities agree on merge/run/source/APK and attempt 1.
- APK/corresponding-source and exact-script-generation jobs passed. No installable release/signature acceptance is claimed here.

These results do not certify Esperanto installed layout, physical devices, large fonts, TalkBack or native-speaker fluency. The nine linguistic holds, 27 wording-only entries and thirteen unchanged outside-priority crop occurrences retain their original distinctions.

## Durable evidence

[Verification packet](merged-runtime-packet.zip) and [SHA-256 checksum](merged-runtime-packet.sha256). The packet includes all 116 raw JVM XML files, complete phase logs/timings, lint XML, run/job/commit/artifact metadata, emulator summaries and an independently rerunnable verifier. It excludes unrelated image/report assets. Extract and run `python verify_hosted.py /path/to/exact/source`; normal and optimized runs passed. This verifies stored results, not a fresh Android execution.

The complete downloaded regression artifact `12114115521` is 83,962,729 bytes with SHA-256 `7dbdfc3737d50d03d3c7c4bfe69bbd8d7d6a7c7c096a43ea1fb98f67c9202ca2`. The complete API35 aggregate artifact `12113483870` is 11,406,289 bytes with SHA-256 `0a9d7c0a3ed112de3b497cc11ca8d16a682f3d5e852a33c2ebe365ad68587713`. Both downloads matched GitHub metadata before extraction. No captured image is claimed visually reviewed.

This evidence commit is additive to the exact merged application tree: every original application blob and mode is retained, with only this README, packet and checksum added on a separate evidence branch. It does not modify develop or remove application files. Earlier PR-runtime evidence remains at [bb1a2aaa](https://github.com/c933103/AN-Paint/blob/bb1a2aaa164cfe172db26546f65a6c3ed281d1d3/evidence/esperanto-priority-review-20261017/runtime-39063156079/README.md).
