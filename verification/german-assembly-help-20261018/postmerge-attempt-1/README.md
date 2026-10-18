# German assembly Help: postmerge attempt 1

Merge: `ec4d74eb222c58d51e4a339e43ca83cc7aa16ec3`, with tree `05f725b3a5c64acdace799cfb8cb5d5768ce8f63` identical to reviewed PR129 head `2686f35c1c43910f659fdfe48944a61516bd473e`.
Run: https://github.com/c933103/AN-Paint/actions/runs/39087387993/attempts/1

## Terminal result: failed evidence collection

Four jobs passed: APK/corresponding source, exact-script resources, regression/lint, and position API35. Core API35 and the dependent combined gate failed. All 74 native and 38 selected core app instrumentation methods passed, but immediately afterward both required screenshot pulls returned `adb: error: failed to get feature set: device offline`. The runner correctly changed success to failure because installed dialog and vertical captures were unavailable. Passing method results do not make this attempt a passing run or supply the missing captures.

The exact core artifact, raw job log, coverage and JUnit summaries are preserved in the packet. `core-failure.log` is the compact failure excerpt. A single rerun of the failed jobs was requested after diagnosing the device-offline collection failure. No assertions, deadlines, production or workflow code were changed. This receipt does not claim the retry has passed.

## Bounded German correction remains exercised

The downloaded regression artifact independently verifies 1,124 JVM tests, zero failures/errors/skips, in 120 suites. All four complete Help/crop consumer methods pass, including the previously failing German toolbar/placement regression. All 120 XML files and the readable affected class XML are retained. Position API35's 7 selected methods passed; its device identity matches the exact downloaded APK/source hashes.

The APK/source artifact digest and both payload hashes match build-info. The APK embeds exactly the companion source ZIP. All 1,206 included tracked payload files match the reviewed Git blobs and executable modes; the archive omits two .gitignore files and .idea/codeStyles/Project.xml. This is a CI-debug-key build, not an upgrade-signed delivery. Exact-script resources passed all nine clean/incremental probes.

The earlier [failed/repaired PR runtime evidence](https://github.com/c933103/AN-Paint/blob/dab89c939d761b6b649899f6daa2562df8bd4e20/verification/german-assembly-help-20261018/repaired-runtime/README.md), including the original locale-fixture failure, remains unchanged. No full German catalogue, native-speaker, installed German glyph/layout or TalkBack acceptance is claimed. PR75 broader obligations and PR56/explicit holds remain unchanged.
