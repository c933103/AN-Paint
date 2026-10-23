# Six missing Amharic editing commands: original drafts

Production `66be61df27c5359bffc32d56db21f3949899f873`. Eight complete files and fresh commit/tree path bindings verified.

Current translations are absent;12 present/705 missing remains unchanged. No independent acceptance or implementation.

## string/ui_undo

English: Undo
Proposed XML: `<string name="ui_undo">"ቀልብስ"</string>`

Undo / reverse the edit

ClassicPaintActivity.undoEdit first calls cancelPending; when no pending edit was discarded it calls document.undo. Pending polygon/curve/changed trim can therefore be discarded without moving the history stack. PaintDocument.moveHistory restores prior pixels/credits and clears selection.

Use the attested ICT Undo command, not a generic Cancel button label. It names reversal, without promising every pending shape can later be restored.

Confidence: semantic medium-high; UI idiom medium.

Independent check: Check the standalone imperative’s familiarity and distinction from Cancel and Redo; do not imply discarded unfinished geometry is redoable.

Lexical source: [ICT glossary](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), 2688, printed p228.

## string/ui_redo

English: Redo
Proposed XML: `<string name="ui_redo">"ዳግም አድርግ"</string>`

Do again / redo

redoEdit discards pending geometry then calls document.redo, moving the redo history entry back to undo. The button requires document.canRedo; no promise that an unfinished gesture discarded by Undo is recoverable.

The explicit again-do command distinguishes Redo from Undo. Here it reinstates committed undo history, rather than replaying arbitrary gestures or repeating the current command.

Confidence: semantic high; UI idiom medium-high.

Independent check: Confirm idiomatic command form and clear pairwise contrast with Undo.

Lexical source: [ICT glossary](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), 2179, printed p189.

## string/ui_cut

English: Cut
Proposed XML: `<string name="ui_cut">"ቁረጥ"</string>`

Cut

cutSelection first copies the transformed selected image to the app clipboard, then deletes the selection. Nonfloating selected pixels are replaced by background colour; a floating selection is discarded. It does not crop canvas dimensions.

Use the ICT clipboard command, not a crop or scissors-only instruction. The button’s selection/clipboard context disambiguates the ordinary cut verb.

Confidence: semantic high; UI idiom medium-high.

Independent check: Check conventional clipboard-cut idiom; do not add a crop, transparency or file-deletion promise.

Lexical source: [ICT glossary](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), 770, printed p65.

## string/ui_copy

English: Copy
Proposed XML: `<string name="ui_copy">"ቅዳ"</string>`

Copy (command)

copySelection renders the transformed selection, replaces the app clipboard bitmap and its credits, and leaves the visible selected content in place. No selection produces a separate explanatory message.

Use the glossary’s verb ቅዳ, not its distinct noun ቅጂ. This requests a duplicate of the selected image content; it does not imply clipboard sharing outside this app.

Confidence: semantic high; UI idiom medium-high.

Independent check: Confirm clipboard-copy imperative and avoid noun substitution.

Lexical source: [ICT glossary](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), 702, printed p59; contrast noun703.

## string/ui_paste

English: Paste
Proposed XML: `<string name="ui_paste">"ለጥፍ"</string>`

Paste

pasteSelection chooses SELECT (committing previous pending work), then document.paste uses the private image clipboard by default. It creates a floating selection at origin after validation/checkpoint; placement and later compositing remain separate. Missing clipboard content shows a hint.

The attested ICT command matches inserting previously copied image content, not physical glue or automatic placement at a text caret.

Confidence: semantic high; UI idiom medium-high.

Independent check: Confirm software-paste idiom; no system clipboard, caret or immediate flattening guarantee.

Lexical source: [ICT glossary](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), 2007, printed p173.

## string/ui_select_all

English: Select all
Proposed XML: `<string name="ui_select_all">"ሁሉንም ምረጥ"</string>`

Select all

Edit menu and Ctrl+A call selectAll: choose SELECT, then select bounds0,0,width,height of the current bitmap. Prior floating/pending work is committed through selection/tool transition. The operation does not select all documents.

The attested Select All command expresses the entire available canvas area in this editor, not every file, tool or menu option.

Confidence: semantic high; UI idiom medium-high.

Independent check: Check natural complete imperative for all canvas pixels; neither plural handling nor formatting is introduced.

Lexical source: [ICT glossary](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), 2311, printed p201.

## Limits

No English correction prerequisite identified for these six complete short labels. Explicit context limits prevent overpromising behavior. If later review establishes a source defect, English correction and cross-language flagging precede translation.

Glossary Cut shortcut typo is excluded from evidence, not propagated.
- Independent checking required for every proposed value; lexical equivalents alone are not acceptance.
- No production edits, application tests/builds, CI, release, Work task or remote publication.
- No native-speaker, rendering, layout, runtime or screen-reader certification.
- All other prior holds and optional recommendations unchanged.
- All12 existing Amharic resources and prior7 drawing candidates are separate, unchanged.
- Palette unresolved and optional Horizontal punctuation remain separate.
- Save/export/new-document flows, destructive clear/crop, format strings, plurals and held full Help excluded.

## Historical software cross-check

[GTK pinned catalogue](https://github.com/GNOME/gtk/blob/4ba83ab573ee1f0f364f52d7c4380cfd8f4bdd30/po/am.po) has fuzzy entries for all six commands. Cut/Paste match; Undo/Redo have alternate expressions, Copy uses a noun, and Select all uses plural/polite ምረጡ rather than draft ምረጥ. These historical variants are not contemporary acceptance. Independent review should check register and the Undo/Redo distinction. PDF text extraction checked the glossary; incomplete screenshot retrieval and unverified publication date remain explicit.
