# Requested rationale-only correction

Independent review found that the batch-C Pencil rationale mistook a stale `one_pixel` key name for behavior. The current English resource value says crisp edges at any selected width, and PaintDocument.kt uses `pencilWidth` for PENCIL. The rationale in `batch-c.tsv` is corrected accordingly; **the source, candidate `ၵမ်ၸိုၼ်း`, attributes and all other rows are unchanged**. `review-c.md` already said only 'crisp line' and is unchanged.

A/B remain byte-frozen. No new linguistic acceptance or technical test is implied.
