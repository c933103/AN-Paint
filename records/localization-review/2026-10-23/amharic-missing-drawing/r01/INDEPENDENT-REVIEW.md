# Independent review: seven missing Amharic drawing labels

Recommendation: retain all seven drafts unchanged. No correction or hold is justified by the inspected source and lexical evidence. This is independent evidence-based review, not native-speaker certification.

Exact proposed XML:
```xml
<string name="ui_brush">"ብሩሽ"</string>
<string name="ui_line">"መስመር"</string>
<string name="ui_curve">"ጥምዝ"</string>
<string name="ui_rectangle">"ቀጤ ጎነ አራት"</string>
<string name="ui_heart">"ልብ"</string>
<string name="ui_star">"ኮከብ"</string>
<string name="ui_arrow">"ቀስት"</string>
```

Per-key findings:
- Brush: retain. Semantic confidence high; UI idiom medium-high. Generic brush noun is appropriate for the selected-tip painting tool. Additional primary evidence strengthens the draft: Unicode CLDR36 names the paintbrush symbol “የሠዓሊ ብሩሽ”, specifically establishing the painting use of ብሩሽ, not merely cleaning.
- Line: retain. Semantic high; UI idiom medium-high. ICT glossary entry 1634 explicitly includes drawing lines. The short noun fits the straight two-endpoint tool without adding an unnecessary adjective.
- Curve: retain. Semantic high; UI idiom medium. ICT glossary entry 759 supplies ጥምዝ against an explicitly nominal mathematical-path definition. Therefore the proposed standalone form is not unsupported merely because it can also function adjectivally. Abyssinica independently maps ጥምዝ to curve. No evidence requires expanding it to a phrase or substituting ኩርባ.
- Rectangle: retain. Semantic high; UI idiom medium. ICT glossary entry 2174 supplies the exact spaced form ቀጤ ጎነ አራት and identifies right angles. Abyssinica also gives that exact form. Do not shorten to generic ጎነ አራት or otherwise lose the rectangle distinction.
- Heart: retain. Semantic high; UI idiom medium-high. CLDR’s heart-symbol keyword is ልብ; appropriate to the closed heart silhouette.
- Star: retain. Semantic high; UI idiom medium-high. CLDR’s star-symbol keyword is ኮከብ; appropriate to the five-pointed shape, not a rating action.
- Arrow: retain. Semantic high; UI idiom medium-high. ICT glossary entry 169 explicitly concerns an arrow-shaped directional mark, matching the shaft-and-head tool rather than relying on bow/arch senses.

Verification:
- All seven exact English values match the draft; all seven keys are absent from values-b+am/strings.xml.
- Canonical catalogue contains 720 containers, including three explicitly nontranslatable strings: 717 translatable containers. Amharic has 12; missing count 705 is correct.
- Recomputed SHA-256 and Git blob hashes for all ten source files match source-bindings.json.
- Inspected PaintTool mappings, ToolButton visible text/contentDescription/tooltip, category accessibility composition, help composition, status composition and options heading. Inspected the brush stroke implementation, line/rectangle paths, staged cubic curve, and heart/star/arrow constructors. Draft descriptions accurately represent those consumers.
- Commit-to-tree provenance was not freshly independently established: the source snapshot is not a Git checkout. The verified file bytes match every supplied blob binding, but the supplied association with commit 66be61df remains inherited provenance.

Primary lexical sources:
- [ICT Development Office / Ethiopian Languages Research Center glossary, mirrored original PDF](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf): printed pages 14, 65, 139, 188, entries 169, 759, 1634, 2174.
- [Unicode CLDR36 annotations](https://www.unicode.org/cldr/cldr-aux/charts/36/annotations/afro_asiatic.html): U+1F58C paintbrush, U+2764 heart, U+2B50 star.
- [Abyssinica brush](https://dictionary.abyssinica.com/brush), [curve](https://dictionary.abyssinica.com/%E1%8C%A5%E1%88%9D%E1%8B%9D), [rectangle](https://dictionary.abyssinica.com/rectangle).

No source edits, builds, CI, publication or Work-side tasks. Polygon remains excluded without asserting an English defect. This review does not accept the surrounding untranslated hints or mixed-language composed strings.
