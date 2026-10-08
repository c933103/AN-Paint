# Traditional Mongolian legacy assembly capacity: new, bounded recheck

This records a narrow repair after the 28 September reset. Earlier completion
claims remain withdrawn. Register R-008's specific missing-capacity claim was
checked anew; this does not close the full manual or PR8 review.

The inspected original PR8 head is
`635a9603a37d44d0e208ac1338b01c7e27ce53c8`; the integration head is
`00e4429dbcf3ae485c88e448334e43474c1fb134`. Their Traditional Mongolian XML blobs
were identical before editing.

The English resource `ui_the_arrow_on_the_left_directly_below_the` says that
Image assembly opens a separate workspace for up to 20 images. In the Mongolian
resource with that exact name, the assembly passage went directly from opening
the feature to sorting thumbnails, without its capacity clause. The later
sentence already describes a separate arrangement workspace. The application
enforces `ImageAssembly.MAX_IMAGES = 20`, including when adding or restoring
images; 20 is an upper bound, not a required count.

The repair inserts this sentence after the opening/sorting sentence:

> ᠨᠢᠭᠡ ᠨᠡᠶᠢᠯᠡᠯ ᠳᠦ 20 ᠬᠦᠷᠲᠡᠯᠡᠬᠢ ᠵᠢᠷᠤᠭ ᠪᠠᠶᠢᠵᠤ ᠪᠣᠯᠣᠨ᠎ᠠ᠃

Its meaning is that one assembly may contain up to 20 images. The same sentence
is present in the locale's separate capacity notice. It was checked for its
upper-bound meaning before reuse; existing presence alone is not approval.
Lexical references consulted on 6 October 2026:
[хүртэл (extent/up to)](https://www.mongoltoli.mn/search.php?opt=1&ug_id=118116)
and [зураг / ᠵᠢᠷᠤᠭ (image)](https://mongoltoli.mn/dictionary/detail/49157).
These are word references, not independent certification of the whole sentence.

The separate `ui_add_up_to_20_images_with_android_s` help already states the
20-image limit. The current short help, `ui_help23`, does not make a capacity
claim in its English or Mongolian text. Neither resource is evidence that the
legacy omission was fixed; both remain unchanged in this patch. The remaining
legacy operational clauses are unchanged and are not declared fully reviewed.

The new regression reads `MAX_IMAGES` from application source and checks the
limit inside the assembly section of this exact legacy key. It fails against
the pre-fix XML and passes after the repair. The seven localized-help checks
pass, and strict AAPT2 resource compilation passes using version
`8.13.0-13719691` (`aapt2 version`: `2.20-13719691`). The edit adds no format
arguments, resource references or plural forms and preserves escaped newlines.

Full Android build/device results are reported separately at publication.
The rest of R-007–R-012, the complete PR8 semantic review, related source/credit
claims and latest-thread reconciliation remain open. Complete latest conversation
transcripts were unavailable; retrieved excerpts do not establish their entirety.
