# Selected-locale numeric display evidence — PR119

Application head: `5401d2bd3a8287ac4ce517c0c8e216bdbe8241fe`
Base: `8c08554995f4d07be1b47736746ab2d0771e810e` (includes Greek #118)
Tree: `47d3226454d474bd8d2b62d859fca2b27afba1e5`

[Bounded source PR](https://github.com/c933103/AN-Paint/pull/119) · [exact-head hosted run](https://github.com/c933103/AN-Paint/actions/runs/39050219892)

## Result

All 876 local host tests passed normally (200.780 s) and optimized (200.446 s). AAPT2 compiled and linked the current resources. Catalogue validation passed. Kotlin 1.9.24 compiled the changed production code and six new actual-consumer JVM tests against API35, fresh resource symbols and existing dependency classes. The exact-template JVM probe passed 2,144 checks, including Arabic hex/index distinctions and ROOT/process-default negative comparisons. All 1,184 remote leaves/modes matched the reviewed base plus exactly seven changed files.

The initial host failure is preserved: one source-string assertion still expected the old unformatted memory-warning call. Its memory-warning assertion now requires the typed locale-aware call and arguments. No ImageImport test was changed.

## Scope

Budget captions and memory rejection warning, selection dimensions/rotation, fractional/integer zoom, and populated/empty recent-colour indices use the selected resource locale. Empty recent captions preserve their `%s` contract by receiving an already localized integer. The three new resource templates contain only numeric format syntax and are non-translatable. Hexadecimal syntax, arithmetic, editable numeric serialization, parsing, memory admission, colour values and wording remain unchanged.

The new Robolectric tests exercise actual consumers for pt-BR, German, English, Arabic and Romanian English fallback while the process default intentionally disagrees. They cover all three dimension-dialog routes, resize budget refresh/cancel, admission boundaries, geometry preservation, empty/populated transitions, zoom label/status and slider accessibility descriptions.

## Limits

Hosted run 39050219892 was **in progress** at receipt creation. Local Gradle wrapper download failed with `Network is unreachable`; full local Gradle, Robolectric, lint and device execution are **not claimed**. Direct Kotlin compilation and the JVM template stand-in are supplementary, not Android execution. Exact-head hosted test/review gates remain required. No installed UI, native-language fluency or complete-localization acceptance is claimed. PR117’s ImageImport/memoryLabel repair is separate.

The ZIP contains raw logs, scripts, exact changed source and templates, the patch, summary and source-bound remote inventory. `packet-manifest.json` gives each member’s SHA-256; the separate archive record identifies the ZIP itself. This evidence is intentionally outside the application diff.
