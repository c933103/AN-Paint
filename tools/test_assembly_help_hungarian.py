"""Exact accepted Hungarian complete assembly Help drift guards, not fluency certification.

Acceptance: https://github.com/c933103/AN-Paint/pull/56#issuecomment-6335891274
The existing attribution fixture keeps its historical C05 provenance; only this
complete Help value and its separator count gain the reviewed successor.
The narrow value digest anchors one accepted resource, not a source snapshot.
XML remains canonical. Nothing here generates translations or rebuilds the app.
Explicit exceptions and unittest assertions retain their checks under python -O.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
KEY = "ui_add_up_to_20_images_with_android_s"
CATALOGUE = ROOT / "Paintroid/src/main/res/values-hu/strings.xml"
FIXTURE = ROOT / "tools/fixtures/current_localization/hungarian_attribution_current_wording.json"
ACCEPTED_SHA256 = "8209ba860f0554452f5539760150f910b15beb680800a7a3e834fd13c622a6e9"
CONSTRAINTS = {'attributes': {'name': 'ui_add_up_to_20_images_with_android_s'},
 'placeholders': {},
 'escaped_newline_count': 14,
 'legal_identifier_counts': {'Catrobat': 1, 'AGPL': 1},
 'forbidden_casefold_substrings': ['jóváírás'],
 'child_elements': 0}
CAPTIONS = (('ui_assembly_exact_position', 'Pontos helyzet', (3,)),
 ('ui_crop_image', 'Kép vágása', (1,)),
 ('ui_batch_crop', 'Kötegelt vágás', (1,)),
 ('ui_reset_crop', 'Vágás visszaállítása', (1,)),
 ('ui_same_width', 'Azonos szélesség', (0, 4)),
 ('ui_same_height', 'Azonos magasság', (0, 4)),
 ('ui_pixels', 'Képpontok', (4,)),
 ('ui_percent', 'Százalék', (4,)),
 ('ui_smallest', 'Legkisebb', (4,)),
 ('ui_largest', 'Legnagyobb', (4,)),
 ('ui_restore_original_sizes', 'Eredeti méretek visszaállítása', (4,)),
 ('ui_unplace', 'Elhelyezés megszüntetése', (5,)),
 ('ui_remove', 'Eltávolítás', (5,)),
 ('ui_undo', 'Visszavonás', (5,)),
 ('ui_redo', 'Újra', (5,)),
 ('ui_show_all', 'Összes megjelenítése', (5,)),
 ('ui_save_png', 'PNG mentése', (6,)),
 ('ui_edit_in_paint', 'Szerkesztés a Paintben', (6,)),
 ('ui_menu_file', 'Fájl', (7,)),
 ('ui_about_credits23', 'Névjegy, licencek és forrásmegjelölések', (7,)))
PARAGRAPH_ANCHORS = ((0, 'Legfeljebb 20 képet adhat hozzá az Android fájlválasztójával.'),
 (0,
  'a képek vágás és az esetleges „Azonos szélesség” vagy „Azonos magasság” beállítás utáni '
  'méreteit'),
 (0, 'ha azt a szolgáltató megadja.'),
 (0, 'ez nem változtatja meg a már elhelyezett képek elrendezését.'),
 (1, 'A vágás roncsolásmentes és visszavonható.'),
 (2, 'Az áttetsző előnézet az illesztés pontos eredményét mutatja.'),
 (2, 'Illesztéskor az első kép bal felső sarka az origóba kerül.'),
 (2, 'A csatolt képek elmozdulhatnak, ha megvágja azt a képet, amelyhez csatlakoznak.'),
 (2, 'Illesztéskor az alkalmazás nem enged átfedést.'),
 (3, 'X- és Y-koordinátáját egész képpontokban, nullától kezdve.'),
 (3, 'A többi kép a helyén marad, és itt megengedett az átfedés.'),
 (4, 'a képek saját képarányának megőrzésével.'),
 (4, 'megszünteti a méretek egységesítését, de megtartja a vágásokat.'),
 (5, 'A többi kép elhelyezve marad; a csatolt képek elmozdulhatnak, hogy kitöltsék a rést.'),
 (5, 'a kimeneti méreteket soha nem változtatja meg.'),
 (6,
  'Ha a kimenet túllépi a memóriakeretet, válasszon kisebb kimeneti másolatot, ha az alkalmazás '
  'felajánlja.'),
 (6,
  'Ha még egy nagyon kicsi kimenet is túllépi a keretet, az alkalmazás a méretválasztó helyett '
  'memóriafigyelmeztetést jelenít meg.'),
 (6, 'Az eredeti forrásfájlok változatlanok maradnak.'),
 (6,
  'Az alkalmazás helyben tárolja az aktuális összeállítást, amely visszatéréskor újra megnyílik.'),
 (7,
  'Ez a mód ugyanazokat a Catrobat/AGPL-re és a felhasznált elemekre vonatkozó '
  'forrásmegjelöléseket használja, amelyek a fő szerkesztő «Fájl > Névjegy, licencek és '
  'forrásmegjelölések» paneljén szerepelnek.'))
HU16 = ('Ez a mód ugyanazokat a Catrobat/AGPL-re és a felhasznált elemekre vonatkozó forrásmegjelöléseket '
 'használja, amelyek a fő szerkesztő «Fájl > Névjegy, licencek és forrásmegjelölések» paneljén '
 'szerepelnek.')
MEMORY_SENTENCES = ('Ha a kimenet túllépi a memóriakeretet, válasszon kisebb kimeneti másolatot, ha az alkalmazás '
 'felajánlja.',
 'Ha még egy nagyon kicsi kimenet is túllépi a keretet, az alkalmazás a méretválasztó helyett '
 'memóriafigyelmeztetést jelenít meg.')


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
    require(isinstance(data, dict) and data.get("schema_version") == 1,
            "Fixture schema differs")
    values = data.get("values", {}).get(KEY)
    require(isinstance(values, dict) and set(values) == {"hu"},
            "Exact Hungarian Help scope differs")
    value = values["hu"]
    require(isinstance(value, str) and bool(value), "Empty complete value")
    require(hashlib.sha256(value.encode("utf-8")).hexdigest() == ACCEPTED_SHA256,
            "Complete accepted value differs")
    require(data.get("constraints", {}).get(KEY) == CONSTRAINTS,
            "Help constraints differ")
    return value


def require_semantics(value, labels):
    require("\n" not in value and "\r" not in value, "Physical newline")
    require(value.count(r"\n") == 14, "Literal escaped newline count differs")
    paragraphs = value.split(r"\n\n")
    require(len(paragraphs) == 8 and all(paragraphs), "Eight paragraphs required")
    require("%" not in value, "Unexpected format argument or literal percent")
    require(value.count("Catrobat") == value.count("AGPL") == 1,
            "Legal identifiers differ")
    require("jóváírás" not in value.casefold(), "Wrong credit meaning")
    for index, phrase in PARAGRAPH_ANCHORS:
        require(paragraphs[index].count(phrase) == 1,
                "Missing or repeated paragraph-bound clause: " + phrase)
    require(paragraphs[7] == HU16, "HU-16 must remain verbatim")
    for key, expected, positions in CAPTIONS:
        require(labels.get(key) == expected, "Current caption changed: " + key)
        for index in positions:
            require(expected in paragraphs[index], "Help caption changed: " + key)
    return value


def require_message(xml, data):
    expected = require_fixture(data)
    root = ET.fromstring(xml)
    nodes = root.findall(f"./string[@name='{KEY}']")
    require(len(nodes) == 1, "Exactly one Help resource required")
    node = nodes[0]
    require(node.attrib == CONSTRAINTS["attributes"], "Resource attributes differ")
    require(len(node) == 0, "Unexpected child markup")
    value = node.text or ""
    require(value == expected, "Complete source wording differs")
    labels = {}
    for key, _, _ in CAPTIONS:
        matches = root.findall(f"./string[@name='{key}']")
        require(len(matches) == 1 and not len(matches[0]),
                "Exactly one plain caption required: " + key)
        labels[key] = "".join(matches[0].itertext())
    return require_semantics(value, labels)


class HungarianAssemblyHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read_fixture(FIXTURE.read_text(encoding="utf-8"))
        cls.xml = CATALOGUE.read_text(encoding="utf-8")
        cls.value = require_fixture(cls.data)
        cls.labels = {key: caption for key, caption, _ in CAPTIONS}

    def xml_with_value(self, value):
        root = ET.fromstring(self.xml)
        root.find(f"./string[@name='{KEY}']").text = value
        return ET.tostring(root, encoding="unicode")

    def test_exact_complete_accepted_source_and_fixture(self):
        self.assertEqual(self.value, require_message(self.xml, self.data))
        self.assertEqual(HU16, self.value.split(r"\n\n")[-1])

    def test_missing_empty_extra_locale_or_changed_fixture_value_is_rejected(self):
        for mutation in ("missing-key", "missing-hu", "empty", "changed", "extra-locale"):
            data = deepcopy(self.data)
            if mutation == "missing-key":
                del data["values"][KEY]
            elif mutation == "missing-hu":
                del data["values"][KEY]["hu"]
            elif mutation == "empty":
                data["values"][KEY]["hu"] = ""
            elif mutation == "changed":
                data["values"][KEY]["hu"] += "?"
            else:
                data["values"][KEY]["default"] = self.value
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_fixture(data)

    def test_all_existing_help_constraints_remain_required(self):
        for field in CONSTRAINTS:
            for mutation in ("missing", "changed"):
                data = deepcopy(self.data)
                if mutation == "missing":
                    del data["constraints"][KEY][field]
                else:
                    data["constraints"][KEY][field] = None
                with self.subTest(field=field, mutation=mutation), self.assertRaises(ValueError):
                    require_fixture(data)
        data = deepcopy(self.data)
        data["constraints"][KEY]["escaped_newline_count"] = 12
        with self.assertRaises(ValueError):
            require_fixture(data)

    def test_missing_duplicate_markup_and_attribute_changes_are_rejected(self):
        for mutation in ("missing", "duplicate", "markup", "formatted", "extra-attribute"):
            root = ET.fromstring(self.xml)
            node = root.find(f"./string[@name='{KEY}']")
            if mutation == "missing":
                root.remove(node)
            elif mutation == "duplicate":
                root.append(deepcopy(node))
            elif mutation == "markup":
                ET.SubElement(node, "b").text = "extra"
            elif mutation == "formatted":
                node.set("formatted", "false")
            else:
                node.set("other", "value")
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_message(ET.tostring(root, encoding="unicode"), self.data)

    def test_changed_truncated_and_parameterized_full_values_are_rejected(self):
        for value in (self.value + "?", self.value[:-1], self.value + "%1$s",
                      self.value.replace(r"\n", "\n"), self.value.replace(r"\n\n", r"\n", 1)):
            with self.subTest(value=value[-60:]), self.assertRaises(ValueError):
                require_message(self.xml_with_value(value), self.data)

    def test_missing_duplicate_and_reordered_paragraphs_are_rejected(self):
        paragraphs = self.value.split(r"\n\n")
        for index in range(8):
            for mutation in ("missing", "duplicate", "swap-next"):
                changed = list(paragraphs)
                if mutation == "missing":
                    changed.pop(index)
                elif mutation == "duplicate":
                    changed.insert(index, changed[index])
                else:
                    other = (index + 1) % 8
                    changed[index], changed[other] = changed[other], changed[index]
                with self.subTest(index=index, mutation=mutation), self.assertRaises(ValueError):
                    require_semantics(r"\n\n".join(changed), self.labels)

    def test_each_qualified_clause_rejects_removal_and_duplication(self):
        for index, phrase in PARAGRAPH_ANCHORS:
            for replacement in ("", phrase + " " + phrase):
                value = self.value.replace(phrase, replacement, 1)
                with self.subTest(paragraph=index, phrase=phrase, replacement=replacement), self.assertRaises(ValueError):
                    require_semantics(value, self.labels)

    def test_conditional_memory_and_warning_direction_cannot_regress(self):
        mutations = (
            self.value.replace(", ha az alkalmazás felajánlja", ""),
            self.value.replace("méretválasztó helyett memóriafigyelmeztetést",
                               "memóriafigyelmeztetés helyett méretválasztót"),
            self.value.replace(MEMORY_SENTENCES[1], ""),
        )
        for value in mutations:
            with self.subTest(value=value[-250:]), self.assertRaises(ValueError):
                require_semantics(value, self.labels)

    def test_each_caption_binding_rejects_source_or_help_drift(self):
        for key, caption, _ in CAPTIONS:
            labels = dict(self.labels)
            labels[key] = caption + "?"
            with self.subTest(key=key, side="control"), self.assertRaises(ValueError):
                require_semantics(self.value, labels)
            with self.subTest(key=key, side="help"), self.assertRaises(ValueError):
                require_semantics(self.value.replace(caption, "BROKEN"), self.labels)

    def test_hu16_attribution_and_legal_tokens_stay_exact(self):
        mutations = (
            self.value.replace(HU16, HU16.replace("«", "„").replace("»", "”")),
            self.value.replace("Catrobat", ""),
            self.value.replace("AGPL", "AGPL AGPL"),
            self.value.replace("forrásmegjelöléseket", "jóváírásokat"),
        )
        for value in mutations:
            with self.subTest(value=value[-180:]), self.assertRaises(ValueError):
                require_semantics(value, self.labels)

    def test_duplicate_json_keys_are_rejected_at_any_depth(self):
        for text in ('{"values": {}, "values": {}}', '{"values": {"hu": "one", "hu": "two"}}',
                     '{"constraints": {"escaped_newline_count": 14, "escaped_newline_count": 12}}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                read_fixture(text)

    def test_unrelated_resource_changes_do_not_require_whole_catalogue_identity(self):
        root = ET.fromstring(self.xml)
        ET.SubElement(root, "string", {"name": "unrelated_guard_probe"}).text = "Changed"
        self.assertEqual(self.value, require_message(ET.tostring(root, encoding="unicode"), self.data))


if __name__ == "__main__":
    unittest.main()
