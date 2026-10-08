# Malay and Indonesian short-string recheck — 6 October 2026

This is a new, bounded source/text review after the 28 September reset. It does
not reinstate the withdrawn PR3/PR4 handoff, certify native fluency, or complete
the other languages or the full localization register.

## Snapshot and exact review population

Original PR3 branch: `translation/fil-ceb-ms-id`, starting at
`bd08a74b51a718e3a670a5fef250c4311d623c5a`. The worktree was clean and
`git ls-remote origin refs/heads/translation/fil-ceb-ms-id` returned that same
commit before editing. Canonical XML was edited directly; no translation
generator or imported application catalogue was used.

The source is every translatable `<string>` in `values/*.xml`, not only
`values/strings.xml`. This includes `editor33_strings.xml` and
`editor34_strings.xml`. The threshold is **the starting localized XML text's
length after XML entity decoding, at most 100 Unicode characters**, keeping
Android escape sequences such as `\n` literal. Resource aliases count as short
source entries, but their long targets are not thereby reviewed as short prose.

| Starting catalogue | Strings | At most 100 characters | Longer nonmanual strings | Manuals |
| --- | ---: | ---: | ---: | ---: |
| Malay `values-ms` | 669 | 604 | 62 | 3 |
| Indonesian `values-in` | 669 | 600 | 66 | 3 |

The three manuals are `ui_help23`,
`ui_add_up_to_20_images_with_android_s`, and
`ui_the_arrow_on_the_left_directly_below_the`. The 607-key union of both short
sets was read against English and the other locale; this also exposes ten
longer counterpart cells. The [entry-by-entry TSV](pr3-ms-id-short-strings-2026-10-06.tsv)
contains each key, source XML, English, both starting lengths/texts, outcomes,
and resulting texts. Its unchanged entries mean only that this comparison
proposed no additional edit; they are not native-speaker acceptance.

This establishes current-source coverage for the cutoff leads R-014–R-017 and
freshly reproduces the earlier 62/66 arithmetic. It does not reconstruct the
historical audit's unspecified starting snapshot or prove that audit occurred.
R-013's wider language obligations and R-018's PR4 languages remain outside this
pass. The central register's pending statuses are not globally cleared.

Starting XML SHA-256:

- Malay: `0931e2da429df7cc3ee01d8abd1f30fcd0ac603207741f274bb90ad4e916b2d8`
- Indonesian: `c2d137f9692b9df2483c13a50acff97baa19e206de7cdd5bd20fb7f321c0ef4c`

## Corrections and semantic checks

| Case | Current evidence and outcome |
| --- | --- |
| Language picker note, both locales | `AppLanguage.showPicker` displays `language20_translation_note` as its custom title. The localized notes asserted that all translatable interface text was present and omitted both the title and English-fallback behavior from current English. Restored the App language title, resource-maintenance sentence, and new/untranslated-text fallback sentence. This removes a completeness claim from the product. |
| PDF crop, both locales | `PdfCodec.decode` rejects negative/out-of-page edges and `left >= right` **or** `top >= bottom`. It does not inspect whether cropped pixels contain visible marks. Replaced ambiguous “not empty” wording with a rectangle within the selected page whose width **and** height exceed zero. Indonesian is included as the longer counterpart of this short Malay entry and an explicitly requested safety meaning. |
| Malay whole-pixel validation | `CropMargins.rect` in `ImageAssembly.kt` requires `n == floor(n)` unless percentage mode is selected, and rejects a trim larger than its side. Changed `piksel bulat` to an instruction to use whole numbers for pixels, retaining the percentage alternative and image-bound condition. This concerns the number, not the shape of a pixel. |
| Malay memory overhead | `ImageResizeDialog.refresh` labels an editing budget before additional decoder memory is accounted for; the subsequent `memoryRequirements.accepts` check controls acceptance. Replaced the unclear `lebihan dekoder` with explicit additional decoder memory. The number, megapixel unit and both positional placeholders remain intact. |
| Malay text-box background | `TextStyleDialog` binds the checkbox to the background-filled text box. The palette already labels background as `Latar`; the short checkbox still said `BG`. It now names `warna latar`, preserving the operation. |
| Malay assembly recovery route | `ClassicPaintActivity` emits the unavailable-output warning, and its File action is captioned `Gabungkan imej`. The short warning now names that action instead of `Gabungan imej`. No change is made to the separate assembly title. |
| Malay Pencil and Preview captions | Aligned `Pensil` to `Pensel`, the wording in both current Pencil hints and the legacy manual, and `Pralihat` to `Pratonton`, used in the other preview captions/messages. These are bounded terminology-consistency edits, not evidence that every manual sentence is accepted. |
| Draft, Save, Discard, Keep editing | Both locales use `Draf` for the ongoing work. `scheduleAutosave`/`saveDraftIfReady` set pending, saving, saved and error states. `confirmReplacement` has separate Save, Discard changes and Keep editing actions; `Buang perubahan` and `Teruskan menyunting` / `Lanjutkan mengedit` retain different meanings. No additional changes proposed. |
| Cut, Copy, Paste versus Crop | `PaintDocument.cutSelection` copies and then deletes; `copySelection` preserves a transformed selection in the internal clipboard; `paste` creates a floating selection. `Potong`, `Salin`, Malay `Tampal` / Indonesian `Tempel`, and crop `Pangkas` distinguish these operations. The Indonesian clipboard explanation already says `papan klip`; no replacement with Malay `papan keratan` was made. That longer explanation was consulted only for this terminology/context, not counted as a complete long-string review. |
| Indonesian leakage leads | Both cursor-off keys say `Nonaktifkan`, whereas Malay uses its `Nyahaktif` forms. The read short set uses Indonesian `berkas`, `ukuran`, `pengaturan`, `otomatis`, `perangkat`, `gulir`, `ketuk`, `salin`, and `tempel` in their respective contexts. No further confirmed Malay-word leakage was found in this bounded comparison; this is not a claim of perfect Indonesian style or full-catalogue fluency. |
| Placement, Show all and Fit | `ImageAssembly.layout` places RIGHT at the parent's right/top and BOTTOM at its left/bottom. The short placement message preserves right/top alignment versus below/left alignment. `AssemblyActivity` binds Show all to `AssemblyCanvas.fit`, and its message explicitly preserves image/output sizes. `PaintCanvas.fit` changes viewport zoom/pan; `PaintDocument.fitSelectionToCanvas` changes floating geometry. Both locales distinguish whole-canvas fit from fitting an inserted image to the canvas. No additional changes proposed. |
| Zoom, colours, text and cursor controls | Short zoom-in/out labels distinguish enlarging and reducing; Indonesian's pinch hint explicitly includes both finger-distance directions. Foreground/background tap/hold hints, hexadecimal/RGB/HSV/HSL units, left/right column directions, italic, underline, strike and percentage line spacing were compared. `TextStyleDialog` supplies the corresponding settings; `ClassicPaintActivity` binds recent colours and cursor settings. No further edit proposed in this pass. |
| Other short messages and constants | The TSV includes gallery/download/provider failures, recovery/undo errors, assembly limits, memory failures, codec/PDF pages, still/animation notices, export dimensions and size limits, filenames, licences, units, format specifiers and numeric display templates. Text comparison retains conditions, negation, bounds, proper names and positional arguments. This does not test every failure path or certify every sentence. |

All code references above are under
`Paintroid/src/main/java/org/catrobat/paintroid/classic/` at the starting snapshot.
The two previously published Malay smoothing repairs were read as part of the
short set; they are not counted among these ten new edits.

## Lexical and coverage limits

Primary lexical lookups were attempted at DBP PRPM for
[pensel](https://prpm.dbp.gov.my/Cari1?d=175768&keyword=pensel),
[pratonton](https://prpm.dbp.gov.my/Cari1?d=175768&keyword=pratonton), and
[nombor bulat](https://prpm.dbp.gov.my/Cari1?keyword=nombor%20bulat).
The browser returned inaccessible/502 responses and the shell request returned
a proxy 403. No dictionary content was obtained or counted as supporting
evidence. The two caption edits therefore rely on the terminology/context
comparison described above; independent lexical/native review remains open.

The remaining long entries and manuals were not comprehensively re-reviewed.
Full Tagalog/Cebuano semantics, other PR batches, the other 81 locales, typography,
device layouts, font rendering and credit-lifecycle behavior were not changed or
closed. Latest conversation retrieval remains excerpt-only, so this does not
claim reconciliation with complete latest transcripts.

## Validation of the resulting resources

- `python3 -m unittest discover -s tools -p 'test_*.py'`: **91 tests passed**.
  These include the locale/resource/placeholder gates and PR3 completeness;
  they establish structural and regression properties, not linguistic approval.
- Strict `/tmp/an-paint-aapt2/aapt2 compile --dir Paintroid/src/main/res` and
  the equivalent `app/src/main/res` command: **passed**, without `--legacy`.
- `git diff --check`: passed. No resource keys, attributes, placeholders or
  plural resources changed. The language notes regain the English source's
  `\n\n` title separator.
- No Gradle unit/lint, emulator, screenshot, accessibility-session or native
  speaker check was run in this subtask. Remote CI and integration publication
  are reported separately by the coordinating task.

Resulting XML SHA-256:

- Malay: `3a1341a95238be477341e20efa46917b502b2331584912668b849234e276ba5d`
- Indonesian: `da4fb3bd2e10f909bf02a70190309db169ced420892f1f195985df40ad8396d6`
