"""Selection status and attached-image warning in paired Assembly consumers."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from translation_catalogues import android_string_errors, placeholders

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
CASES = {
    'b+ia': (
        ('one', 'other'),
        'Imagines seligite pro taliar: %3$d.',
        'Taliar imagines placiate pote mover lor imagines attachate.',
        'Le imagines attachate pote mover se',
    ),
    'b+ast': (
        ('one', 'other'),
        'Imáxenes escoyíes pa recortar: %3$d.',
        'Recortar imáxenes asitiaes pue mover les imáxenes xuníes a elles.',
        'Les imáxenes xuníes puen movese',
    ),
    'gl': (
        ('one', 'other'),
        'Imaxes seleccionadas para recortar: %3$d.',
        'Recortar as imaxes colocadas pode mover as imaxes anexadas a elas.',
        'As imaxes unidas poden moverse',
    ),
    'ca': (
        ('one', 'other'),
        'Imatges seleccionades per retallar: %3$d.',
        'Retallar imatges col·locades pot moure les imatges que hi estan connectades.',
        'Les imatges connectades es poden moure',
    ),
    'b+ca+ES+valencia': (
        ('one', 'many', 'other'),
        'Imatges seleccionades per a escapçar: %3$d.',
        'Escapçar les imatges col·locades pot moure les imatges que tenen adjuntes.',
        'Les imatges connectades es poden moure',
    ),
    'b+oc': (
        ('other',),
        'Imatges seleccionats pel retalh : %3$d.',
        'Retalhar d’imatges plaçats pòt desplaçar los imatges que lor son estacats.',
        'Los imatges ligats se pòdon desplaçar',
    ),
    'ro': (
        ('one', 'few', 'other'),
        'Imagini selectate pentru decupare: %3$d.',
        'Decuparea imaginilor plasate poate deplasa imaginile atașate lor.',
        'Imaginile atașate se pot deplasa',
    ),
    'ru': (
        ('one', 'few', 'many', 'other'),
        'Выбрано изображений для обрезки: %3$d.',
        'При обрезке размещённых изображений присоединённые к ним изображения могут переместиться.',
        'Присоединённые изображения могут перемещаться',
    ),
}


class CropSelectionStatusCompanionsTest(unittest.TestCase):
    def test_selected_count_is_status_and_help_preserves_conditional_movement(self):
        for tag, (forms, status, warning, help_phrase) in CASES.items():
            with self.subTest(locale=tag):
                root = ET.parse(RES / f"values-{tag}" / "strings.xml")
                help_value = root.find("string[@name='ui_add_up_to_20_images_with_android_s']").text
                self.assertIn(help_phrase, help_value.split(r"\n\n")[2])
                items = root.findall("plurals[@name='ui_crop_preview_images']/item")
                self.assertCountEqual(forms, [item.attrib["quantity"] for item in items])
                for item in items:
                    text = item.text.strip('"')
                    preview, detail = text.split(r"\n")
                    self.assertIn("%1$d × %2$d px", preview)
                    self.assertEqual(status + " " + warning, detail)
                    self.assertCountEqual(placeholders("%1$d %2$d %3$d"), placeholders(text))
                    self.assertEqual([], android_string_errors(text))
