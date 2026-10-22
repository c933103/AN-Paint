"""Complete accepted SimplifiedChinese assembly Help, not whole-language acceptance.

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
DIRECTORY = 'values-zh-rCN'
RESOURCE = ROOT / 'Paintroid/src/main/res' / DIRECTORY / 'strings.xml'
FIXTURE = ROOT / 'tools/fixtures/current_localization/simplified_chinese_assembly_help.json'
CAPTIONS = ('ui_same_width', 'ui_same_height', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop', 'ui_assembly_exact_position', 'ui_smallest', 'ui_largest', 'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all', 'ui_save_png', 'ui_edit_in_paint', 'ui_undo', 'ui_redo', 'ui_menu_file', 'ui_about_credits23')


def require_fixture(fixture):
    if (set(fixture) != {'locale', 'directory', 'key', 'value'}
            or fixture['locale'] != 'zh-CN' or fixture['directory'] != DIRECTORY
            or fixture['key'] != KEY or not isinstance(fixture['value'], str)):
        raise ValueError('Unexpected SimplifiedChinese Help fixture identity')
    value = fixture['value']
    paragraphs = value.split(r'\n\n')
    if (len(paragraphs) != 8 or not all(paragraphs)
            or value.count(r'\n') != 14 or '\n' in value or '\r' in value):
        raise ValueError('SimplifiedChinese Help paragraph structure differs')
    return value


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY} or len(nodes[0]):
        raise ValueError('Help key, attributes or child markup changed')
    if nodes[0].text != expected:
        raise ValueError('Complete SimplifiedChinese Help differs')


class SimplifiedChineseAssemblyHelpTests(unittest.TestCase):
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
            for replacement in ('', sentence + sentence):
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
        mutations = {'unscoped-origin': ('使用吸附放置时，第一张图片从原点开始放置。', '第一张图片从原点开始放置。'), 'unscoped-overlap': ('使用吸附放置时，不允许图片重叠。', '不允许图片重叠。'), 'wrong-position-label': ('「精确位置」', '「位置」'), 'wrong-corner': ('左上角的 X/Y', '右下角的 X/Y'), 'wrong-origin': ('从零开始', '从一开始'), 'wrong-position-unit': ('以整数像素为单位', '以百分比为单位'), 'exact-position-moves-others': ('其他图片的位置保持不变', '其他图片的位置随之改变'), 'exact-position-rejects-overlap': ('且允许图片重叠。', '且不允许图片重叠。'), 'crop-movement-unconditional': ('裁剪作为连接基准的图片时，连接到它的图片可能会移动。', '裁剪作为连接基准的图片时，连接到它的图片一定会移动。'), 'gap-movement-unconditional': ('通过吸附连接的图片可能会移动以填补空位。', '通过吸附连接的图片一定会移动以填补空位。'), 'unconditional-smaller-output': ('而应用提供了尺寸选择界面，请选择较小的输出副本。', '请选择较小的输出副本。'), 'wrong-tiny-output-branch': ('应用会显示内存警告，而不会显示尺寸选择界面。', '应用会显示尺寸选择界面。'), 'resize-removes-crop': ('会取消尺寸统一，但保留裁剪。', '会取消尺寸统一和裁剪。'), 'zoom-changes-output': ('绝不会改变输出尺寸。', '会改变输出尺寸。'), 'editor-replacement-not-undoable': ('此操作可撤销。', '此操作不可撤销。'), 'provider-time-unconditional': ('如果文件提供方提供了文件修改时间，也会显示该时间。', '一定会显示文件修改时间。')}
        self.reject_value('可使用 Android 的文件选择器加入最多 20 张图片。下方托盘会在文件提供者有提供数据时，显示缩略图、文件名称、裁剪及「相同宽度」或「相同高度」调整后的图片尺寸及文件修改时间。你可按文件名称或修改时间排序；排序不会重新排列已放置的图片。\\n\\n点按缩略图以选择图片。「裁剪图片」会裁剪该图片；「批次裁剪」会以像素或百分比边距应用至所选图片。拖动裁剪控制点或输入数值。「重设裁剪」会还原原来边缘。裁剪属非破坏性操作，可撤销。\\n\\n长按缩略图，或拖动工作区内已放置的图片，再放到反白显示的边缘。半透明预览会显示准确的贴齐结果。接到右方时会对齐顶端；接到下方时会对齐左边。您也可以先点按缩略图，再点按「+」目标。第一张图片由原点开始。裁剪母图片时，现有连接会随母图片移动。不允许图片互相重叠。\\n\\n「相同宽度」和「相同高度」会在保留各图片本身宽高比的情况下，为所有输入图片设置共同尺寸。可选像素、百分比、最小或最大。「还原原本大小」会取消尺寸统一，但保留裁剪。\\n\\n「取消放置」只会将所选图片放回托盘。后面的图片会填补空位，但仍维持已放置状态。「移除」只会删除该输入图片。「撤销/重做」可还原这些变更。拖动已放置图片可重新排列；拖动空白位置可平移视图。以双指缩放。「显示全部」只会缩放视图以显示整个拼合结果，不会改变输出尺寸。\\n\\n「保存 PNG」会直接保存拼合后的图片。「在 Paint 编辑」会将图片传送到主编辑器，作为可撤销的图片取代操作。如果输出超出内存上限，而应用提供了尺寸选择界面，请选择较小的输出副本。如果连极小的输出也超出内存上限，应用会显示内存警告，而不会显示尺寸选择界面。原始图片文件不会被修改。目前的拼合状态会保存在设备内，返回此功能时会重新打开。\\n\\n此模式使用主编辑器「文件」>「关于、许可与致谢」菜单内相同的 Catrobat/AGPL 及素材致谢数据。')
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
            self.expected.replace('「显示全部」', '显示全部', 1),
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
        conditional = '裁剪作为连接基准的图片时，连接到它的图片可能会移动。'
        self.assertEqual(1, self.paragraphs[2].count(conditional))
        moved = list(self.paragraphs)
        moved[2] = moved[2].replace(conditional, '', 1)
        moved[0] += conditional
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
