# ANG / NON metadata — finite author terminology follow-up M1

## Result first

**Recommend retaining the existing metadata terms, with the explicit bounded definition below, for independent review. No target-byte changes are proposed in this follow-up.** The intended meaning includes embedded structured descriptors. It never required external sidecar files, supplementary prose, or optional/disposable information. The earlier glossary failed to make those negative boundaries explicit enough.

This is a proposed semantic convention, not a dictionary claim that either historical language had software metadata. Its plausibility is **moderate**; spontaneous comprehension by present-day readers has not been measured. The short autosave clauses need no identified grammatical repair for this issue. Colour clauses are assessed individually below; accepting the glossary must not silently approve their remaining syntax or all other held values.

This M1 supplement does not edit or replace frozen author revision10, the independent review ledger, or any application resource. All unrelated holds remain untouched. It is research-assisted AI drafting, not native-human certification or source implementation.

## Binding and scope

Input: `consolidated-current-rev10-dependency-audited/terminology-dependency-audit.md` and the exact current-value ledger. Scope is **four source keys × two locales = eight cells**, not general glossary reform.

Input SHA-256:

- `current-value-recommendations.tsv`: `6e6f8ad79d3243c7e41c75e0c401abf2f23d0eb01e7ff383abfe66fb9df43eb2`
- `terminology-dependency-audit.md`: `c36bc7379a431fe16428b0e999f7069195a6180e882fcc36648870ab784a809b`

English and call sites were read from the supplied AN Paint baseline workspace, previously bound to supplied commit `96681f687671a1fdffe134a325843919c1543401` and tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`. No new claim of a locally resolvable Git HEAD is made.

## Proposed shared definition

**Metadata:** structured descriptive or control records associated with an image or saved editing state, distinguished by their function from the primary pixel content. They may describe interpretation, colour, format or saved-state structure. They may be encoded as text or binary fields, embedded in the same image file, or contained as a record in an archive alongside pixel data.

For this draft:

- ANG **`sidegewrit`**, neuter; plural **`sidegewritu`**. Its newly assigned metadata sense is **associated descriptive/control record**, with `side-` a relational supporting/accompanying metaphor, **not a locative assertion that it sits outside the file**. `hiwsidegewritu` narrows the records to colour information.
- NON **`viðbótarrit`**, neuter; nominative/accusative plural also **`viðbótarrit`**, genitive plural **`viðbótarrita`**. Its newly assigned metadata sense is **descriptive/control records additional to the primary pixel content in function**. `um liti` narrows the records to colour information.

The technical sense expressly **does not entail**:

1. natural-language prose, annotations written by the user, or a supplementary essay;
2. a distinct external file, separate document, or sidecar storage;
3. placement after the pixel bytes or at the end of a file;
4. creation later than the image;
5. optionality, harmless removability, or permission to discard the records;
6. the raw pixels themselves, a replacement image, or a recovery copy.

Thus “additional” is not “unnecessary”: autosave descriptors can be required for restoring a saved state, and embedded colour descriptors can be needed for interpreting colours correctly. The term is intended to name a functional class, not prescribe its physical packaging.

## Evidence and limits

### Historical linguistic bases

- [Bosworth–Toller `síde`, noun](https://bosworthtoller.com/27617) records the ordinary side/flank noun, including sides of objects. This establishes the base, **not** an already lexicalized medieval “ancillary data” prefix. The relational supporting-record sense in the new compound is our explicit metaphor. The separate adverb meaning widely is not the intended component.
- [Bosworth–Toller `ge-writ`](https://bosworthtoller.com/16905) covers written objects, inscriptions and records/documents, not only continuous explanatory prose. This makes extension to recorded encoded symbols plausible; it does **not** attest binary metadata or prove readers will infer that extension unaided.
- [Cleasby–Vigfusson, BÆTA in the B section](https://norroen.info/dct/cleasby/b.html) explicitly discusses adding and `við-bót` as addition. [RIT in the R section](https://norroen.info/dct/cleasby/r.html) records the neuter writing/writ noun. These support the components of the proposed compound, not an attested historical whole-word metadata meaning.

Neither compound lexically says “external file.” Nevertheless, ordinary readers could construe either as supplementary writings without the technical convention. That remains a real intelligibility limitation, not evidence of an inherent exclusion of structured or embedded information. **Recommendation:** resolve the precise convention rather than replace it with another untested “data” compound whose meaning would also need definition. No broader historical attestation or modern-Icelandic substitution is offered.

### Actual source context

Read-only evidence in `Paintroid/src/main/java/org/catrobat/paintroid/classic/`:

- `AutosaveStore.kt`, `metadataBytes()` and `read()`: metadata is bounded UTF-8 JSON with a required version; `draft.json` is an entry in the autosave ZIP. Missing metadata is distinguished from missing `canvas.png` pixels. This is structured saved-state information, not ordinary supplementary prose. The record is alongside pixels **inside the archive**, not necessarily an external sidecar.
- `PlatformImageColour.kt`, `read()`: ICC, cICP, gamma and chromaticity records are read from image-container fields/chunks/segments. PNG, JPEG and WEBP parsing supplies direct evidence that colour metadata can be embedded in the image file.
- `PlatformImageColour.kt`, `withDecodeFile()/copyUntil()`: the truncation wording concerns exhaustion of file data while an expected range is being read. It is not a statement about a visible edge of the picture.

These implementation observations clarify the referent; they are not tests, a code audit, or evidence for historical grammar. No implementation fault is alleged.

## Eight exact M1 re-proposals — surface wording unchanged

“M1” versions the **semantic explanation only**. The exact current target bytes below are retained; this is not a new textual override. Confidence is author draft confidence, not accepted status. All four source strings have no interpolation placeholders.

| Locale / key | Exact English | Exact target proposed for retention | Literal backtranslation / intended technical reading | Author confidence and separate clause assessment |
|---|---|---|---|---|
| ang / ui_autosave_metadata_is_missing | Autosave metadata is missing. | Sidegewritu þære sylfhealdunge wana sind. | Accompanying records of automatic saving are lacking; technically, autosave metadata is missing. | **M**, conditional on the defined metadata convention. Absence, not invalidity, deletion, or absent pixels. No new morphological objection or repair. |
| ang / ui_invalid_autosave_metadata | Invalid autosave metadata. | Unrihte sidegewritu þære sylfhealdunge. | Invalid accompanying records of automatic saving; technically, invalid autosave metadata. | **M**, conditional on the convention. Invalid may include unacceptable structure/version/size; does not assert user error or physical corruption. No wording change needed for this issue. |
| non / ui_autosave_metadata_is_missing | Autosave metadata is missing. | Viðbótarrit sjálfvarðveizlu vantar. | Additional records of automatic saving are lacking; technically, autosave metadata is missing. | **M**, conditional on the convention. Required descriptive records can be missing even when pixel content is present. Existing missing-state construction is retained. |
| non / ui_invalid_autosave_metadata | Invalid autosave metadata. | Ógild viðbótarrit sjálfvarðveizlu. | Invalid additional records of automatic saving; technically, invalid autosave metadata. | **M**, conditional on the convention. Preserves invalid rather than missing; no morphology repair is identified by this semantic follow-up. |
| ang / colour_invalid_metadata | The image has invalid or unsupported colour metadata. | Seo anlicnes hæfþ unriht hiwsidegewritu oþþe swilc þe þis weorctol ne onfo. | The image has invalid colour-associated records, or such records as this application does not accept. | Metadata sense **M** under the convention; full clause **L / retain HOLD**. Invalid OR unsupported are distinct alternatives. The `swilc þe ... ne onfo` construction remains separately reviewable; glossary agreement is not syntactic acceptance. |
| ang / colour_truncated_metadata | The image ends inside its colour metadata. | Þæt anlicnesgewrit endaþ innan his hiwsidegewrita. | The image file ends within its colour-associated records. | Metadata sense **M**; full clause **L / retain HOLD** pending exact truncation-idiom judgment. `anlicnesgewrit` explicitly identifies the file; “within” describes a byte-stream record range, not a visual image border or an external sidecar. |
| non / colour_invalid_metadata | The image has invalid or unsupported colour metadata. | Myndin hefir ógild viðbótarrit um liti eða slík er verkfærit tekr eigi við. | The image has invalid additional records about colours, or such records as the application does not accept. | Metadata sense **M**; full clause **L pending independent judgment**. `um liti` specifies colour descriptors; invalid and unsupported remain alternatives. No new clause defect is alleged. A reviewer may resolve the metadata dependency without assuming all neighbouring held values are settled. |
| non / colour_truncated_metadata | The image ends inside its colour metadata. | Myndritit endar innan viðbótarrita sinna um liti. | The image file ends within its own additional records about colours. | Metadata sense **M**; full clause **L pending independent judgment**. The records are within the file's encoded sequence; the phrase does not locate them in a separate document. The exact file-truncation expression is a separate full-clause judgment. |

### Why the colour holds must remain separable

[B–T on-fón](https://lrc.la.utexas.edu/books/asd/dict-O) supports receive/accept and documents several object cases. That is positive lexical evidence, but it does not independently settle the chosen relative clause's mood or the complete technical-support reading. I therefore do not use the clarified metadata definition to declare the ANG invalid-colour sentence accepted.

[B–T innan](https://lrc.la.utexas.edu/books/asd/dict-I) supports within with genitive among its constructions, so the ANG truncation phrase has a defensible base. Applying containment to a serialized metadata range is a modern metaphor. Its whole sentence still needs its own review; no visual-edge or separate-file interpretation is intended. The corresponding NON sentence likewise requires a whole-clause decision, not a new medieval software citation.

## Requested independent decision and stopping boundary

1. Decide whether the **explicitly non-prose, non-sidecar, non-optional** descriptive-record convention is adequate for both locales and both contexts.
2. If yes, the four short autosave entries have no remaining defect identified **in this finite metadata inquiry**; reconsider their shared-term gate on the unchanged exact text.
3. Assess each colour clause on its own recorded construction/safety meaning. Do not mechanically upgrade all four or transfer any decision to other HOLD families.
4. If the convention is rejected for intelligibility, record that specific semantic reason before choosing another compound; no blanket claim of historical nonexistence or morphology failure follows.

Completed: source/context inspection, primary lexical checks, explicit semantic boundaries and eight exact retained-wording proposals. Pending at this author stage: independent linguistic decision. Research only; no implementation or project test result is asserted.
