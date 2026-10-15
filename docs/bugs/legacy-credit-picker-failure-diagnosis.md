# Legacy-credit export misdiagnoses arbitrary picker-launch exceptions

**Status:** Open bug; documentation-only issue-style tracking PR, not an applied fix. Keep open/draft pending separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Evidence boundary:** independently confirmed linguistic/static-source finding only; no runtime/device reproduction, CI or whole-language acceptance. [Project board](https://github.com/c933103/AN-Paint/pull/39) and [translation review](https://github.com/c933103/AN-Paint/pull/56) track related work. Issues remain disabled; visibility/settings are unchanged.

## Expected and actual

Expected: legacy-credit text export distinguishes a missing picker from Android blocking access or other launch failures. The recommendation to enable Files/Documents should be used only when a picker is actually unavailable.

Actual: the export action catches every `Exception` from launching `ACTION_CREATE_DOCUMENT` and displays `ui_android_could_not_find_a_file_picker_enable`. A `SecurityException` or other launch exception can therefore receive an unsupported “file picker missing” diagnosis.

Impact: users may be directed to enable an already-present Files/Documents app instead of receiving the appropriate blocked-picker or generic failure explanation. This is an error-classification defect; no security vulnerability or observed permission incident is alleged. Pending export state is currently cleared on failure and that protection must remain.

## Static path and evidence

- [LegacyImageCreditsActivity.kt L107–117](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/LegacyImageCreditsActivity.kt#L107-L117) sets `pendingExportToken`, launches `ACTION_CREATE_DOCUMENT`, catches broad `Exception`, clears the token and reports a missing picker regardless of exception kind.
- [ClassicPaintActivity.kt L1083–1092](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1083-L1092) provides a useful existing distinction: `ActivityNotFoundException` maps to missing-picker wording; `SecurityException` maps to `ui_android_blocked_the_file_picker`. Its OPEN_DOCUMENT fallback must not be copied blindly into a create-document export flow.
- Missing-picker resource: [EN L38](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L38), [FR L200](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L200), [JA L248](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L248). Faithful translations are not the cause.

Independent review receipt: [French priority batch 02](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182490731).

## Bounded fix and acceptance

- Classify launch failures narrowly: missing-picker text for `ActivityNotFoundException`; blocked-picker or truthful specific/generic text for `SecurityException` and other handled failures.
- Preserve clearing `pendingExportToken` for every unsuccessful launch and retain the requested create-document/text-export semantics. Do not bypass permissions or silently use another destination.
- Exercise ActivityNotFoundException, SecurityException and a representative generic failure at the actual legacy-credit export action; verify the correct message and cleared pending token.
- Keep successful launch/result handling, cancellation and safe subsequent retry working without stale token/export state.
- Reuse existing truthful localized resources where appropriate; independently review any new/changed values across all affected locales and verify placeholders.

## Next action and dependencies

Implement bounded exception classification with actual launch-action regressions, then current-source review/test gates. Re-review the affected resource's legacy-credit context before changing translation acceptance. Independent of the other new source-context bugs. No platform permission, picker behavior, application code or tests are changed by this tracking PR.
