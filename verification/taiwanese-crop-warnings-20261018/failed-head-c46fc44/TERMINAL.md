# Terminal disposition of initial run39147690887

The initial run ended `cancelled` after corrected source head a2503197 was published. The unchanged repository workflow has `cancel-in-progress: true` for the same PR branch; this was a superseding-source cancellation, not an instruction or refusal from the user and not a retry.

- Regression tests and lint: failure (the preserved sole U+2A736 glyph failure among 1,144 JVM methods; lint itself passed).
- Build APK/source, exact-script generation, position emulator: success.
- Core emulator: cancelled during the later vertical phase.
- Final Emulator API35 composition gate: failure because core was cancelled.

The partial core archive's completed summaries report 74 native, 17 ordinary app, 3 gallery-draft, 12 dialog and 2 first-vertical methods passed. Later vertical/restart phases and mandatory capture collection do not form a complete receipt; no complete API35 union is claimed. `terminal-packet.zip` preserves final run/jobs/artifact metadata, the raw core job log and the exact partial core artifact (its GitHub SHA-256 verified). The earlier original failure packet is unchanged.

The corrected current head has a new normal CI run; no completed result is reused across source heads.

