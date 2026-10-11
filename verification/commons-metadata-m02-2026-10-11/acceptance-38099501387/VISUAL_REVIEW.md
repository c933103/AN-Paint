# M02 rendered-status observations

Inspected 2026-10-11 on original-scale contact sheets generated from current-head CI's real Robolectric NATIVE PNGs. Each row links four distinct captures in this order: normal Copy credit, normal insertion, double-scale Copy credit, double-scale insertion. All **40 captures** were inspected, not just the JSON claims. Original 640×1280 PNGs and JSON remain in the original [Actions regression artifact](https://github.com/c933103/AN-Paint/actions/runs/38099501387/artifacts/11686269936); the prepared `current-scoped-regression.zip` copy is not yet committed. `capture-receipt.json` binds their byte and decoded-pixel hashes.

| Profile | Four-image contact | Observed status and limitation |
|---|---|---|
| en-GB | [English](contacts/en-GB.png) | Distinct outer copy/insertion wrappers, complete English M02 reason and ASCII 503; visibly enlarged at 2× and wrapped without status ellipsis. |
| fr | [French](contacts/fr.png) | Accented glyphs render; both enlarged wrappers and M02 reason wrap across lines. Full horizontal status remains visible. |
| ar | [Arabic](contacts/ar.png) | RTL status and Arabic glyphs render; HTTP and ASCII 503 remain present. At 2× Copy credit the HTTP token and 503 wrap across lines. This does not certify Arabic grammar or detailed shaping. |
| ja | [Japanese](contacts/ja.png) | Kana/Han glyphs and ASCII HTTP 503 render in both wrappers/scales; no obvious missing-glyph boxes in the new status. |
| vi-Hani | [Nôm](contacts/vi-Hani.png) | Han/Nôm forms visibly render at both scales, along with HTTP 503; no obvious tofu in the new status. Character appearance does not certify Nôm wording or rare-glyph correctness. |
| mn-Mong | [Vertical Mongolian](contacts/mn-Mong.png) | Vertical columns, Mongolian glyphs and sideways Latin HTTP 503 remain drawn, visibly enlarged at 2×. Reading-start screenshots do not establish that every long column is simultaneously visible. |
| mnc-Mong | [Vertical Manchu](contacts/mnc-Mong.png) | Vertical Manchu-script forms and HTTP/503 render at both sizes; HTTP and 503 can occupy adjacent columns. No native Manchu terminology or shaping certification. |
| lzh-Hant | [Literary Chinese](contacts/lzh-Hant.png) | Traditional Han columns and Latin HTTP 503 are present in each wrapper. At 2× status occupies more columns; scrolling is part of established layout. |
| en-XV | [Vertical English](contacts/en-XV.png) | Both English wrappers and reason remain visible in vertical columns; enlargement is actual, not merely label/configuration metadata. |
| qaa-Zsye-XV | [Vertical symbolic](contacts/qaa-Zsye-XV.png) | Warning symbol and English metadata reason render alongside HTTP 503 in both wrappers/scales; colored symbols are visibly present. This is the established symbolic convention, not a newly accepted language. |

The executed tests separately assert actual `configuration.fontScale` equals 1 or 2, full accessibility-node text, no ellipsize, full final layout character index, and adequate status layout height. Horizontal profiles assert the whole status is visible; Arabic also asserts RTL direction. Vertical profiles assert visible height and both horizontal scroll endpoints, then reset to reading start before capture. Thus full-text layout and scroll reachability are distinct from a claim that one screenshot shows every column.

Contacts preserve 640-pixel original width and the top 960 pixels below a separate caption. Lower controls/WebView content outside this crop cannot be judged from a contact. At double scale, unrelated controls may lie offscreen or beyond the crop; this check accepts the new status and inherited scrolling boundary, not all controls simultaneously. Full originals remain available.

No obvious missing-glyph boxes were observed in these new status regions. That narrow observation is not a proof of complete glyph coverage, script shaping correctness, reading order fluency, translation adequacy, physical-device behavior, TalkBack/service output or all-language UI acceptance. The 96 inherited installed-emulator captures were decoded/inventory-checked, not given fresh visual acceptance in this bounded M02 review. All target-language proposals remain unreviewed.
