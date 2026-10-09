"""Guard the two memory-limit branches in the five reviewed assembly help texts.

AssemblyRenderer.suggested() can return null when even 1x1 does not fit.
AssemblyActivity.outputSizeDialog then shows ui_assembly_source_memory_floor
and returns without displaying the size chooser. The help must describe both
conditional resizing and the alternative warning, in its output paragraph.

These bounded phrase fixtures protect one known semantic regression. Intentional
rewording needs review and revised fixtures. This is neither a general grammar
checker nor full-catalogue linguistic acceptance, and does not execute Android.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
ASSEMBLY = "ui_add_up_to_20_images_with_android_s"
PHRASES = {
    "values-b+es+ES": (
        "Si la salida supera el límite de memoria, elige una copia de salida más pequeña si se ofrece esa opción.",
        "Si incluso una salida diminuta supera el límite, la aplicación muestra una advertencia de memoria en lugar de un selector de tamaño.",
    ),
    "values-b+es+419": (
        "Si la salida supera el límite de memoria, elige una copia de salida más pequeña si se ofrece esa opción.",
        "Si incluso una salida diminuta supera el límite, la aplicación muestra una advertencia de memoria en lugar de un selector de tamaño.",
    ),
    "values-fr": (
        "Si la sortie dépasse la limite mémoire, choisissez une copie de sortie plus petite si cette option est proposée.",
        "Si même une sortie minuscule dépasse cette limite, l’application affiche un avertissement de mémoire au lieu d’un sélecteur de taille.",
    ),
    "values-de": (
        "Wenn die Ausgabe das Speicherlimit überschreitet, wählen Sie eine kleinere Ausgabekopie, sofern diese Option angeboten wird.",
        "Wenn selbst eine winzige Ausgabe das Limit überschreitet, zeigt die App eine Speicherwarnung statt einer Größenauswahl.",
    ),
    "values-b+eo": (
        "Se la eligo superas la memoran limon, elektu pli malgrandan eligan kopion, se tiu opcio estas proponata.",
        "Se eĉ tre malgranda eligo superas la limon, la aplikaĵo montras averton pri memoro anstataŭ elektilo de grando.",
    ),
    "values": (
        "If the output exceeds the memory budget, choose a smaller output copy if offered.",
        "If even a tiny output exceeds the budget, the app shows a memory warning instead of a size chooser.",
    ),
}


def strings(directory):
    return {node.get("name"): "".join(node.itertext())
            for node in ET.parse(RES / directory / "strings.xml").getroot()
            if node.tag == "string"}


def check_memory_help(test, directory):
    # Do not accept the correct phrase in the source-memory warning resource,
    # a separate help paragraph, or an unrelated part of the main editor manual.
    paragraph = strings(directory)[ASSEMBLY].split(r"\n\n")[5]
    for branch, phrase in zip(("conditional resize", "warning without chooser"), PHRASES[directory]):
        with test.subTest(locale=directory, branch=branch):
            test.assertIn(phrase, paragraph, f"{directory}: missing assembly output guidance for {branch}")


class AssemblyNoResizeHelpTests(unittest.TestCase):
    def test_spanish_spain_memory_limit_branches(self):
        check_memory_help(self, "values-b+es+ES")

    def test_spanish_latin_america_memory_limit_branches(self):
        check_memory_help(self, "values-b+es+419")

    def test_french_memory_limit_branches(self):
        check_memory_help(self, "values-fr")

    def test_german_memory_limit_branches(self):
        check_memory_help(self, "values-de")

    def test_esperanto_memory_limit_branches(self):
        check_memory_help(self, "values-b+eo")

    def test_english_reference_memory_limit_branches(self):
        check_memory_help(self, "values")


if __name__ == "__main__":
    unittest.main()
