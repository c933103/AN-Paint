# Russian and Arabic crop-count recheck — 6 October 2026

Scope: register P05-005, P05-006 and P05-007, only
`ui_crop_preview_images` and its operation/call path.
Reviewed original PR #5 head `6008b43078abe2e32d0537bb4de0624139d408bc`.
No count-specific correction was established, so the canonical XML is unchanged.
This does not reinstate any withdrawn full-translation claim.

## Wording assessment

Russian: `Применить к %3$d изображению` is used for `one`;
`Применить к %3$d изображениям` for `few`, `many` and `other`.
The preposition `к` governs the dative: singular `изображению` versus plural
`изображениям`. The `few` and `many` sentences can correctly share the dative plural;
they do not need different noun spellings merely because the category names differ.
For 0–20, `one` is 1, `few` is 2–4, and `many` is 0 and 5–20.
All four items keep the preview dimensions and the placed-image attachment warning.
Russian `other` is the required fallback; CLDR assigns decimals to it, but the
Android call and image count are integers. Its presence is not evidence that
fractional-image messages have been reviewed or are supported.

Arabic: each of `zero`, `one` and `two` says
`عدد الصور التي سيُطبَّق عليها القص: %3$d` — an explicit number of images to which
the crop will be applied. This neutral count construction retains 0, 1 and 2
without incorrectly attaching a singular noun after the dual count. `few` uses
`تُطبق على %3$d صور` for 3–10; `many` uses `تُطبق على %3$d صورة` for 11–20.
The `other` item also uses `صورة`; its first nonnegative integer examples are
100–102, beyond this assembly's limit. A separate host check selected `other` for
100, 101 and 102. All six items retain the dimensions, explicit count placeholder
and warning that cropping placed images repositions their attachments.
The Arabic count describes the selected crop targets, not every image whose
attachment geometry might subsequently move.

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
for (const locale of ["ru", "ar"]) {
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
| `Paintroid/src/main/res/values-ru/strings.xml` | `d9926144febac7fa61a9ab21933aa479d48d1f8b8a1f3f055d55d8216f745da0` |
| `Paintroid/src/main/res/values-ar/strings.xml` | `b9c98cc26331f396f694a1e3651345c2363ca8d8aa2a6355b9f2e4d922b71957` |

At comparison time, these XML files are byte-identical in integration head
`a6b5956b0ae8f8082fafc2ff21d63e337f3a85af`. The original/integration crop call-path diff
only changes the dialog builder and installs locale typography; the count formula
and apply-map construction are unchanged. This statement does not validate typography.

## Checks run on this original branch

- `python3 -m unittest discover -s tools -p 'test_translations.py'`: 14 passed.
- `python3 -m unittest discover -s tools -p 'test_localization_repairs_pr5.py'`: 2 passed.
- Strict `aapt2 compile` of `values-ru/strings.xml`, `values-ar/strings.xml`: passed with AAPT2 2.20-13719691, without `--legacy`.
- Host ICU category agreement: 42/42 integer cases from 0 through 20.

These checks establish structure, formatting and host category behavior only.
The contextual wording assessment above is separate and is not native-speaker
or Android runtime sign-off. No new implementation-mirroring test was added.

## Every in-range count

### ru

| Count | Host ICU category | Exact count sentence (ASCII digits for inspection) |
| --- | --- | --- |
| 0 | `many` | Применить к 0 изображениям. |
| 1 | `one` | Применить к 1 изображению. |
| 2 | `few` | Применить к 2 изображениям. |
| 3 | `few` | Применить к 3 изображениям. |
| 4 | `few` | Применить к 4 изображениям. |
| 5 | `many` | Применить к 5 изображениям. |
| 6 | `many` | Применить к 6 изображениям. |
| 7 | `many` | Применить к 7 изображениям. |
| 8 | `many` | Применить к 8 изображениям. |
| 9 | `many` | Применить к 9 изображениям. |
| 10 | `many` | Применить к 10 изображениям. |
| 11 | `many` | Применить к 11 изображениям. |
| 12 | `many` | Применить к 12 изображениям. |
| 13 | `many` | Применить к 13 изображениям. |
| 14 | `many` | Применить к 14 изображениям. |
| 15 | `many` | Применить к 15 изображениям. |
| 16 | `many` | Применить к 16 изображениям. |
| 17 | `many` | Применить к 17 изображениям. |
| 18 | `many` | Применить к 18 изображениям. |
| 19 | `many` | Применить к 19 изображениям. |
| 20 | `many` | Применить к 20 изображениям. |

### ar

| Count | Host ICU category | Exact count sentence (ASCII digits for inspection) |
| --- | --- | --- |
| 0 | `zero` | عدد الصور التي سيُطبَّق عليها القص: 0. |
| 1 | `one` | عدد الصور التي سيُطبَّق عليها القص: 1. |
| 2 | `two` | عدد الصور التي سيُطبَّق عليها القص: 2. |
| 3 | `few` | تُطبق على 3 صور. |
| 4 | `few` | تُطبق على 4 صور. |
| 5 | `few` | تُطبق على 5 صور. |
| 6 | `few` | تُطبق على 6 صور. |
| 7 | `few` | تُطبق على 7 صور. |
| 8 | `few` | تُطبق على 8 صور. |
| 9 | `few` | تُطبق على 9 صور. |
| 10 | `few` | تُطبق على 10 صور. |
| 11 | `many` | تُطبق على 11 صورة. |
| 12 | `many` | تُطبق على 12 صورة. |
| 13 | `many` | تُطبق على 13 صورة. |
| 14 | `many` | تُطبق على 14 صورة. |
| 15 | `many` | تُطبق على 15 صورة. |
| 16 | `many` | تُطبق على 16 صورة. |
| 17 | `many` | تُطبق على 17 صورة. |
| 18 | `many` | تُطبق على 18 صورة. |
| 19 | `many` | تُطبق على 19 صورة. |
| 20 | `many` | تُطبق على 20 صورة. |
