"""Known Save/Export manual regressions in five PR #5 catalogues.

Read canonical XML and resolve live menu captions. These narrow, reviewed clauses
protect destination and dirty-state guidance, not general translation fluency.
Keep checks inside the Save paragraph so an unrelated later mention cannot pass.
"""
from pathlib import Path
import re
import unicodedata
import unittest
import xml.etree.ElementTree as ET


RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
MANUAL = "ui_the_arrow_on_the_left_directly_below_the"
CAPTIONS = {
    "save_as": "save20_title",
    "save": "ui_save",
    "export": "ui_export_as23",
    "share": "ui_save_and_share",
}
# Each clause binds its operation to the real caption; tests do not substitute
# corrected help text or generate any resources from these expectations.
CLAUSES = {
    "values-b+es+ES": (
        "«{save_as}» permite elegir el formato de imagen, los ajustes y la ubicación;",
        "«{save}» vuelve a escribir en esa ubicación.",
        "«{export}» y «{share}» escriben una copia sin cambiar el destino actual de «{save}» ni marcar el dibujo como guardado.",
        "«{share}» abre después el sistema de compartir de Android.",
        "El asterisco del nombre de archivo indica que el dibujo actual tiene cambios sin guardar.",
    ),
    "values-b+es+419": (
        "«{save_as}» permite elegir el formato de imagen, la configuración y la ubicación;",
        "«{save}» vuelve a escribir en esa ubicación.",
        "«{export}» y «{share}» escriben una copia sin cambiar el destino actual de «{save}» ni marcar el dibujo como guardado.",
        "«{share}» abre después el sistema de compartir de Android.",
        "El asterisco del nombre de archivo indica que el dibujo actual tiene cambios sin guardar.",
    ),
    "values-fr": (
        "«{save_as}» permet de choisir le format de l’image, les réglages et l’emplacement ;",
        "«{save}» écrit de nouveau à cet emplacement.",
        "«{export}» et «{share}» écrivent une copie sans changer la destination actuelle de «{save}» ni marquer le dessin comme enregistré.",
        "«{share}» ouvre ensuite le partage Android.",
        "L’astérisque du nom de fichier indique que le dessin actuel comporte des modifications non enregistrées.",
    ),
    "values-de": (
        "«{save_as}» legt Bildformat, Einstellungen und Speicherort fest;",
        "«{save}» schreibt erneut an diesen Ort.",
        "«{export}» und «{share}» schreiben eine Kopie, ohne das aktuelle Speicherziel von «{save}» zu ändern oder die Zeichnung als gespeichert zu markieren.",
        "«{share}» öffnet anschließend die Android-Freigabe.",
        "Der Stern am Dateinamen bedeutet, dass die aktuelle Zeichnung ungespeicherte Änderungen enthält.",
    ),
    "values-b+eo": (
        "«{save_as}» ebligas elekti la bildformaton, agordojn kaj lokon;",
        "«{save}» denove skribas al tiu loko.",
        "«{export}» kaj «{share}» skribas kopion sen ŝanĝi la nunan celon de «{save}» aŭ marki la desegnon kiel konservitan.",
        "«{share}» poste malfermas Android-kunhavigon.",
        "La steleto ĉe la dosiernomo signifas, ke la nuna desegno havas nekonservitajn ŝanĝojn.",
    ),
}
STALE_SUBJECTS = {
    "values-b+es+ES": "el archivo exportado",
    "values-b+es+419": "el archivo exportado",
    "values-fr": "le fichier exporté",
    "values-de": "die exportierte Datei",
    "values-b+eo": "la elportita dosiero",
}


def read_catalogue(directory):
    result = {}
    for path in sorted((RES / directory).glob("*.xml")):
        for node in ET.parse(path).getroot():
            if node.tag == "string":
                result[node.get("name")] = "".join(node.itertext())
    return result


def text(value):
    # Retain words, negations, inflections and clause boundaries. Normalize only
    # Android escaping, canonical Unicode and layout whitespace.
    value = value.replace(r"\'", "'").replace(r'\"', '"')
    value = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m[1], 16)), value)
    return " ".join(unicodedata.normalize("NFC", value).split())


def captions(rendered):
    result = {}
    for role, key in CAPTIONS.items():
        seen = set()
        while True:
            if key in seen:
                raise AssertionError(f"Cyclic caption reference: {key}")
            seen.add(key)
            value = rendered[key]
            if not value.startswith("@string/"):
                break
            key = value.removeprefix("@string/")
        # Ellipses indicate a following dialog; help can name the command
        # without that terminal UI punctuation.
        result[role] = text(value).rstrip(".…")
    return result


def save_paragraph(manual):
    paragraphs = re.split(r"\\n\\n|\n\s*\n", manual)
    if len(paragraphs) <= 3:
        raise AssertionError("Manual has no fourth (Save/Export) paragraph")
    return text(paragraphs[3])


def check_clause(case, directory, local, rendered, index):
    expected = CLAUSES[directory][index].format(**captions(rendered))
    case.assertIn(text(expected), save_paragraph(local[MANUAL]))


class ManualSaveExportPr5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.default = read_catalogue("values")
        cls.locales = {directory: read_catalogue(directory) for directory in CLAUSES}

    def check_all(self, index):
        for directory, local in self.locales.items():
            with self.subTest(locale=directory):
                self.assertIn(MANUAL, local, "Missing canonical localized manual")
                check_clause(self, directory, local, {**self.default, **local}, index)

    def test_save_as_chooses_format_settings_and_location(self):
        self.check_all(0)

    def test_save_reuses_that_destination(self):
        self.check_all(1)

    def test_export_and_share_copy_without_changing_destination_or_saved_state(self):
        self.check_all(2)

    def test_save_and_share_then_opens_android_sharing(self):
        self.check_all(3)

    def test_filename_star_describes_current_drawing_changes(self):
        self.check_all(4)
        for directory, local in self.locales.items():
            with self.subTest(locale=directory, stale_subject=True):
                self.assertNotIn(text(STALE_SUBJECTS[directory]), save_paragraph(local[MANUAL]))


if __name__ == "__main__":
    unittest.main()
