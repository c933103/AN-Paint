"""Keep PR #4's assembly help aligned with the no-resize memory branch.

These are narrow regressions for reviewed localized passages, not a general
translation-quality classifier. AssemblyRenderer.suggested returns None/null
when even 1x1 exceeds the budget; AssemblyActivity then warns without a chooser.
Android XML remains the production source; these expectations do not generate it.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
ASSEMBLY = "ui_add_up_to_20_images_with_android_s"
# directory: (old unconditional sentence, offer qualification, no-chooser warning)
MEMORY_HELP = {
    "values-sw": (
        "Ikiwa towe linazidi kikomo cha kumbukumbu, chagua nakala ndogo ya towe.",
        "ikiwa chaguo hilo linatolewa.",
        "Ikiwa hata towe dogo sana linazidi kikomo, programu huonyesha onyo la kumbukumbu badala ya kichaguzi cha ukubwa.",
    ),
    "values-fi": (
        "Jos tuloste ylittää muistirajan, valitse pienempi tulostekopio.",
        "jos sellainen on tarjolla.",
        "Jos hyvin pienikin tuloste ylittää muistirajan, sovellus näyttää muistivaroituksen kokovalitsimen sijaan.",
    ),
    "values-hu": (
        "Ha a kimenet túllépi a memóriakeretet, válasszon kisebb kimeneti másolatot.",
        "ha az alkalmazás felajánlja.",
        "Ha még egy nagyon kicsi kimenet is túllépi a keretet, az alkalmazás a méretválasztó helyett memóriafigyelmeztetést jelenít meg.",
    ),
    "values-b+af": (
        "As die uitvoer die geheuelimiet oorskry, kies ’n kleiner uitvoerkopie.",
        "as dit aangebied word.",
        "As selfs ’n baie klein uitvoer die limiet oorskry, wys die toepassing ’n geheuewaarskuwing in plaas van ’n dialoog om die grootte te kies.",
    ),
    "values-nl": (
        "Als de uitvoer het geheugenbudget overschrijdt, kiest u een kleinere uitvoerkopie.",
        "als die wordt aangeboden.",
        "Als zelfs een zeer kleine uitvoer het budget overschrijdt, toont de app een geheugenwaarschuwing in plaats van een dialoogvenster om de grootte te kiezen.",
    ),
    "values-b+et": (
        "Kui väljund ületab mälupiiri, vali väiksem väljundkoopia.",
        "kui seda pakutakse.",
        "Kui isegi väga väike väljund ületab mälupiiri, näitab rakendus suurusevaliku asemel mäluhoiatust.",
    ),
    "values-b+lv": (
        "Ja izvade pārsniedz atmiņas ierobežojumu, izvēlieties mazāku izvades kopiju.",
        "ja tā tiek piedāvāta.",
        "Ja pat ļoti maza izvade pārsniedz ierobežojumu, lietotne izmēra izvēles dialoga vietā parāda brīdinājumu par atmiņu.",
    ),
    "values-lt": (
        "Jei išvestis viršija atminties ribą, pasirinkite mažesnę išvesties kopiją.",
        "jei ji siūloma.",
        "Jei net labai maža išvestis viršija atminties ribą, programa vietoj dydžio pasirinkimo lango rodo įspėjimą apie atmintį.",
    ),
}


class AssemblyMemoryHelpPr4Tests(unittest.TestCase):
    @staticmethod
    def help_text(directory):
        nodes = ET.parse(RES / directory / "strings.xml").getroot().findall(
            f"string[@name='{ASSEMBLY}']"
        )
        if len(nodes) != 1:
            raise AssertionError(f"{directory}: expected exactly one assembly-help string")
        return "".join(nodes[0].itertext())

    def test_smaller_output_is_only_selected_when_offered(self):
        for directory, (_, qualification, _) in MEMORY_HELP.items():
            with self.subTest(locale=directory):
                self.assertIn(qualification, self.help_text(directory))

    def test_tiny_output_failure_warns_instead_of_offering_size_choice(self):
        for directory, (_, _, warning) in MEMORY_HELP.items():
            with self.subTest(locale=directory):
                self.assertIn(warning, self.help_text(directory))

    def test_old_unconditional_instruction_does_not_return(self):
        for directory, (old, _, _) in MEMORY_HELP.items():
            with self.subTest(locale=directory):
                self.assertNotIn(old, self.help_text(directory))


if __name__ == "__main__":
    unittest.main()
