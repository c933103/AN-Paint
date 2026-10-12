# Translation progress for all 146 tracked language choices

This document is the per-language companion to the project’s tracking-PR workflow (master tracker #39). It is a manually refreshed snapshot; no scheduled updater is installed.

## Requested options merged

**146 offered and tracked choices = 140 from the original pinned baseline + 6 options in [PR #57](https://github.com/c933103/AN-Paint/pull/57).**
The option-registration candidate is pinned to [be60964a5b62](https://github.com/c933103/AN-Paint/commit/be60964a5b62c73f6517ec2fa8f58b101ab05c99).
PR57 merged into develop on 12 October 2026 at [`1011233a89a3`](https://github.com/c933103/AN-Paint/commit/1011233a89a3cac98f56fc2d46a902a9476a1e08). Hausa, Igbo, Lingala, Sundanese, Yoruba and
Zulu each have an intentionally empty canonical catalogue: **0/695 strings and
0/1 plurals translated, 696 gaps**. All 696 translatable app resource keys use default-English fallback.
Autonym/tag verification is distinct from UI translation or linguistic acceptance.
[PR57 CI](https://github.com/c933103/AN-Paint/actions/runs/38258647977) passed, including bounded API30/35 identity and default-resource fallback checks. Full installed-language UI review and linguistic acceptance remain open.

The offered inventory is now 146: 137 non-English
choices, 7 English choices and 2 test modes; 59 full and 87 partial catalogues.
The six added rows below and [option progress data](verification/translation-progress-2026-10-12/pending-language-options.json)
track the requested work now. The original 140-choice coverage snapshot and
historical reviews stay pinned and unchanged; their counts do not describe the
merged option addition. Translation filling remains lower priority; shared locale
improvements and new UI messages must include the six choices as applicable.

## Baseline and priority

Last source scan: **12 October 2026**, `develop` at [4231edaac45d](https://github.com/c933103/AN-Paint/commit/4231edaac45d89c52f51e2b77d0f94a1176ad88c). Review/PR snapshot: 12 October 2026, 12:29 UTC. This is a source/review tracker, not a release certification.

**140 offered choices: 131 non-English locale/script/region choices, 7 English regional choices, and 2 explicitly labelled test modes.** Device default is a setting, not another language. Both the in-app and Android system inventories agree.

**59 exact catalogues contain every source resource; 81 are partial.** The 59 comprise 50 non-English choices, 7 English choices and 2 test modes. None of the 140 choices lacks a catalogue. No whole-language acceptance is inferred from these counts.

Priorities requested by the maintainer:
- Keep filling the 81 baseline partial catalogues and six added empty catalogues as lower-priority work.
- Apply relevant non-translation locale improvements across **all** offered languages, including those with incomplete catalogues; do not exclude them because their translations are partial.
- Continue finding newly introduced or still-hardcoded user-facing text, externalize it, and track each new message across every applicable choice. Preserve English and test-mode conventions.

## What the numbers mean

- The common denominator is **695 translatable strings (S) + 1 plural resource (P) = 696 resource keys**. There are no translatable string-arrays. Exclude 3 fixed-filename strings and the nontranslatable name/tag/alias arrays. A plural counts as one resource, regardless of quantity count; language-required plural forms still need review.
- Direct coverage counts nonempty entries in the **exact canonical locale catalogue**. A local resource reference counts as present; all such references point to entries in the same catalogue. “Gap” is the exact-catalogue missing-key count, not an assertion that each key displays English. Android can inherit same-language parent/shared resources before default English (for example, fa-IR and ca-ES-valencia). Runtime fallback was not simulated by this scan.
- Equal-to-English text is **not** automatically untranslated and is not subtracted: proper names, codec names, symbols and numeric templates may legitimately match. The detailed JSON lists equality only as a review aid.
- Canonical locale XML is source-authored/maintained. Historical translations/coverage.json, language-options.json and imported catalogues are provenance, not live progress. The generated ko-Kore-KR-anpaint directory only mirrors the mixed-Korean source for routing; it is not another language or translation. Unoffered es/ko catalogues are auxiliary resources.
- Source-key presence, linguistic review, technical checks, representative host rendering, installed-emulator checks, merging and release are separate states. Hardcoded UI, dependency strings, external content and verbatim licence bodies are outside the 696-key denominator.
- Read-only structural/placeholder validation at the pinned revision passed. The stricter completeness check reports 162 expected missing-resource errors across the 81 partial catalogues. No Android test or new linguistic review was performed for this tracker.

## Reading the review and UI columns

The [current reset register](https://github.com/c933103/AN-Paint/blob/ef9394f250af8f7b4f60df2a81e680e668162a56/verification/localization-recheck-register.md) has **475 obligations: 3 structural completions (P07-004/005/006), 1 bounded source/semantic completion (R-005), 471 pending**. The develop copy is stale. These are obligation counts, not language completion percentages. Prior completion claims remain withdrawn unless a newer exact-scope receipt explicitly closes them.

- **P02/P03/P04/P05/P06/P07/P08/P09/P12** identify the original PR/recheck groups. “Pending” means broad independent/reconciliation acceptance is still open; a narrower checked item never closes the entire language. “Not established” for the other 81 does not claim that nobody ever reviewed any of their entries.
- **M03** is the landed response-limit message. Exactly ain-Kana, ain-Latn and mnc-Mong have fresh independent source-assisted review of that one value. 54 other explicit entries await independent language review; 2 are test-mode proposals; 81 choices lack the exact key. “M03 checked” below is one-key acceptance only.
- **Routing** means M03 host/API30+35 resource assertions, not visual or installed-device acceptance. **Host M02/M03** means membership in the bounded Robolectric NATIVE render profiles; M02 remains a candidate. **Installed vertical** means declared PR18/41 vertical-control flows only. **PR34 font/viewport** and **PR34 mixed-Korean** name their bounded installed checks. These are not physical-device, TalkBack or full-language certification.
- M04 render profiles remain failed/incomplete. They are never counted as passed UI evidence here. Native-speaker certification is not established by these records; this is an evidence limit, not an added human-review prerequisite.

Bounded review details: [follow-up record](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/localization-followup-2026-10-06.md), [M03 three-language review](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/commons-metadata-m03-languages-2026-10-12/REVIEW.md), [six-language cursor review](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/shared-cursor-recheck-2026-10-06.md), [F01 individual cases](https://github.com/c933103/AN-Paint/blob/3981b84e6dc53f3a6ca772ae9ae1d7738699a5ea/verification/f01-tiff-wording-2026-10-10/combined-evidence/all-language-inventory.json), [M03 dispositions](https://github.com/c933103/AN-Paint/blob/4231edaac45d89c52f51e2b77d0f94a1176ad88c/verification/commons-metadata-m03-2026-10-11/all-language-dispositions.json). Bounded installed evidence: [vertical controls](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6100769642), [PR34 receipt](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6103368757).

## Per-choice progress (140 original baseline + 6 merged additions)

Direct = S+P, with percentage of 696 keys. Gap = absent exact-catalogue keys. All rows remain open for their stated next action. Test modes are explicitly separated in their rows. Rows labelled “added in #57” are merged option registrations with empty catalogues; source-key presence and language acceptance remain distinct.

| Choice / display name | Direct; gap | Independent / bounded review | Bounded UI evidence | Pending PR | Concrete next action |
|---|---:|---|---|---|---|
| `en-001` English (International) [English] | 695+1 (100.00%); 0 | Pending P07; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07 regional wording; review M03 source identity |
| `af` Afrikaans | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `ain-Kana` アイヌ イタㇰ | 695+1 (100.00%); 0 | Pending P09; M03 checked | Routing; host M03 | #52 M02; #55 M04 | Recheck P09; review M02 and F01-C004 |
| `ain-Latn` Aynu itak | 695+1 (100.00%); 0 | Pending P09; M03 checked | Routing; host M03 | #52 M02; #55 M04 | Recheck P09; review M02 and F01-C005 |
| `am` አማርኛ | 12+0 (1.72%); 684 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ar` العربية | 695+1 (100.00%); 0 | Pending P05; crop counts 0–20 checked; M03 pending | Routing; host M02/M03 | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
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
| `nds` Plattdüütsch | 32+0 (4.60%); 664 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ne` नेपाली | 74+0 (10.63%); 622 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `nl` Nederlands | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `nn` Norsk nynorsk | 110+0 (15.80%); 586 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `no` Norsk | 115+0 (16.52%); 581 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `oc` Occitan | 88+0 (12.64%); 608 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `pa-IN` ਪੰਜਾਬੀ (ਭਾਰਤ) | 107+0 (15.37%); 589 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `pl` Polski | 166+0 (23.85%); 530 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ps` پښتو | 45+0 (6.47%); 651 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `pt-BR` Português (Brasil) | 695+1 (100.00%); 0 | Pending P07; bounded A01/F01 checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07; review M02/M03 |
| `pt-PT` Português (Portugal) | 695+1 (100.00%); 0 | Pending P07; 3 structural items closed only; M03 pending | Routing | #52 M02; #55 M04 | Recheck P07; review M02/M03 |
| `qaa-Zsye-XV` 😀 Emoji (vertical test; English hints) **[test mode]** | 695+1 (100.00%); 0 | Test mode; no natural-language acceptance | Routing; host M02/M03; installed vertical | #52/#55 conventions | Check vertical regressions; preserve explicit test labels |
| `ro` Română | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ru` Русский | 695+1 (100.00%); 0 | Pending P05; crop counts 0–20 checked; M03 pending | Routing | #52 M02; #55 M04 | Recheck P05; review M02/M03 |
| `rw` Ikinyarwanda | 14+0 (2.01%); 682 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `ryu` うちなーぐち | 695+1 (100.00%); 0 | Pending P09; M03 pending | Routing | #52 M02; #55 M04 | Recheck P09; review M02/M03; F01-C030 |
| `sd` سنڌي | 60+0 (8.62%); 636 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `se` Davvisámegiella | 28+0 (4.02%); 668 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `shn` တႆး | 9+0 (1.29%); 687 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `si` සිංහල | 52+0 (7.47%); 644 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sk` Slovenčina | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sl` Slovenščina | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sq` Shqip | 65+0 (9.34%); 631 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sr-Cyrl` Српски (Ћирилица) | 170+0 (24.43%); 526 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sr-Latn` Srpski (Latinica) | 168+0 (24.14%); 528 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `su` Sunda **[added in #57]** | 0+0 (0.00%); 696 | Translation/review not started | PR57 API30/35 identity/fallback; full UI pending | — | Low priority: translate 695 strings + 1 plural, then review in UI |
| `sv` Svenska | 127+0 (18.25%); 569 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `sw` Kiswahili | 695+1 (100.00%); 0 | Pending P04; M03 pending | Routing | #52 M02; #55 M04 | Recheck P04; review M02/M03 |
| `ta` தமிழ் | 96+0 (13.79%); 600 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `tdd` ᥖᥭᥰ ᥖᥬᥲ ᥑᥨᥒᥰ | 7+0 (1.01%); 689 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `te` తెలుగు | 97+0 (13.94%); 599 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `th` ไทย | 164+0 (23.56%); 532 | Broader review not established; cursor context checked | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `tl` Tagalog | 695+1 (100.00%); 0 | Pending P03; M03 pending | Routing | #52 M02; #55 M04 | Recheck P03; review M02/M03 |
| `tok` toki pona | 9+0 (1.29%); 687 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
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
| `wuu-Hans` 吴语（上海话书面语，简体） | 695+1 (100.00%); 0 | Pending P06; M03 pending | Routing | #52 M02; #55 M04 | Recheck P06; review M02/M03; F01-C032 |
| `xh` IsiXhosa | 32+0 (4.60%); 664 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `yi` ייִדיש | 7+0 (1.01%); 689 | Broader review not established | Routing | #52/#55 shared only | Low priority: fill missing strings + plural; review in UI |
| `yo` Yorùbá **[added in #57]** | 0+0 (0.00%); 696 | Translation/review not started | PR57 API30/35 identity/fallback; full UI pending | — | Low priority: translate 695 strings + 1 plural, then review in UI |
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
