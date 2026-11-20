# Non-host redirect restrictions are reported as an unsupported host

**Status:** Open shared source-context diagnostic bug; documentation-only tracking PR. No fix is applied. **Baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`. Independently reviewed static paths and complete English/French/Japanese values; no runtime/provider/native incident, outage or security vulnerability is claimed. Faithful translations share the source mismatch. [Board](https://github.com/c933103/AN-Paint/pull/39) · [French review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182795516) · [Japanese review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182776352).

## Expected and actual

Expected: a redirect rejected by the complete image-URL policy is described as an unsupported image URL, or its actual rejected property is reported accurately.

Actual: the message “The gallery redirected outside its supported hosts” is selected whenever `allowsDownload` fails. That predicate also checks scheme, user-info, port, path and extension. A redirect staying on `upload.wikimedia.org` but entering the disallowed `/wikipedia/commons/thumb/` path can therefore produce a false outside-host diagnosis.

Impact: the user receives the wrong reason for a safely rejected redirect. The rejection itself should remain; this is not a request to loosen URL policy or evidence that any real provider currently makes such a redirect.

## Static path and evidence

- [MediaGalleryActivity.kt L319–330](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L319-L330) validates each URL in its redirect loop using `allowsDownload` and chooses `ui_the_gallery_redirected_outside_its_supported_hosts` for every rejection.
- [IllustrationSource.kt L15,L22–35](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L15-L35) requires HTTPS, no user-info, allowed ports and provider-specific image paths/extensions; Commons rejects thumb/archive paths even on the allowed upload host. [Raster extensions L46](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L46) add another non-host condition.
- Resource values: [EN L419](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L419), [FR L479](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L479), [JA L527](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L527).

## Bounded fix and acceptance

- Prefer a neutral unsupported-image-URL explanation or accurately classify each rejected property. Reviewed neutral candidates: EN “The gallery redirected to an unsupported image URL.”; FR “La galerie a redirigé vers une URL d’image non prise en charge.” Review all affected localizations.
- Exercise the actual redirect loop with controlled responses: same allowed host/disallowed path, off-host redirect, disallowed scheme/port/extension, and an allowed redirect. Preserve redirect limits and complete URL checks.
- Assert the message does not claim a host change for same-host rejection. Do not log or expose secret/query values in diagnostics.
- Preserve cancellation, temporary-file cleanup and failure state; run focused policy/redirect-message tests without contacting or depending on live providers.

## Next action

Implement a message accurate for the full predicate, verify controlled redirect cases and current-source review/test gates, then re-review changed locale values. Distinct from external-link handler and native-decoder errors. No policy relaxation, live-provider observation, app/resource/test change or runtime acceptance is made by this tracking PR.
