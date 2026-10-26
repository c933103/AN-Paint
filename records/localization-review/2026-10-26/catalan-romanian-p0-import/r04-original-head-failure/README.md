# PR177 original-head terminal failure preserved

Run [40319792630](https://github.com/c933103/AN-Paint/actions/runs/40319792630), reviewed head `06a2e4078efa1fe8ef8ea37b186ece0431633f08`, completed **failure**. Five checks succeeded; Regression tests and lint failed because of one JVM assertion. This head is not merge eligible.

Actual JUnit: 1361 tests, 1 failure, 0 errors, 0 skips, across 147 XML reports. The exact failed method is preserved with its artifact path, XML hash, message and stack. All new CA/RO methods passed. The failure correctly exposes a test-model gap: `ca-ES-valencia` inherits the new Catalan unsupported-colour message rather than English. It has no explicit resource of its own. Repair must model parent inheritance separately, not add a translation or linguistic acceptance.

Structural family inventory remains 70 direct catalogues /101 without a direct value. Actual Android routing is 70 direct +1 Catalan-parent inheritance +100 English fallbacks. Global59/112 scope remains unchanged. Earlier r03 wording “101 English fallbacks” was a stale runtime assumption; its records remain historical and this receipt corrects the claim explicitly.

Independent successes remain bounded: hosted Python 1388 run = 1386 passed +2 skips; lint has zero issues; API35 has 45 app +74 native source-bound cases; APK has 282 exact scoped compiled displays; source has 1,373 exact packaged tracked files from1,376 blobs with the same three exclusions;13 exact-script probes pass. None overrides the failed JVM gate. Local ordinary/optimized results are separate. No release or paused-scope expansion, no Valencian/native-human/device/layout/whole-locale certification.
