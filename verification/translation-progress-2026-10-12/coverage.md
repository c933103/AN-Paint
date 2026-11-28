# AN Paint per-language translation catalogue baseline

Pinned source: [`4231edaac45d89c52f51e2b77d0f94a1176ad88c`](https://github.com/c933103/AN-Paint/commit/4231edaac45d89c52f51e2b77d0f94a1176ad88c).

140 offered choices: 131 non-English locale/script/region choices, 7 English regional choices, and 2 explicitly labelled test modes. Device default is a setting, not a separate language.

The source denominator is **695 translatable strings + 1 plural resources + 0 string-arrays = 696 resource keys**. Entries marked translatable=false are excluded.

**59 exact catalogues have every source key present**; **81 are partial**; **0 choices have no exact catalogue**. Structural presence is not accepted linguistic completion.

## Definitions and limitations

- Present means a nonempty exact-catalogue entry for a translatable default key. A plural is one resource regardless of quantity count; this does not certify every language-required plural form. Local string references count as present; all reference targets are present in the same catalogue.
- Missing means absent in this exact source catalogue. Android may resolve it from a parent, sibling, shared or default resource. These figures do not assert that every missing key displays English. For example, fa-IR and ca-ES-valencia have potential same-language parents.
- The percentage is key presence, not a translation-quality score. Strings equal to English are NOT subtracted: proper names, format identifiers, symbols and numeric templates can legitimately match. JSON records literal equality only as a review aid and excludes resource aliases from that comparison.
- Canonical locale strings.xml files are directly maintained source. Historical JSON catalogues/coverage and imported snapshots are provenance, not live coverage. The generated ko-Kore-KR-anpaint resource directory is a build-time routing mirror of ko-Kore-KR; it contributes no extra language or progress. es and ko source catalogues are unoffered auxiliaries, not separate picker choices.
- The September 28 reset withdrew earlier completion/verification claims. Do not mark a language accepted from this scan. Review state, bounded accepted corrections, pending PRs and release state must be tracked separately.
- This scan does not count hardcoded UI text, dependency strings, external content or verbatim licence bodies. It does not run Android UI/layout tests and does not prove a build is released.

## Every offered choice

S = nonempty direct string keys out of 695; P = direct plural resources out of 1; missing and coverage use 696 total keys. “All keys” is structural only. Every row still needs language/semantic acceptance tracked separately.

| Locale / canonical catalogue | Display name | Kind | S | P | Missing | Presence | Coverage |
|---|---|---|---:|---:|---:|---|---:|
| [en-001](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+en+001/strings.xml) | English (International) | English | 695 | 1 | 0 | All keys | 100.00% |
| [af](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+af/strings.xml) | Afrikaans | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ain-Kana](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ain+Kana/strings.xml) | アイヌ イタㇰ | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ain-Latn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ain+Latn/strings.xml) | Aynu itak | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [am](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+am/strings.xml) | አማርኛ | Locale | 12 | 0 | 684 | Partial | 1.72% |
| [ar](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ar/strings.xml) | العربية | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ast](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ast/strings.xml) | Asturianu | Locale | 86 | 0 | 610 | Partial | 12.36% |
| [az](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-az/strings.xml) | Azərbaycanca | Locale | 57 | 0 | 639 | Partial | 8.19% |
| [be](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+be/strings.xml) | Беларуская | Locale | 108 | 0 | 588 | Partial | 15.52% |
| [bg](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-bg/strings.xml) | Български | Locale | 127 | 0 | 569 | Partial | 18.25% |
| [bn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-bn/strings.xml) | বাংলা | Locale | 103 | 0 | 593 | Partial | 14.80% |
| [bo](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+bo/strings.xml) | བོད་ཡིག | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [br](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+br/strings.xml) | Brezhoneg | Locale | 85 | 0 | 611 | Partial | 12.21% |
| [bs](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-bs/strings.xml) | Bosanski | Locale | 117 | 0 | 579 | Partial | 16.81% |
| [ca](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ca/strings.xml) | Català | Locale | 127 | 0 | 569 | Partial | 18.25% |
| [ca-ES-valencia](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ca+ES+valencia/strings.xml) | Valencià | Locale | 95 | 0 | 601 | Partial | 13.65% |
| [ceb](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ceb/strings.xml) | Cebuano | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ckb](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ckb/strings.xml) | کوردی | Locale | 40 | 0 | 656 | Partial | 5.75% |
| [cs](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-cs/strings.xml) | Čeština | Locale | 121 | 0 | 575 | Partial | 17.39% |
| [csb](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+csb/strings.xml) | Kaszëbsczi | Locale | 3 | 0 | 693 | Partial | 0.43% |
| [cy](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+cy/strings.xml) | Cymraeg | Locale | 38 | 0 | 658 | Partial | 5.46% |
| [da](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-da/strings.xml) | Dansk | Locale | 127 | 0 | 569 | Partial | 18.25% |
| [de](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-de/strings.xml) | Deutsch | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [dz](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+dz/strings.xml) | ཇོང་ཁ | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [el](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-el/strings.xml) | Ελληνικά | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [en-AU](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-en-rAU/strings.xml) | English (Australia) | English | 695 | 1 | 0 | All keys | 100.00% |
| [en-CA](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-en-rCA/strings.xml) | English (Canada) | English | 695 | 1 | 0 | All keys | 100.00% |
| [en-GB](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-en-rGB/strings.xml) | English (United Kingdom) | English | 695 | 1 | 0 | All keys | 100.00% |
| [en-IN](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-en-rIN/strings.xml) | English (India) | English | 695 | 1 | 0 | All keys | 100.00% |
| [en-SG](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-en-rSG/strings.xml) | English (Singapore) | English | 695 | 1 | 0 | All keys | 100.00% |
| [en-US](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-en-rUS/strings.xml) | English (United States) | English | 695 | 1 | 0 | All keys | 100.00% |
| [en-XV](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+en+XV/strings.xml) | English (vertical layout test) | Test mode | 695 | 1 | 0 | All keys | 100.00% |
| [eo](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+eo/strings.xml) | Esperanto | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [es-419](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+es+419/strings.xml) | Español (América Latina) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [es-ES](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+es+ES/strings.xml) | Español (España) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [et](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+et/strings.xml) | Eesti | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [eu-ES](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-eu-rES/strings.xml) | Euskara (Espainia) | Locale | 123 | 0 | 573 | Partial | 17.67% |
| [fa](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-fa/strings.xml) | فارسی | Locale | 113 | 0 | 583 | Partial | 16.24% |
| [fa-IR](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-fa-rIR/strings.xml) | فارسی (ایران) | Locale | 57 | 0 | 639 | Partial | 8.19% |
| [fi](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-fi/strings.xml) | Suomi | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [fr](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-fr/strings.xml) | Français | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [fy](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+fy/strings.xml) | Frysk | Locale | 41 | 0 | 655 | Partial | 5.89% |
| [ga](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ga/strings.xml) | Gaeilge | Locale | 11 | 0 | 685 | Partial | 1.58% |
| [gd](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+gd/strings.xml) | Gàidhlig | Locale | 76 | 0 | 620 | Partial | 10.92% |
| [gl](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-gl/strings.xml) | Galego | Locale | 116 | 0 | 580 | Partial | 16.67% |
| [gu](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-gu/strings.xml) | ગુજરાતી | Locale | 72 | 0 | 624 | Partial | 10.34% |
| [hak-Hant-TW](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+hak+Hant+TW/strings.xml) | 臺灣客家語（四縣腔，漢字） | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [hak-Latn-TW](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+hak+Latn+TW/strings.xml) | Hak-kâ-ngî (Thòi-vân, Si-yen, Pha̍k-fa-sṳ) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [he](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-iw/strings.xml) | עברית | Locale | 134 | 0 | 562 | Partial | 19.25% |
| [hi](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-hi/strings.xml) | हिन्दी | Locale | 59 | 0 | 637 | Partial | 8.48% |
| [hne](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+hne/strings.xml) | छत्तीसगढ़ी | Locale | 16 | 0 | 680 | Partial | 2.30% |
| [hr](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-hr/strings.xml) | Hrvatski | Locale | 98 | 0 | 598 | Partial | 14.08% |
| [hu](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-hu/strings.xml) | Magyar | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [hy](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+hy/strings.xml) | Հայերեն | Locale | 110 | 0 | 586 | Partial | 15.80% |
| [ia](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ia/strings.xml) | Interlingua | Locale | 60 | 0 | 636 | Partial | 8.62% |
| [id](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-in/strings.xml) | Bahasa Indonesia | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [is](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+is/strings.xml) | Íslenska | Locale | 110 | 0 | 586 | Partial | 15.80% |
| [it](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-it/strings.xml) | Italiano | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ja](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ja/strings.xml) | 日本語 | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [jje](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+jje/strings.xml) | 제주말 | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [jv](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+jv/strings.xml) | Jawa | Locale | 5 | 0 | 691 | Partial | 0.72% |
| [ka](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ka/strings.xml) | ქართული | Locale | 121 | 0 | 575 | Partial | 17.39% |
| [kab](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-kab/strings.xml) | Taqbaylit | Locale | 103 | 0 | 593 | Partial | 14.80% |
| [kk](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-kk/strings.xml) | Қазақша | Locale | 123 | 0 | 573 | Partial | 17.67% |
| [km](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+km/strings.xml) | ភាសាខ្មែរ | Locale | 41 | 0 | 655 | Partial | 5.89% |
| [kn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-kn/strings.xml) | ಕನ್ನಡ | Locale | 70 | 0 | 626 | Partial | 10.06% |
| [ko-Kore-KR](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ko+Kore+KR/strings.xml) | 한국어 (한글·漢字 혼용, 대한민국) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ko-KP](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ko+KP/strings.xml) | 조선말 (조선민주주의인민공화국) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ko-KR](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ko+KR/strings.xml) | 한국어 (대한민국) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ku](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ku/strings.xml) | Kurdî | Locale | 4 | 0 | 692 | Partial | 0.57% |
| [ky](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ky/strings.xml) | Кыргызча | Locale | 35 | 0 | 661 | Partial | 5.03% |
| [la](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+la/strings.xml) | Latina | Locale | 8 | 0 | 688 | Partial | 1.15% |
| [lo](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+lo/strings.xml) | ລາວ | Locale | 31 | 0 | 665 | Partial | 4.45% |
| [lt](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-lt/strings.xml) | Lietuvių | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [lv](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+lv/strings.xml) | Latviešu | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [lzh-Hant](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+lzh+Hant/strings.xml) | 文言（繁體） | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [mai](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+mai/strings.xml) | मैथिली | Locale | 38 | 0 | 658 | Partial | 5.46% |
| [mk](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-mk/strings.xml) | Македонски | Locale | 74 | 0 | 622 | Partial | 10.63% |
| [ml-IN](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ml-rIN/strings.xml) | മലയാളം (ഇന്ത്യ) | Locale | 59 | 0 | 637 | Partial | 8.48% |
| [mn-Cyrl-MN](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+mn+Cyrl+MN/strings.xml) | Монгол (Кирилл, Монгол Улс) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [mn-Mong](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+mn+Mong/strings.xml) | ᠮᠣᠩᠭᠤᠯ ᠬᠡᠯᠡ | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [mnc-Mong](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+mnc+Mong/strings.xml) | ᠮᠠᠨᠵᡠ ᡤᡳᠰᡠᠨ | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [mr](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+mr/strings.xml) | मराठी | Locale | 99 | 0 | 597 | Partial | 14.22% |
| [ms](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ms/strings.xml) | Bahasa Melayu | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [mww](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+mww/strings.xml) | Hmong Daw | Locale | 4 | 0 | 692 | Partial | 0.57% |
| [my](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+my/strings.xml) | မြန်မာဘာသာ | Locale | 74 | 0 | 622 | Partial | 10.63% |
| [nan-Hant-TW](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+nan+Hant+TW/strings.xml) | 臺灣台語（漢字） | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [nan-Latn-TW](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+nan+Latn+TW/strings.xml) | Tâi-gí (Tâi-oân, Pe̍h-ōe-jī) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [nds](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+nds/strings.xml) | Plattdüütsch | Locale | 32 | 0 | 664 | Partial | 4.60% |
| [ne](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ne/strings.xml) | नेपाली | Locale | 74 | 0 | 622 | Partial | 10.63% |
| [nl](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-nl/strings.xml) | Nederlands | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [nn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+nn/strings.xml) | Norsk nynorsk | Locale | 110 | 0 | 586 | Partial | 15.80% |
| [no](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-no/strings.xml) | Norsk | Locale | 115 | 0 | 581 | Partial | 16.52% |
| [oc](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+oc/strings.xml) | Occitan | Locale | 88 | 0 | 608 | Partial | 12.64% |
| [pa-IN](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-pa-rIN/strings.xml) | ਪੰਜਾਬੀ (ਭਾਰਤ) | Locale | 107 | 0 | 589 | Partial | 15.37% |
| [pl](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-pl/strings.xml) | Polski | Locale | 166 | 0 | 530 | Partial | 23.85% |
| [ps](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ps/strings.xml) | پښتو | Locale | 45 | 0 | 651 | Partial | 6.47% |
| [pt-BR](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-pt-rBR/strings.xml) | Português (Brasil) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [pt-PT](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+pt+PT/strings.xml) | Português (Portugal) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [qaa-Zsye-XV](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+qaa+Zsye+XV/strings.xml) | 😀 Emoji (vertical test; English hints) | Test mode | 695 | 1 | 0 | All keys | 100.00% |
| [ro](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ro/strings.xml) | Română | Locale | 127 | 0 | 569 | Partial | 18.25% |
| [ru](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ru/strings.xml) | Русский | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [rw](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+rw/strings.xml) | Ikinyarwanda | Locale | 14 | 0 | 682 | Partial | 2.01% |
| [ryu](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ryu/strings.xml) | うちなーぐち | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [sd](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-sd/strings.xml) | سنڌي | Locale | 60 | 0 | 636 | Partial | 8.62% |
| [se](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+se/strings.xml) | Davvisámegiella | Locale | 28 | 0 | 668 | Partial | 4.02% |
| [shn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+shn/strings.xml) | တႆး | Locale | 9 | 0 | 687 | Partial | 1.29% |
| [si](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-si/strings.xml) | සිංහල | Locale | 52 | 0 | 644 | Partial | 7.47% |
| [sk](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-sk/strings.xml) | Slovenčina | Locale | 127 | 0 | 569 | Partial | 18.25% |
| [sl](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-sl/strings.xml) | Slovenščina | Locale | 127 | 0 | 569 | Partial | 18.25% |
| [sq](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-sq/strings.xml) | Shqip | Locale | 65 | 0 | 631 | Partial | 9.34% |
| [sr-Cyrl](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+sr+Cyrl/strings.xml) | Српски (Ћирилица) | Locale | 170 | 0 | 526 | Partial | 24.43% |
| [sr-Latn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+sr+Latn/strings.xml) | Srpski (Latinica) | Locale | 168 | 0 | 528 | Partial | 24.14% |
| [sv](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-sv/strings.xml) | Svenska | Locale | 127 | 0 | 569 | Partial | 18.25% |
| [sw](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-sw/strings.xml) | Kiswahili | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [ta](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ta/strings.xml) | தமிழ் | Locale | 96 | 0 | 600 | Partial | 13.79% |
| [tdd](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+tdd/strings.xml) | ᥖᥭᥰ ᥖᥬᥲ ᥑᥨᥒᥰ | Locale | 7 | 0 | 689 | Partial | 1.01% |
| [te](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-te/strings.xml) | తెలుగు | Locale | 97 | 0 | 599 | Partial | 13.94% |
| [th](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-th/strings.xml) | ไทย | Locale | 164 | 0 | 532 | Partial | 23.56% |
| [tl](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-tl/strings.xml) | Tagalog | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [tok](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+tok/strings.xml) | toki pona | Locale | 9 | 0 | 687 | Partial | 1.29% |
| [tr](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-tr/strings.xml) | Türkçe | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [tt-Cyrl](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+tt+Cyrl/strings.xml) | Татарча (Кирилл) | Locale | 19 | 0 | 677 | Partial | 2.73% |
| [tt-Latn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+tt+Latn/strings.xml) | Tatarça (Latin) | Locale | 19 | 0 | 677 | Partial | 2.73% |
| [ug](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+ug/strings.xml) | ئۇيغۇرچە / Uyghurche | Locale | 69 | 0 | 627 | Partial | 9.91% |
| [uk](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-uk/strings.xml) | Українська | Locale | 127 | 0 | 569 | Partial | 18.25% |
| [ur](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-ur/strings.xml) | اردو | Locale | 48 | 0 | 648 | Partial | 6.90% |
| [uz-Latn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+uz+Latn/strings.xml) | Oʻzbekcha | Locale | 33 | 0 | 663 | Partial | 4.74% |
| [vi](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-vi/strings.xml) | Tiếng Việt | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [vi-Hani](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+vi+Hani/strings.xml) | 㗂越（𡨸喃） | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [wa](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+wa/strings.xml) | Walon | Locale | 24 | 0 | 672 | Partial | 3.45% |
| [wuu-Hans](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+wuu+Hans/strings.xml) | 吴语（上海话书面语，简体） | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [xh](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+xh/strings.xml) | IsiXhosa | Locale | 32 | 0 | 664 | Partial | 4.60% |
| [yi](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+yi/strings.xml) | ייִדיש | Locale | 7 | 0 | 689 | Partial | 1.01% |
| [yue-Hant](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+yue+Hant/strings.xml) | 粵語（繁體） | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [yue-Latn](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+yue+Latn/strings.xml) | Cantonese (Latin) | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [za](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-b+za/strings.xml) | Vahcuengh | Locale | 7 | 0 | 689 | Partial | 1.01% |
| [zh-CN](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-zh-rCN/strings.xml) | 简体中文（中国大陆） | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [zh-HK](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-zh-rHK/strings.xml) | 繁體中文（香港） | Locale | 695 | 1 | 0 | All keys | 100.00% |
| [zh-TW](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values-zh-rTW/strings.xml) | 繁體中文（台灣） | Locale | 695 | 1 | 0 | All keys | 100.00% |

## Reproduce

Run from any clone that contains the pinned commit (read-only; Python standard library):

```sh
python3 scan_translation_coverage.py --repo /path/to/AN-Paint --ref 4231edaac45d89c52f51e2b77d0f94a1176ad88c --out ./coverage-output
```

The script reads Git objects at the requested commit, verifies each blob hash, checks exact picker/system inventory equality, excludes translatable=false resources, counts nonempty canonical entries and writes JSON plus this Markdown. JSON includes every missing key, literal-equal-English review keys, local references, locale aliases and input SHA-256/Git-blob provenance.

This scanner does not execute the repository’s structural/placeholder validator or Android tests. Separate verification receipts must identify the exact revision and checks actually performed. A missing-key count is not a localization-quality verdict.

Source workflow: [TRANSLATING.md](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/TRANSLATING.md); [picker tags](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values/app_language_tags.xml); [picker names and aliases](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values/app_language_names.xml); [Android inventory](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/xml/app_locales.xml); [build-time routing mirror](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/build.gradle).
