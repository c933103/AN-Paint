"""Complete accepted Jyutping assembly Help, not whole-language acceptance.

The fixture is one reviewed value, not a generator or permanent source hash.
Explicit ValueError checks and unittest assertions remain active under python -O.
"""
from copy import deepcopy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
KEY = 'ui_add_up_to_20_images_with_android_s'
DIRECTORY = 'values-b+yue+Latn'
RESOURCE = ROOT / 'Paintroid/src/main/res' / DIRECTORY / 'strings.xml'
FIXTURE = ROOT / 'tools/fixtures/current_localization/jyutping_assembly_help.json'
CAPTIONS = ('ui_same_width', 'ui_same_height', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop', 'ui_assembly_exact_position', 'ui_smallest', 'ui_largest', 'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all', 'ui_save_png', 'ui_edit_in_paint', 'ui_undo', 'ui_redo', 'ui_menu_file', 'ui_about_credits23')


def require_fixture(fixture):
    if (set(fixture) != {'locale', 'directory', 'key', 'value'}
            or fixture['locale'] != 'yue-Latn' or fixture['directory'] != DIRECTORY
            or fixture['key'] != KEY or not isinstance(fixture['value'], str)):
        raise ValueError('Unexpected Jyutping Help fixture identity')
    value = fixture['value']
    paragraphs = value.split(r'\n\n')
    if (len(paragraphs) != 8 or not all(paragraphs)
            or value.count(r'\n') != 14 or '\n' in value or '\r' in value):
        raise ValueError('Jyutping Help paragraph structure differs')
    return value


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY} or len(nodes[0]):
        raise ValueError('Help key, attributes or child markup changed')
    if nodes[0].text != expected:
        raise ValueError('Complete Jyutping Help differs')


class JyutpingAssemblyHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding='utf-8'))
        cls.expected = require_fixture(cls.fixture)
        cls.root = ET.parse(RESOURCE).getroot()
        cls.paragraphs = cls.expected.split(r'\n\n')

    def reject_value(self, value):
        self.assertNotEqual(self.expected, value, 'Corruption must not be a no-op')
        broken = deepcopy(self.root)
        broken.find(f"./string[@name='{KEY}']").text = value
        with self.assertRaises(ValueError):
            require_complete(broken, self.expected)

    def test_exact_complete_eight_paragraph_value(self):
        require_complete(self.root, self.expected)
        self.assertEqual(8, len(self.paragraphs))
        self.assertEqual(14, self.expected.count(r'\n'))
        self.assertNotRegex(self.expected, r'%\d+\$')
        english = ET.parse(ROOT / 'Paintroid/src/main/res/values/strings.xml').find(f"./string[@name='{KEY}']").text
        self.assertEqual(8, len(english.split(r'\n\n')))
        self.assertEqual(14, english.count(r'\n'))

    def test_actual_captions_and_existing_p3_scope(self):
        for key in CAPTIONS:
            with self.subTest(key=key):
                nodes = self.root.findall(f"./string[@name='{key}']")
                self.assertEqual(1, len(nodes))
                self.assertIn(nodes[0].text, self.expected)
        file_label = self.root.find("./string[@name='ui_menu_file']").text
        about_label = self.root.find("./string[@name='ui_about_credits23']").text
        self.assertIn('“' + file_label + ' > ' + about_label + '”', self.paragraphs[7])
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
        for index in range(8):
            for kind in ('omit', 'duplicate'):
                changed = list(self.paragraphs)
                if kind == 'omit':
                    del changed[index]
                else:
                    changed.insert(index, changed[index])
                with self.subTest(paragraph=index, mutation=kind):
                    self.reject_value(r'\n\n'.join(changed))
        for index in range(7):
            changed = list(self.paragraphs)
            changed[index], changed[index + 1] = changed[index + 1], changed[index]
            with self.subTest(paragraph=index, mutation='adjacent-swap'):
                self.reject_value(r'\n\n'.join(changed))

    def test_oracle_rejects_mode_memory_and_other_semantic_corruptions(self):
        mutations = {'unscoped-origin': ('Jung6 tip3 cai4 fong1 sik1 baai2 wai6 si4, dai6 jat1 zoeng1 tou4 pin2 wui5 jau4 jyun4 dim2 hoi1 ci2.', 'Dai6 jat1 zoeng1 tou4 pin2 wui5 jau4 jyun4 dim2 hoi1 ci2.'), 'unscoped-overlap': ('Jung6 tip3 cai4 fong1 sik1 baai2 wai6 si4, m4 jung4 heoi2 tou4 pin2 cung4 dip6.', 'M4 jung4 heoi2 tou4 pin2 cung4 dip6.'), 'wrong-position-label': ('“Zeon2 kok3 wai6 zi3”', '“Wai6 zi3”'), 'wrong-corner': ('keoi5 zo2 soeng6 gok3 ge3 X/Y', 'keoi5 jau6 haa6 gok3 ge3 X/Y'), 'wrong-origin': ('jau4 0 hoi1 ci2', 'jau4 1 hoi1 ci2'), 'wrong-position-unit': ('ji5 zing2 sou3 zoeng6 sou3 gai3', 'ji5 baak3 fan1 bei2 gai3'), 'exact-position-moves-others': ('Kei4 taa1 tou4 pin2 wui5 bou2 ci4 jyun4 wai6', 'Kei4 taa1 tou4 pin2 wui5 goi2 bin3 wai6 zi3'), 'exact-position-rejects-overlap': ('ji4 ce2 ni1 dou6 jung4 heoi2 cung4 dip6.', 'ji4 ce2 ni1 dou6 m4 jung4 heoi2 cung4 dip6.'), 'crop-movement-unconditional': ('Coi4 zin2 jat1 zoeng1 tou4 pin2 si4, zip3 hai2 keoi5 bin1 jyun4 ge3 tou4 pin2 ho2 nang4 wui5 juk1.', 'Coi4 zin2 jat1 zoeng1 tou4 pin2 si4, zip3 hai2 keoi5 bin1 jyun4 ge3 tou4 pin2 jat1 ding6 wui5 juk1.'), 'gap-movement-unconditional': ('lin4 zip3 zyu6 ge3 tou4 pin2 ho2 nang4 wui5 juk1 lai4 tin4 bou2 hung1 wai6.', 'lin4 zip3 zyu6 ge3 tou4 pin2 jat1 ding6 wui5 juk1 lai4 tin4 bou2 hung1 wai6.'), 'unconditional-smaller-output': ('ji4 cing4 sik1 jau5 tai4 gung1 cek3 cyun3 syun2 zaak6 waa2 min6, cing2 gaan2 gaau3 siu2 ge3 syu1 ceot1 fu3 bun2.', 'cing2 gaan2 gaau3 siu2 ge3 syu1 ceot1 fu3 bun2.'), 'wrong-tiny-output-branch': ('cing4 sik1 wui5 hin2 si6 gei3 jik1 tai2 ging2 gou3, m4 wui5 hin2 si6 cek3 cyun3 syun2 zaak6 waa2 min6.', 'cing4 sik1 wui5 hin2 si6 cek3 cyun3 syun2 zaak6 waa2 min6.'), 'resize-removes-crop': ('wui5 ceoi2 siu1 cek3 cyun3 tung2 jat1, daan6 bou2 lau4 coi4 zin2.', 'wui5 ceoi2 siu1 cek3 cyun3 tung2 jat1 tung4 coi4 zin2.'), 'zoom-changes-output': ('m4 wui5 goi2 bin3 syu1 ceot1 cek3 cyun3.', 'wui5 goi2 bin3 syu1 ceot1 cek3 cyun3.'), 'editor-replacement-not-undoable': ('zok3 wai4 ho2 fuk6 jyun4 ge3 tou4 pin2 ceoi2 doi6 cou1 zok3.', 'zok3 wai4 m4 ho2 fuk6 jyun4 ge3 tou4 pin2 ceoi2 doi6 cou1 zok3.'), 'provider-time-unconditional': ('jyu4 gwo2 dong2 on3 tai4 gung1 ze2 jau5 tai4 gung1 sau1 goi2 si4 gaan1, tok3 pun4 jik6 wui5 hin2 si6.', 'tok3 pun4 jat1 ding6 wui5 hin2 si6 sau1 goi2 si4 gaan1.')}
        self.reject_value('Ho2 jung6 Android ge3 dong2 on3 gaan2 hei3 gaa1 zeoi3 do1 20 zoeng1 tou4 pin2. haa6 min6 tok3 pun4 wui5 hai2 dong2 on3 tai4 gung1 cing4 sik1 jau5 tai4 gung1 zi1 liu2 si4, hin2 si6 suk1 tou4, dong2 on3 ming4 cing1, coi4 zin2 tung4 “Jat1 joeng6 fut3 dou6” waak6 ze2 “Jat1 joeng6 gou1 dou6” tiu4 zing2 hau6 ge3 tou4 pin2 cek3 cyun3 kap6 dong2 on3 sau1 goi2 si4 gaan1. nei5 ho2 on3 dong2 on3 ming4 cing1 waak6 ze2 sau1 goi2 si4 gaan1 paai4 zeoi6; paai4 zeoi6 m4 wui5 zoi3 paai4 lit6 ji5 baai2 wai6 ge3 tou4 pin2.\\n\\ngam6 suk1 tou4 ji5 gaan2 syun2 tou4 pin2. “coi4 zin2 tou4 pin2 ”wui5 coi4 zin2 go2 zoeng1 tou4 pin2; “pai1 ci3 coi4 zin2 ”wui5 ji5 zoeng6 sou3 waak6 ze2 baak3 fan1 bei2 bin1 keoi5 tou3 jung6 zi3 gaan2 zo2 ge3 tou4 pin2. to1 coi4 zin2 hung3 zai3 dim2 waak6 ze2 syu1 jap6 sou3 zik6. “cung4 cit3 coi4 zin2 ”wui5 waan4 jyun4 jyun4 bun2 bin1 jyun4. coi4 zin2 suk6 fei1 po3 waai6 sing3 cou1 zok3, ho2 fuk6 jyun4.\\n\\ngam6 zyu6 suk1 tou4, waak6 ze2 to1 gung1 zok3 keoi1 noi6 ji5 baai2 wai6 ge3 tou4 pin2, zoi3 fong3 dou3 faan2 baak6 hin2 si6 ge3 bin1 jyun4. bun3 tau3 ming4 jyu6 laam5 wui5 hin2 si6 zeon2 kok3 ge3 tip3 cai4 git3 gwo2. zip3 dou3 jau6 bin1 si4 wui5 deoi3 cai4 ding2 dyun1; zip3 dou3 haa6 min6 si4 wui5 deoi3 cai4 zo2 bin1. nei5 jik6 ho2 sin1 gam6 suk1 tou4, zoi3 gam6 “+”muk6 biu1. dai6 jat1 zoeng1 tou4 pin2 jau4 jyun4 dim2 hoi1 ci2. coi4 zin2 mou5 tou4 pin2 si4, jin6 jau5 lin4 zip3 wui5 ceoi4 mou5 tou4 pin2 juk1. bat1 wan5 heoi2 tou4 pin2 wu6 soeng1 cung4 dip6.\\n\\n“jat1 joeng6 fut3 dou6 ”tung4 “jat1 joeng6 gou1 dou6 ”wui5 zoi6 bou2 lau4 gok3 tou4 pin2 bun2 san1 coeng4 fun1 bei2 lai6 ge3 cing4 fong3 haa6, wai6 so2 jau5 syu1 jap6 tou4 pin2 cit3 ding6 gung6 tung4 cek3 cyun3. ho2 ji5 gaan2 zoeng6 sou3, baak3 fan1 bei2, zeoi3 siu2 waak6 ze2 zeoi3 daai6. “waan4 jyun4 jyun4 bun2 daai6 siu2 ”wui5 ceoi2 siu1 cek3 cyun3 tung2 jat1, daan6 bou2 lau4 coi4 zin2.\\n\\n“ceoi2 siu1 baai2 wai6 ”zi2 wui5 zoeng1 gaan2 zo2 ge3 tou4 pin2 fong3 wui4 tok3 pun4. hau6 min6 ge3 tou4 pin2 wui5 tin4 bou2 hung1 wai6, daan6 zung6 wai4 ci4 ji5 baai2 wai6 zong6 taai3. “ji4 ceoi4 ”zi2 wui5 saan1 ceoi4 go2 go3 syu1 jap6 tou4 pin2. “fuk6 jyun4 ／cung4 zou6 ”ho2 waan4 jyun4 ni1 di1 goi2 dung6. to1 ji5 baai2 wai6 tou4 pin2 ho2 zoi3 paai4 lit6; to1 hung1 baak6 wai6 zi3 ho2 ping4 ji4 si6 tou4. ji5 soeng1 zi2 suk1 fong3. “Hin2 si6 cyun4 bou6”zi2 wui5 suk1 fong3 si6 tou4 ji5 hin2 si6 zing2 go3 ping3 hap6 git3 gwo2, m4 wui5 goi2 syu1 ceot1 cek3 cyun3.\\n\\n“cyu5 cyun4 PNG”wui5 zik6 zip3 cyu5 cyun4 ping3 hap6 hau6 ge3 tou4 pin2. “hai2 Paint pin1 cap1 ”wui5 zoeng1 tou4 pin2 cyun4 sung3 dou3 zyu2 pin1 cap1 hei3, zok3 wai4 ho2 fuk6 jyun4 ge3 tou4 pin2 ceoi2 doi6 cou1 zok3. jyu4 gwo2 syu1 ceot1 ciu1 ceot1 gei3 jik1 tai2 soeng6 haan6, ji4 cing4 sik1 jau5 tai4 gung1 cek3 cyun3 syun2 zaak6 waa2 min6, cing2 gaan2 gaau3 siu2 ge3 syu1 ceot1 fu3 bun2. jyu4 gwo2 lin4 gik6 siu2 ge3 syu1 ceot1 dou1 ciu1 ceot1 gei3 jik1 tai2 soeng6 haan6, cing4 sik1 wui5 hin2 si6 gei3 jik1 tai2 ging2 gou3, m4 wui5 hin2 si6 cek3 cyun3 syun2 zaak6 waa2 min6. jyun4 ci2 tou4 pin2 dong2 on3 m4 wui5 bei6 sau1 goi2. ji4 gaa1 ge3 ping3 hap6 zong6 taai3 wui5 cyu5 cyun4 hai2 zong1 zi3 noi6, faan1 heoi3 ni1 go3 gung1 nang4 si4 wui5 zoi3 daa2 hoi1.\\n\\nni1 go3 mou4 sik1 jung6 zyu2 pin1 cap1 hei3 “Dong2 on3” > “Gwaan1 jyu1, sau6 kyun4 tung4 ming4 ze6”syun2 daan1 noi6 jat1 joeng6 ge3 Catrobat/AGPL kap6 sou3 coi4 ming4 ze6 zi1 liu2.')
        for name, (before, after) in mutations.items():
            with self.subTest(mutation=name):
                self.assertEqual(1, self.expected.count(before))
                self.reject_value(self.expected.replace(before, after, 1))

    def test_oracle_rejects_resource_structure_changes(self):
        for mutation in ('missing', 'duplicate', 'wrong-key', 'attribute', 'markup', 'empty', 'truncated'):
            broken = deepcopy(self.root)
            node = broken.find(f"./string[@name='{KEY}']")
            if mutation == 'missing': broken.remove(node)
            elif mutation == 'duplicate': broken.append(deepcopy(node))
            elif mutation == 'wrong-key': node.set('name', KEY + '_wrong')
            elif mutation == 'attribute': node.set('formatted', 'false')
            elif mutation == 'markup': ET.SubElement(node, 'b').text = 'Unexpected'
            elif mutation == 'empty': node.text = None
            elif mutation == 'truncated': node.text = node.text[:-1]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_complete(broken, self.expected)

    def test_oracle_rejects_unicode_escape_placeholder_and_clause_relocation(self):
        mutations = (
            self.expected.replace('“Hin2 si6 cyun4 bou6”', 'Hin2 si6 cyun4 bou6', 1),
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
        conditional = 'Coi4 zin2 jat1 zoeng1 tou4 pin2 si4, zip3 hai2 keoi5 bin1 jyun4 ge3 tou4 pin2 ho2 nang4 wui5 juk1.'
        self.assertEqual(1, self.paragraphs[2].count(conditional))
        moved = list(self.paragraphs)
        moved[2] = moved[2].replace(conditional + ' ', '', 1)
        moved[0] += ' ' + conditional
        self.assertEqual(0, moved[2].count(conditional))
        self.assertEqual(1, moved[0].count(conditional))
        self.assertEqual(1, r'\n\n'.join(moved).count(conditional))
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
