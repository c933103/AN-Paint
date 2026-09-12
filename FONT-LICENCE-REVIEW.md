# Dubai and the former “STC” font: licence review

Review date: 12 September 2026. Scope: bundling the original font binaries in AN Paint’s Android APK and public source, and allowing users to create and export text in images.

**Decision: do not restore either file under the public terms found.** This review found affirmative restrictions on distribution and application use. It does not infer a prohibition simply from missing metadata. Any separate permission granted privately to an upstream distributor would need to be produced and checked for coverage of AN Paint and its downstream recipients.

## Exact upstream files and reproducibility

The relevant source is [Catrobat/Paintroid at `853ce3c346910ea73aa4de5514f2a76ace1396fb`](https://github.com/Catrobat/Paintroid/tree/853ce3c346910ea73aa4de5514f2a76ace1396fb).

| Resource | Original path under `Paintroid/src/main/res/font/` | Bytes | Git blob SHA-1 |
|---|---|---:|---|
| `R.font.dubai` | [`dubai.ttf`](https://github.com/Catrobat/Paintroid/blob/853ce3c346910ea73aa4de5514f2a76ace1396fb/Paintroid/src/main/res/font/dubai.ttf) | 181,484 | `9d9cea18ffa0cdf7b659da4c2460d9e63c42e944` |
| `R.font.stc_regular` | [`stc_regular.otf`](https://github.com/Catrobat/Paintroid/blob/853ce3c346910ea73aa4de5514f2a76ace1396fb/Paintroid/src/main/res/font/stc_regular.otf) | 21,448 | `efb515fd324deec591e750d5d8273d32d8bf6b9f` |

The [2018 resource move](https://github.com/Catrobat/Paintroid/commit/4542bf77e7032aaf2ecc5a34318ffe26ec8da4cc) renamed `assets/Dubai.TTF` and `assets/STC.otf` without changing these blobs. The filename “STC” alone is insufficient to identify the font’s designer or licence.

`tools/inspect_legacy_fonts.py` downloads these pinned bytes into memory, validates their Git blob hashes and sizes, and emits SHA-256 hashes, family/version/designer/copyright/licence name records and `OS/2.fsType` to `build/reports/legacy-font-metadata.json`. It writes no font binaries and adds none to the app or source archive. The technical embedding bits do not replace the applicable licence.

Exact internal metadata verification is pending the CI execution of that script; the findings below separate the documented historical identity from current website evidence.

## Dubai

[Monotype’s own account](https://www.monotype.com/resources/case-studies/dubai) identifies The Executive Council of Dubai’s project, the Microsoft/Monotype collaboration and Nadine Chahine’s design leadership. It describes free public distribution. That establishes provenance and availability, rather than unlimited redistribution or use rights.

The Executive Council’s **End User Licence Agreement – Dubai Font**, [preserved by Font Squirrel](https://www.fontsquirrel.com/license/dubai), contains the following relevant terms:

- Clause 2.2(c) permits some Android application embedding, subject to protections against extracting or installing the font outside the app. It expressly excludes applications that generate output including photos, static/scalable images and other documents or data files. AN Paint does exactly that.
- Clauses 3.1(d), 3.1(f) and 3.1(i) restrict redistribution, modification and making font code available without additional permission. A public repository containing the font and an extractable APK asset would not meet those conditions.
- Clause 3.1(j) also restricts making the font subject to a public-software agreement. This is not an OFL or other open-font licence.

The cited EULA is a third-party preservation of the rights holder’s text. The official `dubaifont.com` site could not be retrieved during this review, so a current replacement licence there has not been verified. The specific image-generating-app exclusion in the available EULA is sufficient to withhold restoration; a broad “free for commercial use” download label does not override it.

## The file called STC

The earlier AN Paint change record identified this file as **STC/GE SS carrying Boutros copyright**. That binary identity must be checked against the pinned name records above rather than assumed from its Android resource name.

[Boutros’s official GE SS TWO page](https://www.boutrosfonts.com/Boutros-GE-SS-TWO.html) links its [licence notification](https://www.boutrosfonts.com/spip.php?id_article=31&page=license). The notification limits the ordinary grant to workstation publishing and explicitly excludes copying or distribution without an additional agreement. [Boutros’s official free-fonts explanation](https://www.boutrosfonts.com/spip.php?page=free) further says that, except for promotions on its own site, it does not authorize other sites to offer its fonts as free downloads.

Those terms do not authorize bundling a GE SS/Boutros font into a publicly distributed Android editor or its source. Purchasing a desktop font alone would not establish the additional rights required here. No app/source redistribution grant applicable to AN Paint was found.

A separate similarly named font exists: [Arabic Typography’s STC Telecom](https://www.arabictypography.com/custom-type/stc-telecom-font). Its designer describes a client-exclusive commission unavailable for general licensing or purchase. That statement must **not** be used as the licence for the upstream file if its metadata instead identifies Boutros/GE SS. It is recorded here to prevent a filename-based misidentification.

## Why the old test used system sans-serif

The earlier implementation removed both bundled resources and used Android’s system sans-serif for their legacy selector entries. The test was changed to compare those fallback typefaces. Retaining the names `dubaiFontFace` and `stcFontFace` was misleading: it no longer tested either named font.

The original selector and `TextToolFontListTest.kt` have since been removed with the original editor. AN Paint’s present font tests load its actual bundled OFL files and system-font choices; it must not label system sans-serif as Dubai or STC.

## Conditions for revisiting restoration

1. Finish and retain the pinned-binary metadata inspection, correcting any family or version mismatch in this review.
2. For Dubai, obtain an authoritative replacement licence or specific permission covering image-generating Android applications, public source redistribution and downstream copies.
3. For the exact Boutros/GE SS file, obtain an applicable app-embedding and redistribution agreement from the authorized rights holder; establish the permission chain for any renamed or modified binary.
4. If such terms are obtained, review them before changing the font catalogue and include the actual required notices and terms. Until then, retain the current accurately named, licensed font choices.

No rights holder has been contacted and no licence has been purchased as part of this review.
