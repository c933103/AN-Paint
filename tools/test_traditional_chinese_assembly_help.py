"""Complete HK/TW assembly Help contract; not whole-catalogue acceptance."""
from copy import deepcopy
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as catalogues
from test_review_followup_pr2 import ASSEMBLY_CLAUSES

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'Paintroid/src/test/resources/traditional-chinese-assembly-help'
HELP = 'ui_add_up_to_20_images_with_android_s'
LOCALES = {'zh-HK': 'values-zh-rHK', 'zh-TW': 'values-zh-rTW'}


def decoded(text):
    return text.replace(r"\'", "'").replace(r'\"', '"').replace(r'\n', '\n')


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{HELP}']")
    if len(nodes) != 1:
        raise ValueError('Missing or duplicated Help')
    node = nodes[0]
    if node.attrib != {'name': HELP} or len(node):
        raise ValueError('Help attributes or markup changed')
    if decoded(node.text or '') != expected:
        raise ValueError('Complete Traditional Chinese Help differs')


class TraditionalChineseAssemblyHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roots = {tag: ET.parse(catalogues.RES / folder / 'strings.xml').getroot()
                     for tag, folder in LOCALES.items()}
        cls.expected = {tag: (FIXTURES / f'{tag}.txt').read_text(encoding='utf-8').removesuffix('\n')
                        for tag in LOCALES}

    def test_complete_eight_paragraph_entries_and_android_escaping(self):
        self.assertEqual({f'{tag}.txt' for tag in LOCALES}, {p.name for p in FIXTURES.iterdir()})
        for tag, root in self.roots.items():
            with self.subTest(locale=tag):
                expected = self.expected[tag]
                require_complete(root, expected)
                value = root.find(f"./string[@name='{HELP}']").text
                self.assertEqual(8, len(expected.split('\n\n')))
                self.assertEqual(14, value.count(r'\n'))
                self.assertNotIn('\n', value)
                self.assertEqual({}, catalogues.placeholders(value))
                self.assertEqual([], catalogues.android_string_errors(value))
                self.assertEqual([], catalogues.format_string_errors(value))

    def test_complete_oracle_rejects_every_missing_paragraph_and_structural_change(self):
        for tag, root in self.roots.items():
            paragraphs = self.expected[tag].split('\n\n')
            for index in range(8):
                broken = deepcopy(root)
                broken.find(f"./string[@name='{HELP}']").text = '\n\n'.join(
                    p for i, p in enumerate(paragraphs) if i != index)
                with self.subTest(locale=tag, paragraph=index), self.assertRaises(ValueError):
                    require_complete(broken, self.expected[tag])
            for mutation in ('missing', 'duplicate', 'attribute', 'markup', 'truncated', 'swapped-locale'):
                broken = deepcopy(root)
                node = broken.find(f"./string[@name='{HELP}']")
                if mutation == 'missing': broken.remove(node)
                elif mutation == 'duplicate': broken.append(deepcopy(node))
                elif mutation == 'attribute': node.set('formatted', 'false')
                elif mutation == 'markup': ET.SubElement(node, 'b').text = 'Unexpected'
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'swapped-locale':
                    node.text = self.expected['zh-TW' if tag == 'zh-HK' else 'zh-HK']
                with self.subTest(locale=tag, mutation=mutation), self.assertRaises(ValueError):
                    require_complete(broken, self.expected[tag])

    def test_snap_rules_and_exact_position_are_separate_complete_paragraphs(self):
        for tag, root in self.roots.items():
            with self.subTest(locale=tag):
                paragraphs = self.expected[tag].split('\n\n')
                self.assertIn('貼齊時，第一張圖片由原點開始。', paragraphs[2])
                self.assertIn('貼齊時不允許圖片互相重疊。', paragraphs[2])
                label = decoded(root.find("./string[@name='ui_assembly_exact_position']").text)
                self.assertEqual('精確位置', label)
                start = '由' if tag == 'zh-HK' else '從'
                self.assertEqual('選取圖片後，使用「' + label + '」設定這張圖片左上角的 X 和 Y 座標。'
                                 '座標以整數像素為單位，' + start + '零開始。'
                                 '其他圖片保持目前的位置；此處允許重疊。', paragraphs[3])
                self.assertNotIn('原點', ''.join(p for i, p in enumerate(paragraphs) if i != 2))
                self.assertNotIn('不允許圖片互相重疊', ''.join(p for i, p in enumerate(paragraphs) if i != 2))

    def test_only_modification_time_is_conditional_and_crop_unplace_movement_is_possible(self):
        for tag, expected in self.expected.items():
            with self.subTest(locale=tag):
                paragraphs = expected.split('\n\n')
                self.assertIn('下方托盤會顯示縮圖、檔案名稱，以及', paragraphs[0])
                self.assertIn('如檔案提供者有提供修改時間，', paragraphs[0])
                self.assertNotIn('下方托盤會在檔案提供者有提供資料時', expected)
                crop = '裁剪' if tag == 'zh-HK' else '裁切'
                self.assertIn(crop + '母圖片時，連接到它的圖片可能會移動。', paragraphs[2])
                self.assertIn('「取消放置」只會將所選圖片放回托盤。其他圖片仍維持已放置狀態；'
                              '相連的圖片可能會移動以填補空位。', paragraphs[5])
                self.assertNotIn('後面的圖片會填補空位', expected)
                self.assertNotIn('現有連接會隨母圖片移動', expected)

    def test_actual_control_names_and_prior_crop_dimension_memory_contracts_are_kept(self):
        for tag, root in self.roots.items():
            expected = self.expected[tag]
            paragraphs = expected.split('\n\n')
            for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                        'ui_same_width', 'ui_same_height', 'ui_restore_original_sizes', 'ui_unplace',
                        'ui_remove', 'ui_undo', 'ui_redo', 'ui_show_all', 'ui_save_png', 'ui_edit_in_paint',
                        'ui_menu_file', 'ui_about_credits23'):
                with self.subTest(locale=tag, key=key):
                    self.assertIn(decoded(root.find(f"./string[@name='{key}']").text), expected)
            dimension, warning, unconditional = ASSEMBLY_CLAUSES[tag]
            with self.subTest(locale=tag):
                self.assertIn(dimension, paragraphs[0])
                self.assertIn(warning, paragraphs[6])
                self.assertNotIn(unconditional, expected)
                self.assertIn('而應用程式提供了尺寸選擇畫面，請選擇較小的輸出副本。', paragraphs[6])
                self.assertIn('原始圖片檔案不會被修改。目前的拼合狀態會儲存在裝置內', paragraphs[6])
                self.assertIn('Catrobat/AGPL', paragraphs[7])
                self.assertFalse(re.search(r'%\d+\$', expected))


if __name__ == '__main__':
    unittest.main()
