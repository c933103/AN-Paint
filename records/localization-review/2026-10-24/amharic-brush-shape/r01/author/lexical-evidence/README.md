# Amharic brush/shape lexical research, 2026-10-24

Scope: seven original short UI drafts for AN Paint. Research only: no product-source edits, Work tasks, publication, builds, CI, or release. None of these drafts represents native acceptance.

## Proposed drafts

- Round: **ክብ**. High-confidence lexical match: exact nonfuzzy LibreOffice line-cap record; appropriate circular marker geometry too.
- Square: **ስኴር**. High-confidence lexical match: exact nonfuzzy LibreOffice line-cap record AND square-object geometry record. This is not square-area terminology.
- Calligraphy: **ሰያፍ ጭረት**. Held original descriptive draft, approximately “diagonal/slanted stroke.” Component support only, not an established translation for calligraphy. Needs native review against repeated short chisel-like marks. No font-selection meaning intended.
- Outline: **ድንበር ብቻ**. Original “border only” phrase, with primary lexical support. Explicitly excludes fill and avoids document-outline hierarchy.
- Solid fill: **መሙያ ብቻ**. Original behavior-based “fill only” phrase. This intentionally emphasizes no outline rather than translating “solid” word-for-word. Alternative **ሙሉ መሙያ** has closer lexical form but less explicit behavior contrast. Neither full phrase is primary-attested here.
- Fill + line: **መሙያ + መስመር**. Original composition of primary graphics nouns; ASCII + preserved. Color roles remain implicit as in the English short label.
- Cursor shape: **የጠቋሚ ቅርጽ**. Original Android-style pointer + LO shape composition. Alternative **የመጠቆሚያ ቅርጽ** follows LO pointer/cursor usage. Check surrounding app terminology before final selection.

## Meaning constraints

Round and Square affect stroke caps, not joins (joins remain round), and separately name circle/square cursor-marker geometry. Cursor shape does not change brushTip or painted ink geometry. Calligraphy is Brush-only and makes repeated slanted short diagonal marks, not a font selection.

The styles must remain distinct: style0 is foreground border only; style1 is foreground interior without outline; style2 is background interior plus foreground border. A short fill label does not establish these color roles alone. Native review should compare the three choices with the actual preview/swatches.

## Evidence quality and exact locations

`sources.json` gives pinned primary-source URLs, SHA-256 checks performed in this task, and available local source paths. Existing pinned LO/Android snapshots were reused after byte-hash verification against their recorded provenance. The additional LO cui PO was fetched directly in this task from the same pinned commit.

`exact-records.json` retains exact source records and local line numbers. For PO records, fuzzy status is explicitly checked. All selected records are nonfuzzy. The full newly fetched cui PO is retained. Relevant primary locators:

- LO commit 681a7f1e79cd6e27496259dab7940c8e490059de, source/am/cui/messages.po: linetabpage|liststoreCAP_STYLE (Round, Square); optctlpage|label2 (Cursor Control); pageformatpage|liststorePageLayout (only left/right).
- Same commit, source/am/svx/messages.po: STR_ObjNameSingulQUAD (Square), STR_ObjNameSingulLINE_Diag (Diagonal line), STR_ObjNameSingulLINE (Line), STR_ObjNameSingulCUSTOMSHAPE (Shape), sidebararea|filllabel|tooltip_text (Fill), sidebararea|transtype (Solid), RID_SVXSTR_BMP46 (Dashed Downward Diagonal).
- Same commit, source/am/helpcontent2/source/text/shared/02.po: 01170101.xhp / hd_id3148912 / help.text (Border).
- Android Settings commit 7c598253ff60f06f8e6fe046f18fd88e9daa72d3, res/values-am/strings.xml and res/values/strings.xml: pointer_stroke_style, pointer_speed, show_stylus_pointer_icon, pointer_fill_style_black_button. These distinguish graphical pointer/stroke vocabulary from text-cursor assumptions.

Do not transfer LO's character Outline → ረቂቅ to this border-only control just because the English string matches. Its retained source comment explicitly says lines of a character shape. Do not infer “solid fill” from the sidebar transparency Solid record alone: it supports a lexical component, not this exact no-outline behavior.

## Search and limits

Primary web search corroborated shape vocabulary in https://help.libreoffice.org/latest/am/text/shared/menu/insert_shape.html. Searches for a primary Amharic Calligraphy brush term did not establish a reliable exact equivalent; this is a bounded negative finding, not proof none exists. The found general art/education mentions did not supply an Amharic UI term and were not used. Numeric rounding, square units, fuzzy GIMP translations, and corrupt Microsoft Ethiopic PDF extraction were not used as positive evidence.

`draft-candidates.json` supplies per-row rationale, confidence, alternatives, and holds. Complete native/contextual review and visual fit testing remain outstanding for every row; Calligraphy has an additional terminology hold. No action was denied or left with an uncertain external outcome during this task.
