# AN Paint translation handoffs

Translation owns meaning, terminology, and language review. Deliver each batch as text keyed by locale/resource and pin the exact English source. Include uncertain wording and context notes explicitly. Do not wait for GitHub Actions or encode Android XML as part of writing or reviewing translations. A handoff is usable once wording is accepted, even if a previous batch is still building.

Integration owns Android resources, escaping, placeholders in the resource file, tests, PRs, merges and releases. Take a pinned wording handoff, verify the source hasn't drifted, and preserve approved wording. Return any meaning conflict to translation rather than silently rewriting it. Track drafted, wording-accepted, merged and runtime-verified counts separately. Do not call CI or automated code review language acceptance.

Existing locale assignments are unchanged. The first handoff preserves the already-drafted Chamorro wording for text, colours, image assembly and memory. The prior resource branch is an integration candidate only. This evidence branch isn't intended to merge into the app.
