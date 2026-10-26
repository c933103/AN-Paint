# Swedish remaining-P1 messages

This bounded change adds 148 complete messages that were absent from the exact
Swedish catalogue at develop `0134e79c588a027bbd239f7685fff52b0771819f`.
No previously present Swedish value or other locale is changed.

An independent model-based review accepted each complete English/Swedish pair:
134 accepted messages have production call-site context; 14 have source-semantic
review only. These distinctions are retained in the current wording fixture.
The final import warning uses “bilddata som Base64-text”.

The legacy `ui_foreground_background_colour_palette` remains absent and falls
back to English: no current caller establishes whether `%3$s` is an action,
state or descriptor. This is the single remaining direct P1 presence gap.
The pre-existing `ui_main23` uncertainty is unchanged. Presence, structural
parity and bounded model review do not certify native-speaker acceptance,
whole-Swedish completeness, installed layout or TalkBack behavior. Earlier
withdrawn review conclusions are not restored.

The [immutable review evidence](https://github.com/c933103/AN-Paint/tree/57e4e46ac965940149c4b337e9da2c5754fd204b)
contains the full source-bound author packet, independent per-entry decisions,
accepted values and structural receipts. Bulky evidence stays outside the
application tree; routine tests do not download it or reconstruct past source.

`swedish_remaining_p1_wording.json` binds every complete English and Swedish
message, attributes, positional format arguments and escaped newlines. Host
regressions reject truncation, markup, missing/duplicate messages and altered
format contracts. Context checks distinguish import failure from success,
original-image retention, canvas/image crop bounds, foreground/background
gestures and the actual navigation names in guidance.

`SwedishRemainingP1WordingTest` checks all compiled accepted resources and the
held English fallback. It exercises numeric-entry errors, cancel/apply behavior
and the distinct foreground/background edit targets. Authored tests are not
executed results: the PR reports local host checks and exact-source hosted JVM,
lint, APK/resource and API35 results separately.

Focused checks:

```sh
python3 -m unittest discover -s tools -p 'test_swedish*wording.py' -v
./gradlew --no-daemon --max-workers=1 :Paintroid:testDebugUnitTest --tests org.catrobat.paintroid.local.SwedishRemainingP1WordingTest
```

Run both final host aggregates from `CI.md`. This change does not authorize a
merge, deployment or release.
