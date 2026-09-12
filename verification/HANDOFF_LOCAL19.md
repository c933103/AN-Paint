# AN Paint local.19

Updated 12 September 2026. Package `io.github.c933103.anpaint`, version
`2.14.1-local.19`, version code `72`. Uses the existing AN Paint signing identity.

## Completion of earlier requests

- Replaced the remaining legacy UI colours with shared Material Design 3 roles,
  including the tool drawers, editor chrome, assembly and dialogs. Actual image
  pixels and selected drawing colours retain their original values.
- Completed translation readiness for advanced RGB/HSV/HSL component labels,
  localized numeric input and assembly placement status.
- Magnifier-scale changes now redraw and autosave while the editor remains open.
- Gallery downloads now honour cancellation through the posted result, close
  connections and remove abandoned temporary files. Added full download-to-insert
  tests covering image pixels, transparency and source attribution.
- Rechecked the earlier tool, selection, canvas, format, assembly, font, credit
  and original-editor consolidation requests. See REQUEST_COMPLETION.md for the
  complete mapping and EDITOR_PARITY.md for the original-view comparison.
- Corrected the asynchronous emulator startup readiness failure. APK/source
  delivery remains independent of long device checks under CI.md.

## Verification status

**Development build: verification is incomplete or contains acknowledged failures.**

APK compilation, package/version identity, exact corresponding source, licences/fonts/icons, all four native CPU architectures, 16 KB alignment and the local.18 upgrade signature passed verification.

| Check | Result |
|---|---|
| Unit/regression | passed; 183 tests |
| Android lint | passed; 0 errors, 0 warnings |
| API 30 native | not-run |
| API 30 installed app | not-run |
| API 35 native | pending |
| API 35 installed app | pending |

Only Ultra HDR is excluded from API 30 because it needs API 34+. No other test exclusion is applied.

Build source: [`1a840c70cc461bb3257f26eacecae07ab25906d1`](https://github.com/c933103/AN-Paint/commit/1a840c70cc461bb3257f26eacecae07ab25906d1).
[Asynchronous Android workflow](https://github.com/c933103/AN-Paint/actions/runs/34702846656).
The downloadable and in-app source ZIPs are identical snapshots of this build. This delivery status was generated afterward; it does not overwrite or claim results from another build.

The detailed JSON report records supplied artifact identities, available test outcomes and missing checks.

Physical-phone installation, ARM runtime execution and third-party sharing remain unverified.

The editor works and exports in opaque 8-bit SDR sRGB. High-bit-depth/HDR import conversion does not preserve HDR output. WebP supports at most 16,383 pixels per side.

## Remaining verification boundaries

No physical phone is attached. Physical installation/update, ARM runtime
performance, manufacturer picker behaviour, live gallery downloading and sharing
to third-party phone apps have not been verified on a phone. Deterministic gallery
regressions substitute the HTTPS transport and exercise the actual app path;
that is not a claim of live phone/network testing.

The working canvas and exports are opaque 8-bit SDR sRGB. Supported high-bit-depth,
wide-gamut and HDR imports are converted to that document format; see
CODEC_SUPPORT.md for supported colour models and format limits. No transparency
controls, layers or HDR output were reintroduced.

Dubai and the file labelled STC remain excluded under the public terms found.
The exact-file and upstream-history review is complete, but no additional grant
covering AN Paint has been established. This does not establish what permission
Catrobat relied on. See FONT-LICENCE-REVIEW.md.

Historical local.18 evidence is retained in verification/local18.json and
verification/HANDOFF_LOCAL18.md. Its counts do not describe this new build.


## Follow-up result, recorded during local.20 work

The API 35 job in [run 34702846656](https://github.com/c933103/AN-Paint/actions/runs/34702846656)
subsequently passed all 35 native/import tests (64.154 seconds) and all eight
installed-editor tests (37.24 seconds). The emulator script completed
instrumentation at 166 seconds. The pending entries above describe the original
delivery snapshot, not the eventual result. No test failure was acknowledged or
bypassed for local.19. API 30 was not rerun; physical-device testing remained
unperformed. These results belong to local.19, not local.20.
