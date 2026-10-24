# Amharic navigation labels: primary lexical draft dossier

Source-only original drafts for four missing AN-Paint labels. No production edits, acceptance, native-reader approval, build/CI or remote write occurred.

## Findings

- Search: ፍለጋ. Exact AOSP menu/search label, retained as a neutral shared field-hint/action form. ፈልግ is an attested imperative alternative.
- Back: ተመለስ. Exact AOSP navigation label. LibreOffice navigation ወደ ኋላ is a documented alternative. AOSP Gallery2 rear-camera “Back” is not navigation evidence.
- Copy all: ሁሉንም ኮፒ ማድረጊያ. Unvalidated original composition, not an upstream exact phrase. Generic complete text, including credits and legal/notices text. Requires fluent review for concise command register.
- Choose location…: የማስቀመጫ ቦታ ይምረጡ…. Unvalidated original composition explicitly referring to a save destination, not geographic location. Exact source Select Path → መንገድ ይምረጡ is retained as an alternative with Android-picker terminology limitations. Single U+2026 ellipsis retained in XML.

## Evidence and boundaries

sources.json gives complete copied snapshot URLs, immutable upstream pins, SHA-256 hashes and reuse provenance. These copies were reused, not downloaded afresh. exact-records.json retains full PO records with contexts/flags/line numbers and AOSP exact key-aligned raw English/Amharic records. The PO lookup strips UI mnemonic markers only for discovery; original text remains untouched. Empty translations and irrelevant senses are not positive evidence. search-limits.json bounds the search and records absence of exact Copy all / Choose location phrases in this corpus only.

draft-candidates.json documents rationale, alternatives, confidence and limits per key. proposed-values.xml is an inspectable draft artifact, not application resources. english-source-records.json is a pinned prior English snapshot; current consumer facts were supplied by the coordinating task and are not independently revalidated here. validation.json covers only source hashes and artifact structure, not linguistic approval or runtime testing.

All four remain pending independent/native Amharic review. In particular the last two must not be counted as accepted labels merely because their components have source support.
