# Preserve the actual soft-keyboard Search action

[Final configured Code review P2](https://github.com/c933103/AN-Paint/pull/30#discussion_r4230957670)
at `9bbfad58ff8a8784240a12db4ec96085c030fc05` identified a gap in the original
listener-only test. Full CI at that head was green, but its test called
`onEditorAction()` directly and did not inspect what the keyboard receives.

Android's TextView input-connection implementation unconditionally adds
`IME_FLAG_NO_ENTER_ACTION` for multiline input. Thus merely setting
`IME_ACTION_SEARCH` on the wrapping query field does not preserve the intended
soft-keyboard action. This shared field affects every offered language.

- [API30 TextView input connection](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-11.0.0_r1/core/java/android/widget/TextView.java#L8685-L8688)
- [API35 precise multiline branch](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/TextView.java#L10057-L10060)

The gallery field now retains the real native EditText connection and clears only
that conflicting flag after the superclass populates EditorInfo. Text still wraps,
the field remains editable, native hint/labelFor semantics and live accessibility
text remain, and no label/font/translation resource changes are needed.

## Regression

- All-catalogue native tests inspect actual EditorInfo with both an empty field and
  a long query that must wrap. They require IME_ACTION_SEARCH and no
  IME_FLAG_NO_ENTER_ACTION, alongside the unchanged full layout/accessibility checks.
- Real Activity tests invoke Search through InputConnection.performEditorAction,
  then verify the production Commons search URL retains the query. This replaces
  the shortcut that called the listener-facing TextView method directly.
- The installed French/Mongolian test uses a long multilingual query that must
  wrap in portrait and landscape. It inspects the real connection and EditorInfo
  in each orientation and logs query line count, input type and IME options.
  All real window/browser/font/cleanup checks and deadlines remain.

This verifies the Android keyboard contract rather than claiming physical-device
or every third-party keyboard testing. The new P2 stays unresolved until the
corrected exact head passes CI and fresh configured reviews.

The preceding green CI receipt is preserved independently at source head 9bbfad5;
its passing tests are not represented as coverage of this newly discovered gap.

Local combined validation: 326 Python tests passed in 51.107 seconds, zero
failures/errors/skips (`logs/host-python-search-ime.log`). Android native/installed
EditorInfo assertions require fresh exact-head CI before resolving the finding.
