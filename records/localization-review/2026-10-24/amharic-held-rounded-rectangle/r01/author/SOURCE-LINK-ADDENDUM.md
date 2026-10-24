# Source locators for the Rounded rectangle proposal

Added 2026-10-24. This addendum changes no proposed wording, confidence assessment, acceptance status or implementation status. The original proposal and evidence files remain unchanged. The existing hold still awaits independent adjudication.

## Immutable application-source locations

These links identify the exact production source examined for the proposal, rather than the moving develop branch. They replace the earlier mutable project links for locating the reviewed evidence.

- [English caption](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L341): the source label is Rounded rectangle.
- [Tool mapping, label accessor and default radius](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L27-L49): the caption identifies ROUND_RECT, and cornerRadius initially equals 16.
- [Locale-aware resource resolution](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/UiText.kt#L37-L69): the label is resolved through the application's text-resource boundary.
- [Visible caption, accessibility description and tooltip](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ToolButton.kt#L10-L12), and [category/accessibility composition](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ToolCategoryButton.kt#L16-L28).
- [Live button selection and label-plus-hint help](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L493-L497), [status interpolation](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L678-L691), and [tool selection/options heading](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L732-L750).
- [Selection may commit previously pending work](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L153-L157), with [applyPending behavior](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L443-L450).
- [Preview dispatch](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L265-L272), [sorted bounds and equal-radius corner geometry](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L406-L412), and [pointer-up commitment/cancellation](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L824-L842).
- [Radius and shape-style controls](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L774-L790), and [fill/outline rendering and commitment](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L272-L286).
- [Compact tile dimensions, line limits and ellipsizing](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/RibbonWidgets.kt#L60-L123). These source constraints do not establish actual rendering fit for the proposed caption.

## Grammar and dictionary page locators

“PDF page” below means the viewer's one-based page count, not the printed number. These are locators within the already examined source copies, not additional linguistic findings. The linked mirrors are mutable hosts of primary authored works; their hosted content is not represented as an immutable edition.

### Wolf Leslau, Amharic Reference Grammar

- Printed page 86; PDF page 103: introduction to relative qualifiers and section 25.1, supporting the qualifying clause before its head and the relative prefix. [Open that page](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=103).
- Printed page 92; PDF page 109: sections 25.6–25.7, relative-clause verb placement and agreement with the clause's own subject, including the beginning of the plural possessed-subject example. [Open that page](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=109).
- Printed page 93; PDF page 110: continuation explaining the plural internal subject with a singular external head; section 25.8 follows. [Open that page](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=110).
- Printed page 137; PDF page 155: section 31.3, especially the final paragraph and example, supporting present adjectival quality through honä in a subordinate clause. [Open that page](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=155).

### Wolf Leslau, Concise Amharic Dictionary

- Printed page 307; PDF page 306: left column, “corner (of room)” entry. The dictionary prints ማእዘን; the proposal's ማዕዘን spelling is separately corroborated by the contemporary sources already cited. [Open that page](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=306).
- Printed page 464; PDF page 463: left column, “round (v.)” and “round (adj.)” entries, with numeric roundness separately specified. [Open that page](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=463).

The complete proposed label remains a productive composition. These page locations substantiate its components and syntax, not exact whole-phrase attestation or human native-reader certification.
