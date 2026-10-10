# F01 Ainu modality follow-up

10 October 2026. Evidence-only supplement for **F01-C004 (ain-Kana)** and **F01-C005 (ain-Latn)**.

**Disposition: linguistically uncertain, unchanged and open. F01 applicability remains unresolved. No replacement is proposed.** High-confidence grammatical subclaims below do not establish the complete UI meaning or native-language acceptance.

This supplement follows the [existing individual inventory](../combined-evidence/all-language-inventory.json), [PR43 evidence discussion](https://github.com/c933103/AN-Paint/pull/43#issuecomment-6097687952) and [PR7 F01/P07-007 discussion](https://github.com/c933103/AN-Paint/pull/7#issuecomment-6097689369). The evidence parent is `9606b613e802bebd46ddb57d44cda9ce4a09eb0d`; the reviewed resource head is `4f9082aa687a5c36b559061bcc10d0e39331610f`. [Structured disposition and source details](review.json).

## Exact originals

Both resources were read directly at the pinned PR43 head, line 558, for `formats22_tiff_description`. The retained text is identical to each original.

### F01-C004: Ainu Kana

[Canonical source](https://github.com/c933103/AN-Paint/blob/4f9082aa687a5c36b559061bcc10d0e39331610f/Paintroid/src/main/res/values-b%2Bain%2BKana/strings.xml#L558)  
Blob: `3b312cc293e7cd8fbe84b729dd5fc5eb1a18144b`

```text
シネ RGB ソㇱ アアマ. チヌイェㇷ゚ アポンテ ヤッカ pixel アシンナレ カ ソモ キ. TIFF チヌイェㇷ゚ ソモ ポンテ ノ アマ クス タン イヤヌ アイカㇷ゚テ ヤン.
```

### F01-C005: Ainu Latin

[Canonical source](https://github.com/c933103/AN-Paint/blob/4f9082aa687a5c36b559061bcc10d0e39331610f/Paintroid/src/main/res/values-b%2Bain%2BLatn/strings.xml#L558)  
Blob: `2bcff550416f01511c2d8894b29157ed060ea33a`

```text
Sine RGB sos a=ama. Cinuyep a=ponte yakka pixel a=sinnare ka somo ki. TIFF cinuyep somo ponte no ama kusu tan iyanu aykapte yan.
```

The two scripts share the targeted `a=ponte / アポンテ`, `yakka / ヤッカ` and `ka somo ki / カ ソモ キ` construction. This exact-source correspondence is high confidence; it is not a full orthographic or translation review.

## Source-backed grammatical findings

### 1. Concessive yakka: high confidence

The National Ainu Museum's digitization of Tamura Suzuko's *Ainu-go Saru hōgen jiten* (1996), entry **yakka**, supplies both hypothetical and factual concessive readings, with the concise English gloss **“even if; although.”** Its examples cover a future commitment despite adverse weather and an actual instance of unsuccessful waiting. These are published dictionary examples, not app-specific attestation. [S1: museum yakka entry, displayed on the upas results page](https://ainugo.nam.go.jp/dic?word=upas)

The Foundation for Research and Promotion of Ainu Culture's *Intermediate Ainu: Saru* (March 2014), printed p. 91, step 37, also identifies **yakka** as a concessive connective. The official PDF text was read; a screenshot request failed. Some PDF extraction lines reverse word order, so no reversed extraction is reproduced here. [S2: official PDF, printed p. 91 / PDF page 92](https://www.ff-ainu.or.jp/web/potal_site/files/saru_tyukyu.pdf#page=92)

### 2. Make-small meaning of ponte: high lexical confidence, access limit retained

The museum archive reproduces Chiri's *人間編Ⅱ*, §021 (33), **arke ciyasa arke ci-ponte kane an**, explicitly analyzing **ponte** as **“小さくした.”** Kayano's corresponding dictionary entry supports the same ordinary lexical interpretation. This does not establish an attested computing term for compression. [S3: institutional dictionary result containing these entries](https://ainugo.nam.go.jp/dic?word=a)

**Access limitation:** this passage was read in the indexed institutional result only. Direct opening of that results page and the direct ponte query routes failed. The yakka page in S1 did open successfully. No claim of independently inspected recordings or app-specific native usage is made.

### 3. Negation ka somo ki: high construction confidence

Nurmi, Jussi (2024), “Contrastive Negation in Ainu,” *言語科学研究* 1, pp. 57–80, explains **VP + ka somo ki** on printed pp. 63–64: the preceding verb phrase is the object of dummy verb **ki**, which is negated by **somo**. The article cautions that whether the construction is emphatic needs further study. [S4: Hokkaido University full-text article; DOI 10.14943/110403](https://eprints.lib.hokudai.ac.jp/dspace/bitstream/2115/91818/1/1_06-NURMI.pdf#page=8)

Applying that published analysis to the catalogue's clause order, the negation follows the pixel predicate. It does not function as a possibility qualifier for the earlier size predicate. This application is model linguistic analysis.

## Contextual meaning and F01 disposition

**Analytical working gloss of the middle sentence only, not an accepted full translation:**

“Even if/although one makes the file smaller, the pixels are not changed.”

The size-reduction clause precedes **yakka**; the following clause supplies the pixel-preservation assertion. A hypothetical reading does not guarantee reduction. A factual concessive reading may nevertheless assume it. The cited descriptions do not select one of those readings for this exact UI context.

Consequently:

- A categorical compression-always-reduces-size interpretation is **not proven**.
- An unequivocal may-reduce qualification is **also not proven**.
- The ordinary make-small meaning or lack of an explicit possibility auxiliary is insufficient to resolve the choice.
- Both cases retain **linguistically-uncertain / unchanged / open / Not closed**.
- Full-string vocabulary, computational terminology, dialect/register suitability, naturalness, rendering and native-language acceptance remain unverified. No native speaker reviewed this UI sentence.

Before proposing a replacement, the remaining requirement is a supported contextual judgment on whether this exact construction presupposes successful file-size reduction. No unsupported insertion of a modal is proposed.

## Scope preservation

This is project evidence only. It introduces no resource, test, application, workflow or inventory-classification change. Existing inventories and completion counts are retained; F01 and P07-007 remain pending. The authoritative register is unchanged at **475 total / 3 structural completed / 472 pending**. PR43's source branch is not updated by this supplement. No external contact, review request, CI dispatch or native-speaker attestation accompanies this linguistic follow-up.

The evidence is published as two new files on a separate evidence branch based on the pinned evidence parent; remote text and tree identities must be checked before reporting publication as verified.
