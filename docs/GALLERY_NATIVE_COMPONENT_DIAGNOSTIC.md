# Gallery native-component diagnostic

The gallery validates downloaded bytes with `ImportedImage` before returning a
file to the editor. JXL validation can initialize `anpaint_jxl`; platform colour
conversion begins later, during editor decode. A broad `LinkageError` at the
gallery boundary therefore does not establish that the colour converter failed.

The gallery now reports:

> A required image component is unavailable. The image was not imported.

`PlatformImageColour.convert` retains the precise `colour_converter_unavailable`
message when the actual converter cannot link. Existing converter messages are
unchanged in every catalogue. The generic message adds one value to the default
and all 59 existing scoped catalogues; 112 other offered languages keep explicit
English fallback. Per-message model review is not native-speaker or
whole-language certification, and translation tracker acceptance is separate.

## Bounded behavior and coverage

No URL policy, redirect limit, provider request, decode fallback, native package,
permission, document mutation, temporary-file ownership or return-result rule is
changed. The `JxlCodec.readNativeInfo` test seam defaults to the existing native
call and is used only by the dimension inspection route. Failure tests inject
at that boundary after the real downloaded-byte classifier and `ImportedImage`
construction have selected JXL, rather than bypassing gallery validation.

`GalleryNativeComponentFailureTest` exercises the real WebView selection,
downloader, validation and status/result paths with fixture HTTPS connections.
It covers controlled native linkage failures, repeated failure/retry, cancellation,
policy rejection, a successful JXL-info stub control, genuine platform-image
validation and the distinct converter failure during editor decode. Complete
compiled-resource expectations cover all offered locale choices.

The JXL-info success stub proves validation and file handback, not native JXL
decoding. Existing `NativeCodecTest` and `PlatformColourImportTest` retain actual
native success controls. The profiled-JPEG failure relies on Robolectric's lack
of the Android converter JNI library and must remain attributed to JVM execution,
not an installed-device library incident. No test contacts a live provider.

Host resource contracts check full values, exact definition/fallback scope,
Android quoting and the distinct precise-converter message. They do not execute
Kotlin, native code, Android layout or accessibility. Run focused JVM tests and
the normal exact-head CI gates before claiming runtime acceptance. The
[documentation tracker](https://github.com/c933103/AN-Paint/pull/88) remains a
separate intentional draft; this change is not a claim of a real provider or
native-library outage.
