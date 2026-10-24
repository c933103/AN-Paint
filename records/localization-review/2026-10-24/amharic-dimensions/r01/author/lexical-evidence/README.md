# Amharic dimension controls: lexical author drafts

2026-10-24. Eight original, unaccepted drafts for independent review. This is lexical evidence and static source analysis, not production implementation, native acceptance, a build, a runtime test, or a release gate. No Work task, CI, release, or remote publication was performed by this task.

## Drafts

| Exact resource key | English | Original Amharic draft |
| --- | --- | --- |
| ui_pixels | Pixels | ፒክሰሎች |
| ui_percent | Percent | ፐርሰንት |
| ui_pixels_6ec9c2 | pixels | ፒክሰሎች |
| ui_percent_fd8671 | percent | ፐርሰንት |
| ui_width | Width (%1$s) | ስፋት (%1$s) |
| ui_height | Height (%1$s) | ቁመት (%1$s) |
| ui_width_in | Width in %1$s | ስፋት በ%1$s |
| ui_height_in | Height in %1$s | ቁመት በ%1$s |

All eight have author_status=review. That means a reasoned original candidate is ready to be examined, not that its wording is accepted. A reviewer may retain, revise, or hold any value. In particular, exact noun evidence is not independent approval of the original accessibility compositions. No prior60 addition or held Lock proportions/aspect-lock wording is included.

## Why these choices need distinct checks

1. AOSP Gallery2 directly attests ፒክሰሎች in the 13M pixels and 4M pixels strings. This is the selected plural spelling family, consistent with prior reviewed terminology. It is NOT an invented normalization of LibreOffice ፒክስሎች. The latter standalone spelling and the alternate UI ፒክስልስ are retained as distinct source records. The candidate noun is an original extraction from an attested plural component, not an exact AOSP standalone Pixels label.
2. LibreOffice directly pairs Percent with ፐርሰንት. AOSP separately attests native መቶኛ and በመቶኛ forms. The selected loanword is a contextual editorial choice; the native alternative is neither suppressed nor declared wrong. Do not silently mix the two unit families across selector and accessibility resources.
3. AOSP image-details directly pairs Width with ስፋት and Height with ቁመት. LibreOffice graphics independently supports ስፋት but uses እርዝመት for Height. Prefer the exact image-details height noun while preserving the genuine alternate. A native reviewer may reasonably choose the other family.
4. English uppercase/lowercase variants remain four distinct keys. Amharic has no corresponding case contrast, so equality of the selected strings is permissible, not a reason to merge keys. The lower-case resources are bare unit nouns. They must NOT contain በ, which the accessibility template supplies exactly once.
5. The full accessibility templates are original moderate-confidence compositions: noun first, then attached በ plus a unit argument. Primary prose attests in pixels/in percent with በ, and AOSP has an attached unit preposition in “Set duration in seconds.” These records support components and spacing choices; they do NOT attest the complete Width/Height in templates, guarantee idiom, or establish screen-reader naturalness.
6. The full positional placeholder %1$s is preserved exactly once in each of four templates. Visible Width/Height parentheses are unchanged. Static substitutions in interpolation-cases.json enumerate all eight results, including the two unit branches for each accessibility label. No rendered or spoken test was run.

## Consumer semantics checked

The actual supplied DimensionControls.kt was inspected, especially lines 30–35, 53–69 and 74–86. Visible labels substitute literal px or %, while accessibility labels substitute the separate translated lower-case noun keys. It preserves canonical pixel dimensions across unit changes and applies a percentage to each respective original dimension.

The actual ImageCropDialog.kt and NormalizeImagesDialog.kt callers were also inspected. Shared Pixels/Percent selectors cover crop margins and normalization as well as dimension controls. Crop values are relative to each applicable image dimension; normalization percent uses the largest current selected axis. Thus the shared unit labels must not incorporate a single denominator. NormalizeImagesDialog also uses the parenthesized Width/Height templates with literal px for accessibility. The labels name dimensions/units, not metric lengths, DPI, area, screen dimensions, or actions.

Source freshness and complete consumer bindings are in the parent dossier. This lexical task verified the supplied English XML bytes against its SHA-256 and Git blob and checked each exact key, value, and attribute. It did not independently fetch the current production head.

## Files and provenance

- draft-candidates.json contains the eight required objects: key, english, draft, rationale, confidence, limitations, author_status, plus exact source attributes, evidence record IDs, status and alternatives.
- exact-records.json contains 16 exact records with full PO records or paired Android XML records, line ranges, contexts, flags, attributes, and immutable URLs. Positive PO records are nonempty and nonfuzzy. Nonfuzzy does not itself guarantee linguistic quality.
- sources.json identifies nine full snapshots with local_source_path, immutable URL, SHA-256, byte count and reuse provenance: eight external primary snapshots plus current project English XML.
- english-source-records.json records each selected canonical English XML element and its attributes and hash.
- interpolation-cases.json lists eight full static substitutions, not runtime test results.
- search-limits.json records the bounded corpus, excluded claims, consumer distinctions, and two unsuccessful fresh web-open attempts.
- validation.json records byte/key/placeholder checks only.
- SHA256SUMS seals all package files other than itself.

All external snapshots were reused from the previous same-day text-geometry packet. Every complete file was copied, hashed again, and matched to its recorded provenance. Two web opens of immutable LibreOffice URLs returned cache misses and no source bytes. This was a generic retrieval failure, not a verified access denial. No successful fresh fetch or current-web validation is claimed.

Full source snapshots preserve their upstream headers and licenses. Terminology reuse does not imply upstream endorsement or native-language acceptance. This bounded corpus is not an exhaustive Amharic dictionary search. There is no claim that an unattested whole phrase does not exist elsewhere.
