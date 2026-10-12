# Measured glyph-start inset candidate

## Result and current limit

This is a source-bound **candidate**, with local host checks recorded separately.
The first two full ordinary host attempts hit the unchanged 240-second cap
(exit 124), and both also logged three historical projection-contract failures.
Their full logs and targeted tracebacks are preserved. The common projection
entry point was repaired through the strict successor inverse; no Kotlin or
pixel-acceptance code changed in that repair. Fresh checks are recorded in
`local-verification.json`. Neither timed-out attempt is a full aggregate pass. The final frozen-source
aggregate also timed out at 240 seconds, with no logged assertion failures;
it is incomplete. Expanded focused tests pass 128 normal and 128 optimized,
and independent checks pass 111 normal and 111 optimized. Hosted validation
must establish the complete result under the unchanged cap. A separate ten-method
supplement passes all nine unexecuted methods plus one conservatively replayed
warning-wrapped method; this does not convert the full timeout into a pass.
New Android compilation, native raster controls and installed raster evidence
are unrun locally because this checkout has no Android SDK. A new hosted run is
required. No earlier passing job or failed checkpoint certifies this source.
The existing `ci:full-android` opt-in selects API30 fallback and API35 coverage;
`expected-api30-identities.json` pins 95 scheduled API30 methods (22 app + 73 library), from 97 declarations
with the two API35 restart identities explicitly omitted,
while the API35 inventory remains 104. Workflow phases and deadlines are unchanged.

The third frozen checkpoint, [run 38250189049](https://github.com/c933103/AN-Paint/actions/runs/38250189049),
ran exactly 892 JVM identities from head `e7855e04a1a4647a1fae3a14937df0c17c3f4d79`,
tree `8752ed99c9350235da46fac1b4a188ca89296889`, synthetic merge
`9af58e46c6a7196ef90c60e345bcd7a5194ffacf`. 890 passed and two methods failed.
The enlarged Arabic COPY, INSERT and intact control each have two reference ink
pixels at content x=1232 outside width 1232, missing from the actual TextView.
Their alphas are 7 and 1. They are inside the physical view but clipped at its
text-content edge. The reference has no allocation-edge contact. This is real
Robolectric native ink loss, separate from the earlier Ainu advance-only mismatch;
it does not establish clipping in the earlier installed app.

`failed-painted-ink-run/` retains all 39 independently reviewed deliverables,
their frozen manifest, selected original PNG/JSON/XML and the separate root
pixel diagnosis. `historical-failure-binding.json` distinguishes all three
failed checkpoints. The first two are unchanged in prior history, including the
[immutable diagnostic record](https://github.com/c933103/AN-Paint/tree/746d41107b8251d2b288a62931da5c1e80810b08/verification/commons-metadata-m04-pr55-diagnostic-ci-2026-10-12).
None is relabeled as passing.

## Bounded production change

Only horizontal gallery status views on API35+ select the new status subclass.
Older APIs and vertical routes keep the original TextView. Fonts, wording,
resource catalogues, provider logic, accessibility text and action semantics are
unchanged.

The subclass explicitly uses glyph bounds for width and keeps global overhang
shifting disabled. Enabling width bounds alone was rejected as an established
RTL fix: Android15 still anchors a plain RTL line at the right content edge.
After native measurement, the subclass reserves a measured logical-start inset
using one standard, non-drawing paragraph margin over the complete unchanged
message. A standard margin moves each paragraph's own leading edge inward,
including right-to-left paragraphs. It never replaces glyphs or inserts text.

Android15's computed glyph box omits paragraph margin offsets. The box therefore
provides an **absolute** required inset; it is never repeatedly added to the
current inset. Up to three bounded native remeasurements are allowed, with a
2em maximum inset as a defensive production work limit. This is not a clipping
allowance: any remaining overflowing or missing ink still fails acceptance.
A new status message resets the inset. Width, native paint/font settings,
padding or direction changes reset measurement before recalculating. Repeated
measurement with unchanged inputs cannot accumulate padding.

## Exact reference and tests

The complete native Layout text must still equal the original message, with
contiguous UTF-16 coverage, no ellipsis and unchanged accessibility text.
The only newly supported drawing feature is at most one exact
`LeadingMarginSpan.Standard`, covering the complete text with exact flags,
equal first/rest margins and a positive bounded size. Replacement/custom spans
remain rejected. The view and Layout must agree on bounds-based width, and both
must have start-overhang drawing shift disabled. No implicit drawing-origin
shift is ignored.

Reference allocation expands the API glyph box by the actual known margin in
both directions, then unions every line extent and the complete layout box.
This conservatively covers per-paragraph LTR/RTL offset differences. Every
nonzero-alpha reference pixel is scanned; any allocation-edge contact fails.
The strict acceptance function is byte-identical to the prior painted-ink
successor: zero horizontal overflow, zero expected ink outside the actual view,
zero missing ink and exact whole-view ARGB equality. No tolerance, border mask,
alpha cutoff or cropped expected-image shortcut is added.

Native tests retain every prior identity and all 72 defect-specific real draw
mutations across English, Ainu, Tibetan, Arabic, Japanese and Nôm at scales 1/2.
They add an independent original plain Arabic before-control at identical native
width/text/font, which must reproduce actual overflow and loss. All six scripts
also exercise repeated measurement, narrower width, changed font size, mixed
paragraph directions, a new short message and restoration. The expected native
inventory is **181 PNG pairs/JSON records**, including all previous 120, 60 reset
cases and one original before-control, plus four summaries. This is an expected
inventory until the new source executes successfully.

The installed viewport method retains its original French and Mongolian checks,
then adds Arabic on API35 only. At actual installed font scale 2 and landscape
geometry it injects the exact COPY/INSERT M04 status texts into the real status
view and compares native software rasters against complete references at zero
tolerance. It records default TextView flags, actual view/Layout flags, density,
viewport, text/accessibility, source inventory and full PNGs. This is injected
actual status-view software-raster evidence, not a network-route or hardware
screenshot proof; the existing native local-fixture tests retain route coverage.

Two explicit `Instrumentation.addResults` keys carry the PNG/JSON records through
the already retained raw protocol. Each record is limited to 128KiB UTF-8 and the
whole Bundle to 512KiB of actual Parcel data. It emits no test status codes and
changes no runner behavior or deadlines. The independent stdlib-only decoder
binds the source/profile, verifies records/PNG hashes and dimensions, recomputes
all ink/ARGB counts, and separately requires the exact successful ordinary-app
partition. Malformed, missing, duplicate, truncated and false-success evidence
must fail. The complete installed audit still requires all 104 identities.

## Provenance and acceptance gate

The new pinned inverse fixture restores exactly seven changed baseline files.
All 2,008 predecessor leaves are unchanged or byte-exactly reversible. Historical
fixtures, failed evidence, fonts, catalogues, workflow phases and deadlines stay
unchanged. New live-source controls reject deletion, restoration of old bytes,
duplicated edits, corruption and unrelated content. Host-only source contracts
do not establish runtime convergence, compilation or successful pixels.

Before accepting this candidate, verify the exact publication/merge tree,
all 892 JVM identities, 112 original success captures, 28 normal-landscape
diagnostics, all 181 native raster pairs and four summaries, all 72 intended
negative rejections, and the complete 104 installed inventory with both source-
bound Arabic raster records. Confirm the two historical Arabic pixels survive
in the new complete/actual rasters and inspect the rendered result. A flag,
setter call, source token or partial receipt is insufficient.
