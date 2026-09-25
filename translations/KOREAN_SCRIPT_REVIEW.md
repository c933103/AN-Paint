# Korean script handoff review — 2026-09-25

The original mixed-script handoff promised an auditable general-domain
Hangul/Hanja vocabulary check. The earlier cited
[Kyubyong/h2h_converter](https://github.com/Kyubyong/h2h_converter#data) explicitly
uses the KRV Bible. That citation did not establish general-domain review.
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

## General-domain paired prose and AN Paint decisions

The following are contextual checks, not a claim that an encyclopedia is a
complete parallel translation corpus. The paired terms were checked in the
original publishers' articles on 2026-09-25. They supplement the full dictionary
pair inventory and distinguish a word's spelling from its UI meaning.

| Concept | AN Paint choice | Evidence and contextual decision |
| --- | --- | --- |
| Image | 이미지 | English loan remains Hangul; [NIKL image entry](https://krdict.korean.go.kr/m/eng/searchResultView?ParaWordNo=49299). Do not silently replace the Korean word with the synonym 畫像. |
| Colour | 色相 | 색상/色相 paired in [AKS, 빛깔](https://encykorea.aks.ac.kr/Article/E0025316). Colour context, not the unrelated Buddhist meaning of the same written word. |
| Settings | 設定 | Dictionary exact pair; contextual technical pairing in [NIKL, 초깃값 설정](https://kli.korean.go.kr/term/trgtWord/indexTrgtWord.do?trgtWordNo=2491042). |
| Save | 貯藏 | 저장/貯藏 exact pair and [NIKL basic entry](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74621); app action stores image data. |
| Select | 選擇 | Dictionary exact pair; it retains the existing Korean 선택 word and its particles, rather than borrowing unrelated vocabulary. |
| Edit | 編輯 | 편집/編輯 paired in [AKS, 비선형 편집](https://encykorea.aks.ac.kr/Article/E0074626), including digital editing. |
| File | 파일 | English loan remains Hangul. No fabricated character spelling. |
| Memory | 메모리 | English loan remains Hangul; [NIKL technical entry](https://kli.korean.go.kr/term/trgtWord/indexTrgtWord.do?trgtWordNo=202078). Do not convert arbitrary syllables or replace it with a different Korean word simply to increase Hanja density. |

Native Korean verbs, particles and endings remain Hangul. Examples: 모두 表示,
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
