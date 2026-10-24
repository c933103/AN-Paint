# Independent adjudication: three existing Amharic holds

Date: 2026-10-24. Scope: `ui_same_width`, `ui_same_height`, and `ui_lock_proportions` only. This is an independent AI contextual translation assessment, not a native-speaker certification, implementation, or release authorization.

## Decisions

| Key | Decision | Exact accepted display value | Contextual confidence |
| --- | --- | --- | --- |
| `ui_same_width` | Release with revision | እኩል ስፋት | High semantics; medium-high complete-label confidence |
| `ui_same_height` | Release with revision | እኩል ቁመት | High semantics; medium-high complete-label confidence, less direct attestation than width |
| `ui_lock_proportions` | Release unchanged | ተመጣጣኝነት መጠበቂያ | High semantics; medium-high complete-label confidence, with formal-register limitation |

All three prior textual holds are resolved by this adjudication. No substantive grammatical or semantic objection remains that warrants retaining one of these three holds. This does not assert that the original two sameness drafts were mistranslations. It does not remove the old decisions from the record.

The exact quoted Android XML text, element hashes, original decisions, alternatives, and per-key reasoning are in `adjudicated-values.json`. `adjudicated-values.xml` is a review artifact only, not an application-source edit or an instruction to add these values to an implementation batch.

## Authority, integrity, and method

The input dossier's manifest SHA-256 is `d113853881663749a9b02859739b1c320dae3bbbec5fd80295d3426ee67d5b35`. All 49 listed payload files match that seal. The complete dossier remains unchanged.

The source binding is AN-Paint commit `66be61df27c5359bffc32d56db21f3949899f873`, tree `870c5a584120d92710be516af0dc3b3847b183d9`. I independently recomputed SHA-256 and Git blob SHA-1 for all 16 complete supplied project files and matched their supplied tree entries and sizes. This verifies those supplied bytes, not a new remote-head refresh by this reviewer. Each of the three exact English values and each proposed quoted XML value was independently hashed; all three target keys remain absent in the supplied Amharic production catalogue.

I read the exact previous hold reasons and release conditions, the new recommendations, complete relevant source contexts, the new primary UI records, preserved earlier records, and the primary grammar's relevant sections. All 11 selected PO records match their complete local file line ranges and are nonempty, nonfuzzy, and nonobsolete. All 12 lexical source snapshots match their recorded hashes; all six with new GitHub blob bindings reproduce those blob IDs. Both new controls are actual `GtkCheckButton` objects with exact matching translation contexts, not assumed control types inferred from label text.

I also reopened the primary grammar successfully on the public web. A separate web open of the pinned Writer PO returned a cache miss. That outcome is neither a denial nor evidence of an empty source; the complete supplied Writer bytes are independently Git-blob-verified and sufficient for this review. No additional GitHub retrieval is claimed.

The evaluation is of each complete target phrase in the actual consumer context. Exact whole-caption corpus matching and native-reader certification are not universal release prerequisites. Conversely, source-code semantics, a dictionary component, or a similar UI string alone cannot establish idiom. The findings below explain the productive adaptation and the remaining empirical limits rather than treating attestation as an automatic pass.

## 1. Same width: release with revision to እኩል ስፋት

### What the old hold actually said

The old value was `ተመሳሳይ ስፋት`. The previous review accepted lexical and structural plausibility but lacked enough assurance that the short full label conveyed one equal/common width rather than a merely similar width. It expressly did not establish mistranslation and did not require an exact corpus match. Its release condition required complete-phrase assessment in both toolbar-opener and dialog-title uses, with exact shared width and individually proportional cropped heights. The equal-width alternative was preserved but not accepted solely by changing the modifier.

### What changes the evidentiary position

The new Writer record at `source/am/sw/messages.po`, lines 13960–13964, contains the complete control **“Equal width for all columns” → “እኩል ስፋት ለሁሉም አምዶች”**. The exact candidate is its intact initial dimension phrase. The adjacent tooltip at 13966–13970 and another width-control explanation at 13084–13088 bind it to numerical equality of widths. The core UI at immutable blob `1705f692e769dc5b1223387fa9427c02099e847a`, lines 248–258, binds the first record to an actual checkbox and its accessibility description. This is new full-phrase and control evidence, not the old Equalize action relabeled as new.

The grammar corroborates bare nominal phrases and modifier-before-noun order. It does not independently establish UI familiarity or endorse this particular expression. [Primary grammar, §§2.2–2.3, printed pp. 23–24](https://web.stanford.edu/group/cslipublications/cslipublications/TLS/TLS9-2005/TLS9_Beermann_and_Ephrem.pdf).

### Complete-label judgment

`እኩል` modifies the width extent `ስፋት`; the phrase names the equality property. Removing the column-specific scope phrase does not remove or change the equality relation. It produces a coherent caption for configuring common width, with the dialog introduction and separate Apply-to-all control providing the scope. This app's toolbar use is an opener, so the absence of an immediate-action imperative is appropriate; the same noun phrase naturally names the dialog's subject. It does not announce that normalization has already occurred.

The phrase denotes equality of the named width, not equality of width with height, equal area, file size, or whole-image shape. Applying the setting to two crops with different ratios leaves their resulting heights different. That is compatible with the full target phrase, not merely with the word for width.

The new same-height prose and similarity-search record show that the old modifier has actual same/similar polysemy. They do not prove the old draft wrong. I prefer the equality wording for this exact scalar operation on positive contextual grounds, not to manufacture an English defect or to erase valid lexical variation.

Decision: **release with revision**, not release of the old draft. The original draft and alternative history remain preserved.

## 2. Same height: release with revision to እኩል ቁመት

### What the old hold actually said

The old value was `ተመሳሳይ ቁመት`. The earlier review noted that AOSP supports this image-height noun whereas the LibreOffice height record used `እርዝመት`. It lacked sufficient full-label assurance about exact common height rather than similarity or vertical alignment. It required evaluating both opener and title and preserving, rather than silently flattening, the real height-word variation.

### What is new, and what is not

The new equal-width control supplies the complete productive equality-plus-dimension construction. The primary grammar supports its order and bare nominal form. The new Writer same-height passage at 13246–13250 preserves positive evidence for the previous same/length wording, rather than establishing that it was erroneous.

The AOSP image-height noun at Gallery2 Amharic XML line 129, with the English media-height context at lines 303–304, is prior evidence. The previous Equalize Height action at LibreOffice UI PO lines 23476–23484 is also prior evidence and genuinely uses a different noun. Neither is presented as newly found. No exact standalone `እኩል ቁመት` control was established in this bounded research.

### Complete-label judgment

The accepted phrase applies equality to an image's vertical extent. Replacing the bare width noun in the supported construction with the established bare image-height noun yields a normal modifier-plus-noun phrase without a new possessive, personal, definite, or object relation that would require a different construction. This is productive translation, not a claim of verbatim corpus reuse.

The phrase is a property caption for the common-height configuration, appropriate both before the dialog opens and as its title. The image context supports extent rather than a person's stature, and the named scalar height together with the numeric dialog distinguishes equal height from matching y-coordinate or aligning objects. No alignment or position expression is introduced. Common-height application allows each width to follow its own crop ratio; the complete phrase makes no claim that widths, shapes, or aspect ratios match.

The precise equality modifier addresses the old same/similar concern. The whole-label assessment and axis/control analysis address the old concern that acceptance of a noun alone was insufficient. This is not an inference that every substitution into an attested pattern is automatically idiomatic: here the two heads are parallel scalar dimensions in the same image domain and the same opener/title construction.

Decision: **release with revision**. `እርዝመት` remains a documented alternative lexical family; its existence is not a defect in the selected image-height noun. Confidence is medium-high rather than high for complete-label idiom because the exact candidate lacks direct standalone attestation and native comprehension has not been measured.

## 3. Lock proportions: release unchanged as ተመጣጣኝነት መጠበቂያ

### What the old hold actually said

The previous review already found that preserving proportionality matched the consumer and that the exact candidate occurred inside same-function explanatory prose. It did not find the phrase grammatically wrong. Its unresolved point was the transition to a clear standalone on/off checkbox label. Its stated unblock paths were contextual native review or reliable standalone same-function Amharic UI precedent, with the interpretation remaining current-ratio preservation rather than frozen dimensions.

### What changes the evidentiary position

The newly verified Impress photo-album record at `source/am/sd/messages.po`, lines 9043–9047, translates **“Keep aspect ratio” → “የ መጠን አንጻር መጠበቂያ”**. The core UI at immutable blob `874a8ceca99b1a17f0923cd6778cc76a5e258c4f`, lines 340–348, makes this an actual checkbox, not just a help heading or prose fragment. This directly supports a nominal preservation construction as the stable label of a selectable aspect-ratio option.

The new phrase is not identical to the candidate and is not adopted as a replacement. It resolves the specific register/control-type gap together with, not instead of, the prior exact contiguous phrase in symbol width/height resizing prose at shared help PO lines 27244–27251 and the object-resizing tooltip at cui PO lines 19963–19967. A single translation ecosystem is not multiple independent native judgments.

### Complete-label judgment and both states

The full candidate combines the property proportionality with a preservation-function noun. In the existing resizing sentence, removing the symbol-specific possessor and the following when-clause leaves that coherent function name; it does not turn a finite statement into a fragment falsely asserting the current checked state. The new checkbox precedent establishes that the preservation-function form can label an option, while the more specific proportionality noun distinguishes the option from keeping an absolute size.

- Checked: the named preservation function is enabled; a current 2:1 selection retains that relation during resizing.
- Unchecked: that function is disabled; width and height can change independently. The label remains the option's name rather than a statement that it is currently active.

This is appropriate for both rectangle and free-form selection tool options. It does not promise restoration of an imported image ratio after prior distortion. It does not claim that size, position, or rotation are frozen. The exact consumer applies the lock to the gesture-start rectangle, which is the relation a user is presently preserving.

The shorter size-preservation alternative remains less explicit, and the new longer aspect-ratio wording is not established as clearer. No rewrite is warranted merely to use a corpus-identical checkbox string. The accepted candidate's full relation is semantically appropriate, its nominal label construction has relevant on/off precedent, and no remaining concrete grammatical or semantic defect is established.

Decision: **release unchanged**. This is a new evidence-backed adjudication of the old hold, not a claim that an exact standalone target or native review was newly obtained. The phrase is comparatively formal; reader familiarity remains an empirical limitation, not an indefinite textual veto.

## Consumer verification and limits

The normalization labels open the appropriate axis dialog from `AssemblyActivity.kt` lines 97–98, and the dialog reuses them for its title at `NormalizeImagesDialog.kt` lines 37–38. The separate positive-button handler at lines 77–82 performs the application. `ImageAssembly.kt` lines 24–32 computes the other dimension from each crop and lines 123–124 operate over all inputs, not only placed thumbnails. The common-width and common-height examples in the dossier follow these formulas. I treated them as explanatory arithmetic, not executed tests.

The proportions checkbox is bound at `ClassicPaintActivity.kt` lines 752–764. `PaintCanvas.kt` lines 617–642 uses the gesture-start rectangle and routes the aspect constraint only into resizing, while movement and rotation have separate cases. `SelectionGeometry.kt` lines 28–60 applies one scale to both current dimensions for locked corner and edge resizing. A hypothetical current 200×100 selection resized to width 300 therefore has height 150 under a ratio-preserving operation; this is a mathematical illustration, not an observed gesture or a claim about a particular arbitrary pointer trajectory.

No English defect is established for any of the three keys. The translations preserve the existing English operation rather than changing it. There is therefore no English rewrite or cross-language edit flag to initiate from this adjudication. If a future product decision actually changes the English operation, that remains a separate source-first change with affected translations reviewed afterward.

No native-speaker consultation, empirical comprehension study, spoken accessibility check, Amharic font/line-wrap/fit inspection, lifecycle exercise, Android build, runtime test, CI run, deployment, or release occurred. These are ordinary downstream implementation/UI-verification limits; this textual acceptance must not be represented as those checks passing. Source/extraction/hash/XML verification is not app testing.

## Reconciliation, scope, and preserved disagreement

The supplied current programme baseline is **91 ready, 17 held, 0 implemented**. These decisions move three existing held keys to textually ready, yielding **94 ready, 14 held, 0 implemented when the parent reconciles the ledger**. They do not add new unique reviewed keys, begin a new group, change the other eleven original holds, or change the three separate selection-tool holds. The historical 14-hold ledger remains historical evidence, not a file to overwrite as if these results had always been known.

The pending implementation batch remains **90 values**. The separate newly ready Eyedropper and these three resolution outcomes remain outside that requested batch until its scope is explicitly settled. Textual readiness is not implementation authority. No Work-side task was started or resumed; no external action, production edit, build, CI, remote publication, or release was performed in this review.

The exact previous decisions and release conditions survive in `prior-held-records.json` and again per key in `adjudicated-values.json`. All prior and newly supplied alternatives are retained. This review disagrees with continuing the three holds on the enlarged evidence; it does not rewrite the earlier reviewers' actual conclusions or portray their earlier uncertainty as proven error. There is no additional dissent invented on behalf of a native reader or other reviewer.

## Source navigation

`sources.json` contains complete immutable source locators, hashes, line references, and bounded evidence. Complete upstream source bytes remain in the sealed input dossier, not bulk-republished in this output. Principal references:

- [Writer Amharic equal-width and same-height records](https://github.com/LibreOffice/translations/blob/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/sw/messages.po#L13960-L13970).
- [Impress Amharic aspect-preservation checkbox](https://github.com/LibreOffice/translations/blob/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/sd/messages.po#L9043-L9047).
- [Prior proportion-preserving resizing phrase](https://github.com/LibreOffice/translations/blob/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po#L27244-L27251).
- [AOSP Gallery2 image-dimension catalogue](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml).
- [AN-Paint normalization dialog](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L17-L82).
- [AN-Paint selection geometry](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/SelectionGeometry.kt#L28-L60).
