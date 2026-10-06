# Lithuanian crop-count recheck — 6 October 2026

Scope: register P04-017 and GH-012, plus only the crop-count part of P04-009.
Reviewed original PR #4 head `d30a08e4ec959844ee66a8d2b842598559babc93`.
No count-specific correction was established, so the canonical XML is unchanged.
This does not reinstate any withdrawn full-translation claim.

## Wording assessment

The current `one` uses `Taikyti %3$d vaizdui`, `few` uses
`Taikyti %3$d vaizdams`, and `other` uses `Taikyti %3$d vaizdų`.
The operation is applying a crop to the indicated number of images; the first two
noun forms are dative singular/plural, while the numeric groups 0 and 10–20 take
the genitive plural after their numeral. The `few` entry is present and is selected
for every count 2–9, not for 12–19. The count table checks all 21 values, including
10, 11, 19 and the maximum 20.

The width × height preview and the warning that cropping placed images moves
attachments are retained in all three items. `one` uses singular `išdėstytą vaizdą`
and `jo priedai`; `few`/`other` use plural `išdėstytus vaizdus` and `jų priedai`.
No missing clause was found in this specific resource. This does not settle
terminology elsewhere in the catalogue.

CLDR also defines Lithuanian `many` for nonzero fractional digits. This operation
accepts an integer image count only, so that category is unreachable here;
adding an unused fractional form is not required to fix the 0–20 crop display.

## Operation and count meaning

Freshly read `ImageCropDialog.kt` (lines 56–60, 91–94, 125–138 and 145–150),
`AssemblyActivity.kt` (lines 270–274), and `ImageAssembly.kt` (lines 54, 138–143
and 161–182). The batch dialog receives the assembly images; the single-image
dialog receives only the selected image. Checkboxes determine `selected`.
The status derives `count` from `images.count { it.id in selected }` and passes
that same value as both the Android quantity argument and `%3$d`. `%1$d` and
`%2$d` remain the preview width and height. The apply callback constructs a map
from exactly the selected images and passes it to `assembly.crop`.

The stated count is the number of images receiving crop rectangles. It does not
include other attached images whose positions reflow. The attachment warning
therefore describes an additional effect, not additional images counted as cropped.
The preview can show zero after None; Apply rejects the empty selection. The model
limits the assembly to 20 images. The preview-image spinner changes the dimensions
being previewed, not the selected-image count. These are source observations;
this recheck did not execute those controls on an Android runtime.

## Reproducible category check and limits

All integers 0 through 20 were checked using Node 24.19.0 `Intl.PluralRules`
(ICU 78.3 / CLDR 48.0), comparing each result to the reviewed CLDR ranges below.
This checks host plural selection, **not Android resource selection or rendering**.
Tables substitute ASCII digits to make the number easy to inspect; they are not
screenshots or proof of Android localized digit formatting.

```js
for (const locale of ["lt"]) {
  const rules = new Intl.PluralRules(locale);
  console.log(locale, Array.from({length: 21}, (_,n) => [n, rules.select(n)]));
}
```

Every existing plural item was separately parsed from canonical XML and checked
for one each of `%1$d`, `%2$d`, `%3$d` and one escaped newline. No generator or
reference JSON was used to alter the translations.

Primary references, retrieved 6 October 2026:
[Unicode CLDR 48 cardinal rules](https://www.unicode.org/cldr/charts/48/supplemental/language_plural_rules.html)
and [Android quantity-string contract](https://developer.android.com/guide/topics/resources/string-resource#Plurals).
CLDR supports the category mapping; it does not certify the wording. The wording
assessment above is a contextual source review, not native-speaker acceptance.

No Android SDK is configured in this workspace, so Gradle Android tests, actual
`Resources.getQuantityString` selection on supported APIs, visual layout, bidi
ordering and screen-reader output remain unverified here. The earlier withdrawn
CI/semantic claims are not used as evidence. The full PR and full locale reviews
remain open; this record covers only `ui_crop_preview_images` and its call path.

## Reviewed resource identity

| File | SHA-256 |
| --- | --- |
| `Paintroid/src/main/res/values-lt/strings.xml` | `97843c060b55792c174fc978965c13e24ca14e0ceaeda9a5541beaf54aab3e2d` |

At comparison time, these XML files are byte-identical in integration head
`a6b5956b0ae8f8082fafc2ff21d63e337f3a85af`. The original/integration crop call-path diff
only changes the dialog builder and installs locale typography; the count formula
and apply-map construction are unchanged. This statement does not validate typography.

## Checks run on this original branch

- `python3 -m unittest discover -s tools -p 'test_translations.py'`: 14 passed.
- `python3 -m unittest discover -s tools -p 'test_localization_repairs_pr4.py'`: 2 passed.
- Strict `aapt2 compile` of `values-lt/strings.xml`: passed with AAPT2 2.20-13719691, without `--legacy`.
- Host ICU category agreement: 21/21 integer cases from 0 through 20.

These checks establish structure, formatting and host category behavior only.
The contextual wording assessment above is separate and is not native-speaker
or Android runtime sign-off. No new implementation-mirroring test was added.

## Every in-range count

### lt

| Count | Host ICU category | Exact count sentence (ASCII digits for inspection) |
| --- | --- | --- |
| 0 | `other` | Taikyti 0 vaizdų. |
| 1 | `one` | Taikyti 1 vaizdui. |
| 2 | `few` | Taikyti 2 vaizdams. |
| 3 | `few` | Taikyti 3 vaizdams. |
| 4 | `few` | Taikyti 4 vaizdams. |
| 5 | `few` | Taikyti 5 vaizdams. |
| 6 | `few` | Taikyti 6 vaizdams. |
| 7 | `few` | Taikyti 7 vaizdams. |
| 8 | `few` | Taikyti 8 vaizdams. |
| 9 | `few` | Taikyti 9 vaizdams. |
| 10 | `other` | Taikyti 10 vaizdų. |
| 11 | `other` | Taikyti 11 vaizdų. |
| 12 | `other` | Taikyti 12 vaizdų. |
| 13 | `other` | Taikyti 13 vaizdų. |
| 14 | `other` | Taikyti 14 vaizdų. |
| 15 | `other` | Taikyti 15 vaizdų. |
| 16 | `other` | Taikyti 16 vaizdų. |
| 17 | `other` | Taikyti 17 vaizdų. |
| 18 | `other` | Taikyti 18 vaizdų. |
| 19 | `other` | Taikyti 19 vaizdų. |
| 20 | `other` | Taikyti 20 vaizdų. |

