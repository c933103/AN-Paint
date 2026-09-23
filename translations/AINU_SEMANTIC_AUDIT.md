# Ainu catalogue semantic audit — 23 September 2026

This review covers the Latin and Kana canonical catalogues together. Both contain
all current resource keys, but that is **resource coverage, not a certification
of complete or fluent Ainu**. The full catalogues, including the long editor,
assembly, recovery and insertion instructions, were read against their English
sources. The first pass repairs verifiable semantic errors and navigation
references. The second rewrites the active main help, cursor instructions,
assembly instructions, and gallery credit requirements in paired Ainu clauses.
This is a substantive repair, not a finished native-speaker certification: other
active messages and the older help resource still contain mixed English/Ainu.

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
| Two fingers | `tu askepet` / `トゥ アㇱケペッ` | [Museum: askepet](https://ainugo.nam.go.jp/dic?word=askepet). The old `tu tek` means two hands, not the pinch gesture's two fingers. |
| Make smaller | `ponte` / `ポンテ` | [Museum: ponte](https://ainugo.nam.go.jp/dic?word=ponte) includes the small-making construction; [ponre](https://ainugo.nam.go.jp/dic?word=ponre) is a nickname, not a reduce command. |
| Send an image | `eikra` / `エイㇰラ` | [Museum: eikra](https://ainugo.nam.go.jp/dic?word=eikra), send an object. The digital use is an application extension, replacing unsupported `ukopaye` here. |
| Move the view or a placed image | `moymoye` / `モイモイェ` | [Museum: moymoye](https://ainugo.nam.go.jp/dic?word=moymoye), move something. The Navigate caption describes moving and looking. |
| Information concerning an image | `noka oruspe` / `ノカ オルㇱペ` | [Museum: oruspe](https://ainugo.nam.go.jp/dic?word=oruspe), the broad matters/circumstances-about-something sense, not the separate narrow rumour sense. |
| Conditions of use | `irenka` / `イレンカ` | [Museum: irenka](https://ainugo.nam.go.jp/dic?word=irenka), the rule/promise sense. This does not translate or replace the legal licence text. |

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

## Active instruction rewrite

The second pass rewrites `ui_help23`, `ui_cursor_help31` and its gesture/marker
hints, `ui_add_up_to_20_images_with_android_s`, `gallery_description`, the credit
editor hint, and the Catrobat, Irasutoya and Openclipart instructions. Kana was
authored alongside the Latin text; English letters were not transliterated as
if that would produce Ainu. The app calls the first two help resources from
`ClassicPaintActivity` and the assembly resource from `AssemblyActivity`.

The assembly instructions retain the 20-image limit, provider-dependent metadata,
sorting, individual/batch crop, preview, attachment alignment, origin coordinates,
non-overlap rule, proportional resizing, unplace/remove behavior, undo/redo,
navigation, export, memory fallback, original-file preservation, and restoration.
The final paragraph names the actual File → About panel. Cursor instructions
distinguish moving the view, starting/stopping drawing, and marker enlargement
that does not change the brush size.

[NINJAL's grammatical introduction](https://ainu.ninjal.ac.jp/folklore/) supplies
the basic word-order/person-marking framework. The instructions use direct
imperatives, including polite `yan`, whose imperative use is documented by the
[museum](https://ainugo.nam.go.jp/dic?word=yan). These sources support the selected
forms; they do not establish that every newly composed sentence is idiomatic.

Modern software vocabulary also needs a source beyond traditional dictionaries.
The [community terminology collection](https://ss1.xrea.com/toracatman.s324.xrea.com/ainu/dictionary.html)
and its linked `js/ainu.js`/`js/source.js` identify their contributors and source
classes. It explicitly warns that its proposals are not absolute answers. This
pass uses its documented `cinuyep` (file), `iyanu` (settings), `sonep` (category),
`uesere` (licence), and `attupte` (copy); the collection attributes the latter and
category terminology to Oota. Its English/Japanese language labels are
`Inkiriskur itak` and `Sisam itak`. The dimension labels `pororu`, `pararu` and
`riru` are **published community neologisms**, explicitly classified as such by
that collection, not claimed here as universally established Ainu terms.

Technical identifiers remain recognizable: Android, Catrobat, Irasutoya,
Openclipart, PNG, ICO, ASCII art, Base64, CC0, CC BY-SA 4.0, URL, and x/y. The
external button `Large PNG download` remains exact. `commercial design` remains
a visibly quoted external legal category. Cursor, pixel, percent, zoom and
memory terminology still need a consistent community terminology decision;
their presence is not a claim of established Ainu loanword status.

The credit instructions preserve attribution, source/owner notices, modification
indication, and ShareAlike or compatible-licence requirements, checked against
the [CC BY-SA 4.0 deed](https://creativecommons.org/licenses/by-sa/4.0/deed.en).
Irasutoya's [terms](https://www.irasutoya.com/p/terms.html) and
[FAQ](https://www.irasutoya.com/p/faq.html) retain the commercial-use threshold of
21 images and the possibility of separate collaboration conditions.
[Openclipart's source policy](https://openclipart.org/share) supplies CC0.

## Remaining review required

The following are concrete outstanding language issues, not build failures:

- Active memory/codec instructions still mix English technical phrases with
  Ainu, particularly `ui_d_d_pixels_2f_mp_exceeds_the_current`,
  `ui_estimates_include_the_current_canvas_and_clipboard_sampled`,
  `ui_the_decoder_and_editing_buffers_need_about_the`,
  `ui_the_full_image_and_working_buffers_exceed_the`,
  `ui_codec_resize_memory_floor` and `ui_no_resize_fits_decoder_memory`.
- Several active captions and short descriptions retain `Crop`, `Draft`,
  `Resize`, `Export`, `Quality`, `Aspect ratio`, `Pencil`, `Airbrush`, and
  `Watercolor`. Tool descriptions still contain `bounding box` and `stroke`.
  The older, currently uncalled help resource
  `ui_the_arrow_on_the_left_directly_below_the` remains substantially mixed;
  only its navigation, script consistency and verified vocabulary were repaired.
  These need consistent community terminology and a fluent rewrite.
- Existing terms and constructions such as `sinna`, `tatum`, `saysu`, `sampes`
  and `huskokatukar` need provenance and context review. Sourced modern terms
  such as `iyanu` also need sentence-level review. A borrowed term,
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
insertion paths against the editor's menus. Both scripts include the actual
current About caption in the Catrobat, assembly and older help resources checked
by the integrated navigation regression. All template caption references used
while editing have been expanded; none remain in the XML.

The full translation unittest run on the starting worktree reports existing
Hakka directory/literal and Manchu Base64-literal failures that belong to other
parallel integration changes; none concern these Ainu edits. Run the complete
suite again on the combined integration branch. No fluency score is inferred
from these structural checks.
