# Dubai and the former “STC” font: licence review

Review date: 12 September 2026. Scope: bundling the original font binaries in AN Paint’s Android APK and public source, and allowing users to create and export text in images.

**Decision: do not restore either file under the public terms found.** This review found affirmative restrictions on distribution and application use. It does not infer a prohibition simply from missing metadata. **This is a decision about the permission established for AN Paint, not a finding that Catrobat distributed the fonts unlawfully.** Any separate permission granted to an upstream distributor would need to be produced and checked for coverage of AN Paint and its downstream recipients.

## Why Pocket Paint included them

The upstream history gives a concrete implementation reason: additional fonts were added for Arabic/right-to-left text. It does not establish the licence under which upstream obtained the files.

| Event | Evidence | What it establishes |
|---|---|---|
| Dubai added on 3 August 2017; merged on 10 August 2017 | [Commit `edbfd8e`](https://github.com/Catrobat/Paintroid/commit/edbfd8ef8766e4d72e9be26ebc9d18b6391a01de), [PR #367](https://github.com/Catrobat/Paintroid/pull/367) | The Arabic/RTL font change added Dubai and Alarabiya to the text tool, including Arabic text tests. The Dubai blob is exactly `9d9cea18ffa0cdf7b659da4c2460d9e63c42e944`, matching the file inspected below. |
| “STC” replaced Alarabiya on 15 January 2018 | [Commit `8bfe771`](https://github.com/Catrobat/Paintroid/commit/8bfe77178dc5d3a97117c281cbfea9380da1c0c3), [PR #471](https://github.com/Catrobat/Paintroid/pull/471) | The change removed Alarabiya and added `STC.otf`, updating the selector and tests. The added blob is exactly `efb515fd324deec591e750d5d8273d32d8bf6b9f`, the Boutros GE SS file inspected below. The PR gives no further reason for the substitution. |
| Both files moved into font resources in August 2018 | [Commit `4542bf7`](https://github.com/Catrobat/Paintroid/commit/4542bf77e7032aaf2ecc5a34318ffe26ec8da4cc) | Git records unchanged-blob renames from `assets/Dubai.TTF` and `assets/STC.otf` to `res/font/dubai.ttf` and `res/font/stc_regular.otf`. This was a resource refactor, not a change to the font binaries or a newly documented licence. |

We checked the introducing commits, both PR descriptions, changed-file lists, public issue comments, inline comments and reviews. PR #367's discussion concerns code and tests; PR #471 has an empty description and a request to run tests. Neither PR adds a font licence file or records a redistribution grant. Searches of the repository's GitHub issues and PRs for the two font names and font licensing did not locate such a grant. The historical Jira tickets `PAINT-172` and `PAINT-271` could not be retrieved, so their contents have not been checked. This is a bounded public-record review; it cannot establish that no separate agreement exists.

Therefore, the answer is: **Pocket Paint included these exact fonts as part of its Arabic text support. We have not established what permission upstream relied on.** Inclusion and a successful merge demonstrate that the assets were shipped in source; they do not, by themselves, supply the missing permission for a downstream APK and repository. Conversely, restrictions found in public terms do not prove that upstream lacked a different applicable grant. Any earlier shorthand saying that upstream “was not allowed” to include them would go beyond the evidence.

## Exact upstream files and reproducibility

The relevant source is [Catrobat/Paintroid at `853ce3c346910ea73aa4de5514f2a76ace1396fb`](https://github.com/Catrobat/Paintroid/tree/853ce3c346910ea73aa4de5514f2a76ace1396fb).

| Resource | Original path under `Paintroid/src/main/res/font/` | Bytes | Git blob SHA-1 |
|---|---|---:|---|
| `R.font.dubai` | [`dubai.ttf`](https://github.com/Catrobat/Paintroid/blob/853ce3c346910ea73aa4de5514f2a76ace1396fb/Paintroid/src/main/res/font/dubai.ttf) | 181,484 | `9d9cea18ffa0cdf7b659da4c2460d9e63c42e944` |
| `R.font.stc_regular` | [`stc_regular.otf`](https://github.com/Catrobat/Paintroid/blob/853ce3c346910ea73aa4de5514f2a76ace1396fb/Paintroid/src/main/res/font/stc_regular.otf) | 21,448 | `efb515fd324deec591e750d5d8273d32d8bf6b9f` |

The [2018 resource move](https://github.com/Catrobat/Paintroid/commit/4542bf77e7032aaf2ecc5a34318ffe26ec8da4cc) renamed `assets/Dubai.TTF` and `assets/STC.otf` without changing these blobs. The filename “STC” alone is insufficient to identify the font’s designer or licence.

`tools/inspect_legacy_fonts.py` downloads these pinned bytes into memory, validates their Git blob hashes and sizes, and emits SHA-256 hashes, family/version/designer/copyright/licence name records and `OS/2.fsType` to `build/reports/legacy-font-metadata.json`. It writes no font binaries and adds none to the app or source archive. The technical embedding bits do not replace the applicable licence.

The script completed in CI and both files matched the pinned blobs and sizes.
The full result is retained as [verification/legacy-font-metadata.json](verification/legacy-font-metadata.json).

| File | Verified internal identity | Version | `fsType` | SHA-256 |
|---|---|---|---:|---|
| `dubai.ttf` | Dubai Regular; Monotype Imaging Inc.; copyright Dubai Executive Council, 2016 | 1.10 | 8 | `7a0be62452c4a73b8f86f3b6c1b0915074c47fa40bb658255b3d0b1cdf6d2f2f` |
| `stc_regular.otf` | GE SS Text Light; typographic family GE SS, Light; Boutros International, 2004 | 1.200; PS 001.002; hotconv 1.0.38 | 0 | `d03c34017360a88a55237dd3582b2f6d7085e8c519f4e1b8dde84d82d7582273` |

The [OpenType specification](https://learn.microsoft.com/en-us/typography/opentype/spec/os2#fstype) describes value 8 as editable document embedding and value 0 as installable embedding. For value 0, the recipient remains subject to the original purchaser’s licence and obligations. These flags must therefore be considered alongside the distribution terms; neither says that a font is openly licensed for unrestricted APK/source distribution.

## Dubai

The exact original binary supplies direct evidence: name record 13 identifies it as a Microsoft-supplied font, ties content creation to the supplying product’s licence, permits the specified content embedding and temporary output-device use, and excludes other uses. Its value 8 embedding flag concerns editable documents. This is an explicit limited-use notice, not an empty licence field. [Verified metadata](verification/legacy-font-metadata.json).

[Monotype’s own account](https://www.monotype.com/resources/case-studies/dubai) identifies The Executive Council of Dubai’s project, the Microsoft/Monotype collaboration and Nadine Chahine’s design leadership. It describes free public distribution. That establishes provenance and availability, rather than unlimited redistribution or use rights.

We also checked a possible separately distributed version: The Executive Council’s **End User Licence Agreement – Dubai Font**, [preserved by Font Squirrel](https://www.fontsquirrel.com/license/dubai), contains the following relevant terms:

- Clause 2.2(c) permits some Android application embedding, subject to protections against extracting or installing the font outside the app. It expressly excludes applications that generate output including photos, static/scalable images and other documents or data files. AN Paint does exactly that.
- Clauses 3.1(d), 3.1(f) and 3.1(i) restrict redistribution, modification and making font code available without additional permission. A public repository containing the font and an extractable APK asset would not meet those conditions.
- Clause 3.1(j) also restricts making the font subject to a public-software agreement. This is not an OFL or other open-font licence.

The cited EULA is a third-party preservation of the rights holder’s text, not the licence record extracted from the upstream 1.10 file. The official `dubaifont.com` site could not be retrieved, so a current replacement licence there has not been verified. Both the original file’s limited-use notice and this alternative EULA fail to authorize the proposed inclusion. A broad download label does not override either restriction.

## The file called STC

The binary inspection confirms that `stc_regular.otf` is **GE SS Text Light by Boutros International**, version 1.200. The Windows family/full-name record says GE SS Text Light; the typographic family is GE SS, style Light. Its designer, manufacturer, copyright and trademark records all identify Boutros. The upstream STC filename and label do not match that internal family identity; the reviewed records do not explain the relationship between those names. [Verified metadata](verification/legacy-font-metadata.json).

[Boutros’s official GE SS TWO page](https://www.boutrosfonts.com/Boutros-GE-SS-TWO.html) links its [licence notification](https://www.boutrosfonts.com/spip.php?id_article=31&page=license). The notification limits the ordinary grant to workstation publishing and explicitly excludes copying or distribution without an additional agreement. [Boutros’s official free-fonts explanation](https://www.boutrosfonts.com/spip.php?page=free) further says that, except for promotions on its own site, it does not authorize other sites to offer its fonts as free downloads.

The linked notification is the foundry’s current general distribution statement, not a recovered purchase agreement for the 2004 file. The binary’s `fsType=0` signals installable embedding, but the specification keeps the original licence obligations in force. Neither that flag nor a desktop purchase establishes the additional APK/source redistribution rights needed here. No agreement applicable to AN Paint was found. The confirmed Boutros identity and official restriction support keeping this font excluded unless the applicable additional rights can be documented.

A separate similarly named font exists: [Arabic Typography’s STC Telecom](https://www.arabictypography.com/custom-type/stc-telecom-font). Its designer describes a client-exclusive commission unavailable for general licensing or purchase. That statement is **not** the licence for the inspected upstream Boutros file. It is recorded here to prevent a filename-based misidentification.

## Why the old test used system sans-serif

The earlier implementation removed both bundled resources and used Android’s system sans-serif for their legacy selector entries. The test was changed to compare those fallback typefaces. Retaining the names `dubaiFontFace` and `stcFontFace` was misleading: it no longer tested either named font.

The original selector and `TextToolFontListTest.kt` have since been removed with the original editor. AN Paint’s present font tests load its actual bundled OFL files and system-font choices; it must not label system sans-serif as Dubai or STC.

## Conditions for revisiting restoration

1. For Dubai, obtain an authoritative replacement licence or specific permission covering image-generating Android applications, public source redistribution and downstream copies.
2. For the exact Boutros/GE SS file, obtain an applicable app-embedding and redistribution agreement from the authorized rights holder; establish the permission chain for any renamed or modified binary.
3. If such terms are obtained, review them before changing the font catalogue and include the actual required notices and terms. Until then, retain the current accurately named, licensed font choices.

No rights holder has been contacted and no licence has been purchased as part of this review.
