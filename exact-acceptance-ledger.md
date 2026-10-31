# Independent linguistic review: next 90 P0/P1 proposals

**Review date:** 2026-10-30. **Final result:** 90 missing entries accepted for wording (45 P0, 45 P1), plus 15 existing-string wording corrections (6 P0, 9 P1). No source changes are applied by this record. All author-final proposals and corrections were rechecked; exact input hashes are recorded below.

## Binding and limits

PR #242; supplied commit `1aeed6e3860067c9224dfc6129ee0672c7917a01`; supplied tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`. The checkout did not have a resolvable Git HEAD: these identifiers are supplied provenance, not independently verified local Git identity. Exact English strings and related localized terminology were read from the catalogues. Tier assignments were checked against `translations/string-importance.json`.

This is independent model-assisted static linguistic review, **not native-human certification, Android resource serialization validation, execution evidence, or installed-UI/RTL/layout acceptance**. No source edits, source scripts, tests, public mutations, or Work-task actions were performed. Targets below are display text, not XML-escaped resource literals. Confidence concerns wording and meaning, not runtime fitness.

For missing entries, the previous localized value is absent. All numbered placeholders and JPEG/JPEG XL/PNG literals are preserved. Palette targets preserve the three argument roles and isolate `%3$s` neutrally: no active production caller establishing that legacy payload contract was found in the inspected main-source scope. This is not a guarantee for every possible substituted value. Generic Main labels do not establish Home, menu, screen, or navigation context. No active caller for the reviewed legacy Main, palette, Fit image, or Pinch and pan mode keys was found in that same scope; wording approval does not make a route active.

Basque `ui_discard`, Pashto `ui_discard`, all unrelated holds, and all existing implementation pauses remain unchanged.

### Independently observed input hashes

SHA-256 values bind the exact local catalogue bytes read; they do not prove Git ancestry. Locale catalogue paths are specified in the ledger sections.

| Input | SHA-256 |
|---|---|
| English source catalogue | `743bd9f04c391fb8e94dfb72f81fb24bbe2e3eb36f1584f35821687a1b96a261` |
| Importance-tier catalogue | `9b5bfb6d25f2ad034158816d943b94feed8296ad4117c2176f09a95dad506879` |
| ary catalogue | `6be6c782c6036651514b3a173770cfb873d168bbab2ec45c3250b22f545c27fa` |
| tok catalogue | `1b308df246c2e5b7dfac15d3de83d4e86f5891a4c698f278d275d6954f72df67` |
| sm catalogue | `c7f25822af3fba4eb9508b8b048f608ef713d81b91697e49a4448a40261b84e3` |
| nds catalogue | `4fb79ab75158e22b942867b2a131755732b0551ec1212d1002096c60f853e591` |
| eu-ES catalogue | `acf559c3faa2c888173a47ae11ed62c3c311f99e6d561fa268625cc1c41d7b9f` |
| ca-ES-valencia catalogue | `0240dc08ed447b5c449e3050fb5faf5df58aea6a92f0ec3dc86f2ff4623740e9` |
| ps catalogue | `525320ae9b7f4e525ac085ecbd0e5fa2dd5b801235735cb885b0c191f93ab4c1` |
| sd catalogue | `f96766371a804ac8b991a88aff4680f3e7ca0773638543f855d49742e39cbbcc` |
| ug catalogue | `0d71036e89acb0a37bc4e886e3a02ea5415b6ee9a9fa4414b25b247d3ce648c4` |
| Final ary/tok/sm missing proposals | `506a3aa42b03651af9dcce347c79e754f1689a98f4e13f79a79c29550b240a70` |
| Final ary/tok/sm existing review | `c2f634a086621edd6d0ffe845e51b8bdc3e25dfc91a7f521a014936739cb71f2` |
| Final nds/eu-ES/ca-ES-valencia missing proposals | `7e2e694eede5989b1ba52f82256495eb2645eeeab63c83121c3f3f915aab52ac` |
| Final nds/eu-ES/ca-ES-valencia existing review | `48a02ea28d0c625b6c29b73bed13fe95122f41d0747ba9a431a328ae2c88c362` |
| Final ps/sd/ug missing proposals | `f31d6db0c3201b19d907aeca323dc6b53f402d9a1273def2ba06a13f04a98b1a` |
| Final ps/sd/ug existing review | `a03bca5289835faafe45ce6c96bf9cd99d7a044d502d4bf1789c81a76f94bb92` |

## Exact source catalogue

Each ledger key below binds to the exact source here, in `Paintroid/src/main/res/values/strings.xml`.

| Key | Tier | Exact English source |
|---|---|---|
| `formats22_derived_exported` | P0 | `%1$s exported. Your full drawing still has unsaved changes; save a full image copy before replacing it.` |
| `ui_save_as` | P0 | `Save as %1$s` |
| `ui_save_as_jpeg` | P0 | `Save as JPEG…` |
| `ui_save_as_jpeg_xl` | P0 | `Save as JPEG XL…` |
| `ui_save_as_png` | P0 | `Save as PNG…` |
| `ui_bg` | P1 | `BG` |
| `ui_fg` | P1 | `FG` |
| `ui_fit_image` | P1 | `Fit image` |
| `ui_foreground_background_colour_palette` | P1 | `Foreground %1$s, background %2$s. %3$s colour palette.` |
| `ui_main23` | P1 | `Main` |
| `ui_pinch_and_pan_mode` | P1 | `Pinch and pan mode` |

## Missing-entry ledger

“Accept wording” is an exact-text linguistic disposition after final-revision recheck, not permission to lift an unrelated hold or perform implementation. H = high confidence; MH = medium-high; M = medium. The only new candidate-level lexical hold considered in this pass, Low German Main, was resolved by the direct dictionary evidence discussed below; existing Basque/Pashto Discard and other context/runtime/implementation holds remain.

### Moroccan Arabic (`ary`) — 11

Catalogue: `Paintroid/src/main/res/values-b+ary/strings.xml`.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | تصدّر %1$s. الرسم ديالك كامل ما زال فيه تغييرات ما تحفظوش؛ حفظ نسخة كاملة من الصورة قبل ما تعوّض الرسم. | Accept wording | MH |
| `ui_save_as` | حفظ بصيغة %1$s | Accept wording | H |
| `ui_save_as_jpeg` | حفظ بصيغة JPEG… | Accept wording | H |
| `ui_save_as_jpeg_xl` | حفظ بصيغة JPEG XL… | Accept wording | H |
| `ui_save_as_png` | حفظ بصيغة PNG… | Accept wording | H |
| `ui_bg` | الخلفية | Accept wording | H |
| `ui_fg` | اللون الأمامي | Accept wording | H |
| `ui_fit_image` | بيّن الصورة كاملة فالعرض | Accept wording | MH |
| `ui_foreground_background_colour_palette` | اللون الأمامي: %1$s، لون الخلفية: %2$s. لوحة الألوان: %3$s. | Accept wording; payload contract unestablished | MH |
| `ui_main23` | الرئيسي | Accept wording | H |
| `ui_pinch_and_pan_mode` | وضع التكبير والتصغير بجوج صبيعات وتحريك العرض | Accept wording | MH |

### Toki Pona (`tok`) — 11

Catalogue: `Paintroid/src/main/res/values-b+tok/strings.xml`.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | ilo li pana e %1$s. sitelen sina ale li jo e ante pi awen sona ala. sina wile pana e sitelen ante lon ma ona la o awen sona e sitelen sina ale lon lipu ante lon tenpo nanpa wan. | Accept wording | M |
| `ui_save_as` | o awen sona kepeken nasin %1$s | Accept wording | MH |
| `ui_save_as_jpeg` | o awen sona kepeken nasin JPEG… | Accept wording | MH |
| `ui_save_as_jpeg_xl` | o awen sona kepeken nasin JPEG XL… | Accept wording | MH |
| `ui_save_as_png` | o awen sona kepeken nasin PNG… | Accept wording | MH |
| `ui_bg` | monsi | Accept wording | MH |
| `ui_fg` | sinpin | Accept wording | MH |
| `ui_fit_image` | o pona e suli lukin: sitelen ale li lon lukin | Accept wording | M |
| `ui_foreground_background_colour_palette` | kule sinpin: %1$s. kule monsi: %2$s. kulupu kule: %3$s. | Accept wording; payload contract unestablished | MH |
| `ui_main23` | lawa | Accept wording | M |
| `ui_pinch_and_pan_mode` | nasin ni: o kama poka e palisa luka tu anu o kama weka e ona. ni li suli anu lili e lukin. o tawa e ma lukin. | Accept wording after correction | M |

**Toki Pona correction rechecked:** the earlier draft used `tawa suli anu lili e lukin` like an English purpose infinitive with a direct object. The current target separates the zoom-result clause, preserving both zoom directions, the two-finger gesture, and view panning. The grammatical distinction is supported by the primary teaching account of [prepositions and context](https://mun.la/sona/preps.html); the application to this sentence is the reviewer's linguistic analysis. The export opening was also revised to `ilo li pana e %1$s`, explicitly making the program the exporter rather than the exported item the giver. Both revisions have been re-read.

### Samoan (`sm`) — 11

Catalogue: `Paintroid/src/main/res/values-b+sm/strings.xml`.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | Ua auina atu %1$s. E iai pea suiga e leʻi sefeina i lau ata tusi atoa; sefe se kopi o le ata atoa a o leʻi suia i se isi ata. | Accept wording | MH |
| `ui_save_as` | Sefe o se %1$s | Accept wording | M |
| `ui_save_as_jpeg` | Sefe o se JPEG… | Accept wording | M |
| `ui_save_as_jpeg_xl` | Sefe o se JPEG XL… | Accept wording | M |
| `ui_save_as_png` | Sefe o se PNG… | Accept wording | M |
| `ui_bg` | Pito i tua | Accept wording | MH |
| `ui_fg` | Pito i luma | Accept wording | MH |
| `ui_fit_image` | Fetaui le ata i le vaaiga | Accept wording | M |
| `ui_foreground_background_colour_palette` | Lanu pito i luma: %1$s; lanu pito i tua: %2$s. Laupapa lanu: %3$s. | Accept wording; payload contract unestablished | MH |
| `ui_main23` | Autū | Accept wording | MH |
| `ui_pinch_and_pan_mode` | Faiga e faatelē pe faaitiiti ai le vaaiga i tamatamailima e lua ma faaseʻe ai le vaaiga | Accept wording | MH |

### Low German (`nds`) — 11

Catalogue: `Paintroid/src/main/res/values-b+nds/strings.xml`.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | %1$s exporteert. Dien hele Teknung hett noch nich spiekerte Ännern; spieker en Kopie vun dat hele Bill, ehr du de Teknung utwesselst. | Accept wording | MH |
| `ui_save_as` | Spiekern as %1$s | Accept wording | H |
| `ui_save_as_jpeg` | Spiekern as JPEG… | Accept wording | H |
| `ui_save_as_jpeg_xl` | Spiekern as JPEG XL… | Accept wording | H |
| `ui_save_as_png` | Spiekern as PNG… | Accept wording | H |
| `ui_bg` | Achtergrund | Accept wording | H |
| `ui_fg` | Vörgrund | Accept wording | H |
| `ui_fit_image` | Bill inpassen | Accept wording | MH |
| `ui_foreground_background_colour_palette` | Vörgrund %1$s, Achtergrund %2$s. Klöörpalett: %3$s. | Accept wording; payload contract unestablished | MH |
| `ui_main23` | Hööft | Accept wording; generic label only | M |
| `ui_pinch_and_pan_mode` | Modus för dat Gröter- un Lüttermaken mit twee Fingers un dat Verschuven vun de Ansicht | Accept wording | MH |

**Low German Main: lexical question resolved, medium confidence.** [SASS](https://netz.sass-platt.de/platt-hoch/?term=H%C3%B6%C3%B6ft) directly records `Hööft` as a noun including German *Haupt*, *Hauptsache*, and *Kopf*, not only in compounds. In particular, the standalone main-thing sense supports a generic elliptic Main caption. No concrete semantic contradiction or required noun-agreement error was established. Requiring a published isolated UI occurrence would impose a stronger condition than the source itself supplies; lack of such attestation is not a linguistic defect. The tentative candidate hold is therefore resolved as **accepted wording with medium idiom confidence**, without adding Home/menu or claiming a caller, layout, runtime, or implementation acceptance. This conclusion is the reviewer's inference from the dictionary and source context, not dictionary certification of the full UI.

### Basque (`eu-ES`) — 7

Catalogue: `Paintroid/src/main/res/values-eu-rES/strings.xml`. Existing `ui_discard` hold is outside these entries and remains unchanged.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | %1$s esportatu da. Zure marrazki osoak oraindik gorde gabeko aldaketak ditu; gorde irudi osoaren kopia bat marrazkia ordeztu aurretik. | Accept wording | H |
| `ui_save_as` | Gorde honela: %1$s | Accept wording | H |
| `ui_save_as_jpeg` | Gorde JPEG gisa… | Accept wording | H |
| `ui_save_as_jpeg_xl` | Gorde JPEG XL gisa… | Accept wording | H |
| `ui_save_as_png` | Gorde PNG gisa… | Accept wording | H |
| `ui_foreground_background_colour_palette` | Aurreko planoa: %1$s; atzeko planoa: %2$s. Kolore-paleta: %3$s. | Accept wording; payload contract unestablished | H |
| `ui_pinch_and_pan_mode` | Bi hatzez zooma handitu edo txikitu eta ikuspegia desplazatzeko modua | Accept wording | H |

### Valencian (`ca-ES-valencia`) — 8

Catalogue: `Paintroid/src/main/res/values-b+ca+ES+valencia/strings.xml`.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | S’ha exportat %1$s. El vostre dibuix complet encara té canvis sense guardar; guardeu una còpia de la imatge completa abans de substituir-lo. | Accept wording | H |
| `ui_save_as` | Guarda com a %1$s | Accept wording | H |
| `ui_save_as_jpeg` | Guarda com a JPEG… | Accept wording | H |
| `ui_save_as_jpeg_xl` | Guarda com a JPEG XL… | Accept wording | H |
| `ui_save_as_png` | Guarda com a PNG… | Accept wording | H |
| `ui_foreground_background_colour_palette` | Primer pla: %1$s; fons: %2$s. Paleta de colors: %3$s. | Accept wording; payload contract unestablished | H |
| `ui_main23` | Principal | Accept wording; wording only | H |
| `ui_pinch_and_pan_mode` | Mode per a ampliar o reduir amb dos dits i desplaçar la vista | Accept wording | H |

### Pashto (`ps`) — 9

Catalogue: `Paintroid/src/main/res/values-ps/strings.xml`. Existing `ui_discard` hold is outside these entries and remains unchanged.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | %1$s صادر شو. ستاسو په بشپړ رسم کې لا هم ناخوندي شوي بدلونونه شته؛ د رسم تر بدلولو مخکې د بشپړ انځور یوه کاپي خوندي کړئ. | Accept wording | MH |
| `ui_save_as` | په %1$s بڼه خوندي کړئ | Accept wording | MH |
| `ui_save_as_jpeg` | په JPEG بڼه خوندي کړئ… | Accept wording | MH |
| `ui_save_as_jpeg_xl` | په JPEG XL بڼه خوندي کړئ… | Accept wording | MH |
| `ui_save_as_png` | په PNG بڼه خوندي کړئ… | Accept wording | MH |
| `ui_bg` | شالید | Accept wording | MH |
| `ui_fg` | مخکینی رنګ | Accept wording | MH |
| `ui_foreground_background_colour_palette` | مخکینی رنګ %1$s، شالید %2$s. د رنګونو تخته: %3$s. | Accept wording; payload contract unestablished | M |
| `ui_pinch_and_pan_mode` | په دوو ګوتو د لویولو او کوچني کولو او د لید د خوځولو حالت | Accept wording | MH |

### Sindhi (`sd`) — 11

Catalogue: `Paintroid/src/main/res/values-sd/strings.xml`.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | %1$s برآمد ٿيو. توهان جي مڪمل ڊرائنگ ۾ اڃا به اڻمحفوظ تبديليون آهن؛ ڊرائنگ کي مٽائڻ کان اڳ مڪمل تصوير جي هڪ ڪاپي محفوظ ڪريو. | Accept wording | MH |
| `ui_save_as` | %1$s فارميٽ ۾ محفوظ ڪريو | Accept wording | MH |
| `ui_save_as_jpeg` | JPEG فارميٽ ۾ محفوظ ڪريو… | Accept wording | MH |
| `ui_save_as_jpeg_xl` | JPEG XL فارميٽ ۾ محفوظ ڪريو… | Accept wording | MH |
| `ui_save_as_png` | PNG فارميٽ ۾ محفوظ ڪريو… | Accept wording | MH |
| `ui_bg` | پسمنظر | Accept wording | MH |
| `ui_fg` | اڳيون رنگ | Accept wording | MH |
| `ui_fit_image` | تصوير کي ڏيک ۾ سمائيو | Accept wording | MH |
| `ui_foreground_background_colour_palette` | اڳيون رنگ %1$s، پسمنظر %2$s. رنگن جي تختي: %3$s. | Accept wording; payload contract unestablished | M |
| `ui_main23` | مکيه | Accept wording | MH |
| `ui_pinch_and_pan_mode` | ٻن آڱرين سان ويجهو يا پري ڏيکارڻ ۽ ڏيک سرڪائڻ وارو موڊ | Accept wording | MH |

### Uyghur (`ug`) — 11

Catalogue: `Paintroid/src/main/res/values-b+ug/strings.xml`.

| Key | Exact target | Decision | Confidence |
|---|---|---|---|
| `formats22_derived_exported` | %1$s چىقىرىلدى. تولۇق رەسىمىڭىزدە تېخى ساقلانمىغان ئۆزگەرتىشلەر بار؛ رەسىمنى ئالماشتۇرۇشتىن بۇرۇن تولۇق سۈرەتنىڭ بىر نۇسخىسىنى ساقلاڭ. | Accept wording | MH |
| `ui_save_as` | %1$s پىچىمىدا ساقلاش | Accept wording | MH |
| `ui_save_as_jpeg` | JPEG پىچىمىدا ساقلاش… | Accept wording | MH |
| `ui_save_as_jpeg_xl` | JPEG XL پىچىمىدا ساقلاش… | Accept wording | MH |
| `ui_save_as_png` | PNG پىچىمىدا ساقلاش… | Accept wording | MH |
| `ui_bg` | تەگلىك | Accept wording | MH |
| `ui_fg` | ئالدى كۆرۈنۈش | Accept wording | MH |
| `ui_fit_image` | سۈرەتنى كۆرۈنۈشكە سىغدۇرۇش | Accept wording | MH |
| `ui_foreground_background_colour_palette` | ئالدى كۆرۈنۈش %1$s، تەگلىك %2$s. رەڭ تاختىسى: %3$s. | Accept wording; payload contract unestablished | M |
| `ui_main23` | ئاساسىي | Accept wording | MH |
| `ui_pinch_and_pan_mode` | ئىككى بارماق بىلەن چوڭايتىش، كىچىكلىتىش ۋە كۆرۈنۈشنى يۆتكەش ھالىتى | Accept wording | MH |

## Existing-string corrections

### Low German: Save interaction cue — accepted wording correction

- **Key / tier:** `ui_save_a5d0d9` / P0.
- **Exact source:** `Save…`
- **Previous raw value:** `@string/ui_save`; resolved display: `Spiekern`.
- **Exact target:** `Spiekern…`
- **Reason / confidence:** restores the source's deliberate ellipsis distinction from Save without it. High confidence. This is not a runtime-save-failure allegation.
- **Evidence:** `values/strings.xml:350–351`; `values-b+nds/strings.xml:13–14`.

### Low German: Navigate mode reference — accepted wording correction

- **Key / tier:** `ui_drawing_canvas_pinch_and_move_two_fingers_to` / P1.
- **Exact source:** `Drawing canvas. Pinch and move two fingers to zoom and pan. Navigate mode also pans with one finger.`
- **Previous display:** `Tekengebiet. Beweg twee Fingers openeen to oder uteneen, üm to zoomen, un verschuuv se tosamen, üm de Ansicht to verschuven. In den Beweegmodus lett sik de Ansicht ok mit een Finger verschuven.`
- **Exact target:** `Tekengebiet. Beweg twee Fingers openeen to oder uteneen, üm to zoomen, un verschuuv se tosamen, üm de Ansicht to verschuven. In den Modus „Verschuven un zoomen“ lett sik de Ansicht ok mit een Finger verschuven.`
- **Reason / confidence:** names the actual localized `ui_navigate` control instead of the inconsistent Beweegmodus. Preserves both zoom directions and view movement. Medium-high confidence.
- **Evidence:** `values/strings.xml:160,271`; `values-b+nds/strings.xml:155,219`.

### Toki Pona: monospaced characters — accepted wording correction

- **Key / tier:** `formats22_ascii_description` / P0.
- **Exact source:** `Writes plain text using light and dark characters. View it in a monospaced font. This is a visual rendition; it cannot be reopened as the original image.`
- **Previous display:** `ilo li pana e sitelen toki suno e sitelen toki pimeja. o lukin e ona kepeken nasin sitelen ni: leko sitelen ale li jo e suli poka sama. ni li lukin sama sitelen taso; ona li ken ala kama sitelen open sama.`
- **Exact target:** `ilo li pana e sitelen toki suno e sitelen toki pimeja. o lukin e ona kepeken nasin sitelen ni: sitelen toki wan wan li jo e suli poka sama. ni li lukin sama sitelen taso; ona li ken ala kama sitelen open sama.`
- **Reason / confidence:** the previous monospace instruction describes equal pixel widths using the catalogue's exact Pixels term. The target describes each text character having equal width and preserves the visual-rendition and cannot-reopen-as-original warnings. High confidence in the correction; no runtime or data-loss bug is alleged.
- **Evidence:** `values-b+tok/strings.xml:18,259–260`.

### Pashto: complete gesture verbs — accepted wording correction

- **Key / tier:** `ui_drawing_canvas_pinch_and_move_two_fingers_to` / P1.
- **Exact source:** `Drawing canvas. Pinch and move two fingers to zoom and pan. Navigate mode also pans with one finger.`
- **Previous display:** `د رسم مخ. د زوم او خوځولو لپاره دوه ګوتې نږدې یا لرې او وخوځوئ. د «ګرځېدنه» په حالت کې په یوه ګوته هم خوځول کېږي.`
- **Exact target:** `د رسم مخ. د لید د لویولو او کوچني کولو لپاره دوه ګوتې له یو بله لرې یا یو بل ته نږدې کړئ، او د لید د خوځولو لپاره یې وخوځوئ. د «ګرځېدنه» په حالت کې لید په یوه ګوته هم خوځول کېږي.`
- **Reason / confidence:** completes the omitted near/far verb, explicitly states both zoom directions and view panning, and retains the existing Navigate label and one-finger alternative. High confidence on the defect; medium-high on the full replacement wording.
- **Evidence:** `values/strings.xml:160`; `values-ps/strings.xml:198,259`.

### Toki Pona: recovery ZIP purpose clause — accepted wording correction

- **Key / tier:** `ui_a_separate_recovery_copy_has_been_kept_use` / P0.
- **Exact source:** `%1$s A separate recovery copy has been kept. Use File > Export recovery copy to save its ZIP. Extract canvas.png from it and load that image to use the normal resize options if needed.`
- **Previous display:** `%1$s lipu ante pi kama sin li awen. o kepeken «lipu > o pana e lipu pi kama sin» tawa awen sona e ZIP ona. o kama jo e canvas.png tan ona. sina wile e ante suli pi nasin kulupu la o open e sitelen ni.`
- **Exact target:** `%1$s lipu ante pi kama sin li awen. o awen sona e ZIP ona kepeken «lipu > o pana e lipu pi kama sin». o kama jo e canvas.png tan ona. sina wile e ante suli pi nasin kulupu la o open e sitelen ni.`
- **Reason / confidence:** promotes save-ZIP to the main predicate and attaches the menu command with `kepeken`, avoiding an English-like purpose infinitive. The separate recovery copy, `%1$s`, `ZIP`, `canvas.png`, and subsequent loading/resize instruction are retained. High confidence on the specific grammatical repair.
- **Evidence:** `values/strings.xml:11`; `values-b+tok/strings.xml:33`.

### Toki Pona: protecting the draft and current work — accepted wording correction

- **Key / tier:** `ui_autosave_is_paused_to_protect_that_draft_use` / P0.
- **Exact source:** `%1$s Autosave is paused to protect that draft. Use “File → Export recovery copy…” to keep it, and “File → Save as…” (File format: PNG / JPEG) to save your current work.`
- **Previous display:** `%1$s awen sona pi ilo taso li awen pali ala tawa awen pona pi sitelen pini ala ni. o kepeken «lipu → o pana e lipu pi kama sin…» tawa awen e ona. o kepeken «lipu → o awen sona kepeken nasin…» (nasin lipu: PNG / JPEG) tawa awen e pali sina pi tenpo ni.`
- **Exact target:** `%1$s awen sona pi ilo taso li awen pali ala tawa awen pona pi sitelen pini ala ni. o awen e ona kepeken «lipu → o pana e lipu pi kama sin…». o awen sona e pali sina pi tenpo ni kepeken «lipu → o awen sona kepeken nasin…» (nasin lipu: PNG / JPEG).`
- **Reason / confidence:** gives keeping the draft and saving current work their own main predicates; preserves pause/protection, the two separate menu commands, `%1$s`, and `PNG / JPEG`. High confidence on the specific grammatical repairs.
- **Evidence:** `values/strings.xml:51`; `values-b+tok/strings.xml:39`.

### Toki Pona: choose an app and share the copy — accepted wording correction

- **Key / tier:** `ui_share_explanation34` / P0. Preserve `formatted="false"` when serializing.
- **Exact source:** `Save a copy to your chosen location, then choose an app to share it. Your current Save destination stays unchanged.`
- **Previous display:** `o awen sona e sitelen sama lon ma pi wile sina. ni la o anu e ilo tawa pana e ona. ma lipu pi awen sona tenpo ni li ante ala.`
- **Exact target:** `o awen sona e sitelen sama lon ma pi wile sina. ni la o anu e ilo. o pana e sitelen sama ni kepeken ilo ni. ma lipu pi awen sona tenpo ni li ante ala.`
- **Reason / confidence:** separates app choice and sharing that same copy through it. Preserves save-copy-first order, selected location, and unchanged current Save destination. High confidence.
- **Evidence:** `values/strings.xml:688`; `values-b+tok/strings.xml:82`.

### Toki Pona: palette scrolling — accepted wording correction

- **Key / tier:** `ui_colour_palette_tap_for_foreground_hold_for_background` / P1.
- **Exact source:** `Colour palette. Tap for foreground; hold for background. Scroll for more colours.`
- **Previous display:** `kulupu kule. o luka tawa kule sinpin; o awen luka tawa kule monsi. o tawa e kulupu tawa lukin e kule ante.`
- **Exact target:** `kulupu kule. o luka tawa kule sinpin; o awen luka tawa kule monsi. o tawa e kulupu. ni la sina ken lukin e kule ante.`
- **Reason / confidence:** separates scrolling from its result rather than placing an `e` object in the purpose phrase. Foreground/background and tap/hold remain distinct and in the same order. High confidence.
- **Evidence:** `values/strings.xml:92`; `values-b+tok/strings.xml:152`.

### Toki Pona: drag inside the crop — accepted wording correction

- **Key / tier:** `ui_crop_preview_drag_an_edge_or_corner_drag` / P1.
- **Exact source:** `Crop preview. Drag an edge or corner; drag inside to move the crop.`
- **Previous display:** `lukin open pi kipisi. o tawa e poka pini anu nena. o tawa lon insa tawa tawa e ma kipisi.`
- **Exact target:** `lukin open pi kipisi. o tawa e poka pini anu nena. o tawa e ma kipisi kepeken tawa luka lon insa ona.`
- **Reason / confidence:** makes moving the crop area the main predicate and describes hand/finger movement inside it as the method. Keeps the separate edge/corner instruction. Medium-high confidence.
- **Evidence:** `values/strings.xml:122`; `values-b+tok/strings.xml:166`.

### Toki Pona: memory to finish opening — accepted wording correction

- **Key / tier:** `ui_not_enough_memory_to_finish_opening_this_image` / P1.
- **Exact source:** `Not enough memory to finish opening this image`
- **Previous display:** `poki sona pali (RAM) li lili tawa pini e open sitelen ni`
- **Exact target:** `poki sona pali (RAM) li lili tawa pini pi open sitelen ni`
- **Reason / confidence:** uses a nominal completion-of-opening phrase after `tawa`, keeping the insufficiency and this-image scope. High confidence on the specific grammatical repair.
- **Evidence:** `values/strings.xml:281`; `values-b+tok/strings.xml:247`.

### Toki Pona: memory to inspect — accepted wording correction

- **Key / tier:** `ui_not_enough_memory_to_inspect_this_image` / P1.
- **Exact source:** `Not enough memory to inspect this image`
- **Previous display:** `poki sona pali (RAM) li lili tawa lukin sona e sitelen ni`
- **Exact target:** `poki sona pali (RAM) li lili tawa lukin sona pi sitelen ni`
- **Reason / confidence:** uses a nominal examination-of-this-image phrase after `tawa`, retaining the insufficiency. High confidence on the specific grammatical repair.
- **Evidence:** `values/strings.xml:283`; `values-b+tok/strings.xml:248`.

### Toki Pona: tap to enter a number — accepted wording correction

- **Key / tier:** `ui_tap_to_type_a_number` / P1.
- **Exact source:** `%1$s: %2$s. Tap to type a number.`
- **Previous display:** `%1$s: %2$s. o luka tawa pana e nanpa.`
- **Exact target:** `%1$s: %2$s. o luka. ni la sina ken pana e nanpa.`
- **Reason / confidence:** separates tap from the resulting ability to enter a number, keeping both numbered placeholders exact and in order. High confidence.
- **Evidence:** `values/strings.xml:400`; `values-b+tok/strings.xml:303`.

### Toki Pona: tool-category scrolling — accepted wording correction

- **Key / tier:** `ui_tool_categories` / P1.
- **Exact source:** `Tool categories. Scroll to see more tools`
- **Previous display:** `kulupu ilo. o tawa e kulupu tawa lukin e ilo ante`
- **Exact target:** `kulupu ilo. o tawa e kulupu. ni la sina ken lukin e ilo ante`
- **Reason / confidence:** separates scrolling from the resulting ability to see more tools, matching the palette-scroll repair. High confidence.
- **Evidence:** `values/strings.xml:651`; `values-b+tok/strings.xml:317`.

The nine purpose-phrase repairs are specific grammatical corrections, not a blanket prohibition on verbal `tawa e`, `e` inside quoted control names, or transitive `kepeken` variants. They have been checked against their exact English/current counterparts. Broader Toki Pona vocabulary modernization is outside this correction set.

### Toki Pona: destination replacement failure — accepted wording correction

- **Key / tier:** `save20_destination_error` / P0.
- **Exact source:** `The completed image could not replace its destination.`
- **Previous display:** `sitelen pi pali pini li ken ala kama lon lipu pi ma wile, li ken ala weka e lipu ni.`
- **Exact target:** `ilo li ken ala ante e lipu pi ma wile kepeken sitelen pi pali pini.`
- **Reason / confidence:** the previous second clause asserts inability to remove the file, which the source does not separately establish. The replacement says the program could not replace/change the destination file using the completed image, without making a deletion assertion. High confidence on the unsupported extra assertion; medium-high on the concise replacement wording.
- **Evidence:** `values/strings.xml:643`; `values-b+tok/strings.xml:24`.

### Toki Pona: no canvas-size substitution — accepted wording correction

- **Key / tier:** `commons_svg_original_size_unavailable` / P1.
- **Exact source:** `The SVG does not declare a usable original size. No canvas-based size was substituted.`
- **Previous display:** `lipu SVG li pana ala e suli open pi ken kepeken. ilo li kepeken ala e suli ma sitelen lon anpa suli open.`
- **Exact target:** `lipu SVG li pana ala e suli open pi ken kepeken. ilo li kepeken ala e suli ma sitelen.`
- **Reason / confidence:** the previous `lon anpa suli open` adds an under/below-original-size relation to an unconditional no-substitution statement. Removing it says plainly that no usable original size was given and the canvas size was not used. High confidence on the spurious relation; medium-high on the concise replacement wording.
- **Evidence:** `values/strings.xml:709`; `values-b+tok/strings.xml:103`.

## Non-defects and unproven concerns

- All nine full-drawing export warnings distinguish export completion from unsaved full drawing changes, and retain a full-image copy before replacement. Toki Pona uses an explicit replacement conditional and another file to express that copy.
- All nine pinch/pan candidates retain zoom in, zoom out, two-finger operation, and view panning; the Toki Pona grammar correction is separate from this semantic coverage.
- FG/BG targets use localized role labels consistent with their foreground/background colour terms, not opaque English initials. Width and rendering remain untested.
- Samoan Save-as/Fit choices merit ordinary native idiom review, but no sufficiently evidenced specific defect was established here. They are not additional mandatory corrections.
- Identical Sindhi Cancel/Discard wording is an optional distinction question without an established conflicting active caller, not a confirmed defect and not authority to change either string.
- Resolution terminology concerns were not substantiated as concrete defects.
- Continue-drawing translations of `ui_draw_again` are consistent with the inspected caller: `Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt:770` calls `chooseTool(drawingTool)` from Navigate options. A literal “draw anew” reading is not required by that behavior. No correction is recommended on the English label alone.
