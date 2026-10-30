# Russian crop-preview plural: fresh bounded review, 13 October 2026

## Decision

**Count/case wording passes; the whole resource needs one shared warning correction before source/context acceptance.** The changed `many` sentence is grammatical and describes the selected crop targets correctly. The warning in every quantity item names connections/relations (`связи`) as the objects moved, instead of the attached images whose positions actually change. This is a narrow affected-object meaning error, not a plural-category defect. Keep this exact resource open for that correction; do not turn a successful count review into whole-resource or whole-language acceptance.

Confidence: high for integer-count meaning, category mapping and case forms; medium-high for the warning's lexical/contextual defect. The latter is a linguistic judgment supported by the current code and the current Russian help, not a measured claim about how every reader will interpret it. No native-speaker acceptance is claimed or required for this bounded review.

## Fresh identities

GitHub `develop` was independently resolved on 13 October 2026 to [6a77442847e385742ab274b059cb4d022c364e08](https://github.com/c933103/AN-Paint/commit/6a77442847e385742ab274b059cb4d022c364e08). All five files below were independently fetched at that exact ref. Temporary file bytes were Git-blob-hashed and checked against the current recursive tree. They also match the earlier temporary copies supplied for this review.

| File under Paintroid/src/main/ | Current Git blob |
| --- | --- |
| [res/values/strings.xml](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/res/values/strings.xml#L489-L492) | `005ec95b25cc816f067b78a073a2b1b8c37b71d6` |
| [res/values-ru/strings.xml](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/res/values-ru/strings.xml#L676-L681) | `c804c1bff63e601be5286e241ed69889d992a6f2` |
| [java/org/catrobat/paintroid/classic/ImageCropDialog.kt](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt) | `c7ee442c2ae9741500b401b0a22c2994b90d8134` |
| [java/org/catrobat/paintroid/classic/AssemblyActivity.kt](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L271-L274) | `7391229f13d4bc53702c0be60da57c6dbe344d99` |
| [java/org/catrobat/paintroid/classic/ImageAssembly.kt](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt) | `dea06f0eb76052b40cd1e22b478b1b6de86672a7` |

Companion `russian-review-identities.json` records full-file SHA-256 digests, bytes, exact parsed items and host category results.

## Exact current English and Russian items

These are XML text values, retaining the source's literal backslash-n escape.

English `one`:
```text
Preview: %1$d × %2$d px\nApply to %3$d image. Cropping placed images repositions their attachments.
```

English `other`:
```text
Preview: %1$d × %2$d px\nApply to %3$d images. Cropping placed images repositions their attachments.
```

Russian `one`:
```text
Предпросмотр: %1$d × %2$d px\nПрименить к %3$d изображению. Обрезка размещённых изображений перемещает их связи.
```

Russian `few`:
```text
Предпросмотр: %1$d × %2$d px\nПрименить к %3$d изображениям. Обрезка размещённых изображений перемещает их связи.
```

Russian `many`:
```text
Предпросмотр: %1$d × %2$d px\nИзображений для обрезки: %3$d. Обрезка размещённых изображений перемещает их связи.
```

Russian `other`:
```text
Предпросмотр: %1$d × %2$d px\nПрименить к %3$d изображениям. Обрезка размещённых изображений перемещает их связи.
```

## Source meaning and reachable counts

- [AssemblyActivity 271–274](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L271-L274): batch crop supplies all assembly inputs; single-image crop supplies only the selected image. Empty input does not open the dialog.
- [ImageCropDialog 57–65, 85–94](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt#L57-L94): preview reference and selected targets are separate. The spinner changes the reference image. Count is exactly `images.count { it.id in selected }`, passed both as Android's selection quantity and as the third formatted argument. Arguments one and two are the reference image's proposed crop width and height, not a common size promised for every target.
- [ImageCropDialog 125–148](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt#L125-L148): checkboxes and All/None update selected targets. With valid margins, None can display zero. Apply rejects an empty selection; otherwise its map contains exactly the selected images and their crop rectangles.
- [ImageAssembly 54, 82–84, 183–188, 213–215](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L183-L188): the model enforces a maximum of 20 images, including loaded projects. Reachable preview quantities across these UI paths are integers 0–20; single-image mode stays at 1.
- [ImageAssembly 138–143 and 162–192](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L138-L192): `crop(Map)` copies crop rectangles into selected images and calls `change`; it does not call `reflow` or modify `attachment`. Layout derives child positions from their parent's right/bottom/left/top bounds. Thus additional attached images can move without being additional crop targets. Placement relationships remain unchanged on this path.

## Linguistic assessment of every component

The preview prefix accurately labels the one preview size; retaining `px` does not change the units. All six English/Russian items contain exactly one each of `%1$d`, `%2$d`, `%3$d` and one newline escape.

- `one`: `Применить к 1 изображению.` is correct dative singular after `к`. The omitted object of “apply” is supplied by the crop dialog.
- `few`: `Применить к 2/3/4 изображениям.` correctly uses dative plural. A genitive form appropriate to a standalone counting phrase would be wrong after `к`.
- `many`: `Изображений для обрезки: 0/5/…/20.` is an acceptable inverted, elliptical count label (“Images to crop: N”). The genitive plural describes how many images are designated for cropping. It preserves the prospective selected-target meaning, including zero, and does not claim the operation has already happened. Switching from an instruction to a count label is stylistic variation, not a semantic defect.
- `other`: the dative plural text is present with correct arguments and the same crop/warning meaning. It is a fallback, not evidence that fractional-image quantities are supported or linguistically accepted. No integer in this UI reaches this CLDR category.

The [Gramota dictionary's declension of изображение](https://gramota.ru/meta/izobrazhenie) independently lists `изображению` / `изображениям` as dative and `изображений` as genitive plural. Its indexed dictionary content was available; direct page opens returned HTTP 403. The exact application's wording assessment above is this reviewer's judgment, not dictionary certification.

### Shared warning: meaning correction required

`Обрезка размещённых изображений перемещает их связи.` literally assigns movement to their connections. [Gramota's Большой толковый словарь entry for связь](https://gramota.ru/poisk?dicts%5B%5D=42&mode=slovari&query=%D1%81%D0%B2%D1%8F%D0%B7%D1%8C) supports relationship/connection/joining senses, not “the images attached to an image.”

The source establishes that the affected visible objects are attached images and that `Attachment(anchor, edge)` relationships are retained. The current [Russian assembly help, line 189](https://github.com/c933103/AN-Paint/blob/6a77442847e385742ab274b059cb4d022c364e08/Paintroid/src/main/res/values-ru/strings.xml#L189) already states this explicitly: `Существующие присоединённые изображения перемещаются при обрезке их родительского изображения.`

A reader might infer the intended movement from context, but the present warning does not correctly name what moves. This is the confirmed textual referent mismatch; this review does **not** claim that the wording literally promises reparenting, broken links or corrupted attachments. Those would overstate it.

**Minimal proposed correction:** in all four Russian quantity items, replace only the warning with:
```text
Обрезка размещённых изображений перемещает присоединённые к ним изображения.
```
Keep the prefix, dimensions, newline, count sentences and placeholders unchanged. This preserves the current source's warning strength and makes the moved objects explicit. “Предварительный просмотр” instead of “Предпросмотр”, a Cyrillic pixel abbreviation, or identical count-label style in all forms would be optional style work and are not blockers here.

## Selection verification and limits

[Unicode CLDR 48 Russian cardinal rules](https://www.unicode.org/cldr/charts/48/supplemental/language_plural_rules.html) select `one` for integer endings in 1 except 11; `few` for 2–4 except 12–14; `many` for the remaining nonnegative integers. `other` covers visible-fraction cases. Within 0–20: `one = {1}`, `few = {2,3,4}`, `many = {0,5,6,…,20}`, `other = {}`.

[Android's plural-resource contract](https://developer.android.com/guide/topics/resources/string-resource#Plurals) separates language-dependent category selection from the supplied item labels. [Resources.getQuantityString](https://developer.android.com/reference/android/content/res/Resources#getQuantityString(int,%20int,%20java.lang.Object...)) takes an integer quantity plus formatting arguments, matching the inspected call.

Fresh Node 24.19.0 / ICU 78.3 / CLDR 48.0 `Intl.PluralRules("ru")` selection matched those expected categories for all 21 integers, 0–20. This is a host check, not an Android runtime test. XML parsing and placeholder/newline checks passed. No Android resource-selection, compiled-resource, UI-layout, typography, digit-rendering or screen-reader test was run in this review.

## Historical receipt reconciliation

The [6 October receipt pinned at 4231edaa](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/crop-plural-recheck-pr5-2026-10-06.md), independently fetched with blob `152b893011f01991549043e6821b9fa97f008246`, assessed original PR #5 head `6008b430…`. It described a different `many` count sentence: `Применить к %3$d изображениям.` Its successful count/case observations cannot accept the changed label without a new review.

The actual Russian resource at `4231edaa` (blob `5a6caf2e63671195b2a4ef10a1c1ab998c3469d3`) already has the same four plural items as current develop, including the new `many` label. Thus “changed” here is relative to the wording described by that historical receipt, not a new change between `4231edaa` and `6a774428`.

This new review resolves that stale count assessment, but it finds the shared-warning defect when examining the whole current resource. No source was edited or published. No other resource, locale, original PR or full-language review is signed off.

