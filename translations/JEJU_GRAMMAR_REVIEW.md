# Jeju handoff review — 25 September 2026

The original Jeju/Manchu/Ainu/Okinawan conversation resumed at Jeju string 126 on
23 September. It said Korean was a drafting reference and that Jeju grammar still
needed review. A later 669-string completion count did not prove that review had
happened. The published integration still contained Korean finite clauses,
Korean perfectives followed by Jeju-looking endings, and factual statements
ending in the Jeju propositive (an invitation to act).

This pass read all 669 strings and the plural in `values-b+jje/strings.xml` against
the default resource meanings. It changes 173 strings and the plural. Short
technical labels and shared vocabulary are retained when their meaning is right;
being different from Korean is not itself a translation-quality test. The editor,
assembly, and legacy manuals were read as complete instructions, including the
output/memory distinctions, preserved original files, selection state, save vs
export, and the captions that the user must find. Their already-rewritten Jeju
paragraphs were retained.

## Sources and decisions

- Jeong Seung-cheol, [Characteristics of Jeju speech](https://www.korean.go.kr/nkview/nklife/1998_4/8-7.html), NIKL, 1998: section III.1 distinguishes statements and aspect; III.2 treats questions; III.3 distinguishes commands and proposals. Examples 18–19 are especially relevant to the incorrect `-읍주` statements. Section II and the connective discussion support `-곡`, `-민`, `-멍`, and `-엉` in the rewritten clauses.
- O'Grady, Yang, and Yang, [A Sketch Grammar of Jejueo](https://www.researchgate.net/publication/394072212_A_SKETCH_GRAMMAR_OF_JEJUEO), author-uploaded version, updated October 2024: sections 4–5 provide an additional check on negation and the ordering of aspect and sentence endings. This is supporting grammar evidence, not a translated software corpus.

| Meaning/function | Defect in the published resource | Repair |
|---|---|---|
| Current state: memory is insufficient | `부족헙주` invites a joint action instead of stating a condition | `메모리가 모자라우다` |
| General capability and limits | “An assembly can contain 20 images” used `들어갑주` | `20장꺼지 합칠 수 이수다` |
| User instruction | `입력허옵서` repeated an artificial generic command template | Per-context `적읍서`, `고릅서`, `누릅서`, or `정헙서` |
| Completed operation | Korean `했-` plus `수다` | Jeju `허엿-` in the actual completed-status clauses |
| Import warning | Korean `줄이세요`, `아닙니다`, and conditional clauses left intact | Whole clauses rewritten with purpose/condition, capability, and state distinguished |
| Pixel and colour behaviour | Standard Korean `그립니다`, `채워집니다`, `커집니다` | Drawing instructions and resulting states expressed separately |
| Codec requirements | Propositive used for mandatory decoding, file limits, or page constraints | Requirement or negative-capability clauses; exact codec names and limits retained |
| Animation | Source distinction between the first frame and PNG's separate poster image | Both branches rewritten separately; animation loss remains explicit |
| Saving and export | A button instruction and an automatic effect conflated | Choose settings; later Save reuses them; Export leaves the active save target unchanged |
| Crop plural | Two factual effects used propositive endings | Apply to `%3$d` images, followed by the effect on attached images |

These are original UI translations informed by grammar, not copied example
sentences or a dictionary-generated catalogue. They preserve the technical
identifiers, all formatting arguments, 512 MiB and GIF/ICO limits, and the source
clauses. The changed watercolor hint quotes the actual `강도(%)` caption and is
marked `formatted="false"` for its literal percent sign.

The three shared gallery-help routes are owned by the integration-wide route
repair and should be combined with this change. Do not overwrite those route
updates when integrating this catalogue.

Validation: all 27 translation tests pass and `git diff --check` is clean.
Structural checks are not a linguistic certificate. This is a source-assisted
editorial review; it is not an independent native-speaker sign-off, and technical
terminology choices remain open to such review.

## Adjacent Manchu correction

Only two obsolete sentences in the first legacy-help paragraph were changed in
`values-b+mnc+Mong/strings.xml`: they told users to open a generic Menu and Android
arrows. The replacement points to the actual localized File → About/credits
captions. The rest of the previously completed Manchu catalogue was preserved.

A subsequent shared-route pass updates the legacy manual's insertion paragraph
to Draw → Insert → Other images, including all three online providers, device
files, the Use image action, and floating selection. Assembly is now File-only.
That additional manual key is separate from the 173-string grammar batch above.
