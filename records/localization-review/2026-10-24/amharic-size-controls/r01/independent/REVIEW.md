# Independent Amharic size-controls review

Input manifest: `a6441b78c07df68b8acbf3ae1669d8f8ca7aedc1f39df3ad2e3f15b007df4aa1`
Production: `66be61df27c5359bffc32d56db21f3949899f873`. Tree: `870c5a584120d92710be516af0dc3b3847b183d9`.

**Result: 5 retain, 0 revise, 2 hold.** The added hold is Lock proportions; Spray radius remains held.

Retain is a bounded independent wording/source judgment, not native-reader or product-release acceptance. No source input or production file changed; no Work task, app build, CI or release. Prior 47 ready/four holds are separate and unchanged.

## Integrity and exact-value checks

All 33 input manifest entries match. All 14 complete source files match both their supplied Git blob IDs and SHA-256 hashes. All seven source values, proposed XML text hashes, keys and attributes match. All seven keys are absent from the supplied production Amharic catalogue. All 19 lexical records match 23 exact source fragments. The seven pinned lexical snapshot files match their recorded hashes.

Three literal (px) labels and one literal (%) label are preserved. Strength and Original size preserve formatted="false". Tolerance has no percent unit. No selected value contains a printf argument placeholder. NumericSlider formatting and accessibility templates are excluded.

Checks were completed before the environment restart and retained. This reviewer did not refetch production or lexical sources: production-tree freshness is dossier provenance, and the seven lexical sources are expressly reused pinned snapshots.

## string/ui_size_px: RETAIN

English: Size (px)
Proposed value: መጠን (px)
Exact XML: `<string name="ui_size_px">"መጠን (px)"</string>`

The exact graphics UI Size record supports መጠን. It retains the same generic noun as the English source and does not incorrectly narrow a shared setting to diameter, line width, or a guarantee that every tool mark changes. The literal pixel unit is unchanged.

Consumer check: ClassicPaintActivity.kt:774,778 supplies a separate Pencil size or shared strokeWidth, each 1..100. PaintCanvas.kt:18..20 maps Pencil size to pencilWidth. PaintDocument.kt:247..258 consumes width; PaintCanvas.kt:526..535 separately draws Spray with fixed 1px points. This is a bounded label approval, not validation of every shared tool option.

Confidence: High lexical and semantic confidence; no native-reader or rendered acceptance.

Primary evidence:
- size_label: [libreoffice-am-cui.po:19993–19997](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)

Limits:
- A shared Size control being ineffective for an individual tool cannot be repaired by changing only this translation. No English correction is established by this review.
- Native preference and UI fit remain unverified.

Source-value SHA-256: `2c1cb5c678172ab54740dc1dac9cef90006b4c168faa7359b348e116ef0d6790`
Proposed XML-text SHA-256 (including resource quote wrappers): `d6590da501c9d51e667db4eab26d39add1be18113dfb90b1560f6b14f79d8fb6`
Per-key decision seal: `72f9e32493654f015defd91589e9384a1d6b70b0aad2c97706aeb504326e7992`

## string/ui_radius_px: RETAIN

English: Radius (px)
Proposed value: ራዲየስ (px)
Exact XML: `<string name="ui_radius_px">"ራዲየስ (px)"</string>`

The Radius record and its adjacent corner-rounding explanation directly support ራዲየስ for this geometric radius. Corner radius in the UI supplies independent same-domain corroboration. The untranslated Radius-to-Radius record is not positive evidence.

Consumer check: ClassicPaintActivity.kt:779..782 exposes the rounded-rectangle corner-radius slider, minimum 0. PaintCanvas.kt:411 clamps the actual radius to half the shorter rectangle dimension. This is radius, not diameter; slider range and effective geometry clamp are distinct.

Confidence: High lexical and same-function semantic confidence; no native-reader or rendered acceptance.

Primary evidence:
- radius_label: [libreoffice-am-help01.po:30529–30536](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)
- radius_corner_context: [libreoffice-am-help01.po:30538–30545](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)
- radius_corner_svx: [libreoffice-am-svx.po:2122–2126](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)

Limits:
- The evidence supports the loanword and geometry, not a claim that it is the only preferred native technical term.
- Preserve literal (px).

Source-value SHA-256: `1ec84edf1e8551f375b863282a8e1117715ab18312f4bdaf52d39cb3b9cbc794`
Proposed XML-text SHA-256 (including resource quote wrappers): `a10340f6a7aaa67f46851000a1b0ccdd722a017da813c8c2a2e29163bff8d8fc`
Per-key decision seal: `fb2bc18cd5e7d2275ae5081a3d5ebf81d27f7afd3c9c6c0675a8c98e754ebbdd`

## string/ui_spray_radius_px: HOLD

English: Spray radius (px)
Proposed value: የመርጫ ራዲየስ (px)
Exact XML: `<string name="ui_spray_radius_px">"የመርጫ ራዲየስ (px)"</string>`

The exact Radius attestation cannot certify the original spray component መርጫ or the whole compound. The supplied bounded corpus contains no eligible Spray or Spray radius primary record. The existing terminology hold is therefore preserved, without calling the proposed word definitively wrong or inventing a replacement.

Consumer check: ClassicPaintActivity.kt:784 exposes 1..100 image pixels. PaintCanvas.kt:526..535 generates points in a disk using sqrt(random)*radius, with fixed 1px points and max(8,integer radius) point count. The label concerns the spray disk radius, not dot width or diameter.

Confidence: Low for the complete Amharic compound; high for the radius component and consumer meaning.

Primary evidence:
- radius_label: [libreoffice-am-help01.po:30529–30536](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)

Limits:
- No claim that no translation exists outside the searched corpus.
- Native graphics-tool terminology review is needed for Spray and the full compound.
- Preserve literal (px); do not promote this value to accepted coverage.

To clear hold: Obtain a reliable Amharic graphics-tool attestation or competent native-context review confirming the spray noun and complete radius label against the disk-radius behavior.

Source-value SHA-256: `dbce2d022204ede1adbb04a6bc8e3546066f52befe68f00fd6532690b8ee242e`
Proposed XML-text SHA-256 (including resource quote wrappers): `e07620a3c22a2d26d2b5d41a558fb4406556571fc44bb9bd9c7b4bb47a57499e`
Per-key decision seal: `8d7dd5080c084cf26a088a26bc6f030ffc4438205cf25e7ffd4a1e61e650c4e8`

## string/ui_strength: RETAIN

English: Strength (%)
Proposed value: ጥንካሬ (%)
Exact XML: `<string name="ui_strength" formatted="false">"ጥንካሬ (%)"</string>`

AOSP pairs the short visual Intensity label with ጥንካሬ and independently uses the same noun in signal and vibration strength phrases. This supports the ordinary strength/intensity noun without rewriting English Strength into Opacity. The painting application is a cross-context translation, not an exact pre-existing watercolor UI translation.

Consumer check: ClassicPaintActivity.kt:783 exposes the watercolor slider at 1..100. PaintDocument.kt:254..256 sets paint alpha to integer strength*255/100 and separately applies blur. Strength is not width. The source has literal (%) and formatted=false.

Confidence: Medium-high lexical transfer confidence; high consumer/format confidence; no native-reader or rendered acceptance.

Primary evidence:
- strength_intensity: [android-settings-en.xml:5682](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values/strings.xml?format=TEXT)
- strength_intensity: [android-settings-am.xml:2452](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT)
- strength_signal: [android-settings-en.xml:2253](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values/strings.xml?format=TEXT)
- strength_signal: [android-settings-am.xml:1002](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT)
- strength_vibration: [android-settings-en.xml:5499](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values/strings.xml?format=TEXT)
- strength_vibration: [android-settings-am.xml:2363](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT)

Limits:
- Retain (%) and formatted="false" exactly.
- Watercolor-specific naturalness remains below the confidence of direct graphics-label matches.
- No inference that AOSP already contains this full Strength (%) painting label.

Source-value SHA-256: `10071fc0ff7b2ee939efb78974a73b25390bee49e5e9595c496bde71516f06a7`
Proposed XML-text SHA-256 (including resource quote wrappers): `24e59b19c58c9b4e0d8492f43bcc83f2a24d5902f4730a99e85fd10df9d9e1e0`
Per-key decision seal: `8a8655c9355046dbd2cb4cca10f083a556c2d7758aef5eb9d9869e22fd147873`

## string/ui_tolerance: RETAIN

English: Tolerance
Proposed value: ገደብ
Exact XML: `<string name="ui_tolerance">"ገደብ"</string>`

The nonfuzzy graphics Tolerance label gives ገደብ, with Color Tolerance independently using the same noun. A limit/threshold noun fits acceptance of color differences. The adjacent replacement-help prose is useful for context but uses other wording and does not prove completely consistent Amharic terminology. No percentage or global-replacement behavior is imported.

Consumer check: ClassicPaintActivity.kt:767 exposes 0..100. ScanlineFill.kt:14..32 takes the seed color, squares tolerance.toInt(), and compares squared absolute ARGB component differences; zero requires exact equality. Lines 34..54 implement connected scanline expansion. The value is an absolute component-distance threshold, not percent.

Confidence: High for same-domain short-label support and app semantics; medium-high for standalone clarity; no native-reader or rendered acceptance.

Primary evidence:
- tolerance_label: [libreoffice-am-svx.po:16068–16072](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)
- tolerance_color_label: [libreoffice-am-svx.po:17412–17416](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)
- tolerance_color_context: [libreoffice-am-svx.po:16150–16154](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po)

Limits:
- Do not append (%) or treat a 0..100 control range as percentage.
- Transfer the short lexical choice only, not LibreOffice Color Replacer semantics.
- No need to add Color to the translation when the current English is simply Tolerance.

Source-value SHA-256: `f71041bb481fcfb42b6e8fd8c081fa11320ff3ce7ceae2634a285814dee860c3`
Proposed XML-text SHA-256 (including resource quote wrappers): `e03cc67d9bebf4fa46f953aaeb189898ebbcccda701a10006e8a09047b88ac1f`
Per-key decision seal: `615bdbb922f8e4647ec217adf3a7ce59ef7925389b72130a0926e36f1e33f11c`

## string/ui_original_size34: RETAIN

English: Original size
Proposed value: ዋናው መጠን
Exact XML: `<string name="ui_original_size34" formatted="false">"ዋናው መጠን"</string>`

The crop-page Original Size UI label supplies _ዋናው መጠን; removing only the desktop mnemonic underscore yields the proposed exact phrase. The help-heading ዋነኛው መጠን is a distinct alternative, not silently identical evidence. Neither the source label nor the candidate promises a general undo.

Consumer check: PaintDocument.kt:415..420 resets the floating rectangle width/height to retained s.image pixel dimensions around its existing center and leaves rotation unchanged. startMovingSelection at 319..325 can checkpoint and lift pixels first. ClassicPaintActivity.kt:758..760 subsequently fits the viewport. This is not restoration of location, rotation, all edits, or a 100% zoom command.

Confidence: High direct UI lexical support and verified consumer semantics; no native-reader or rendered acceptance.

Primary evidence:
- original_size_label: [libreoffice-am-cui.po:8913–8917](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)
- original_size_alt: [libreoffice-am-help01.po:23320–23327](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)

Limits:
- Retain formatted="false".
- Preserve the exact ui_original_size34 key, not another Original size resource.
- Native preference between attested variants and rendered button fit remain unverified.

Source-value SHA-256: `097c5b7689bb87ac95e60328a1ef7d486461f4fb352178189f2ae2d0ec467184`
Proposed XML-text SHA-256 (including resource quote wrappers): `485bbce47a52af47e428bcd2f4805f041e7c847b3cd0085edddf6af02a54bee4`
Per-key decision seal: `195af77a6a6601c851efb85c2e913a04b4b82951e1e7a2bee3831e0749550b5c`

## string/ui_lock_proportions: HOLD

English: Lock proportions
Proposed value: ተመጣጣኝነት መጠበቂያ
Exact XML: `<string name="ui_lock_proportions">"ተመጣጣኝነት መጠበቂያ"</string>`

The candidate is a contiguous phrase in same-function LibreOffice explanatory prose, and maintaining proportionality matches the feature. However, extracting this nominal phrase does not by itself establish a clear standalone on/off checkbox label. I cannot confidently endorse its checkbox-state idiom from these records alone. This is an evidence/idiom hold, not a finding that the phrase is grammatically wrong, and not a blanket rule requiring every new translation to have an exact full-phrase precedent.

Consumer check: ClassicPaintActivity.kt:761..764 toggles lockSelectionAspect. PaintCanvas.kt:617..642 uses initialSelectionRect for the current gesture. SelectionGeometry.kt:28..60 scales both current dimensions together for corner and edge drags. It preserves the current gesture-start ratio, not necessarily the source-image ratio, and does not freeze movement, rotation, or size or repair prior distortion.

Confidence: High consumer meaning; medium compositional semantic support; insufficient independent confidence in the standalone checkbox idiom.

Primary evidence:
- keep_proportions_context: [libreoffice-am-cui.po:19963–19967](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po)
- keep_proportions_phrase: [libreoffice-am-help01.po:27244–27251](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po)

Limits:
- Do not automatically replace it with መጠን መጠበቂያ, whose shortened noun can suggest preserving size instead of proportions.
- The empty Keep ratio UI record is not a translation.
- The separate AOSP Aspect ratio noun is not a complete replacement for Lock proportions.
- No exact new wording is justified here; hold the proposed value without adding it to accepted coverage.

To clear hold: Obtain competent native-context review of this exact checkbox label with unchecked/checked states and resizing examples, or a reliable standalone same-function Amharic UI precedent. Confirm that it means preserve current width:height proportion while resizing, not freeze dimensions.

Source-value SHA-256: `5c66db32dfaaf528a8c9451204fae25b54546714582431ed43962b7641436f4d`
Proposed XML-text SHA-256 (including resource quote wrappers): `5cf3b18011b5153843765e7a5be513598d44b74d66cfc62cfdce30ea64f1041a`
Per-key decision seal: `5ab0f0e5657202cbad3550b3b8bc514e3289a7315ba8b37228f80a944e0b605d`

## Source gate and next action

No English defect was established. The important distinctions are preserved: Tolerance is absolute ARGB distance, Original size restores dimensions while preserving center/rotation, and Lock proportions preserves the current ratio. Do not silently rewrite the English meaning in Amharic.

The two holds need terminology/idiom evidence, not more hash checking. No replacement is justified by this bounded review. Native-reader, rendered fit, accessibility, lifecycle and broader app behavior remain untested for every retained value.

Full exact records, source and target bindings, hash definitions, exclusions and per-key decisions are in review.json. The report manifest is a byte-integrity seal, not a digital signature.
