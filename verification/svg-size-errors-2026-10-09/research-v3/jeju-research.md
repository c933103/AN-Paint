# Jeju SVG unavailable message: targeted review candidate

**Review only.** No accepted coverage change, production resource edits, or native-acceptance claim.

## Full pair for review

The complete pair and both messages’ clause evidence are in [pair-for-review.json](pair-for-review.json). The too-large wording is copied unchanged from the prior v2 review input:

SVG의 원래 크기가 Android 비트맵 크기 한도를 넘엇수다. 크기 조절은 아니 허엿수다.

## New unavailable candidate

SVG에 적어진 쓸 수 있는 원래 크기가 엇수다. 캔버스 크기를 기준으로 헌 크기를 대신 쓰지 아니허엿수다.

Backtranslation: There is no usable original size written in the SVG. A size based on the canvas size was not used instead.

## Meaning preserved

- The first clause negates existence of a size meeting all three conditions: written in SVG, original, and usable. It does not claim the SVG contains no dimensions of any kind.
- Written in is an ordinary-language paraphrase of a document declaring dimensions. It does not narrow to visible text on the drawn image.
- The second clause negates using a canvas-based size as a substitute. It does not mean no canvas size was changed, no user could make a substitution, or only no automatic substitute.
- No Android wording belongs in this unavailable message; SVG identity is retained. There are no placeholders.

## Evidence by clause

| Segment | Support | Review boundary |
| --- | --- | --- |
| SVG에 적어진 | written/stated in SVG; CORPUS-WRITTEN, canonical source-recording terminology | Locative file identity is combined with attested passive-adnominal 적어진. |
| 쓸 수 있는 원래 크기가 엇수다 | no usable original size exists in that restricted class; CORPUS-USABLE, YANG2020, canonical ui_original_size34 / ui_enter_valid_dimensions / memory warning | Two relative modifiers precede 원래 크기. Need an independent check that attachment and UI reading are natural. |
| 캔버스 크기를 기준으로 헌 크기를 대신 쓰지 | use a size based on canvas size instead; CORPUS-BASIS, CORPUS-SUBSTITUTE, canonical ui_normalize_width_info / ui_edit_canvas33 | 기준으로 헌 combines independently attested basis wording and adnominal 헌; canvas-size numeric context comes from catalogue. Instead-use is independently attested. |
| 아니허엿수다 | did not perform that substitute-use action; CORPUS-COMPLETED-NEGATION, YANG2020, canonical completed polite 허엿수다 | Uncontracted long negation + completed aspect + catalogue polite ending. This is not a Korean -않다 string with its ending replaced. |

## Public sources inspected

### CORPUS-USABLE

[CORPUS-USABLE](https://www.jeju.go.kr/jedu/map/record.htm?q=%EC%93%B8+%EC%88%98)

HTTP 200 direct public HTML; first result page inspected; 11 matching records reported. Search matches either Jeju text or its standard-Korean gloss, so the layers were inspected separately.

표선면 성읍리 / 주생활 / 2018; 제보자 (informant)

Short attestation: 혼자만 쓸 수 있는 톱

An actual informant uses the ability-relative construction 쓸 수 있는 before a usable tool. This independently supports the exact canonical 쓸 수 있는 크기 wording, without importing Korean ability morphology on resemblance alone.

Limit: This is tool usability, not a full SVG sentence; original and dimensions terminology come from the catalogue.

### CORPUS-WRITTEN

[CORPUS-WRITTEN](https://www.jeju.go.kr/jedu/map/record.htm?q=%EC%A0%81%ED%9E%8C)

HTTP 200 direct public HTML; the only matching record inspected in both layers.

성산읍 삼달리 / 통과의례 / 2018; 조사자 (interviewer)

Short attestation: 결혼 날짜 적어진 거

The Jeju-layer interviewer utterance uses 적어진 for information recorded in a letter. The aligned Korean layer has 적힌. The candidate uses the actually recorded Jeju form 적어진, not the gloss.

Limit: Interviewer rather than informant evidence; not a computing declaration attestation. New stacked relative modifiers still require composition review.

### CORPUS-BASIS

[CORPUS-BASIS](https://www.jeju.go.kr/jedu/map/record.htm?q=%EA%B8%B0%EC%A4%80)

HTTP 200 direct public HTML; first page inspected; 43 matching records reported.

제주시 도련1동 / 밭일 / 2017; 제보자 (informant)

Short attestation: 음력은 달을 기준헌 거니까

Informant uses a 기준헌 relative construction for a lunar-calendar basis; the same page includes 기준으로 헤서. Canonical normalization separately establishes 기준으로 for a numeric dimensional basis. The candidate combines these constructions as 기준으로 헌.

Limit: The new size noun phrase is composition, not a quote of a pre-existing technical phrase.

### CORPUS-SUBSTITUTE

[CORPUS-SUBSTITUTE](https://www.jeju.go.kr/jedu/map/record.htm?q=%EB%8C%80%EC%8B%A0+%EC%93%B0)

HTTP 200 direct public HTML; all five matching records on the page inspected.

남원읍 수망리 / 놀이 / 2018; 제보자 (informant)

Short attestation: 비누 대신 쓰멍

An informant describes using another material in place of unavailable soap. Other informants use 대신 쓰는 for an object taking a brazier’s role and for ritual food substitution. This establishes actual substitute-use semantics, not mere replacement of files or an interviewer-only construction.

Limit: Substituting a computed size is a new application of ordinary language; no native acceptance claimed.

### CORPUS-COMPLETED-NEGATION

[CORPUS-COMPLETED-NEGATION](https://www.jeju.go.kr/jedu/map/record.htm?q=%EC%95%84%EB%8B%88%ED%97%88%EC%97%BF)

HTTP 200 direct public HTML; only matching record inspected.

조천읍 신촌리 / 경험담, 속담, 금기어 / 2019; 제보자 (informant)

Short attestation: 빠먹어보질 아니허엿는데

Attests a completed negative action with uncontracted 아니허엿 and no intervening space. The UI candidate uses the established catalogue polite ending 수다; the whole exact finite form is newly composed.

Limit: The corpus inflection is a connective, not the candidate’s sentence-final polite form.

### YANG2020

[YANG2020](https://www.mlsk1984.com/articles/pdf/0zWo/mlsk-2020-036-01-5.pdf)

Full 20-page publisher PDF parsed with web tool; relevant printed pages 75–80 and 83 (PDF pages 2–7,10).

Sections 3.1.1, 3.1.2, 3.1.4, 3.1.5 and 3.2.2; examples 8,17–18,39–40

Explains ordinary 아니 negation versus inability 못; long negative -지 아니다 and completed 아니엿; and 엇다 as absence/nonexistence, including at a location. This supports reporting no substitute was used and no usable recorded original size exists, rather than inability or a prohibition.

Limit: Does not independently certify the relative-clause ordering or the complete new UI sentence.

### JEJUEO-INSTITUTE-USE

[JEJUEO-INSTITUTE-USE](https://www.jejueo999.kr/index.php/contents/qna?act=view&bd_bcid=qna&page=39&seq=2131)

Public indexed answer read; direct web open returned Internal Error.



Jejueo Research Institute answer identifies 쓰다/씨다 forms for use and writing senses, among other homonyms. Supports that shared 쓰다 is not automatically invalid merely because Korean also has it.

Limit: Only index text was retrieved. No claim that this Q&A validates the proposed inflection or entire translation.

## Residual review questions

- Is the stack SVG에 적어진 쓸 수 있는 원래 크기 natural in this catalogue register while keeping both modifiers attached to the size?
- Does 기준으로 헌 크기 read smoothly as a canvas-derived size, without suggesting the canvas was resized?
- Confirm final polite auxiliary 아니허엿수다 and spacing in this catalogue. Source evidence supports morphology, but the exact full sentence is new.
- The first passive-adnominal external attestation is interviewer speech. The original catalogue also supplies 적힌 in a written-source context; neither constitutes native acceptance of this new composition.

## Bounded-pass result

A full review-only unavailable-message candidate is now defensible from actual Jeju constructions and catalogue terminology. It is not an accepted translation. The original 48-pair proposal snapshot and all earlier candidate files are unchanged. The previous too-large candidate remains in its original v2 file.

The JSON records all twelve targeted corpus queries, exact URLs, HTTP outcomes, local evidence hashes, unsuccessful PDF retrievals, and the distinction between Jeju text and Korean glosses. First-page matches were inspected; matching-record counts are not claims to have read every result. No login or correspondence was used.
