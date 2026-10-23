"""Bound one accepted complete Jeju Help value, not language or runtime certification.

XML is canonical. The digest binds only this exact reviewed value, not a whole
source snapshot. PR67 controls, PR9 reset and the two-warning HOLD are separate.
Explicit ValueError/unittest checks remain active under python -O.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
KEY = 'ui_add_up_to_20_images_with_android_s'
CATALOGUE_PATH = 'Paintroid/src/main/res/values-b+jje/strings.xml'
ACCEPTED_SHA256 = 'e0ffcda58a6e999e464c80ba16fb91c7af8a0553f04489c2c6fe0503e2be969b'
REVIEW_URL = 'https://github.com/c933103/AN-Paint/pull/56#issuecomment-6337746630'
REVIEW_LIMIT = ('Moderate-confidence model linguistic acceptance of this exact complete Jeju Help value only; not '
 'native-human, whole-language, runtime, or acceptance of either separately held memory-warning '
 'resource.')
CAPTIONS = (('ui_crop_image', '이미지 자르기', (1,)),
 ('ui_batch_crop', '일괄 자르기', (1,)),
 ('ui_reset_crop', '자르기 초기화', (1,)),
 ('ui_assembly_exact_position', '정확헌 위치', (3,)),
 ('ui_same_width', '같은 너비', (0, 4)),
 ('ui_same_height', '같은 높이', (0, 4)),
 ('ui_smallest', '가장 작게', (4,)),
 ('ui_largest', '가장 크게', (4,)),
 ('ui_restore_original_sizes', '원래 크기 복원', (4,)),
 ('ui_unplace', '배치 해제', (5,)),
 ('ui_remove', '제거', (5,)),
 ('ui_undo', '실행 취소', (1, 5, 6)),
 ('ui_redo', '재실행', (5,)),
 ('ui_show_all', '모두 표시', (5,)),
 ('ui_save_png', 'PNG 저장', (6,)),
 ('ui_edit_in_paint', 'Paint에서 편집', (6,)),
 ('ui_menu_file', '파일', (0, 6, 7)),
 ('ui_about_credits23', '앱 정보, 라이선스 및 크레딧', (7,)))
SEMANTIC_MUTATIONS = ((0, '자르기영 「같은 너비」나 「같은 높이」로 맞춘 것을 반영헌 이미지 크기', '원래 이미지 크기'),
 (0, '파일 고친 시간은 파일 제공자가 보내 주민 보입네다.', '파일 고친 시간은 몬딱 보입네다.'),
 (0, '그 차례를 바꾸어도 작업 공간에 이미 놓은 이미지 자리는 그대로우다.', '그 차례를 바꾸민 이미지 자리도 바뀝네다.'),
 (1, '잘라도 원본은 그대로곡 「실행 취소」로 되돌릴 수 이수다.', '잘라 놓은 것은 되돌릴 수 엇수다.'),
 (2, '반투명 미리보기', '불투명 미리보기'),
 (2, '오른쪽으로 붙이민 위 가장자리가 맞춰지곡', '오른쪽으로 붙이민 아래 가장자리가 맞춰지곡'),
 (2, '아래로 붙이민 왼쪽 가장자리가 맞춰집네다.', '아래로 붙이민 오른쪽 가장자리가 맞춰집네다.'),
 (2, '가장자리에 맞춰 붙일 때는 첫 이미지가 원점에 놓입네다.', '첫 이미지는 몬딱 원점에 놓입네다.'),
 (2, '다른 이미지가 붙어 이신 기준 이미지를 자르민 거기에 붙은 이미지덜도 움직일 수도 이수다.', '기준 이미지를 자르민 몬딱 움직입네다.'),
 (2, '가장자리에 맞춰 붙일 때는 서로 겹치게 놓을 수 엇수다.', '이미지는 언제나 겹치게 놓을 수 엇수다.'),
 (3, '왼쪽 위 모서리 X/Y 좌표를 0서 시작허는 정수 픽셀 값', '가운데 X/Y 좌표를 소수 픽셀 값'),
 (3, '다른 이미지의 위치는 바꾸지 안헙네다.', '다른 이미지의 위치도 바꿉네다.'),
 (3, '이디서는 이미지가 겹쳐도 뒙네다.', '이디서는 이미지가 겹치민 안뒙네다.'),
 (4, '경허여도 이미지마다 제 가로세로 비율은 그대로우다.', '이미지 비율도 몬딱 같게 맞춥네다.'),
 (4, '크기를 같게 맞춘 것만 풀리곡 잘라 놓은 모양은 남아 이수다.', '잘라 놓은 모양도 몬딱 풀립네다.'),
 (5, '「배치 해제」는 고른 이미지만 트레이로 돌려놓읍네다.', '「배치 해제」는 몬딱 트레이로 돌려놓읍네다.'),
 (5, '붙어 이신 이미지덜은 그 빈자리를 메우게 움직일 수도 이수다.', '뒤에 이신 이미지덜은 언제나 빈자리를 메웁네다.'),
 (5, '빈 디를 끌엉 화면을 옮깁서.', '빈 디를 끌엉 이미지를 옮깁서.'),
 (5, '「모두 표시」는 합친 이미지가 몬딱 보이게 화면 배율만 바꿉네다. 출력 크기는 그대로우다.', '「모두 표시」는 출력 크기를 바꿉네다.'),
 (6, '이 교체도 「실행 취소」로 되돌릴 수 이수다.', '이 교체는 되돌릴 수 엇수다.'),
 (6, '출력에 쓸 메모리가 한도를 넘으민 크기를 고르는 창이 나올 때 더 작은 출력 사본을 고릅서.', '출력에 쓸 메모리가 한도를 넘으민 더 작은 출력 사본을 고릅서.'),
 (6, '아주 작은 출력도 메모리 한도를 넘으민 크기를 고르는 창 대신 메모리 경고가 나옵네다.', '아주 작은 출력도 메모리 한도를 넘으민 크기를 고르는 창이 나옵네다.'),
 (6, '원본 이미지 파일은 그대로우다.', '원본 이미지 파일도 바뀝네다.'),
 (6, '지금 합쳐 놓은 상태는 기기에 저장뒈엉, 다시 들어오민 그대로 열립네다.', '지금 합쳐 놓은 상태는 저장되지 안헙네다.'))
FIXTURE = ROOT / 'tools/fixtures/current_localization/jeju_assembly_help.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate fixture key: " + key)
        result[key] = value
    return result


def read_fixture(text):
    return json.loads(text, object_pairs_hook=unique_object)


def require_fixture(data):
    require(isinstance(data, dict), "Fixture must be an object")
    fields = {"schema_version", "locale", "catalogue", "key", "attributes", "value",
              "review_url", "review_limit"}
    require(set(data) == fields, "Fixture field scope differs")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1,
            "Schema differs")
    require(data["locale"] == "jje" and data["catalogue"] == CATALOGUE_PATH
            and data["key"] == KEY, "Only current Jeju assembly Help belongs here")
    require(data["attributes"] == {"name": KEY}, "Attributes differ")
    require(data["review_url"] == REVIEW_URL and data["review_limit"] == REVIEW_LIMIT,
            "Bounded acceptance differs")
    value = data["value"]
    require(isinstance(value, str) and bool(value), "Complete value required")
    require(hashlib.sha256(value.encode("utf-8")).hexdigest() == ACCEPTED_SHA256,
            "Exact accepted full value differs")
    return value


def require_semantics(value, labels):
    require("\n" not in value and "\r" not in value, "Physical newline")
    require(value.count(r"\n") == 14, "Escaped newline count differs")
    require(not re.search(r"\\(?!n)", value), "Unknown Android escape")
    require(not any(c in value for c in ('%', '"', "'", '\ufffd')),
            "Unexpected placeholder, quote or replacement character")
    paragraphs = value.split(r"\n\n")
    require(len(paragraphs) == 8 and all(paragraphs), "Eight paragraphs required")
    for index, phrase, _ in SEMANTIC_MUTATIONS:
        require(paragraphs[index].count(phrase) == 1, "Source distinction differs: " + phrase)
    for key, label, indexes in CAPTIONS:
        require(labels.get(key) == label, "Live caption differs: " + key)
        for index in indexes:
            require(label in paragraphs[index], "Help caption differs: " + key)
    require(value.count("Catrobat") == value.count("AGPL") == 1, "Legal identifiers differ")
    return value


def require_message(xml, data):
    expected = require_fixture(data)
    root = ET.fromstring(xml)
    require(root.tag == "resources", "Resources root required")
    nodes = [n for n in root if n.get("name") == KEY]
    require(len(nodes) == 1 and nodes[0].tag == "string", "One scalar Help required")
    node = nodes[0]
    require(node.attrib == {"name": KEY} and not len(node), "Help attributes or markup differ")
    value = node.text or ""
    require(value == expected, "Complete source wording differs")
    labels = {}
    for key, _, _ in CAPTIONS:
        matches = [n for n in root if n.get("name") == key]
        require(len(matches) == 1 and matches[0].tag == "string" and not len(matches[0]),
                "One plain current caption required: " + key)
        labels[key] = matches[0].text or ""
    return require_semantics(value, labels)


class JejuAssemblyHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read_fixture(FIXTURE.read_text(encoding="utf-8"))
        cls.xml = (ROOT / CATALOGUE_PATH).read_text(encoding="utf-8")
        cls.value = require_fixture(cls.data)
        cls.labels = {key: label for key, label, _ in CAPTIONS}

    def xml_with_value(self, value):
        root = ET.fromstring(self.xml)
        root.find(f"./string[@name='{KEY}']").text = value
        return ET.tostring(root, encoding="unicode")

    def test_complete_accepted_value_and_source_distinctions(self):
        self.assertEqual(self.value, require_message(self.xml, self.data))
        self.assertEqual(self.value, require_semantics(self.value, self.labels))

    def test_fixture_missing_changed_extra_fields_are_rejected(self):
        for field in self.data:
            for mutation in ("missing", "changed"):
                changed = deepcopy(self.data)
                if mutation == "missing": del changed[field]
                else: changed[field] = None
                with self.subTest(field=field, mutation=mutation), self.assertRaises(ValueError):
                    require_fixture(changed)
        changed = deepcopy(self.data)
        changed["extra_locale"] = "ko-KR"
        with self.assertRaises(ValueError): require_fixture(changed)
        for field, value in (("locale", "cju"), ("review_limit", "Whole-language accepted"),
                             ("schema_version", True)):
            changed = deepcopy(self.data); changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): require_fixture(changed)

    def test_duplicate_fixture_keys_and_joint_wording_drift_are_rejected(self):
        for text in ('{"locale":"jje","locale":"ko-KR"}',
                     '{"attributes":{"name":"x","name":"y"}}'):
            with self.subTest(text=text), self.assertRaises(ValueError): read_fixture(text)
        changed = deepcopy(self.data); changed["value"] += " extra"
        with self.assertRaises(ValueError):
            require_message(self.xml_with_value(changed["value"]), changed)

    def test_missing_duplicate_markup_attribute_root_and_shadow_definitions_are_rejected(self):
        for mutation in ("missing", "duplicate", "markup", "formatted", "translatable",
                         "name", "root", "plural", "shadow"):
            root = ET.fromstring(self.xml); node = root.find(f"./string[@name='{KEY}']")
            if mutation == "missing": root.remove(node)
            elif mutation == "duplicate": root.append(deepcopy(node))
            elif mutation == "markup": ET.SubElement(node, "b").text = "extra"
            elif mutation == "formatted": node.set("formatted", "false")
            elif mutation == "translatable": node.set("translatable", "false")
            elif mutation == "name": node.set("name", KEY + "_other")
            elif mutation == "root": root.tag = "not-resources"
            elif mutation == "plural": node.tag = "plurals"
            else: ET.SubElement(root, "plurals", name=KEY)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_message(ET.tostring(root, encoding="unicode"), self.data)

    def test_omitted_duplicated_and_reordered_paragraphs_are_rejected(self):
        paragraphs = self.value.split(r"\n\n")
        for index in range(8):
            for mutation in ("omitted", "duplicated"):
                changed = list(paragraphs)
                if mutation == "omitted": del changed[index]
                else: changed.insert(index, changed[index])
                with self.subTest(index=index, mutation=mutation), self.assertRaises(ValueError):
                    require_message(self.xml_with_value(r"\n\n".join(changed)), self.data)
        for index in range(7):
            changed = list(paragraphs)
            changed[index], changed[index+1] = changed[index+1], changed[index]
            with self.subTest(index=index), self.assertRaises(ValueError):
                require_message(self.xml_with_value(r"\n\n".join(changed)), self.data)

    def test_all_42_target_sentences_remain_required(self):
        sentences = [s + "." for p in self.value.split(r"\n\n") for s in p[:-1].split(". ")]
        self.assertEqual(42, len(sentences))
        for sentence in sentences:
            self.assertEqual(1, self.value.count(sentence))
            for replacement in ("", sentence + " " + sentence):
                changed = self.value.replace(sentence, replacement, 1)
                with self.subTest(sentence=sentence, replacement=replacement), self.assertRaises(ValueError):
                    require_message(self.xml_with_value(changed), self.data)

    def test_snap_exact_position_normalization_and_memory_branches_do_not_regress(self):
        for index, original, replacement in SEMANTIC_MUTATIONS:
            self.assertEqual(1, self.value.split(r"\n\n")[index].count(original))
            self.assertNotEqual(original, replacement)
            changed = self.value.replace(original, replacement, 1)
            with self.subTest(original=original), self.assertRaises(ValueError):
                require_semantics(changed, self.labels)

    def test_live_caption_missing_duplicate_changed_and_shadow_are_rejected(self):
        for key, label, _ in CAPTIONS:
            for mutation in ("missing", "duplicate", "changed", "shadow"):
                root = ET.fromstring(self.xml); node = root.find(f"./string[@name='{key}']")
                if mutation == "missing": root.remove(node)
                elif mutation == "duplicate": root.append(deepcopy(node))
                elif mutation == "changed": node.text = label + "?"
                else: ET.SubElement(root, "plurals", name=key)
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_message(ET.tostring(root, encoding="unicode"), self.data)

    def test_syntax_placeholders_and_legal_identifiers_are_required(self):
        changes = (self.value.replace(r"\n", "\n", 1), self.value + r"\q",
                   self.value + "%1$s", self.value + "%", self.value + '"',
                   self.value + "'", self.value + "\ufffd", self.value.replace("Catrobat", "Cat-robat"),
                   self.value.replace("AGPL", "GPL"))
        for value in changes:
            with self.subTest(value=value[-70:]), self.assertRaises(ValueError):
                require_semantics(value, self.labels)

    def test_unrelated_resource_edits_and_formatting_are_outside_this_acceptance(self):
        root = ET.fromstring(self.xml)
        ET.SubElement(root, "string", name="unrelated_guard_probe").text = "Other work"
        # Deliberate scope probe: this guard must not claim acceptance of either held warning.
        for key in ("ui_no_resize_fits_decoder_memory", "ui_assembly_source_memory_floor"):
            root.find(f"./string[@name='{key}']").text = "Separate unreviewed warning"
        ET.indent(root)
        self.assertEqual(self.value, require_message(ET.tostring(root, encoding="unicode"), self.data))


if __name__ == "__main__":
    unittest.main()
