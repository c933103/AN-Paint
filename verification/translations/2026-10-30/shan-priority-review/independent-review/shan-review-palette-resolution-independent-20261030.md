# Shan palette alias — independent resolution

## Decision

**Accept the exact revised P1 parent value:**

`သီတၢင်းၼႃႈ %1$s၊ သီပိုၼ်ႉလင် %2$s။ ပၢၼ်ႉသီ — %3$s။`

Backtranslation: **Foreground color %1$s, background color %2$s. Color palette — %3$s.**

Confidence: **moderate-high semantic, moderate idiomatic**. This independent AI/model review is not native-human certification.

This exact revision and newly recovered argument contract supersede the earlier batch-E integration hold. They do not retroactively accept the original unseparated target or establish a current runtime caller.

## Independently verified contract

The [historical ColourStatusButton source at f47d9ee9458f2f9207eae5e3514f211baecdfa51](https://github.com/c933103/AN-Paint/blob/f47d9ee9458f2f9207eae5e3514f211baecdfa51/Paintroid/src/main/java/org/catrobat/paintroid/classic/ColourStatusButton.kt#L37-L44) was fetched and read directly. It passes:

1. Foreground hexadecimal color, already including `#`.
2. Background hexadecimal color, already including `#`.
3. A complete localized **left-arrow/collapse action fragment when expanded**, otherwise a complete localized **right-arrow/expand action fragment**.

The third argument is not a palette name, color count or expanded/collapsed state adjective. That positive source evidence resolves the earlier uncertainty rather than simply waiving it.

The current source at develop **96681f687671a1fdffe134a325843919c1543401**, tree **39bb7351fa5532194e2c0430432b2f0cc6358a86**, was also read. Its status control uses separate foreground/background wording, not the historical composite. Current English resources retain the parent and both fragments; current Shan resources contain none of those three keys. No current-call or restored-call claim is made.

## Whole-value composition

The parent names the palette as a topic, separated by an em dash, and then gives the intact arrow/action instruction. This is appropriate compact instructional phrasing. It avoids attempting to insert an object into the supplied collapse verb-plus-particle construction or appending an unknown action as if it were a noun modifier.

Both exact Shan compositions in `shan-review-palette-compositions-independent-20261030.tsv` are linguistically accepted. Direction/action pairs remain correct, foreground/background roles are unchanged, and no extra `#` is added. All three indexed `%s` arguments are retained exactly once; the sole attribute remains `name`.

The right fragment **ပိုၼ်ၸီႉၶႂႃ: ၶႂၢၵ်ႈ** is independently acceptable as **right-pointing arrow: expand**. This is an **ancillary P2 wording assessment only**, with no P0/P1 credit or source-integration authorization. The left P1 fragment's previous acceptance remains unchanged, not counted twice.

Both English-fallback compositions are compatible with the parent topic structure but are explicitly mixed-language. They do not become fully Shan merely because the parent is accepted. They are conditional source-derived examples, not observed output. Punctuation speech, rendering and TalkBack behavior remain untested.

## Disposition effect

The parent resolves one missing P1 hold:

- Accepted missing lexical values: **140 = 26 P0 + 114 P1**.
- Separate notation-only values: **7 P1**.
- All accepted missing values: **147 = 26 P0 + 121 P1**.
- Remaining holds: **36 = 27 P0 + 9 P1**.
- Entire scope remains **183 missing values = 53 P0 + 130 P1**.

Airbrush and all 35 other existing holds remain unchanged. Undo's unchanged review, Brush replacement, previous accepted entries and ancillary P2 evidence receive no duplicate missing-priority credit.

## Input fingerprints

| Record | SHA-256 |
|---|---|
| `palette-historical-contract-revision.tsv` | `350b0b18557e5a2e9a753ca963a01fc0608ac500d9f193c475c6d4b75b402c7e` |
| `palette-historical-compositions.tsv` | `9758ac8455ca7c39c91040639a4839fdf3ba3907e6c29f79fed35e82c4e77ee1` |
| `palette-historical-contract-review.md` | `fe9ccb215d9522fbc68daac55ffa45f3b6f1437550e7c4e2497433f86d9f42ec` |

Completed: historical/current source reading, exact parent and four composition assessments, ancillary right-fragment assessment. Uncertain: installed/runtime/assistive-technology behavior. No implementation or test result is asserted.
