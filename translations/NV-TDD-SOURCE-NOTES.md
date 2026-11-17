# Navajo / Tai Nüa bounded follow-up

Base: `c8f565c480df47926ae6c0a576ba1db1d1fc7c06`. This pass adds four labels, not a complete or native-certified translation. With 719 canonical typed slots, Navajo missing slots decrease 327 → 324 and Tai Nüa 321 → 320.

## Source and consumer review

- Navajo `ui_search34`: exact `hanishtá` from [MediaWiki nv, pinned revision](https://github.com/wikimedia/mediawiki/blob/377002822b34077904f4e83c21faaf69d1bfea9a/languages/i18n/nv.json), `sp-contributions-submit`. The app uses it as a gallery search hint and submit button. The different title-exact-search label was not substituted. Existing MediaWiki attribution and GPL notices continue to apply.
- Navajo filename sort labels reuse the existing `save20_file_name` noun unchanged and append A–Z / Z–A ordering notation. No new sentence grammar is claimed.
- Tai Nüa wheel: Luo Yongxian, *A dictionary of Dehong, Southwest China* (1999), Pacific Linguistics C-145, printed p. 48 (PDF p. 88), entry `koŋ²`, wheel of a millstone/spinning wheel. [ANU online edition](https://openresearch-repository.anu.edu.au/bitstreams/1b27afe2-adda-4fe2-95bf-5402206be010/download), CC BY-SA 4.0, ©1999 Pacific Linguistics and/or the author(s). This lexical word is used metaphorically for the palette wheel, not represented as a source-attested software phrase. No dictionary page or prose is reproduced in the app.
- Tai Le historical diaeresis mapping to U+1970 is supported by [Unicode L2/2024/24098](https://www.unicode.org/L2/L2024/24098-tai-le-update.pdf) and [Unicode chapter 16](https://unicode.org/versions/Unicode17.0.0/core-spec/chapter-16/). The resulting sequence is U+1950 U+1968 U+1952 U+1970. The mapping is based on the old mark, not a blanket assumption that historical tone numbers equal Unicode names.

