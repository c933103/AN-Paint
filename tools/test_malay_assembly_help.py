"""Complete accepted Malay assembly Help, not whole-language acceptance.

The fixture is one reviewed value, not a generator or permanent source hash.
Explicit ValueError checks and unittest assertions remain active under python -O.
"""
import json
from pathlib import Path
import unittest
import assembly_help_checks as help_checks

ROOT = Path(__file__).resolve().parents[1]
KEY = 'ui_add_up_to_20_images_with_android_s'
DIRECTORY = 'values-ms'
RESOURCE = ROOT / 'Paintroid/src/main/res' / DIRECTORY / 'strings.xml'
FIXTURE = ROOT / 'tools/fixtures/current_localization/malay_assembly_help.json'
CAPTIONS = ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop', 'ui_same_width', 'ui_same_height', 'ui_smallest', 'ui_largest', 'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all', 'ui_save_png', 'ui_edit_in_paint', 'ui_menu_file', 'ui_about_credits23', 'ui_undo', 'ui_redo')


def require_fixture(fixture):
    if (set(fixture) != {'locale', 'directory', 'key', 'value'}
            or fixture['locale'] != 'ms' or fixture['directory'] != DIRECTORY
            or fixture['key'] != KEY or not isinstance(fixture['value'], str)):
        raise ValueError('Unexpected Malay Help fixture identity')
    value = fixture['value']
    paragraphs = value.split(r'\n\n')
    if (len(paragraphs) != 8 or not all(paragraphs)
            or value.count(r'\n') != 14 or '\n' in value or '\r' in value):
        raise ValueError('Malay Help paragraph structure differs')
    return value


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY} or len(nodes[0]):
        raise ValueError('Help key, attributes or child markup changed')
    if nodes[0].text != expected:
        raise ValueError('Complete Malay Help differs')


class MalayAssemblyHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        help_checks.set_up_class(cls, FIXTURE, RESOURCE, require_fixture)

    def reject_value(self, value):
        help_checks.reject_value(self, value, KEY, require_complete)

    def test_exact_complete_eight_paragraph_value(self):
        help_checks.check_complete_eight_paragraph_value(self, ROOT, KEY, require_complete)

    def test_actual_captions_and_existing_p3_scope(self):
        for key in CAPTIONS:
            with self.subTest(key=key):
                nodes = self.root.findall(f"./string[@name='{key}']")
                self.assertEqual(1, len(nodes))
                self.assertIn(nodes[0].text, self.expected)
        file_label = self.root.find("./string[@name='ui_menu_file']").text
        about_label = self.root.find("./string[@name='ui_about_credits23']").text
        self.assertIn(file_label + ' > ' + about_label, self.paragraphs[7])
        tiers = json.loads((ROOT / 'translations/string-importance.json').read_text(encoding='utf-8'))['tiers']
        actual = {key: tier['id'] for tier in tiers for key in tier['keys']}
        self.assertEqual('P3', actual['string/' + KEY])

    def test_oracle_rejects_each_sentence_omission_and_duplication(self):
        sentences = [sentence + '.' for paragraph in self.paragraphs
                     for sentence in paragraph[:-1].split('. ')]
        self.assertEqual(34, len(sentences))
        for sentence in sentences:
            self.assertEqual(1, self.expected.count(sentence))
            for replacement in ('', sentence + ' ' + sentence):
                with self.subTest(sentence=sentence, replacement=replacement):
                    self.reject_value(self.expected.replace(sentence, replacement, 1))

    def test_oracle_rejects_each_paragraph_omission_duplication_and_reorder(self):
        help_checks.check_paragraph_corruptions(self)

    def test_oracle_rejects_mode_memory_and_other_semantic_corruptions(self):
        mutations = {'unscoped-origin': ('Semasa mencantumkan imej, imej pertama', 'Imej pertama'), 'unscoped-overlap': ('Pertindihan ditolak semasa mencantumkan imej.', 'Pertindihan sentiasa ditolak.'), 'wrong-position-label': ('gunakan Kedudukan tepat', 'gunakan Kedudukan'), 'wrong-corner': ('penjuru kiri atasnya', 'penjuru kanan bawahnya'), 'wrong-origin': ('bermula dari sifar', 'bermula dari satu'), 'wrong-position-unit': ('dalam piksel menggunakan nombor bulat', 'dalam peratus'), 'exact-position-moves-others': ('Imej lain kekal pada kedudukannya', 'Imej lain berubah kedudukan'), 'exact-position-rejects-overlap': ('dan pertindihan dibenarkan.', 'dan pertindihan ditolak.'), 'crop-movement-unconditional': ('Imej yang dicantumkan mungkin bergerak apabila imej induknya dipangkas.', 'Imej yang dicantumkan sentiasa bergerak apabila imej induknya dipangkas.'), 'gap-movement-unconditional': ('imej yang dicantumkan mungkin bergerak untuk mengisi jurang.', 'imej yang dicantumkan sentiasa bergerak untuk mengisi jurang.'), 'unconditional-smaller-output': (' jika pilihan itu ditawarkan.', '.'), 'wrong-tiny-output-branch': ('memaparkan amaran memori dan bukannya pemilih saiz.', 'memaparkan pemilih saiz.'), 'resize-removes-crop': ('tetapi mengekalkan pangkasan.', 'dan membuang pangkasan.'), 'zoom-changes-output': ('ia tidak pernah mengubah dimensi output.', 'ia mengubah dimensi output.'), 'editor-replacement-not-undoable': ('sebagai penggantian yang boleh dibuat asal.', 'sebagai penggantian yang tidak boleh dibuat asal.')}
        for name, (before, after) in mutations.items():
            with self.subTest(mutation=name):
                self.assertEqual(1, self.expected.count(before))
                self.reject_value(self.expected.replace(before, after, 1))

    def test_oracle_rejects_resource_structure_changes(self):
        help_checks.check_resource_structure(self, KEY, require_complete)

    def test_oracle_rejects_unicode_escape_placeholder_and_clause_relocation(self):
        mutations = (
            self.expected.replace('«Tunjuk semua»', 'Tunjuk semua', 1),
            self.expected.replace(r'\n', '\n', 1),
            self.expected.replace(r'\n\n', r'\n', 1),
            self.expected.replace(r'\n\n', r'\n\n\n', 1),
            self.expected + '\r',
            self.expected + ' %1$s',
            self.expected + '\ufffd',
        )
        for value in mutations:
            with self.subTest(value=value):
                self.reject_value(value)
        conditional = 'Imej yang dicantumkan mungkin bergerak apabila imej induknya dipangkas.'
        self.assertEqual(1, self.paragraphs[2].count(conditional))
        moved = list(self.paragraphs)
        moved[2] = moved[2].replace(conditional + ' ', '', 1)
        moved[0] += ' ' + conditional
        self.reject_value(r'\n\n'.join(moved))

    def test_fixture_rejects_wrong_identity_and_malformed_paragraphs(self):
        for field, replacement in (('locale', 'lt'), ('directory', 'values'), ('key', KEY + '_wrong'), ('value', None)):
            broken = dict(self.fixture)
            broken[field] = replacement
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_fixture(broken)
        for field in self.fixture:
            broken = dict(self.fixture)
            del broken[field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                require_fixture(broken)
        broken = dict(self.fixture, extra='not-in-contract')
        with self.assertRaises(ValueError):
            require_fixture(broken)
        for value in (r'\n\n'.join(self.paragraphs[:-1]),
                      self.expected + r'\n\n' + self.paragraphs[-1],
                      self.expected.replace(r'\n\n', r'\n', 1),
                      self.expected.replace(r'\n\n', r'\n\n\n', 1),
                      self.expected.replace(r'\n', '\n', 1), self.expected + '\r',
                      r'\n\n' + r'\n\n'.join(self.paragraphs[1:])):
            with self.subTest(value=value), self.assertRaises(ValueError):
                require_fixture(dict(self.fixture, value=value))


if __name__ == '__main__':
    unittest.main()
