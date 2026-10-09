# First complete PR #30 CI run

[Run 37927180323](https://github.com/c933103/AN-Paint/actions/runs/37927180323)
tested merge `1964b005a454593ad9b8e1727a2ba2fb12c9aecf`, whose complete tree
`de0742cdd47a55e84ed2773f4808ddd7e3575d29` matches source head
`0a2d19db6805016f17b860f8d9964677cfc7880c` exactly.

- APK, corresponding source and instrumentation APK compilation passed.
- JVM: 706 tests, 12 failures, zero errors/skips. The 4 new vertical-status and
  8 existing full SVG-status tests passed. Lint was **not reached** after JVM failure.
- API35 installed: 74 library + 17 ordinary app + 1 restart seed + 1 restart
  verification = 93 passed. Ordinary app: 143.188 seconds under the unchanged
  180-second limit. Other invocations: 36.757, 4.564 and 6.466 seconds respectively.
- Catalogue matrix: all four executions stopped before completing a case.
  This run provides no all-catalogue acceptance or full-matrix runtime estimate.
- Reachability: all eight executions stopped at the first French same-Activity
  rotation, after initial French status/actions/native query checks. Later
  representative languages and Mongolian rotation were not reached.

`test-results.json` preserves all 799 JVM/installed case identities, timings and
failure details. `artifact-manifest.json` identifies every file of both downloaded,
SHA256-verified ZIPs, including the native PNG/JSON captures. Original artifacts
are linked in that manifest; their Actions retention is finite. Both complete ZIPs
and extracted contents were retained for subsequent evidence publication.

## Diagnosed setup defects and bounded correction

1. The lightweight catalogue controls were detached from a window. Android API30
   and API35 return before initializing the base accessibility node in that state:
   [API30 View source](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r1/core/java/android/view/View.java#L9483-L9486),
   [API35 View source](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/view/View.java#L10641-L10644).
   The corrected fixture reuses one attached Activity window per API/font-scale
   execution and records actual detached/attached nodes. Native Button class,
   source text, editable query, dimensions and no-shrink checks stay required.
2. Configuration-only rotation changed the manually measured decor but left the
   ViewRoot clip at the original size. Three independent failures exactly match
   that old clip: 640−288=352px, 480−288=192px, and 640−423=217px.
   Robolectric's [configurationChange implementation](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/android/controller/ActivityController.java#L362-L425)
   updates resources/configuration, while its `visible()` dispatches the
   [Display-backed resize](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowViewRootImpl.java#L107-L234).
   The corrected fixture supplies matching configuration/metrics and updates the
   simulated Display before dispatching its real resize. It records old/new
   ViewRoot, display, window and control bounds, then asserts that the full decor
   is visible before running the unchanged per-slice reachability checks.

No failed case or locale was removed, no visible rectangle is fabricated, no
control size is forced to satisfy reachability, and no production scrolling
workaround is inferred from these fixture failures. Fresh exact-head Android
results remain required to establish the corrected setup and remaining behavior.
