# Independent review of repaired PR18 screenshots

Decision: **accept the bound API35 capture-state evidence**. All 32 original PNGs were opened individually. All eight format-popup screenshots visibly show an open native popup, including the previously stale en-XV landscape capture. No capture-state blocker remains in this exact artifact.

## Evidence binding and independent checks

- Head: `66c39ca345ef7bc8c5fe1da8ce64cb872c3a0e88`
- Tested merge: `f2162094bec001f13970ae7cf79621aec94c6e3a`
- Tree: `a90cdf84be34e6a08ab7a9d25b46cdce2f71b776`
- Run: `38022416053`, attempt 1; API35 job `114127351184`; artifact `11659005722`
- ZIP SHA-256: `cbb0326a2ce6a5e25325bb2fbdc6844d4bb0ac7f99d3eec3ffbbd77a894e0577`
- ZIP digest verified; every PNG matches both ZIP bytes and the receipt hash/size/dimensions. All 32 fully decode and are unique both bytewise and by decoded RGBA pixels. Production screenshot verifier passed.
- All 98 installed XML cases independently checked: 74 native, 18 ordinary app, 4 vertical, 1 seed, 1 verify; no failed/error/skipped cases. Production 24-method app phase-union verification passed against the reviewed source inventory.

The repaired en-XV landscape popup hash is `012ff064658059aba3420efd909aee308656318e6f9a387ff5e205a17a5da11d`; closed Save is `8232cf80c376769ed71f47da68e89de2c2399fc9235ac033188c793fadabf5ca`. The actual format-list overlay is visible, so the distinguishing pixels are meaningful popup content, not just a clock change.

## Bounded acceptance

Workspace images show the retained canvas and selected Arrow state; initial Save images show closed forms; all popup images show an open list; JPEG-quality images show quality controls in their current viewports. Per-image observations and hashes are in the accompanying JSON receipt.

Horizontal clipping and partial/offscreen neighboring columns remain visible. In particular, the Manchu landscape JPEG slider thumb is partly cut by the right content-viewport boundary. Several portrait quality labels/readouts or filename/help columns are also partial. This evidence does not establish full-range slider reachability, entirely visible controls or broad usability acceptance.

Manchu-shaped connected runs, upright Chinese glyphs and rendered emoji are observable within these captured viewports. That is not linguistic, all-string or all-glyph certification. This review applies to this API35 emulator run only, not API30 or physical devices. Earlier failed captures retain their failed classification.

No source or remote state was changed during this review.
