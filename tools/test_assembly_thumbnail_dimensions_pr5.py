"""Guard the reviewed tray-dimensions clause, not general translation quality.

AssemblyActivity.renderTray uses AssemblyImage.placedSize for its visible label
and content description. placedSize applies optional width/height normalization
after cropping. Merely mentioning those controls in a later help paragraph does
not describe the tray correctly, so check the first paragraph only.

The five phrase fixtures are deliberately bounded to this known regression. A
future intentional rewording needs semantic review and an updated fixture; this
test is not a grammar evaluator or full-catalogue acceptance.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
ASSEMBLY = "ui_add_up_to_20_images_with_android_s"
PHRASES = {
    "values-b+es+ES": "dimensiones de las imágenes tras el recorte y cualquier ajuste de {width} o {height}",
    "values-b+es+419": "dimensiones de las imágenes tras el recorte y cualquier ajuste de {width} o {height}",
    "values-fr": "les dimensions des images après recadrage et après tout ajustement avec {width} ou {height}",
    "values-de": "Bildmaße nach dem Zuschneiden und einer etwaigen Anpassung mit «{width}» oder «{height}»",
    "values-b+eo": "bildajn dimensiojn post stuĉado kaj eventuala alĝustigo per {width} aŭ {height}",
    "values": "image dimensions after cropping and any {width} or {height} adjustment",
}


def strings(directory):
    return {node.get("name"): "".join(node.itertext())
            for node in ET.parse(RES / directory / "strings.xml").getroot()
            if node.tag == "string"}


def check_dimensions(test, directory, local):
    paragraph = local[ASSEMBLY].split(r"\n\n", 1)[0]
    phrase = PHRASES[directory].format(width=local["ui_same_width"],
                                       height=local["ui_same_height"])
    test.assertIn(phrase, paragraph,
                  f"{directory}: tray dimensions must include crop and both optional normalization controls")


class AssemblyThumbnailDimensionsTests(unittest.TestCase):
    def test_spanish_spain_tray_dimensions(self):
        check_dimensions(self, "values-b+es+ES", strings("values-b+es+ES"))

    def test_spanish_latin_america_tray_dimensions(self):
        check_dimensions(self, "values-b+es+419", strings("values-b+es+419"))

    def test_french_tray_dimensions(self):
        check_dimensions(self, "values-fr", strings("values-fr"))

    def test_german_tray_dimensions(self):
        check_dimensions(self, "values-de", strings("values-de"))

    def test_esperanto_tray_dimensions(self):
        check_dimensions(self, "values-b+eo", strings("values-b+eo"))

    def test_english_reference_tray_dimensions(self):
        check_dimensions(self, "values", strings("values"))


if __name__ == "__main__":
    unittest.main()
