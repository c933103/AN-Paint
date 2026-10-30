# Shan palette composite — recovered historical contract

## Exact proposed target

Key: `ui_foreground_background_colour_palette` (P1)

Source: `Foreground %1$s, background %2$s. %3$s colour palette.`

Target: **သီတၢင်းၼႃႈ %1$s၊ သီပိုၼ်ႉလင် %2$s။ ပၢၼ်ႉသီ — %3$s။**

Backtranslation: **Foreground colour %1$s, background colour %2$s. Colour palette — %3$s.**

Disposition: author recommends this revised exact target for independent linguistic review against the recovered historical contract. This does not revive the caller, approve present runtime behavior, or silently accept an unknown argument contract. The original batch-E bytes remain unchanged; `palette-historical-contract-revision.tsv` is the separate revision receipt.

## Source binding actually verified

- Current remote `develop` was read as commit **96681f687671a1fdffe134a325843919c1543401**, tree **39bb7351fa5532194e2c0430432b2f0cc6358a86**.
- Current [English strings](https://github.com/c933103/AN-Paint/blob/96681f687671a1fdffe134a325843919c1543401/Paintroid/src/main/res/values/strings.xml), content blob **b50c607aac54c6148e5ac4e44325cb6db3be3612**, retain the exact parent source plus `Left arrow: collapse` and `Right arrow: expand` fragments.
- Current [Shan strings](https://github.com/c933103/AN-Paint/blob/96681f687671a1fdffe134a325843919c1543401/Paintroid/src/main/res/values-b%2Bshn/strings.xml), content blob **352c80913acef74688d71c28a10307663de01b3a**, have **none of the three keys**. The local read-only materialization agrees. It would be false to claim current canonical Shan fragment values.
- Historical [ColourStatusButton.kt at f47d9ee9458f2f9207eae5e3514f211baecdfa51, lines 37–44](https://github.com/c933103/AN-Paint/blob/f47d9ee9458f2f9207eae5e3514f211baecdfa51/Paintroid/src/main/java/org/catrobat/paintroid/classic/ColourStatusButton.kt#L37-L44), content blob **f76a3a4c2481fc2ea1f4fa925f322a64031d1433**, passes foreground `hex`, background `hex`, then `expanded ? Left arrow: collapse : Right arrow: expand`. Its `hex` helper already supplies the leading `#`; the target must not add another hash.
- At [fd80d394e83104395f7e425a5b781e343943583c](https://github.com/c933103/AN-Paint/blob/fd80d394e83104395f7e425a5b781e343943583c/Paintroid/src/main/java/org/catrobat/paintroid/classic/ColourStatusButton.kt), content blob **c4c4797fe5868a22aef6f33f2def3500a817c016**, that composite caller has been replaced by separate foreground/background wording. Current file blob **f233c81fbdbfefd76f461ca5dbb1c0da5351448e** retains the replacement. The resource's survival is historical source evidence, not proof of a current call.

## Whole Shan composition, not English word-order copying

The third argument includes both arrow direction and an action. It cannot safely be treated as a palette name, colour count or expanded/collapsed state adjective.

The independently reviewed C left fragment is **ပိုၼ်ၸီႉသၢႆႉ: တူပ်ႉဝႆႉ**. In an ordinary Shan transitive clause, an explicit palette object would occur within **တူပ်ႉပၢၼ်ႉသီဝႆႉ**, not be blindly appended after the already complete **တူပ်ႉဝႆႉ**. `%3$s` cannot be split to insert that object. Moving `%3$s` before the palette noun merely to imitate English would therefore not solve the composition.

The revised parent instead explicitly makes **ပၢၼ်ႉသီ** the topic, separated by an em dash, followed by the complete arrow/action instruction. This is a topic-plus-instruction structure, not a malformed verb/object splice. The foreground and background values retain their respective roles, and all three indexed placeholders occur exactly once.

Exact expanded composition with the reviewed left fragment:

> သီတၢင်းၼႃႈ #000000၊ သီပိုၼ်ႉလင် #FFFFFF။ ပၢၼ်ႉသီ — ပိုၼ်ၸီႉသၢႆႉ: တူပ်ႉဝႆႉ။

Meaning: Foreground colour #000000, background colour #FFFFFF. Colour palette — left-pointing arrow: collapse.

For the missing right fragment, the bounded ancillary proposal is **ပိုၼ်ၸီႉၶႂႃ: ၶႂၢၵ်ႈ** (right-pointing arrow: expand). This uses accepted right-direction vocabulary and the previously reviewed expand action, but the exact right-fragment string itself still requires independent review. It is P2 in the current importance file and receives no P0/P1 credit here.

Exact conditional collapsed composition:

> သီတၢင်းၼႃႈ #000000၊ သီပိုၼ်ႉလင် #FFFFFF။ ပၢၼ်ႉသီ — ပိုၼ်ၸီႉၶႂႃ: ၶႂၢၵ်ႈ။

Meaning: Foreground colour #000000, background colour #FFFFFF. Colour palette — right-pointing arrow: expand.

`palette-historical-compositions.tsv` also shows both English-fallback compositions arising from the actual current missing-fragment inventory. They must not be represented as fully translated Shan or as observed runtime output. The revised parent is linguistically assessable now, but any later whole-control completeness claim must account for the missing P2 right fragment.

## Limits and unchanged scope

Completed: verified historical argument roles, current canonical fragment absence, independently reviewed left wording, exact full compositions and a source-bound revised parent target. Pending: independent review of the parent revision and any separate right-fragment proposal. Uncertain: present runtime/assistive-technology rendering and punctuation speech, which were not tested and are outside this linguistic review.

Airbrush and every unrelated held item remain untouched. No application integration, runtime approval or native-human certification is asserted.
