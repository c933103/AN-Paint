# SVG original-size reasons: Ainu and Okinawan, v3

Three complete review-only pairs are now proposed. No canonical resources, frozen repository files or earlier snapshots were changed. No native or independent language acceptance is claimed.

## What changed from v2

The task-focused pass searched every string in the complete English, Ainu Latin, Ainu Kana and Okinawan XML catalogues, then read relevant long help, assembly, normalization, source-condition, replacement and error clauses. The previous small sample missed:

- `formats22_ico_dimensions_error`: “size written in the file” in both languages, directly relevant to a plain paraphrase of “declare”.
- `ui_each_px_px_percent_is_relative_to_the`: Ainu X ani a=kar for a value made using/based on X.
- Assembly help: Ainu [replacement] ani [existing image] a=itasare, making both replacement arguments explicit.
- `formats22_animation_poster`: Okinawan targetぬ代わりんかい, “in place of target”.
- `colour_converter_unavailable`: completed negative non-operation, rather than only future policy or inability.

The [Miyara practical dictionary](https://repository.ninjal.ac.jp/records/3227) additionally confirms a written-information predicate in examples 303/1568 and polite negative-past morphology in example 2722. The [Saru grammar](https://ainugo.nam.go.jp/pages/ainu_basic.html) and [NINJAL corpus grammar](https://ainu.ninjal.ac.jp/folklore/) support the Ainu ordering, negation and person-marking analysis.

These findings support composition. A complete new UI sentence need not already occur in a dictionary. The catalogues remain unaccepted reference evidence, so composition from them is a proposal, not proof of linguistic correctness.

## Full review-only candidates

### ain-Latn

Unavailable:

SVG or ta a=nuye hoski pororu anak isam hene a=eywanke eaykap hene ne. Kampiso kor pororu ani a=kar pororu ani hoski pororu a=itasare ka somo ki.

Too large:

SVG kor hoski pororu anak Android Bitmap kor pararu newa riru a=anu easkay pakno kasu. Noka kor pororu a=sinnare ka somo ki.

### ain-Kana

Unavailable:

SVG オㇿ タ アヌイェ ホㇱキ ポロル アナㇰ イサㇺ ヘネ アエイワンケ エアイカㇷ゚ ヘネ ネ. カㇺピソ コㇿ ポロル アニ アカㇻ ポロル アニ ホㇱキ ポロル アイタサレ カ ソモ キ.

Too large:

SVG コㇿ ホㇱキ ポロル アナㇰ Android Bitmap コㇿ パラル ネワ リル アアヌ エアㇱカイ パㇰノ カス. ノカ コㇿ ポロル アシンナレ カ ソモ キ.

Intended literal meanings:

1. The original size recorded in the SVG is absent or cannot be used. We/one did not replace the original size with a size made using the canvas size.
2. The original SVG size exceeds the range within which the width and height of an Android Bitmap can be set. We/one did not change the image size.

The generic a= subject is not treated as a universal passive marker. In the substitution clause the inner ani marks the input used to derive the size; the outer ani marks the replacement value. Hoski pororu is the object being replaced. Android Bitmap retains the recognizable Android type identifier, avoiding a newly invented Ainu technical noun.

### ryu

Unavailable:

SVGんかいや、ちかゆる元ぬサイズぬ 書かっとーいびらん。キャンバスぬサイズっし 決みたるサイズや、元ぬサイズぬ代わりんかい ちかやびらんたん。

Too large:

SVGぬ元ぬサイズや、Androidぬビットマップぬ寸法ぬ上限やか まぎさいびーん。サイズけーゆしや さびらんたん。

Intended meanings:

1. A usable original size is not recorded in the SVG. A size determined using the canvas size was not used in place of the original size.
2. The original SVG size exceeds the dimensional limit for Android bitmaps. Changing the size was not done.

The construction explicitly names the canvas-size basis and the replaced original size. The final sentence reuses the existing negative resize clause with only the automatic-only modifier removed.

## Review focus

- Ainu: idiomaticity of absent-or-unusable predication; readability of nested ani phrases; abstract size replacement with itasare; whether the width/height range is understood collectively, without suggesting both must exceed their limits individually.
- Okinawan: the complete polite negative written-information and use predicates; the technical noun chain for bitmap dimension limit.
- Existing neologisms and technical loans are not automatically invalid. Pororu is documented in a named independent lexicon; this does not establish community acceptance.

## Checks and files

All six candidates passed XML round-trip and placeholder checks. SVG/Android remain recognizable. No automatic-only or shrinking-only modifier remains. Token-by-token Ainu Latin/Kana alignment passed for both messages; the two scripts encode the same wording and argument roles.

- `proposals.json`: candidates, literal backtranslations, per-clause provenance, argument roles, remaining review questions and validation
- `full-catalogue-evidence.json`: exact English-aligned source clauses and catalogue counts
- `targeted-practical-search.json`: additional primary-source search counts and relevant example IDs

The source snapshot is commit 5bf82b67199aaecbd341a8b150a887f8d60b5567. PR29 head ea60a00001d766674cbd6b91da791894af5ea624 is parent-provided context, not an independently rechecked publication state in this pass.
