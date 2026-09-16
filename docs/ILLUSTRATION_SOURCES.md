# Online illustration insertion

Draw > Insert > Other images groups device files and three optional sources.
Each image is downloaded only after a user chooses it, validated with the normal
image importer, then inserted as a floating selection. No illustration catalogue
or third-party artwork is distributed with the application.

## Source behaviour checked on 16 September 2026

| Source | Search and insertion | Terms and credit |
|---|---|---|
| Catrobat | Existing figures gallery; its image download actions become Use image, with Copy credit beside them. | Catrobat original artwork: CC BY-SA 4.0; preserve separately named creators and terms. |
| Irasutoya | Native Search submits the site's English/Japanese search form. On an artwork page, Use image and Copy credit are added beside full image anchors. Titles and site text stay Japanese. | Copyright Takashi Mifune. Conditional free use; commercial designs with 21 or more items require payment; special collaborations can have other conditions. |
| Openclipart | Native Search uses the site's query form. Artwork pages gain actions beside the published Large PNG link. | CC0. Preserve the artwork page so its contributor and provenance remain available. |

Public references: [Catrobat gallery](https://catrobat.org/figures-download/),
[Catrobat terms](https://developer.catrobat.org/pages/legal/licenses/catrobat/),
[Irasutoya terms](https://www.irasutoya.com/p/terms.html),
[Openclipart terms](https://openclipart.org/share).
Irasutoya is not public domain and its copyright is not replaced with the
Catrobat or Openclipart licence. Its terms also restrict redistribution as stock
material; use must comply with the source terms. The app links those terms and
keeps per-image source and credit text under File > About > Image credits.

## Integration details

Irasutoya's current form has an input labelled `Search in English`; submitting
`cat` was checked against the site's Google custom-search results. The app uses
the actual form and submit handler, rather than embedding a guessed search API.
The checked [typhoon detail page](https://www.irasutoya.com/2026/06/typhoon.html)
has `.entry .separator a` artwork anchors on blogger.googleusercontent.com:
the anchor points to the available `s740` PNG while the image uses `s400`.
The app imports the anchor, without inventing a larger size. Legacy
1–4.bp.blogspot.com artwork hosts are also supported.

The checked [Openclipart detail page](https://openclipart.org/detail/250963/public-domain)
offers `/image/2000px/250963` as Large PNG. The application uses that raster link;
it does not pass the SVG download to the bitmap importer. Contributor details
remain on the saved source page; a publisher is not presented as the individual
artist. Credit text is editable for publication-specific attribution and edits.

Web navigation, image hosts and redirect destinations are checked separately per
provider. Downloads must use HTTPS and pass the existing size/content checks.
Scripts add ordinary links, not a JavaScript/native bridge. Script fixtures cover
idempotence, full image anchors, unrelated links and PNG selection. Transport
substitution tests cover download/result handling and provider-specific credits.
These tests do not promise that third-party websites will keep their markup.
