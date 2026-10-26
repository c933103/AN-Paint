# PR174: terminal exact-head gates

[PR174](https://github.com/c933103/AN-Paint/pull/174), head `3c8123707106dfc991221517e443276f857797db`, base `857a20103285a77846e340b326667c15a402ff9e`. [Run 40279026132](https://github.com/c933103/AN-Paint/actions/runs/40279026132) completed successfully: all six jobs passed, last aggregate API35 job completed 06:42:12 UTC on 26 October 2026. Tested merge `ccf60becbb36d17849b907c49bad7d23c17f02cf` has the exact reviewed tree `8ca5fc4f3989cf8c9307432d5e5c28ceef698251`.

**Merge eligible subject to live base/head/ref verification.** [Exact-head Code review](https://github.com/c933103/AN-Paint/pull/174#issuecomment-6409612193) is clean. Optional Security also completed clean; it is not promoted into a required merge gate. These are PR results, not postmerge results.

## Executed results

- Hosted JVM: **1,349 passed**, 144 JUnit XML suites, zero failures, errors or skips. Five focused suites contain 26 executed tests; their complete method sets match current source, including new compiled resources, recovery behavior and real GIF/APNG import consumer checks. The existing export/dirty-state regression passed.
- Hosted Python: **1,364 run = 1,362 passed + 2 skipped**. The non-verbose terminal summary does not name the skipped identities; they are not inferred from source or local runs. Local ordinary and optimized runs were separately recorded in r03 with 1,364 passing and zero skips each.
- Android lint: **zero issues**. All four hosted phase receipts have exit status zero.
- API35 emulator: **45 app + 74 native tests**, unique exact case identities and current test-source hashes independently revalidated. Main APK, source ZIP and instrumentation APK hashes match the executed prebuilt identity. No missing, unexpected or failed cases.
- Previously verified r04 remains applicable: 13 exact-script probes, all 1,364 packaged tracked source files, embedded source ZIP, APK signature, and all 80 bounded reviewed Nynorsk compiled values.

`verify_regression_artifact.py` and `verify_api35_artifact.py` reproduce the terminal artifact checks with explicit source, commit, run, artifact and digest inputs. The API verifier re-extracts an unchanged archive and preserves its original receipt before independent reconstruction. Verification development exposed two local checker defects, not product/CI failures: the first JVM inventory parser missed an intervening `@Config` annotation; the first in-memory app comparison compared tuples with JSON lists. The corrected checkers reject unparsed annotations, compare exact case sets, and normalize only the JSON representation. Both final checks pass against the unchanged downloaded artifacts. No CI rerun or source change was needed.

## Scope and holds

72 newly reviewed values, 118 prior values unchanged, five no-current-consumer identities absent. Paired memory-warning oracle remains 120 entries/60 tags; Nynorsk is only a separate P0 single-key expectation, not a new paired/P1 acceptance. All four reviews retain their static qualifications and mixed-fallback limitations. No native-human, physical-device, whole-language or layout certification. PR56 never-merge, PR159 freeze, PR113 hold, Help callback/archive identity and release pauses remain unchanged.
