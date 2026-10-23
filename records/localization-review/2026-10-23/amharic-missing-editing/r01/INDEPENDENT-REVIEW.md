# Independent review: six missing Amharic editing labels

Recommendation: retain all six exact draft values. No translation correction or hold is justified by the independently inspected implementation and primary lexical evidence. This is evidence-based AI review, not native-speaker certification or implementation acceptance.

```xml
<string name="ui_undo">"ቀልብስ"</string>
<string name="ui_redo">"ዳግም አድርግ"</string>
<string name="ui_cut">"ቁረጥ"</string>
<string name="ui_copy">"ቅዳ"</string>
<string name="ui_paste">"ለጥፍ"</string>
<string name="ui_select_all">"ሁሉንም ምረጥ"</string>
```

## Per-key decisions

- Undo: retain. Semantic confidence medium-high; UI idiom medium. The imperative expresses reversal rather than generic cancellation. ICT glossary entry 2688 supplies exactly ቀልብስ for Undo. In this app Undo first discards pending polygon points, staged curve, or changed trim; only when cancelPending returns false does it move document history. An unchanged trim alone does not count as a pending edit. This label must not be explained as always moving history or guaranteeing Redo of discarded unfinished geometry.
- Redo: retain. Semantic confidence high; UI idiom medium-high. ዳግም አድርግ is an explicit again-do imperative, clearly distinct from Undo and attested as Redo in glossary entry 2179. The glossary definition loosely describes repeating the last action; that definition is not sufficient evidence for the app's behavior and must not be imported. Here the command cancels pending geometry and restores the existing redo-stack snapshot. The header button requires document.canRedo. It does not replay arbitrary actions or reconstruct discarded unfinished geometry. No evidence requires replacing the attested phrase with a different synonym.
- Cut: retain. Semantic confidence high; UI idiom medium-high. ቁረጥ is a command, attested in software context by glossary entry 770. It copies the transformed selected image into the app's bitmap clipboard, then deletes the selection. Nonfloating pixels are replaced by background color; floating content is discarded. It does not crop canvas dimensions or delete a file. The glossary's CTRL-C typo is excluded, not propagated.
- Copy: retain. Semantic confidence high; UI idiom medium-high. ቅዳ is the verb explicitly distinguished from noun ቅጂ in glossary entries 702–703. The command renders the transformed selection, replaces app clipboard bitmap/credits, and leaves selected content visible. Do not substitute the noun solely to match fuzzy GTK history. No operating-system clipboard sharing is promised.
- Paste: retain. Semantic confidence high; UI idiom medium-high. ለጥፍ is the software insertion imperative in glossary entry 2007. Tool selection first applies pending work; the default document.paste argument is its own clipboard bitmap. Validation/checkpoint precede creation of a floating selection at the origin. This is neither text-caret insertion nor immediate flattening, and no cross-app clipboard guarantee follows from the label.
- Select all: retain. Semantic confidence high; UI idiom medium-high. ሁሉንም ምረጥ directly expresses the complete selection command, exactly as glossary entry 2311. Additional first-party Google Gallery documentation uses this exact UI label. This resolves the draft's concern that the singular imperative might require changing to GTK's plural/polite ምረጡ. In this app it selects the current bitmap bounds after pending/floating work is applied, not every document or menu item.

## Command register

All six form a consistent direct imperative set. Existing Amharic ui_edit_background already uses the direct imperative ለውጥ, so the proposed register is not an obvious departure from every current app command. This is a local consistency observation, not a newly established app-wide style policy. GTK's historical Select all plural/polite variant does not compel a register change. Action labels need not be rewritten into explanatory sentences, and behavior caveats belong in the review, not added to the translation.

## Source, consumers, and independent provenance

- Target commit: 66be61df27c5359bffc32d56db21f3949899f873. Fresh independent GitHub Git-commit lookup establishes root tree 870c5a584120d92710be516af0dc3b3847b183d9. A separate recursive tree lookup returned truncated=false and matched all eight path-to-blob bindings. This verifies the pinned commit, not perpetual branch freshness.
- Fetched all eight blobs independently through GitHub and materialized complete UTF-8 bytes. Recomputed Git blob SHA-1 and SHA-256 match every source-bindings.json entry, including exact file sizes. All four input MANIFEST file digests pass. English and proposed XML-text hashes pass for all six rows.
- Exact canonical English values are Undo, Redo, Cut, Copy, Paste, Select all. All six exact keys are absent from values-b+am/strings.xml. Canonical catalogue has 720 containers, three explicitly nontranslatable, therefore 717 translatable; Amharic has 12, leaving 705 missing. No production resources changed.
- ActionButton.kt: EditIcon maps all six IDs; ActionButton uses icon.label for contentDescription and LocaleTooltip. ClassicPaintActivity.actionIcon also shows that label in the help toast.
- ClassicPaintActivity.kt: lines 579–584 instantiate five header commands; lines 719–721 establish Undo/Redo enabled-state distinctions. Edit menu line 848 binds Select all. panelButton lines 552–556 supplies visible text, contentDescription and tooltip. Ctrl+A line 1060 invokes selectAll. Inspected the calls at lines 917–922 and 1030–1043.
- PaintCanvas.kt: hasPendingEdit line 73, selectTool lines 153–157, applyPending/cancelPending lines 443–457 confirm pending-geometry handling and tool-transition commits.
- PaintDocument.kt: undo/redo and moveHistory lines 230–245 restore pixel/credit snapshots and clear selection; floating content is finished before saving the reverse-direction snapshot. select, transformedSelectionImage, copy/delete/cut/paste, eraseSelection and finishSelection confirm the selection semantics above. In particular, “committed history only” distinguishes redo history from discarded pending geometry; it must not falsely imply floating selections are never captured by history transitions.
- UiText.kt and LocaleText.kt were inspected as shared resolution plumbing. These labels introduce no placeholders, plurals or extra punctuation. Their surrounding hints and mixed-language composed UI are not accepted by this review.

No English-label defect identified. If a source defect is subsequently established, correct English and flag affected translations across all languages before reviewing those translations, as requested. The glossary's unrelated definition/shortcut defects are not AN Paint English-source defects.

## Primary lexical evidence and limits

1. ICT Development Office / Ethiopian Languages Research Center, Translation of ICT Terms into three major Ethiopian Languages, original authored glossary on a third-party mirror: https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf . Independently read entries 702/703 (printed p59), 770 (p65), 2007 (p173), 2179 (p189), 2311 (p201), 2688 (p228). Text extraction confirms all six spellings. Two attempted page screenshots returned cache-miss errors; visual PDF verification remains unavailable. Publication date not verified.
2. Google Android Help, Gallery: https://support.google.com/android/answer/9361143?hl=am . Independently opened the first-party page; its multiple-selection instructions explicitly use ሁሉንም ምረጥ as the UI label. This is supporting register evidence, not proof of this app's runtime behavior.
3. GTK historical catalogue: https://github.com/GNOME/gtk/blob/4ba83ab573ee1f0f364f52d7c4380cfd8f4bdd30/po/am.po . Independently fetched; all six stock-label entries are fuzzy. Cut/Paste match; Undo/Redo alternatives, Copy noun, and Select all plural/polite are historical comparison only, not accepted contemporary translations. Mnemonic markers are not imported.

No implementation, application build/test, CI, publication, Work-side task, native-speaker assessment, font/rendering/layout test or screen-reader certification was performed. Existing twelve resources, prior drawing-label decisions, Palette hold, optional punctuation question, and full Help remain separate and unchanged. Review result: six retain, zero correct, zero hold; zero implemented.
