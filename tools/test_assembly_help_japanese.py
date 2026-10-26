"""Complete Japanese assembly Help contract; no whole-catalogue/fluency acceptance.

The complete reviewed value is shared with the real Android Help consumer test.
Host checks cover scope, control names, P3 and corruption; they do not execute UI.
"""
from copy import deepcopy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
KEY = 'ui_add_up_to_20_images_with_android_s'
POSITION = ('画像を選択し、［正確な位置］でその左上隅の X 座標と Y 座標をピクセル単位で指定します。'
            '座標には 0 以上の整数を指定してください。他の画像の位置は変わらず、画像を重ねることもできます。')
GAP = '他の画像は配置済みのままで、接続された画像が隙間を埋めるように移動する場合があります。'


def decoded(value):
    return value.replace(r"\'", "'").replace(r'\"', '"').replace(r'\n', '\n')


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY} or len(nodes[0]):
        raise ValueError('Help key, attributes or markup changed')
    if decoded(nodes[0].text or '') != expected:
        raise ValueError('Complete Help differs')


class JapaneseAssemblyHelpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads((ROOT / 'Paintroid/src/test/resources/assembly-help-japanese/expected.json')
                                  .read_text(encoding='utf-8'))
        cls.root = ET.parse(ROOT / 'Paintroid/src/main/res/values-ja/strings.xml').getroot()
        cls.values = {node.get('name'): decoded(node.text or '')
                      for node in cls.root if node.tag == 'string'}
        cls.help = cls.values[KEY]
        cls.paragraphs = cls.help.split('\n\n')

    def test_complete_japanese_value_and_eight_paragraphs(self):
        self.assertEqual('ja', self.expected['locale'])
        self.assertEqual('values-ja', self.expected['directory'])
        require_complete(self.root, self.expected['help'])
        self.assertEqual(8, len(self.paragraphs))

    def test_snap_and_exact_position_have_different_rules(self):
        snap = self.paragraphs[2]
        self.assertIn('右側への接続では上端がそろい、下側への接続では左端がそろいます。', snap)
        self.assertIn('スナップで配置する場合、最初の画像は原点に配置されます。', snap)
        self.assertIn('親画像をトリミングすると、そこに接続した画像も移動する場合があります。', snap)
        self.assertTrue(snap.endswith('スナップで配置する場合は、画像の重なりは許可されません。'))
        self.assertEqual(POSITION, self.paragraphs[3])
        self.assertIn('［配置解除］は選択した画像だけをトレイへ戻します。' + GAP, self.paragraphs[5])
        self.assertNotIn('後続の画像は隙間を詰めますが、配置済みのままです。', self.help)

    def test_full_review_preserves_units_dimensions_undo_and_conditional_memory(self):
        self.assertIn('トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法', self.paragraphs[0])
        self.assertIn('並べ替えても配置済み画像の位置は変わりません。', self.paragraphs[0])
        self.assertIn('選択した画像の各辺から切り取る量を、ピクセル数またはパーセントで指定します。', self.paragraphs[1])
        self.assertIn('トリミング範囲を元画像全体に戻せます。', self.paragraphs[1])
        self.assertIn('各画像固有の縦横比を維持したまま、すべての入力画像の幅または高さをそろえます。', self.paragraphs[4])
        self.assertIn('寸法の統一だけを解除し、トリミングは保持します。', self.paragraphs[4])
        self.assertIn('［元に戻す］／［やり直す］でこれらの変更を取り消したり、やり直したりできます。', self.paragraphs[5])
        self.assertIn('配置済み画像をドラッグすると配置を変更でき、', self.paragraphs[5])
        self.assertIn('出力寸法は変更しません。', self.paragraphs[5])
        self.assertIn('結合画像でメインエディターの画像を置き換えます。この置き換えは元に戻せます。', self.paragraphs[6])
        self.assertIn('選択画面が表示されたときに小さい出力コピーを選択してください。', self.paragraphs[6])
        self.assertIn('サイズの選択画面の代わりにメモリ警告が表示されます。', self.paragraphs[6])
        self.assertIn('元の画像ファイルは変更されません。', self.paragraphs[6])
        self.assertIn('端末内に保存され、戻ってきたときに再度開かれます。', self.paragraphs[6])
        self.assertIn('Catrobat/AGPL および素材クレジット', self.paragraphs[7])

    def test_help_uses_current_control_names_including_redo_and_units(self):
        self.assertEqual(self.values['ui_assembly_exact_position'], self.expected['positionLabel'])
        for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                    'ui_same_width', 'ui_same_height', 'ui_smallest', 'ui_largest', 'ui_pixels', 'ui_percent',
                    'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all',
                    'ui_undo', 'ui_redo', 'ui_save_png', 'ui_edit_in_paint', 'ui_about_credits23'):
            with self.subTest(key=key):
                self.assertIn('［' + self.values[key] + '］', self.help)

    def test_complete_oracle_rejects_omissions_wrong_claims_and_resource_corruption(self):
        replacements = {
            'unscoped-origin': ('スナップで配置する場合、最初の画像', '最初の画像'),
            'unscoped-overlap': ('スナップで配置する場合は、画像の重なり', '画像の重なり'),
            'guaranteed-gap': (GAP, '後続の画像は隙間を詰めますが、配置済みのままです。'),
            'wrong-origin': ('0 以上の整数', '1 以上の整数'),
            'wrong-units': ('ピクセル単位で指定', 'パーセント単位で指定'),
            'wrong-corner': ('その左上隅', 'その右下隅'),
            'reject-overlap': ('画像を重ねることもできます', '画像を重ねることはできません'),
            'moves-others': ('他の画像の位置は変わらず', '他の画像の位置も変わり'),
            'wrong-position-label': ('［正確な位置］', '［位置の調整］'),
            'wrong-redo-label': ('［やり直す］', '［やり直し］'),
            'wrong-percent-label': ('［パーセント］', '［百分率］'),
            'unconditional-resize': ('選択画面が表示されたときに小さい', '必ず小さい'),
        }
        for name, (old, new) in replacements.items():
            broken = deepcopy(self.root)
            node = broken.find(f"./string[@name='{KEY}']")
            self.assertIn(old, node.text, name)
            node.text = node.text.replace(old, new)
            with self.subTest(mutation=name), self.assertRaises(ValueError):
                require_complete(broken, self.expected['help'])
        for index in range(8):
            broken = deepcopy(self.root)
            node = broken.find(f"./string[@name='{KEY}']")
            paragraphs = node.text.split(r'\n\n')
            del paragraphs[index]
            node.text = r'\n\n'.join(paragraphs)
            with self.subTest(omitted_paragraph=index + 1), self.assertRaises(ValueError):
                require_complete(broken, self.expected['help'])
        for mutation in ('truncated', 'duplicate', 'missing', 'attribute', 'markup'):
            broken = deepcopy(self.root)
            node = broken.find(f"./string[@name='{KEY}']")
            if mutation == 'truncated': node.text = node.text[:-1]
            elif mutation == 'duplicate': broken.append(deepcopy(node))
            elif mutation == 'missing': broken.remove(node)
            elif mutation == 'attribute': node.set('formatted', 'false')
            elif mutation == 'markup': ET.SubElement(node, 'b').text = 'extra'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_complete(broken, self.expected['help'])

    def test_help_remains_p3(self):
        tiers = json.loads((ROOT / 'translations/string-importance.json').read_text())['tiers']
        actual = {key: tier['id'] for tier in tiers for key in tier['keys']}
        self.assertEqual('P3', actual['string/' + KEY])


if __name__ == '__main__':
    unittest.main()
