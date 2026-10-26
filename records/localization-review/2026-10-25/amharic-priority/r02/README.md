# Amharic shared-family fixture follow-through

Parent head: c089ada7a562bb2aec37c11f4970d98212fa4a79.
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/40254007866
Regression job: https://github.com/c933103/AN-Paint/actions/runs/40254007866/job/121351844826

The complete Python run reported 1,343 tests, two failures and one error (two pre-existing skips): Amharic Commons SVG exact inventory and tagged-colour English fallback expectations. JVM tests reported 1,341 tests with five failures in CommonsSvgErrorTranslationTest and TaggedColourImportTest for the same newly translated message families. APK build, exact-script generation, lint and position API35 passed. These were unregistered current expectations, not a new linguistic defect.

This five-file repair registers only the three already independently reviewed Amharic values in the family fixtures/runtime oracles. Tagged-colour becomes 63 localized and 108 fallback options; global 59/112 scope is unchanged. Amharic raw XML retains Android outer quotes while decoded runtime oracles omit them. Python explicitly checks the family values against the independent Amharic priority fixture. Existing positive, malformed, missing, arbitrary/default and other corruption checks remain and now exercise Amharic too. The SVG actual-gallery test retains Amharic and adds Asturian as a genuine incomplete-catalogue fallback control rather than dropping the fallback requirement.

All 61 tests in the seven available relevant Python modules pass normally and under optimization. This is not a complete host suite or local JVM run; new hosted CI remains necessary. No production text or behavior changes. The original independent linguistic review, including source/context qualifications, remains unchanged.
