# Independent review of Amharic dimension and unit labels

Six candidate values are retained unchanged for their lexical and static contextual roles; two complete accessibility templates are held. No candidate needs an evidence-backed textual revision at this point. All 231 independent static checks pass. No production change, native-reader acceptance, build or release is implied.

The held values are `ui_width_in` and `ui_height_in`. Their meaning and placeholder structure are sound, but confidence in the complete short spoken-label idiom and pixel measure-word choice is insufficient. Keeping a plausible draft on hold is not a finding that it is ungrammatical. Retention of the two bare unit keys does not clear their held compositions.

## Scope and seal

Input manifest SHA-256: `830cf544de5bd76f85e4117484a2f9d97b18f8a92d36a0a0078cc706d894de3e`.
Pinned production: `66be61df27c5359bffc32d56db21f3949899f873`; tree: `870c5a584120d92710be516af0dc3b3847b183d9`.

This review recomputed the seal for all 43 listed files, the SHA-256 and Git blob of all 18 complete source copies, nine lexical snapshot hashes, all 16 lexical records and 24 exact fragments, every exact English key/value/attribute and candidate hash, four single `%1$s` contracts, and all eight expanded examples. It did not independently refetch the production head. The parent-provided freshness statement is retained as provenance rather than represented as this reviewer’s live-head observation.

## Decisions

| Key | Proposed display value | Decision |
| --- | --- | --- |
| `string/ui_pixels` | ፒክሰሎች | retain |
| `string/ui_percent` | ፐርሰንት | retain |
| `string/ui_pixels_6ec9c2` | ፒክሰሎች | retain |
| `string/ui_percent_fd8671` | ፐርሰንት | retain |
| `string/ui_width` | ስፋት (%1$s) | retain |
| `string/ui_height` | ቁመት (%1$s) | retain |
| `string/ui_width_in` | ስፋት በ%1$s | hold |
| `string/ui_height_in` | ቁመት በ%1$s | hold |

### ui_pixels

English: Pixels
Candidate XML text: `"ፒክሰሎች"`
Decision: **retain**. Confidence: medium-high lexical and contextual.

The AOSP paired camera records attest the exact plural ፒክሰሎች. Removing the explicit camera quantity leaves the generic unit without introducing a resize, crop, normalization, DPI or screen-density meaning. A bare plural is suitable for the unit choice. This is a justified component extraction, not an exact standalone AOSP label. LibreOffice alternatives are not silently normalized.

English value SHA-256: `48b027ebcdab5067b2f39188207faa13921c025d8fd8282f5976ceb94149d642`
Candidate XML-text SHA-256: `995eb4b9165b940a62b910949c0e99396cf45da0d6451aa90e4ada9253b74140`
Candidate display SHA-256: `8201371b5dc132f57d961527d59a1da3e321bbef8312f1205b5e149b67f20c9a`
Canonical source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L301

Evidence:
- `pixels_aosp_13mp`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 255; positive lexical component evidence).
- `pixels_aosp_4mp`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 258; positive lexical component evidence).
- `pixels_lo_plural`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po (snapshot line 32968; alternative unit-label evidence).
- `pixels_lo_ui_variant`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 22253; alternative spelling evidence).

Preserved alternatives:
- ፒክስሎች: Exact LibreOffice standalone plural variant; not the selected project/AOSP spelling family.

No textual revision requested by this review. Keep exact key and source contract; usual native, rendering and runtime validation remains outside this review.

### ui_percent

English: Percent
Candidate XML text: `"ፐርሰንት"`
Decision: **retain**. Confidence: high lexical; medium-high contextual.

LibreOffice has an exact nonfuzzy Percent label with ፐርሰንት in two contexts. The candidate names the unit alone, so it survives every inspected percentage baseline. The AOSP native alternative መቶኛ is legitimate but is not evidence that this loanword is wrong.

English value SHA-256: `716d633b125adb76832f17bee5bce63be33094820cd46ef1222cec4a7ae8eb58`
Candidate XML-text SHA-256: `ea81e985913506c1413427b1fbbe504e0ae4ac7cbc3c0507b411c26db488ea76`
Candidate display SHA-256: `efa86045b92ae7519efde8ca8c0742e113c1cd582892dc4ccc549ba785c80756`
Canonical source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L296

Evidence:
- `percent_lo_category`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 37; positive exact unit-label evidence).
- `percent_lo_command`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po (snapshot line 4250; corroborating exact unit-label evidence).
- `percent_aosp_native_variant`: https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT (snapshot line 524; alternative native percent noun evidence).
- `percent_aosp_preposition_variant`: https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT (snapshot line 2688; alternative native noun and preposition evidence).

Preserved alternatives:
- መቶኛ: Native AOSP alternative attested inside accessibility and settings phrases. If adopted, review the standalone and interpolated keys together rather than mix families.

No textual revision requested by this review. Keep exact key and source contract; usual native, rendering and runtime validation remains outside this review.

### ui_pixels_6ec9c2

English: pixels
Candidate XML text: `"ፒክሰሎች"`
Decision: **retain**. Confidence: medium-high lexical; complete spoken phrase pending.

Retain the exact attested plural as a bare unit resource. It has no preposition, number, screen-density meaning or fixed baseline. It can be combined with the template without duplicated በ. This lexical retention does not clear the held Width/Height-in compositions; whether a singular measure-word is more idiomatic in those phrases remains open.

English value SHA-256: `6ec9c2b0eb14010746c8bce8939303b382344b296206612eb8a907a37b2b2f37`
Candidate XML-text SHA-256: `995eb4b9165b940a62b910949c0e99396cf45da0d6451aa90e4ada9253b74140`
Candidate display SHA-256: `8201371b5dc132f57d961527d59a1da3e321bbef8312f1205b5e149b67f20c9a`
Canonical source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L302

Evidence:
- `pixels_aosp_13mp`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 255; positive lexical component evidence).
- `pixels_aosp_4mp`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 258; positive lexical component evidence).
- `pixels_lo_in_unit`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 22259; grammatical component evidence).
- `units_aosp_attached_preposition`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 423; grammatical component evidence).

No textual revision requested by this review. Keep exact key and source contract; usual native, rendering and runtime validation remains outside this review.

### ui_percent_fd8671

English: percent
Candidate XML text: `"ፐርሰንት"`
Decision: **retain**. Confidence: high lexical; complete spoken phrase pending.

Retain the same denominator-neutral percent noun. The LibreOffice in-percent prose supports use with በ, and the resource correctly does not contain that preposition itself. English capitalization does not require distinct Amharic values or permit merging the separate keys. Full spoken-label acceptance is withheld with the templates.

English value SHA-256: `fd86717aca41c558c78c19ab2b50691179a57ba5200bc7e3317be70efd4043ad`
Candidate XML-text SHA-256: `ea81e985913506c1413427b1fbbe504e0ae4ac7cbc3c0507b411c26db488ea76`
Candidate display SHA-256: `efa86045b92ae7519efde8ca8c0742e113c1cd582892dc4ccc549ba785c80756`
Canonical source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L297

Evidence:
- `percent_lo_category`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 37; positive exact unit-label evidence).
- `percent_lo_in_unit`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 8543; grammatical component evidence).
- `percent_aosp_preposition_variant`: https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT (snapshot line 2688; alternative native noun and preposition evidence).

No textual revision requested by this review. Keep exact key and source contract; usual native, rendering and runtime validation remains outside this review.

### ui_width

English: Width (%1$s)
Candidate XML text: `"ስፋት (%1$s)"`
Decision: **retain**. Confidence: high noun evidence; medium-high composed-label confidence.

The AOSP image-details Width record and LibreOffice graphics Width record agree on ስፋት. Both static results, ስፋት (px) and ስፋት (%), are clear noun-plus-parenthetical-unit labels. There is no unit inflection across the parenthesis boundary. The argument remains a unit token, not a numeric value.

English value SHA-256: `26452d4d4e24d067c14d1b46f59743fd2d85a52dc8ec93464008974fe38b89d5`
Candidate XML-text SHA-256: `4885032ddde2ca2aecc6827110c59af087491faf6bfe94356c2411c7765785af`
Candidate display SHA-256: `612871284621dc0ed13ffedf9de79df847c629ec4f3225b35214fe3476efefe4`
Canonical source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L469

Evidence:
- `width_aosp_image`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 128; positive exact image-dimension noun evidence).
- `width_lo_graphics`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po (snapshot line 20603; corroborating graphics dimension noun evidence).

No textual revision requested by this review. Keep exact key and source contract; usual native, rendering and runtime validation remains outside this review.

### ui_height

English: Height (%1$s)
Candidate XML text: `"ቁመት (%1$s)"`
Decision: **retain**. Confidence: high image-noun evidence; medium-high composed-label confidence.

The exact paired AOSP image-details Height record supports ቁመት in this image-dimension context. Both ቁመት (px) and ቁመት (%) retain that meaning without action or area semantics. LibreOffice እርዝመት remains a genuine alternative, but the more directly paired image evidence supports retaining the proposed noun rather than forcing a revision.

English value SHA-256: `691378ea0a4b0e5023bf65437a044ade7923f64d6349516079a0607d768619ed`
Candidate XML-text SHA-256: `479b99cc3edf33d8f6de233a16760e7a9d1921be978706c368adb4e650e5753a`
Candidate display SHA-256: `5885d4fe8b0b54fc7d9fb94e837e0663debfda38c5a13c52e86e5318a768f893`
Canonical source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L218

Evidence:
- `height_aosp_image`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 129; positive exact image-dimension noun evidence).
- `height_lo_graphics_variant`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po (snapshot line 20621; alternative graphics dimension noun evidence).

Preserved alternatives:
- እርዝመት (%1$s): Original template composition using the exact LibreOffice graphics Height noun. Not selected because AOSP provides an exact image-details Height counterpart.

No textual revision requested by this review. Keep exact key and source contract; usual native, rendering and runtime validation remains outside this review.

### ui_width_in

English: Width in %1$s
Candidate XML text: `"ስፋት በ%1$s"`
Decision: **hold**. Confidence: medium semantic plausibility; insufficient complete-label idiom confidence.

The two results are semantically intelligible: ስፋት በፒክሰሎች and ስፋት በፐርሰንት. The attached በ is structurally plausible, occurs exactly once, and is supported by AOSP unit-preposition usage. However, the preserved pixel/percent precedents are finite prose, and the AOSP seconds example is an imperative. They do not settle the naturalness of this noun-first short accessibility label or the plural versus singular pixel measure-word in it. Supplemental LibreOffice width-as-percentage prose corroborates the sequence but still does not settle the label idiom. Hold the exact candidate, do not invent a replacement or call it incorrect.

English value SHA-256: `3297aa59eb3953cb425c7ae48189df1234f398453e2f481339806861eeb4e604`
Candidate XML-text SHA-256: `f09978dd693620c5aea2ea702aa42b4d1f71f6d1cb39822f7da9e64bbbd5f1ff`
Candidate display SHA-256: `e3e29c593ffe6cc0654bdee080fc3d10d5271032e7fca6710d5ae14ecedd5d0a`
Canonical source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L470

Evidence:
- `width_aosp_image`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 128; positive exact image-dimension noun evidence).
- `pixels_lo_in_unit`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 22259; grammatical component evidence).
- `percent_lo_in_unit`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 8543; grammatical component evidence).
- `units_aosp_attached_preposition`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 423; grammatical component evidence).

A competent Amharic reviewer should assess both complete unit expansions as short accessibility labels, including noun order and singular/plural pixel measure-word choice. Review both dimension templates and both bare unit resources together; runtime speech remains a separate later check.

### ui_height_in

English: Height in %1$s
Candidate XML text: `"ቁመት በ%1$s"`
Decision: **hold**. Confidence: medium semantic plausibility; insufficient complete-label idiom confidence.

The results ቁመት በፒክሰሎች and ቁመት በፐርሰንት preserve height and the intended units. Placeholder, preposition and bare-noun integration are structurally sound. Whole-label naturalness and pixel measure-word choice remain unresolved for the same reason as Width-in; the additional height-as-percentage prose uses the alternative እርዝመት, not this exact noun. Hold this candidate and retain that alternative for a coordinated contextual decision. No grammatical defect is proved and no stronger replacement is established.

English value SHA-256: `193af0dda260fe2967e99a5c3eda5b77eb36345e9283f09aa6f7c92148fa4112`
Candidate XML-text SHA-256: `a4b146f3e07107aa8478242d392e6686ffc0c9a9406a131cebf58b09f578ed43`
Candidate display SHA-256: `1a86276fc8cef5bf4f6fc1759b1649eaa5fc4cffcc8c2061176b92128fe625ec`
Canonical source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L219

Evidence:
- `height_aosp_image`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 129; positive exact image-dimension noun evidence).
- `height_lo_graphics_variant`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po (snapshot line 20621; alternative graphics dimension noun evidence).
- `pixels_lo_in_unit`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 22259; grammatical component evidence).
- `percent_lo_in_unit`: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po (snapshot line 8543; grammatical component evidence).
- `units_aosp_attached_preposition`: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT (snapshot line 423; grammatical component evidence).

Preserved alternatives:
- እርዝመት በ%1$s: Original full composition using LibreOffice Height; would require joint review with ui_height and both substituted unit forms.

A competent Amharic reviewer should assess both complete unit expansions as short accessibility labels, including noun order and singular/plural pixel measure-word choice. Review both dimension templates and both bare unit resources together; runtime speech remains a separate later check.

## Full interpolation review

| Template | Argument | Exact expanded result | Review |
| --- | --- | --- | --- |
| `string/ui_width` | px | ስፋት (px) | Retain noun-plus-unit label |
| `string/ui_width` | % | ስፋት (%) | Retain noun-plus-unit label |
| `string/ui_height` | px | ቁመት (px) | Retain noun-plus-unit label |
| `string/ui_height` | % | ቁመት (%) | Retain noun-plus-unit label |
| `string/ui_width_in` | ፒክሰሎች | ስፋት በፒክሰሎች | Structural/semantic pass; complete-label idiom held |
| `string/ui_width_in` | ፐርሰንት | ስፋት በፐርሰንት | Structural/semantic pass; complete-label idiom held |
| `string/ui_height_in` | ፒክሰሎች | ቁመት በፒክሰሎች | Structural/semantic pass; complete-label idiom held |
| `string/ui_height_in` | ፐርሰንት | ቁመት በፐርሰንት | Structural/semantic pass; complete-label idiom held |

The visible parenthetical forms introduce no noun agreement across the unit boundary. The four spoken forms have one attached በ and one bare unit, with no doubled preposition or numerical argument. Their semantic reading is width/height measured in the named unit. The remaining judgement is whether these exact short labels are the preferred natural Amharic phrasing, including whether pixels should use a singular measure-word. The evidence does not justify silently changing spelling, noun order or number.

## Consumer semantics

### DimensionControls

Percent is relative to the original.width or original.height argument supplied when the control is created, not image area. The original argument can be the current canvas dimensions, import source dimensions or renderer original output dimensions. The shared words must not promise restoration to a historical untouched file.
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L53-L69
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L86
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1012-L1024
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageResizeDialog.kt#L29-L31
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L297-L306

### Crop

Left/right percentage trims use each source width; top/bottom use each source height. These are margins to remove, not percentages of resulting width/height to retain. Generic Pixels/Percent remains correct. Pixel-mode margins must be integers even though the input widget allows decimals; CropMargins validates and rounds resolved values.
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt#L75-L108
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L39-L50

### Normalization

The baseline is the largest current placedSize on the selected axis across assembly.images, including crop/normalization effects, not each source original size. Width/Height parenthesized templates serve pixel-mode content descriptions with px; percent-mode accessibility has distinct normalization-specific keys outside this review.
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L19-L35
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L50-L61
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L19-L32

### Interpolation

Visible dimension labels receive literal px or %. Spoken dimension templates receive translated bare pixels/percent nouns. A literal percent sign inserted as a string argument is data, not another template token. The ui boundary routes to LocaleText, which validates placeholder contracts and formats once. This is source inspection, not runtime execution.
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L86
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/UiText.kt#L48-L67
- https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleText.kt#L95-L108

## Supplemental evidence and its limits

The official LibreOffice Amharic Position and Size page contains the dimension-before-unit sequences “ስፋት በ ፐርሰንት” and “እርዝመት በ ፐርሰንት” in longer relative-size explanations. This is useful corroboration for semantic composition, not direct short-label acceptance: https://help.libreoffice.org/latest/am/text/swriter/01/05060100.html . The corresponding English context is https://help.libreoffice.org/latest/en-US/text/swriter/01/05060100.html . The retrieved views displayed different versions, 26.2 and 26.8 respectively, so they are not presented as a pinned same-revision bilingual pair. The preserved immutable packet remains the principal evidence.

Searched exact full and near-full Amharic dimension/unit combinations both in the two established primary domains and on the general web. General-web hits with unestablished translation provenance were not used to clear the holds. This is bounded search, not proof that an acceptable exact label exists nowhere.

## English source and coverage

No defect was established in these eight canonical English labels. Do not compensate for a hypothetical source problem in Amharic. If a genuine English defect is identified later, correct English first, flag every affected language, and review those translations individually.

There are 720 named source containers, including three explicitly nontranslatable file-name strings. Excluding those gives the dossier’s 717 canonical translatable containers. The supplied Amharic catalogue has 12 present and 705 missing; all eight reviewed keys remain absent. Prior 60 ready/retained items and six prior holds are untouched. This review adds six independent retentions and two new holds to this batch only, not eight production additions or eight newly cleared spoken labels.

## Exact next step for the held pair

Competent Amharic contextual review of all four complete spoken phrases or stronger well-provenanced short-label usage.

Assess ስፋት በፒክሰሎች, ስፋት በፐርሰንት, ቁመት በፒክሰሎች and ቁመት በፐርሰንት together. Keep the alternatives visible: pixel singular ፒክሰል, LibreOffice plural ፒክስሎች, percent መቶኛ, and height እርዝመት. These are review options, not accepted replacements. A phrase need not exist verbatim in a corpus to be a valid translation; the hold is this reviewer’s confidence limit for the composed accessibility idiom, not an exact-match policy.

## Limits

- No production head fetch was performed by this reviewer. Byte/blob bindings were recomputed against the supplied parent provenance.
- No Kotlin/Java or Android runtime, build, rendering, accessibility speech, UI fit, or native speaker test was run.
- Static Python string substitution validates supplied examples, not formatter execution.
- All eight candidate keys are absent in the supplied production Amharic XML.
- All prior 60 retained/ready items, six earlier holds, and aspect-lock wording remain separate.
- The bound source search covered the 18 supplied files, not the whole repository.
- No Work task, further delegation, production edit, app build, CI, release, repository publication, or third-party contact was performed.
- The eight external lexical snapshots are reused pinned copies; their hashes and exact records were independently checked, not independently re-fetched.
- Native-reader judgement, accessibility speech, UI fit and lifecycle behavior remain untested.

## Reproducibility

`verify.py` is a read-only verifier of the input dossier and regenerates `validation.json`. `review.json` contains decisions, candidate/source hashes, evidence links, confidence, limits and the exact pending linguistic gate. `supplemental-evidence.json` records the added web evidence without claiming immutable provenance. `MANIFEST.json` and `SEAL.txt` bind the full review package. The original dossier is not modified.
