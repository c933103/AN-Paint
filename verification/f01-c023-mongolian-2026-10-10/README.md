# F01-C023: bounded Cyrillic Mongolian TIFF qualification

10 October 2026. This isolated source/evidence increment is based on frozen PR43 head `4f9082aa687a5c36b559061bcc10d0e39331610f`, tree `04a84df1535297f13a314c521b55647f6d15a678`.

**Disposition: bounded source/test proposal reviewed for separate-branch publication; F01-C023 and P08-009 remain open. No end-to-end acceptance, merge, runtime verification or native-speaker verification is claimed.** The original PR43 source branch and concurrent integration branches are not changed by this increment. No new PR or CI workflow is created.

## Exact change

- Case: **F01-C023**, `mn-Cyrl-MN`, `formats22_tiff_description`.
- Canonical path: `Paintroid/src/main/res/values-b+mn+Cyrl+MN/strings.xml`, line 570.
- [Frozen original source](https://github.com/c933103/AN-Paint/blob/4f9082aa687a5c36b559061bcc10d0e39331610f/Paintroid/src/main/res/values-b%2Bmn%2BCyrl%2BMN/strings.xml#L570), blob `575e8c401ab2e013b7a2afa1d0848024ddb53a8c`.

Original:

> Нэг RGB хуудсыг хадгална. Шахалт нь пикселийг өөрчлөхгүйгээр файлын хэмжээг багасгана; шахалтгүй TIFF хадгалахын тулд унтраана.

Proposal:

> Нэг RGB хуудсыг хадгална. Шахалт нь пикселийг өөрчлөхгүйгээр файлын хэмжээг багасгаж магадгүй; шахалтгүй TIFF хадгалахын тулд унтраана.

The sole resource substitution is **багасгана → багасгаж магадгүй**. All other resource bytes, including the RGB-page clause, pixel-preservation clause, unchecked instruction and compression checkbox, remain unchanged. Traditional Mongolian F01-C024 and every other catalogue are unchanged.

## Primary linguistic support

1. [Mongoltoli, БАГАСГАХ](https://mongoltoli.mn/search.php?opt=1&ug_id=9881&word=%D0%91%D0%90%D0%93%D0%90%D0%A1%D0%93%D0%90%D0%A5), sense 1, gives **“Бага болгох”** and includes reducing its size. Its [institutional description](https://mongoltoli.mn/a001.php) identifies Mongolian Academy of Sciences research institutes among its creators.
2. [TUFS nonpast grammar](https://www.coelang.tufs.ac.jp/mt/mn/gmod/contents/explanation/014.html) describes **“語幹-на”**, including generic actions and general truths. Applying that account to this UI, `багасгана` asserts reduction without an explicit possibility hedge. This contextual interpretation is model linguistic analysis; the suffix itself does not literally mean “always.”
3. [TUFS modality grammar](https://www.coelang.tufs.ac.jp/mt/mn/gmod/courses/c02/lesson17/step2/explanation/082.html) directly pairs **“-ж магадгүй”** with **“可能性・蓋然性”**. It supplies a possibility construction appropriate to a prospective result.
4. [TUFS converb and negative coordination](https://www.coelang.tufs.ac.jp/mt/mn/gmod/contents/explanation/041.html) documents `-ж/-ч` and the unchanged `-хгүйгээр` without-doing construction. Its referenced [spelling rules](https://www.coelang.tufs.ac.jp/mt/mn/gmod/contents/explanation/012.html) do not select `-ч` for vowel-final `багасга-`.

Morphological analysis: dictionary `багасгах` → stem `багасга-`; original `багасга- + -на`; proposal `багасга- + -ж + магадгүй` → `багасгаж магадгүй`. The stem-final `а` is retained. The application of the published grammar to this exact verb and UI sentence is model analysis, not app-specific native attestation.

Working gloss of the changed clause: “Compression may reduce the file size without changing the pixels.”

The [pinned encoder](https://github.com/c933103/AN-Paint/blob/4f9082aa687a5c36b559061bcc10d0e39331610f/Paintroid/src/main/cpp/tiff_bridge.cpp#L480-L518) chooses Deflate or no compression directly and writes scanlines; it does not compare complete outputs and retain the smaller. [RFC1951 §1.1](https://www.rfc-editor.org/rfc/rfc1951.html#section-1.1) permits expansion. No complete-TIFF expansion percentage or measured regression is claimed.

## Narrow test composition

The original `tools/fixtures/tiff_size_wording_scope.json` remains byte-identical with its 37 entries and SHA256 `9cead98f8f826c5c853f4b0dc6cd6b80f8760274770a00f600c690d44fba0ac1`. Its existing tests and pin are unchanged.

A separate one-entry `tools/fixtures/tiff_c023_wording_scope.json` is pinned at SHA256 `d2dcbbeaef13c80ae9dfe4d1ec9595c8ba82cbe92d057479f5b25e4deba3d6c4`. The Copy-credit scope helper reverses only that exact C023 line after its existing normalization; every historical whole-file hash remains unchanged. Reversion, corruption, deletion, duplication and expanded scope still fail.

Nine focused host tests assert the independent wording oracle, complete-file reversal to the frozen original, single-case fixture, unchanged original 37 entries, historical Copy-credit hash, eight embedded negative controls and Traditional Mongolian byte identity. The negative controls are four invalid resource replacements, one unrelated-content mutation and three malformed extension fixtures.

Two methods added to the existing `TiffDescriptionDialogTest` exercise C023's actual language selection, both initial compression choices, toggles and confirmed flags, DIB/TIFF switching, and both Cancel routes. Expected text is a fixed independent literal, never read back as its own oracle. These Kotlin methods are prepared but **not compiled or executed in this isolated pass**. Final exact integrated Codex review and applicable CI remain pending.

The parent independently inspected the exact five-path source/test diff and the separate fixture composition, independently passed all nine focused host tests, and accepted this narrow proposal for separate-branch publication. This is a bounded independent source/host check; it is not a clean Codex review or execution of the two new Kotlin methods.

Fresh validation: **421 host tests passed with no skips** in 76.227 seconds, including all nine C023 tests. Canonical catalogue structural validation and diff whitespace checks passed. Restoring the old resource caused the focused suite to fail; restoring the candidate returned it to green. Deliberately rejected mocked instrumentation summaries in the all-host log are host negative controls, not executed device failures.

See [structured review](review.json), [source manifest](source-manifest.json), [exact five-path source patch](source.patch), [focused host log](focused-host.log), [all-host log](all-host.log), [structural validation](structural-validation.log) and [red/green control record](negative-controls.json). The test results describe source/host checks only.

## Tracking and acceptance boundary

Related records: [individual F01 inventory](https://github.com/c933103/AN-Paint/blob/3981b84e6dc53f3a6ca772ae9ae1d7738699a5ea/verification/f01-tiff-wording-2026-10-10/combined-evidence/all-language-inventory.json), [canonical recheck register](https://github.com/c933103/AN-Paint/blob/review/localization-integration/verification/localization-recheck-register.md), [AN-W02 project card](https://github.com/c933103/AN-Paint/blob/docs/project-kanban-2026-10-10/docs/PROJECT_KANBAN.md), [PR43](https://github.com/c933103/AN-Paint/pull/43) and [PR7](https://github.com/c933103/AN-Paint/pull/7).

F01-C023 records this bounded patch; full-language **P08-009 stays pending**. This does not close F01, P07-007, AN-W02 or any broader language obligation. The historical 37-qualified/12-probable/4-uncertain inventory remains an immutable snapshot; this separate C023 increment does not silently rewrite it. The canonical register remains **475 total / 3 structural completed / 472 pending**.

No native speaker reviewed the exact sentence. Complete-string naturalness, computing terminology, installed rendering/accessibility and full-language acceptance remain unverified. These are evidence limits, not newly imposed requirements. No conclusion is propagated to another script or language; the Ainu follow-up is not repeated.
