# PR122 repaired runtime verification

[Run 39059990522](https://github.com/c933103/AN-Paint/actions/runs/39059990522) completed successfully at PR head `0d56dd970c22398f7fa032d1baee4a1b74c83f2b`. All six jobs passed: exact-script resource generation, APK/source build, regression/lint, core API35 emulator, position API35 emulator, and aggregate Emulator API35 gate.

The workflow tested synthetic merge `24eb78f21b5260cf38af112362664ab6b3ce2e0c`, whose parents are develop `5dba779c904a25bde2ec6d6f8f48eb3cad901a1e` and PR head `0d56dd970c22398f7fa032d1baee4a1b74c83f2b`. Its application tree `b8655bf9b69f89afd3499b9efce1414746de326c` is identical to the published PR head tree. GitHub run/artifact metadata also records that exact PR head.

## Raw JVM artifact results

Regression artifact `12110999914` (`regression-and-lint-24eb78f21b5260cf38af112362664ab6b3ce2e0c`), 83,961,348 bytes, SHA256 `7185755ff282825476cef86d1cd6e01ee0093176c70996ff845cd6df8178536b`:

- 115 JUnit XML reports: **1,106 tests; zero failures, errors or skips**.
- `AssemblyActivityTest`: **22 passed**, zero failures/errors/skips.
- `englishHelpModesReachActualHelpAndExactPositionToolbarWithCurrentLabels`: **passed**, 1.084s. This executes the separate complete language-only en→en-US and unmatched zxx→default assertions, followed by the nine app-language actual Help/Exact position toolbar consumers.
- `exactFirstPlacementAndUnplaceMatchHelpWhileSnapRemovalCanFillTheGap`: **passed**, 0.429s.
- Hosted Python contracts: **902 passed** (206.450s).
- JVM Gradle task and Android lint: successful.

The previously pending zxx/default routing and repaired actual Help loop are now runtime-verified in the hosted API33 Robolectric configuration. This does not claim every locale, every Android version, a whole language, or a separate device Help visual review. Position/core emulator success is reported at the job scope above, not as equivalent to the complete JVM Help fixture check.

`runtime-report.json` includes every JUnit report count and each AssemblyActivityTest method result. The exact AssemblyActivityTest XML, relevant regression log excerpt, completed job states, synthetic merge commit, and workflow status are preserved alongside it. `receipt.json` hashes these evidence files.

The [immutable failure and strict repair receipt](https://github.com/c933103/AN-Paint/blob/20fc50f45b2a78d2b255fb51772800a11b2c8dd4/README.md) remains the historical record of the first failed head and subsequent repair. It correctly recorded the new run as pending at publication; this runtime receipt resolves that pending check without rewriting the historical receipt. The [separate other-language full Help/source-binding re-review inventory](https://github.com/c933103/AN-Paint/blob/878c912c017e7b145d51d366e064727b34602e38/other-language-source-bindings.json) remains required. Review and merge remain with the parent reviewer. P3 and held PR56 remain unchanged.
