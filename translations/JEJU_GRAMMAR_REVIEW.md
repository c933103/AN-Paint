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
paragraphs were initially retained. The follow-up below records a real
remaining predicate defect found in that decision; the initial review was not
sufficient to establish grammatical completion.

## Sources and decisions

- Jeong Seung-cheol, [Characteristics of Jeju speech](https://www.korean.go.kr/nkview/nklife/1998_4/8-7.html), NIKL, 1998: section III.1 distinguishes statements and aspect; III.2 treats questions; III.3 distinguishes commands and proposals. Examples 18–19 are especially relevant to the incorrect `-읍주` statements. Section II and the connective discussion support `-곡`, `-민`, `-멍`, and `-엉` in the rewritten clauses.
- O'Grady, Yang, and Yang, [A Sketch Grammar of Jejueo](https://www.researchgate.net/publication/394072212_A_SKETCH_GRAMMAR_OF_JEJUEO), author-uploaded version, updated October 2024: sections 4–5 provide an additional check on negation and the ordering of aspect and sentence endings. This is supporting grammar evidence, not a translated software corpus.

| Meaning/function | Defect in the published resource | Repair |
|---|---|---|
| Current state: memory is insufficient | `부족헙주` invites a joint action instead of stating a condition | `이 작업에 쓸 만큼 메모리가 엇수다` |
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

## Follow-up after independent review

The independent review found bare action stems followed by `-우다/-수다`,
including `놓이우다`, `나오우다`, `뒤집히우다`, `지우우다`,
`돌려놓수다`, and `다루우다`. The first pass had missed this in the retained
manuals and had also introduced it in new clauses.

The Sketch Grammar §7.1, pp. 19–20, distinguishes honorific endings on inflected
verbs from those on uninflected descriptive verbs; NIKL III.1 makes the same
relevant distinction. Neither licenses the bare event predicates above.
Sketch Grammar §7 gives formal `-up-ney-ta`, without the direct-observation
implication of `-up-tey-ta`. The
[Jeju Province oral corpus](https://www.jeju.go.kr/jedu/map/record.htm?page=206),
Goseong-ri, food, 2017, independently illustrates its ordinary habitual use:
“경 아니ᄒᆞᆫ 사람은 젓갈 놩 헹 먹곡 경 헙네다.”
The UI sentences below are newly composed applications of that grammar.

All finite predicates in the catalogue, including the three complete manuals
and the plural, were reconsidered by clause function:

| Function | Result of the follow-up |
|---|---|
| Routine behavior and conditional button effects | Formal `-ㅂ네다/-읍네다`: `첫 이미지는 원점에 놓입네다.`; `다시 누르민 접히멍 화살표 방향도 뒤집힙네다.` |
| Current over-limit errors | Perfective result `한도를 넘엇수다`, not an uninflected event stem. |
| Preserved state | Explicit `그대로우다` for unchanged save destinations, image sizes, and crop settings. |
| Unsupported operation or insufficient capacity | Existential capability or quantity statements; the decoder-floor warning still says that even the smallest output does not fit. |
| Ongoing operation | Retained `초안을 저장허염수다`; no conversion of general manual descriptions into progress reports. |
| Completed operations | Retained perfective success/failure predicates and preserved their distinction from a still-running save. |
| Requirements and permission | `-어사 헙네다` versus `-어도 뒙네다`; compulsory decoding does not become merely possible. |
| Descriptive predicates and copulas | Retained `크우다`, `많수다`, `이우다`, and descriptive negation; they are not event verbs. |
| Questions and commands | Kept the prospective questions `저장허쿠과?`, `넣으쿠과?`, and `고치쿠과?`; corrected malformed commands `고쳡서` and `열읍서` to `고칩서` and `엽서`. |

The command allomorphy follows Sketch Grammar §7 (examples 65 and surrounding
text). The opening command also occurs as “이 문 엽서” in the
[Jeju Studies Archive's Yi Yong-ok narrative transcription](https://jst.re.kr/upload/pdf/RC00085701.pdf), p. 94.

The shared Irasutoya-help requirement clauses now use `지켜사 헙네다` and
`내사 헙네다`, preserving the current File → About → Image credits captions.
No Ainu or Manchu text changes are part of this follow-up.

Validation: the 27 resource tests still pass and the patch is whitespace-clean.
This follow-up corrects an identified class of errors; it does not convert those
structural results or the number of edited keys into native-speaker approval.

The final state check also removed `모자라우다` from eight memory errors.
A meaning that describes a state does not by itself prove that a particular
lexeme takes descriptive-verb inflection. No primary attestation for that form
was established here, so these warnings now express the insufficient amount
with `…헐 만큼 메모리가 엇수다` (not enough memory to perform the named
operation). The operation, unchanged-original clause, and retry advice remain.
