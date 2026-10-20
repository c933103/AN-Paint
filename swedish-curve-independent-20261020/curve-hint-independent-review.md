# Independent review: corrected Swedish Curve Help hint

Decision: ACCEPTED, bounded to this one complete pair and actual production context. No wording revision required.

Reviewed source: `ad3ef6d9e1e44b364a65188a6d20235f68eb16c8`. Correction: `cafb244e8bd8342926d5696ce63a67860cb9b9ad`. PR #151 merge: `f0705a33c6f5aa3bc1e4020eef5f0a3ea1d3e6a6`. Exact English and Swedish values, attributes and string-file blob IDs match all three snapshots.

English: Drag a line, then drag twice to set its two bends. Finish curve commits it early.

Swedish: Dra en linje och dra sedan två gånger för att ställa in dess två böjar. Med Avsluta kurva kan du slutföra kurvan innan båda böjarna har ställts in.

English UTF-8 SHA-256: `4b55a4e7bd81aa9b32c8639026a36758fc8895f8922766e7e67eb41ae6b3a8c9`

Swedish UTF-8 SHA-256: `fc85a5cabd8f0c1c09cb299cfbe13569b6166bc38a4bb14c9bd2a617002e207e`

Canonical pair SHA-256: `428968ac6c080238de14444efa5e2667de57f4a08b889f5a09ae50f9b4e8f5b1`. Serialization is defined in the accompanying JSON.

## Why accepted

The complete target preserves the line and two-bend gestures, names the real **Avsluta kurva** button exactly, and describes optional completion before both bends are set. **slutföra kurvan** means finish the curve and removes the misleading attachment meaning of **fästa**. It does not promise saving a file.

The actual Curve Help button displays this hint. Finish curve calls `applyPending()`, which commits the current path and resets the curve state. Zero/one completed bends correspond to internal `curveStage` **1/2**, not 0/1. Internal stage 0 has no pending curve. The second bend increments to stage 3 and auto-commits. The existing regression source covers early completion, repeated apply and undo/redo; I read it but did not execute it.

## Scope and limits

This is an independent, model-based, complete-pair review, with high confidence in semantic and action correspondence and moderate-to-high confidence in the short Swedish sentence's grammar and clarity. It is not native-speaker, whole-language, installed-layout, TalkBack, runtime, build, CI or release certification. The original independent receipt is unchanged; its superseded fästa target is not carried forward. Three unrelated Main/palette/full-manual holds remain. No other entry is newly accepted here.

The specific no-new-independent-review qualification for this corrected hint may now be replaced by this bounded acceptance. A 714 total would be the prior 713 plus this one entry, conditional on the other prior bindings remaining valid; this review does not newly certify that inventory.

The JSON includes full source bindings, exact values and hashes, detailed semantic reasoning, implementation references, preservation statements and confidence limits.
