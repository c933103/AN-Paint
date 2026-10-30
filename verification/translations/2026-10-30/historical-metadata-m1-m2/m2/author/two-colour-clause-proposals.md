# Metadata M2 — two exact colour-clause proposals

## Result first

**Propose one word-form change in each of the two remaining clauses:** ANG `onfo` → `onfehþ`; NON `endar` → `endisk`. The full proposed targets are below. Both have **moderate author draft confidence**, pending independent exact review. They preserve the M1 metadata convention and do not reopen or clear any unrelated HOLD.

These are separate **M2 proposed overrides**, not edits to frozen revision10, the M1 receipt, any adoption packet, or application resources. The earlier forms are not declared categorically impossible: the ANG subjunctive relative may have a generic/modal analysis, and neuter NON `Myndritit` permits a surface-identical accusative impersonal analysis. The revisions choose more directly evidenced constructions for the intended messages rather than prohibit those alternatives.

## Source binding

Read: `m1/independent-review/metadata-M1-independent-review.md`, SHA-256 `8f0b130d7c37814e64ac2ced248dacfc1ab3c78ccf298ee09b665311729737c8`.

Exact English rechecked in `Paintroid/src/main/res/values/strings.xml`, lines 553–554, in the supplied baseline workspace `frozen baseline resource snapshot`. Supplied baseline commit `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`; no new claim of locally resolvable HEAD.

The read-only call-site check in `classic/PlatformImageColour.kt` confirms that the truncation string is raised for exhausted input while copying an expected range; the invalid string is used for metadata-processing errors. This delimits the intended file/record meaning, not historical grammar, and is not a test or code audit.

## 1. ANG / `colour_invalid_metadata` / M2

**Exact English:** The image has invalid or unsupported colour metadata.

**Previous target:** Seo anlicnes hæfþ unriht hiwsidegewritu oþþe swilc þe þis weorctol ne onfo.

**Proposed full target:** **Seo anlicnes hæfþ unriht hiwsidegewritu oþþe swilc þe þis weorctol ne onfehþ.**

**Literal backtranslation:** The image has invalid colour-associated records, or such [colour-associated records] as this application does not accept.

**Intended UI reading:** The image has colour metadata that is invalid or is not supported by this application.

### Historical construction and exact change

- B–T `on-fón` III supplies the acceptance sense and the finite form in **“Se yfela déma onféhþ feó”** (Blickling Homilies 61,30). Its non-material reception examples also include **“Se ðe Godes word mid blisse onféhþ”** (Matthew 13,20). These positively establish the lexical base and third-person singular indicative form; the proposed normalization omits the vowel-length accent, as elsewhere in this ANG draft. [B–T on-fón](https://bosworthtoller.com/24545).
- The University of Glasgow's authored grammar, §67, describes indeclinable `þe`, including object relatives, and indicative as the usual relative-clause mood. This supports a factual relative with a third-person singular subject; it does **not** prohibit subjunctive relatives. [Essentials of Old English, subordinate clauses, §67](https://stella.glasgow.ac.uk/eoe/plus-sentence-structure-3.html).
- Here `þis weorctol` is the relative clause's nominative singular subject, and `onfehþ` its present indicative. `Swilc` is the neuter plural alternative object of matrix `hæfþ`, with the same colour-record antecedent; indeclinable `þe` introduces the relative. No new genitive-only or other exclusive object-case rule is imposed on `onfón`.

### Meaning, limits, and confidence

`Ne onfehþ` directly predicates non-acceptance of these records by the application. The technical convention is **functional acceptance as supported input**, not a user's refusal, discretionary permission, a future promise, or a claim that the records do not exist. This remains a disclosed modern software extension of historical acceptance vocabulary. The wording does not say the program supports a format merely because it can open a file.

`Oþþe` is retained: invalid and unsupported remain alternative grounds, with no assertion that every unsupported record is invalid, and no replacement of OR by AND. The second alternative inherits the same colour-metadata referent, not arbitrary unsupported material.

The former `onfo` could be subjunctive in a generic/modal relative. I have not established that it is ungrammatical; the reason to revise is to express the diagnosed unsupported state without depending on that less-settled interpretation. Nor is indicative claimed to encode every distinction of modern technical support by morphology alone.

**Confidence: M for the whole proposed clause.** Historical form and ordinary relative construction have positive evidence; the software-support extension and new compounds remain bounded experimental terminology, not medieval computing usage or measured reader comprehension. Independent review should decide the exact clause, not infer acceptance from this backtranslation.

## 2. NON / `colour_truncated_metadata` / M2

**Exact English:** The image ends inside its colour metadata.

**Previous target:** Myndritit endar innan viðbótarrita sinna um liti.

**Proposed full target:** **Myndritit endisk innan viðbótarrita sinna um liti.**

**Literal backtranslation:** The image-file comes to an end within its own additional records about colours.

**Intended UI reading:** The image file's data ends within its embedded colour metadata.

### Historical construction and exact change

- C–V ENDA II.1 expressly records the middle/reflexive come-to-an-end sense, including **“reiði mannsins endisk á einu augabragði”** (656 A.ii.17). Its additional example beginning `þá endisk sá enn mikli höfðingskapr` has an overtly nominative masculine subject, so the construction is not inferred solely from a case-ambiguous neuter. ENDA III separately records historical impersonal `sögu endar` and labels nominative `saga endar` as modern usage. The proposed `endisk` chooses II.1, not the separate last-out/endure sense in II.2. [C–V ENDA II–III](https://norroen.info/dct/cleasby/e.html).
- Sweet's historical-language grammar §130 describes the middle in `-sk`, with final active `r` dropped. The exact `endisk` is independently supplied by C–V, rather than invented by applying a modern `-st` paradigm. [Sweet, *An Icelandic Primer*, §130](https://www.gutenberg.org/files/5424/5424-h/5424-h.htm).
- The proposed syntax takes `Myndritit`, the definite neuter singular image-file noun, as nominative subject of the middle come-to-an-end predicate. The middle does not make the file an intentional agent destroying itself.

### Reflexive possession and case

`Innan viðbótarrita sinna` retains the already-reviewed genitive containment phrase. `Viðbótarrita` is genitive plural; **`sinna` is the agreeing genitive plural possessive**, pointing to the image-file subject. Its plural ending follows the possessed records, not the singular possessor. It is not the uninflected personal reflexive `sín`.

C–V SINN gives the reflexive possessive with subject reference as an ordinary construction, while also documenting other antecedents; no subject-only universal is inferred. Sweet's possessive table and §110 give the `minn` paradigm with genitive plural `minna`, and explicitly apply it to `sinn`, supporting `sinna`. The subject-based `endisk` clause makes the intended local antecedent explicit without needing to settle reflexive binding in the older sentence's possible impersonal analysis. [C–V SINN](https://norroen.info/dct/cleasby/s.html), [Sweet, possessive table and §110](https://www.gutenberg.org/files/5424/5424-h/5424-h.htm).

### Meaning, limits, and confidence

`Myndritit` identifies the file, not the visible image border. Under the M1 convention, the records are structured descriptors within the file's serialized content; `innan` locates the termination within that record span. It does not put the file physically inside an external document, say that metadata itself ends normally, or imply successful completion of saving. No advice to discard or replace anything is added.

The previous `Myndritit endar` is not declared impossible: neuter nominative and accusative are syncretic, and the dictionary supplies an impersonal pattern. The change is preferable because the intended nominative-subject analysis and its reflexive possession now rest on an explicitly historical middle construction. C–V also records other senses of `endask`; this contextual technical application is an inference, not an assertion that the verb has only one meaning.

**Confidence: M for the whole proposed clause.** The historical construction and possessive inflection have positive evidence. Applying termination and containment to encoded record boundaries, and the modern file/metadata compounds, remains a transparent modern extension, not native historical software attestation or an empirically tested UI phrase.

## Review boundary

Only these two full target cells are proposed for change, each by one word form. Their English has no interpolation placeholders. No source implementation or project test result is asserted. The six M1-adopted cells and every unrelated HOLD remain untouched. The frozen revision10 author files remain unchanged.

Completed: primary dictionary/grammar checks, exact source and clause binding, two full candidate overrides with backtranslations and confidence limits. Pending: independent linguistic review and the final bounded wording decision. No claim of native-human certification or implementation authorization.
