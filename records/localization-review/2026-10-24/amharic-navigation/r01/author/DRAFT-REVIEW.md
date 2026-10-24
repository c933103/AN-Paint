# Amharic gallery/file navigation drafts

Four original drafts for independent checking. Prior 77 ready and 12 held proposals remain separate. No implementation; production stays 12 present / 705 missing of 717 translatable containers.

## string/ui_search34

English: Search

Proposed XML: `<string name="ui_search34">"ፍለጋ"</string>`

Shared gallery search action button and generic search-field hint/caption. The same noun-style label can name the field and action. Query is trimmed, limited to512characters and empty query does nothing. Provider-specific behavior: Catrobat finds text in current WebView page; Openclipart navigates to search URL; Commons searches within Blank maps; Irasutoya submits its search form or reloads home with pending query.

Qualification: Not only remote internet search or only local search; no promise of results. Irasutoya field uses a separate Search in English or Japanese key, outside scope; common Search action is still this key. Vertical visible field caption branch is not proof Amharic takes that branch.

Evidence and confidence: {"key": "ui_search34", "english": "Search", "proposed_value": "ፍለጋ", "status": "draft_only", "confidence": "moderate-high lexical; context review pending", "evidence_ids": ["android-gallery2:menu_search", "android-settings:search_settings", "android-settings:print_menu_item_search"], "rationale": "Exact AOSP Search label. Noun-style form accommodates both field hint/caption and action button, including provider web search and Catrobat in-page find.", "alternatives": [{"value": "ፈልግ", "evidence_ids": ["android-settings:locale_search_menu"], "limit": "Imperative AOSP alternative; less neutral as a shared field hint."}], "limits": ["No native-reader or screen-reader review. No claim that AOSP context exactly matches every AN-Paint consumer."], "value": "ፍለጋ"}

## string/ui_gallery_back34

English: Back

Proposed XML: `<string name="ui_gallery_back34">"ተመለስ"</string>`

Content description of arrow navigation button. Click goes back in WebView history when possible; otherwise loads selected provider home. Arrow orientation follows horizontal layout direction.

Qualification: Not Undo, not close gallery or application, not always previous page because history-empty fallback loads home. Android system back handler is separate and may exit; do not transfer that meaning to this label. No spoken/accessibility acceptance is claimed.

Evidence and confidence: {"key": "ui_gallery_back34", "english": "Back", "proposed_value": "ተመለስ", "status": "draft_only", "confidence": "moderate-high lexical; context review pending", "evidence_ids": ["android-settings:wizard_back"], "rationale": "Exact AOSP navigation command, interpreted as return/back. Suitable draft for arrow contentDescription that navigates web history or returns to provider home; not Undo or close application.", "alternatives": [{"value": "ወደ ኋላ", "evidence_ids": ["libreoffice-am-ui:L37916"], "limit": "Exact LibreOffice navigation label; alternative, not additional approval of chosen form."}], "limits": ["Gallery2 rear-camera Back is explicitly excluded as positive navigation evidence.", "Actual screen-reader announcement remains untested."], "value": "ተመለስ"}

## string/ui_copy_all

English: Copy all

Proposed XML: `<string name="ui_copy_all">"ሁሉንም ቅዳ"</string>`

Generic full-text copy command across three consumers. Gallery copies all nonblank stored document-credit texts joined with blank lines, or shows no-credit notice when empty. Save-options credits panel copies its complete supplied credit text. Legal/notices dialog copies the entire displayed text parameter, not just selected/visible viewport text.

Qualification: Not Copy all images/files, not only image-credit text, not Select all, not transfer to remote recipient. Clipboard copy requests can fail; label is not completion guarantee. Does not itself save unsaved credit-editor drafts. Complete legal text is not being translated in this group.

Evidence and confidence: {"key": "ui_copy_all", "english": "Copy all", "proposed_value": "ሁሉንም ቅዳ", "status": "draft_only_unvalidated_composition", "confidence": "medium component semantics; composed full command requires independent review", "evidence_ids": ["libreoffice-am-ui:L22435", "libreoffice-am-ui:L23636", "android-settings:select_all"], "rationale": "Original composition of attested ሁሉንም (all) and LibreOffice ኮፒ ማድረጊያ (copy operation). Generic complete-content action, applicable to both image credits and displayed legal/notices text. Does not narrow the object to images, credits, or files.", "limits": ["No exact Copy all source phrase found. Full proposed phrase is not quoted from upstream.", "Longer nominal command may be less idiomatic than an imperative; native-reader review must choose final register and brevity.", "Does not mean select all, copy all files, or copy all images."], "value": "ሁሉንም ቅዳ", "author_addendum": "See author-copy-all-addendum.json. Helper nominal proposal retained unchanged in lexical-evidence, not selected by author."}

## string/ui_choose_location

English: Choose location…

Proposed XML: `<string name="ui_choose_location">"የማስቀመጫ ቦታ ይምረጡ…"</string>`

Positive action in shared save/export/share options dialog. Validates filename, constructs SaveRequest with format/settings/name, invokes caller, then dismisses options. Caller launches Android ACTION_CREATE_DOCUMENT with MIME and suggested filename so user chooses output destination. Invalid name leaves form open with field error.

Qualification: Location means file storage destination, not geographic location/device location access. It is not Save now: destination picker selection and encoding/write still follow. Preserve U+2026. No guarantee of chooser availability or save success.

Evidence and confidence: {"key": "ui_choose_location", "english": "Choose location…", "proposed_value": "የማስቀመጫ ቦታ ይምረጡ…", "status": "draft_only_unvalidated_composition", "confidence": "low-moderate; context-explicit composition requires Amharic review", "evidence_ids": ["libreoffice-am-cui:L11921", "libreoffice-am-cui:L10126"], "rationale": "Original composition intended as choose a saving place/destination. Uses source-attested save-related ማስቀመጫ and selection imperative ይምረጡ; adding የ and ቦታ is author synthesis, not an exact upstream phrase. Explicit save qualifier avoids geographic-location meaning. Keeps single U+2026 ellipsis indicating the destination picker opens after name validation.", "alternatives": [{"value": "መንገድ ይምረጡ…", "evidence_ids": ["libreoffice-am-cui:L11921"], "limit": "Exact Select Path plus added ellipsis, but path may overemphasize technical filesystem paths and is not necessarily Android picker terminology."}], "limits": ["No exact Choose location source phrase found.", "Do not substitute geographic/GPS Location terminology based solely on English match.", "No claim that የማስቀመጫ ቦታ is an attested complete phrase in the copied corpus.", "Native-reader review should confirm grammar, register, destination meaning, and fit."], "value": "የማስቀመጫ ቦታ ይምረጡ…"}

## Scope and limitations

Copy all is generic full-text copying across gallery credits, save-panel credits and complete legal/notices text. It does not copy images/files, only a selected substring, or unsaved credit drafts. Back names a navigation arrow via contentDescription; it returns through web history or loads provider home, not Undo or app-close. Search is shared field hint/caption and button, spanning provider search and Catrobat in-page find. Choose location validates filename and opens Android create-document destination selection; it is file location, not geographic location or immediate successful saving.

No English defect established. Four strings contain no units/placeholders; Choose location retains U+2026. Broader descriptions, search-language instructions, legal text, errors and held Help are excluded. No acceptance is inferred from dictionaries or source-product translations. Composed phrases and competing label registers remain explicit for independent evaluation; absence of exact corpus match is not itself a universal rejection rule.

15 complete current source copies are supplied, with fresh develop ref/commit/tree path-to-blob binding and SHA-256 values. Bounded rescan identifies seven exact occurrences in three direct caller files. Historical discovery was rebound to current complete bytes; this is not a fresh exhaustive repository-wide search. Source66be61df27c5359bffc32d56db21f3949899f873/tree870c5a584120d92710be516af0dc3b3847b183d9. Lexical evidence records retained snapshots as reuse, not fresh upstream retrieval. Primary URLs, exact original contexts, excluded empty/non-navigation matches, alternatives and confidence remain in lexical-evidence.

No native-speaker, runtime, rendering, spoken-accessibility or whole-language certification. No production changes, Work task, app builds, CI or release. All existing holds and optional recommendations remain unchanged.
