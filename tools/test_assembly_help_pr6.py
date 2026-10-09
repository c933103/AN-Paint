"""PR #6 assembly-help clause regressions, scoped to its six canonical locales.

Source: https://github.com/c933103/AN-Paint/pull/6#discussion_r4213751711
Behavior checked by inspection at 8e8f90cd4b0a3feea7537e4b2f68e88b8fbb49c9:
AssemblyActivity.kt:140,155 uses placedSize; ImageAssembly.kt:22-30 includes
normalization; AssemblyRenderer.kt:38-47 returns null when even 1x1 cannot fit;
AssemblyActivity.kt:290-295 warns and returns before constructing a size chooser.

These literal clause checks deliberately prevent the identified regressions,
not all semantic errors. Their candidate wording requires locale review before
acceptance; future reviewed paraphrases should update these small expectations.
"""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / 'Paintroid/src/main/res'
KEY = 'ui_add_up_to_20_images_with_android_s'

CASES = {'lzh-Hant': {'folder': 'values-b+lzh+Hant',
              'old_dimensions': '裁切之寸',
              'dimensions': '裁切及「同寬」或「同高」調整後之圖寸',
              'old_memory': '若輸出逾記憶體限，宜擇較小副本。',
              'choice': '若輸出逾記憶體限，且程式示尺寸選單，宜擇較小副本。',
              'warning': '若輸出雖極小仍逾限，程式但示記憶體警告，不示尺寸選單。'},
 'hak-Hant-TW': {'folder': 'values-b+hak+Hant+TW',
                 'old_dimensions': '裁切尺寸',
                 'dimensions': '裁切摎用「相同闊度」抑係「相同高度」後个圖像尺寸',
                 'old_memory': '輸出若係超過記憶體上限，請揀較細个輸出副本。',
                 'choice': '輸出若係超過記憶體上限，程式若係有提供尺寸揀取畫面，請揀較細个輸出副本。',
                 'warning': '輸出就算縮到當細還係超過上限个時節，程式會顯示記憶體警告，毋會顯示尺寸揀取畫面。'},
 'hak-Latn-TW': {'folder': 'values-b+hak+Latn+TW',
                 'old_dimensions': 'chhài-chhiet chhak-chhun',
                 'dimensions': 'chhài-chhiet lâu yung “Siông-thùng fat thu” ia-he “Siông-thùng kô-thu” heu '
                               'ke thù-siong chhak-chhun',
                 'old_memory': 'Sû-chhut na-he chhêu-ko ki-yit-thí sông-han, chhiáng kién kha-se ke sû-chhut '
                               'fu-pún.',
                 'choice': 'Sû-chhut na-he chhêu-ko ki-yit-thí sông-han, chhàng-sṳt na-he yû thì-kiûng '
                           'chhak-chhun kién-chhí fa-mien, chhiáng kién kha-se ke sû-chhut fu-pún.',
                 'warning': 'Sû-chhut chhiu-son sok to tông-se hàn-he chhêu-ko sông-han ke sṳ̀-chiet, '
                            'chhàng-sṳt voi hién-sṳ ki-yit-thí kín-ko, m̀-voi hién-sṳ chhak-chhun kién-chhí '
                            'fa-mien.'},
 'nan-Hant-TW': {'folder': 'values-b+nan+Hant+TW',
                 'old_dimensions': '裁切尺寸',
                 'dimensions': '裁切佮用「相同闊度」抑是「相同高度」調整了後的圖片尺寸',
                 'old_memory': '輸出若超過記憶體上限，請揀較細的輸出副本。',
                 'choice': '輸出若超過記憶體上限，程式若有提供尺寸選取畫面，請揀較細的輸出副本。',
                 'warning': '輸出就算縮甲真細猶是超過上限的時陣，程式會顯示記憶體警告，袂顯示尺寸選取畫面。'},
 'nan-Latn-TW': {'folder': 'values-b+nan+Latn+TW',
                 'old_dimensions': 'chhâi-chhiat chhioh-chhùn',
                 'dimensions': 'chhâi-chhiat kah ēng “Sio-tâng khoah-tō͘” ia̍h-sī “Sio-tâng ko-tō͘” '
                               'tiâu-chéng liáu-āu ê tô͘-phìⁿ chhioh-chhùn',
                 'old_memory': 'Su-chhut nā chhiau-kòe kì-ek-thé siōng-hān, chhiáⁿ kéng khah sè ê su-chhut '
                               'hù-pún.',
                 'choice': 'Su-chhut nā chhiau-kòe kì-ek-thé siōng-hān, thêng-sek nā ū thê-kiong '
                           'chhioh-chhùn soán-chhú ōe-bīn, chhiáⁿ kéng khah sè ê su-chhut hù-pún.',
                 'warning': 'Su-chhut chiū-sǹg siok kah chin sè iáu sī chhiau-kòe siōng-hān ê sî-chūn, '
                            'thêng-sek ē hián-sī kì-ek-thé kéng-kò, bē hián-sī chhioh-chhùn soán-chhú '
                            'ōe-bīn.'},
 'wuu-Hans': {'folder': 'values-b+wuu+Hans',
              'old_dimensions': '裁剪尺寸',
              'dimensions': '裁剪搭用「相同宽度」或「相同高度」调整后个图片尺寸',
              'old_memory': '假使输出超出内存上限，请拣小眼个输出副本。',
              'choice': '假使输出超出内存上限，程序有提供尺寸选择画面个辰光，请拣小眼个输出副本。',
              'warning': '输出就算缩得邪气小也超出上限个辰光，程序会显示内存警告，勿会显示尺寸选择画面。'}}


def catalogue(tag):
    path = RES / CASES[tag]['folder'] / 'strings.xml'
    nodes = ET.parse(path).getroot()
    keys = [node.get('name') for node in nodes]
    if keys.count(KEY) != 1:
        raise AssertionError(f'{tag}: expected exactly one {KEY}')
    values = {node.get('name'): ''.join(node.itertext()) for node in nodes}
    paragraphs = values[KEY].split(r'\n\n')
    if len(paragraphs) != 7:
        raise AssertionError(f'{tag}: assembly help paragraph structure changed')
    return values, paragraphs


class AssemblyHelpPr6Tests(unittest.TestCase):
    def test_scope_is_the_six_active_pr6_catalogues(self):
        self.assertEqual(set(CASES), {
            'lzh-Hant', 'hak-Hant-TW', 'hak-Latn-TW',
            'nan-Hant-TW', 'nan-Latn-TW', 'wuu-Hans',
        })
        picker = {node.text for node in ET.parse(RES / 'values/app_language_tags.xml').findall('.//item')}
        self.assertLessEqual(set(CASES), picker)
        for tag, case in CASES.items():
            self.assertEqual(case['folder'], 'values-b+' + tag.replace('-', '+'))


def dimension_test(tag):
    def test(self):
        values, paragraphs = catalogue(tag)
        case = CASES[tag]
        self.assertIn(case['dimensions'], paragraphs[0], tag + ': tray must describe crop and normalization')
        self.assertNotIn(case['old_dimensions'], paragraphs[0])
        for key in ('ui_same_width', 'ui_same_height'):
            self.assertIn(values[key], paragraphs[0], tag + ': name the actual local normalization caption')
        if 'Latn' in tag:
            self.assertNotRegex(values[KEY], r'[\u3400-\u9fff\U00020000-\U000323af]')
    return test


def choice_test(tag):
    def test(self):
        _, paragraphs = catalogue(tag)
        case = CASES[tag]
        self.assertIn(case['choice'], paragraphs[5], tag + ': smaller-copy choice must be conditional on being offered')
        self.assertNotIn(case['old_memory'], paragraphs[5], tag + ': unconditional choice instruction returned')
    return test


def warning_test(tag):
    def test(self):
        _, paragraphs = catalogue(tag)
        self.assertIn(CASES[tag]['warning'], paragraphs[5], tag + ': tiny output may yield a memory warning instead of a chooser')
    return test


for tag in CASES:
    suffix = tag.replace('-', '_')
    setattr(AssemblyHelpPr6Tests, 'test_tray_dimensions_' + suffix, dimension_test(tag))
    setattr(AssemblyHelpPr6Tests, 'test_conditional_choice_' + suffix, choice_test(tag))
    setattr(AssemblyHelpPr6Tests, 'test_warning_instead_of_chooser_' + suffix, warning_test(tag))


if __name__ == '__main__':
    unittest.main()
