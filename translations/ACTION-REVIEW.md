# Editor vocabulary review — 0.0.23

Paintroid's copied vocabulary was not uniformly suitable for this editor. Examples
included Traditional Chinese Cut = 切, Apply = 申請, Outline = 大綱, and identical
Cancel/Discard labels; Danish Cancel was Slet (Delete). Czech, Ukrainian, Albanian
and Kabyle also reused the same Cancel/Discard label. The review is about command
meaning in context, not merely whether a string is translated.

`android-actions.json` records the exact selected clipboard, Cancel, OK and Select
all strings from Android Open Source Project tag `android-15.0.0_r1`, with source
URLs and blob hashes. These strings are licensed under Apache-2.0; the complete
licence is in `ANDROID-APACHE-2.0.txt`. They supplement the original Paintroid
vocabulary, whose pinned source files and AGPL attribution remain intact.

`reviewed-actions.json` corrects editor-specific meanings and supplies explicit
Discard changes wording and principal navigation labels in the recorded locales.
Unreviewed absent strings retain English fallback. Kabyle's colliding Discard
label deliberately falls back to English until an appropriate translation is
available; this is not presented as a completed Kabyle translation.

The unsaved-change prompt has three distinct outcomes: Save, Discard changes,
and Keep editing. Where a longer Keep editing translation is unavailable, the
locale's ordinary Cancel label is used. The generator checks destructive and
non-destructive labels for collisions. Clipboard commands and the unrelated Apply,
Outline and image Quality terms receive separate context corrections.

The new `lzh-Hant` and `mn-Mong` catalogues are initial translation foundations,
with English fallback for missing text. They do not claim a completed native-speaker
review. Their ribbon labels use the shared vertical text renderer. Literary Chinese
uses columns from right to left; traditional Mongolian uses columns from left to
right and preserves word shaping. Native Android dialogs and editable fields keep
the platform layout; the inserted-text preview and output use the selected writing
mode. The unmodified Noto Sans Mongolian font and its original OFL are included.

References:
- https://github.com/aosp-mirror/platform_frameworks_base/tree/android-15.0.0_r1/core/res/res
- https://www.w3.org/International/articles/vertical-text/
- https://github.com/notofonts/mongolian
