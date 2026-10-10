"""Bounded regression for PR 4's manual Save/Export contract.

The copy/star anchors are reviewed wording for one known defect, not a language
or fluency classifier. XML remains canonical; this test generates no resources.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
MANUAL = "ui_the_arrow_on_the_left_directly_below_the"
# locale: (old exported-file claim, copy + unchanged destination/saved-state anchor,
#          drawing-dirty star anchor)
ANCHORS = {
    "sw": (
        "faili iliyohamishwa ina mabadiliko ambayo hayajahifadhiwa",
        "huandika nakala bila kubadilisha eneo la sasa la Hifadhi wala kuashiria mchoro kuwa umehifadhiwa",
        "Nyota kwenye jina la faili inamaanisha kuwa mchoro una mabadiliko ambayo hayajahifadhiwa",
    ),
    "fi": (
        "vietyyn tiedostoon nähden on tallentamattomia muutoksia",
        "kirjoittavat kopion muuttamatta nykyistä tallennussijaintia tai merkitsemättä piirrosta tallennetuksi",
        "Tiedostonimen tähti tarkoittaa, että piirroksessa on tallentamattomia muutoksia",
    ),
    "hu": (
        "az exportált fájlhoz képest vannak mentetlen módosítások",
        "másolatot ír a jelenlegi mentési hely módosítása nélkül, és nem jelöli mentettnek a rajzot",
        "A fájlnév melletti csillag azt jelzi, hogy a rajzon mentetlen módosítások vannak",
    ),
    "b+af": (
        "die uitgevoerde lêer ongestoorde veranderinge het",
        "skryf ’n kopie sonder om die huidige stoorbestemming te verander of die tekening as gestoor te merk",
        "Die ster by die lêernaam beteken dat die tekening ongestoorde veranderinge het",
    ),
    "nl": (
        "het geëxporteerde bestand niet-opgeslagen wijzigingen heeft",
        "schrijven een kopie zonder de huidige opslaglocatie te wijzigen of de tekening als opgeslagen te markeren",
        "De ster bij de bestandsnaam betekent dat de tekening niet-opgeslagen wijzigingen heeft",
    ),
    "b+et": (
        "eksporditud faili suhtes on salvestamata muudatusi",
        "kirjutavad koopia, muutmata praegust salvestuskohta või märkimata joonistust salvestatuks",
        "Failinime tärn tähendab, et joonistusel on salvestamata muudatusi",
    ),
    "b+lv": (
        "eksportētajam failam ir nesaglabātas izmaiņas",
        "ieraksta kopiju, nemainot pašreizējo saglabāšanas vietu un neatzīmējot zīmējumu kā saglabātu",
        "Zvaigznīte pie faila nosaukuma nozīmē, ka zīmējumā ir nesaglabātas izmaiņas",
    ),
    "lt": (
        "eksportuoto failo atžvilgiu yra neišsaugotų pakeitimų",
        "įrašo kopiją nekeisdami dabartinės išsaugojimo vietos ir nepažymėdami piešinio kaip išsaugoto",
        "Žvaigždutė prie failo pavadinimo reiškia, kad piešinyje yra neišsaugotų pakeitimų",
    ),
}


def catalogue(locale):
    path = RES / f"values-{locale}" / "strings.xml"
    return {node.get("name"): "".join(node.itertext())
            for node in ET.parse(path).getroot() if node.tag == "string"}


def save_paragraph(local):
    # Validate this paragraph itself, so captions elsewhere cannot mask the bug.
    return local[MANUAL].split(r"\n\n")[3]


class SaveExportHelpPr4Tests(unittest.TestCase):
    def test_save_paragraph_names_all_four_actual_controls(self):
        for locale in ANCHORS:
            local = catalogue(locale)
            paragraph = save_paragraph(local)
            for key in ("ui_save", "save20_title", "ui_export_as23", "ui_save_and_share"):
                with self.subTest(locale=locale, key=key):
                    label = local[key].rstrip("….")
                    self.assertTrue(label in paragraph,
                                    f"{locale}: Save paragraph is missing control caption {label!r}")

    def test_export_is_a_copy_and_preserves_destination_and_saved_state(self):
        for locale, (_, copy, _) in ANCHORS.items():
            with self.subTest(locale=locale):
                self.assertTrue(copy in save_paragraph(catalogue(locale)),
                                f"{locale}: missing explicit copy/destination/saved-state wording")

    def test_star_describes_the_drawing_unsaved_changes(self):
        for locale, (_, _, star) in ANCHORS.items():
            with self.subTest(locale=locale):
                self.assertTrue(star in save_paragraph(catalogue(locale)),
                                f"{locale}: missing drawing-dirty star wording")

    def test_known_exported_file_star_claim_does_not_return(self):
        for locale, (stale, _, _) in ANCHORS.items():
            with self.subTest(locale=locale):
                self.assertFalse(stale in save_paragraph(catalogue(locale)),
                                 f"{locale}: exported-file star claim remains")


if __name__ == "__main__":
    unittest.main()
