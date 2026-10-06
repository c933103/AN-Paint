# PR8 language-resource note: fresh recheck, 6 October 2026

Starting commit: `c1226cc0f7886e618ab51d6e44581e4ba4849a3b`.

The four current PR8 locales do **not** claim all translations are complete.
Each correctly states that new or untranslated text appears in English.
The actual defect is a separate omission: all four drop the default source's
sentence that translations are maintained in AN Paint's language resources.

Only `language20_translation_note` in each of these canonical files changes:
`Paintroid/src/main/res/<directory>/strings.xml`. The added sentences are:

| Directory | Added local sentence |
| --- | --- |
| `values-b+bo` | སྐད་བསྒྱུར་རྣམས་ AN Paint ཡི་སྐད་ཡིག་ཐོན་ཁུངས་ནང་ཉར་ཚགས་བྱེད། |
| `values-b+dz` | སྐད་བསྒྱུར་ཚུ་ AN Paint གི་སྐད་ཡིག་ཐོན་ཁུངས་ནང་བདག་འཛིན་འབདཝ་ཨིན། |
| `values-b+mn+Cyrl+MN` | Орчуулгыг AN Paint-ийн хэлний нөөцөд хадгалж, шинэчилдэг. |
| `values-b+mn+Mong` | ᠣᠷᠴᠢᠭᠤᠯᠭ᠎ᠠ ᠶᠢ AN Paint ᠤᠨ ᠬᠡᠯᠡᠨ ᠦ ᠨᠥᠭᠡᠴᠡ ᠳᠦ ᠬᠠᠳᠠᠭᠠᠯᠠᠵᠤ ᠰᠢᠨᠡᠴᠢᠯᠡᠨ᠎ᠡ᠃ |

The Tibetan and Dzongkha sentences use their own grammatical forms. The two
Mongolian sentences describe storing and updating translations in language
resources. None introduces a completion, accuracy or acceptance claim. This is
an editorial translation correction, not independent native-speaker approval.

The original local title and complete English-fallback sentence remain byte for
byte unchanged in all four entries. The two escaped newlines, resource name,
attributes and lack of format arguments also remain unchanged. Every other
resource node in these four XML files is unchanged from the starting commit.

`python3 tools/translation_catalogues.py` passes the full structural check;
strict whole-resource AAPT2 compilation and `git diff --check` pass. These checks
do not certify native fluency or runtime rendering. No other locale, app code,
generator or historical reference catalogue changes.

The earlier manual recheck remains recorded against its own starting/ending
snapshots. This separate note correction does not reopen unchanged manuals or
claim that other PR8 obligations are complete. Original PR8 and integration
publication, remote-tree checks and CI are handled separately.
