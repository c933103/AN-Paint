# Independent Amharic navigation/action review

Result: **retain 4, revise 0, hold 0** at the source-only textual review gate. No implementation or production change.

Input manifest SHA-256: `8fc79af33abc5537e961f0aaed41dcdb1b885f27b8457feb2937cd1951e0f55e`.

## Exact per-key verdicts

### string/ui_search34

English: Search

Retain: **ፍለጋ**

The noun search labels an operation or field without restricting it to online search, image search, or in-page text search. It therefore covers all inspected consumers.

Established concise noun-style UI label. Prefer it to the otherwise valid imperative ፈልግ for this shared hint/caption/action resource. A noun label need not be converted to an imperative merely because some consumers are buttons.

Evidence: android-gallery2:menu_search, android-settings:search_settings, android-settings:print_menu_item_search. Source context: [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L129-L160), [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryControls.kt#L94-L110).

Confidence: high for bounded text/context fit; no runtime or native-reader certification.

### string/ui_gallery_back34

English: Back

Retain: **ተመለስ**

The return/back imperative describes backward history navigation and the provider-home fallback. It does not say Undo, close, or previous page only.

Concise singular imperative attested for an actual AOSP wizard navigation button. Appropriate text for the arrow content description; spoken delivery remains untested.

Evidence: android-settings:wizard_back. Source context: [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L123-L128).

Confidence: high for bounded text/context fit; no spoken-accessibility certification.

### string/ui_copy_all

English: Copy all

Retain: **ሁሉንም ቅዳ**

The all-object expression followed by the copy imperative preserves the complete-content scope without inventing an object such as images, files, or credits. Legal/notices and both credits consumers are covered.

ሁሉንም functions as the all/everything object and ቅዳ as the copy command. This is an ordinary concise object-plus-imperative construction, matching the short-command register of Back. The fuller nominal helper candidate is unnecessary; it is not the selected draft.

New full-phrase composition. No exact Copy all match and no prior Copy acceptance is transferred. The independent judgment is based on component roles, ordinary syntax, and all three complete-content consumers.

Evidence: android-settings:select_all, author-copy-all-addendum:ICT glossary entry 702 contrasted with 703, visually rechecked at identical PDF hash. Source context: [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L107-L110), [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt#L122-L140), [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/LegalInfo.kt#L82-L103), [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L47-L59), [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCredit.kt#L8-L22).

Confidence: moderate-high for this bounded composition; no native-reader or runtime certification.

### string/ui_choose_location

English: Choose location…

Retain: **የማስቀመጫ ቦታ ይምረጡ…**

The phrase asks the user to choose a saving/storage place. The save qualifier disambiguates the source meaning established by the actual file-destination caller; it adds no new operation. It does not request GPS/location access and does not claim immediate save success.

የማስቀመጫ ቦታ is a transparent saving/storage-place noun phrase and ይምረጡ is an attested polite/plural selection imperative. The genitive construction is not a demonstrated error or a reason to force a shorter technical path label. The result is somewhat fuller than English but faithful.

New full UI phrase; the source-product records attest components, not the full translation. Supplemental institutional prose corroborates the noun-phrase construction but is about physical storage, not software. Digital-destination fit is this review’s contextual linguistic inference.

Register advisory: This is polite/plural ይምረጡ, unlike singular ተመለስ/ቅዳ. Do not describe the set as one uniform address register. Both are conventional UI styles in the primary corpus, and no supplied project-wide rule makes this difference a fidelity error. A future uniform-register decision must be applied deliberately across the relevant labels rather than silently changing this one.

Retain exactly one U+2026. The subsequent picker follows filename validation; selection and writing still remain.

Evidence: libreoffice-am-cui:L10126, libreoffice-am-cui:L11921, supplemental:NEBE article 10, bounded noun-phrase corroboration only. Source context: [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt#L187-L201), [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1110-L1128), [inspected caller](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1092-L1101).

Confidence: moderate for full-phrase idiom and register, high for the established file-destination sense; native-reader and fit checks remain outside scope.

## Integrity and evidence boundaries

All 43 input files match the sealed manifest. All 15 complete source copies match both their SHA-256 and Git blob identities and their supplied tree bindings. The bounded rescan reproduces seven occurrences across three direct caller files. Ten snapshots were rehashed and all 63 raw extracted records match their recorded source locations. Each selected XML element parses; source and target strings have no substitution placeholders, and the single U+2026 is preserved.

The copy glossary verb/noun distinction was independently checked visually on printed page 59 of the hash-matching PDF. [ICT glossary mirror](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf). This establishes the component distinction, not acceptance of the composed phrase.

Supplemental [NEBE primary institutional prose](https://nebe.org.et/sites/default/files/Directive%20on%20Materials%20Allocation-V2-14.10.21%20%28edited%29_0.pdf), printed page 8, article 10, uses the proposed storage-place noun phrase in a physical-storage context. It corroborates construction only. It is not software terminology evidence, an exact complete label match, or a legal interpretation.

## Preserved alternative and scope

The helper XML and helper draft-candidates intentionally still contain the nominal Copy all alternative. The author record has the imperative selected value but retains some helper nominal rationale. Read it together with the author addendum. Only the exact author values above were adjudicated; helper XML must not be mistaken for the selected four-string result. No source file was changed.

- Retain means keep the exact proposed text at this source-only review gate. It is not implementation, whole-language certification, a native-speaker sign-off, or runtime/accessibility acceptance.
- Prior 77 ready proposals and 12 holds are not re-reviewed, merged into these verdicts, or changed by this report. No earlier acceptance supplies linguistic proof here.
- The complete copies are bound to supplied source commit 66be61df27c5359bffc32d56db21f3949899f873 and tree 870c5a584120d92710be516af0dc3b3847b183d9. This reviewer recomputed their identities and checked supplied tree bindings, but did not freshly query GitHub HEAD.
- The consumer rescan is bounded to the 15 supplied complete source files, not an exhaustive fresh repository-wide scan. Seven occurrences in three direct caller files were reproduced.
- The ten supplied snapshots comprise nine external lexical files and one project English file. They were rehashed, not freshly downloaded. All 63 extracted records match their supplied raw source positions.
- The ICT glossary is primary-authored material on a public mirror, not an authenticated institutional host. The matching local PDF was hashed and page 59 visually inspected; no complete PDF/page image is republished in this deliverable.
- No exact upstream full-phrase match is claimed for Copy all or Choose location. Absence in this bounded corpus is not proof of absence everywhere and is not by itself a rejection criterion.
- No human native-reader assessment, rendered-app fit check, spoken-screen-reader check, application build, CI, Work task, release, production change, or remote write was performed.
- No English-source defect was established. The source-fix/all-languages workflow therefore was not triggered.
