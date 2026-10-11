# Current-base Copy credit diagnostic integration

This candidate composes the bounded PR34 correction and its prepared diagnostics
on develop `eab28203893ffba45f14a7f96df6d19cf4d19d3b`, tree
`537185be479023d1567ab583d808ffaa7a4d3db8`.

## Preserved work and limits

All 81 file payloads from the earlier diagnostic candidate are byte-identical.
The current base's other 1,229 blob paths are preserved exactly, including PR33's
RTL navigation, PR35's eight notice-characterization paths and the three release
preparation paths. There are no removals. No language preference/routing code,
picker tags, aliases, artwork, fonts, workflow or application version is changed.

The production change remains three catch routes in metadata-only Copy credit
and three complete strings in the default and 59 scoped resource catalogues.
The other 81 offered tags remain explicitly incomplete default-English fallback.
This does not complete or supersede the withdrawn historical localization audits.

## What is established

The [first hosted run](https://github.com/c933103/AN-Paint/actions/runs/37964790893)
tested head `1cd0eeac6bc4a30cb331f3b27cdfa30ff62b97df`. Its exact resource tests
failed at API30 and API35 for `ko-Kore-KR`: ordinary Korean `복사` was returned
instead of the mixed-script catalogue's `複寫`. The 13 original route/layout
methods and both 81-tag fallback methods passed. Build, lint and the installed
API35 suites also passed; none of those results resolves the exact-string failure.

The prepared diagnostic selects and reads every tag through actual
`AppLanguage.select`, `selectedTag` and `wrap`, retains all exact expected strings,
and records requested, persisted and configured tags alongside actual resources.
A fourteenth route test starts the gallery using `ko-Kore-KR` and requires its
mixed-script failure message. It does not replace the expected text with fallback.

Source inspection finds no alias rewriting `ko-Kore-KR`: `select` persists the
tag and `wrap` passes the chosen locale to Android's resource configuration.
This is therefore a diagnostic of the actual application route, not a demonstrated
fix for the failed Android resource resolution. The earlier possible script-ranking
tie remains a source-level hypothesis. Android runtime results are still required.

## Current local verification

`host-results.txt` records all **363 Python tests passing** on this current-base
source; the command exited 0. `git diff --check` also passed.
The negative instrumentation-parser fixture outputs within that log are expected
test data; the unittest summary and exit status determine its host result.
These checks cover resources/source contracts, not Android runtime or linguistic
acceptance. The exact earlier archive is retained without repackaging or splitting.

Only a Java runtime is available locally. No `javac`, Gradle distribution,
Android SDK, `adb`, emulator or `aapt2` was found, so the prepared Android diagnostics
have not run locally. Fresh hosted results for the eventual published head must
be inspected before claiming the failure is fixed. PR34 remains excluded from
the separate 0.0.38 release preparation.
