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

Release verification is in progress. The final signed APK report will be recorded after build and packaging checks complete.

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
