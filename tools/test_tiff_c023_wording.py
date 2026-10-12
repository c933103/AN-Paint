"""Current Cyrillic Mongolian TIFF wording contract."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
KEY = "formats22_tiff_description"
PATH = "Paintroid/src/main/res/values-b+mn+Cyrl+MN/strings.xml"
ORIGINAL = "Нэг RGB хуудсыг хадгална. Шахалт нь пикселийг өөрчлөхгүйгээр файлын хэмжээг багасгана; шахалтгүй TIFF хадгалахын тулд унтраана."
EXPECTED = "Нэг RGB хуудсыг хадгална. Шахалт нь пикселийг өөрчлөхгүйгээр файлын хэмжээг багасгаж магадгүй; шахалтгүй TIFF хадгалахын тулд унтраана."

class TiffC023WordingTests(unittest.TestCase):
    def test_exact_single_definition_and_unchanged_checkbox(self):
        root = ET.parse(ROOT / PATH).getroot()
        nodes = root.findall(f"./string[@name='{KEY}']")
        self.assertEqual(1, len(nodes))
        self.assertEqual({"name": KEY}, nodes[0].attrib)
        self.assertEqual(0, len(nodes[0]))
        self.assertEqual(EXPECTED, nodes[0].text)
        self.assertNotIn("%", nodes[0].text)
        checkbox = root.findall("./string[@name='formats22_tiff_compression']")
        self.assertEqual(1, len(checkbox))
        self.assertEqual("Алдагдалгүй шахалт (Deflate)", checkbox[0].text)
