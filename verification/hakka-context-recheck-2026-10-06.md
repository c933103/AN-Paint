# Hakka contextual-reading and paired-clause recheck — 6 October 2026

This is fresh, bounded evidence for PR #6, starting at
`3ed8f1296dd802af542b6dd0e20cad810f20e243`. It does not reinstate any withdrawn
completion claim or close the whole PR #6 register. Only the canonical
`hak-Hant-TW` and `hak-Latn-TW` XML catalogues are changed.

## Confirmed defects corrected

1. Seven Latin resources gave spatial 背 the reading `pà`, which belongs to the
   verb “carry on one's back”, instead of spatial `poi`. Five inside-area
   instructions now render 肚背 as `tú-poi`; two below-the-control instructions
   now say `chhai hâ-poi`. The Han wording was already spatial and is retained.
2. All four 下擺 (“next time”) occurrences used `hâ pái`. The official current
   Ministry appendix explicitly gives Sixian `ha55 bai31`. They now use
   `ha pái`, retaining the existing PFS mapping of high departing tone 55 to
   no tone mark and rising tone 31 to an acute accent. The spatial 下背 reading
   remains `hâ-poi` (`ha24 boi55`); this is a contextual correction, not a
   replacement of every 下.
3. `language20_translation_note` in both scripts supplied only the Sixian
   convention and a technical-vocabulary note. It omitted the English source's
   maintenance and English-fallback explanation. Both scripts now retain those
   two meanings, the source heading/paragraph break, and the useful Sixian
   convention. Neither text asserts that translation work is complete.

The eleven reading corrections affect ten Latin resources:

| Resource | Corrected context |
| --- | --- |
| `ui_crop_preview_drag_an_edge_or_corner_drag` | Drag inside the crop |
| `ui_drag_a_selection_drag_inside_to_move_square` | Drag inside the selection |
| `ui_drag_between_opposite_corners_choose_outline_or_fill` | Choose below |
| `ui_drag_out_to_expand_in_to_trim_drag` | Drag inside the bounds |
| `ui_draw_around_an_area_drag_inside_to_move` | Drag inside the freeform selection |
| `ui_the_arrow_on_the_left_directly_below_the` | Drag inside; remember the choice next time |
| `ui_trim_from_the_original_edges_drag_the_handles` | Enter numbers below |
| `ui_add_up_to_20_images_with_android_s` | Reopen the assembly next time |
| `ui_save_explanation23` | Reuse Save settings next time |
| `ui_help23` | Reuse Save settings next time |

## Primary lexical evidence and source identity

- The current [MOE function-word appendix](https://hakkadict.moe.edu.tw/appendix/),
  time-adverb table, was opened during this recheck. Its 下擺 row gives Sixian
  `ha55 bai31`. The same appendix supplies 還吂, used in the fallback sentence.
- The current [MOE 系統 entry, web ID 12651](https://hakkadict.moe.edu.tw/search_result/?accent=1&id=12651)
  was reopened and gives Sixian `ne55 tung31`. The page displays several dialect
  records; the Sixian record, rather than the Zhao'an `he` record, is relevant.
- The current [MOE 抑係 entry, web ID 250](https://hakkadict.moe.edu.tw/search_result/?accent=1&id=250)
  was reopened: the alternative conjunction in the new fallback sentence uses
  Sixian `ia55 he55`, rendered `ia-he` in this catalogue.
- For the spatial contrast and several constituents, the original MOE 30 April
  2021 ODS was read from the [archived public mirror at commit
  `4c870f43db6fbc750b54e8b527f589cffbdb05b7`](https://github.com/i3thuan5/moe-hakkadict/blob/4c870f43db6fbc750b54e8b527f589cffbdb05b7/%E8%AA%BF%E5%80%BC%E8%B3%87%E6%96%99_raw/%E3%80%8A%E8%87%BA%E7%81%A3%E5%AE%A2%E5%AE%B6%E8%AA%9E%E5%B8%B8%E7%94%A8%E8%A9%9E%E8%BE%AD%E5%85%B8%E3%80%8B%E5%85%A7%E5%AE%B9%E8%B3%87%E6%96%99%281100430%29.ods).
  Its SHA-256 is
  `15bfb825d635be419d8c8379893d143abc1ed3e648c40c3700758cf7cca47544`.
  The mirror's CSV SHA-256 is
  `09ab6ab6f0953360dcdee366fd17e6a54f99e4c27132f50076383a95613962d0`.
  Relevant readings were checked in the ODS itself as well as its CSV derivative.
  These are dated primary dictionary records, not application translations.

| 2021 ODS system ID | Word | Sixian reading | Contextual decision |
| --- | --- | --- | --- |
| `HK0000000147` | 背 | `ba11` | Carrying; do not use its PFS `pà` in spatial instructions |
| `HK0000000643` | 背 | `boi55` | Back/reverse/positional side; PFS `poi` |
| `HK0000002167` | 裡背 | `di24 boi55` | Independent evidence for spatial 背 in an inside expression |
| `HK0000004821` | 下背 | `ha24 boi55` | Below; PFS `hâ-poi` |
| `HK0000012039` | 上背 | `song55 boi55` | Above; independently supports spatial `poi` |
| `HK0000000578` | 保存 | `bo31 sun11` | Save/preserve; existing PFS `pó-sùn` retained |
| `HK0000009080` | 系統 | `ne55 tung31` | Agrees with the reopened current Sixian web record |
| `HK0000013492` | 維護 | `vi11 fu55` | Maintenance in the paired note; PFS `vì-fu` |
| `HK0000006092` | 英文 | `in24 vun11` | English in the paired note; existing convention `Yîn-vùn` |

PFS mappings here are editorial orthographic renderings of the stated Sixian
readings, not quotations of PFS from the Ministry. In particular MOE unaspirated
`b` maps to PFS `p`, 11 to a grave accent, 24 to a circumflex, and 55 to no mark.
The existing correctly rendered `Hâ-poi` button and other spatial instructions
use the same spelling. The software expression 語言資源 is a constituent-based
technical term; this recheck does not claim a dictionary entry for that whole
compound or for a complete translated UI sentence.

The current [MOE download listing](https://hakkadict.moe.edu.tw/resource_download/)
was reopened and links a Sixian ODS updated on 8 September 2026. Downloading its
bytes in this environment failed with proxy HTTP 403; the web reader rejects
the ODS content type. Therefore the earlier claimed current-file hash
`a19d2e07fd5213f26bc2d4db9be0301418208d207c8e74f4df01278940ac0380`
has **not** been reconfirmed. The 2021 ODS, its `HK...` system IDs, the historical
2026 ODS row numbers, and current web IDs must not be treated as interchangeable.
No dictionary definitions or example sentences are copied into the app.

## Fresh checks that did not require a wording repair

- All **58 resources** containing literal 保存 were inspected for their paired
  Save/preserve term; they contain **82 occurrences** in each script. Every
  resource has the same per-key 保存 / `pó-sùn` count. Thus “58 resources” and
  “82 token occurrences” are different units, not a discrepancy. The Save alias
  `ui_save_a5d0d9` refers to `ui_save` in both scripts. Standalone 存 in Discard
  and Save as remains `chhùn`; it is not forced to take the compound reading.
- All three 系統 contexts (device-language default, safe-editing limit, and
  memory failure) use `ne-thúng`. The reopened current entry supports this
  choice; no replacement is necessary.
- The large legacy help retains both initially open panels and the later
  remembered user choice in both scripts. The Han clause `下擺會記等你个揀法`
  pairs with Latin `ha pái voi ki tén ǹ ke kién-fap` after the temporal-reading
  correction. The clause was present, rather than missing, at the starting head.
- All five 肚背 contexts, all seventeen 下背 occurrences across ten resources,
  and all four 下擺 contexts were compared after editing. The
  [per-resource term inventory](hakka-paired-terms-2026-10-06.tsv) records these
  counts along with every Save and system occurrence. Counts aid completeness
  within these term families; they do not certify surrounding sentence fluency.

## Validation and remaining limits

- `python3 -m unittest discover -s tools -p 'test_*.py'`: **97 passed**, including
  three new context/pair regression checks. As a negative control, running those
  new checks against the unedited starting XML detects all eleven bad readings;
  the unchanged Save/system pairing check passes on that baseline.
- Strict AAPT2 `compile --dir Paintroid/src/main/res`: **passed** without legacy
  mode. This is resource compilation, not an APK build or a device check.
- `validate_catalogue(tag, require_complete=True)`: **passed** for all six PR #6
  catalogues (`lzh-Hant`, both Hakka, both Taiwanese, `wuu-Hans`). This checks
  resource coverage/formatting, not semantic acceptance of those six languages.
- `git diff --check`: **passed**.

Register coverage: P06-002/003 now have an exhaustive current Save-term inventory;
P06-004/005 have a fresh paired-clause check and a corrected temporal reading;
P06-006 has all three current system occurrences checked. P06-007/009/010 have
only the bounded lexical evidence above, not an entire catalogue audit.
P06-008 remains blocked for the historical 2026 ODS byte hash. P06-001/011 and
the historical claim of 47 decisions remain unresolved: complete latest thread
transcripts and a reconstructable mapping for every claimed decision have not
been recovered. P06-012–017 and the rest of the Han/PFS semantic and regional
review are outside this bounded change and still require recheck. No full Hakka
completion, native-speaker certification, typography/runtime verification, or
user acceptance is claimed.
