# M02 test-only font-scale fixture correction

The original PR47 head `9f985b7a144fd49cb33a87ba5a5a73fc7be84a2b` used `fontScale200` as an Android resource-qualifier suffix in the double-scale M02 readability test. Pinned Robolectric 4.14.1 does not support that spelling. The existing `CommonsCopyCreditErrorTest` instead uses the dedicated `@Config(fontScale=2f)` attribute.

This follow-up changes the annotation to `@Config(qualifiers="w320dp-h640dp-port-xhdpi",fontScale=2f)` and adds a host contract requiring that attribute and rejecting the unsupported suffix. The expected `2f` runtime configuration, text/geometry/accessibility assertions and all forty intended capture pairs remain. No production/resource/translation changes, no disabled method, and no relaxed assertion or timeout.

The original normal CI run [38098843107](https://github.com/c933103/AN-Paint/actions/runs/38098843107) remains historical. Its source/Android test execution is not transferred to the new head. The defect was source-identified; no local Robolectric execution is claimed. Original local Gradle bootstrap remains blocked before compilation. Six focused host contracts pass normally and under Python -O after this correction. A fresh aggregate replay and normal CI are tracked in the PR discussion; the original 516-pass record describes the earlier snapshot.

The original source manifest and preparation logs remain unchanged and tied to the original head. This separate note records the later test-only correction. PR47 remains draft, with parent-owned merge and all documented language/fallback/native-acceptance limits still open.
