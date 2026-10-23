# Method, schema and limits

Fresh production and current resource bindings use Git blob SHA-1 plus raw-file SHA-256. Canonical scope: 716 strings + one plural container = 717 containers / 718 quantity/string leaves. Strings use full decoded XML itertext UTF-8 without appended newline. Plural container hashes use sorted-key compact Unicode-preserving JSON; canonical quantity leaves are separate. The three translatable=false filename constants ui_an_paint_assembly_png, ui_an_paint_recovery_zip, ui_an_paint_source_zip are excluded. Configuration arrays are not translation-string units.

Important hash distinction: historical source/target hashes in original-receipt-recovery.json are SHA-256 of compact JSON-serialized values, including JSON string quotes. Current raw UTF-8 hashes are explicitly named separately. Equal complete values were verified before comparing these separate encodings.

canonical-unit-hashes.json defines all 717 identities once. Each option-ledgers entry enumerates every present canonical target hash, an explicit S override for cursor help, and default U for every other canonical resource, present or missing. The exact set difference supplies missing containers; the absent plural accounts for two missing canonical leaves. No missing value receives an English localized hash. English-identical is not automatically untranslated or reviewed. Presence is independent from quality.

The original shared receipt explicitly includes both scripts, so one bounded report may preserve both separate rows. Its independent source trace does not establish independent linguistic reviewers, native-speaker fluency or exhaustive grammar. S is not I and is not a new linguistic acceptance. No adjacent hint, entire composed message, current device execution or whole-language completion is inferred.

Own original source a6b5956b0ae8f8082fafc2ff21d63e337f3a85af is compared to current5bfed632. Complete function/enum/control scopes are compared, with exact hashes and only the necessary tooltip substitutions enumerated. Whole-file differences remain acknowledged. Runtime dependencies and rendering are not recertified by byte equality.

Original source/assertion filenames are locators only: this task ran no app tests/builds/generators/CI and changed no app source. Records branch is non-production and must never be merged into app branches. Existing snapshots/comments are append-only. Next step is recover own independent linguistic scopes and source/translation coverage for remaining U units, without manufacturing credit from related scripts or fallback.
