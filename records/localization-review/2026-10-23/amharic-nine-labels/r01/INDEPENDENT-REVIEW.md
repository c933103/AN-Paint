# Independent Amharic nine-label review

Independent review complete: seven retain conclusions, one supported optional punctuation refinement, and Palette remains unresolved rather than an accepted correction.

Verified all 16 complete-file SHA256 bindings and all nine English/current XML pairs against production 66be61df27c5359bffc32d56db21f3949899f873. Read actual consumers and relevant behavior. No implementation, builds, execution, or publication.

## Per-key conclusions

1. ui_eraser — Eraser / “ላጲስ”
Retain. High semantic confidence, medium-high UI confidence. The primary teaching workbook explicitly gives this exact spelling as eraser. Background-colour erasing does not invalidate the conventional tool metaphor. [Primary vocabulary, printed p.15](https://conference.usu.edu/SYSTEM/Uploads/Handouts/15233_1981miriamredleaf.pdf)

2. ui_pencil — Pencil / “እርሳስ”
Retain. High semantic confidence. Conventional pencil noun fits the crisp drawing tool. Width is adjustable; the actual English hint already says 1–100 pixels, so the old resource identifier creates no English-source defect. [Publisher dictionary](https://dictionary.abyssinica.com/pencil)

3. ui_text — Text / “ጽሑፍ”
Retain. High semantic confidence. Appropriate noun for placing written text and opening its style controls. Not limited to prose reading or font selection. [Publisher dictionary](https://dictionary.abyssinica.com/text)

4. ui_palette — Palette / “መደርደሪያ”
Do not accept the proposed replacement as a demonstrated correction. Current wording has relevant software precedent, not merely the unrelated everyday meaning “shelf”: GNOME GTK’s colour selector catalogue contains “_Palette:” → “መደርደሪያ (_P)”. However, this entry is marked fuzzy and the translator revision is historical, so it proves precedent, not contemporary acceptance.

Proposed “የቀለም ስብስብ” is semantically plausible as “colour collection”, but I did not establish a sufficiently authoritative full-phrase precedent or native UI judgment proving it preferable. Search results using the phrase included apparently automated localization and do not settle idiomatic quality.

Recommendation: preserve current resource pending targeted terminology adjudication; record both alternatives and uncertainty. Confidence high that evidence is insufficient for an accepted correction; medium concerning either wording’s current usability. [Primary GTK catalogue, gtkcolorsel.c entry](https://raw.githubusercontent.com/GNOME/gtk/main/po/am.po)

Consumer clarification: mode 0 specifically shows basic swatches. Saved/custom swatches occupy a shared panel available to every selector. The author’s “basic/saved swatches” description is broadly visible-context accurate but should not imply saved colours belong exclusively to this tab.

5. ui_preview — Preview / “ቅድመ ዕይታ”
Retain. High semantic, medium-high UI confidence. Stronger evidence than the author recovered: GTK’s non-fuzzy “_Preview:” entry for gtkfontsel.c uses “ቅድመ _ዕይታ፦”, matching both the current spelling and font-preview context. No basis for changing ዕ to እ merely to match another glossary. [Primary GTK catalogue](https://raw.githubusercontent.com/GNOME/gtk/main/po/am.po)

6. ui_zoom_in — Zoom in / “ከቅርበት ዕይታ”
Retain provisionally as the coherent near-view half of the pair. Medium-high semantic, medium UI confidence. Source verifies viewport multiplication by 1.5, not image resizing. GTK contains the same phrase for Zoom In, although marked fuzzy. A noun phrase can label the resulting view without being a literal imperative.

7. ui_zoom_out — Zoom out / “ከርቀት ዕይታ”
Retain provisionally alongside Zoom In. Medium-high semantic, medium UI confidence. Source verifies viewport multiplication by 1/1.5. GTK also contains this exact far-view phrase, marked fuzzy. The ICT glossary offers imperative alternatives, but that does not establish the existing pair as erroneous. [GTK pair](https://raw.githubusercontent.com/GNOME/gtk/main/po/am.po), [ICT glossary, final page](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

8. ui_horizontal23 — Horizontal / “አግድም፦”
Support optional proposed literal body “አግድም”, exact XML text "\"አግድም\"". Medium-high confidence. The directional word is appropriate; this standalone spinner choice introduces neither a following value nor an explanation. Removing terminal introductory punctuation improves the label without changing its meaning. Treat as punctuation polish, not a substantive mistranslation. No synonym replacement warranted.

9. ui_category_selection — Selection / “ምርጫ”
Retain. Medium-high semantic, medium UI confidence. Broad selection/choice noun fits the category grouping rectangular and lasso image-area selection; contextual disambiguation is sufficient. This does not accept the complete composed accessibility strings, which include other resources. [Publisher dictionary](https://dictionary.abyssinica.com/selection)

## Evidence limits

- These are independent AI source-context judgments, not native-speaker certification or runtime/accessibility validation.
- Historical GTK entries are evidence of precedent only. Fuzzy Palette/Zoom entries must not be represented as validated current translations.
- The glossary’s extracted Palette equivalent “ቤተ ስእል” remains unsuitable as a replacement basis without resolving the author’s extraction concern and its broader sense.
- No English-source correction prerequisite identified for these nine labels.
- No acceptance of missing Amharic strings or unrelated held scopes.
