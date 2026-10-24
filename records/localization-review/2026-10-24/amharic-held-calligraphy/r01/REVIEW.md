# Amharic Calligraphy: independent adjudication

**Decision: release the translation hold with revision.** Accept **ቁም ጽሕፈት** for **string/ui_calligraphy — Calligraphy**, replacing the held proposal **ሰያፍ ጭረት**. This is a wording decision, not a production change or application release.

## Why the hold is resolved

The previous candidate describes a diagonal stroke but omits the named calligraphic character. The new candidate supplies that missing concept rather than substituting another implementation description. The earlier hold was justified for the old wording; its historical record remains intact.

I independently rendered and visually inspected the calligraphy entry in [Wolf Leslau’s Concise Amharic Dictionary](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=287), English–Amharic section, printed p. 288 / PDF p. 287. It reads **(የ)ቁም ጽሕፈት**, with the source’s Ethiopic word separators normalized here to spaces. This supports the compound as a lexical unit for calligraphy, not an invented combination of “upright” and “writing.” The optional prefix supports the unprefixed form, but does not by itself establish a uniquely preferred modern UI label. The scan’s exact edition is not established.

I also independently re-read the [publisher-hosted Amharic IRS article](https://www.irs-az.com/sites/default/files/2021-01/10-20_0.pdf#page=5), printed p. 14 / PDF p. 5. The Navvab passage uses **ቁም ጽሕፈት** for an Azerbaijani artist’s calligraphic art. This is evidence of broader artistic usage, not solely an Ethiopian bookhand or a literal upright stroke. It does not prove universal contemporary familiarity. Its PDF text was readable; visual confirmation of that page remained unavailable. No unrelated historical claims are adopted. [Abyssinica’s entry](https://dictionary.abyssinica.com/Calligraphy) corroborates the prefixed form, but its unspecified derivation is not counted as an independent lexicographic judgment.

## Full label in the actual control

The [Brush options and selection callback](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L747-L827) present Round, Square and Calligraphy, then set the selected tip and show its caption. Watercolor, Eraser and Line receive only the first two choices. The nearby Brush heading supplies the context; neither the English noun nor the accepted Amharic noun has to repeat “brush tip.”

The [renderer](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L507-L526), together with [paint construction](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L247-L258), repeats a fixed diagonal, elongated, round-capped footprint along arbitrary user-drawn paths. Its directional width effect supports the calligraphic-tip interpretation. It is not a diagonal-only path, an exact rectangular nib, a font selector, a handwriting-input mode or automatic lettering. Ordinary touch and cursor drawing reach the same stroke routine; cursor-marker shape is separate. These are static-source findings, not executed behavior tests.

[Inkscape’s own guide](https://inkscape-manuals.readthedocs.io/en/latest/calligraphy-tool.html) corroborates the English graphics-domain association between calligraphy and pen/brush geometry. Its additional features are not attributed to AN Paint.

My contextual judgment is that **ቁም ጽሕፈት** is a defensible, compact noun label for this calligraphic brush-tip style. It preserves the source concept without adding a specific script, font or text-conversion promise. This judgment combines lexical meaning, grammatical form and the control’s purpose; an exact earlier software caption is neither required nor claimed.

## Alternatives and confidence

- **የቁም ጽሕፈት** is attested and defensible with an implied head noun. The bare noun is preferred here because it is independently supported and avoids requiring that genitive ellipsis. This is a contextual choice, not a claim that the prefixed alternative is wrong.
- **ካሊግራፊ** is a viable borrowing, independently re-read in the public descriptions/captions of [Habiba Calligraphy](https://t.me/s/Habibacalligraphy?before=643) and [Khalid Arts](https://t.me/s/Khalid_Arts?before=233). These establish use, not broader familiarity or superiority for this UI. The unretrieved textbook lead contributes no positive evidence.
- Generic handwriting, beautiful-writing paraphrases and diagonal-stroke wording have no demonstrated advantage over the accepted lexical term. The old diagonal-stroke proposal remains rejected.

Confidence: **high** for source semantics and lexical concept match; **medium-high** for contextual fidelity and the bounded decision; **medium** for contemporary idiom and UI preference. No native-speaker, rendering, accessibility or whole-language acceptance is claimed. Those limits do not recreate the resolved translation-fidelity hold.

## Scope and accounting

Keep the English source unchanged: no source defect was established. The exact Amharic key is absent from the inspected catalogue; nothing was implemented. No other key was adjudicated.

Applied to the supplied baseline only, this decision moves one item from held to ready: **102 ready, 6 held, 0 implemented; 90 pending unchanged**. This arithmetic is not a new audit of the other items or a claim that a durable register has already been updated.

No Work task, production edit, app execution, app build/test, CI, remote publication or release occurred. The independent report and structured decision are the only publication candidates from this review; full sources, scans and private verification material are excluded.
