"""Current Save/Export safety clauses and live captions, not complete prose approval."""
from pathlib import Path
import unittest
import translation_catalogues as catalogues
from test_assembly_help_pr8 import code_locations

ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
MANUAL = 'ui_the_arrow_on_the_left_directly_below_the'
ASSEMBLY = 'ui_add_up_to_20_images_with_android_s'


class HelpSaveExportPr8Tests(unittest.TestCase):
    def test_save_export_captions_and_safety_clauses_share_the_actual_save_context(self):
        # Independent copy/destination/saved-state/private-draft/original guarantees.
        # Do not freeze sentence order, paragraph count, or surrounding help prose.
        for tag, clauses in (
            ('bo', ('འདྲ་བཤུས་ཉར', 'ད་ལྟའི་ཉར་གནས་མི་བསྒྱུར',
                    'ཉར་ཟིན་པའི་རྟགས་ཀྱང་མི་འགོད', 'སྒེར་གྱི་ལས་ཀའི་ཟིན་བྲིས',
                    'མ་ཡིག་པར་རིས་ཀྱི་སྟེང་དུ་ནམ་ཡང་བསྐྱར་འབྲི་མི་བྱེད')),
            ('dz', ('འདྲ་བཤུས་སྲུང་བཞག', 'ད་ལྟོའི་སྲུང་བཞག་ས་གནས་མི་བསྒྱུརཝ',
                    'སྲུང་བཞག་ཚར་བའི་རྟགས་མི་བཀལ', 'སྒེར་གྱི་ལཱ་འབད་སའི་ཟིན་བྲིས',
                    'མ་ཡིག་གཟུགས་བརྙན་གྱི་ཐོག་ལུ་ནམ་ཡང་ཚབ་འབྲི་མི་འབད')),
            ('mn-Mong', ('ᠬᠠᠭᠤᠯᠪᠤᠷᠢ ᠪᠢᠴᠢᠨ᠎ᠡ',
                         'ᠣᠳᠣᠭᠠᠨ ᠤ ᠬᠠᠳᠠᠭᠠᠯᠠᠬᠤ ᠪᠠᠶᠢᠷᠢᠰᠢᠯ ᠢ ᠥᠭᠡᠷᠡᠴᠢᠯᠡᠬᠦ ᠦᠭᠡᠢ',
                         'ᠬᠠᠳᠠᠭᠠᠯᠠᠭᠰᠠᠨ ᠭᠡᠵᠦ ᠲᠡᠮᠳᠡᠭᠯᠡᠬᠦ ᠦᠭᠡᠢ',
                         'ᠬᠤᠪᠢ ᠶᠢᠨ ᠠᠵᠢᠯ ᠤᠨ ᠨᠣᠣᠷᠠᠭ',
                         'ᠡᠬᠢ ᠵᠢᠷᠤᠭ ᠢ ᠬᠡᠵᠢᠶ᠎ᠡ ᠴᠤ ᠳᠠᠪᠬᠤᠷᠯᠠᠨ ᠪᠢᠴᠢᠬᠦ ᠦᠭᠡᠢ')),
        ):
            strings = catalogues.read_strings(catalogues.catalogue_paths()[tag])
            labels = [strings[k].rstrip('….།༎') for k in ('save20_title', 'ui_save', 'ui_export_as23', 'ui_save_and_share')]
            paragraphs = strings[MANUAL].split(r'\n\n')
            save_context = [p for p in paragraphs if '«' + labels[2] + '»' in p]
            self.assertEqual(1, len(save_context))
            value = save_context[0]
            for label in labels:
                self.assertIn('«' + label + '»', value)
            for clause in clauses:
                self.assertIn(clause, value)

    def test_mongolian_attachment_movement_is_conditional_and_overlap_is_rejected(self):
        value = catalogues.read_strings(catalogues.catalogue_paths()['mn-Mong'])[ASSEMBLY]
        self.assertIn('ᠲᠡᠭᠦᠨ ᠳᠦ ᠬᠣᠯᠪᠣᠭᠰᠠᠨ ᠵᠢᠷᠤᠭ ᠤᠳ ᠬᠥᠳᠡᠯᠵᠦ ᠪᠣᠯᠣᠨ᠎ᠠ', value)
        self.assertIn('ᠳᠠᠪᠬᠤᠷᠳᠠᠭᠤᠯᠬᠤ ᠶᠢ ᠵᠥᠪᠰᠢᠶᠡᠷᠡᠬᠦ ᠦᠭᠡᠢ', value)
        self.assertNotIn('ᠵᠢᠷᠤᠭ ᠤᠳ ᠴᠤ ᠬᠥᠳᠡᠯᠦᠨ᠎ᠡ', value)

    def test_active_main_help_and_assembly_keep_their_distinct_resource_routes(self):
        classic = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')
        assembly = (CLASSIC / 'AssemblyActivity.kt').read_text(encoding='utf-8')
        self.assertTrue(code_locations(classic, 'private fun showHelp() = message(ui(R.string.ui_help23))'))
        self.assertTrue(code_locations(assembly, 'private fun showHelp() = message(ui(R.string.' + ASSEMBLY + '))'))
        # Prevent attributing this retained-resource correction to displayed main Help.
        for path in CLASSIC.glob('*.kt'):
            self.assertFalse(code_locations(path.read_text(encoding='utf-8'), 'R.string.' + MANUAL), path.name)

if __name__ == "__main__":
    unittest.main()
