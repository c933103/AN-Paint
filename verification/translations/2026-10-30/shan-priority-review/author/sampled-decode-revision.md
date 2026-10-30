# Author correction before independent acceptance

`sampled-decode-revision.tsv` supersedes only the sampled-decoding clause of the batch-F candidate for `ui_sampled_resize_memory_explanation`. It does not silently edit historical F bytes or create another key for credit.

On rereading `ImageImport.kt:ImportPlan.create`, `sample` starts at 1 and is increased only while the power-of-two sampled dimensions remain at least the target dimensions. It can remain 1 even when final scaling produces a smaller output. Therefore my first paraphrase, decoding to fewer pixels, was too absolute; the revised clause says decoding **that can reduce pixel count**. No execution/test was used or needed to identify this source-level linguistic issue.

The surrounding clipboard/canvas/buffers, variable actual memory, lost detail in the smaller copy, and unchanged original remain identical. Independent review must assess whether the functional sampling paraphrase is sufficiently clear. If not, hold this one clause rather than accepting a false guarantee of reduced decoder memory. The batch-F review's lower-pixel sampling explanation should be read with this correction, not as a claim that every sampled decode uses fewer pixels.
