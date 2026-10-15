# Missing external-link handler is reported as a gallery network failure

**Current status:** A bounded implementation is prepared on merged develop `0aa6c89c9d3a4d133a8b231e7002783b60ead46d`; see the [fix, resource scope and verification limits](../gallery-external-link-handler.md). Exact-head Android compilation and runtime checks remain pending. This tracker stays open until its acceptance gates are met.

**Original diagnostic status (before the prepared fix):** Open shared source-context diagnostic bug; documentation-only tracking PR. No fix is applied. **Baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`. Independently reviewed static paths and complete English/French/Japanese values; no runtime/provider/native incident, outage or security vulnerability is claimed. Faithful translations share the source mismatch. [Board](https://github.com/c933103/AN-Paint/pull/39) · [French review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182795516) · [Japanese review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182776352).

## Expected and actual at the original baseline

Expected: when Android cannot find an app to open the external Terms link, the user receives a link-opening/handler explanation.

Actual: `openExternal` catches `ActivityNotFoundException` from `ACTION_VIEW` and displays “The online gallery could not be loaded. Check your connection and try again.” Missing external intent handling does not establish a gallery load or network failure.

Impact: in that failure condition, users are directed to check connectivity instead of the external-link handler. No missing browser or provider outage was observed in this static review.

## Static path and evidence

- [Terms action, MediaGalleryActivity.kt L112](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L112) passes the provider's terms URI to `openExternal`.
- [openExternal L298–300](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L298-L300) launches `ACTION_VIEW` and maps `ActivityNotFoundException` directly to the online-gallery/network resource.
- `ui_the_online_gallery_could_not_be_loaded_check`: [EN L424](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L424), [FR L484](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L484), [JA L532](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L532). The text may remain appropriate at genuine gallery-loading call sites; this is a selection/context defect.

## Bounded fix and acceptance

- Use a truthful external-link/handler error at this catch, retaining existing network/gallery messages where supported. Do not infer a connectivity problem from this exception.
- Exercise the actual Terms/ACTION_VIEW launch with a missing-handler test double or supported environment configuration and verify the correct message without opening a network bypass.
- Include successful external launch and actual gallery load-failure controls, preserving each purpose and existing UI state. Keep this separate from any permission/security exception classification not established here.
- Enumerate all uses of the selected resources and update/review all affected locale values and fallback behavior if new text is needed.
- Complete focused intent/message regressions and current-source review/testing; no handler installation, permission or system-setting changes are part of this fix.

## Original tracker next action

Repair the bounded exception-to-message mapping and verify the actual launch/error branch. Preserve Terms destinations and gallery behavior. No application/resource/test edits, runtime results, merge or release are made by this tracker.
