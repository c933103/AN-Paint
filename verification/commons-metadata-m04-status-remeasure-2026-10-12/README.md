# M04 status-remeasurement candidate

This successor of `d5fb31f6cb1562eecba51e5ccff9b118a7e71714` makes two bounded corrections:

- Use `this.text` in the native before-control, fixing the confirmed Kotlin shadowing compilation error.
- Request layout after replacing the API35 horizontal status message, so TextView's fixed-width/same-height shortcut cannot bypass the existing glyph-inset measurement.

The installed regression first settles the actual `GlyphBoundsStatusView`, replaces it with different same-height Arabic COPY/INSERT messages, requires production to change its layout-request state from false to true, and waits for ordinary traversal. It then retains the unchanged strict complete-reference/actual pixels, full text, accessibility and line coverage. No test-forced measurement is used for this installed regression. Native reset checks also require the setter to schedule measurement. All wording, fonts, zero-pixel thresholds, old evidence and test identities are preserved through exact inverse projections.

## Evidence and pending gates

- [Failed predecessor checkpoint](https://github.com/c933103/AN-Paint/tree/94b91c4eb04d856853e29bdf7c90c61d52405bff/verification/commons-metadata-m04-glyph-bounds-ci-2026-10-12): JVM compilation failed; no JVM/render execution. Installed API30 passed95/95; API35 had101 pass, one failure and two missing. Each enlarged Arabic route lost one alpha1 pixel. It remains failed.
- [Frozen authoring checks and independent review](https://github.com/c933103/AN-Paint/tree/82bd9bc0e8e4c7a47784fa157a22e2bd9b52c72c/verification/commons-metadata-m04-status-remeasure-2026-10-12) retain exact source pins, full logs, corruption controls and incomplete aggregate receipt.
- Writer focused135+135 and independent118+118 passed. The full frozen local suite is incomplete:407 methods passed before the unchanged240-second cap, exit124;719 discovered. No Android SDK was available locally.
- Required fresh hosted inventory:892 JVM identities;112 original captures;28 diagnostics;181 complete-reference/actual triplets;72 rejected native overflow/clipping mutations; API30 scheduled95 and API35 scheduled104; both source-bound same-height natural-update records and strict Arabic pixels. The expected-gates file records expectations at publication, not test success.

Only these eight source/control paths, this short report and compact pins are added by this successor. New raw logs and independent reviews are kept on the dedicated evidence branch. Existing bulky historical evidence is not silently migrated or deleted. This candidate remains stacked on PR52 at `71f4d288669858e7975ec4c094b7f47a9a1ff145`; fresh hosted checks and exact-head review are required before acceptance.
