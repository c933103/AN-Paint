# Independent review: five Amharic top-level tabs

Review complete: 5 retain, 0 revise, 0 hold. No implementation, acceptance publication, build, CI or release.

retain means preserve this exact candidate as evidence-supported at the stated confidence; it is not a claim of native approval, runtime acceptance or permission to implement.

Input seal: `b676ebfe81ecbc03ff8b56781bdb15acb6a0c9451460fef7bd49d4b2ebe43c90`. Source commit: `66be61df27c5359bffc32d56db21f3949899f873`; tree: `870c5a584120d92710be516af0dc3b3847b183d9`.

Integrity checks passed for 22 sealed files, all eight source blobs, all five source/candidate text hashes, and both independently downloaded PDFs. The additional exact-revision ToolCategoryButton source was also blob-verified.

## Exact decisions

### string/ui_menu_view — RETAIN

<string name="ui_menu_view">"መመልከቻ"</string>

Confidence: source semantics high; linguistic/UI fit medium-high.

Retain the established nominal viewing/display label for the View control category. Its menu and settings uses are directly attested, and the actual panel controls navigation, grid, cursor, magnifier, language and fullscreen. It must not be narrowed to a Zoom action.

Conventional software-UI register. መመልከቻ has an instrumental/nominal shape, not an instruction to look now. The competing glossary noun does not invalidate this attested UI convention.

Limit: No native naturalness ranking between this label and other attested View nouns; screen fit was not tested.

Evidence: [lo_view](https://help.libreoffice.org/latest/am/text/shared/optionen/01060100.html), [lo_view_menu](https://help.libreoffice.org/latest/am/text/shared/optionen/01160200.html), [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf).

### string/ui_draw26 — RETAIN

<string name="ui_draw26">"መሳያ"</string>

Confidence: source semantics high; linguistic/UI fit medium.

Retain መሳያ as a defensible short drawing-category label. The source tab opens the existing drawing panel without selecting a new tool or making a mark. Additional exact-revision source confirms BRUSH, SELECTION and INSERT tool families. LibreOffice drawing-bar content likewise includes selection and insertion, so the category is not limited to freehand drawing.

Nominal/instrumental drawing-domain term. It does not carry the lottery/chance sense of English draw. Using the attested component as a standalone tab is a context-based inference, not a directly observed standalone-tab translation. Do not replace it with a generic Tools label or rewrite the English source on this evidence.

Limit: Standalone tab idiomaticity is the weakest inference among the five. The glossary also attests ስእል for a Drawing toolbar; there is no evidence here that it is uniquely preferable. Native idiom and runtime fit remain untested.

Evidence: [lo_draw](https://help.libreoffice.org/latest/am/text/shared/02/01140000.html), [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf).

### string/ui_menu_file — RETAIN

<string name="ui_menu_file">"ፋይል"</string>

Confidence: source semantics high; linguistic/UI fit high.

Retain the conventional file noun/loanword. An actual File menu path supports the exact form; AN Paint uses this tab for new/open/save/export/share and related document commands, not a filing verb.

Established computing loanword in the same software-UI register as the other labels. Native-origin morphology in neighboring labels does not require replacing a conventional loanword.

Limit: No claim that the File category excludes help/about; its full source scope is retained. Runtime rendering was not tested.

Evidence: [lo_file](https://help.libreoffice.org/latest/am/text/shared/guide/template_manager.html?DbPAR=SHARED).

### string/ui_menu_edit — RETAIN

<string name="ui_menu_edit">"ማረሚያ"</string>

Confidence: source semantics high; linguistic/UI fit medium-high.

Retain the established Edit-menu label. Direct clipboard-menu evidence defeats a narrow reading as only correcting errors. It is suitable for the AN Paint editing category including selection, size, crop, transforms, inversion and clear.

Conventional nominal/instrumental software label. Do not infer that an imperative alternative would be wrong merely because a tab is a category. Microsoft permits either grammatical convention.

Limit: The cited LibreOffice path establishes conventional usage, not native preference for every image-editing context. Microsoft uncertain Ethiopic glyphs are excluded, not resolved by guessing. Runtime fit was not tested.

Evidence: [lo_edit](https://help.libreoffice.org/latest/am/text/shared/optionen/01010800.html), [microsoft](https://download.microsoft.com/download/6/2/a/62a993f1-d3b2-4f28-b3e7-22965eb91426/amh-eth-styleguide.pdf).

### string/ui_colour_tab23 — RETAIN

<string name="ui_colour_tab23">"ቀለም"</string>

Confidence: source semantics high; linguistic/UI fit high.

Retain the color noun. It matches foreground/background, swap/reset, palette and advanced color controls. LibreOffice independently uses the exact term to open the Color toolbar, a close category-navigation analogue.

Neutral color noun, not an imperative to color the image. No added singular-object or immediate-action restriction is introduced.

Limit: This does not decide the separate Palette translation. Runtime rendering was not tested.

Evidence: [lo_color](https://help.libreoffice.org/latest/am/text/shared/menu/submenu_image.html).

## Consumer and source findings

- ClassicPaintActivity.kt lines 588-599 construct exactly five RibbonTab controls in View, Draw, File, Edit, Color order and set contentDescription to the same translated caption.
- menuTitle at lines 829-832 maps the five source keys. selectTab at lines 461-464 changes activeTab, expands the panel and synchronizes it; Color additionally refreshes custom palette. It does not draw or execute an Edit/File command.
- RibbonWidgets.kt lines 193-209 explicitly implements tabs, including ActionBar$Tab accessibility class. The label is therefore both visual and accessibility category text.
- Draw contents at ClassicPaintActivity.kt lines 286-326 use ToolCategory.values; the independently retrieved ToolCategoryButton.kt lines 13-19 verifies BRUSH, SELECTION and INSERT.
- View controls are at lines 862-874; File commands at 835-846; Edit commands at 847-861; Color controls at 415-432.
- The exact English sources remain View, Draw, File, Edit, Color. No source defect or source correction is established by this review. Explanatory phrases such as drawing-category are consumer analysis, not substitute source strings.

## Boundaries

- No native-speaker review or user-preference ranking was performed. This is independent source-backed AI review.
- No application run, layout, font, truncation or accessibility-rendering test was performed. Source-level consumer inspection is not runtime verification.
- LibreOffice /latest/ pages are mutable and partially translated. Exact pertinent forms were verified in independent downloads, whose hashes and snapshots are retained; wider locale completeness is not inferred.
- Primary-authored ICT/ELRC content is hosted on a third-party mirror. Both PDFs independently downloaded byte-identically to the sealed originals.
- No whole-repository exhaustive consumer search is claimed; the displayed top-level tab consumer and its exact control path are verified.
- Microsoft Ethiopic extraction and uncertain exact Edit glyphs remain excluded. No purported repair of corrupted extracted text was used.
- The earlier 24 reviewed additions, 12 resources, Palette uncertainty, optional Horizontal and held Help are separate and unchanged. No aggregate accepted-coverage increment is made here.

Full exact values, hashes, consumer links, primary-reference snapshots and qualifications are in review.json. Independent commit/tree linkage is in independent-git-provenance.json. No production source was edited.
