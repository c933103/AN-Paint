# PR55 b0697 actual delivery and platform-binding defect checkpoint

Source b0697fd58a2a37fb94e351f4c4ec68757b0f6b5e; tree b5d8cbeac9bf6d613ed7c3be787aa984826daafd; synthetic merge e3dc717586539f8bbfe2ae3e3aae87e83db16d19; run38296205283.

All five CI jobs completed successfully. Independent runtime review and archival replay are recorded separately as they finish. This checkpoint preserves a genuine additional compiled-artifact finding: all167 picker/platform XML entries are correct, but the actual application manifest omits android:localeConfig. The same compiled manifest was present in accepted predecessor6d603. This is a pre-existing platform registration gap, not a loss of the27 new catalogue files.

Exact official AGP8.13.0 dependency sources explain the result: manifest-merger31.13.0 applies STRICT_MAIN_OR_OVERLAY_MERGING_POLICY to localeConfig, rejecting a library-only attribute. The current app module has no declaration, while the Paintroid library does. This run's actual merger report was not retained; the version-bound rule plus actual source/APK observations support the diagnosis. No runtime override was found; actual system Settings UI was not inspected.

The accompanying independent delivery proof includes current compiled XML/manifest parsing, corresponding-source and font/legal checks. Keep the platform binding failure explicit even though existing CI passed. A separate reviewed successor will add the app-level declaration and a real installed framework LocaleConfig check without changing offered tags, wording, fonts or rendering guards. The correct Codex HANDOFF81-to108 finding will be corrected with it. Fresh compiled and installed proof remains required for that successor.
