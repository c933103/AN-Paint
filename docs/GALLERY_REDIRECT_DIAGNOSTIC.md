# Gallery redirect diagnostic

A redirect can be rejected by the complete image-URL policy even when its host
remains supported. The policy checks HTTPS, user information, port and provider
image paths/extensions as well as the hostname. For example, Wikimedia Commons
rejects its `thumb/` and `archive/` paths on the allowed upload host.

The message now says “The gallery redirected to an unsupported image URL.”
The historical `ui_the_gallery_redirected_outside_its_supported_hosts` resource
key remains stable. Default English and all 59 existing locale definitions are
updated together; the other 112 selectable locales retain their existing English
fallback. Wording expectations do not certify full catalogues or native idiom.

URL policy, explicit redirect handling, the redirect limit, status/result state,
cancellation and temporary-file cleanup are unchanged. No destination URL or query
value is interpolated into this diagnostic. This is a diagnostic correction, not
an observation that a live provider currently issues a rejected redirect.

`GalleryRedirectTest` exercises the production WebView-selection/download/status
path using controlled `HttpURLConnection` responses. Its cases cover same-host
thumb/archive paths, off-host targets, scheme, user information, port, extension,
allowed relative redirects after retry, the existing five/six-redirect boundary,
cancellation after a redirect and every selectable locale's compiled message.
The Python wording contracts separately cover complete resource values, exact
scope/fallback preservation, missing/duplicate entries and wrong-cause mutations.

Run the focused checks from the repository root:

```sh
python3 -m unittest discover -s tools -p 'test_gallery_redirect_wording.py' -v
./gradlew --no-daemon --max-workers=1 :Paintroid:testDebugUnitTest --tests org.catrobat.paintroid.local.GalleryRedirectTest
```

[Tracking PR #87](https://github.com/c933103/AN-Paint/pull/87) records the original
source-context defect. Authored tests are not executed evidence: use exact-source
CI results before claiming runtime acceptance. Live-provider behavior, installed
rendering and independent native-speaker review are separate from these checks.
