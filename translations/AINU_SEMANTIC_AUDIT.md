# Ainu catalogue semantic audit — 23 September 2026

This review covers the Latin and Kana canonical catalogues together. Both contain
all current resource keys, but that is **resource coverage, not a certification
of complete or fluent Ainu**. The full catalogues, including the long editor,
assembly, recovery and insertion instructions, were read against their English
sources. This change repairs verifiable semantic errors and navigation references.
The remaining mixed English/Ainu prose requires a fluent Ainu reviewer; it must
not be described as a finished native-language translation.

## Evidence and corrections

The primary lexical source is the National Ainu Museum's searchable editions of
Shigeru Kayano's and Suzuko Tamura's dictionaries, with dialect and author
identified per entry. These are lexical evidence, not an official software
terminology standard. No dictionary examples or corpus were copied into the app.
The new software uses of ordinary words below are contextual translations.

| Meaning in AN Paint | Corrected Latin / Kana wording | Evidence and reason |
| --- | --- | --- |
| Right side | `simoysam` / `シモイサㇺ` | [Museum: simoysam](https://ainugo.nam.go.jp/dic?word=simoysam). The old `sam` means side/beside without specifying right. Uses genuinely meaning “beside” remain. |
| Left side | `harkisam` / `ハㇻキサㇺ` | [Museum: harki](https://ainugo.nam.go.jp/dic?word=harki). The old `harkiso` names a particular hearth seat, unsuitable for a screen coordinate. |
| Corner | `sikkew` / `シッケウ` | [Museum: sikkew](https://ainugo.nam.go.jp/dic?word=sikkew). The old `sike` means baggage, not a corner. |
| Square handles | `osikkewnu` / `オシッケウヌ` | [Museum: osikkewnu](https://ainugo.nam.go.jp/dic?word=osikkewnu). The old `sik` does not mean square. |
| Restore a retained image | Forms of `hosipire` / `ホシピレ` | [Museum: hosipire](https://ainugo.nam.go.jp/dic?word=hosipire). [NINJAL's folklore introduction](https://ainu.ninjal.ac.jp/folklore/en/) identifies `uepeker` as prose folktale; it was incorrectly used for recovery. |
| Record modifications in credits | `nuye` / `ヌイェ` | [Museum: nuye](https://ainugo.nam.go.jp/dic?word=nuye), writing/recording sense. Folktale vocabulary also appeared in the instruction to indicate modifications. |
| Open a document or panel | `maka` / `マカ` | [Museum: maka](https://ainugo.nam.go.jp/dic?word=maka), opening sense. Replaces the unsupported `neire` in this catalogue. Applying it to files is a software extension. |
| Wait for the current operation | `tere` / `テレ` | [Museum: tere](https://ainugo.nam.go.jp/dic?word=tere). Replaces `isamne`. |
| Reverse colours or the tool arrow | `ehorka` / `エホㇿカ` | [Museum: ehorka](https://ainugo.nam.go.jp/dic?word=ehorka), reverse/opposite sense. The old `hontomotuye` means interrupt/stop, and remains the Cancel caption. |
| Swap colours, light/dark characters, or opposite sides | `itasare` / `イタサレ` | [Museum: itasare](https://ainugo.nam.go.jp/dic?word=itasare), exchange sense. Flip labels explicitly identify the exchanged sides. |
| Rotate | `kiru` / `キル` | [Museum: kiru](https://ainugo.nam.go.jp/dic?word=kiru), turn/change direction sense. The 90° control specifies the right side; the angle is retained. |
| Arrow, star, heart | `ay`, `nociw`, `sampe` / `アイ`, `ノチウ`, `サンペ` | Museum entries for [ay](https://ainugo.nam.go.jp/dic?word=ay), [nociw](https://ainugo.nam.go.jp/dic?word=nociw), and [sampe](https://ainugo.nam.go.jp/dic?word=sampe). The same terms appear in their drawing instructions. |

Directions were reviewed in the alignment labels, crop/resize descriptions,
attachment instructions, palette help and both vertical column-order choices.
The words for left and right were not substituted globally: `sam` beside an
image, tab or button is a valid different meaning.

The Advanced caption uses `Na poronno` (more), replacing the misleading `Na komke`.
The text-direction caption describes the manner of writing rather than using
`hosipi` (return). The portrait tool-strip description now names its left-to-right
course instead of saying “toward the heart”. These are descriptive application
phrases and still warrant speaker review.

## Paired script and navigation repairs

Help now refers to the actual localized captions for File, Draw, Drawing, Insert,
Other images, Load image, Save, Save as, Export recovery copy, Use image, Copy
credit, and the selection/assembly controls. The credits path is File → About,
licences & credits → Image credits, matching the active editor. Both script
catalogues use the same semantic paths.

The Kana catalogue previously converted pieces of English words as if they were
Ainu syllables: `Use image` became `ウセ image`, `Save as` became `Save アㇱ`, and
`Other images` became `オッヘㇾ images`. These app-control references now use their
Kana resource captions. Remaining technical English is retained visibly as
English; converting its letters to arbitrary Kana would not translate it.
The `tu` notation was normalized to `トゥ`, as in the museum examples, and the
font sample retains its intended `Aa Bb` case comparison.

The existing community-sourced Brush, Save and Done labels remain. Historical
loans such as `hunte` are documented Ainu vocabulary and must not be rejected
merely because they have Japanese origins. Similarly, a traditional dictionary's
absence of a software sense does not alone disprove modern community usage.
For example, the modern community glossary attributes `hayta` in the failure
sense to Oota; this review does not classify it as an error solely from the
traditional meanings. The existing source history remains in README.md.

## Remaining review required

The following are concrete outstanding language issues, not build failures:

- Long passages still mix English terms such as `bounding box`, `stroke`, `aspect
  ratio`, `working buffer` and `resize` with Ainu clauses. Several tool captions
  also remain English. They need consistent community terminology and a fluent
  rewrite, not a script converter or a word-replacement pass.
- Modern terms and constructions such as `iyanu`, `sinna`, `tatum`, `saysu`,
  `sampes` and `huskokatukar` need provenance and context review. A borrowed term,
  a semantic extension and an invented string of dictionary words are different
  things; this audit cannot settle every one of those cases.
- Person marking, verb valency, number, register and sentence-level naturalness
  need checking throughout both versions. Matching Latin/Kana labels does not
  validate the grammar of the surrounding instructions.
- The Kana catalogue still contains Latin technical English. Its presence must
  not be hidden by claiming all text is native Ainu. The in-app language note now
  states that Ainu and English are both present.

## Validation

Both Ainu catalogues pass `validate_catalogue(tag, require_complete=True)` and
Android string validation, including placeholders and protected literals. No
keys, plurals, format identifiers or licence identifiers were removed.
`git diff --check` passes. Source inspection also checked the new credits and
insertion paths against the editor's menus.

The full translation unittest run on the starting worktree reports existing
Hakka directory/literal and Manchu Base64-literal failures that belong to other
parallel integration changes; none concern these Ainu edits. Run the complete
suite again on the combined integration branch. No fluency score is inferred
from these structural checks.
