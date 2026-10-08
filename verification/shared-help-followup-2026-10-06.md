# Bounded shared-help corrections, 6 October 2026

This is a new, narrowly scoped source-backed correction. It does not reinstate prior withdrawn completion claims or close the full localization recheck.

## Changes

The integration change contains 10 XML files, 21 string values and 34 exact replacement fragments:
- Default English and seven scoped English overrides (en-001, en-AU, en-CA, en-GB, en-IN, en-SG, en-US): clarify that the filename star follows unsaved drawing changes; Export as and Save and share preserve the Save destination and dirty state; tray dimensions include Same width/Same height adjustment; a memory warning replaces the size chooser when even a tiny output cannot fit.
- Malay and Indonesian: apply the same behavior corrections and restore Irasutoya/Openclipart plus the localized Use image route in the retained legacy import passage.
- Malay only: correct two references to the actual File command, Gabungkan imej, while preserving Gabungan imej as a workspace noun.

The retained legacy key is ui_the_arrow_on_the_left_directly_below_the. Current main help calls ui_help23. The assembly-help key ui_add_up_to_20_images_with_android_s is active. Only these bounded passages were checked; this does not establish that the complete legacy manual is current.

## Source evidence

The reviewed integration baseline is 8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5.
- [Save/export actions and saved-state handling](https://github.com/c933103/AN-Paint/blob/8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1235-L1255)
- [Tray dimensions](https://github.com/c933103/AN-Paint/blob/8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L134-L157) and [normalization calculation](https://github.com/c933103/AN-Paint/blob/8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L20-L30)
- [No-size-fits warning branch](https://github.com/c933103/AN-Paint/blob/8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L277-L310) and [renderer limit](https://github.com/c933103/AN-Paint/blob/8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyRenderer.kt#L36-L49)
- [Import provider menu](https://github.com/c933103/AN-Paint/blob/8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L844-L851), [localized gallery action](https://github.com/c933103/AN-Paint/blob/8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L106-L123) and [Malay command caption](https://github.com/c933103/AN-Paint/blob/8dfd0dc6ce6ed5ec717778c59dcfde4762a866e5/Paintroid/src/main/res/values-ms/strings.xml#L97)

## Validation and limits

Before publication, all 10 current target blobs were rechecked against the reviewed baseline on every affected original branch and integration. Local XML parsing passed; keys, attributes, non-target values, format tokens, literal percent counts and Android newline/quote escapes are unchanged. Exact raw fragments preserve existing entity and escape spelling. The whitespace check is clean. All 10 uploaded XML blobs match the local proposed Git blob hashes.

No new AAPT2, full host suite, Gradle/lint, emulator, screenshot, accessibility or physical-device result is claimed by this report. New automatic CI results must be read at the corresponding new head; earlier green runs are not substituted. Linguistic proofreading is bounded, not native-speaker certification.

The 475-row/evidence recheck, other scoped-language equivalents, full latest-conversation reconciliation, wider semantics, native/script rendering, typography, source-access blockers and credit lifecycle remain separate open obligations. No rare-language content was guessed. The other 81 locales remain outside this task. No merge, deployment or draft-state change is included.

## Original-branch propagation

Default-English changes belong on all original PRs below. Malay/Indonesian overrides are scoped to PR3; the seven English overrides are scoped to PR7. Resource parity is not semantic acceptance.

- PR2: [published correction 1c12006da](https://github.com/c933103/AN-Paint/commit/1c12006da3dd13641d70e79a6d518d01eb3676e4)
- PR3: [published correction 604debeb1](https://github.com/c933103/AN-Paint/commit/604debeb135ed556b426b93bd571e8e9e13dcd14)
- PR4: [published correction 8510da795](https://github.com/c933103/AN-Paint/commit/8510da795377a9ebee0204201a620d0aff84c9f1)
- PR5: propagation pending; last verified head 01d73123e9b1415ddcfb15550e62ec46349b65b6
- PR6: propagation pending; last verified head f776005434b555f9afb23efb8f2ba72f2d8ac499
- PR7: [published correction 10c7578df](https://github.com/c933103/AN-Paint/commit/10c7578dff45aba93e2b79a520f2eb9c919c7a76)
- PR8: [published correction e29c8d367](https://github.com/c933103/AN-Paint/commit/e29c8d36749420a2e5aae22f08bc9774f32abd9f)
- PR9: propagation pending; last verified head bc79aab6edc6e20b94beaf43f6dac701182d0b7e
- PR12: propagation pending; last verified head 5b2a421a6effb5314e42e913c31eddfa7ad0e855
