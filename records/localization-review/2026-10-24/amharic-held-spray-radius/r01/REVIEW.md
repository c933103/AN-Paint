# Independent adjudication: Amharic Spray radius

Date: 2026-10-24

## Decision: RELEASE UNCHANGED

Clear the terminology hold for **string/ui_spray_radius_px** and accept **የመርጫ ራዲየስ (px)** as the exact Amharic candidate for implementation. The value is unchanged. This is a bounded linguistic-review decision, not an application release, implemented translation, rendered-UI pass or native-reader certification.

Overall confidence in the complete caption: **medium**. Confidence in the geometric meaning and radius component is high; confidence in the spray-device noun and productive grammatical construction is medium-high. The remaining uncertainty concerns preferred technical idiom, not an identified mistranslation.

## What the original hold lacked, and what now resolves it

The [original review](https://github.com/c933103/AN-Paint/tree/0ccbec849aefa83b1fe4e4129fead677699fe9cf/records/localization-review/2026-10-24/amharic-size-controls/r01) had evidence for the radius component but no eligible spray record in its bounded software corpus. It did not find the candidate wrong. Its proposed clearance routes were same-function graphics terminology or competent native-context review. Neither of those events is claimed here: this adjudication accepts a different sufficient route, combining reliable lexical usage, productive grammar and the verified consumer context.

The reviewer independently examined the Ministry of Finance annex page images. **መርጫዎች እና ኖዝሎች** corresponds to “Sprayers and Nozzles”; **መርጫ ሆዝ** corresponds to “Spray Hose.” Together they establish the exact spray-device component, including its uninflected use in a compound. They are one institutional authority, not two independent endorsements. The agricultural hardware context supplies vocabulary, not digital-painting terminology. [Annex page 39](https://www.mofed.gov.et/media/filer_public/03/1d/031de9e9-a0b7-4333-b90c-d88fc5dc05e0/1064_yakaapitaale_eqaawoce_zerezere_investment_incentive_annexes.pdf#page=39), [page 108](https://www.mofed.gov.et/media/filer_public/03/1d/031de9e9-a0b7-4333-b90c-d88fc5dc05e0/1064_yakaapitaale_eqaawoce_zerezere_investment_incentive_annexes.pdf#page=108).

The reviewer also checked Leslau’s dictionary entry for **ረጨ**, which includes the spray/sprinkle sense. This is independent root-level corroboration, not an attestation of the exact instrument noun or full caption. [Concise Amharic Dictionary, printed page 46](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=47).

The grammar evidence supports a prefixed nominal modifier preceding its head, with relationships beyond literal ownership. The instrument-noun discussion supports the implement reading. Adafre independently corroborates the prenominal and possessive construction. These sources license the construction; they do not certify this newly composed term. [Leslau, section 18.1](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=66), [section 50.1](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=232), [Adafre, section 3](https://aclanthology.org/2004.eamt-1.6/).

The pinned LibreOffice entries and rechecked official help establish **ራዲየስ** as the geometric head; the corner-radius heading corroborates a modifier with that head. The live page and catalogue are the same linguistic authority. No untranslated entry counts as positive evidence. [Pinned catalogue](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po), [official radius help](https://help.libreoffice.org/latest/am/text/shared/01/05230400.html).

## Whole-caption judgment, not component voting

In **የመርጫ ራዲየስ**, the spray-device noun qualifies the radius head: the radius associated with the spray tool. In an image editor’s Spray-only parameter control, the relevant tool property is the radial extent of its spray pattern. That contextual relation is a productive terminology judgment. It is not presented as an exact full-phrase quotation or a proven universal native preference.

The candidate retains the measurable quantity explicitly. It does not replace radius with diameter, point width or generic size. The instrument noun does not require a physical-nozzle-dimension reading, because the active consumer is a virtual painting tool and the caption includes image-pixel units. That hypothetical reading is not a concrete unresolved defect in this context. An activity-noun alternative may be reasonable, but no evidence establishes it as clearer or more idiomatic here. The longer painting-specific alternative adds words without resolving an identified problem. Neither warrants changing this candidate.

Thus the original absent-noun evidence gap is resolved, while normal residual idiom uncertainty remains disclosed. Requiring an exact prior full-caption match or an unavailable human credential despite this sufficient composition would preserve the hold for the wrong reason. This decision does not establish a rule that component evidence automatically approves other compounds.

## Consumer and contract review

The inspected source binds the caption only to Spray, with integer range **1–100**, default **10**, and a separate sprayRadius property. The drawing function samples point centers inside an image-space disk using a square-root-scaled radial distance; each point separately has width **1**. The setting is the distribution radius, not a promise of an exactly filled disk, constant density, a strict rasterized outer edge or a hardware dimension. [Control binding](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L774-L790), [geometry](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L526-L535), [image coordinates](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L222).

The label remains a noun phrase when used in the slider description, numeric-value text, tap-to-enter description and dialog title. Those uses do not require an imperative, and appending a numeric value does not change the quantity being named. Their actual visual rendering and spoken output were not tested. [NumericSlider consumers](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NumericSlider.kt#L54-L76).

Persistence stores the radius separately, and restoration clamps it to 1–100. A missing-value legacy fallback based on stroke width is not the ordinary control’s meaning. [State](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L48-L57), [persistence](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1602), [recovery](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/EditorDraftRecovery.kt#L72-L80).

Preserve the exact key, literal **(px)**, and existing resource attributes. The English source has no placeholders or explicit formatted override. The Amharic key is absent, so eventual implementation is an addition, not a replacement of production Amharic text. Do not modify the separate numeric or accessibility templates. No English-source defect was established. [English resource](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L387), [Amharic catalogue](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values-b%2Bam/strings.xml).

## Status and limits

This adjudication releases one existing hold to accepted/ready for implementation. Applied to the supplied baseline of 99 ready, 9 held and 0 implemented, its accounting effect is **100 ready, 8 held and 0 implemented**. The separate pending batch of 90 is unchanged. No aggregate register was edited in this review.

No Work task, production edit, application execution, build, project test, CI run, deployment or release was performed. Source identities and resource syntax were checked as review-artifact checks only. The complete caption has no claimed exact precedent, native-reader certification, rendered-fit acceptance or screen-reader acceptance. Those presentation checks remain ordinary implementation QA, not a renewed terminology hold without a concrete defect.
