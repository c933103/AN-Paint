# Exact mixed-script Korean resource routing candidate

This candidate integrates current develop `80c14372b0504bc44f9f2809ad477247fdc8100b`
without changing its seven SDK-inventory correction files. It builds on PR34
head `209098ae341d28a6ca3279c5c1ed53476d84ee99`. Publication and fresh Android
execution require review; no passing runtime result is claimed for this candidate.

## Established failure

[Run 38017319227](https://github.com/c933103/AN-Paint/actions/runs/38017319227)
tested exactly PR34's source tree. Its [retained JSON/JUnit evidence](../diagnostic-209098ae/)
records 755 JVM cases with three failures. Both API30/API35 resource reports
contain all 59 scoped tags. Only `ko-Kore-KR` mismatches, despite requested,
persisted and configured tags all being `ko-Kore-KR`. The real gallery failure
route also displays ordinary Korean `복사` instead of required `複寫`.

The other 13 Copy credit route/layout tests, both 81-tag fallback cases, 363
Python tests, build, lint and installed API35 checks passed. These results do not
override the failed exact-string checks or certify linguistic acceptance.

## Framework mechanism and affected scope

Android [API30's locale table](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r48/libs/androidfw/LocaleDataTables.cpp)
and [API35's table](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/libs/androidfw/LocaleDataTables.cpp)
infer `Kore` for ordinary `ko`. In both revisions, `ResTable_config::match`
accepts the resulting same-script candidates. `isLocaleBetterThan` then compares
region and variant; explicit script spelling is not a preference when scripts
already match. Thus `ko-KR` and `ko-Kore-KR` have no locale-ranking discriminator.
See [API30 ranking](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r48/libs/androidfw/ResourceTypes.cpp)
and [API35 ranking](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/libs/androidfw/ResourceTypes.cpp).

The canonical catalogue audit finds only two exact scriptless/scriptful pairs:
`ko-KR`/`ko-Kore-KR` and `vi`/`vi-Hani`. The same tables infer `Latn` for `vi`,
which differs from `Hani`, so that pair does not have the Korean same-script tie.
Other scriptful catalogues have no same-language/region scriptless counterpart.
This bounded analysis is not a claim of complete validation of all locale fallback.

## Proposed correction

- Keep `ko-Kore-KR` in preferences, Android's application locale setting, the
  picker, declared system-language list and the Java default locale.
- Resolve only that exact locale through internal resource variant
  `ko-Kore-KR-anpaint`. The same region/script and matching variant give Android
  a discriminator. This synthetic qualifier is an implementation detail, not a
  new public language choice.
- Before resource processing, a Gradle `Sync` task mirrors every XML file from
  the canonical `values-b+ko+Kore+KR` directory into the generated variant
  directory. Strings, plurals, escapes and resource types remain byte-identical.
  `Sync` removes stale generated files; there is no second editable catalogue.
- Apply the resource mapping consistently in `wrap`, `refresh` and device-label
  lookup. Keep orientation, dimensions, font scale and chosen layout direction.
- Leave the other 139 offered tags, all catalogue text, provider data, import
  behavior and existing error expectations unchanged. No per-message replacement
  or hardcoded translated fallback is introduced.

## Regression plan and current verification

The strict original three-string oracle and real-gallery `複寫` expectation are
unchanged. Only the diagnostic's expected internal configured tag changes; the
requested/persisted tag is still asserted exactly.

`AppLanguageResourceRoutingTest` adds API30/API35 coverage of all 21 explicit-script
choices plus seven regional/scriptless controls using independent general-UI
expectations. It also checks all 140 routing identities, ordinary Korean,
whole-catalogue plural formatting, repeated switching, live configuration refresh,
number symbols, device-default labels and the Android13+ preference backend.
The general-UI observations are emitted separately from Copy credit observations.

Five new Python contracts check the bounded mapping, canonical build input,
generation dependency, complete fixture scope and known competing catalogues.
All **376 Python tests passed**; the full local host result is in
`host-results.txt`. Android compilation,
generated-resource packaging and runtime selection remain unrun locally because
the SDK, Gradle distribution and compiler are unavailable. Hosted checks must
validate this candidate before it can be called fixed or merge-ready.
