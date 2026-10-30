# Batch 1 — common controls and save/destruction distinctions

Read `00-conventions.md`. Each row is a candidate for **each** named locale; none is accepted. English is source-bound. Confidence is ang/non. Backtranslations spell out intended meaning, not independent proof.

| Key | Tier | Exact English | ang candidate | ang backtranslation | non candidate | non backtranslation | Rationale | Confidence |
|---|---|---|---|---|---|---|---|---|
| ui_save | P0 | Save | Healdan | Keep/save | Varðveita | Preserve/save | A,N,S: disk-save extension | M/M |
| ui_save_a5d0d9 | P0 | Save… | Healdan… | Keep/save… | Varðveita… | Preserve/save… | Same action; ellipsis retained | M/M |
| ui_save_as | P0 | Save as %1$s | Healdan swa %1$s | Save as %1$s | Varðveita sem %1$s | Save as %1$s | N,S,P: format placeholder | M/M |
| ui_save_as_jpeg | P0 | Save as JPEG… | Healdan swa JPEG… | Save as JPEG… | Varðveita sem JPEG… | Save as JPEG… | S: literal format | M/M |
| ui_save_as_jpeg_xl | P0 | Save as JPEG XL… | Healdan swa JPEG XL… | Save as JPEG XL… | Varðveita sem JPEG XL… | Save as JPEG XL… | JPEG XL distinct from JPEG | M/M |
| ui_save_as_png | P0 | Save as PNG… | Healdan swa PNG… | Save as PNG… | Varðveita sem PNG… | Save as PNG… | S: literal format | M/M |
| ui_save_png | P0 | Save PNG | Healdan PNG | Save PNG | Varðveita PNG | Save PNG | S: not export wording | M/M |
| ui_save_your_changes | P0 | Save your changes? | Healdan þine awendinga? | Save your alterations? | Varðveita breytingar þínar? | Save your alterations? | N,S: explicit object and question | M/M |
| ui_saved | P0 | Saved %1$s | Gehealden: %1$s | Saved: %1$s | Varðveitt: %1$s | Saved: %1$s | P: avoids inflecting unknown placeholder | M/M |
| ui_save_and_share | P0 | Save and share… | Healdan and dælan… | Save and share… | Varðveita ok deila… | Save and share… | N,S: both actions, in order | M/M |
| ui_save_and_share_41edb4 | P0 | Save and share | Healdan and dælan | Save and share | Varðveita ok deila | Save and share | Same distinction without ellipsis | M/M |
| ui_could_not_save_image | P0 | Could not save image | Ne mihte man þa anlicnesse healdan | The image could not be saved | Eigi mátti varðveita myndina | It was not possible to save the image | S: failure, not success | M/M |
| ui_discard | P0 | Discard | Forlætan | Abandon | Kasta brott | Cast away | S: distinct from cancel | M/M |
| ui_discard_changes23 | P0 | Discard changes | Forlætan þa awendinga | Abandon the alterations | Kasta breytingum brott | Cast away the alterations | S: dative with kasta; no save implied | M/M |
| ui_keep_editing23 | P0 | Keep editing | Forð awendan | Continue altering | Halda áfram at breyta | Continue altering | G: continuation idiom requires review | L/L |
| ui_clear_all | P0 | Clear all | Eall adilegian | Erase all | Má allt brott | Erase everything | S: destructive clear, not cancel | M/M |
| ui_clear_image | P0 | Clear image | Adilegian þa anlicnesse | Erase the image | Má myndina brott | Erase the image | S: object explicit | M/M |
| ui_your_current_image_has_unsaved_changes | P0 | Your current image has unsaved changes. | On þinre andweardan anlicnesse sind awendinga þe ne sind gehealdene. | In your current image are alterations that are not saved. | Í myndinni er þú vinnr nú eru breytingar er eigi eru varðveittar. | In the image you are working on now are alterations that are not saved. | S,G: preserves current/unsaved; relative syntax provisional | L/L |
| ui_draft_not_saved_yet | P0 | Draft not saved yet | Weorcgewrit ne is giet gehealden | Working draft is not saved yet | Vinnurit er enn eigi varðveitt | Working draft is not saved yet | N,S: draft not final image | L/L |
| ui_draft_saved | P0 | Draft saved | Weorcgewrit gehealden | Working draft saved | Vinnurit varðveitt | Working draft saved | N,S: draft-specific state | L/L |
| ui_draft_restored | P0 | Draft restored | Weorcgewrit eft gestaþelod | Working draft restored again | Vinnurit aptr fengit | Working draft recovered | N,S,G: restoration not merely saved | L/L |
| ui_export_recovery_copy | P0 | Export recovery copy… | Utberan efenwyrhte to eftstaþelunge… | Export a copy for restoration… | Fœra út eptirrit til viðgerðar… | Export a copy for restoration… | N,S: separate recovery export | L/L |
| ui_export_recovery_copy_144b8a | P0 | Export recovery copy | Utberan efenwyrhte to eftstaþelunge | Export a copy for restoration | Fœra út eptirrit til viðgerðar | Export a copy for restoration | Same action, no ellipsis | L/L |
| ui_could_not_export_the_recovery_copy | P0 | Could not export the recovery copy | Ne mihte man utberan þa efenwyrhte to eftstaþelunge | Could not export the restoration copy | Eigi mátti fœra út eptirritit til viðgerðar | Could not export the restoration copy | N,S: export failure | L/L |
| ui_export_as23 | P1 | Export as… | Utberan swa… | Export as… | Fœra út sem… | Export as… | N,S: not save-as | M/M |
| ui_cancel | P1 | Cancel | Ablinnan | Cease this action | Hætta við | Cease this action | A,S,G: not discard; Norse idiom review | M/L |
| ui_done | P1 | Done | Gedon | Done | Lokit | Finished | A: completion | M/M |
| ui_ok | P1 | OK | Swa beo hit | Let it be so | Svá sé | Let it be so | A,N: confirmation; no deletion implied | M/M |
| ui_new | P1 | New… | Niwe… | New… | Nýtt… | New… | A: neuter elliptical object | M/M |
| ui_new_image | P1 | New image | Niwe anlicnes | New image | Ný mynd | New image | A: feminine agreement | M/M |
| ui_load_image | P1 | Load image… | Inlædan anlicnesse… | Bring an image in… | Fœra mynd inn… | Bring an image in… | N: loading, not save/export | M/M |
| ui_undo | P1 | Undo | Undon | Undo | Gera aptr ógert | Make undone again | A,N,G: Norse periphrasis rather than modern afturkalla | M/L |
| ui_redo | P1 | Redo | Eft don | Do again | Gera aptr | Do again | S: paired with undo, not recovery | M/M |
| ui_menu_file | P1 | File | Gewrit | Written item/file | Rit | Written item/file | N: file sense, not claim of text-only file | L/L |
| ui_menu_edit | P1 | Edit | Awendan | Alter | Breyta | Alter | A,N: not proofread-only | M/M |
| ui_menu_image | P1 | Image | Anlicnes | Image/likeness | Mynd | Image | A,N: raster extension | M/M |
| ui_menu_view | P1 | View | Gesihþ | View/sight | Sýn | View/sight | A,N: view menu | M/M |
| ui_menu_help | P1 | Help | Help | Help | Hjálp | Help | A: OE Help is genuinely historical, not an English fallback | M/M |
| ui_menu_colours | P1 | Colors | Hiwu | Colours/forms | Litir | Colours | A,N: OE hiw has multiple senses; review clarity | M/M |
