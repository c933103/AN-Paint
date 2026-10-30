## Draft result — 30 October 2026

**21 candidate additions: Hindi (hi), Tamil (ta), Thai (th), each 5 P0 + 2 P1.** These are all exact missing P0/P1 strings for these three catalogues at develop `e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5`, not a deliberately reduced subset. Candidate-only record: not implemented, independently reviewed, merged, released or counted as production coverage. No source/test changes or CI dispatch.

## Source and scope evidence

Pinned source: [English strings](https://github.com/c933103/AN-Paint/blob/e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5/Paintroid/src/main/res/values/strings.xml); [priority manifest](https://github.com/c933103/AN-Paint/blob/e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5/translations/string-importance.json) (92 P0 and 249 P1).

- [hi catalogue](https://github.com/c933103/AN-Paint/blob/e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5/Paintroid/src/main/res/values-hi/strings.xml), blob `c88bc8df71b22907a5a832dd53baeb2e86afe896`: all seven keys below absent; exact presence before this draft is 87/92 P0 and 247/249 P1. Existing generic Main caption remains unchanged: `"मुख्य"`.
- [ta catalogue](https://github.com/c933103/AN-Paint/blob/e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5/Paintroid/src/main/res/values-ta/strings.xml), blob `32b005dee0b6751de47864f507c74d7199092a29`: all seven keys below absent; exact presence before this draft is 87/92 P0 and 247/249 P1. Existing generic Main caption remains unchanged: `முதன்மை`.
- [th catalogue](https://github.com/c933103/AN-Paint/blob/e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5/Paintroid/src/main/res/values-th/strings.xml), blob `be19850723a4d4f80f1d94a980f67341e138141f`: all seven keys below absent; exact presence before this draft is 87/92 P0 and 247/249 P1. Existing generic Main caption remains unchanged: `หลัก`.

Indonesian, Malay and Vietnamese were also checked and had no exact P0/P1 gaps at this source, so were not selected. No excluded/pending locale payload is duplicated.

| Tier | Key | Complete English source |
|---|---|---|
| P0 | `formats22_derived_exported` | %1$s exported. Your full drawing still has unsaved changes; save a full image copy before replacing it. |
| P0 | `ui_save_as` | Save as %1$s |
| P0 | `ui_save_as_jpeg` | Save as JPEG… |
| P0 | `ui_save_as_jpeg_xl` | Save as JPEG XL… |
| P0 | `ui_save_as_png` | Save as PNG… |
| P1 | `ui_foreground_background_colour_palette` | Foreground %1$s, background %2$s. %3$s colour palette. |
| P1 | `ui_pinch_and_pan_mode` | Pinch and pan mode |

## Context / semantic constraints

- Derived export is not saving the full drawing: all three candidates retain successful export, still-unsaved changes in the full drawing, and the instruction to save a full-image copy before replacing it.
- Format labels retain JPEG / JPEG XL / PNG, ellipses, and the generic format placeholder. They do not change “Save as” into export or share.
- Palette accessibility text keeps foreground %1$s, background %2$s, palette %3$s in that order; no unsupported identity is assigned to %3$s.
- Pinch/pan wording describes view zoom and navigation, not image resampling. Tamil is intentionally explanatory rather than a literal borrowing; its longer label needs UI-fit review.
- Main remains generic (मुख्य / முதன்மை / หลัก). This is not new coverage or a claim that Main refers to a palette.
- Related source inspected: [ClassicPaintActivity](https://github.com/c933103/AN-Paint/blob/e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L769-L772) provides zoom/navigation controls; [PaintCanvas](https://github.com/c933103/AN-Paint/blob/e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L652-L663) uses two-touch scale/span and focus movement; [SaveOptionsDialog](https://github.com/c933103/AN-Paint/blob/e6b207b7373b33dd832e6b32cd9a8139b6fa6fc5/Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt#L42) precedes Android's destination picker. ColourStatusButton was also read. These four files did not contain direct references to these seven exact resource IDs; this is not a repository-wide reachability assertion or a translation prerequisite. The English catalogue and existing locale save/foreground/background/navigation terms supply bounded wording context.

## Complete candidates

### hi — 5 P0 + 2 P1

Intended resource: `Paintroid/src/main/res/values-hi/strings.xml`

```xml
<string name="formats22_derived_exported">%1$s निर्यात किया गया। आपके पूरे चित्र में अब भी ऐसे बदलाव हैं जो सहेजे नहीं गए हैं; उसे बदलने से पहले पूरे चित्र की एक प्रति सहेजें।</string>
<string name="ui_save_as">%1$s के रूप में सहेजें</string>
<string name="ui_save_as_jpeg">JPEG के रूप में सहेजें…</string>
<string name="ui_save_as_jpeg_xl">JPEG XL के रूप में सहेजें…</string>
<string name="ui_save_as_png">PNG के रूप में सहेजें…</string>
<string name="ui_foreground_background_colour_palette">अग्रभूमि %1$s, पृष्ठभूमि %2$s। %3$s रंग पट्टिका।</string>
<string name="ui_pinch_and_pan_mode">दो उँगलियों से ज़ूम करने और दृश्य खिसकाने का मोड</string>
```

### ta — 5 P0 + 2 P1

Intended resource: `Paintroid/src/main/res/values-ta/strings.xml`

```xml
<string name="formats22_derived_exported">%1$s ஏற்றுமதி செய்யப்பட்டது. உங்கள் முழு ஓவியத்தில் இன்னும் சேமிக்கப்படாத மாற்றங்கள் உள்ளன; அதை மாற்றுவதற்கு முன் முழுப் படத்தின் ஒரு நகலைச் சேமிக்கவும்.</string>
<string name="ui_save_as">%1$s ஆகச் சேமி</string>
<string name="ui_save_as_jpeg">JPEG ஆகச் சேமி…</string>
<string name="ui_save_as_jpeg_xl">JPEG XL ஆகச் சேமி…</string>
<string name="ui_save_as_png">PNG ஆகச் சேமி…</string>
<string name="ui_foreground_background_colour_palette">முன்புலம் %1$s, பின்புலம் %2$s. %3$s நிறத்தட்டு.</string>
<string name="ui_pinch_and_pan_mode">இரு விரல்களை நெருக்கி அல்லது விரித்துக் காட்சியைப் பெரிதாக்கவும் சிறிதாக்கவும் நகர்த்தவும் உதவும் பயன்முறை</string>
```

### th — 5 P0 + 2 P1

Intended resource: `Paintroid/src/main/res/values-th/strings.xml`

```xml
<string name="formats22_derived_exported">ส่งออก %1$s แล้ว ภาพวาดฉบับเต็มของคุณยังมีการเปลี่ยนแปลงที่ยังไม่ได้บันทึก โปรดบันทึกสำเนาภาพฉบับเต็มก่อนแทนที่ภาพนั้น</string>
<string name="ui_save_as">บันทึกเป็น %1$s</string>
<string name="ui_save_as_jpeg">บันทึกเป็น JPEG…</string>
<string name="ui_save_as_jpeg_xl">บันทึกเป็น JPEG XL…</string>
<string name="ui_save_as_png">บันทึกเป็น PNG…</string>
<string name="ui_foreground_background_colour_palette">สีพื้นหน้า %1$s สีพื้นหลัง %2$s จานสี %3$s</string>
<string name="ui_pinch_and_pan_mode">โหมดจีบนิ้วเพื่อซูมและเลื่อนภาพ</string>
```

## Verification and limits

- Compared every key in the full P0/P1 manifest with exact locale string names; each locale has exactly the seven missing keys listed. This measures presence, not correctness of all existing translations, alias resolution or whole-language acceptance.
- All 21 candidate placeholder sequences were compared with their English sources and match exactly. There is no source markup to preserve in these seven strings; candidate text contains no XML metacharacters requiring escaping or ASCII apostrophes requiring Android escaping. Literal format names and ellipses are retained.
- Model-authored with reasonable working competence for these bounded ordinary Hindi, Tamil and Thai UI sentences. Not a native-human translation certification or independent linguistic review. Review should check naturalness, especially the explanatory gesture-mode labels, warning pronoun referents, and actual accessibility/UI fit.
- No XML/resource compilation, installed-device rendering, TalkBack, test suite or CI run was performed. Those technical checks cannot be inferred from placeholder comparison.
- Next: independent linguistic review of all 21 complete messages, then separately authorized integration using the existing checks. Re-read current develop before applying; do not overwrite later translations.
