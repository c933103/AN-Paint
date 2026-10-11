# Exact-head Korean resource-routing result

Run [38019693421](https://github.com/c933103/AN-Paint/actions/runs/38019693421)
tested PR34 head `c157eaaee6e13f416ae76b9827c51d6ed3fe4782` through merge
`2c444ec99f8a4721ac58c34d7e290399e7e66c74`. GitHub readback confirmed the merge
tree is exactly reviewed tree `226fc014cc13f47322c60fcd5e4d7aec8fdfb12b`.

## Actual results

- Universal debug APK/corresponding source and lint passed. CI Python discovered
  376 tests: 374 passed and two were skipped (`OK (skipped=2)`, 67.626 seconds).
  The skipped cases are the optional Pillow ICO-export open and Adam7 fixture
  independent decoder checks; structural checks remain active. The earlier local
  source-validation run executed all 376 without skips.
- JVM: **766 executed, 762 passed, four failed, zero errors/skips**.
- All **11** new routing cases passed on their declared API30/API35 matrix.
  Both general-resource reports contain all **28** expected rows with no text
  mismatches. Public preference/platform identity remains unchanged.
- Both **59**-row Copy-credit reports have exact text, including the required
  Korean `複寫`. All **14** Copy-credit route/layout cases and all four
  translation/fallback cases passed, including both **81**-tag fallback tests.
- Installed API35 passed 74 native tests, 18 ordinary app tests, and the separate
  one-test seed/verify phases. The new targeted installed picker/rotation case
  is not in this head. API30 installed execution did not run.

This establishes the original three Korean JVM text failures are repaired on
both tested native-resource backends. It does not make the whole JVM run pass,
certify linguistic completeness, or establish targeted installed behavior.

## The four retained failures

`DeviceLanguagePickerTest.everyOfferedDeviceLocaleUsesTheSameFormattingAsExplicitChoices`
failed twice, on API30 and API35: its old expected-label helper queried the
unmapped plain `ko-Kore-KR` framework locale and obtained `시스템 언어 사용`.
The application now correctly returned the canonical `시스템 言語 使用`.
The follow-up uses that fixed, independent mixed-script text rather than calling
the production resolver to manufacture an expected value.

`GalleryBackDirectionTest.everyOfferedLocaleUsesAccessibleBackAndKeepsBothNavigationBranches`
failed twice because it expected `ko-Kore-KR` in the internal resource
configuration rather than `ko-Kore-KR-anpaint`. The follow-up asserts the exact
internal tag plus separate public preference, Java-default and platform tags.
All 140 locale iterations, navigation branches and completeness checks remain.
These two failing loops did not complete all their rows in this historical run;
their unaffected assertions still require a fresh complete pass.

The failure JUnit XML is retained without alteration. No failure was converted
to a skip, excluded, relabelled as a pass, or retried unchanged.

## APK/source inspection

The downloaded artifact SHA-256 matched GitHub's digest. Build Tools 35.0.0 AAPT2
from that artifact printed `b+ko+Kore+KR+anpaint` in `dump configurations`.
`dump resources` showed **695** compiled resource entries (694 strings and one
plural) exactly identical between the canonical and generated catalogues.
The four fixed Save/Copy-credit values and per-resource compiled-value hashes
are retained in `packaged-resource-evidence.json`.

The embedded source ZIP contains the byte-identical canonical XML, Gradle
generator and AppLanguage source from the reviewed snapshot. It has no
checked-in generated variant copy. This inspection is not a clean/incremental
Gradle replay; the added independent CI probe must establish that separately.
Command reference: [AAPT2 dump](https://developer.android.com/tools/aapt2).

## Pending exact-head acceptance

The follow-up adds disposable-worktree generation probes and the installed
real-picker/rotation regression. With `ci:full-android` applied before the next
code synchronization, the existing workflow must run API30 and API35. The
source-inventory expectations are 73 native + 18 ordinary app methods on API30,
and 74 native + 19 ordinary app + one seed + one verify on API35. These counts
include the new method and retain the existing SDK-specific exclusions.

Require a fresh 766-case JVM pass, complete 140-row older checks, all strict
59/28-row resource reports, successful clean/incremental probe summary and both
installed platforms. None of these pending results is claimed by this record.
The single Codex request was [usage-limit blocked](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6093180539);
there were no repeated requests or PR state changes to seek another review.
