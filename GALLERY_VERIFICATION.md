# Online gallery verification

Checked 12 September 2026 against the live publisher pages and the current app source.

## Live contract checked

- [Catrobat Figures – Download](https://catrobat.org/figures-download/) is reachable and lists image/download links. The sampled entries link directly to [Apple(1)](https://catrobat.org/wp-content/uploads/2025/01/Apple1.png) and [Sun](https://catrobat.org/wp-content/uploads/2025/01/Sun.png); both image URLs resolve. Their HTTPS host and `.png` paths match the app’s existing download interception.
- The current listing gives artwork names, with no separate creator or licence field beside those sampled entries. [Catrobat’s own licence page](https://developer.catrobat.org/pages/legal/licenses/catrobat/) covers its own non-software artwork under CC BY-SA 4.0, with exceptions for project names/logos. This supports the app’s Catrobat attribution and licence link; it is not a grant over unrelated third-party artwork.

## App behavior reviewed

`MediaGalleryActivity` opens the publisher’s page in a WebView. Tapping a direct supported image link or long-pressing an image opens the insertion confirmation. The downloader allows specified Catrobat hosts, checks each redirect, caps the transfer at 128 MiB and validates image dimensions before returning a private cache filename and the requested source URL.

The main editor validates the returned cache file and URL, records the URL under Help > Image credits, then uses the normal image insertion/resize flow. Credits are retained as an app-wide source history; they are not embedded into exported image files. The app provides a generic Catrobat credit and licence explanation. It does **not** parse individual creator, title or licence metadata from the website. Any separately stated attribution must still be checked at its source.

The review found and corrected one translation-related defect: the HTTP redirect header name was being read from a translatable string. It now uses the protocol name `Location` directly, and the otherwise-unused string resource was removed.

## Verification boundary and remaining device check

The live checks establish that the current webpage and sampled image links match the app’s expected URL contract. Existing automated checks establish the File-menu ordering and host validation. They do not establish an actual Android WebView tap, network download and insertion round trip.

The remaining focused check is to install the built app, open File > Catrobat sticker gallery, select Apple(1), confirm insertion and verify the floating image appears on the current canvas with its source URL under Help > Image credits. Cancel a second insertion and confirm the current canvas remains intact. A redirect and an unavailable image should also produce the intended visible result without losing the canvas.

This document does not claim that physical-phone gallery verification has occurred.
