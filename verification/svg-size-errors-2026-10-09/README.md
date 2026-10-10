# Two SVG original-size errors: scoped source-assisted draft

The current draft has **two default resources and 118 proposed values across all
59 scoped catalogues**. The unchanged scoped completeness gate now passes locally.
The other **81 offered catalogues remain incomplete** and retain normal fallback;
no English-filled overrides were added. These are source-assisted proposals,
not native-language, script-layout, screen-reader or physical-device acceptance.
The PR remains draft pending fresh-head review and CI.

Analysis base: `5bf82b67199aaecbd341a8b150a887f8d60b5567`.
Publication base: merged #28, `4b615ce2d9e27814df84812b90858b5f676ce51a`.
The six-pair revision followed `ea60a00001d766674cbd6b91da791894af5ea624`;
its language-picker changes remain untouched. This continues the bounded
[AN-W05-C01 inventory](https://github.com/c933103/AN-Paint/pull/20#issuecomment-6077456325).

## Runtime and meaning boundaries

`SvgOriginalSize` retains its finite/positive, ceiling and `Int.MAX_VALUE` checks.
A typed `IllegalArgumentException` subclass identifies the two reasons without
Android dependencies. The existing gallery display boundary maps only that type
to resources; unrelated provider diagnostics pass through unchanged.

- No usable original size is declared by the SVG; no canvas-derived size is used instead.
- Original dimensions exceed Android bitmap dimensions; no resizing occurred.
- The dimensional limit is separate from memory budgets and download byte limits.
- No resize must not become only no automatic shrink.

No parser condition, numeric limit, successful-import path, network host, provider
validation, cleanup, credit association or retained user edit changes. The latest
revision adds six resource pairs and exact test oracles. No production Kotlin file
changed after the initial two-reason extraction.

## Source-assisted composition review

The initial draft contained 48 pairs, the second revision 53, and this revision
adds `ain-Kana`, `ain-Latn`, `jje`, `mn-Mong`, `mnc-Mong`, and `ryu`.
Full-catalogue inspection found useful recorded-size, replacement and completed
negative constructions missed by the earlier narrow sample. Primary grammar,
dictionary and corpus evidence supports the composed clauses; no source is
represented as containing the entire technical sentence.

Independent review corrected Ainu verbal coordination in both scripts from
`hene ne` to `hene ki`. Okinawan now explicitly says usable with `ちかーりーる`
and uses the independently documented determination form `ちわみたる`.
The Mongolian, Manchu and Jeju candidates remain as proposed. Sources, scope,
case/argument analysis and remaining idiom/orthography uncertainties are recorded
in the self-contained review artifacts:

- [All current values and explicit other-81 dispositions](translations.json)
- [Six added exact values](research-v3/added-proposed-values.json)
- [Jeju independent review](research-v3/jeju-independent-review.json)
- [Other five independent reviews](research-v3/five-locale-independent-review.json)
- [Research index and publication hashes](research-v3/README.md)

There are no remaining uncovered clauses in these six pairs at this bounded
composition-review level. This is not native acceptance or approval of the rest
of any catalogue. The technical loan labels and long-clause naturalness remain
explicit fluent-review questions.

## Font support

The second revision added the supported Nôm character 豫 (U+8C6B) to the bundled
subset. All 735 old glyphs and 733 mapped codepoints, outlines, metrics and existing
metadata were preserved. Two independent outputs were byte-identical. The font
is still 275,312 bytes, SHA256
`797ac4ef00f0dd8a982d5216dbd78db3edda07b578b9f8642d0156add90bd526`.
No further font or inventory change is made in this revision.
[Preservation evidence](nom-svg-font-extension.json) and the pinned reproduction
wrapper remain available. The font helper has additional input-preservation unit
checks; they use only temporary fixtures and do not require fontTools in CI.

## Actual local results and pending runtime evidence

[checks.json](checks.json) records **321 host tests passed, zero failures, errors
or skips**, with the [latest complete log](host-tests-v4.log). Negative instrumentation
fixtures intentionally print simulated failure payloads; the unittest run itself
exits zero. All existing scoped completeness gates remain intact. XML,
placeholders, Android string syntax, font coverage/preservation and whitespace
checks pass. Global strict completeness still reports the separate 81 offered
tags, with 162 missing-resource/plural report entries.

The API30/35 Robolectric real-gallery tests exercise both actual download/parser
failure paths, independent exact wording, repeated attempts, cancellation/no
substitute dialog, cleanup/no credit association and external `%`/Unicode
passthrough. Amharic supplies a representative genuinely unfilled-catalogue
fallback; Manchu now has its reviewed exact pair.

New [readability checks](readability/README.md) use the real activity at 320×640 dp,
1×/2× system font scale, API30/35 native-rendered host graphics. Horizontal cases
assert full lines and ancestor visibility for long, RTL, Nôm, Tibetan and Dzongkha
messages. Mongolian/Manchu cases record explicit diagnostic PNG/JSON captures
without claiming vertical acceptance. These tests have **not run locally**: this
workspace has no Android SDK or Gradle cache. At c73ad1a, CI compiled and executed
them, but all four readability executions stopped at the 2× Activity-scale
precondition (observed 1×). Eight actual 1× French/Mongolian captures and full
JUnit results are [preserved here](readability/c73ad1a/README.md). The six real SVG
translation-error executions passed. Lint, APK/test-APK build and existing API35
device tests passed separately. The overall regression run failed (686 JVM tests,
four failures), so it is not a complete pass.

The revised fixture selects each scale through method-level `@Config` before
application/resources exist, instead of mutating scale with cached wrapped
resources alive. Production `fontScale=0f` preserves inherited configuration.
System/application/wrapper/Activity checks and actual glyph enlargement remain
required; no status text size is injected or assertion weakened. The revised
setup and its expanded capture matrix await fresh compilation/runtime evidence.

The SVG errors use persistent `gallery_status` text, not Toast. Android's two-line
Toast cap does not govern them. A separate **AN-W04 source- and host-capture-confirmed layout gap**
remains: this native status never receives the app's vertical renderer. A proper
failing regression candidate is isolated outside automatic source sets for that
separate fix. Capturing horizontal text in a vertical locale is not a vertical
readability pass. No production layout change is folded into this translation PR.

## Historical evidence remains historical

The [53-pair local snapshot](history/ea60a00-checks.json) and earlier logs preserve
seven scoped completeness failures before these six pairs were added. At that
head, [workflow 37914105355](https://github.com/c933103/AN-Paint/actions/runs/37914105355)
failed: 316 host tests, seven failures, two optional skips; JVM/lint did not run.
APK/source build and API35 existing device tests passed separately (74 codec,
14 editor, one credit seed and one restart test). The actual failed host log is
[losslessly preserved](ci-host-tests-ea60a00.log.gz). Those passes do not apply to
the latest test/resource revision.

The initial 48-pair snapshot and 16-failure evidence also remain preserved in the
[historical readme](history/ea60a00-README.md), original logs and manifests.
Earlier research text saying resources were unedited or a clause was blocked
refers to its dated research stage, not current counts. No historical acceptance
is revived. Fresh-head checks and root's integration decision are still required.
