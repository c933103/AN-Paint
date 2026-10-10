# AN-W04: translated gallery controls are clipped by fixed rectangles

## Confirmed defect and baseline

At PR #29 `afbb8015130dd82546a4c22a9d3337782f7b995f`, four actions shared equal
widths and fixed 48 dp heights. Back/search used another fixed 48 dp row. API30/35
native-host evidence at 320×640 dp and real system 2× text shows French “Modi”,
“Crédi”, “Term”, incomplete Latin Hakka labels, clipped Tibetan/Dzongkha search
hints, and Mongolian/Manchu glyph fragments. The persistent SVG status itself
fits in those portrait captures. This is a separate defect from absent vertical
prose rendering; passing the old status check did not accept these controls.

Reproduce using French or Latin Hakka and system font scale 2.0: open the Commons
gallery and inspect the four document actions and search controls. SVG rejection
makes the status/control distinction clear but is not required to trigger clipping.

## Bounded repair

- Naturally measure native buttons and wrap horizontal action rows when necessary.
- Keep the previous text sizes; never shrink, ellipsize or replace full labels.
- Keep native 48 dp minimum touch targets and ordinary Button accessibility.
- Give vertical native labels the accepted shared caption renderer, with full
  horizontally scrollable columns and the same script/direction policy.
- Give search the full available width and natural multiline height. It remains
  Android's editable field, accepts the same query, and retains Search IME/action.
  Vertical locales additionally display the existing search label in columns with
  `labelFor`; the edit buffer itself is not converted to a noneditable caption.
- Scroll the complete native controls area when needed, preserving 120 dp of
  WebView where available, or one third of very shallow windows. A newly shown
  status is brought to its start. Full portrait status visibility remains required
  when it fits; larger content must have demonstrated scroll reachability.
- Remove the nested fixed-height vertical description scroller. Only orthogonal
  column rails are nested inside the main vertical controls scroller.

The shared controls apply across all offered catalogues, including ordinary RTL,
bundled-font languages and fallback strings. No resources, translation values,
font binaries, provider navigation rules, image parsing or credit semantics change.
No new translation key is required: the visible vertical search caption reuses
`ui_search34` / `ui_search_english34` in their existing search-label context.

## Regression plan implemented in source

`GalleryControlsLayoutTest`: every offered catalogue, API30/35, real 1×/2× system
font scale, 240/320/640 dp widths. Actual control factories must retain all label
characters without ellipsis/height clipping; actions cannot overlap; buttons keep
48 dp minimum targets and click/accessibility semantics. Search hint and entered
long query both receive intrinsic-height checks.

`GalleryControlReachabilityTest`: real gallery Activity with French, Latin Hakka,
Arabic, Nôm, Tibetan, Dzongkha, Mongolian, Manchu and Literary Chinese. Normal and
large portrait, large narrow portrait and large landscape configurations cover
all native actions (including retained credits), native search/IME, editable and
label accessibility, scroll-to-rectangle reachability, simultaneous visibility
where a full view fits, horizontal-column versus vertical-parent touch gestures,
a visible WebView viewport, repeated existing actions and Done. French/Mongolian
also rotate the same live Activity in both directions, checking reflow without
replacing the WebView, native search field or entered query. PNG/JSON outputs
are kept under `build/reports/gallery-controls` before later assertions.

The existing `CommonsSvgErrorReadabilityTest` portrait full-status assertions are
unchanged. `GalleryVerticalStatusTest` covers all five shared vertical profiles,
including both test-only directions, with real SVG failure messages and repeated
first-column reset. Existing parser/no-substitution/no-credit checks remain.

## Verification status before CI

Source and regression tests are prepared in an isolated checkout based on PR #29.
No Android SDK or Gradle distribution is available in this executor. Native-host
and installed-device results are pending and must not be represented as passed.
Physical-device gestures, keyboard behavior, TalkBack and fluent-language review
remain distinct from native-host test acceptance.
