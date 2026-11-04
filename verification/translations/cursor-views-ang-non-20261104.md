# Cursor drawing and magnified views: Old English and Old Norse

Base commit: 78c4c4ce870f9f35cba392f442aebc94dc0b0a82.

Adds 20 previously absent P2 strings to each offered `ang` (Ænglisc) and `non` (Norrœna) catalogue. Independent semantic review accepted all 40 unchanged. The batch covers cursor-mode enable/disable, drawing start/stop, pan/tap guidance, x/y position, shape, marker size and settings; pixel-grid show/hide and label; magnifier and enlarged-preview captions.

The current cursor-options panel, drawing-toggle callback, View commands and coordinate-status consumer were inspected. Enabling cursor mode stays distinct from starting a stroke. Guidance preserves the pan-then-draw and tap-to-stop sequence, and separately describes positioning the cursor before tapping the drawing button. Tapping the cursor itself starts or stops drawing. The size label identifies the visible cursor marker, not the painted brush width. Existing round/square labels are reused by the cursor shape picker. Grid display retains the 800%-or-greater threshold. No full-screen, toolbox or fit-to-view translation is included, and detailed cursor help outside this P2 block remains separate.

Validation passed:
- Exact English and target base Git identities; offered picker entries; XML parsing and duplicate-name checks; exactly 20 additions per locale; all 390 previous entries, attributes and surrounding bytes unchanged.
- Android escaping/formatting, source attributes and exact typed placeholders/newlines. The x/y identifiers and ordered `%1$d`/`%2$d` arguments are unchanged. Literal `(800%+)` and `(%)` retain source `formatted="false"` attributes.
- Duplicate Disable captions are identical; the two enlarged-preview captions differ only by the source ellipsis. Mode enable/disable vocabulary remains distinct from drawing start/stop.
- 78 host tests: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery.
- Structural catalogue validation passed for all 171 offered options. All 1,276 materialized tracked base files matched their Git blob identities and executable modes. The 159 unmaterialized research/verification documents are retained unchanged in the publication tree and were not needed by these checks.

Each locale changes from P2 47/305 to 67/305, leaving 238 P2 keys absent. P0 remains 94/94, P1 249/249 and P3 0/71. These are direct-key-presence counts, not whole-catalogue quality ratings. The priority manifest is unchanged.

Vocabulary follows existing drawing, settings, pan, tap, preview and magnification resources. Pointer, drawing-button, magnifier and grid terms are authored technical adaptations. They are not claimed historical computing vocabulary or full-sentence attestations.

Limits: no historical-language specialist certification, whole-catalogue linguistic acceptance, Android build, device/rendering check or CI result is claimed. Canonical Android resources own current wording; this evidence is not a wording freeze.
