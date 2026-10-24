# Five missing Amharic file-replacement labels: author drafts

Production `66be61df27c5359bffc32d56db21f3949899f873`.11 complete source copies included under source/. Five keys absent;19 prior candidates excluded.

## string/ui_new

English: New…
Proposed XML: `<string name="ui_new">"አዲስ…"</string>`

confirmReplacement first handles unsaved edits, then dimensionsDialog(false,true). No new image is created merely by opening the menu item.

Concise new-item menu label; preserve U+2026 because a dimensions dialog follows. The File menu and New image title supply the image noun.

Confidence: semantic high; UI idiom medium-high.

Independent check: Confirm short menu adjective and ellipsis; do not imply immediate replacement.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), [lo_new](https://help.libreoffice.org/latest/am/text/shared/04/01010000.html)

## string/ui_new_image

English: New image
Proposed XML: `<string name="ui_new_image">"አዲስ ምስል"</string>`

Fresh dimensions dialog title; valid Apply checks image size then document.newImage with selected dimensions. PaintDocument.newImage creates a blank background-colour image, resets document history through replace and clears savedTarget in activity.

Original noun phrase from attested new/image components, not a command. Fits the dimensions-dialog title.

Confidence: semantic high; UI idiom medium-high.

Independent check: Confirm compound title idiom; neither filename nor save action.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_load_image

English: Load image…
Proposed XML: `<string name="ui_load_image">"ምስል ክፈት…"</string>`

launchOpen(false) launches ACTION_OPEN_DOCUMENT, falling back to GET_CONTENT if unavailable. OPEN_IMAGE results call readImage(import=false), possibly select frame/page/size, then decodeImage replaces current bitmap only on success. IMPORT_IMAGE/paste is a different path.

Use open rather than the glossary verb shared by load/insert. Actual action opens an image as the current document, not a pasted floating insertion. Preserve ellipsis. Full phrase is an original contextual draft.

Confidence: semantic medium-high; UI idiom medium.

Independent check: Review contextual open-for-load equivalence; this does not assert a canonical English defect or change the key.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), [google_open](https://support.google.com/accessibility/answer/90559?hl=am)

## string/ui_keep_editing23

English: Keep editing
Proposed XML: `<string name="ui_keep_editing23">"አርትዖቱን ቀጥል"</string>`

Negative button with null callback dismisses dirty-document confirmation; no replacement/save/finish action invoked. paintCanvas.applyPending ran before prompt, so pending geometry may already be committed. Shared prompt also guards external image open and Back/exit.

Historical Android phrase supports continuing the editing activity rather than saving. Keep the prompt-dismissal meaning; no restoration or rollback promise.

Confidence: semantic medium-high; UI idiom medium.

Independent check: Independently recover/check the historical exact phrase and contemporary register; do not claim an untouched pre-prompt geometry state.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), [android_keep](https://android.googlesource.com/platform/packages/apps/Contacts/+/refs/heads/nougat-mr2-pixel-release/res/values-am/strings.xml)

## string/ui_discard_changes23

English: Discard changes
Proposed XML: `<string name="ui_discard_changes23">"ለውጦችን አስወግድ"</string>`

Neutral button directly invokes continuation: new dimensions, open picker, external-image decode, or finish on Back. It does not itself erase the bitmap or delete saved files. Later chooser/dialog cancellation can leave current document intact; no promise that recovery drafts are permanently destroyed.

Discard verb targets changes, not saved files. Indexed first-party phrase corroborates lexical components, but full-page verification remains missing. The UI choice proceeds without first saving.

Confidence: semantic high; UI idiom medium.

Independent check: Verify phrase/imperative idiom and explicit changes-versus-file distinction. No immediate or irreversible deletion claim.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), [google_discard](https://support.google.com/googleplay/android-developer/answer/13849271?hl=am)

## Limits

- No Work task, production edit, app build/test, CI, release or remote publication.
- No native-speaker, rendering, accessibility, lifecycle/runtime acceptance.
- 19 prior reviewed additions, existing12 resources, previous9-label judgments, Palette uncertainty, optional Horizontal and all holds unchanged.
- Save/Cancel generic labels and broad shared consumers excluded; source inspection of their behavior is context only, not translation acceptance.
- Indexed external phrase evidence is explicitly weaker than successful full-page reads; independent reviewer should recover or adjudicate it.
- No complete unsaved-changes prompt or surrounding hints accepted by these short-label drafts.
- Exact Android Keep editing and Google Discard changes phrases were found in indexed first-party excerpts; direct pages cache-missed/returned429. They are not claimed as fully inspected pages.
- Ellipses remain U+2026 in New… and Load image…. Production coverage remains12 present/705 missing; no accepted coverage added.
