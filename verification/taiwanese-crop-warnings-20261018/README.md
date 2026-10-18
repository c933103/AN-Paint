# Taiwanese crop-warning evidence — 18 October 2026

Source: [PR139](https://github.com/c933103/AN-Paint/pull/139), head `c46fc4495e7afc1e460e1f52cab5607b9422fc25`, tree `9f9e58fc77ee0dda24c0dacffed4aa218fe4c2b0`; base develop `248d5d41e4114f9252c858c3ac08f2bb124746dc`.

## Bounded result

Only the Taiwanese Han/POJ `ui_crop_preview_images/other` production values change. The selected count remains the count; the consequence describes cropping placed images and images attached to those images, with possible movement. Hakka/Wu and all long Help entries are unchanged. The POJ apply prefix now uses PTS-supported `Thò-iōng`.

Complete values:

- Han: `預覽：%1$d × %2$d px\n套用佇 %3$d 張圖片。裁囥好的圖片時，接佇𪜶的圖片可能會移動。`
- POJ: `Ī-lám: %1$d × %2$d px\nThò-iōng tī %3$d tiuⁿ tô͘-phìⁿ. Chhâi khǹg-hó ê tô͘-phìⁿ sî, chiap tī in ê tô͘-phìⁿ khó-lêng ē î-tōng.`

The explicit 接佇𪜶/chiap tī in relative clause replaces the preliminary generic 相連/sio-liân candidate from [tracker75 review](https://github.com/c933103/AN-Paint/pull/75#issuecomment-6252423955). Independent full-sentence review has moderate confidence; lexical/readings support is stronger. This is an original technical composition, not native-speaker certification.

Primary lexical sources checked: [囥](https://sutian.moe.edu.tw/zh-hant/su/3017/), [裁](https://sutian.moe.edu.tw/zh-hant/su/8985/), [接](https://sutian.moe.edu.tw/zh-hant/su/7306/), [𪜶](https://sutian.moe.edu.tw/zh-hant/su/13567/), [可能](https://sutian.moe.edu.tw/zh-hant/su/1522/), [移動](https://sutian.moe.edu.tw/zh-hant/su/7706/), [PTS 套用](https://taigiwords.taigitv.org.tw/zh_tw/dic/-7306347). [MOE romanization comparison](https://language.moe.gov.tw/uploads/files/17579930721182.pdf), printed pp4,44–45, supports POJ/Tâi-lô orthographic differences. Dictionary lexical support does not certify the complete sentence.

## Actual local results

- `focused.log`: four full-value/placeholder/escape/mutation/shape contract methods passed.
- `python-full.log`, `python-full.exit`: all 985 host methods passed, exit 0.
- `python-optimized.log`, `python-optimized.exit`: all 985 host methods passed with `python3 -O`, exit 0.
- `gradle-attempt.log`: wrapper distribution download failed with Network is unreachable before compilation. Local JVM/lint/APK/device stages are unrun.
- `scope-and-tree-check.log`: full base/current content and mode comparison, exact two resource entries, and unchanged Hakka/Wu. Remote tree was separately compared across all 1,225 blob paths/content/modes before the branch was moved using a non-force expected-head lease.
- `source.patch`: exact four-file delta, with no removed files.

## Authored runtime coverage, pending hosted execution

Two existing native Robolectric real batch-crop toolbar cases cover placed parent + attached child + unplaced initial selection; selected count, trim/reset, complete string and accessibility text, Cancel/reopen and unchanged assembly/project/original image bytes. Native font/raster guards cover 𪜶 U+2A736, POJ combining dot U+0358, non-tofu ink and no crop of the isolated padded raster; actual status layout checks cover complete UTF-16 text, no ellipsis and sufficient status height after updates. These are not full-dialog pixel clipping or installed Taiwanese screenshot tests.

[Exact-head hosted run39147690887](https://github.com/c933103/AN-Paint/actions/runs/39147690887) is running. [Exact-head Codex request](https://github.com/c933103/AN-Paint/pull/139#issuecomment-6252649973) is pending. Neither code review nor pending CI is claimed as passed. No merge, release, private upgrade signing, physical-device, legacy-platform or whole-language acceptance is claimed here. Source is preserved as this evidence commit's parent; new hosted receipts can be added without replacing this local record.

