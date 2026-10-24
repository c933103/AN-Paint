# Amharic Rounded rectangle: release the hold with a revision

Date: 2026-10-24. Resource: string/ui_rounded_rectangle. English source: Rounded rectangle.

Decision: **RELEASE_WITH_REVISION**, for a reviewed textual proposal, not an application release.

Accepted wording: **ማዕዘኖቹ ክብ የሆኑ ቀጤ ጎነ አራት**

Meaning: a rectangle whose corners are round.

This independent review accepts the exact complete composition above. It replaces the held proposal **የተከበበ አራት ማእዘን** for this one resource. The older wording and its original hold remain part of the review history; they are not silently overwritten or approved. No production resource has been changed.

## Why the terminology hold is resolved

The earlier hold concerned a substantive interpretation risk: the old modifier could describe an enclosed or surrounded object instead of specifically rounded corners. Exact publication of that old phrase in LibreOffice did not resolve its ambiguity. The replacement makes the corners the subject of roundness and keeps an explicit rectangular base. It is a label for a shape family, not an instruction to enclose an object or to modify an already drawn rectangle.

The whole phrase is a defensible descriptive Amharic noun phrase. The corners form the plural internal subject; the relative verb agrees with them, while the head names a singular rectangle. The qualifying clause precedes that head. Leslau's grammar supports this structure and the present adjectival use of the copula. The conclusion is a compositional judgment, not a claim that the grammar publishes this UI phrase. See printed pages 86, 92–93 and 137, corresponding to PDF pages 103, 109–110 and 155. [Amharic Reference Grammar](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=103).

The lexical components have relevant support. Leslau supplies the adjective for round and a physical-corner noun, with a spelling variant in the dictionary. The ICT Development Office and Ethiopian Languages Research Center glossary supplies the precise rectangle term at entry 2174. The complete composition is assessed here independently; acceptance of the separate Rectangle proposal is not being reused as automatic approval. [Concise Amharic Dictionary, printed pages 307 and 464](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=463), [ICT terminology, entry 2174](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf).

An official school mathematics handout provides a close structural parallel using plural possessed parts, an adjectival relative clause and a singular shape head. It also provides round-object wording. This is useful corroboration, not comprehensive idiom certification: some unrelated wording in that handout is awkward. [Montgomery County Public Schools Amharic mathematics handout, pages 1–2](https://www.montgomeryschoolsmd.org/siteassets/district/info/enroll/kindergarten/2024-25/gettingready-math/0646.24_gettingreadyforkindergarten_math_amharic_web.pdf).

Software evidence is supplementary. JGraph uses round-boundary wording for a rounding-style control and separately names corners; LibreOffice corner-radius help applies roundness to a rectangular object's boundary features. Neither is exact attestation of the accepted caption, and multiple files from one project are not separate authorities. The decision does not depend on Unicode's less precise sides wording. [JGraph components](https://github.com/jgraph/drawio-i18n/blob/1c5b1f23fe0b5ba1ce51d749b0d63d946a5f9e17/dia_am.txt#L750), [JGraph control](https://github.com/jgraph/drawio/blob/84487b4891cbc0f32d7e30f34cf878c87cb1f414/src/main/webapp/js/grapheditor/Format.js#L8375-L8385), [LibreOffice corner-radius help](https://help.libreoffice.org/latest/am/text/shared/01/05230400.html).

Exact previous publication of a novel complete translation is not required. Here the specific meaning, construction and application context are sufficiently supported to resolve the old terminology hold. This does not claim that every possible alternative is worse or that all readers will find the terminology equally familiar.

## Application-context boundaries

The reviewed code makes a path from sorted rectangular drag bounds, using equal horizontal and vertical corner radii clamped from zero to half the shorter dimension. The accepted wording describes that configurable family. Zero radius, equal dimensions or capsule-like limits do not establish an English-source defect or require a different generic tool name. Fill and outline are independent choices. Selecting this tool does not itself create a new rounded rectangle, but changing tools may commit earlier pending work. [Geometry](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L406-L412), [style controls](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L779-L790), [tool switching](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L153-L157).

The six-word label is longer than the old proposal. Compact tiles have line limits and ellipsizing, while tooltip and accessibility assignments receive the complete caption. Actual fit, font fallback, pronunciation and spoken delivery were not tested. Length is therefore a later rendering-review requirement, not evidence of either successful fit or a failed translation. [Caption assignment](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ToolButton.kt#L10-L12), [tile constraints](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/RibbonWidgets.kt#L60-L123).

No English-source defect was established. If one is later established, correct English first, flag affected terms across languages, then review them individually. This decision does not approve other labels, hints or surrounding templates.

## Confidence and preserved alternatives

- Semantic fit: medium-high.
- Productive grammar: medium-high.
- Whole-caption naturalness and technical-term familiarity: medium.
- Rendering, native-reader and screen-reader certification: not performed.

The complete alternative **ክብ ማዕዘኖች ያሉት ቀጤ ጎነ አራት** remains a defensible, unselected option. It offers no meaningful length advantage. Versions using a broader edge word are less explicit about the corners; changing only the old rectangle noun leaves the original modifier ambiguity. **ማዕዘኖቹ የተጠጋጉ ቀጤ ጎነ አራት** is not rejected as incorrect, but the present evidence does not justify preferring it.

Inventory effect when this decision is recorded: one held proposal becomes ready with revised wording. The supplied baseline of 98 ready / 10 held would become 99 ready / 9 held. Implemented remains 0, and the separately pending 90 remain unchanged. These are the effect of this single decision, not a new independent audit of the complete inventory.

No Work task, production edit, build, application test, CI, deployment or release was started. The outcome is a completed textual adjudication with explicit implementation limits.
