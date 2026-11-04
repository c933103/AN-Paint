# Protected-draft route guard correction

This supplements, without changing, the immutable [localization reconciliation receipt](https://github.com/c933103/AN-Paint/blob/2035ae6ee9e4e2c7fd4a509abc2d5ec41ebcafaf/verification/localization-reconcile-20261104/README.md).

The receipt correctly reports three failing subtests, but its statement that the nch, nhe and nhw warning strings order the routes differently is incorrect. Each warning names recovery export before a separate Save-as route, with PNG/JPEG following Save as. The test matched the shorter Save-as caption inside the longer recovery-export caption. Normalization removes spaces and strips final ellipses from captions, allowing this prefix collision.

Normalized match spans are: nch recovery 88–134, false Save-as 88–102, actual Save-as 154–168; nhe recovery 93–142, false Save-as 93–108, actual Save-as 163–178; nhw recovery 92–140, false Save-as 92–106, actual Save-as 160–174.

The test blob b7e280606a7ec32f91777ddbf4ecc57cd1f04c5b is unchanged at merge base df0b1e4cb247a728e108bd2b666a96ce5114da2a, develop parent 1f763dbd25e93ad13285041e3d2bcb5051a40241, locale parent 4e0c3a8f061e1b54d4951357f4d05b97aefd27aa and merge 31fdd100c5f1162e2e416284a051e78732c53b46. The base/develop catalogues have no localized protected-warning entries for these three locales, so the check skips them. The locale parent already contains the exact inputs preserved in the merge. This is a pre-merge false positive exposed by added locale strings. These three failures are not evidence of a PR296 runtime regression.

The proposed test-only change excludes Save-as matches overlapping full recovery-route matches, while preserving route ordering, placeholder and trailing PNG/JPEG requirements. Synthetic regressions cover shared prefixes with >, → and ← separators, missing separate Save as (including repeated recovery routes), reversed order and formats attached only to recovery. Existing Hebrew left-arrow regression remains unchanged.

Local checks against the content-verified merge snapshot: original module runs 9 tests with 3 failing locale subtests; patched module runs 13 tests successfully. These are host-side structural/routing checks, not Android builds, device tests or linguistic certification. No translations or application source changed. Independent review passed: all 13 focused tests passed, including the negative cases. This correction accompanies the reviewed test-only fix; no hosted CI, Android build or device run is claimed.
