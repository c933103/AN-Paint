# Author-stage corrections before independent review

The original d6bd8525 packet is superseded for the following draft-only judgments; no production text was changed.

- GIMP primary fa.po explicitly uses Pixels=تصدانه‌ها, Dithering=لرزاندن, Undo=برگردان. Initial unfamiliarity-based claim that the pixel term was malformed is withdrawn. Preserve current two pixel labels and Undo, and align new recovery/history and GIF description to existing terminology. No correction credit for these retained labels.
- GIMP primary he.po has non-fuzzy Dithering=ערבוב צבעים, matching the existing checkbox. Replace the author's unsupported רישות draft with that established term; preserve checkbox wording.
- Hebrew crop-edge descriptions use a neutral label prefix (%1$s: חיתוך בפיקסלים / באחוזים), avoiding incorrect adjective agreement when standalone Left/Right/Top/Bottom labels are inserted.
- Add three finite test/consumer companions (crop preview-image accessible label, Quality(%), Strength(%)) to the previous13;16total per locale. Full priority inventory unchanged.

Sources inspected2026-10-29: https://raw.githubusercontent.com/GNOME/gimp/master/po/fa.po and https://raw.githubusercontent.com/GNOME/gimp/master/po/he.po. These support bounded terminology, not full AN Paint sentences or native acceptance. Urdu PO was unavailable at the attempted corresponding path; no Urdu primary terminology verification is claimed. All complete FA/HE/UR candidate values still need independent linguistic/context review.

The Keep editing replacements are source/intent clarity improvements, not evidence of broken cancellation: ClassicPaintActivity.confirmReplacement lines1074–1079 uses the negative button with a null listener, so existing Cancel does in fact dismiss and preserve editing. Do not count them as destructive-action defects. A pending behavior test should prove no save/discard/replacement is triggered.

Packet validation passed10 tests in normal and optimized modes. These check all complete source/current pairs, consumer-window binding, typed341 identity sets, attributes, placeholders, Android quoting, technical literals and negative mutations. They are mechanical source-packet checks, not application/runtime or linguistic acceptance. First diagnostic version correctly exposed that the generic existing literal checker did not cover sRGB; added an explicit operational-literal guard and retained the negative test. No production validator was changed.
