# Italian, Greek and Turkish source validation

[PR189](https://github.com/c933103/AN-Paint/pull/189), head `0ba9f9dd90f2017c1bf3f360020aa6c8850a68dc`, tree `f35a14b65be904318b16e800f0d20ef9d30fd17b`, actual parent `1126b650216478c422997dcd1236ca6cc780e4e3`.

- Actual-parent ordinary suite: **1,500 passed**, 191.963 s, exit 0.
- Actual-parent optimized suite: **1,500 passed**, 195.739 s, exit 0.
- Independent new + prior Italian/Greek/Turkish suites: **42 passed**.
- All **1,408 source/test file blobs and modes** read back exactly. Six intended changed paths only; all six earlier PR188 paths preserved without fresh credit.
- Independent full typed-resource readback and static test review passed. Seven new JVM consumer methods remain subject to hosted execution, not inferred from Python or static inspection.

## Original stages retained

The earlier base651 suite passed 1,490 tests. The first nine-test focused run failed one assertion that incorrectly expected a named `dither` constructor argument rather than the actual positional argument. The corrected exact-source assertion and current guards pass. Original failure logs, exit codes and all later stage logs are preserved, not relabelled. Synthetic negative-example output printed after aggregate OK remains part of the original passing-test logs.

The manifest binds every original and sanitized file hash. Sanitization is limited to local workspace prefixes and internal role terminology; failure evidence and review outcomes are unchanged. The source-validation archive is a distinct record from the separately pending bulky linguistic-review archive and does not claim that archive is available.

## Hosted gates at this checkpoint

Exact-head [Codex code review](https://github.com/c933103/AN-Paint/pull/189#issuecomment-6440727543) completed clean. [Run40494757661](https://github.com/c933103/AN-Paint/actions/runs/40494757661) has successful resource generation, APK/source build and Position API35 jobs; regression/lint and Core API35 remain in progress. No Android, JVM, lint or installed-device result is inferred beyond those observed job states. No release or whole-language/native-reader certification is claimed.
