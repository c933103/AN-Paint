# Taiwanese crop-warning evidence — current correction

[PR139](https://github.com/c933103/AN-Paint/pull/139), current head `a2503197cdf9d268beb512bbde40e576bbc84922`, tree `958ca32244b43131e181186c836a8bb31b09fe26`, based on develop `248d5d41e4114f9252c858c3ac08f2bb124746dc`.

## Current full pair

- Han: `預覽：%1$d × %2$d px\n套用佇 %3$d 張圖片。裁囥好的圖片時，接佇怹的圖片可能會移動。`
- POJ: `Ī-lám: %1$d × %2$d px\nThò-iōng tī %3$d tiuⁿ tô͘-phìⁿ. Chhâi khǹg-hó ê tô͘-phìⁿ sî, chiap tī in ê tô͘-phìⁿ khó-lêng ē î-tōng.`

Only these two `ui_crop_preview_images/other` production values and existing consumer/full-value tests change. Placement and attached-to-cropped-images antecedent are explicit, with possible rather than guaranteed movement. Hakka/Wu and all long Help entries stay unchanged.

## Orthographic correction and retained failure

The initial head's API33 Robolectric native crop-status font chain had no glyph for preferred 𪜶 U+2A736. Its exact positive guard failed, the sole failure among 1,144 JVM methods. [Original failure and raw packet](failed-head-c46fc44/README.md) are retained; [terminal run disposition](failed-head-c46fc44/TERMINAL.md) separates that failure from the later superseding cancellation.

[MOE entry13567](https://sutian.moe.edu.tw/zh-hant/su/13567/) lists 怹 under 異用字 for 𪜶/in, with third-person-plural sense. Independent review approved this same-pronunciation/sense alternate graph for the bounded full Han value; POJ stays unchanged. The positive hasGlyph/non-tofu raster/layout guards are unchanged except for the chosen graph. This is a reviewed spelling choice, not a repair of preferred 𪜶 coverage. That font limitation is [separately recorded in tracker75](https://github.com/c933103/AN-Paint/pull/75#issuecomment-6252833986); no other platform or installed-device absence is inferred.

The original lexical sources and complete-pair rationale remain in the [initial immutable evidence](https://github.com/c933103/AN-Paint/blob/d379d05f1fd3f62dfe9ad3525149b3669a05e480/verification/taiwanese-crop-warnings-20261018/README.md). Full-sentence confidence is moderate and lexical/readings support stronger; neither version is native-speaker certification or whole-language acceptance.

## Corrected-head local checks

`corrected-local/` retains four passing focused methods, 985 normal and 985 optimized passing host methods (both exit0), and the exact small correction patch. The entire 1,225-blob application tree, including retained contents and modes, was compared before publication; the correction changes three existing files, with no removal and unchanged POJ. Initial logs remain in this directory and initial source/evidence remain in ancestry.

Local Gradle could not download its distribution, so local JVM/lint/APK/device stages remain unrun. Corrected-head [run39149447853](https://github.com/c933103/AN-Paint/actions/runs/39149447853) is now terminal green: six jobs, 1,144 JVM methods, 985 hosted Python methods, nine generation probes and the complete API35 source-discovered union (74 native +45 app). Actual artifacts and complete inventories were independently replayed. Current-head Codex Code review completed without findings. Advisory Security is initial-head only.

See [corrected-head terminal verification](current-head-a2503197/README.md), raw packet and focused receipts for APK/source/signature/compiled-values binding, actual-consumer glyph/layout checks and exact limitations. The passing Han assertion covers alternate 怹, not preferred 𪜶. The broader font limitation remains open. No installed Taiwanese pixel/TalkBack, physical-device, legacy-platform, release or whole-catalogue acceptance is claimed. The parent merged PR139 as `798e6159939fa06beb27755700a1320a5970cb7b` after these gates passed; the natural develop push run also passed independent content verification. See [post-merge terminal evidence](postmerge-798e6159/README.md).
