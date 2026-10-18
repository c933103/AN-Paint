# Cantonese and Literary Chinese crop-warning correction

## Exact scope and source

- Baseline: develop `8700ca4d921875bdc9f3cf824290cfb83cda2037`, freshly checked on 18 October 2026.
- Implementation: `c46d303495fb65cba4c993930c0bdfe930dcacf3`; reviewed tree `8f5e51ffbbdee2f80c9e916aa6a1c6d969239b84`.
- Exactly three production changes: the complete `other` value of `plurals/ui_crop_preview_images` in `values-b+yue+Hant`, `values-b+yue+Latn`, and `values-b+lzh+Hant`.
- Every other XML entry is preserved. No production code, long Help text, workflow, deadline, existing assertion or historical evidence is removed or relaxed. The original full values and precise replacements are retained in `source.patch`.
- The other five audited counterparts remain unaccepted and unchanged: Sixian Hakka Han/Pha̍k-fa-sṳ, Taiwanese Han/Pe̍h-ōe-jī and Shanghainese-based written Wu. Their linguistic evidence remains insufficient. This work does not accept the long Simplified Chinese Help or any whole catalogue.

## Reviewed full replacement values

`yue-Hant`:

```text
預覽：%1$d × %2$d px\n套用去 %3$d 張圖片。裁剪已經擺好嘅圖片時，連住佢哋嘅圖片可能會移動。
```

`yue-Latn`:

```text
Jyu6 laam5: %1$d × %2$d px\nTou3 jung6 heoi3 %3$d zoeng1 tou4 pin2. Coi4 zin2 ji5 ging1 baai2 hou2 ge3 tou4 pin2 si4, lin4 zyu6 keoi5 dei6 ge3 tou4 pin2 ho2 nang4 wui5 ji4 dung6.
```

`lzh-Hant`:

```text
預覽：%1$d × %2$d px\n施於 %3$d 圖。裁已置之圖，所連諸圖或因之而移。
```

All three retain the width/height/count positional integer arguments, one escaped newline and the `px` unit. The Latin value has no Han characters. Its spacing and sentence capitalization are part of the reviewed complete value.

## Independent linguistic/source review

The full replacement values received an independent review completed at 14:03 UTC on 18 October 2026, before implementation. Cantonese confidence is high; technical Literary Chinese confidence is medium-high. This is source/linguistic review, not native-speaker certification, whole-catalogue acceptance or a rendered-device test.

Cantonese `已經擺好` describes already placed images, `連住佢哋` makes the attached-image relation to those parents explicit, and `可能會` expresses possible movement. The Latin counterpart is Jyutping of that Cantonese wording. The component/construction evidence is:

- words.hk: [擺](https://words.hk/zidin/%E6%93%BA), [已經](https://words.hk/zidin/%E5%B7%B2%E7%B6%93), [連](https://words.hk/zidin/%E9%80%A3), [住](https://words.hk/zidin/%E4%BD%8F), [佢哋](https://words.hk/zidin/%E4%BD%A2%E5%93%8B), [可能](https://words.hk/zidin/%E5%8F%AF%E8%83%BD), [移動](https://words.hk/zidin/%E7%A7%BB%E5%8B%95).
- [Linguistic Society of Hong Kong Jyutping scheme](https://lshk.org/jyutping-scheme/).
- [CantoDict 片](https://www.cantonese.sheik.co.uk/dictionary/characters/876/): the base `pin3` and changed `pin2` reading support the selected `tou4 pin2` throughout this value.

Literary Chinese retains `已置` (already placed) and `所連諸圖` (attached images). `或因之而移` expresses that those attached images may move as a consequence, without implying that the parent itself has to move. See the [possibility sense of 或](https://ctext.org/dictionary.pl?char=%E6%88%96&if=gb) and [CUHK 因 causal usage](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=%E5%9B%A0).

These lexical references support the components and constructions. None is an independent certification of the complete application sentence. The held Taiwanese POJ prefix also needs separate review against [PTS thò-iōng](https://taigiwords.taigitv.org.tw/zh_tw/dic/-7306347); it is not changed here.

## Behavioral basis and regression design

[`ImageCropDialog.kt`](https://github.com/c933103/AN-Paint/blob/c46d303495fb65cba4c993930c0bdfe930dcacf3/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt) formats the preview dimensions and selected count. Selection is independent of placement. Preview changes do not apply a crop.

[`ImageAssembly.kt`](https://github.com/c933103/AN-Paint/blob/c46d303495fb65cba4c993930c0bdfe930dcacf3/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt) retains attachment metadata when crop geometry changes and recomputes attached-child positions from the parent. Movement depends on the affected dimension. The existing [`AssemblyModelTest` control](https://github.com/c933103/AN-Paint/blob/c46d303495fb65cba4c993930c0bdfe930dcacf3/Paintroid/src/test/java/org/catrobat/paintroid/local/AssemblyModelTest.kt#L254-L272) checks relevant versus orthogonal crops, relationship retention, original bytes and Undo/Redo. It is unchanged.

The extended Python regression checks every complete value, sole `other` form, argument types, newline and Android escaping. Its negative cases reject the exact old complete messages, categorical movement, truncation, malformed placeholders and missing/extra forms. The existing TW/CN coverage remains.

The extended Robolectric consumer regression checks compiled resource resolution for counts 0, 1, 2, 3, 20, 21 and 101. Each new locale exercises the real assembly batch-crop toolbar with two placed linked images and an unplaced third image. It checks complete display/accessibility text, unplaced-only initial selection, All/None/one selection, trim/reset, Cancel and reopen. Model/layout/project/source bytes must remain unchanged. Literary Chinese must use the real vertical-dialog shell. These tests are not installed-device, pixel-clipping, native touch, enlarged-font or full-layout acceptance.

## Local verification

- Focused full-value Python tests: 4 passed.
- Canonical catalogue structure/format validation: passed.
- Full Python host suite: 976 passed in 180.372 seconds.
- Optimized Python host suite: 976 passed in 192.309 seconds; full output is retained in `python-optimized.log`.
- Complete-catalogue mode: failed on the existing missing entries, retained in `catalogue-completeness.log`; semantic edits add no missing keys and do not restore withdrawn completeness claims.
- Exact production scope, Kotlin/XML template equality, whitespace and tree-content/mode checks: passed. All 1,224 source blobs were reconciled with the remote baseline, and the proposed remote tree matches the reviewed local tree exactly.
- Attempted `./gradlew --offline :Paintroid:testDebugUnitTest --tests org.catrobat.paintroid.local.ChineseCropPreviewTest --tests org.catrobat.paintroid.local.AssemblyModelTest`: stopped before Gradle execution while downloading the missing wrapper distribution (`Network is unreachable`). No local JVM, Android lint, compile, emulator or installed test pass is claimed. Hosted exact-source CI must provide those results.

Host logs include intentionally invalid synthetic scenarios printed by negative tests. The final unittest summary identifies whether the host suite itself passed. New hosted CI and Codex review remain separate gates; this evidence does not establish them or authorize a release.
