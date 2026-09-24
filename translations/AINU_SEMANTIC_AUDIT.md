# Ainu catalogue semantic audit — 24 September 2026

Both canonical Ainu catalogues now contain 669 string entries and the required
crop-preview plural forms. The remaining mixed English explanatory passages have
been rewritten in both Latin and Kana: memory warnings, codec descriptions,
recovery guidance, drawing and colour controls, vertical-text instructions,
gallery requirements, and the complete older ten-paragraph manual. The active
main help, cursor help and seven-paragraph assembly help were completed in the
preceding pass and kept consistent with the final control captions.

This is completed resource and prose work with source-based semantic review.
It is not a claim of native-speaker certification or a universal Ainu software
terminology standard. Person marking, register and idiomatic preference can
still benefit from fluent-speaker feedback; those ordinary review limits are
not a reason to leave English instructions in place.

## Scope and retained meaning

The English sources and both complete catalogues were read. An independent
second review compared all newly authored batches, the complete older manual,
and the inherited resource values. Its concrete corrections were applied before
this report was updated. The plural forms were also inspected and rewritten.

- Memory messages distinguish an editing limit from installed RAM, include the
  complete image and temporary loading/editing space, stop before unsafe
  allocation, and preserve the no-automatic-resize and unchanged-source clauses.
  Smaller output still may need the full source image or tiles decoded first.
- Codec descriptions retain first-frame/default-poster behavior, lossless versus
  detail-losing output, quality controls, colour-profile handling, unprotected PDF
  copies, and all dimensions, limits and format identifiers.
- Recovery text distinguishes the previous retained work, the current drawing,
  uncommitted selections, undo history and a separate exported ZIP. It preserves
  the `canvas.png` recovery instruction and the actual File menu captions.
- Assembly text preserves all placement/cropping gestures, alignment and
  non-overlap rules, proportional resizing, unplace/remove effects, restoration,
  output-size limits, and the unchanged original files.
- Drawing and colour instructions preserve exact gesture counts, side/corner
  handles, stroke versus cursor-marker size, palette behavior, selected colours,
  numeric controls and all original radius/size constraints.
- Vertical instructions distinguish 90° rotated joined words from upright
  individual characters, preserve combining marks and emoji sequences, and
  explain that a new line creates another top-to-bottom writing area.
- Gallery text retains named creators, ownership/source notices, modification
  descriptions, licence requirements and the actual File → About → Image credits
  route. Irasutoya's commercial 21-image threshold is mandatory; special
  collaboration conditions remain conditional.

Product, licence and format names, units, colour-model components, script names,
filenames and syntax remain recognizable. `Large PNG download` is the exact
external website button. These retained identifiers are not untranslated English
sentences and are not respelled as arbitrary Kana. ASCII art has a descriptive
Ainu label using the unchanged ASCII identifier.

## Lexical evidence and semantic repairs

The primary traditional source is the National Ainu Museum's searchable Kayano
and Tamura dictionaries. These establish meanings and dialectal usage, not an
official modern computing vocabulary. Dictionary examples and corpora were not
copied into the application.

| Application meaning | Wording / evidence | Repair |
| --- | --- | --- |
| Right and left sides | [simoysam](https://ainugo.nam.go.jp/dic?word=simoysam), [harkisam](https://ainugo.nam.go.jp/dic?word=harki) | `sam` only means side/beside; `harkiso` names a hearth seat. Valid beside-uses of `sam` remain. |
| Corner and rectangular shape | [sikkew](https://ainugo.nam.go.jp/dic?word=sikkew), [osikkewnu](https://ainugo.nam.go.jp/dic?word=osikkewnu) | Replaced baggage/eye vocabulary. The square caption specifies equal width and height. |
| Restore an image | [hosipire](https://ainugo.nam.go.jp/dic?word=hosipire) | Replaced `uepeker`, identified as a prose-folktale genre by [NINJAL](https://ainu.ninjal.ac.jp/folklore/en/). |
| Record changes in credits | [nuye](https://ainugo.nam.go.jp/dic?word=nuye) | Replaced the same folktale error with writing/recording. |
| Open / wait | [maka](https://ainugo.nam.go.jp/dic?word=maka), [tere](https://ainugo.nam.go.jp/dic?word=tere) | Replaced unsupported catalogue forms `neire` and `isamne`. File/panel opening is a software extension. |
| Reverse / exchange / rotate | [ehorka](https://ainugo.nam.go.jp/dic?word=ehorka), [itasare](https://ainugo.nam.go.jp/dic?word=itasare), [kiru](https://ainugo.nam.go.jp/dic?word=kiru) | Distinguishes reversal and replacement from interrupting or rotating. |
| Two fingers | [askepet](https://ainugo.nam.go.jp/dic?word=askepet) | Replaces `tu tek`, which meant two hands. |
| Make smaller | [ponte](https://ainugo.nam.go.jp/dic?word=ponte) | Replaces [ponre](https://ainugo.nam.go.jp/dic?word=ponre), nickname. |
| Send an image | [eikra](https://ainugo.nam.go.jp/dic?word=eikra) | Uses the sending-an-object sense, extended to digital images. |
| Move the view | [moymoye](https://ainugo.nam.go.jp/dic?word=moymoye) | Uses moving something. Existing `raye` also has genuine movement senses and was not rejected from a homonym alone. |
| Image information / conditions | [oruspe](https://ainugo.nam.go.jp/dic?word=oruspe), [irenka](https://ainugo.nam.go.jp/dic?word=irenka) | Uses the matters-concerning-something and rule/promise senses. The legal licence itself is not replaced. |
| Curved / round | [rewke](https://ainugo.nam.go.jp/dic?word=rewke), [sikari](https://ainugo.nam.go.jp/dic?word=sikari) | Shape controls use descriptive Ainu properties and actions. |
| Copper / silver | [hurekane](https://ainugo.nam.go.jp/dic?word=hurekane), [sirokane](https://ainugo.nam.go.jp/dic?word=sirokane) | Uses documented colour/material vocabulary. |
| Insufficient | [ehaye](https://ainugo.nam.go.jp/dic?word=ehaye) | Uses shortage wording for RAM. `kon rusuy` is a complete requirement phrase; `kon` alone was not treated as insufficient. |

Arrow, star and heart use the museum-attested `ay`, `nociw` and `sampe`. Empty
colour slots use absence (`isam`), not dryness (`sat`). Fewer selected files now
means a smaller file count, not smaller individual files. Horizontal text uses
explicit left-to-right direction; sideways vertical words explicitly rotate 90°.

## Published community computing vocabulary

Traditional dictionary absence alone is not evidence against modern usage.
These primary community pages establish actual published forms and meanings:

| Form | Documented use | Source |
| --- | --- | --- |
| `saysu` | Size, explicitly identified as a modern loan | [saysu](https://itak.aynu.org/saysu) |
| `tatum` | Data; also used in the collection's own interface | [tatum](https://itak.aynu.org/tatum) |
| `sinna`, `isina` | Computing change/diff and limitation | [sinna](https://itak.aynu.org/sinna) |
| `husko katukar` | Undo, with the published word spacing | [husko](https://itak.aynu.org/husko) |
| `nure`, `sanke` | Load and export | [community collection](https://ss1.xrea.com/toracatman.s324.xrea.com/ainu/dictionary.html), linked `js/ainu.js` and `js/source.js` |
| `raye`, `nuye`, `hontomotuye` | Move, edit and cancel | [ye](https://itak.aynu.org/ye) |
| `irukay`, `irukaypo an` | Brief duration / temporary modifier | [irukay](https://itak.aynu.org/irukay) |
| `nokan`, `komke` | Fine/detailed versus invalid | [nokan](https://itak.aynu.org/nokan), [komke](https://itak.aynu.org/komke) |
| `hayta` | Computing error/failure | [hayta](https://itak.aynu.org/hayta) |
| `itaktupte` | Translation, attributed to Oota | [tak](https://itak.aynu.org/tak) |
| `ipe`, `owpeka` | Content and valid in computing | [ipe](https://itak.aynu.org/ipe), [owpeka](https://itak.aynu.org/owpeka) |
| `iosno` | Last / most recent | [ios](https://itak.aynu.org/ios) |

The community collection also documents `cinuyep` (file), `iyanu` (settings),
`sonep` (category), `uesere` (licence), `attupte` (copy), and `nikamkorinuyep`
(pencil), with contributor/source labels. Its `pororu`, `pararu` and `riru`
dimension terms are explicitly **published community neologisms**, not asserted
here to be universally established traditional nouns. It identifies different
sources and dialectal proposals rather than claiming an absolute standard.
Historical loans such as `hunte` and `sirokane` are documented Ainu vocabulary;
Japanese origin does not make an established Ainu loan an untranslated template.

New technical explanations use ordinary clauses rather than claiming invented
standard compounds. Decoding is described as making an image from file data,
encoding as making an image file, and buffers as temporary space used for loading
or editing. RAM remains a technical identifier. Lossless storage keeps each
pixel's colour unchanged; raising quality preserves more fine detail. Serif
controls describe the presence/absence of small terminal strokes. These are
contextual compositions and remain open to idiomatic refinement.

## Grammar, paired scripts and review corrections

[NINJAL's introduction](https://ainu.ninjal.ac.jp/folklore/en/) and the museum's
[grammar introduction](https://ainugo.nam.go.jp/pages/ainu_basic.html) supply the
word-order, person-marking and verb-valency framework. Direct instructions use
imperatives, including the attested polite [yan](https://ainugo.nam.go.jp/dic?word=yan).
Explicit third-person subjects such as Android are distinguished from impersonal
transitive `a=` constructions. These sources support selected forms; they do not
certify every composed sentence as the only idiomatic option.

Kana represents the authored Ainu, with product/format identifiers protected.
Ainu person prefixes are rendered in Kana rather than left as Latin A/E markers.
The chosen small-ッ spelling for doubled consonants follows NINJAL's explicit
pp/tt/kk guidance and museum examples; true final consonants retain their Ainu
small-letter forms. `wakka` is also written ワッカ in the Foundation's
[primary introductory textbook](https://www.ff-ainu.or.jp/web/potal_site/files/ishikari_shokyu.pdf).
The earlier erroneous conversions of English fragments (`Use`, `Save as`, `Other`)
were replaced by actual translated control captions.

Independent review produced substantive fixes: uncommitted versus unpositioned
selections; freeing some storage rather than deleting all files; straight versus
merely long lines; glyph tilt versus moving text; cursor markers versus brush
strokes; a rectangular square with equal dimensions; unprotected versus merely
passwordless PDF files; quality-setting linkage; explicit hex controls; the
actual second edit row; ownership notices; and most-recently-used category tools.

## Licence evidence

Credit requirements were checked against the
[CC BY-SA 4.0 deed](https://creativecommons.org/licenses/by-sa/4.0/deed.en).
Irasutoya's [terms](https://www.irasutoya.com/p/terms.html) and
[FAQ](https://www.irasutoya.com/p/faq.html) establish the commercial 21-image
threshold and possible separate collaboration conditions.
[Openclipart's source policy](https://openclipart.org/share) supplies CC0.
The Ainu interface explains these requirements; the full licence identifiers and
legal texts remain available through the app's existing panels.

## Validation

Both scripts pass complete-catalogue validation, Android string validation,
format-placeholder and protected-literal checks. All 27 translation tests pass
with the integrated literal-percent validator. Both catalogues also compile with
strict SDK 35 AAPT2. Static percent text uses `formatted="false"`; percent signs
in strings with actual format arguments use `%%`.
No resource keys, plural quantities, placeholders or licence identifiers were
removed. The cursor-help alias resolves to the intended resource. Both scripts
contain their actual About caption in all three globally checked help passages.
No editing-template references remain. A residual Latin-token scan was reviewed
against retained identifiers; crop-preview plural text was checked as well.
`git diff --check` passes.

These are source and structural checks, plus the described semantic review.
They are not a claim of device-layout verification, native-speaker certification,
or a new official terminology standard.
