# AN Paint 0.0.29 — language and cursor corrections

Package `paint.anpaint.android`; version code 82. The user clarified Tai Nüa
(`tdd`): its native name and five sourced action labels replace the mistaken
`tai` collection choice, with saved-preference migration. See the translation
audit in `translations/README.md`: regional Spanish and Korean still share base
catalogues, and all non-English editor translations remain partial.

Mongolian language radio alignment now retains the native CheckedTextView
padding. Both Ainu scripts are selectable: `ain-Latn` and `ain-Kana`, with
sourced Brush/Save/Done terms and migration of the old `ain` preference.
Cursor drawing directly adapts Paintroid's brush-sized circle/square overlay,
alternating crosshairs, activation dot and cumulative travel detection. Its
circular magnifier samples the cursor and defaults on, with adjustable zoom.
See `translations/README.md` and `docs/CURSOR_UPSTREAM.md` for provenance.

The final source, including Tai Nüa, passed release workflow 34914389654:
75 host checks, 255 release regression tests, zero app lint issues, 76 Android
API 30 tests and 77 API 35 tests. All passed. The universal release APK is signed
with the existing upgrade certificate; package, version, non-debuggable manifest,
four ABIs and 16 KB ZIP alignment are verified. Its embedded source ZIP matches
the separate source archive and all 788 exported repository blobs.

Source commit: https://github.com/c933103/AN-Paint/commit/01681570c448824a32039473bede5ae9591795c9
Build and checks: https://github.com/c933103/AN-Paint/actions/runs/34914389654
Release: https://github.com/c933103/AN-Paint/releases/tag/v0.0.29

APK SHA-256: `97de3f95832c560b20fe39b46e78e2f15658a8ba73d0a7c2a5c76871c905d940`
Source ZIP SHA-256: `0ed0526a5c91fdb3ceb0629743f5925431bf47e3e765e36a93dfa20ef16b64df`

The checked-in release request publishes this exact signed APK with corresponding
source, checksums and verification evidence. The private signing key and build
backup remain outside GitHub. Earlier results below describe 0.0.28 only.

---

# AN Paint 0.0.28

Package `paint.anpaint.android`; version code 81. Universal, non-debuggable release
APK, signed with the existing certificate to update 0.0.27 and earlier compatible
installations. Minimum Android API 21; target API 35.

## Changes and review

PR #1's one-catalogue translation consolidation preserves all 4,867 existing
strings. Its merged build, lint, regression and Android 35 checks passed.
The review found and fixed missing starter coverage, a Save label that fell back
to English in the unsaved prompt, and inaccurate starter vocabulary. Ainu and the
Tai collection remain offered with English fallback. Partial starter translations
still require native-speaker review; automated tests do not certify their quality.

The Mongolian language option now contains only its native name and `[mn-Mong]`.
The two joined words occupy adjacent vertical columns. The complete name and code
fit the actual menu row in portrait, landscape and at enlarged text size.

The release build also corrects Kvazaar's C dialect and HEIF file-offset flags on 32-bit Android.
Existing image formats, editing features and earlier colour/zoom fixes remain.

## Completed verification

- 75 host checks passed, including generation, release gating and exact APK signing-patch round trips.
- 10 local language/layout tests passed; local release lint has zero issues.
- Release APK and both instrumentation APKs compiled locally for x86_64.
- CI release regression: 251 passed; release lint: 0 issues.
- Android 30: 76 instrumentation tests passed.
- Android 35: 77 instrumentation tests passed.
- Universal ABIs: arm64-v8a, armeabi-v7a, x86_64 and x86.
- The remote tree matched before building. All 781 exported repository blobs
  match their Git objects; four pinned native source trees are also included.
- The APK embeds the identical corresponding-source ZIP. Signature, package,
  version, non-debuggable manifest and 16 KB ZIP alignment verified after signing.

Source commit: https://github.com/c933103/AN-Paint/commit/30968c60299d05cf4dd2335e8e1b887c4cf66209
Build and checks: https://github.com/c933103/AN-Paint/actions/runs/34794257334
Release: https://github.com/c933103/AN-Paint/releases/tag/v0.0.28

APK SHA-256: `f154728854af0be1c8bb62d4908fde75f4b082a9c7e2bc1aab217ce2819e5c1c`
Source ZIP SHA-256: `0c7481d566eb35a6daefaceaef4d35c72cb5f1061f901b9f394f768bbd8157f2`
Signing certificate SHA-256: `f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`

The private backup contains the APK, source, original signing key and final
verification reports. Keep that backup private; GitHub receives only public
release assets and public signature/alignment bytes, never the key.

Snapshot: 2026-09-14T01:25:39.390893+00:00
