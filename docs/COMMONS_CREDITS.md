# Commons attribution and gallery lifecycle (PR #20)

The gallery retrieves file-specific attribution from Wikimedia Commons `imageinfo` / `extmetadata`, rather than using the Commons site footer or assigning every upload one licence. The API's original upload URL must match the selected original; a download redirect to a different original is rejected. The API request itself does not follow redirects.

The retained snapshot includes the title, artist(s), creator/source links, required attribution, licence name and URL, usage/permission text and copyright/restriction fields when supplied. HTML is converted to text without loading it. Safe HTTP(S) attribution links are preserved. Metadata can be incomplete; the Commons file-page link and existing reminder to check that file's requirements remain part of the credit. Missing fields do not become an invented author or CC0/CC-BY-SA licence.

`Copy credit` on a Commons file page retrieves metadata only, without downloading the artwork or adding an inserted-image entry. An import obtains and persists the snapshot before returning a result. Only the editor's successful `onInserted` callback records the source in the existing image-credit library. Cancellation and metadata/decoder errors cannot register an unused source. Retained credits copy offline. Later imports do not overwrite custom edited credit text.

The imported credit records AN Paint's conversion/white-backing operation. Source-only copying does not claim an import or modification. SVG handling still uses the document's declared original dimensions, with no canvas-size substitution, size prompt or silent shrinking; normal raster import remains supported.

## Lifecycle

`MediaGalleryActivity` now handles orientation, screen-size and keyboard-hidden changes without recreation. Downloads/rendering, WebView state and open credit fields survive those changes without another provider request; header and credit-dialog sizing adapt. This addresses Codex discussion `4213568191` even though the old SVG size chooser has already been removed.

For an actual activity recreation, an open credit editor saves its selected source and unconfirmed text in instance state, including an empty field. Restoring that draft does not overwrite the saved credit. The existing Copy, Save, Done and source-switch actions commit edits. Cancelling a draft leaves the saved credit unchanged and does not reopen it after another recreation. This is not a guarantee of resuming an in-flight download after process death.

This branch retains the pre-existing global source-credit library. It does not merge the separate per-document attribution/export/autosave changes under draft PR #19, and does not claim that every exported image format embeds these credits. That integration needs separate verification when those branches are combined.

## Checks

Local checks on 2026-10-08: **88 Python host tests passed**, no failures or skips. The new Node-backed adapter contract contributes **35 assertions** for original SVG/raster actions, encoded/index file pages, thumbnail/archive/host rejection and mutation idempotency. `git diff --check` passed. A stub DOM contract is not an Android WebView runtime test.

Added **14 Robolectric tests** across `CommonsAttributionTest` and `CommonsCreditFlowTest` for metadata matching/retention, safe links, absent fields, copy-only behavior, actual gallery-result-to-editor insertion, offline copying, rotation during a blocked download, empty/multilingual draft recreation, reinsertion and failure cleanup. Existing original-size/raster gallery tests now use local metadata fixtures. The source-menu regression now explicitly includes Wikimedia Commons as the fifth entry.

Added **3 installed Android tests** in `CommonsCreditDeviceTest` for the real WebView's SVG/raster credit actions and the native HTML parser/attribution store. Fixtures block network loads. Android compilation, Robolectric, lint and installed execution are reported by CI, not inferred from local host checks.

Baseline head `29281a9`, workflow `37711392421`: universal APK/source and API 35 jobs succeeded; 302 unit/Robolectric tests ran with one failing old four-entry source-menu expectation. That baseline does not verify the new code or tests.

## API references

- https://www.mediawiki.org/wiki/API:Imageinfo
- https://www.mediawiki.org/wiki/Extension:CommonsMetadata
