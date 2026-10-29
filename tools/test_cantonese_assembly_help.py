"""Complete accepted Cantonese assembly Help, not whole-language acceptance.

The fixture is one reviewed value, not a generator or permanent source hash.
Explicit ValueError checks and unittest assertions remain active under python -O.
"""
import json
from pathlib import Path
import unittest
import assembly_help_checks as help_checks

ROOT = Path(__file__).resolve().parents[1]
KEY = 'ui_add_up_to_20_images_with_android_s'
DIRECTORY = 'values-b+yue+Hant'
RESOURCE = ROOT / 'Paintroid/src/main/res' / DIRECTORY / 'strings.xml'
FIXTURE = ROOT / 'tools/fixtures/current_localization/cantonese_assembly_help.json'
CAPTIONS = ('ui_same_width', 'ui_same_height', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop', 'ui_assembly_exact_position', 'ui_smallest', 'ui_largest', 'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all', 'ui_save_png', 'ui_edit_in_paint', 'ui_undo', 'ui_redo', 'ui_menu_file', 'ui_about_credits23')


def require_fixture(fixture):
    if (set(fixture) != {'locale', 'directory', 'key', 'value'}
            or fixture['locale'] != 'yue-Hant' or fixture['directory'] != DIRECTORY
            or fixture['key'] != KEY or not isinstance(fixture['value'], str)):
        raise ValueError('Unexpected Cantonese Help fixture identity')
    value = fixture['value']
    paragraphs = value.split(r'\n\n')
    if (len(paragraphs) != 8 or not all(paragraphs)
            or value.count(r'\n') != 14 or '\n' in value or '\r' in value):
        raise ValueError('Cantonese Help paragraph structure differs')
    return value


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY} or len(nodes[0]):
        raise ValueError('Help key, attributes or child markup changed')
    if nodes[0].text != expected:
        raise ValueError('Complete Cantonese Help differs')


class CantoneseAssemblyHelpTests(unittest.TestCase):
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
        self.assertIn('「' + file_label + '」>「' + about_label + '」', self.paragraphs[7])
        tiers = json.loads((ROOT / 'translations/string-importance.json').read_text(encoding='utf-8'))['tiers']
        actual = {key: tier['id'] for tier in tiers for key in tier['keys']}
        self.assertEqual('P3', actual['string/' + KEY])

    def test_oracle_rejects_each_sentence_omission_and_duplication(self):
        sentences = [sentence + '。' for paragraph in self.paragraphs
                     for sentence in paragraph[:-1].split('。')]
        self.assertEqual(34, len(sentences))
        for sentence in sentences:
            self.assertEqual(1, self.expected.count(sentence))
            for replacement in ('', sentence + ' ' + sentence):
                with self.subTest(sentence=sentence, replacement=replacement):
                    self.reject_value(self.expected.replace(sentence, replacement, 1))

    def test_oracle_rejects_each_paragraph_omission_duplication_and_reorder(self):
        help_checks.check_paragraph_corruptions(self)

    def test_oracle_rejects_mode_memory_and_other_semantic_corruptions(self):
        mutations = {'unscoped-origin': ('用貼齊方式擺位時，第一張圖片由原點開始。', '第一張圖片由原點開始。'), 'unscoped-overlap': ('貼齊時唔容許圖片重疊。', '唔容許圖片重疊。'), 'wrong-position-label': ('「準確位置」', '「位置」'), 'wrong-corner': ('佢左上角嘅 X/Y', '佢右下角嘅 X/Y'), 'wrong-origin': ('由零開始', '由一開始'), 'wrong-position-unit': ('座標以整數像素計', '座標以百分比計'), 'exact-position-moves-others': ('其他圖片會保持原位', '其他圖片會改變位置'), 'exact-position-rejects-overlap': ('而且容許重疊。', '而且唔容許重疊。'), 'crop-movement-unconditional': ('裁剪作為連接基準嘅圖片時，連住佢嘅圖片可能會郁。', '裁剪作為連接基準嘅圖片時，連住佢嘅圖片一定會郁。'), 'gap-movement-unconditional': ('已連接嘅圖片可能會郁嚟填補空位。', '已連接嘅圖片一定會郁嚟填補空位。'), 'unconditional-smaller-output': ('而程式有提供尺寸選擇畫面，請揀較細嘅輸出副本。', '請揀較細嘅輸出副本。'), 'wrong-tiny-output-branch': ('程式會顯示記憶體警告，唔會顯示尺寸選擇畫面。', '程式會顯示尺寸選擇畫面。'), 'resize-removes-crop': ('會取消尺寸統一，但保留裁剪。', '會取消尺寸統一同裁剪。'), 'zoom-changes-output': ('唔會改輸出尺寸。', '會改輸出尺寸。'), 'editor-replacement-not-undoable': ('取代原有圖片，而且可以復原。', '取代原有圖片，而且唔可以復原。'), 'provider-time-unconditional': ('如果檔案提供程式有提供修改時間，亦會顯示。', '一定會顯示修改時間。')}
        self.reject_value('可用 Android 嘅檔案揀器加最多 20 張圖片。下面托盤會喺檔案提供程式有提供資料時，顯示縮圖、檔案名稱、裁剪同「一樣闊度」或者「一樣高度」調整後嘅圖片尺寸及檔案修改時間。你可按檔案名稱或者修改時間排序；排序唔會再排列已擺位嘅圖片。\\n\\n撳縮圖以揀選圖片。「裁剪圖片」會裁剪嗰張圖片；「批次裁剪」會以像素或者百分比邊距套用至揀咗嘅圖片。拖裁剪控制點或者輸入數值。「重設裁剪」會還原原本邊緣。裁剪屬非破壞性操作，可復原。\\n\\n撳住縮圖，或者拖工作區內已擺位嘅圖片，再放到反白顯示嘅邊緣。半透明預覽會顯示準確嘅貼齊結果。接到右邊時會對齊頂端；接到下面時會對齊左邊。你亦可先撳縮圖，再撳「+」目標。第一張圖片由原點開始。裁剪母圖片時，現有連接會隨母圖片郁。不允許圖片互相重疊。\\n\\n「一樣闊度」同「一樣高度」會在保留各圖片本身長寬比例嘅情況下，為所有輸入圖片設定共同尺寸。可以揀像素、百分比、最小或者最大。「還原原本大小」會取消尺寸統一，但保留裁剪。\\n\\n「取消擺位」只會將揀咗嘅圖片放回托盤。後面嘅圖片會填補空位，但仲維持已擺位狀態。「移除」只會刪除嗰個輸入圖片。「復原／重做」可還原呢啲改動。拖已擺位圖片可再排列；拖空白位置可平移視圖。以雙指縮放。「顯示全部」只會縮放視圖以顯示整個拼合結果，唔會改輸出尺寸。\\n\\n「儲存 PNG」會直接儲存拼合後嘅圖片。「喺 Paint 編輯」會將圖片傳送到主編輯器，作為可復原嘅圖片取代操作。如果輸出超出記憶體上限，而程式有提供尺寸選擇畫面，請揀較小嘅輸出副本。如果連極小嘅輸出都超出記憶體上限，程式會顯示記憶體警告，唔會顯示尺寸選擇畫面。原始圖片檔案唔會被修改。而家嘅拼合狀態會儲存喺裝置內，返去呢個功能時會再打開。\\n\\n呢個模式用主編輯器「檔案」>「關於、授權同鳴謝」選單內一樣嘅 Catrobat/AGPL 及素材鳴謝資料。')
        for name, (before, after) in mutations.items():
            with self.subTest(mutation=name):
                self.assertEqual(1, self.expected.count(before))
                self.reject_value(self.expected.replace(before, after, 1))

    def test_oracle_rejects_resource_structure_changes(self):
        help_checks.check_resource_structure(self, KEY, require_complete)

    def test_oracle_rejects_unicode_escape_placeholder_and_clause_relocation(self):
        mutations = (
            self.expected.replace('「顯示全部」', '顯示全部', 1),
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
        conditional = '裁剪作為連接基準嘅圖片時，連住佢嘅圖片可能會郁。'
        self.assertEqual(1, self.paragraphs[2].count(conditional))
        moved = list(self.paragraphs)
        moved[2] = moved[2].replace(conditional, '', 1)
        moved[0] += conditional
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
