# App platform-locale binding repair

Frozen successor: `dc1ba97dacc573ead73729297eb739ecb244dcf5`.
Base: public `b0697fd58a2a37fb94e351f4c4ec68757b0f6b5e`, tree `b5d8cbeac9bf6d613ed7c3be787aa984826daafd`.

The application module now binds the existing `@xml/app_locales` resource. The existing API33+ installed app-language test reads the framework configuration, requires `LocaleConfig.STATUS_SUCCESS`, and compares count and exact tag membership against the current target-app picker resource. It logs status and the complete expected/actual tag lists before assertions. API34+ explicitly ignores dynamic locale overrides; the API33 path uses the constructor. Existing language-switch assertions remain unchanged. This does not claim Android Settings UI visibility.

The only other change is the previously frozen HANDOFF fallback count correction from 81 to 108. No resources, font assets, wording, locale registrations, workflow or deadlines change. All 1,094 source leaves remain present; 1,091 are exact in bytes and executable modes. See `source-diff.patch` and `candidate-tree.json`.

## Verification scope

- `source-and-inventory.json`: live-source tag/manifest scope and exact identity deltas, with full current JVM and installed inventories in companion JSON files.
- JVM declarations remain 684 methods / 910 SDK-expanded execution identities, with all JVM source bytes unchanged.
- Installed identities remain 74 native and 30 app. API30 selects 73 native + 22 app; API35 selects 74 native + 30 app. API30 still suppresses the API33+ method; no phase or budget changes.
- `focused-normal.log` and `focused-optimized.log`: current language additions/contracts and app instrumentation matrix host checks. These do not execute Android framework code.
- `git diff --check` passes. No full host aggregate was launched here; aggregate coordination belongs to the parent.

No local Android SDK, Kotlin compiler or device is available. Android compilation, the new installed assertions and independent compiled application-attribute inspection require the fresh matching hosted build. The old APK remains a verified failing baseline for the missing compiled binding; its packaged locale XML is not successor proof. The independent reviewer owns exact AGP merger diagnosis and fresh compiled-attribute evidence. No current in-progress hosted run was cancelled or replaced here.

API reference: https://developer.android.com/reference/android/app/LocaleConfig
