# Gallery external-link handler error

Implementation for the bounded bug tracked by [PR85](https://github.com/c933103/AN-Paint/pull/85),
initially prepared on develop `e53b2e6aaaa9ac231cfdd38485e28ee9d638e870` and
rebased onto merged PR67 develop `0aa6c89c9d3a4d133a8b231e7002783b60ead46d`.
The six PR67 resource keys and its code/tests/workflow remain intact.

## Behavior

`MediaGalleryActivity.openExternal` still submits the same `ACTION_VIEW` intent
and URI to Android. Only `ActivityNotFoundException` now selects
`gallery_external_link_no_handler`: “Android could not find an app to open this
link.” The injected launcher permits exercising this branch without installing
or disabling a browser or changing device settings. Its production default is
the existing `startActivity` call.

The catch covers the actual Terms button and the existing external HTTPS
navigation route. It does not catch or relabel permission/security exceptions.
Provider Terms destinations, HTTPS/navigation/download policy and gallery state
are unchanged. The separate main-frame WebView load-error callback retains
`ui_the_online_gallery_could_not_be_loaded_check`; subresource failures retain
their existing no-status-change behavior. No provider outage or missing browser
has been observed or inferred from this source fix.

## Resource scope

The new key belongs to P2 because it is an operational error in a gallery workflow.
It adds one source identity. The merged progress denominator changes only when
the key merges; catalogue presence is not linguistic acceptance.

The target is default English plus the existing 59 scoped catalogues. The seven
ordinary English variants use the same sentence. The two synthetic/layout
options retain their existing English/emoji conventions. The 112 explicitly
outside-scope catalogues keep default-English fallback. Exact whole statements
are retained in `tools/fixtures/current_localization/gallery_external_link_current_wording.json`;
the current scoped/fallback identities remain in `locale_contract_scope.json`
beside it. No existing key-coverage assertion is relaxed.

Translation drafting and independent statement review are separate from native
speaker acceptance, whole-catalogue rechecking, font/rendered validation and
installed-device testing. Earlier withdrawn localization conclusions remain
withdrawn; this correction gives no completion credit to unrelated entries.
Ainu (`ain-Kana`, `ain-Latn`), Hakka PFS (`hak-Latn-TW`), Manchu (`mnc-Mong`)
and Okinawan (`ryu`) retain explicit whole-sentence idiom/attestation limits after
independent agent review. Key presence does not close those linguistic limits.

## Verification

`GalleryExternalLinkTest` exercises production UI/callback paths under
Robolectric on API30 and API35:

- Actual Terms clicks for all four providers, with exact `ACTION_VIEW` URI checks.
- A missing-handler launcher double, repeated attempts and localized EN/FR/JA status.
- Successful default `startActivity`, retaining the loaded gallery and search query.
- Actual main-frame versus subresource load-error callbacks, including a successful
  Terms launch after a gallery failure without clearing that independent status.
- Existing allowed-page and blocked non-HTTPS navigation, plus external HTTPS.
- A distinct `SecurityException` control, outside this catch.
- Whole compiled messages for every offered locale, with explicit English fallback.

`test_gallery_external_link_wording.py` checks whole resource values, complete
scope, explicit fallback, deliberate P2 classification and missing/duplicate/
wrong-cause negative controls. Host checks do not substitute for Android compilation
or execution of the new branch tests. Robolectric uses offline WebView and launcher
models; even a pass does not establish installed-device/browser behavior or a
provider network result. No app installation or system-security change is required
by these tests.

At preparation time local Android execution is blocked before compilation: the
Gradle wrapper cannot download its distribution in the current environment.
Exact-head hosted compilation, JVM/lint and applicable device results must be
reported separately before claiming verified completion.
