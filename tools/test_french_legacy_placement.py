"""Bounded French direction wording in the dormant long-help resource.

The active Help action uses ui_help23. These are resource consistency checks,
not a demonstration that the legacy manual is displayed or a fluency certificate.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as catalogues


RES = Path(__file__).resolve().parents[1] / 'Paintroid/src/main/res'
MANUAL = 'ui_the_arrow_on_the_left_directly_below_the'
DRAG = 'ui_drop_at_a_highlighted_edge_right_top_aligned'
PLACEMENT = ('à droite avec les bords supérieurs alignés, '
             'ou en dessous avec les bords gauches alignés')
ASSEMBLY_PARAGRAPH = (
    '«Fichier» > Assemblage d’images ouvre un espace de travail distinct pour jusqu’à 20 images. '
    'Triez les miniatures par nom de fichier ou date. Recadrez une image ou plusieurs par lot. '
    'Même largeur / Même hauteur normalise toutes les images chargées tout en conservant leur rapport hauteur/largeur. '
    'Faites glisser les miniatures ou images placées pour les placer ' + PLACEMENT + '. '
    'Retirer du placement supprime uniquement le placement sélectionné et comble l’espace. '
    'Tout afficher ajuste le zoom de la vue. Enregistrer PNG exporte l’assemblage ; '
    'Modifier dans Paint le transfère comme modification annulable. '
    'L’application utilise un éditeur d’une seule image opaque. '
    'Assemblage d’images est un espace de disposition distinct.'
)


def resource(directory, key):
    nodes = ET.parse(RES / directory / 'strings.xml').getroot().findall(f"string[@name='{key}']")
    if len(nodes) != 1:
        raise AssertionError(f'{directory}/{key}: expected one resource, found {len(nodes)}')
    return nodes[0]


class FrenchLegacyPlacementTest(unittest.TestCase):
    def test_complete_assembly_paragraph_distinguishes_placement_from_alignment(self):
        paragraphs = resource('values-fr', MANUAL).text.split(r'\n\n')
        assembly = [paragraph for paragraph in paragraphs
                    if paragraph.startswith('«Fichier» > Assemblage d’images ')]
        self.assertEqual([ASSEMBLY_PARAGRAPH], assembly)

    def test_legacy_manual_and_active_drag_hint_agree_on_both_edges(self):
        manual = resource('values-fr', MANUAL).text
        self.assertIn('pour les placer ' + PLACEMENT + '.', manual)
        self.assertEqual('Déposez sur un bord surligné : ' + PLACEMENT + '.',
                         resource('values-fr', DRAG).text)

    def test_complete_manual_keeps_paragraph_and_android_format_structure(self):
        source = resource('values', MANUAL)
        french = resource('values-fr', MANUAL)
        self.assertEqual({'name': MANUAL, 'formatted': 'false'}, french.attrib)
        self.assertEqual(0, len(french))
        self.assertEqual(10, len(french.text.split(r'\n\n')))
        self.assertEqual(source.text.count(r'\n'), french.text.count(r'\n'))
        self.assertEqual(catalogues.placeholders(source.text), catalogues.placeholders(french.text))
        self.assertEqual([], catalogues.android_string_errors(french.text))
        self.assertEqual([], catalogues.format_string_errors(french.text, formatted=False))


if __name__ == '__main__':
    unittest.main()
