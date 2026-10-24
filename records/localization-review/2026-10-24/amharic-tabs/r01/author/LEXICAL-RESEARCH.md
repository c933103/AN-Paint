# AN Paint: Amharic top-level panel terminology

Research date: 2026-10-24. Research-only candidate assessment, not native-speaker review or implementation approval.

## Scope and result

Source inspection supplied by the parent establishes visible order **View, Draw, File, Edit, Color**. Selecting a tab changes the active panel, expands the sidebar and refreshes controls; it does not itself execute drawing or editing. The Draw panel contains drawing, selection and insert tools, not lottery/random-draw functions. View controls navigation, grid, cursor, language and fullscreen, not a command to look at a particular object.

An internally consistent, directly attested LibreOffice-style candidate set is:

| Source | Key | Candidate | Function/part-of-speech assessment | Confidence |
|---|---|---|---|---|
| View | ui_menu_view | መመልከቻ | Nominal/instrumental viewing/display category, not an imperative | High attestation; medium-high AN Paint fit |
| Draw | ui_draw26 | መሳያ | Nominal/instrumental drawing-tools category, not lottery draw and not an instruction to draw now | High drawing-domain attestation; medium panel-label fit |
| File | ui_menu_file | ፋይል | File noun/loanword, appropriate document-actions category | High attestation and fit |
| Edit | ui_menu_edit | ማረሚያ | Nominal/instrumental editing category, not a direct edit command | High attestation; medium-high panel fit |
| Color | ui_colour_tab23 | ቀለም | Color noun, covers foreground/background/palette controls | High attestation and fit |

These are candidates, not uniquely correct translations. Category semantics favor nominal labels, but do **not** prove that established imperative-form menu labels are wrong. Source ecosystems differ. No width/rendering or native review was performed.

## Direct primary-source evidence

1. **File**: LibreOffice Template Manager help, menu-bar instructions contain the exact fragment `ፋይል - አዲስ - ቴምፕሌቶች`. This establishes File as an actual menu ancestor, not merely a noun in explanatory prose.
   https://help.libreoffice.org/latest/am/text/shared/guide/template_manager.html?DbPAR=SHARED

2. **Edit**: LibreOffice View options help uses exact menu-path fragment `ማረሚያ - ኮፒ/መቁረጫ /ማስገቢያ`. This is direct Edit-menu usage. The same page's heading is `መመልከቻ`.
   https://help.libreoffice.org/latest/am/text/shared/optionen/01010800.html
   Additional Edit heading with corresponding English description: https://help.libreoffice.org/latest/am/text/shared/01/06130000.html

3. **View**: LibreOffice Calc View options page is headed `መመልከቻ`; the localized settings navigation terminates in the same label. The settings control what spreadsheet-window elements are displayed. A separate registered-databases page also uses that term in the View → Data Sources navigation.
   https://help.libreoffice.org/latest/am/text/shared/optionen/01060100.html
   https://help.libreoffice.org/latest/am/text/shared/optionen/01160200.html

4. **Draw**: LibreOffice's drawing-toolbar page is headed `የ መሳያ ተግባሮች ማሳያ` and describes opening the toolbar for shapes, lines, text and callouts. The short candidate is the drawing-category component, not a claim that this page has a standalone top-level Draw tab. LibreOffice also localizes its Draw application name with this component.
   https://help.libreoffice.org/latest/am/text/shared/02/01140000.html
   https://help.libreoffice.org/latest/am/text/shared/guide/start_parameters.html

5. **Color**: LibreOffice Image submenu help contains exact heading `ቀለም`; its English description says it opens the Color toolbar for editing object properties. This closely matches category navigation rather than an immediate coloring action.
   https://help.libreoffice.org/latest/am/text/shared/menu/submenu_image.html

## Terminology divergence and alternatives

**ICT Development Office / Ethiopian Languages Research Center glossary** (primary-authored document, accessed through a third-party mirror):
https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf

- Printed p85, entry 1009, draw tool: `መሳያ መሰሪያ`.
- Printed p85, entry 1010, Drawing: `ስእል`; definition is “Name of toolbar in Word, Excel, PowerPoint.” This is a directly relevant nominal alternative for a drawing-tools panel. Do not silently normalize its exact spelling to a different Ethiopic sequence when quoting.
- Printed p88, entry 1049, Edit: `አርትእ`, defined as changing something. This entry is action-oriented and does not by itself establish the best panel noun.
- Printed p232, entry 2739, View: `ትይታ`, accompanied by a derivational explanation; other compound entries elsewhere use the more familiar-looking `እይታ`. This is genuine terminology variation, not grounds to assert one spelling is a transcription error.
- Printed p48, entry 579, color: `ቀለም`.

The drawing and View table rows were checked against locally rendered PDF pages (`ict-page85.png`, `ict-page232.png`). The full PDF is retained for checking the other entries. The mirror is not the original institutional publisher URL, so provenance should be described accurately.

**Microsoft Amharic style guide**, printed p39:
https://download.microsoft.com/download/6/2/a/62a993f1-d3b2-4f28-b3e7-22965eb91426/amh-eth-styleguide.pdf

Exact English excerpt: “Typically, main menus should be a noun or a Verb (infinitive or imperative).” The guide distinguishes nominal and verbal forms, and its following page discusses imperative commands separately. This supports selecting a form based on UI function, while not banning imperative menu labels.

Important extraction warning: search-rendered Amharic examples disagree with the downloaded PDF's visible p39, while `pdftotext` returns corrupted Ethiopic sequences. In particular, do not cite the search rendition's View pair as exact PDF text. The p39 image visibly separates noun and imperative rows, but this report intentionally does not promote an uncertain transcription into a candidate. Search output for p45 reported Edit `አርትዕ` as a menu; because of the demonstrated extraction problem, a local p45 rendering confirms the Edit-menu example, but the researcher cannot confidently resolve the exact final Ethiopic glyph against the conflicting extraction. Do not use that spelling as verified evidence. Prefer the directly verified LibreOffice candidate ማረሚያ for this draft. The earlier preliminary finding should be read with this correction.

## Decision guidance

- The five LibreOffice-derived terms above are a defensible consistent set for an evidence-backed draft inventory.
- `ስእል` is an attested drawing-toolbar alternative, but may emphasize the drawing/image noun rather than the tool family. `መሳያ` is therefore the provisional tool-panel preference, not a linguistic verdict.
- Keep View's viewing/display category separate from imperative forms meaning show/look, and Draw separate from chance/lottery senses.
- If the inventory already uses another established label (especially Edit), do not replace it solely on a noun-versus-command argument. Compare its exact form, lexical source and intended UI convention.
- Native review remains needed to settle naturalness, dialect/style preferences, and the nominal Edit/View alternatives. No native approval is claimed here.

## Retrieval status

LibreOffice HTML and glossary web text were accessible. Some guessed LibreOffice pages and Android source pages returned cache/access errors through web retrieval; these were tool-fetch failures, not user denials. Microsoft's PDF failed web open because of its octet-stream content type, then downloaded successfully through curl and was rendered locally. No remote writes, build, implementation or external task was performed.

Files: this report; original Microsoft PDF; its extracted text (explicitly unreliable for Ethiopic); Microsoft p39 and p45 images; SHA256SUMS for both original PDFs; mirrored ICT/ELRC PDF; ICT/ELRC p85 and p232 images. URLs containing `/latest/` are mutable; the retrieval date above is part of this record.
