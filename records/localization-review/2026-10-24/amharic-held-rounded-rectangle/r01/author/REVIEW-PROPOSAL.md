# Rounded rectangle: complete Amharic revision proposed

Date: 2026-10-24. Resource: string/ui_rounded_rectangle. English: Rounded rectangle.

Proposed wording: **ማዕዘኖቹ ክብ የሆኑ ቀጤ ጎነ አራት**

Meaning: a rectangle whose corners are round. This is a newly composed complete label, not an attested quotation. Recommend independent adjudication of this revision instead of retaining **የተከበበ አራት ማእዘን**. The existing hold remains in force; this proposal is neither acceptance nor implementation.

## Why revise

The old full phrase really occurs in LibreOffice. Its problem was not lack of attestation: its modifier leaves an enclosed/surrounded interpretation available. Replacing only its rectangle noun would not remove that ambiguity. LibreOffice also uses related wording for a closed shape. This is a reason to prefer explicit corners, not proof that the old phrase is unintelligible to every reader. [LibreOffice object labels](https://github.com/LibreOffice/translations/blob/master/source/am/svx/messages.po), [drawing help](https://help.libreoffice.org/latest/am/text/shared/02/01140000.html).

The revision identifies the corners as the things that are round, then names the rectangular base. It does not call the whole object a circle, add an enclosing border, require a square, or describe rotation. The established rectangle term is used as a component, without importing the separate Rectangle review's approval into this whole label. [ICT Development Office and ELRC terminology](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf).

## Linguistic basis and its limits

- Leslau's dictionary supplies ክብ for the adjective “round” and the physical-corner noun, spelled ማእዘን in that source. The proposed ማዕዘን spelling is also present in the contemporary corner/geometry sources below. These support components, not the complete UI phrase. [Concise Amharic Dictionary, primary authored work via public mirror](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf).
- Leslau's grammar supports a relative clause preceding its head, agreement with that clause's own subject, and ሆነ for present adjectival quality in a subordinate clause. Thus plural የሆኑ describes the corners, not a plural number of rectangles. The possessive form links those corners to the singular head. This is a grammatical composition judgment, not a quotation from the grammar. [Amharic Reference Grammar, primary authored work via university mirror](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf).
- An official school geometry handout uses an analogous possessive plural-parts + adjectival relative clause when describing a four-sided shape. It also uses a relative expression for a round object. This is limited contemporary corroboration, not endorsement of this caption or of every translation in the handout. [Montgomery County Public Schools Amharic mathematics handout](https://www.montgomeryschoolsmd.org/siteassets/district/info/enroll/kindergarten/2024-25/gettingready-math/0646.24_gettingreadyforkindergarten_math_amharic_web.pdf).
- The already-known JGraph entry ክብ ጠርዝ and LibreOffice's corner-rounding help independently support applying roundness to a boundary feature. JGraph uses its “rounded” resource for a rounding-style control. Neither is the proposed whole phrase. These are re-examined existing software leads, not newly discovered exact translations. [JGraph catalog](https://github.com/jgraph/drawio-i18n/blob/dev/dia_am.txt#L750), [rounding control](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/js/grapheditor/Format.js#L8375-L8385), [LibreOffice corner-radius help](https://help.libreoffice.org/latest/am/text/shared/01/05230400.html).
- Unicode's rounded-corner-square annotation uses a roundness expression, but calls the relevant features “sides.” It corroborates that approach, not the precise noun or whole phrase recommended here. [Unicode Amharic annotations](https://github.com/unicode-org/cldr/blob/release-47/common/annotations/am.xml#L562-L563).

## Actual application meaning

Fresh source review confirms a drawing-tool caption, not an edit command applied to an existing rectangle. Dragging sets rectangular bounds; the drawing path rounds corners with equal horizontal and vertical radii, clamped between zero and half the shorter dimension. Zero radius is allowed, so the name denotes a configurable shape family, not a guarantee of visibly curved corners in every result. Outline and fill choices are separate. Selecting a different tool may commit previously pending work. [Geometry](https://github.com/c933103/AN-Paint/blob/develop/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L406-L412), [tool options](https://github.com/c933103/AN-Paint/blob/develop/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L774-L790).

The same label supplies the tile, tooltip, accessibility description, options heading and larger status/help text. The tile is compact and ellipsizes long captions: this six-word proposal needs later rendering review, which was not performed. The complete label remains available to tooltip/accessibility consumers in source. No English source defect was established. [Caption consumers](https://github.com/c933103/AN-Paint/blob/develop/Paintroid/src/main/java/org/catrobat/paintroid/classic/ToolButton.kt#L10-L12), [tile constraints](https://github.com/c933103/AN-Paint/blob/develop/Paintroid/src/main/java/org/catrobat/paintroid/classic/RibbonWidgets.kt#L60-L123).

## Confidence, alternatives, and decision requested

Semantic fit: medium-high. Productive grammar: medium-high. Complete-caption naturalness and technical-term familiarity: medium. Rendered fit: unassessed. No human native-reader certification is claimed.

The alternative **ክብ ማዕዘኖች ያሉት ቀጤ ጎነ አራት** (“rectangle having round corners”) is also a defensible composition, but offers no material shortening. A version using ጠርዝ is less explicit about corners rather than the entire edge. The old modifier with a more precise rectangle noun retains the original ambiguity. A የተጠጋጉ version was not preferred because this pass did not establish a sufficiently strong primary geometric usage for that modifier; that is not a finding that it is wrong.

The independent decision should assess the entire proposed wording: does it naturally identify round corners while retaining the rectangular base, and is its descriptive length acceptable as a textual proposal? Exact prior publication of the whole phrase is not required. No resources, application behavior, builds, tests, CI, release, or deployment changed.
