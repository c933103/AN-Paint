# Malay smoothing labels: new, bounded recheck

This records new work after the 28 September reset. It does not reinstate any
earlier completion claim or complete the PR3 semantic review. Register items
R-003–R-006 are the specific leads examined here.

At original PR3 head `df94e3fa89c782c03398d366dbc3ce01970d99fd` and integration
head `00e4429dbcf3ae485c88e448334e43474c1fb134`, the Malay XML contained:

| Resource | Before | Correction |
| --- | --- | --- |
| `ui_smooth_freehand_strokes` | Pakiniskan sapuan bebas | Licinkan sapuan bebas |
| `ui_smooth_pixel_edges_anti_aliasing` | Pakiniskan tepi piksel (antialias) | Licinkan tepi piksel (antialias) |

The two original/integration XML blobs were compared and were identical before
the edit. `Pakiniskan` is inappropriate Tagalog wording in this Malay catalogue.
The replacement is the Malay imperative of *melicinkan*, in its smoothing sense;
see [DBP, Kamus Dewan/Kamus Pelajar](https://prpm.dbp.gov.my/Cari1?d=175768&keyword=melicinkan),
consulted on 6 October 2026. This lexical reference supports the verb, not a claim
that DBP approved these complete application labels.

The labels retain different objects because they operate on different properties:

- `ClassicPaintActivity` binds the first toggle to `document.strokeSmoothing`.
  `PaintCanvas.stroke` uses that property for quadratic interpolation of freehand
  motion (excluding Pencil).
- The second toggle sets `document.antialiasing`. `PaintDocument.paint` applies it
  to `Paint.isAntiAlias` (also excluding Pencil), smoothing rendered pixel edges.

Only these two string values change. Their resource names, XML attributes and
formatting stay intact; neither contains placeholders or plural forms. This is
a direct edit to canonical Android XML, with no generator or provenance changes.

Validation: PR3's 14 translation tests pass. The full integration checks and
Android build status are reported separately at publication. These structural
checks do not certify Malay fluency or the remaining short/long strings.

The other PR3 obligations, wider language review and full latest-thread
reconciliation remain open. Conversation retrieval supplied excerpts only;
complete latest transcripts and exact message identities were unavailable.
