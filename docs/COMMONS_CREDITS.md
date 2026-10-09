# Commons attribution and gallery lifecycle (PR #20)

The gallery retrieves file-specific attribution from Wikimedia Commons `imageinfo` / `extmetadata`, rather than using the Commons site footer or assigning every upload one licence. The API's original upload URL must match the selected original; a download redirect to a different original is rejected. The API request itself does not follow redirects.

The retained snapshot includes the title, artist(s), creator/source links, required attribution, licence name and URL, usage/permission text and copyright/restriction fields when supplied. HTML is converted to text without loading it. Safe HTTP(S) attribution links are preserved. Metadata can be incomplete; the Commons file-page link and existing reminder to check that file's requirements remain part of the credit. Missing fields do not become an invented author or CC0/CC-BY-SA licence.

`Copy credit` on a Commons file page retrieves metadata only, without downloading the artwork or associating a source with a drawing. An import obtains and persists the snapshot before returning a result. The editor passes its file-specific credit to `PaintDocument.paste()` with the decoded bitmap; successful insertion associates both in one operation. Cancellation and metadata/decoder errors cannot associate an unused source. Retained document credits copy offline. Later imports do not overwrite the drawing's custom edited credit text.

The imported credit records AN Paint's conversion/white-backing operation. Source-only copying does not claim an import or modification. SVG handling still uses the document's declared original dimensions, with no canvas-size substitution, size prompt or silent shrinking; normal raster import remains supported.

## Lifecycle

`MediaGalleryActivity` now handles orientation, screen-size and keyboard-hidden changes without recreation. Downloads/rendering, WebView state and open credit fields survive those changes without another provider request; header and credit-dialog sizing adapt. This addresses Codex discussion `4213568191` even though the old SVG size chooser has already been removed.

For an actual activity recreation, the accepted base's durable `CreditEditSession` retains the selected source and unconfirmed text, including an empty field. Restoring that draft does not overwrite the saved credit. The existing Copy, Save, Done and source-switch actions accept edits through the same session/archive validation as other gallery providers. Cancelling a draft leaves the saved credit unchanged and does not reopen it after another recreation. This is not a guarantee of resuming an in-flight download after process death.

Gallery results retain the opaque session token and the editor's existing ownership checks. An independently accepted credit edit is preserved even if a later Commons import fails. Metadata-only copying does not accept a draft or claim an image transformation.

## Integration with the current default branch

The repository's default and PR target is `develop`. The 9 October integration merges `3f8bb0f64cfad485a1e725223d3475d8d60f9e5b`, including the already merged PR #15 credit/session architecture and PRs #21–#24. Those accepted changes are preserved. Draft PR #19 and its independent commits are not merged or copied into this branch.

This supersedes the original PR's global-credit-library description. Commons now follows the current base's per-document credit, export-panel and recovery behavior; embedding attribution into every exported file format is not claimed. Six unused strings describing the removed SVG size chooser are removed, and the live Commons labels retain the existing catalogue completeness gate.

## Checks

The previous PR head `1f27bec7c318c93aabb5b1c6f75a8f61653cd5fb` passed all three jobs in [workflow 37717543582](https://github.com/c933103/AN-Paint/actions/runs/37717543582). That run predates this conflict resolution and does not establish the integration result. The updated PR records the new source snapshot, local checks, review and CI outcome separately.

Integration regressions use document ledgers and real session tokens, preserving metadata-only copying, offline credit copying, original SVG dimensions, hard edges, opaque raster backgrounds, empty and multilingual drafts, cancellation and reinsertion. Additional failures cover decoder rejection without association and an accepted credit edit surviving a failed Commons download.

The host watchdog diagnostic fixture now uses its existing genuinely hung child instead of an immediate exit 124. The immediate-exit fixture could finish between `TimeoutExpired` and the process scan, making its assertion about killed processes race on a busy host. Cleanup also includes the known positive `Popen` child PID even when an executor's `/proc` view omits it; every signal retains the exact owned-session check. A deterministic regression covers that omission and retained diagnostics. Production emulator deadlines and the separate immediate-124 failure test are unchanged.

Historical local checks on 2026-10-08: **88 Python host tests passed**, no failures or skips. The Node-backed adapter contract contributes **35 assertions** for original SVG/raster actions, encoded/index file pages, thumbnail/archive/host rejection and mutation idempotency. `git diff --check` passed. A stub DOM contract is not an Android WebView runtime test.

Added **14 Robolectric tests** across `CommonsAttributionTest` and `CommonsCreditFlowTest` for metadata matching/retention, safe links, absent fields, copy-only behavior, actual gallery-result-to-editor insertion, offline copying, rotation during a blocked download, empty/multilingual draft recreation, reinsertion and failure cleanup. Existing original-size/raster gallery tests now use local metadata fixtures. The source-menu regression now explicitly includes Wikimedia Commons as the fifth entry.

Added **3 installed Android tests** in `CommonsCreditDeviceTest` for the real WebView's SVG/raster credit actions and the native HTML parser/attribution store. Fixtures block network loads. Android compilation, Robolectric, lint and installed execution are reported by CI, not inferred from local host checks.

Baseline head `29281a9`, workflow `37711392421`: universal APK/source and API 35 jobs succeeded; 302 unit/Robolectric tests ran with one failing old four-entry source-menu expectation. That baseline does not verify the new code or tests.

## API references

- https://www.mediawiki.org/wiki/API:Imageinfo
- https://www.mediawiki.org/wiki/Extension:CommonsMetadata
