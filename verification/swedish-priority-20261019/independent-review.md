# Independent Swedish challenge and final implementation readback

## Review scope and evidence boundary

A separate model-based linguistic reviewer read all 193 complete draft pairs: 92 P0, 100 P1 and one P2 composition dependency. This includes 103 pre-existing Swedish values and 90 proposed additions. It checked meaning, grammar, idiom and the relevant Save/Export/Share, dimensions, animation, recovery, credits, accessibility and undo-cache source consumers. This was a review of the draft proposal, not a native-speaker certification or a review cryptographically bound to later final source bytes.

The implementation author applied the findings. A separate coordinating readback then independently verified final Swedish XML Git blob `1091273745864fdf74e767152f545c62300dc203` and equality of all 193 final ledger values with that XML. It explicitly checked every changed phrase listed below and the retained Main uncertainty. This later step is implementation readback of the linguistic findings; it is not relabelled as a second full linguistic review, runtime test or native-speaker review.

## Findings applied

1. `ui_the_encoder_did_not_finish`: `Kodaren slutfördes inte.` wrongly describes the encoder itself as incomplete. Final: `Kodningen slutfördes inte.`
2. `save20_file_format`: existing `Bildformat` is too narrow in the shared Save/Export form, which includes Base64 and ASCII text. Final: `Filformat`.
3. `ui_autosave_is_paused_to_protect_that_draft_use`: its embedded field reference now uses `(Filformat: PNG / JPEG)` to match that label.
4. `save20_gif_description`: final complete value uses `Färgutjämning` to match the existing option and explicitly describes opening an animated GIF as its first frame. `Gitter` is an attested Swedish term; this was consistency/idiom improvement, not a claim that the word is wrong.
5. `ui_pixels_6ec9c2`: lowercase `bildpunkter` is appropriate inside composed descriptions; standalone `ui_pixels` stays `Bildpunkter`.
6. `ui_percent`: standalone `Procent` now matches the capitalized companion radio label; composed `ui_percent_fd8671` remains lowercase.
7. `ui_the_image_was_saved_but_android_could_not`: `delningsdialogen` identifies the sharing dialog idiomatically while preserving successful saving and failed opening.
8. `ui_sampled_resize_memory_explanation`: `den aktuella ritytan, urklippets innehåll, avkodning med nedsampling samt redigeringsbuffertar` fixes the list and explicitly names clipboard contents. Variable memory, detail loss and unchanged original remain intact.
9. `ui_cannot_create_the_undo_cache_free_some_device`: `Cachen för ångrahistoriken kan inte skapas. Frigör lagringsutrymme på enheten och försök igen.` replaces the ungrammatical `för ångra` and fits the on-disk RasterHistory cache.
10. `ui_the_undo_cache_is_damaged`: `Cachen för ångrahistoriken är skadad.`
11. `ui_unexpected_data_in_the_undo_cache`: `Oväntade data i cachen för ångrahistoriken.`

No additional substantive recovery/credit semantics defect was found in the remaining draft values. The reviewer found `källangivelser`, `ångrahistorik`, `bildmontage`, first-frame import and separate-PNG-poster meanings sound within this bounded source context.

## Open uncertainty

`ui_main23` remains `Huvud`. This is awkward standalone Swedish, but no current production consumer establishes the intended sense of Main. Possible replacements such as Huvudmeny, Start or Allmänt would guess at missing context. It is retained as uncertain, with no accepted-current credit. Contextless entries are not claimed to have UI validation.

## Reconciled outcome

The final ledger records 90 new translations, 18 corrected existing values, 84 retained values and one uncertain retained value. These describe the bounded work, not PR56 counter imports. No other language, held processing label, CN Help or Hakka/Wu value was changed. No native-speaker, installed UI, TalkBack, release or whole-language approval follows from this review.
