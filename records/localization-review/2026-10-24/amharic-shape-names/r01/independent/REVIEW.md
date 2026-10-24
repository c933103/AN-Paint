# Independent Amharic shape-caption review

Date: 2026-10-24. Source-only linguistic and consumer-context review, not implementation or native-reader certification.

## Decision

| Resource | Exact English | Exact proposed Amharic | Verdict |
|---|---|---|---|
| `string/ui_ellipse` | Ellipse | ኤሊፕስ | RETAIN |
| `string/ui_polygon` | Polygon | ፖሊጎን | RETAIN |
| `string/ui_rounded_rectangle` | Rounded rectangle | የተከበበ አራት ማእዘን | HOLD |

The batch result is two retained proposals, zero revised caption values, and one terminology hold. Retain means the exact proposal passes this bounded evidence-based review; it is not a deployment instruction or a claim of human native-speaker approval. The prior 88 ready / 13 held proposals are separate and untouched. No cumulative total is adjudicated here.

## Input identity and independent checks

Reviewed directory: `amharic-shape-names-draft-20261024`.

Input `MANIFEST.json` SHA-256: `65b99c6021205118c3bf54bdc0e6f5d7bbe3bd54581d3c78ca8742ab78949cc0`.

All 30 listed input file SHA-256 values pass. All 13 complete project source copies match both their recorded SHA-256 and the Git blob identity recomputed from the complete bytes. They also match the selected path, size, and blob identities in the supplied tree evidence for commit `66be61df27c5359bffc32d56db21f3949899f873`, tree `870c5a584120d92710be516af0dc3b3847b183d9`.

This establishes exact agreement with the supplied pinned evidence. The reviewer did not independently re-fetch the repository HEAD, authenticate the saved remote response, or perform an exhaustive fresh whole-repository consumer search. “Current” is bounded by the parent's source retrieval and the pinned commit, not a new live-HEAD claim.

All 52 extracted PO blocks match their specified source-file line ranges. Their parsed msgid, msgstr, msgctxt and flags match the JSON records. None has a fuzzy flag. The four primary snapshots are four files from one LibreOffice translation project, not four independent linguistic authorities.

Evidence correction: 42 records contain Amharic script, nine are explicitly untranslated English context, and one is the unchanged English pair Polyline → Polyline at `libreoffice-am-svx.po:277`. That last record is labelled “primary lexical evidence” in the input but must be treated only as English contrast, not evidence for an Amharic term. The sealed input has not been edited.

## 1. Ellipse: RETAIN ኤሊፕስ

Fidelity: the concise geometric loanword matches Ellipse without changing it to Circle, Oval, ellipsis punctuation, a selection, or an effect. It is attested as a complete non-fuzzy label, not assembled from word fragments. LibreOffice uses the identical word for a drawing object, drawing command, and help heading: `svx:211`, `ui:20480`, and `help02:253`. Those contexts matter more than simple string frequency.

The application consumer is geometric. The resource maps to ELLIPSE in `PaintDocument.kt:30`; `PaintCanvas.kt:406–412` sorts the drag endpoints into a RectF and calls `addOval`. Preview dispatch is at `PaintCanvas.kt:265–272`, and pointer-up commitment is at `PaintCanvas.kt:835`; `PaintDocument.kt:272–286` supplies outline/fill rendering and commit. Equal dimensions can yield a circle, and degenerate gestures remain possible, without changing the tool's name.

Idiomatic judgment: acceptable compact technical UI terminology, with high source-fidelity and contextual confidence, and medium general-reader familiarity confidence. The same exact loanword also appears in the official JGraph/draw.io Amharic catalog, independently inspected during this review. This corroborates real software usage, not universal familiarity or linguistic standardization. No stronger reason to replace it with the broader ኦቫል was established.

Consumer-description correction: “Label selection alone does not draw” is too broad. `PaintCanvas.selectTool`, lines 153–157, first invokes `applyPending`, which may commit existing geometry. Use: “Selecting Ellipse does not itself create a new ellipse, but changing tools may commit already-pending geometry.” This is a correction to explanatory evidence, not to either language's caption.

## 2. Polygon: RETAIN ፖሊጎን

Fidelity: the complete loanword preserves Polygon. It is not an invented compound and does not promise that every intermediate path or every configuration is a closed, nondegenerate mathematical polygon. Exact drawing-object and command attestations occur at `svx:259`, `help02:280`, and `ui:24266`. The official JGraph/draw.io catalog independently repeats `polygon=ፖሊጎን`.

The application maps the caption to POLYGON at `PaintDocument.kt:29`. `PaintCanvas.kt:419–421` joins vertices with straight segments and conditionally closes the path. `closePolygon` defaults to true at line 71 and is user-controlled in `ClassicPaintActivity.kt:798–800`. `applyPending` at `PaintCanvas.kt:443–449` commits at least two vertices as POLYGON when closed, or as LINE when open. The LINE dispatch disables interior filling in `PaintDocument.kt:274–281`, irrespective of shapeStyle. Closed-mode double-tap eligibility requires at least three vertices; open mode requires at least two (`PaintCanvas.kt:751–753`). Finish and changing tools can invoke `applyPending` separately. These are not guarantees against self-intersection or degenerate geometry.

The source name need not be silently changed to Polyline. In fact, the supplied LibreOffice help record at `help02:298` also explains a Polygon tool that produces straight segments and can finish open or be closed. That is useful evidence of a drawing-tool convention, not a mathematical redefinition. The actual AN-Paint behavior is established by AN-Paint source, not borrowed from LibreOffice.

Idiomatic judgment: acceptable compact technical UI loanword; high fidelity and behavioral-context confidence, medium broader-reader familiarity confidence. Native-form alternatives may be worth future research, but no verified full replacement is established here. No change to English, no rename to Polyline, and no acceptance of the separate Finish/Close controls or hints follows from this verdict.

## 3. Rounded rectangle: HOLD የተከበበ አራት ማእዘን

The proposed full phrase is genuinely attested, exactly and non-fuzzily, at `svx:127` for Rounded rectangle. Related command forms occur at `ui:17190`, `ui:20470`, and `ui:24056`. The phrase is not falsely presented as a new composition. Attestation is high-confidence; adequate idiom and semantic precision remain unestablished.

The required referent is specifically a rectangle with rounded corners. `PaintDocument.kt:31` maps the label to ROUND_RECT; `PaintCanvas.kt:411` clamps cornerRadius between zero and half the shorter drag-bound dimension, then calls `addRoundRect` with equal x/y radii. The radius control at `ClassicPaintActivity.kt:779–781` changes that parameter and invalidates the preview. Zero radius is permitted and yields the unrounded limit; the name describes the tool's configurable family, not a guarantee that every resulting shape has visibly curved corners.

The modifier የተከበበ can invite an encircled, enclosed, or surrounded reading rather than unambiguously denoting corner rounding. This is a substantive interpretation risk, not proof that all native readers would find the phrase wrong. Additional context in the same primary snapshot supports caution: `help02:370` uses the spaced form የ ተከበበ ቅርጽ for “closed shape.” The same corpus's use of the modifier for rounded callouts does not eliminate that ambiguity. The broad base phrase also needs to identify the intended rectangle precisely in the complete caption.

Keep HOLD until a qualified native reviewer confirms the full phrase in the actual rounded-corner tool context, or supplies a source-supported, independently checked complete alternative. Ask them to distinguish a rounded-corner rectangle from a merely closed/enclosed rectangle. Do not carry over acceptance of a separate Rectangle translation, and do not construct an accepted phrase by inserting ቀጤ ጎነ አራት.

The independently viewed JGraph catalog has `rounded=ክብ ጠርዝ`. This is a possible component-research lead only: it is not the full English source string, its consumer chain was not investigated here, and concatenating it with a Rectangle term would require a new review. No replacement string is approved by this report. Confidence is high that the hold is warranted, not high that one particular replacement is correct.

## Shared live-consumer chain

`values/strings.xml:168,308,341` contains the three exact English captions. They are absent from the supplied Amharic resource file. `PaintDocument.kt:29–36` resolves the enum labels through `ui(labelId)`. `UiText.kt` routes resource text through the locale-aware resolver. `ToolCategoryButton.kt:16–17` includes all three under INSERT. `ToolButton.kt:11` uses each label as visible text, contentDescription, and tooltip; `ClassicPaintActivity.kt:493–497` attaches selection and help behavior. `chooseTool` at lines 732–736 calls `PaintCanvas.selectTool`; the canvas paths and document renderer then establish the relevant shapes.

The labels also feed the options heading (`ClassicPaintActivity.kt:750`), help label-plus-hint (`:496`), normal status interpolation (`:689`), and selected-tool category accessibility text (`ToolCategoryButton.kt:27–28`). Accepting a caption does not approve those larger templates, hints, pronunciation, layout, or spoken delivery.

## Source links and additional corroboration

- [Pinned AN-Paint geometry consumers](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L406-L449).
- [Pinned AN-Paint drawing dispatch](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L272-L286).
- [Pinned LibreOffice shape-object terms](https://github.com/LibreOffice/translations/blob/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po#L127-L281).
- [Pinned LibreOffice drawing help](https://github.com/LibreOffice/translations/blob/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/02.po#L253-L378).
- [Official LibreOffice Amharic help, additionally viewed](https://help.libreoffice.org/latest/am/text/shared/02/01140000.html): confirms the two headings and open/closed Polygon convention; this is supplementary live-page corroboration, not another independent translation authority.
- [Official JGraph/draw.io Amharic catalog, additionally viewed](https://github.com/jgraph/drawio-i18n/blob/dev/dia_am.txt): ellipse, polygon, and rounded entries are recorded in `supplementary-evidence.json`. This is an unpinned archived-project branch page, not a newly hashed primary snapshot and not part of the original 52-record seal.

## Boundaries and stopping condition

No English source defect is established by this review. If a source defect is later established, correct the English source, flag affected terms across languages, and review each translation rather than silently compensating in Amharic. No English string, Amharic string, repository file, production artifact, Work task, app build, CI job, or release was changed or started by this review. Temporary review files only were created.

No human native-reader check, runtime/rendering check, screen-reader check, accessibility certification, geometry-quality certification, exhaustive terminology survey, or whole-language certification is claimed. The unresolved work is a qualified native full-phrase judgment for Rounded rectangle. The two retained caption values do not depend on resolving that separate hold.
