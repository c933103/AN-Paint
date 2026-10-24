# Amharic geometric drawing-tool captions

Three missing live captions for independent review, not accepted additions. Rounded rectangle carries a tentative author terminology HOLD; it does not yet change the prior adjudicated hold total. Prior 88 ready and 13 held proposals remain separate; zero implemented; production 12 present / 705 missing of 717 translatable containers.

## string/ui_ellipse

English: Ellipse

Proposed XML: `<string name="ui_ellipse">"ኤሊፕስ"</string>`

Drawing tool caption selecting ELLIPSE. Opposite drag points define sorted RectF bounds; shapePath uses Path.addOval. Preview/commit draw that path using current outline/fill style.

Qualification: Shape ellipse/oval, not punctuation ellipsis, elliptical selection or text effect. Circle is possible with equal bounds but source is not renamed Circle. Label selection alone does not draw; actual pointer gesture commits. No pixel/rendering certification.

Evidence and confidence: {"key": "ui_ellipse", "english": "Ellipse", "value": "ኤሊፕስ", "confidence": "high exact-source lexical support; medium idiomatic accessibility; draft only", "composition": "None. Exact whole-word non-fuzzy LibreOffice drawing-object and drawing-command translation.", "source_contexts": ["STR_ObjNameSingulCIRCE", "GenericCommands.xcu / .uno:Ellipse / Label", "GenericCommands.xcu / .uno:BasicShapes.ellipse / Label"], "behavior_fit": "An ellipse drawn inside a dragged bounding box. The exact geometric term preserves Ellipse, not a generalized egg shape.", "alternatives": [{"value": "ኦቫል", "confidence": "source-attested for Oval, not an exact Ellipse translation", "note": "LibreOffice Effects motionpath-oval. Broader shape term; not preferred over exact Ellipse support."}], "review_hold": "Native reviewer should judge familiarity and UI register. No native acceptance or visual fit test is claimed.", "consumer_context_from_parent": "Source uses addOval within the drag bounds; original English Ellipse unchanged."}

## string/ui_polygon

English: Polygon

Proposed XML: `<string name="ui_polygon">"ፖሊጎን"</string>`

Caption for multi-vertex POLYGON tool. Points build a line-connected path; closePolygon controls closure. Finish or qualified double-tap applies pending path. Closed mode dispatches POLYGON; open mode dispatches LINE and has no interior fill irrespective of shapeStyle.

Qualification: Keep English tool name Polygon, not silently Polyline or always-closed promise. It is a tool supporting closed/open configuration, not a guarantee every intermediate gesture is a mathematical nondegenerate polygon. Existing Close/Finish polygon controls and hints excluded. No English defect established solely from optional open mode.

Evidence and confidence: {"key": "ui_polygon", "english": "Polygon", "value": "ፖሊጎን", "confidence": "high exact-source lexical support; medium idiomatic accessibility; draft only", "composition": "None. Exact non-fuzzy whole-word translation in svx drawing objects and help drawing tools.", "source_contexts": ["STR_ObjNameSingulPOLY", "shared/02/01140000.xhp / hd_id3155308", "GenericCommands.xcu / .uno:Polygon / Label (Polygon, Filled)"], "behavior_fit": "Names the source Polygon tool. AN-Paint may leave the multi-vertex path open when Close polygon is off. Preserve the English label rather than renaming it Polyline; document that behavior separately.", "alternatives": [{"value": "ጎነ ብዙ", "confidence": "unverified native-form terminology possibility; no primary exact pair established in this task", "note": "Not promoted to a supported candidate. Requires authoritative mathematics source and native review; do not substitute based on compositional intuition."}], "review_hold": "Native reviewer should check loanword familiarity; the open-path behavior is a contextual caveat, not permission to translate Polygon as Polyline.", "consumer_context_from_parent": "Polygon can dispatch LINE for open mode, with no interior fill. Original English Polygon unchanged. Context supplied by parent, not independently inspected by lexical researcher."}

## string/ui_rounded_rectangle

English: Rounded rectangle

Proposed XML: `<string name="ui_rounded_rectangle">"የተከበበ አራት ማእዘን"</string>`

Caption selecting ROUND_RECT. Drag bounds feed Path.addRoundRect with equal x/y radius clamped to0..half the shorter side. Radius option changes document.cornerRadius and invalidates preview; shape can approach ordinary rectangle at zero radius.

Qualification: Rounded corners, not rotated rectangle, circle, enclosed/surrounded rectangle or arbitrary quadrilateral. Exact source-product translation presence alone cannot establish idiomatic reading; earlier Rectangle acceptance does not transfer to the full phrase. No new radius/units/hints acceptance.

Evidence and confidence: {"key": "ui_rounded_rectangle", "english": "Rounded rectangle", "value": "የተከበበ አራት ማእዘን", "confidence": "high exact-source attestation; low-to-medium idiom/semantic confidence; terminology HOLD, draft only", "composition": "Exact full phrase in LibreOffice STR_ObjNameSingulRECTRND, not newly composed. However exact-source status is not quality approval. The modifier may be read as encircled/surrounded, and the base phrase is broader than precise rectangle terminology.", "source_contexts": ["STR_ObjNameSingulRECTRND", "GenericCommands.xcu / .uno:BasicShapes.round-rectangle / Label (Rectangle, Rounded)", "GenericCommands.xcu / .uno:Rect_Rounded_Unfilled / Label"], "behavior_fit": "Rectangle with rounded corners controlled by a radius setting, not a circled or rotated rectangle. This exact semantic distinction needs native review.", "alternatives": [{"value": "አራት ማእዘን: የተከበበ", "confidence": "exact non-fuzzy UI source, same semantic caveats", "note": "Attested for Rectangle, Rounded in two LibreOffice commands; changes order, not the underlying wording concern."}, {"value": "የተከበበ ቀጤ ጎነ አራት", "confidence": "low, unattested composed alternative; not recommended for acceptance", "note": "Substitutes previously reviewed but unapplied Rectangle candidate. That earlier review does not approve this full phrase and does not resolve the rounded-modifier concern. A native reviewer may instead prefer an explicitly rounded-corners paraphrase; none is forced here."}], "review_hold": "Keep terminology HOLD until a native reviewer confirms rounded corners and the complete phrase. Do not inherit whole-phrase approval from the earlier Rectangle review.", "consumer_context_from_parent": "Source uses addRoundRect with radius clamped to half the smaller side; zero radius allowed. Original English Rounded rectangle unchanged. Context supplied by parent, not independently inspected by lexical researcher."}

## Shared consumer chain and limits

All three keys map to PaintTool enum labels, feed live INSERT tool buttons, options headings and indirect help/status/category accessibility text. ToolButton supplies visible text, contentDescription and tooltip; makeToolButton selects the tool; PaintCanvas handles the geometry and PaintDocument draws/commits. Complete current files are supplied rather than enum-only evidence. Review of names does not certify the larger templates or hints, spoken delivery or runtime rendering.

Ellipse uses addOval within dragged bounds, not ellipsis punctuation. Polygon supports closed and open mode; open mode uses LINE, with no interior fill irrespective of fill option. This existing configuration is disclosed rather than silently changing the English tool name. Rounded rectangle uses addRoundRect with clamped corner radius, including zero; its idiom must indicate rounded corners, not merely enclosure. Prior Rectangle acceptance is not transferred to this complete phrase. No English defect established for this bounded scope.

13 complete project copies are bound to freshly retrieved develop commit 66be61df27c5359bffc32d56db21f3949899f873 / tree 870c5a584120d92710be516af0dc3b3847b183d9. Three exact resource references are enum mappings; indirect consumers are separately identified above and in consumer-context.json. Historical discovery was rebound to current complete bytes, not a fresh exhaustive repository search. Primary lexical copies, exact records, alternatives and confidence retain their source provenance and reuse limits.

No placeholders/units/ellipses in these names. Longer shape hints, Close/Finish polygon controls, radius and fill-style wording are excluded. Prior Palette uncertainty, Swap hold, fill/calligraphy and all other holds remain. No human native-reader, runtime/rendering, accessibility, geometry-quality or whole-language certification. No Work task, production edits, app builds, CI or release.
