# Translation entry review: all 171 offered choices

## Merged language-option and identity changes

[PR65](https://github.com/c933103/AN-Paint/pull/65) is merged into the pinned source. Old English(`ang`), Old Norse(`non`), Moroccan Arabic(`ary`) and Standard Moroccan Tamazight(`zgh`) are registered choices with empty exact catalogues and English fallback. They are distinct identities; no broader Arabic, Amazigh or historical-language translation acceptance is implied. Filipino(`fil`) replaces the offered`tl` tag with saved-selection compatibility. Historical Tagalog reviews remain attributed to Tagalog until explicitly re-reviewed as Filipino.

## Current review overview — 15 October 2026

Pinned current source: [develop `edd566a6`](https://github.com/c933103/AN-Paint/commit/edd566a62fe59d8e95bb08fe00f71a2c87dc6ad0). **699 strings + 1 plural resource = 700 entries per choice; 171 offered choices.** A plural is one entry regardless of quantity forms. Direct coverage is **59 full catalogues, 81 nonempty partial catalogues and 31 empty catalogues**.

Across all choices: **2,967 reviewed-current bounded receipts; 35 entries needing re-review; 44,198 present entries unreviewed/unknown; 72,500 exact-catalogue gaps. Total: 119,700 slots (171 × 700).** Six current receipts are test-mode convention checks.

Language-level status remains **0 fully reviewed, 57 broad re-review required, 6 bounded-partial outside that reset, 75 review not established, 31 translation/review not started and 2 test modes**. Bounded partial choices: Hebrew, Armenian, Polish, Serbian Cyrillic, Serbian Latin and Thai.

### What the entry counts mean

- **Reviewed current** requires matching exact source values and accepted bounded review scope without an unresolved finding. Complete dormant linguistic-only and moderate-confidence semantic reviews retain their explicit limits. This is not whole-language, runtime or release certification.
- **Needs re-review¹** includes required corrections, shared source/context concerns, affected aliases and language-identity transfer review, even when hashes match. The draft-saving diagnosis remains an **unproven reachability** investigation rather than a confirmed visible bug. Three legacy background-promise entries remain open with their removed live callsite recorded.
- **Unreviewed / unknown** means no mapped complete current/open receipt. Historical or partial-term evidence may exist. Nine memory-key inheritance checks and 47 historical colour-error narrow-delta reviews remain preserved as partial evidence. One of those HK values now has a later complete review; the other 46 still have no complete-entry credit.
- **Missing** means absent from the exact catalogue. Android inheritance and default-English fallback are separate.
- Broader language mandates and all historical receipts remain preserved. Confidence is not a substitute for scope: a complete bounded review may count; a delta-only review does not become full-entry credit merely because confidence is high.

### French and Japanese catalogue pass and merged follow-ups

- Current **French:680 reviewed /20 open**, including 68 dormant linguistic-only acceptances. **Japanese:689 reviewed /11 open**, including 68 dormant linguistic-only acceptances. Each of the 700 entries now has an explicit current/open disposition; these are completed catalogue passes with remaining findings, not unqualified acceptance.
- The original pass at `647a4b56` added 675 French and 697 Japanese records, plus eight deduplicated earlier French confirmations/helpers. The original 1,290 baseline records and all earlier history remain preserved; one baseline Tagalog record is now historical rather than counted as Filipino.
- Merged [PR78](https://github.com/c933103/AN-Paint/pull/78),[PR79](https://github.com/c933103/AN-Paint/pull/79) and[PR81](https://github.com/c933103/AN-Paint/pull/81) close five exact FR/JA findings after static guard, error-routing and corrected-Japanese-text review. Original findings remain in superseded history.
- Merged [PR80](https://github.com/c933103/AN-Paint/pull/80) supplies the background-neutral memory key. [Complete-value review evidence](https://github.com/c933103/AN-Paint/pull/80#issuecomment-6182923640) supports 50 bounded H/M reviews; 49 remained current after the Tagalog→Filipino identity change; the one identity hold is now independently accepted by the fresh Filipino review below. Nine other values retain partial-only inheritance evidence.
- Merged [PR65](https://github.com/c933103/AN-Paint/pull/65) adds empty `ang`,`ary`,`non` and`zgh` catalogues and changes the offered identity from`tl` to`fil`. Each new empty catalogue has700 missing entries. Two old Tagalog reviews remain historical. Both corresponding current values now have fresh Filipino-specific acceptance below; unchanged bytes alone did not transfer acceptance.
- Merged [PR86](https://github.com/c933103/AN-Paint/pull/86) switches all four unsupported-profile message sites to a new format-neutral key. The two old FR/JA literals are now dormant linguistic-only acceptances. Twelve new values have complete bounded review: French, Japanese, eight English variants, emoji-English test mode, and [fresh Filipino-specific review](https://github.com/c933103/AN-Paint/pull/86#issuecomment-6184251067), with [exact-head Codex response](https://github.com/c933103/AN-Paint/pull/86#issuecomment-6184285983). The historical 47 [handoff deltas](https://github.com/c933103/AN-Paint/pull/86#issuecomment-6183064757) retain their narrow historical scope; a later complete HK review below supplies credit for that one value, while the other 46 remain unknown.
- **Filipino:3 reviewed /0 needing identity review /697 unknown.** The [fresh two-entry complete Filipino review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6185844544) accepts the Commons failure and sampled-memory guidance unchanged, in addition to the earlier generic colour-error review. Semantic confidence is high and idiomatic confidence moderate; no whole-catalogue or device-rendering claim.
- Active mapped records total **3,002 = 2,967 current + 35 open**. Fifteen superseded records are historical, not extra active credits. Fifty-six historical partial records (9 memory + 47 colour) do not themselves earn current credit; one HK colour value is now counted through its later complete receipt.
- [Exact receipts](https://github.com/c933103/AN-Paint/blob/tracking/language-translation-progress-20261012/verification/translation-entry-review-2026-10-13/entry-review-receipts.json) · [Per-language counts and exact keys](https://github.com/c933103/AN-Paint/blob/tracking/language-translation-progress-20261012/verification/translation-entry-review-2026-10-13/entry-review-counts.json) · [Historical FR/JA source/evidence reconciliation](https://github.com/c933103/AN-Paint/blob/tracking/language-translation-progress-20261012/verification/translation-entry-review-2026-10-13/fr-ja-full-catalogue-review-20261015.json).

This publication changes review data, documentation and a data-validator only. It does not rerun or independently certify application tests, installed layout, fonts, external-provider terms, release readiness or whole-language acceptance.

### Hong Kong Chinese bounded successor

[Original complete 270-key receipt and independently reviewed repairs](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6184969042): 260 active static accepts, 4 linguistic-only accepts and 6 open findings, disjoint from the two preceding HK receipts. After the two merged PR90 repairs, current **Hong Kong Chinese:268 reviewed /4 open /428 unknown**. Five coherent cohorts cover save/recovery, formats/import/export, memory/errors and assembly/crop controls; this is not a completed HK catalogue pass.

The live picker and New-image hint contexts are corrected in merged source. The old BMP/GIF diagnostic is now accepted as dormant wording, and the new generic-colour value has complete current HK review. Four findings remain explicit: unproven generic-busy reachability, external-link diagnosis, native-component diagnosis and dormant background wording. Merged [PR90](https://github.com/c933103/AN-Paint/pull/90) applies the independently accepted complete help and crop-plural corrections. [Exact-value acceptance](https://github.com/c933103/AN-Paint/pull/90#issuecomment-6185032467) matches merged source; [clean Codex and four-job premerge CI](https://github.com/c933103/AN-Paint/pull/90#issuecomment-6185299268) are separate technical evidence. Only these two HK findings move from open to current; their original findings remain in superseded history. Shared English/French/Japanese findings and broader obligations remain open.

### Current per-language entry counts

| Language / choice | Reviewed current | Needs re-review¹ | Unreviewed / unknown | Missing | Total | Broader status |
|---|---:|---:|---:|---:|---:|---|
| `en-001` English (International) | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `af` Afrikaans | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `ain-Kana` アイヌ イタㇰ | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `ain-Latn` Aynu itak | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `am` አማርኛ | 0 | 0 | 12 | 688 | 700 | Not established |
| `ang` Ænglisc | 0 | 0 | 0 | 700 | 700 | Not started |
| `ar` العربية | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `ary` الدارجة المغربية | 0 | 0 | 0 | 700 | 700 | Not started |
| `as` অসমীয়া | 0 | 0 | 0 | 700 | 700 | Not started |
| `ast` Asturianu | 0 | 0 | 86 | 614 | 700 | Not established |
| `az` Azərbaycanca | 0 | 0 | 57 | 643 | 700 | Not established |
| `be` Беларуская | 0 | 0 | 108 | 592 | 700 | Not established |
| `bg` Български | 0 | 0 | 127 | 573 | 700 | Not established |
| `bn` বাংলা | 0 | 0 | 103 | 597 | 700 | Not established |
| `bo` བོད་ཡིག | 1 | 0 | 699 | 0 | 700 | Broad re-review |
| `br` Brezhoneg | 0 | 0 | 85 | 615 | 700 | Not established |
| `bs` Bosanski | 0 | 0 | 117 | 583 | 700 | Not established |
| `ca` Català | 0 | 0 | 127 | 573 | 700 | Not established |
| `ca-ES-valencia` Valencià | 0 | 0 | 95 | 605 | 700 | Not established |
| `ceb` Cebuano | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `ch` Chamoru | 0 | 0 | 0 | 700 | 700 | Not started |
| `chr` ᏣᎳᎩ | 0 | 0 | 0 | 700 | 700 | Not started |
| `ckb` کوردی | 0 | 0 | 40 | 660 | 700 | Not established |
| `cs` Čeština | 0 | 0 | 121 | 579 | 700 | Not established |
| `csb` Kaszëbsczi | 0 | 0 | 3 | 697 | 700 | Not established |
| `cy` Cymraeg | 0 | 0 | 38 | 662 | 700 | Not established |
| `da` Dansk | 0 | 0 | 127 | 573 | 700 | Not established |
| `de` Deutsch | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `dz` ཇོང་ཁ | 1 | 0 | 699 | 0 | 700 | Broad re-review |
| `el` Ελληνικά | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `en-AU` English (Australia) | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `en-CA` English (Canada) | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `en-GB` English (United Kingdom) | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `en-IN` English (India) | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `en-SG` English (Singapore) | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `en-US` English (United States) | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `en-XV` English (vertical layout test) | 3 | 0 | 697 | 0 | 700 | Test mode |
| `eo` Esperanto | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `es-419` Español (América Latina) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `es-ES` Español (España) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `et` Eesti | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `eu-ES` Euskara (Espainia) | 0 | 0 | 123 | 577 | 700 | Not established |
| `fa` فارسی | 0 | 0 | 113 | 587 | 700 | Not established |
| `fa-IR` فارسی (ایران) | 0 | 0 | 57 | 643 | 700 | Not established |
| `fi` Suomi | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `fil` Filipino | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `fr` Français | 680 | 20 | 0 | 0 | 700 | Broad re-review |
| `fy` Frysk | 0 | 0 | 41 | 659 | 700 | Not established |
| `ga` Gaeilge | 0 | 0 | 11 | 689 | 700 | Not established |
| `gd` Gàidhlig | 0 | 0 | 76 | 624 | 700 | Not established |
| `gl` Galego | 0 | 0 | 116 | 584 | 700 | Not established |
| `gu` ગુજરાતી | 0 | 0 | 72 | 628 | 700 | Not established |
| `ha` Hausa | 0 | 0 | 0 | 700 | 700 | Not started |
| `hak-Hant-TW` 臺灣客家語（四縣腔，漢字） | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `hak-Latn-TW` Hak-kâ-ngî (Thòi-vân, Si-yen, Pha̍k-fa-sṳ) | 1 | 0 | 699 | 0 | 700 | Broad re-review |
| `he` עברית | 1 | 0 | 133 | 566 | 700 | Bounded partial |
| `hi` हिन्दी | 0 | 0 | 59 | 641 | 700 | Not established |
| `hne` छत्तीसगढ़ी | 0 | 0 | 16 | 684 | 700 | Not established |
| `hr` Hrvatski | 0 | 0 | 98 | 602 | 700 | Not established |
| `ht` Kreyòl ayisyen | 0 | 0 | 0 | 700 | 700 | Not started |
| `hu` Magyar | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `hy` Հայերեն | 1 | 0 | 109 | 590 | 700 | Bounded partial |
| `ia` Interlingua | 0 | 0 | 60 | 640 | 700 | Not established |
| `id` Bahasa Indonesia | 602 | 0 | 98 | 0 | 700 | Broad re-review |
| `ig` Igbo | 0 | 0 | 0 | 700 | 700 | Not started |
| `is` Íslenska | 0 | 0 | 110 | 590 | 700 | Not established |
| `it` Italiano | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `ja` 日本語 | 689 | 11 | 0 | 0 | 700 | Broad re-review |
| `jje` 제주말 | 1 | 0 | 699 | 0 | 700 | Broad re-review |
| `jv` Jawa | 0 | 0 | 5 | 695 | 700 | Not established |
| `ka` ქართული | 0 | 0 | 121 | 579 | 700 | Not established |
| `kab` Taqbaylit | 0 | 0 | 103 | 597 | 700 | Not established |
| `kk` Қазақша | 0 | 0 | 123 | 577 | 700 | Not established |
| `km` ភាសាខ្មែរ | 0 | 0 | 41 | 659 | 700 | Not established |
| `kn` ಕನ್ನಡ | 0 | 0 | 70 | 630 | 700 | Not established |
| `ko-Kore-KR` 한국어 (한글·漢字 혼용, 대한민국) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `ko-KP` 조선말 (조선민주주의인민공화국) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `ko-KR` 한국어 (대한민국) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `ku` Kurdî | 0 | 0 | 4 | 696 | 700 | Not established |
| `ky` Кыргызча | 0 | 0 | 35 | 665 | 700 | Not established |
| `la` Latina | 0 | 0 | 8 | 692 | 700 | Not established |
| `ln` Lingála | 0 | 0 | 0 | 700 | 700 | Not started |
| `lo` ລາວ | 0 | 0 | 31 | 669 | 700 | Not established |
| `lt` Lietuvių | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `lv` Latviešu | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `lzh-Hant` 文言（繁體） | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `mai` मैथिली | 0 | 0 | 38 | 662 | 700 | Not established |
| `mi` Māori | 0 | 0 | 0 | 700 | 700 | Not started |
| `mk` Македонски | 0 | 0 | 74 | 626 | 700 | Not established |
| `ml-IN` മലയാളം (ഇന്ത്യ) | 0 | 0 | 59 | 641 | 700 | Not established |
| `mn-Cyrl-MN` Монгол (Кирилл, Монгол Улс) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `mn-Mong` ᠮᠣᠩᠭᠤᠯ ᠬᠡᠯᠡ | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `mnc-Mong` ᠮᠠᠨᠵᡠ ᡤᡳᠰᡠᠨ | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `mr` मराठी | 0 | 0 | 99 | 601 | 700 | Not established |
| `ms` Bahasa Melayu | 606 | 0 | 94 | 0 | 700 | Broad re-review |
| `mww` Hmong Daw | 0 | 0 | 4 | 696 | 700 | Not established |
| `my` မြန်မာဘာသာ | 0 | 0 | 74 | 626 | 700 | Not established |
| `nan-Hant-TW` 臺灣台語（漢字） | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `nan-Latn-TW` Tâi-gí (Tâi-oân, Pe̍h-ōe-jī) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `nch` Mexicano (Central Huasteca) | 0 | 0 | 0 | 700 | 700 | Not started |
| `nds` Plattdüütsch | 0 | 0 | 32 | 668 | 700 | Not established |
| `ne` नेपाली | 0 | 0 | 74 | 626 | 700 | Not established |
| `nhe` Náhuatl (Eastern Huasteca) | 0 | 0 | 0 | 700 | 700 | Not started |
| `nhw` Náhuatl (Western Huasteca) | 0 | 0 | 0 | 700 | 700 | Not started |
| `nl` Nederlands | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `nn` Norsk nynorsk | 0 | 0 | 110 | 590 | 700 | Not established |
| `no` Norsk | 0 | 0 | 115 | 585 | 700 | Not established |
| `non` Norrœna | 0 | 0 | 0 | 700 | 700 | Not started |
| `nv` Diné bizaad | 0 | 0 | 0 | 700 | 700 | Not started |
| `oc` Occitan | 0 | 0 | 88 | 612 | 700 | Not established |
| `pa-IN` ਪੰਜਾਬੀ (ਭਾਰਤ) | 0 | 0 | 107 | 593 | 700 | Not established |
| `pcm` Naijá | 0 | 0 | 0 | 700 | 700 | Not started |
| `pl` Polski | 1 | 0 | 165 | 534 | 700 | Bounded partial |
| `ps` پښتو | 0 | 0 | 45 | 655 | 700 | Not established |
| `pt-BR` Português (Brasil) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `pt-PT` Português (Portugal) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `qaa-Zsye-XV` 😀 Emoji (vertical test; English hints) | 3 | 0 | 697 | 0 | 700 | Test mode |
| `qug` Kichwa (Chimborazo) | 0 | 0 | 0 | 700 | 700 | Not started |
| `quh` Qhichwa (South Bolivian) | 0 | 0 | 0 | 700 | 700 | Not started |
| `quy` Qichwa (Ayacucho / Chanka) | 0 | 0 | 0 | 700 | 700 | Not started |
| `quz` Qichwa (Cusco) | 0 | 0 | 0 | 700 | 700 | Not started |
| `ro` Română | 0 | 0 | 127 | 573 | 700 | Not established |
| `ru` Русский | 3 | 0 | 697 | 0 | 700 | Broad re-review |
| `rw` Ikinyarwanda | 0 | 0 | 14 | 686 | 700 | Not established |
| `ryu` うちなーぐち | 1 | 0 | 699 | 0 | 700 | Broad re-review |
| `sa` संस्कृतम् | 0 | 0 | 0 | 700 | 700 | Not started |
| `sd` سنڌي | 0 | 0 | 60 | 640 | 700 | Not established |
| `se` Davvisámegiella | 0 | 0 | 28 | 672 | 700 | Not established |
| `shn` တႆး | 0 | 0 | 9 | 691 | 700 | Not established |
| `si` සිංහල | 0 | 0 | 52 | 648 | 700 | Not established |
| `sk` Slovenčina | 0 | 0 | 127 | 573 | 700 | Not established |
| `sl` Slovenščina | 0 | 0 | 127 | 573 | 700 | Not established |
| `sm` Gagana Samoa | 0 | 0 | 0 | 700 | 700 | Not started |
| `so` Soomaaliga | 0 | 0 | 0 | 700 | 700 | Not started |
| `sq` Shqip | 0 | 0 | 65 | 635 | 700 | Not established |
| `sr-Cyrl` Српски (Ћирилица) | 1 | 0 | 169 | 530 | 700 | Bounded partial |
| `sr-Latn` Srpski (Latinica) | 1 | 0 | 167 | 532 | 700 | Bounded partial |
| `su` Sunda | 0 | 0 | 0 | 700 | 700 | Not started |
| `sv` Svenska | 0 | 0 | 127 | 573 | 700 | Not established |
| `sw` Kiswahili | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `ta` தமிழ் | 0 | 0 | 96 | 604 | 700 | Not established |
| `tdd` ᥖᥭᥰ ᥖᥬᥲ ᥑᥨᥒᥰ | 0 | 0 | 7 | 693 | 700 | Not established |
| `te` తెలుగు | 0 | 0 | 97 | 603 | 700 | Not established |
| `tg` Тоҷикӣ | 0 | 0 | 0 | 700 | 700 | Not started |
| `th` ไทย | 1 | 0 | 163 | 536 | 700 | Bounded partial |
| `tok` toki pona | 0 | 0 | 9 | 691 | 700 | Not established |
| `tpi` Tok Pisin | 0 | 0 | 0 | 700 | 700 | Not started |
| `tr` Türkçe | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `tt-Cyrl` Татарча (Кирилл) | 0 | 0 | 19 | 681 | 700 | Not established |
| `tt-Latn` Tatarça (Latin) | 0 | 0 | 19 | 681 | 700 | Not established |
| `ug` ئۇيغۇرچە / Uyghurche | 0 | 0 | 69 | 631 | 700 | Not established |
| `uk` Українська | 0 | 0 | 127 | 573 | 700 | Not established |
| `ur` اردو | 0 | 0 | 48 | 652 | 700 | Not established |
| `uz-Latn` Oʻzbekcha | 0 | 0 | 33 | 667 | 700 | Not established |
| `vi` Tiếng Việt | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `vi-Hani` 㗂越（𡨸喃） | 1 | 0 | 699 | 0 | 700 | Broad re-review |
| `wa` Walon | 0 | 0 | 24 | 676 | 700 | Not established |
| `wo` Wolof | 0 | 0 | 0 | 700 | 700 | Not started |
| `wuu-Hans` 吴语（上海话书面语，简体） | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `xh` IsiXhosa | 0 | 0 | 32 | 668 | 700 | Not established |
| `yi` ייִדיש | 0 | 0 | 7 | 693 | 700 | Not established |
| `yo` Yorùbá | 0 | 0 | 0 | 700 | 700 | Not started |
| `yua` Maaya t’aan | 0 | 0 | 0 | 700 | 700 | Not started |
| `yue-Hant` 粵語（繁體） | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `yue-Latn` Cantonese (Latin) | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `za` Vahcuengh | 0 | 0 | 7 | 693 | 700 | Not established |
| `zgh` ⵜⴰⵎⴰⵣⵉⵖⵜ / Tamaziɣt (Morocco) | 0 | 0 | 0 | 700 | 700 | Not started |
| `zh-CN` 简体中文（中国大陆） | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `zh-HK` 繁體中文（香港） | 268 | 4 | 428 | 0 | 700 | Broad re-review |
| `zh-TW` 繁體中文（台灣） | 2 | 0 | 698 | 0 | 700 | Broad re-review |
| `zu` isiZulu | 0 | 0 | 0 | 700 | 700 | Not started |

¹ An open source/linguistic/identity finding remains needing re-review even when exact values are unchanged. No automatic acceptance follows from merge, resource presence, matching hashes, or a test passing.

### Preserved earlier review checkpoints

The material below remains historical evidence at its own pinned source and denominator. Earlier167-choice /698-entry or699-entry figures are superseded by the current171-choice /700-entry table above.

### Fresh review evidence and merged correction

[Indonesian current-pair review](https://github.com/c933103/AN-Paint/blob/tracking/language-translation-progress-20261012/verification/translation-entry-review-2026-10-13/indonesian-budget-rereview.md) · [Russian full-resource review and proposed correction](https://github.com/c933103/AN-Paint/blob/tracking/language-translation-progress-20261012/verification/translation-entry-review-2026-10-13/russian-crop-rereview.md). The original fresh reviews are pinned to `6a774428`; the [corrected Russian acceptance and current-source binding](https://github.com/c933103/AN-Paint/blob/tracking/language-translation-progress-20261012/verification/translation-entry-review-2026-10-13/merged-russian-current-review.md) bind its merged successor to develop `5cb65ac4`; the unchanged reviewed pair remains current at `647a4b56`. None of the 57 broader language mandates is closed.

### Bounded French shape review

[Ten exact French entries and independent acceptance](https://github.com/c933103/AN-Paint/blob/tracking/language-translation-progress-20261012/verification/translation-entry-review-2026-10-13/french-shape-review.json): Ligne, Courbe, Rectangle, Rectangle arrondi, Ellipse, Polygone, Cœur, Étoile, Flèche and the complete five-pointed Star hint. Values are unchanged; the former Écanevas corruption is absent from these exact entries. The Cœur finding was editorially corrected to describe its œ ligature accurately; the original artifact hash and correction are recorded. This does not close P05-003, GH-013, CAT-021 or a broader language mandate, and supplies no French runtime/rendering approval.

### Bounded French Save/export review — 14 October 2026

[Four exact current pairs and independent acceptance](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6160338774), with [compact machine-readable receipt](https://github.com/c933103/AN-Paint/blob/tracking/language-translation-progress-20261012/verification/translation-entry-review-2026-10-13/french-save-export-review-20261014.json): Save settings reuse, export preserving the image and remembered destination, successful export distinct from saving, and unsaved-change warning. Both independent reviews accept the complete current values unchanged at `647a4b56`; high bounded semantic confidence. One optional idiomatic alternative is recorded without changing the accepted text. No runtime/rendering or whole-language acceptance.

This successor adds exactly four previously unmapped `(fr, key)` receipts: French **15 current / 683 unknown**, aggregate **1,290 current / 0 mapped stale / 45,792 unknown / 69,484 missing**. All preceding 1,286 receipts and superseded history remain unchanged; 167 choices × 698 entries, all broad mandates and the unapplied Cebuano checkbox remain unchanged. The earlier Cebuano checkpoint’s dated 1,286 aggregate recorded in this document is preserved as prior history and is superseded by this current total. Proposed PR66 priority metadata was only a batch-selection aid.

## Preserved historical cohorts and evidence

The dated material below is preserved as historical evidence. Its PR/status claims and 696-key tables are not the current overview above. PR52 and PR55 have since merged; bounded technical acceptance does not supply linguistic sign-off. No historical cohort is rewritten by this new tally.

<details>
<summary>Expand the earlier source/review cohorts (140 + 6 + 21 choices)</summary>

# Translation progress for all 167 tracked language choices

This document is the per-language companion to master tracker #39. The original
140-choice source scan remains pinned below; requested option registrations are
tracked separately from translated UI and release acceptance.

## Current denominator checkpoint: 13 October 2026

Current develop [`7e3aa5ca403a23c6652e32c3f967d6ec7b83689a`](https://github.com/c933103/AN-Paint/commit/7e3aa5ca403a23c6652e32c3f967d6ec7b83689a) offers 167 choices and declares **697 translatable strings + 1 plural resource = 698 resource keys**. A read-only check of the current default resources and all 27 added canonical catalogues confirms **0/697 strings + 0/1 plurals**, or 698 exact-catalogue gaps each. They remain empty with default-English fallback; translation and linguistic review have not advanced.

The 695-string/696-key figures and per-row data below belong to their explicitly pinned historical cohorts and remain unchanged. This checkpoint does not rescan or reclassify the other catalogues, transfer technical acceptance into linguistic acceptance, or change the 475-row reset register: **3 structural + 1 bounded semantic/source distinction complete, 471 pending**.

PR60 changes font notice metadata, tests and documentation only; it changes no translated text, catalogue or licence terms. No new translation work was performed for this count correction.

## Requested option progress

**167 tracked choices = 140 pinned-baseline choices + 6 options from
[PR57](https://github.com/c933103/AN-Paint/pull/57) + 21 options from
[PR58](https://github.com/c933103/AN-Paint/pull/58).** PR57 is merged at `1011233a89a3cac98f56fc2d46a902a9476a1e08`; the first six options are now on develop.
PR57's [accepted CI run](https://github.com/c933103/AN-Paint/actions/runs/38258647977)
includes bounded API30/35 app-language identity and default-resource fallback
checks for the first six options. This is not complete installed-language UI or
linguistic acceptance. PR58 merged as `484d1b31cb113c88351e6d0dbdaa0d503e5dd834`. Its merge tree equals the reviewed source tree. The accepted source is pinned to
[`e3c56d3b70e6`](https://github.com/c933103/AN-Paint/commit/e3c56d3b70e6bf9c87f007c93d247ccb60d01808).

PR58's [accepted four-job CI](https://github.com/c933103/AN-Paint/actions/runs/38264239986) includes API30/35 exact-identity and default-resource fallback assertions, build/source, lint, exact-script generation and the installed API35 suite. This is bounded technical evidence, not full-language UI, glyph or linguistic acceptance. The separate [post-merge push CI](https://github.com/c933103/AN-Paint/actions/runs/38266883873) also passed all four jobs on merge `484d1b31cb113c88351e6d0dbdaa0d503e5dd834`. No release publication is claimed.

The first six are Hausa, Yoruba, Lingala, Sundanese, Igbo and Zulu. The next sixteen requested language groups
are Nigerian Pidgin, Somali, Assamese, Wolof, Haitian Creole, Tok Pisin, Navajo,
Cherokee, Nahuatl, Yucatec Maya, Quechua, Chamorro, Samoan, Māori, Sanskrit and Tajik.
At the pinned PR57/PR58 snapshots, all 27 exact catalogues have **0/695 strings and 0/1 plural resources**,
with 696 gaps each. These translatable app resource keys use default-English
fallback. Translation and linguistic review have not started.

The clarified principal Nahuatl choices are **Central Huasteca (`nch`), Eastern
Huasteca (`nhe`) and Western Huasteca (`nhw`)**. The Quechua choices are **Cusco
(`quz`), Ayacucho/Chanka (`quy`), South Bolivian (`quh`) and Chimborazo Kichwa
(`qug`)**. These are seven concrete individual-language identities; `quz` does
not represent all Southern Quechua, and `qug` does not represent all Ecuadorian
Kichwa. The selection is practical and non-exhaustive. The earlier unpublished
162-option candidate with registered umbrella tags `nah`/`qu` was superseded.
Name bases are source-backed; regional qualifiers are editorial disambiguators.
See the [primary-source decision record](https://github.com/c933103/AN-Paint/blob/e3c56d3b70e6bf9c87f007c93d247ccb60d01808/verification/language-options-second-2026-10-12/principal-variety-decision.md).
Sanskrit `sa` separately retains its IANA macrolanguage scope; define its
translation scope before filling the catalogue. The other 20 second-batch
choices are individual-language tags.

After PR58 merged, the offered inventory is **167 choices: 158 non-English,
7 English and 2 test modes; 59 full-key and 108 partial catalogues**. The
[first six-option snapshot](verification/translation-progress-2026-10-12/pending-language-options.json)
and [second option snapshot](verification/translation-progress-2026-10-12/further-language-options.json)
pin their respective source and status. Their dated snapshots do not replace the
original 140-choice scan. Lower-priority translation work includes the added empty
catalogues; shared locale improvements and new UI messages must cover every
applicable offered choice.

## Baseline and priority

Pinned baseline source scan: **12 October 2026**, `develop` at [4231edaac45d](https://github.com/c933103/AN-Paint/commit/4231edaac45d89c52f51e2b77d0f94a1176ad88c). Review/PR snapshot: 12 October 2026, 12:29 UTC. This is a source/review tracker, not a release certification.

**140 offered choices: 131 non-English locale/script/region choices, 7 English regional choices, and 2 explicitly labelled test modes.** Device default is a setting, not another language. Both the in-app and Android system inventories agree.

**59 exact catalogues contain every source resource; 81 are partial.** The 59 comprise 50 non-English choices, 7 English choices and 2 test modes. None of the 140 choices lacks a catalogue. No whole-language acceptance is inferred from these counts.

Priorities requested by the maintainer:
- Keep filling the 81 baseline partial catalogues and 27 added empty catalogues as lower-priority work.
- Apply relevant non-translation locale improvements across **all** offered languages, including those with incomplete catalogues; do not exclude them because their translations are partial.
- Continue finding newly introduced or still-hardcoded user-facing text, externalize it, and track each new message across every applicable choice. Preserve English and test-mode conventions.

## What the numbers mean

- The pinned baseline denominator is **695 translatable strings (S) + 1 plural resource (P) = 696 resource keys**. There are no translatable string-arrays. Exclude 3 fixed-filename strings and the nontranslatable name/tag/alias arrays. A plural counts as one resource, regardless of quantity count; language-required plural forms still need review.
- Direct coverage counts nonempty entries in the **exact canonical locale catalogue**. A local resource reference counts as present; all such references point to entries in the same catalogue. “Gap” is the exact-catalogue missing-key count, not an assertion that each key displays English. Android can inherit same-language parent/shared resources before default English (for example, fa-IR and ca-ES-valencia). Runtime fallback was not simulated by this scan.
- Equal-to-English text is **not** automatically untranslated and is not subtracted: proper names, codec names, symbols and numeric templates may legitimately match. The detailed JSON lists equality only as a review aid.
- Canonical locale XML is source-authored/maintained. Historical translations/coverage.json, language-options.json and imported catalogues are provenance, not live progress. The generated ko-Kore-KR-anpaint directory only mirrors the mixed-Korean source for routing; it is not another language or translation. Unoffered es/ko catalogues are auxiliary resources.
- Source-key presence, linguistic review, technical checks, representative host rendering, installed-emulator checks, merging and release are separate states. Hardcoded UI, dependency strings, external content and verbatim licence bodies are outside that pinned 696-key denominator.
- Read-only structural/placeholder validation at the pinned revision passed. The stricter completeness check reports 162 expected missing-resource errors across the 81 partial catalogues. No Android test or new linguistic review was performed for this tracker.

## Reading the review and UI columns

The [current reset register](https://github.com/c933103/AN-Paint/blob/ef9394f250af8f7b4f60df2a81e680e668162a56/verification/localization-recheck-register.md) has **475 obligations: 3 structural completions (P07-004/005/006), 1 bounded source/semantic completion (R-005), 471 pending**. The develop copy is stale. These are obligation counts, not language completion percentages. Prior completion claims remain withdrawn unless a newer exact-scope receipt explicitly closes them.

- **P02/P03/P04/P05/P06/P07/P08/P09/P12** identify the original PR/recheck groups. “Pending” means broad independent/reconciliation acceptance is still open; a narrower checked item never closes the entire language. “Not established” for the other 81 does not claim that nobody ever reviewed any of their entries.
- **M03** is the landed response-limit message. Exactly ain-Kana, ain-Latn and mnc-Mong have fresh independent source-assisted review of that one value. 54 other explicit entries await independent language review; 2 are test-mode proposals; 81 choices lack the exact key. “M03 checked” below is one-key acceptance only.
- **Routing** means M03 host/API30+35 resource assertions, not visual or installed-device acceptance. **Host M02/M03** means membership in the bounded Robolectric NATIVE render profiles; M02 remains a candidate. **Installed vertical** means declared PR18/41 vertical-control flows only. **PR34 font/viewport** and **PR34 mixed-Korean** name their bounded installed checks. These are not physical-device, TalkBack or full-language certification.
- M04 render profiles remain failed/incomplete. They are never counted as passed UI evidence here. Native-speaker certification is not established by these records; this is an evidence limit, not an added human-review prerequisite.

Bounded review details: [follow-up record](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/localization-followup-2026-10-06.md), [M03 three-language review](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/commons-metadata-m03-languages-2026-10-12/REVIEW.md), [six-language cursor review](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/shared-cursor-recheck-2026-10-06.md), [F01 individual cases](https://github.com/c933103/AN-Paint/blob/3981b84e6dc53f3a6ca772ae9ae1d7738699a5ea/verification/f01-tiff-wording-2026-10-10/combined-evidence/all-language-inventory.json), [M03 dispositions](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/commons-metadata-m03-2026-10-11/all-language-dispositions.json). Bounded installed evidence: [vertical controls](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6100769642), [PR34 receipt](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6103368757).

## Per-choice progress (140 baseline + 27 requested additions)

Direct = S+P, with percentage of 696 keys. Gap = absent exact-catalogue keys. All rows remain open for their stated next action. Test modes are explicitly separated in their rows. All 27 requested additions are now on develop and are marked with their merged option PR. Option registration and bounded technical checks do not close translation or full UI review.

| Choice / display name | Direct; gap | Independent / bounded review | Bounded UI evidence | Pending PR | Concrete next action |
|---|---:|---|---|---|---|
| `en-001` English (International) [English] | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07 regional wording; review M03 source identity |
| `af` Afrikaans | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `ain-Kana` アイヌ イタㇰ | 695+1 (100.00%); 0 | Pending P09; M03 checked | Routing; host M03 | #52 M02; #55 M04 | Recheck P09; review M02 and F01-C004 |
| `ain-Latn` Aynu itak | 695+1 (100.00%); 0 | Pending P09; M03 checked | Routing; host M03 | #52 M02; #55 M04 | Recheck P09; review M02 and F01-C005 |
| `am` አማርኛ | 12+0 (1.72%); 684 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ar` العربية | 695+1 (100.00%); 0 | Pending P05; crop counts 0–20 checked; M03 pending | Routing; host M02/M03 | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
| `as` অসমীয়া **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `ast` Asturianu | 86+0 (12.36%); 610 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `az` Azərbaycanca | 57+0 (8.19%); 639 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `be` Беларуская | 108+0 (15.52%); 588 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `bg` Български | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `bn` বাংলা | 103+0 (14.80%); 593 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `bo` བོད་ཡིག | 695+1 (100.00%); 0 | Pending P08; language note corrected; M03 pending | Routing | #52 M02; #55 M04 | Recheck P08; review M02/M03; F01-C006 |
| `br` Brezhoneg | 85+0 (12.21%); 611 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `bs` Bosanski | 117+0 (16.81%); 579 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ca` Català | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ca-ES-valencia` Valencià | 95+0 (13.65%); 601 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ceb` Cebuano | 695+1 (100.00%); 0 | Pending P03; M03 pending | Routing | #52 M02; #55 M04 | Recheck P03; review M02/M03; F01-C007 |
| `ch` Chamoru **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `chr` ᏣᎳᎩ **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `ckb` کوردی | 40+0 (5.75%); 656 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `cs` Čeština | 121+0 (17.39%); 575 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `csb` Kaszëbsczi | 3+0 (0.43%); 693 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `cy` Cymraeg | 38+0 (5.46%); 658 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `da` Dansk | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `de` Deutsch | 695+1 (100.00%); 0 | Pending P05; M03 pending | Routing | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
| `dz` ཇོང་ཁ | 695+1 (100.00%); 0 | Pending P08; language note corrected; M03 pending | Routing | #52 M02; #55 M04 | Recheck P08; review M02/M03; F01-C008 |
| `el` Ελληνικά | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07; review M02/M03 |
| `en-AU` English (Australia) [English] | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07 regional wording; review M03 source identity |
| `en-CA` English (Canada) [English] | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07 regional wording; review M03 source identity |
| `en-GB` English (United Kingdom) [English] | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing; host M02/M03 | #52 M02; #55 M04 | Recheck P07 regional wording; review M03 source identity |
| `en-IN` English (India) [English] | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07 regional wording; review M03 source identity |
| `en-SG` English (Singapore) [English] | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07 regional wording; review M03 source identity |
| `en-US` English (United States) [English] | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07 regional wording; review M03 source identity |
| `en-XV` English (vertical layout test) **[test mode]** | 695+1 (100.00%); 0 | Test mode; no natural-language acceptance | Routing; host M02/M03; installed vertical | #52/#55 conventions | Check vertical regressions; preserve explicit test labels |
| `eo` Esperanto | 695+1 (100.00%); 0 | Pending P05; M03 pending | Routing | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
| `es-419` Español (América Latina) | 695+1 (100.00%); 0 | Pending P05; M03 pending | Routing | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
| `es-ES` Español (España) | 695+1 (100.00%); 0 | Pending P05; M03 pending | Routing | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
| `et` Eesti | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `eu-ES` Euskara (Espainia) | 123+0 (17.67%); 573 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `fa` فارسی | 113+0 (16.24%); 583 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `fa-IR` فارسی (ایران) | 57+0 (8.19%); 639 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `fi` Suomi | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `fr` Français | 695+1 (100.00%); 0 | Pending P05; M03 pending | Routing; host M02/M03; PR34 font/viewport | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
| `fy` Frysk | 41+0 (5.89%); 655 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ga` Gaeilge | 11+0 (1.58%); 685 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `gd` Gàidhlig | 76+0 (10.92%); 620 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `gl` Galego | 116+0 (16.67%); 580 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `gu` ગુજરાતી | 72+0 (10.34%); 624 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ha` Hausa **[added in #57]** | 0+0 (0.00%); 696 | Translation/review not started | PR57 API30/35 identity/fallback; full UI pending | — | Low priority: translate 695 strings + 1 plural, then review in UI |
| `hak-Hant-TW` 臺灣客家語（四縣腔，漢字） | 695+1 (100.00%); 0 | Pending P06; paired context checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P06; review M02/M03; F01-C015 |
| `hak-Latn-TW` Hak-kâ-ngî (Thòi-vân, Si-yen, Pha̍k-fa-sṳ) | 695+1 (100.00%); 0 | Pending P06; paired context checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P06; review M02/M03; F01-C016 |
| `he` עברית | 134+0 (19.25%); 562 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `hi` हिन्दी | 59+0 (8.48%); 637 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `hne` छत्तीसगढ़ी | 16+0 (2.30%); 680 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `hr` Hrvatski | 98+0 (14.08%); 598 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ht` Kreyòl ayisyen **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `hu` Magyar | 695+1 (100.00%); 0 | Pending P04; C05 17-value candidate reviewed; M03 pending | Routing; PR52 composition only | #48/#52 C05+M02; #55 M04 | Reconcile C05 candidate; recheck P04; review M02/M03 |
| `hy` Հայերեն | 110+0 (15.80%); 586 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ia` Interlingua | 60+0 (8.62%); 636 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `id` Bahasa Indonesia | 695+1 (100.00%); 0 | Pending P03; 600 short entries checked; M03 pending | Routing | #52 M02; #55 M04 | Review excluded long text/P03; review M02/M03 |
| `ig` Igbo **[added in #57]** | 0+0 (0.00%); 696 | Translation/review not started | PR57 API30/35 identity/fallback; full UI pending | — | Low priority: translate 695 strings + 1 plural, then review in UI |
| `is` Íslenska | 110+0 (15.80%); 586 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `it` Italiano | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07; review M02/M03 |
| `ja` 日本語 | 695+1 (100.00%); 0 | Pending P02; C03 one-key checked; M03 pending | Routing; host M02/M03 | #52 M02; #55 M04 | Recheck P02; review M02/M03 |
| `jje` 제주말 | 695+1 (100.00%); 0 | Pending P09; M03 pending | Routing | #52 M02; #55 M04 | Recheck P09; review M02/M03; F01-C017 |
| `jv` Jawa | 5+0 (0.72%); 691 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ka` ქართული | 121+0 (17.39%); 575 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `kab` Taqbaylit | 103+0 (14.80%); 593 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `kk` Қазақша | 123+0 (17.67%); 573 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `km` ភាសាខ្មែរ | 41+0 (5.89%); 655 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `kn` ಕನ್ನಡ | 70+0 (10.06%); 626 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ko-Kore-KR` 한국어 (한글·漢字 혼용, 대한민국) | 695+1 (100.00%); 0 | Pending P12; bounded Korean context checked; M03 pending | Routing; PR34 mixed-Korean | #52 M02; #55 M04 | Recheck P12; review M02/M03 |
| `ko-KP` 조선말 (조선민주주의인민공화국) | 695+1 (100.00%); 0 | Pending P12; bounded Korean context checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P12; review M02/M03 |
| `ko-KR` 한국어 (대한민국) | 695+1 (100.00%); 0 | Pending P12; bounded Korean context checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P12; review M02/M03 |
| `ku` Kurdî | 4+0 (0.57%); 692 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ky` Кыргызча | 35+0 (5.03%); 661 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `la` Latina | 8+0 (1.15%); 688 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ln` Lingála **[added in #57]** | 0+0 (0.00%); 696 | Translation/review not started | PR57 API30/35 identity/fallback; full UI pending | — | Low priority: translate 695 strings + 1 plural, then review in UI |
| `lo` ລາວ | 31+0 (4.45%); 665 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `lt` Lietuvių | 695+1 (100.00%); 0 | Pending P04; crop counts 0–20 checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `lv` Latviešu | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `lzh-Hant` 文言（繁體） | 695+1 (100.00%); 0 | Pending P06; M03 pending | Routing; host M02/M03; installed vertical | #52 M02; #55 M04 | Recheck P06; review M02/M03 |
| `mai` मैथिली | 38+0 (5.46%); 658 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `mi` Māori **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `mk` Македонски | 74+0 (10.63%); 622 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ml-IN` മലയാളം (ഇന്ത്യ) | 59+0 (8.48%); 637 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `mn-Cyrl-MN` Монгол (Кирилл, Монгол Улс) | 695+1 (100.00%); 0 | Pending P08; language note corrected; M03 pending | Routing | #52 M02; #55 M04 | Recheck P08; review M02/M03 |
| `mn-Mong` ᠮᠣᠩᠭᠤᠯ ᠬᠡᠯᠡ | 695+1 (100.00%); 0 | Pending P08; bounded manuals corrected, language note corrected; M03 pending | Routing; host M02/M03; PR34 font/viewport | #52 M02; #55 M04 | Recheck P08; review M02/M03; F01-C024 |
| `mnc-Mong` ᠮᠠᠨᠵᡠ ᡤᡳᠰᡠᠨ | 695+1 (100.00%); 0 | Pending P09; M03 checked | Routing; host M02/M03; installed vertical | #52 M02; #55 M04 | Recheck P09; review M02 and F01-C025 |
| `mr` मराठी | 99+0 (14.22%); 597 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ms` Bahasa Melayu | 695+1 (100.00%); 0 | Pending P03; 604 short entries checked, R-005 closed only; M03 pending | Routing | #52 M02; #55 M04 | Review excluded long text/P03; review M02/M03 |
| `mww` Hmong Daw | 4+0 (0.57%); 692 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `my` မြန်မာဘာသာ | 74+0 (10.63%); 622 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `nan-Hant-TW` 臺灣台語（漢字） | 695+1 (100.00%); 0 | Pending P06; M03 pending | Routing | #52 M02; #55 M04 | Recheck P06; review M02/M03; F01-C026 |
| `nan-Latn-TW` Tâi-gí (Tâi-oân, Pe̍h-ōe-jī) | 695+1 (100.00%); 0 | Pending P06; M03 pending | Routing | #52 M02; #55 M04 | Recheck P06; review M02/M03; F01-C027 |
| `nch` Mexicano (Central Huasteca) **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `nds` Plattdüütsch | 32+0 (4.60%); 664 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ne` नेपाली | 74+0 (10.63%); 622 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `nhe` Náhuatl (Eastern Huasteca) **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `nhw` Náhuatl (Western Huasteca) **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `nl` Nederlands | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `nn` Norsk nynorsk | 110+0 (15.80%); 586 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `no` Norsk | 115+0 (16.52%); 581 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `nv` Diné bizaad **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `oc` Occitan | 88+0 (12.64%); 608 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `pa-IN` ਪੰਜਾਬੀ (ਭਾਰਤ) | 107+0 (15.37%); 589 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `pcm` Naijá **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `pl` Polski | 166+0 (23.85%); 530 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ps` پښتو | 45+0 (6.47%); 651 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `pt-BR` Português (Brasil) | 695+1 (100.00%); 0 | Pending P07; bounded A01/F01 checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07; review M02/M03 |
| `pt-PT` Português (Portugal) | 695+1 (100.00%); 0 | Pending P07; 3 structural items closed only; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07; review M02/M03 |
| `qaa-Zsye-XV` 😀 Emoji (vertical test; English hints) **[test mode]** | 695+1 (100.00%); 0 | Test mode; no natural-language acceptance | Routing; host M02/M03; installed vertical | #52/#55 conventions | Check vertical regressions; preserve explicit test labels |
| `qug` Kichwa (Chimborazo) **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `quh` Qhichwa (South Bolivian) **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `quy` Qichwa (Ayacucho / Chanka) **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `quz` Qichwa (Cusco) **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `ro` Română | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ru` Русский | 695+1 (100.00%); 0 | Pending P05; crop counts 0–20 checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
| `rw` Ikinyarwanda | 14+0 (2.01%); 682 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ryu` うちなーぐち | 695+1 (100.00%); 0 | Pending P09; M03 pending | Routing | #52 M02; #55 M04 | Recheck P09; review M02/M03; F01-C030 |
| `sa` संस्कृतम् [macrolanguage] **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Decide concrete translation scope, then translate/review 696 keys at lower priority |
| `sd` سنڌي | 60+0 (8.62%); 636 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `se` Davvisámegiella | 28+0 (4.02%); 668 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `shn` တႆး | 9+0 (1.29%); 687 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `si` සිංහල | 52+0 (7.47%); 644 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sk` Slovenčina | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sl` Slovenščina | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sm` Gagana Samoa **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `so` Soomaaliga **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `sq` Shqip | 65+0 (9.34%); 631 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sr-Cyrl` Српски (Ћирилица) | 170+0 (24.43%); 526 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sr-Latn` Srpski (Latinica) | 168+0 (24.14%); 528 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `su` Sunda **[added in #57]** | 0+0 (0.00%); 696 | Translation/review not started | PR57 API30/35 identity/fallback; full UI pending | — | Low priority: translate 695 strings + 1 plural, then review in UI |
| `sv` Svenska | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sw` Kiswahili | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `ta` தமிழ் | 96+0 (13.79%); 600 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `tdd` ᥖᥭᥰ ᥖᥬᥲ ᥑᥨᥒᥰ | 7+0 (1.01%); 689 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `te` తెలుగు | 97+0 (13.94%); 599 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `tg` Тоҷикӣ **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `th` ไทย | 164+0 (23.56%); 532 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `tl` Tagalog | 695+1 (100.00%); 0 | Pending P03; M03 pending | Routing | #52 M02; #55 M04 | Recheck P03; review M02/M03 |
| `tok` toki pona | 9+0 (1.29%); 687 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `tpi` Tok Pisin **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `tr` Türkçe | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07; review M02/M03 |
| `tt-Cyrl` Татарча (Кирилл) | 19+0 (2.73%); 677 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `tt-Latn` Tatarça (Latin) | 19+0 (2.73%); 677 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ug` ئۇيغۇرچە / Uyghurche | 69+0 (9.91%); 627 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `uk` Українська | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ur` اردو | 48+0 (6.90%); 648 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `uz-Latn` Oʻzbekcha | 33+0 (4.74%); 663 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `vi` Tiếng Việt | 695+1 (100.00%); 0 | Pending P12; M03 pending | Routing | #52 M02; #55 M04 | Recheck P12; review M02/M03 |
| `vi-Hani` 㗂越（𡨸喃） | 695+1 (100.00%); 0 | Pending P12; C03 one-key checked; M03 pending | Routing; host M02/M03 | #52 M02; #55 M04 | Recheck P12; review M02/M03; F01-C031 |
| `wa` Walon | 24+0 (3.45%); 672 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `wo` Wolof **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `wuu-Hans` 吴语（上海话书面语，简体） | 695+1 (100.00%); 0 | Pending P06; M03 pending | Routing | #52 M02; #55 M04 | Recheck P06; review M02/M03; F01-C032 |
| `xh` IsiXhosa | 32+0 (4.60%); 664 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `yi` ייִדיש | 7+0 (1.01%); 689 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `yo` Yorùbá **[added in #57]** | 0+0 (0.00%); 696 | Translation/review not started | PR57 API30/35 identity/fallback; full UI pending | — | Low priority: translate 695 strings + 1 plural, then review in UI |
| `yua` Maaya t’aan **[added in #58]** | 0+0 (0.00%); 696 | Translation/review not started | PR58 API30/35 identity/fallback; full UI pending | — | Translate and review all 696 app resource keys at lower priority |
| `yue-Hant` 粵語（繁體） | 695+1 (100.00%); 0 | Pending P02; M03 pending | Routing | #52 M02; #55 M04 | Recheck P02; review M02/M03 |
| `yue-Latn` Cantonese (Latin) | 695+1 (100.00%); 0 | Pending P02; M03 pending | Routing | #52 M02; #55 M04 | Recheck P02; review M02/M03 |
| `za` Vahcuengh | 7+0 (1.01%); 689 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `zh-CN` 简体中文（中国大陆） | 695+1 (100.00%); 0 | Pending P02; M03 pending | Routing | #52 M02; #55 M04 | Recheck P02; review M02/M03 |
| `zh-HK` 繁體中文（香港） | 695+1 (100.00%); 0 | Pending P02; M03 pending | Routing | #52 M02; #55 M04 | Recheck P02; review M02/M03 |
| `zh-TW` 繁體中文（台灣） | 695+1 (100.00%); 0 | Pending P02; M03 pending | Routing | #52 M02; #55 M04 | Recheck P02; review M02/M03 |
| `zu` isiZulu **[added in #57]** | 0+0 (0.00%); 696 | Translation/review not started | PR57 API30/35 identity/fallback; full UI pending | — | Low priority: translate 695 strings + 1 plural, then review in UI |

## Shared open message work and PR boundaries

- **M02 / #47 composed in [#52](https://github.com/c933103/AN-Paint/pull/52)**: 59 explicit candidate values; 81 exact-key gaps. 50 target-language/script proposals remain independently unreviewed; English/test conventions are separate. #52 at `71f4d288` has accepted bounded technical composition evidence but is **unmerged**. It contributes zero landed coverage to this baseline. [M02 per-choice evidence](https://github.com/c933103/AN-Paint/blob/a8074c5c4f3b76767f479c6716d823e61ab06aed/verification/commons-metadata-m02-2026-10-11/all-language-dispositions.json).
- **C05 / #48 composed in #52**: 17 Hungarian attribution values have bounded model/source and technical review. Both remain unmerged. This does not close Hungarian catalogue review.
- **M03 / #54**: landed in this baseline, 59 explicit values and 81 gaps. Only the three exact Ainu/Manchu entries have the newer independent source-assisted review described above; preserve the remaining review statuses.
- **M04 / [#55](https://github.com/c933103/AN-Paint/pull/55)**: head `dc46abc2add7984358565a88fe65c5278212dcf6`, stacked on #52, **unmerged**. All 59 explicit values have bounded independent model/source-assisted review; the 81 other choices still lack the exact key. The initial 53-entry review was superseded by six later decisions. Diagnostic [run 38244193872](https://github.com/c933103/AN-Paint/actions/runs/38244193872) failed; runtime/visual acceptance remains open. Neither proposals nor failed diagnostics increase landed progress. [Per-choice manifest](https://github.com/c933103/AN-Paint/blob/dc46abc2add7984358565a88fe65c5278212dcf6/verification/commons-metadata-m04-2026-10-12/all-language-dispositions.json); [six later decisions](https://github.com/c933103/AN-Paint/blob/dc46abc2add7984358565a88fe65c5278212dcf6/verification/commons-metadata-m04-2026-10-12/linguistic-review/successor-recovered/six-final-decisions-reconstructed.json).
- **M01 and M05–M12**: nine separate reasons remain open for all choices; no language is functionally N/A. English needs extraction/wording review, not translation into another language. [Message inventory](https://github.com/c933103/AN-Paint/blob/c6fbbc7d23483a48bbef066313849129197398ce/verification/commons-metadata-message-inventory-2026-10-09/README.md).
- **F01 TIFF wording**: retain F01-C001–C060 individually (C001 is default English, not a 141st picker choice). 37 bounded corrections landed via #43, with the separate mn-Cyrl-MN C023 correction also landed. The other probable/qualified/uncertain entries and the 81 exact-key gaps keep their distinct statuses. A landed wording correction does not close installed TIFF-dialog or whole-language acceptance.

## Completion checklist and update procedure

- [ ] Re-scan the actual default/source catalogue and both language inventories whenever a source key, locale option or relevant PR changes; record the full source SHA and date.
- [ ] Preserve every offered row. For added/changed messages, record exact keys, per-choice direct source status, fallback, source/context evidence, reviewer disposition and unresolved uncertainty. Detect hardcoded user-facing strings as a separate extraction backlog so the denominator does not hide them.
- [ ] Keep the lower-priority partial-catalogue queue separate from shared locale-engineering work. Apply relevant layout, font, routing, direction, numeric-entry and accessibility improvements to all affected choices and verify their applicable paths.
- [ ] Resolve broad reset/reconciliation obligations individually. Credit a bounded accepted change only to its exact key/scope; do not restore a historical full-language claim.
- [ ] Verify placeholders, plural categories, references, exact script/region, app meaning and consistency; distinguish strings legitimately equal to English. Regional/script inheritance does not prove an independently authored exact variant.
- [ ] Keep structural validation, representative host renders, installed-emulator flows, physical-device/accessibility checks and linguistic acceptance in separate fields. Retain failures and exact tested revisions.
- [ ] Before moving a candidate into landed progress, confirm its merge commit is reachable from the tracked baseline; then rerun counts. A closed PR, CI pass, source rewrite or model review alone is not merge/release/full-language acceptance.
- [ ] Close this umbrella only when every in-scope choice has its required resource coverage and recorded independent review/verification disposition, and the shared message backlog is resolved or explicitly deferred by the maintainer. Test modes retain separate behavior/convention criteria.

Reproduction command (read-only, standard-library Python; run from a clone containing the baseline commit):

```sh
python3 verification/translation-progress-2026-10-12/scan_translation_coverage.py --repo /path/to/AN-Paint --ref 4231edaac45d89c52f51e2b77d0f94a1176ad88c --out ./coverage-output
```

Durable companion files: [scan_translation_coverage.py](verification/translation-progress-2026-10-12/scan_translation_coverage.py), [coverage.md](verification/translation-progress-2026-10-12/coverage.md) (every exact catalogue URL), [coverage-summary.json](verification/translation-progress-2026-10-12/coverage-summary.json), [coverage.json.gz](verification/translation-progress-2026-10-12/coverage.json.gz) (full missing-key/equality/source-hash evidence), [verification.json](verification/translation-progress-2026-10-12/verification.json), [review-map.json](verification/translation-progress-2026-10-12/review-map.json), [independent-review.md](verification/translation-progress-2026-10-12/independent-review.md). The scanner reads immutable Git objects and verifies source blob hashes; it does not edit catalogues or run builds.

Source authority: [English source](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values/strings.xml), [picker tags](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values/app_language_tags.xml), [display names/aliases](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/values/app_language_names.xml), [system locales](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/Paintroid/src/main/res/xml/app_locales.xml), [translation workflow](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/TRANSLATING.md).


</details>


### Cebuano TIFF description correction — 14 October 2026

[PR64](https://github.com/c933103/AN-Paint/pull/64) is merged at develop [`647a4b56`](https://github.com/c933103/AN-Paint/commit/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb). Its tree equals the independently reviewed implementation and composed CI tree. The exact English and accepted Cebuano values, resource identities, original proposal, historical unmerged checkpoint and current outcomes are preserved in [the bounded receipt](verification/translation-entry-review-2026-10-13/cebuano-tiff-correction-20261014.json). Technical-semantic confidence remains high; idiomatic confidence remains moderate. The separately proposed checkbox-label amendment is unchanged and earns no receipt.

The implementation has completed clean exact-head code and security reviews. [PR CI attempt 2](https://github.com/c933103/AN-Paint/actions/runs/38491601846) and [exact merge CI attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38495011152) passed regression/JVM/lint, resource generation, APK/corresponding source and API35. The initial failed API35 evidence-collection attempt remains recorded as failed. All four portrait/landscape PNGs with compression off/on were loaded with Pillow and visually inspected: complete description, ordinary wrapping, reachable description and visible destination button. Captures are preserved on this evidence ref. These are native Robolectric software captures; no Cebuano-specific installed-render or physical-device proof is claimed.

Exactly one bounded description receipt is now current: Cebuano **2 current / 696 unknown**; aggregate **1,286 current / 0 mapped stale / 45,796 unknown / 69,484 missing**, denominator 698 across 167 choices. All preceding 1,285 active receipts and historical superseded receipts remain unchanged. All 167 catalogue partitions and source identities were recomputed. Independent exact-head evidence review is recorded in PR56 discussion. Whole-Cebuano review, all broader obligations and the intentional tracking draft remain open. No release is authorized or published.
