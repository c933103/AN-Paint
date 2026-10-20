# Swedish extended catalogue

This change adds 350 formerly missing typed entries, including the complete crop
plural, and repairs eight existing labels. Independent model-based wording
review also covers the 16 unchanged previously unreviewed entries. The 340 prior
bounded accepts remain exact-source-bound; they are not newly rereviewed.

The 374 newly reviewed current-source entries comprise 334 with direct production
call-site context and 40 source-semantic-only entries. Coverage is 715/717 typed
entries; bounded wording acceptance is 714/717. Neither number certifies installed
rendering, TalkBack, native-speaker fluency or whole-language completion.

The complete eight-paragraph assembly Help uses the exact English source merged
by PR #122 and the unchanged independently reviewed Swedish proposal. Its later
source-binding supplement is a mechanical author check, not a new linguistic review.

## Remaining explicit limits

- `ui_main23` remains present as `Huvud` but unaccepted. It has no production
  caller establishing what “Main” names.
- `ui_foreground_background_colour_palette` remains absent. No production caller
  establishes the role of its third argument.
- The dormant legacy full manual remains absent until its English source is
  corrected for Commons, Exact position and conditional gap-closing behavior.
  Its full English/Swedish proposal is preserved with the review evidence.

These limits are not reasons to withhold unrelated reviewed active workflows.
All P2 entries now have direct Swedish resources. App-owned Commons diagnostics,
gallery credits, page/PDF/TIFF controls, colour slots/ranges, cursor/magnifier
controls, tool hints and the active Help text have complete Swedish proposals
accepted within the bounded review. Provider-authored titles or error details
remain provider text; proper names, technical identifiers and licences are not
misrepresented as English fallback.

## Tests and evidence

The compact fixture binds complete critical messages, actual control references,
plural forms, placeholders, technical literals and the named holds. The host
coverage check discovers current source identities, rather than freezing 717 as
an eternal count. Existing per-family fixtures and Android fallback oracles now
explicitly include reviewed Swedish only; the older 59-locale baseline is not
silently relabelled as whole-language acceptance.

`SwedishExtendedWordingTest` checks compiled messages, all 12 real Commons reason
branches, singular/plural crop controls and cancellation, exact-position errors,
state preservation and permitted overlap, and PDF/TIFF page-chooser controls.
The page chooser is invoked directly with no staged decoder input, so it does not
claim file decoding. The updated existing Help test includes Swedish through the
actual File Help and Other images routes. The assembly Activity test opens the
real Swedish Help toolbar action and compares its complete displayed text without
changing the assembly. Hosted JVM, lint, APK and installed
checks remain required; the local Gradle wrapper could not download its
distribution because the network was unreachable.

Full source/target/context decisions, corrected manual proposals and the
independent review receipt are preserved in the [immutable evidence record](https://github.com/c933103/AN-Paint/blob/cb3b384c69ca999ad3de95aa677a149f84c6360f/swedish-completion-20261020/CURRENT.md),
not duplicated throughout the application tree. It distinguishes the original
independent review from the later exact-source binding and records actual test
outcomes. The current normal host suite passed 1,055 tests; the focused Swedish
wording checks passed 22 tests. Hosted JVM and installed checks are not implied.
