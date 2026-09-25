# Korean script handoff review — 2026-09-25

The original mixed-script handoff promised a general-domain aligned
Hangul/Hanja **corpus**, plus explicit decisions for eight AN Paint concepts.
The initial 97-pair dictionary check was necessary spelling evidence, but it
was a lexicon check and did not fulfil the corpus promise. The earlier cited
[Kyubyong/h2h_converter](https://github.com/Kyubyong/h2h_converter#data) explicitly
uses the KRV Bible. That citation did not establish general-domain review.
This follow-up actually uses externally published literary annotations and
parallel civic prose, with their different alignment levels identified below.
No model from that project was used for this review.

`KOREAN_HANJA_REVIEW.tsv` records all 97 distinct replacement pairs found by
comparing the ko-KR and ko-Kore-KR catalogues at integration commit 7939f1292.
It is review evidence, not a generator or translation source. Android XML remains
the independently editable canonical catalogue. Of these pairs, 91 are exact
Hangul/Hanja entries in the general-purpose NIKL Standard Korean Language
Dictionary snapshot; six are explicitly identified editorial compositions or
synonyms. The table does not pretend that the six are exact dictionary headwords.

## Reproducible dictionary evidence

- Publisher: National Institute of Korean Language, Standard Korean Language
  Dictionary; source dump `전체 내려받기_표준국어대사전_JSON_20260606.zip`.
- Derived TSV: [Gukhanmun, commit fb9d665bef5aee48532111534912dbac20bc6a0c](https://github.com/dahlia/gukhanmun/blob/fb9d665bef5aee48532111534912dbac20bc6a0c/crates/gukhanmun-stdict/data/stdict.tsv).
- TSV SHA-256: `4e3796dfc85a16345b7c4395d89f68e23a5606fd03f62da5d197c77dc75c438a`.
- Line numbers in the review table refer to this pinned file, including its header.
- The selected lexical data and its adaptation in `KOREAN_HANJA_REVIEW.tsv` are
  CC BY-SA 2.0 KR, attributed to NIKL and the Gukhanmun contributors.
  [Publisher policy](https://stdict.korean.go.kr/join/copyrightPolicy.do),
  [license](https://creativecommons.org/licenses/by-sa/2.0/kr/),
  [upstream notice](https://github.com/dahlia/gukhanmun/blob/fb9d665bef5aee48532111534912dbac20bc6a0c/NOTICE.md).
  No example prose or multimedia from the dictionary is redistributed.

## External literary corpus: published annotation alignment

The [Open Korean Historical Corpus (OKHC)](https://github.com/seyoungsong/OKHC)
by Seyoung Song and collaborators supplies the external text, independently of
AN Paint. We read its Korea Copyright Commission **GongU Madang** component:

- [Pinned `gongu.jsonl`](https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus/resolve/2d16d39c774ef788069d63223d07e31e038c05df/gongu.jsonl),
  revision `2d16d39c774ef788069d63223d07e31e038c05df`.
- 254,638,515 bytes; SHA-256
  `b689360119c1fc68c2dbcfdabc27589997e2a54a988051739c1644634db1785c`.
- The component contains 13,291 records. Its 9,566 records labelled Korean,
  Modern Korean or Early Modern Korean yield 119,720 explicit `Hangul(Hanja)`
  occurrences under the checker's deliberately narrow extraction rule.
  These are published **word-span alignments in running text**, not newly
  authored app examples and not sentence-parallel editions.
- Exact matches occur for 44 of the 97 app pairs before contextual review.
  `KOREAN_CORPUS_OCCURRENCES.tsv` selects 42: 41 accepted occurrences from
  non-Biblical fiction, travel writing, literary criticism and other essays,
  plus one rejected UI sense. The selected records exclude Bible commentary
  and translated royal annals. The two remaining raw matches, 제거 and 초안,
  were only found in the excluded annals within this extraction.
- Each row records the actual source ID, JSONL line, zero-based half-open
  Unicode-code-point offsets in `text`, the published annotation, source URL,
  and our contextual decision. Compatibility Hanja is normalized with NFKC
  only when comparing the word pair; the source span is retained verbatim.
  All 35 selected records carry the corpus's `Public Domain` source status.

This is an occurrence review, not a claim that historical prose validates modern
UI phrasing. For example, 배경/背景 appears in a travel account describing a
photograph, 전경/前景 in an essay describing pictorial composition, and 출처/出處
in fiction about the origin of a photograph. Those contexts help resolve senses.
The sole 색상/色相 match concerns physiognomic appearance; it is explicitly
**rejected as colour evidence**. The colour decision instead uses the AKS
colour article below. Settings, save and editing are not falsely presented as
attested by this selected literary sample.

Recheck the recorded spans after downloading the pinned file outside the repo:

```sh
python tools/verify_korean_corpus_evidence.py /path/to/gongu.jsonl
```

The OKHC compilation is [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/),
as stated in its [dataset card](https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus).
It is research input, not an app asset, and is not redistributed here. The table
records selected word facts, factual coordinates and our review comments; it
does not copy the stories, essays or the compiled corpus. Publisher URLs are
retained for attribution and inspection of the underlying works. The public
OKHC newspaper sample contains copyright-removal placeholders, so it was not
used as purported accessible parallel newspaper evidence.

## External parallel prose: civic domain

The existing [Wikisource 대한민국헌법 (한자혼용), revision 407869](https://ko.wikisource.org/w/index.php?oldid=407869)
publishes separate Hangul-only and mixed-script columns for the same 130
numbered articles. These are externally published aligned prose, not output
from our conversion rules. Its original-text provenance is
[대한민국 관보 제10771호(그2), 1987-10-29](https://ko.wikisource.org/wiki/색인:Gwanbo,_vol._10771-2.pdf),
linked to the [National Archives copy](https://theme.archives.go.kr/viewer/common/archWebViewer.do?singleData=N&archiveEventId=0052442367).
This supplements the literary annotation corpus with actual sentence-parallel
material; its civic/legal domain is not representative of every register.

`KOREAN_PARALLEL_PROSE.tsv` records 12 app-relevant word pairs from selected
clauses that were compared in both published columns. It retains the complete
attesting word or inflected span, so a component such as 선택 within 직업선택
is not misrepresented as an independently occurring word. The clause checksum
is SHA-256 of the exact Hangul clause, one LF, then the exact mixed clause,
UTF-8, retaining paragraph numbers and source punctuation. The 13-clause
research snapshot (including two grammar examples) was checked on 2026-09-25;
its SHA-256 is `754906c85855bebcbd30ef83ca938e6277141bbf1048c1bfdc6d2831c942021b`.
Only the short attesting spans and these two grammar examples are reproduced:

| Clause | Published Hangul | Published mixed script |
| --- | --- | --- |
| 1(1) | ①대한민국은 민주공화국이다. | ①大韓民國은 民主共和國이다. |
| 18 | 모든 국민은 통신의 비밀을 침해받지 아니한다. | 모든 國民은 通信의 秘密을 침해받지 아니한다. |

The source preserves native words and endings: 모든, 은, 의, 을, 이다 and
침해받지 아니한다 remain Hangul. It also leaves some Sino-Korean words in
Hangul. For example, 사용 in Article 23(3) does **not** attest 使用, and
확정될 in Article 27(4) does **not** attest 確定. The accepted 確定 evidence
is the actual 確定法律/확정법률 compound in Article 53(6). This supports
contextual mixed-script editing rather than maximizing character conversion.

Source-quality limits are explicit: the main-page revision does not freeze
separately transcluded Gazette-page revisions; the recorded literal spans and
clause hashes identify what was observed. Original Gazette images were not
independently checked. We do not claim all 130 articles are clean. Suspect
transcriptions in Articles 26(1) (`任權`), 32(1) (`最低臨金制`), 32(2)
(`義武`) and 32(3) (`法率`) were excluded, not silently repaired and reused
as evidence. Dictionary spellings remain an independent check.

The underlying statute is excluded from copyright under
[Copyright Act Article 7](https://www.law.go.kr/lsLinkCommonInfo.do?lsJoLnkSeq=1029423769).
Credit for the paired transcription/arrangement is **Wikisource contributors**,
with the pinned source link above. The selected transcription/arrangement
material in `KOREAN_PARALLEL_PROSE.tsv` retains
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) attribution;
that does not change the public-domain status of the underlying statute.

Across both reviewed corpus selections, **47 of the 97 app pairs** have
accepted occurrences (41 literary, 12 civic, six overlapping). The remaining
50 are not claimed corpus-attested here: 44 retain dictionary/context evidence,
and six remain the explicitly marked editorial compositions/synonym choices
in the original inventory. No historical source is used to invent modern
computer terminology or replace Korean sentence grammar.

## AN Paint concept decisions (editorial application)

The following decisions apply the spelling and context evidence to this app;
they are not themselves an external corpus. Encyclopedia and dictionary
entries were checked in the original publishers' articles on 2026-09-25.
They distinguish a word's spelling from its UI meaning.

| Concept | AN Paint choice | Evidence and contextual decision |
| --- | --- | --- |
| Image | 이미지 | English loan remains Hangul; [NIKL image entry](https://krdict.korean.go.kr/m/eng/searchResultView?ParaWordNo=49299). Do not silently replace the Korean word with the synonym 畫像. |
| Colour | 色相 | 색상/色相 paired in [AKS, 빛깔](https://encykorea.aks.ac.kr/Article/E0025316). Colour context, not the unrelated Buddhist meaning of the same written word. |
| Settings | 設定 | Dictionary exact pair; contextual technical pairing in [NIKL, 초깃값 설정](https://kli.korean.go.kr/term/trgtWord/indexTrgtWord.do?trgtWordNo=2491042). |
| Save | 貯藏 | 저장/貯藏 exact pair and [NIKL basic entry](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74621); app action stores image data. |
| Select | 選擇 | Dictionary exact pair, published literary annotation in `gongu:13313664`, and parallel civic Article 15; retain the existing Korean 선택 word and its particles. |
| Edit | 編輯 | 편집/編輯 paired in [AKS, 비선형 편집](https://encykorea.aks.ac.kr/Article/E0074626), including digital editing. |
| File | 파일 | English loan remains Hangul. No fabricated character spelling. |
| Memory | 메모리 | English loan remains Hangul; [NIKL technical entry](https://kli.korean.go.kr/term/trgtWord/indexTrgtWord.do?trgtWordNo=202078). Do not convert arbitrary syllables or replace it with a different Korean word simply to increase Hanja density. |

Native Korean verbs, particles and endings remain Hangul. Editorial app examples: 모두 表示,
이미지를 選擇, 크기를 變更합니다. Homonyms must be resolved by the whole word and
sentence: 커서 in 너무 커서 is the inflected adjective 크다, not the cursor loan.

## Concrete repairs from reading the catalogues

- ko-KP PDF dimension warning had `너무 지시자` (“too cursor”) from a substring
  replacement of `커서`. Restore the grammatical size explanation.
- ko-KP metadata was `중간자료` (“intermediate data”). Use the descriptive
  `자료의 설명 정보` / `색상 설명 정보` in the affected warnings.
- The ko-KP colour-profile warning had both a profile/outline false friend and
  the wrong object particle. Describe the unsupported colour information.
- Remove the unsupported `반톱날` calque from the antialiasing label; the label
  directly describes smoothing pixel edges.
- Correct the final legal/source paragraph's stale Help route and the first
  paragraph's obsolete generic Android submenu description in all three Korean
  catalogues and Vietnamese. Quote the actual five tab names.
- Align Korean help's image-open, image-assembly, cursor-drawing and KP gallery
  names with the actual controls.

These are source-assisted semantic checks. Neither dictionary matching nor a
successful build is a claim of independent native-speaker approval.
