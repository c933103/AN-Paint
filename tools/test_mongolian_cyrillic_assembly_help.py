"""Complete accepted Cyrillic Mongolian assembly Help, not whole-language acceptance.

Independent exact-value acceptance: PR56 issuecomment 6342506827.
PR8 withdrawal, PR67 six controls and separate memory warnings retain their scopes.
This host oracle does not certify vertical text, rendering or runtime behavior.

The fixture is one reviewed value, not a generator or permanent source hash.
Explicit ValueError checks and unittest assertions remain active under python -O.
"""
import json
from pathlib import Path
import unittest
import assembly_help_checks as help_checks

ROOT = Path(__file__).resolve().parents[1]
KEY = 'ui_add_up_to_20_images_with_android_s'
DIRECTORY = 'values-b+mn+Cyrl+MN'
RESOURCE = ROOT / 'Paintroid/src/main/res' / DIRECTORY / 'strings.xml'
FIXTURE = ROOT / 'tools/fixtures/current_localization/mongolian_cyrillic_assembly_help.json'
CAPTIONS = ('ui_menu_file', 'ui_about_credits23', 'ui_undo', 'ui_redo', 'ui_batch_crop', 'ui_crop_image', 'ui_edit_in_paint', 'ui_largest', 'ui_remove', 'ui_reset_crop', 'ui_restore_original_sizes', 'ui_same_height', 'ui_same_width', 'ui_save_png', 'ui_show_all', 'ui_smallest', 'ui_unplace', 'ui_assembly_exact_position')
SENTENCES = ('Android-ын файл сонгогчоор 20 хүртэл зураг нэмнэ.', 'Доод тавиурт өнгөц зураг, файлын нэр, тайралт болон «Ижил өргөн» эсвэл «Ижил өндөр» тохируулгын дараах зургийн хэмжээ, мөн үйлчилгээ үзүүлэгчээс өгсөн тохиолдолд файлын өөрчлөгдсөн хугацаа харагдана.', 'Файлын нэр эсвэл өөрчлөгдсөн хугацаагаар эрэмбэлж болно; эрэмбэлэхэд байрлуулсан зургуудын байрлал өөрчлөгдөхгүй.', 'Өнгөц зургийг товшиж сонгоно.', '«Зураг тайрах» нь тухайн зургийг тайрна; «Бөөнөөр тайрах» нь сонгосон зургуудын ирмэгээс пикселээр эсвэл хувиар заасан хэмжээгээр тайрна.', 'Тайрах бариулыг чирэх эсвэл хэмжээг тоогоор оруулна.', '«Тайралтыг сэргээх» нь анхны ирмэгүүдийг сэргээнэ.', 'Тайрах нь эх зургийг өөрчлөхгүй бөгөөд тайралтыг буцааж болно.', 'Өнгөц зургийг удаан дарж, эсвэл ажлын талбарт байгаа зургийг чирээд тодруулсан ирмэг дээр тавина.', 'Хагас тунгалаг урьдчилсан харагдац нь ирмэгт залгаж байрлуулахад гарах үр дүнг яг таг харуулна.', 'Баруун талд залгахад дээд ирмэгүүд, доод талд залгахад зүүн ирмэгүүд зэрэгцэнэ.', 'Мөн өнгөц зургийг товшоод дараа нь + тэмдэгтэй байг товшиж болно.', 'Ирмэгт залгаж байрлуулах үед эхний зураг координатын эхлэл цэгээс эхэлнэ.', 'Залгаж байрлуулсан зургууд нь залгасан суурь зургийг нь тайрахад шилжиж болно.', 'Ирмэгт залгаж байрлуулах үед зураг давхцахыг зөвшөөрөхгүй.', 'Зургийг сонгоод «Яг таг байрлал»-аар зүүн дээд булангийн X/Y координатыг тэгээс эхлэх бүхэл пикселээр тохируулна.', 'Бусад зургийн байрлал өөрчлөгдөхгүй бөгөөд зургуудыг давхцуулж болно.', '«Ижил өргөн» болон «Ижил өндөр» нь зураг бүрийн өргөн, өндрийн харьцааг хадгалж, бүх оролтын зургийн өргөн эсвэл өндрийг ижил болгоно.', 'Пиксел, хувь, «Хамгийн бага» эсвэл «Хамгийн их»-ийг сонгоно.', '«Анхны хэмжээг сэргээх» нь хэмжээг ижилсүүлсэн тохируулгыг цуцалж, тайралтыг хэвээр үлдээнэ.', '«Байрлалаас гаргах» нь зөвхөн сонгосон зургийг тавиурт буцаана.', 'Бусад зураг байрлуулсан хэвээр үлдэнэ; залгаж байрлуулсан зургууд сул зайг нөхөхөөр шилжиж болно.', '«Устгах» нь зөвхөн тухайн оролтын зургийг устгана.', '«Буцаах» болон «Дахин хийх»-ээр эдгээр өөрчлөлтийг буцааж, дахин хийж болно.', 'Байрлуулсан зургийг чирж дахин байрлуулна; хоосон зайг чирэхэд харагдац шилжинэ.', 'Хоёр хуруугаар чимхэх хөдөлгөөнөөр харагдацыг томруулж, жижигрүүлнэ.', '«Бүгдийг харуулах» нь бүх эвлүүлгийг багтаан харуулахаар харагдацын томруулалтыг тохируулна; гаралтын хэмжээг огт өөрчлөхгүй.', '«PNG хадгалах» нь эвлүүлсэн зургийг шууд хадгална.', '«Paint-д засах» нь эвлүүлсэн зургийг үндсэн засварлагч руу шилжүүлж, одоогийн зургийг буцааж болох үйлдлээр солино.', 'Гаралт санах ойн хязгаараас давбал жижиг хэмжээтэй гаралтын хуулбар сонгох боломж санал болгосон тохиолдолд түүнийг сонгоно.', 'Маш жижиг гаралт ч хязгаараас давбал апп хэмжээ сонгогчийн оронд санах ойн анхааруулга харуулна.', 'Эх зургийн файлууд өөрчлөгдөхгүй.', 'Одоогийн эвлүүлгийг төхөөрөмжид хадгалж, буцаж ороход дахин нээнэ.', 'Энэ горимд үндсэн засварлагчийн «Файл > Тухай, лиценз ба талархал» самбарт харуулсан Catrobat/AGPL болон ашигласан материалын талаарх талархлын мэдээллийг мөн ашиглана.')


def require_fixture(fixture):
    if (set(fixture) != {'locale', 'directory', 'key', 'value'}
            or fixture['locale'] != 'mn-Cyrl-MN' or fixture['directory'] != DIRECTORY
            or fixture['key'] != KEY or not isinstance(fixture['value'], str)):
        raise ValueError('Unexpected Cyrillic Mongolian Help fixture identity')
    value = fixture['value']
    paragraphs = value.split(r'\n\n')
    if (len(paragraphs) != 8 or not all(paragraphs)
            or value.count(r'\n') != 14 or '\n' in value or '\r' in value):
        raise ValueError('Cyrillic Mongolian Help paragraph structure differs')
    return value


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY} or len(nodes[0]):
        raise ValueError('Help key, attributes or child markup changed')
    if nodes[0].text != expected:
        raise ValueError('Complete Cyrillic Mongolian Help differs')


class CyrillicMongolianAssemblyHelpTests(unittest.TestCase):
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
        self.assertIn('«' + file_label + ' > ' + about_label + '»', self.paragraphs[7])
        tiers = json.loads((ROOT / 'translations/string-importance.json').read_text(encoding='utf-8'))['tiers']
        actual = {key: tier['id'] for tier in tiers for key in tier['keys']}
        self.assertEqual('P3', actual['string/' + KEY])

    def test_oracle_rejects_each_sentence_omission_and_duplication(self):
        sentences = SENTENCES
        self.assertEqual(34, len(sentences))
        for sentence in sentences:
            self.assertEqual(1, self.expected.count(sentence))
            for replacement in ('', sentence + sentence):
                with self.subTest(sentence=sentence, replacement=replacement):
                    self.reject_value(self.expected.replace(sentence, replacement, 1))

    def test_oracle_rejects_each_paragraph_omission_duplication_and_reorder(self):
        help_checks.check_paragraph_corruptions(self)

    def test_oracle_rejects_mode_memory_and_other_semantic_corruptions(self):
        mutations = {'unscoped-origin': ('Ирмэгт залгаж байрлуулах үед эхний зураг координатын эхлэл цэгээс эхэлнэ.', 'Эхний зураг координатын эхлэл цэгээс эхэлнэ.'), 'unscoped-overlap': ('Ирмэгт залгаж байрлуулах үед зураг давхцахыг зөвшөөрөхгүй.', 'Зураг давхцахыг зөвшөөрөхгүй.'), 'wrong-position-label': ('«Яг таг байрлал»', '«Байрлал»'), 'wrong-corner': ('зүүн дээд булангийн X/Y', 'баруун доод булангийн X/Y'), 'wrong-origin': ('тэгээс эхлэх', 'нэгээс эхлэх'), 'wrong-position-unit': ('бүхэл пикселээр', 'хувиар'), 'exact-position-moves-others': ('Бусад зургийн байрлал өөрчлөгдөхгүй', 'Бусад зургийн байрлал өөрчлөгдөнө'), 'exact-position-rejects-overlap': ('зургуудыг давхцуулж болно.', 'зургуудыг давхцуулж болохгүй.'), 'crop-movement-unconditional': ('залгасан суурь зургийг нь тайрахад шилжиж болно.', 'залгасан суурь зургийг нь тайрахад заавал шилжинэ.'), 'gap-movement-unconditional': ('сул зайг нөхөхөөр шилжиж болно.', 'сул зайг нөхөхөөр заавал шилжинэ.'), 'unconditional-smaller-output': ('жижиг хэмжээтэй гаралтын хуулбар сонгох боломж санал болгосон тохиолдолд түүнийг сонгоно.', 'жижиг хэмжээтэй гаралтын хуулбар сонгоно.'), 'wrong-tiny-output-branch': ('санах ойн анхааруулга харуулна.', 'хэмжээ сонгогч харуулна.'), 'resize-removes-crop': ('тайралтыг хэвээр үлдээнэ.', 'тайралтыг арилгана.'), 'zoom-changes-output': ('гаралтын хэмжээг огт өөрчлөхгүй.', 'гаралтын хэмжээг өөрчилнө.'), 'editor-replacement-not-undoable': ('буцааж болох үйлдлээр солино.', 'буцааж болохгүй үйлдлээр солино.')}
        for name, (before, after) in mutations.items():
            with self.subTest(mutation=name):
                self.assertEqual(1, self.expected.count(before))
                self.reject_value(self.expected.replace(before, after, 1))

    def test_oracle_rejects_resource_structure_changes(self):
        help_checks.check_resource_structure(self, KEY, require_complete)

    def test_oracle_rejects_unicode_escape_placeholder_and_clause_relocation(self):
        mutations = (
            self.expected.replace('Android', 'Аndroid', 1),
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
        conditional = 'Залгаж байрлуулсан зургууд нь залгасан суурь зургийг нь тайрахад шилжиж болно.'
        self.assertEqual(1, self.paragraphs[2].count(conditional))
        moved = list(self.paragraphs)
        moved[2] = moved[2].replace(conditional, '', 1)
        moved[0] += conditional
        self.reject_value(r'\n\n'.join(moved))

    def test_fixture_rejects_wrong_identity_and_malformed_paragraphs(self):
        for field, replacement in (('locale', 'mn-Mong'), ('directory', 'values'), ('key', KEY + '_wrong'), ('value', None)):
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
