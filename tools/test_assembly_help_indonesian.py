"""One accepted Indonesian assembly Help value: bounded drift guards, not fluency certification.

Acceptance: https://github.com/c933103/AN-Paint/pull/56#issuecomment-6336650894
XML remains canonical. The digest anchors this one reviewed value, not a whole
source snapshot. Existing PR125/PR67 contracts and other locales are untouched.
Explicit exceptions and unittest assertions remain active under python -O.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
KEY = "ui_add_up_to_20_images_with_android_s"
CATALOGUE_PATH = "Paintroid/src/main/res/values-in/strings.xml"
FIXTURE = ROOT / "tools/fixtures/current_localization/indonesian_assembly_help.json"
ACCEPTED_SHA256 = "3cfebea71e94ddfff8a2960725a633defe16dfd8e00b9978f6131aa395b6133c"
PROTECTED_PARAGRAPHS = {0: 'Tambahkan hingga 20 gambar menggunakan pemilih berkas Android. Baki bawah menampilkan gambar '
    'mini, nama berkas, dimensi gambar setelah pemangkasan dan penyesuaian Lebar sama atau Tinggi '
    'sama jika ada, serta waktu perubahan berkas jika disediakan oleh penyedia. Urutkan menurut '
    'nama berkas atau waktu perubahan; pengurutan ini tidak mengubah susunan gambar yang telah '
    'ditempatkan.',
 4: 'Lebar sama dan Tinggi sama memberikan satu dimensi yang sama pada setiap gambar sambil '
    'mempertahankan rasio aspeknya masing-masing. Pilih Piksel, Persen, Terkecil, atau Terbesar. '
    'Pulihkan ukuran asli membatalkan penyeragaman ukuran tetapi mempertahankan pemangkasan.',
 6: 'Simpan PNG langsung menyimpan gambar gabungan. Edit dalam Paint memindahkannya ke editor '
    'utama sebagai penggantian yang dapat diurungkan. Jika hasil melebihi batas memori, pilih '
    'salinan hasil yang lebih kecil jika opsi itu ditawarkan. Jika hasil yang sangat kecil pun '
    'melebihi batas memori, aplikasi menampilkan peringatan memori, bukan pilihan ukuran. Berkas '
    'sumber asli tidak berubah. Gabungan saat ini disimpan secara lokal dan dibuka kembali saat '
    'Anda kembali.',
 7: 'Mode ini menggunakan kredit Catrobat/AGPL dan aset yang sama seperti yang tercantum di panel '
    '«Berkas > Tentang, lisensi & kredit» pada editor utama.'}
CAPTIONS = (('ui_crop_image', 'Pangkas gambar', (1,)),
 ('ui_batch_crop', 'Pangkas massal', (1,)),
 ('ui_reset_crop', 'Atur ulang pemangkasan', (1,)),
 ('ui_assembly_exact_position', 'Posisi tepat', (3,)),
 ('ui_same_width', 'Lebar sama', (0, 4)),
 ('ui_same_height', 'Tinggi sama', (0, 4)),
 ('ui_pixels', 'Piksel', (4,)),
 ('ui_percent', 'Persen', (4,)),
 ('ui_smallest', 'Terkecil', (4,)),
 ('ui_largest', 'Terbesar', (4,)),
 ('ui_restore_original_sizes', 'Pulihkan ukuran asli', (4,)),
 ('ui_unplace', 'Lepaskan penempatan', (5,)),
 ('ui_remove', 'Hapus', (5,)),
 ('ui_undo', 'Urungkan', (5,)),
 ('ui_redo', 'Ulangi', (5,)),
 ('ui_show_all', 'Tampilkan semua', (5,)),
 ('ui_save_png', 'Simpan PNG', (6,)),
 ('ui_edit_in_paint', 'Edit dalam Paint', (6,)),
 ('ui_menu_file', 'Berkas', (6, 7)),
 ('ui_about_credits23', 'Tentang, lisensi & kredit', (7,)))
PARAGRAPH_SENTENCES = ((1, 'Ketuk gambar mini untuk memilihnya.'),
 (1,
  'Pangkas gambar memangkas gambar tersebut; Pangkas massal menerapkan margin dalam piksel atau '
  'persentase pada gambar yang dipilih.'),
 (1, 'Seret pegangan pemangkasan atau masukkan nilainya.'),
 (1, 'Atur ulang pemangkasan mengembalikan tepi asli.'),
 (1, 'Pemangkasan tidak merusak sumber dan dapat diurungkan.'),
 (2,
  'Tekan lama gambar mini, atau seret gambar yang sudah berada di ruang kerja, lalu lepaskan pada '
  'tepi yang disorot.'),
 (2, 'Pratinjau semitransparan menunjukkan hasil penyambungan secara tepat.'),
 (2,
  'Penyambungan di kanan menyejajarkan tepi atas; penyambungan di bawah menyejajarkan tepi kiri.'),
 (2, 'Anda juga dapat mengetuk gambar mini lalu sasaran +.'),
 (2, 'Saat menyambungkan gambar, gambar pertama dimulai dari titik asal.'),
 (2, 'Gambar yang tersambung dapat bergeser saat gambar induknya dipangkas.'),
 (2, 'Tumpang tindih ditolak saat menyambungkan gambar.'),
 (3,
  'Pilih gambar dan gunakan Posisi tepat untuk mengatur koordinat X/Y sudut kiri atasnya dalam '
  'piksel dengan nilai bilangan bulat mulai dari nol.'),
 (3, 'Gambar lain tetap berada di posisinya dan tumpang tindih diperbolehkan.'),
 (5, 'Lepaskan penempatan mengembalikan hanya gambar yang dipilih ke baki.'),
 (5,
  'Gambar lain tetap berada di ruang kerja; gambar yang tersambung dapat bergeser untuk mengisi '
  'celah.'),
 (5, 'Hapus hanya menghapus gambar masukan tersebut.'),
 (5, 'Urungkan/Ulangi mengembalikan perubahan ini.'),
 (5,
  'Seret gambar yang telah ditempatkan untuk menyusun ulang; seret pada ruang kosong untuk '
  'menggeser tampilan.'),
 (5, 'Rapatkan atau renggangkan dua jari untuk memperkecil atau memperbesar tampilan.'),
 (5,
  'Tampilkan semua menyesuaikan pembesaran agar seluruh gabungan terlihat; dimensi hasil tidak '
  'berubah.'))


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
    required = {"schema_version", "locale", "catalogue", "key", "attributes", "value",
                "review_url", "review_limit"}
    require(set(data) == required, "Fixture field scope differs")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1,
            "Fixture schema differs")
    require(data["locale"] == "id" and data["catalogue"] == CATALOGUE_PATH and data["key"] == KEY,
            "Only Indonesian assembly Help belongs here")
    require(data["attributes"] == {"name": KEY}, "Resource attributes differ")
    require(data["review_url"] ==
            "https://github.com/c933103/AN-Paint/pull/56#issuecomment-6336650894",
            "Accepted review binding differs")
    require(isinstance(data["review_limit"], str) and bool(data["review_limit"].strip()),
            "Review scope must remain explicit")
    value = data["value"]
    require(isinstance(value, str) and bool(value), "Complete accepted value required")
    require(hashlib.sha256(value.encode("utf-8")).hexdigest() == ACCEPTED_SHA256,
            "Complete accepted value differs")
    return value


def require_semantics(value, labels):
    require("\n" not in value and "\r" not in value, "Physical newline")
    require(value.count(r"\n") == 14, "Escaped newline count differs")
    require(not re.search(r"\\(?!n)", value), "Unknown Android escape")
    require(not any(char in value for char in ('%', '"', "'", '\ufffd')),
            "Unexpected format argument, quote or replacement character")
    paragraphs = value.split(r"\n\n")
    require(len(paragraphs) == 8 and all(paragraphs), "Eight nonempty paragraphs required")
    for index, expected in PROTECTED_PARAGRAPHS.items():
        require(paragraphs[index] == expected, "Protected paragraph differs: " + str(index))
    for index, sentence in PARAGRAPH_SENTENCES:
        require(paragraphs[index].count(sentence) == 1,
                "Reviewed paragraph-bound sentence differs: " + sentence)
    for key, expected, positions in CAPTIONS:
        require(labels.get(key) == expected, "Current caption changed: " + key)
        for index in positions:
            require(expected in paragraphs[index], "Help caption changed: " + key)
    require(value.count("Catrobat") == value.count("AGPL") == 1,
            "Legal identifiers differ")
    return value


def require_message(xml, data):
    expected = require_fixture(data)
    root = ET.fromstring(xml)
    require(root.tag == "resources", "Expected Android resources root")
    nodes = root.findall(f"./string[@name='{KEY}']")
    require(len(nodes) == 1, "Exactly one Help resource required")
    node = nodes[0]
    require(node.attrib == {"name": KEY} and len(node) == 0,
            "Unexpected Help attributes or child markup")
    value = node.text or ""
    require(value == expected, "Complete source wording differs")
    labels = {}
    for key, _, _ in CAPTIONS:
        matches = root.findall(f"./string[@name='{key}']")
        require(len(matches) == 1 and not len(matches[0]),
                "Exactly one plain caption required: " + key)
        labels[key] = matches[0].text or ""
    return require_semantics(value, labels)


class IndonesianAssemblyHelpTests(unittest.TestCase):
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

    def test_complete_accepted_value_and_protected_paragraphs(self):
        self.assertEqual(self.value, require_message(self.xml, self.data))
        self.assertEqual(self.value, require_semantics(self.value, self.labels))
        for index, expected in PROTECTED_PARAGRAPHS.items():
            self.assertEqual(expected, self.value.split(r"\n\n")[index])

    def test_fixture_fields_cannot_be_removed_or_changed(self):
        for field in self.data:
            for mutation in ("missing", "changed"):
                changed = deepcopy(self.data)
                if mutation == "missing":
                    del changed[field]
                else:
                    changed[field] = None
                with self.subTest(field=field, mutation=mutation), self.assertRaises(ValueError):
                    require_fixture(changed)
        changed = deepcopy(self.data)
        changed["extra_locale"] = "en"
        with self.assertRaises(ValueError):
            require_fixture(changed)

    def test_duplicate_fixture_keys_and_joint_source_fixture_drift_are_rejected(self):
        for text in ('{"locale":"id","locale":"en"}',
                     '{"attributes":{"name":"x","name":"y"}}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                read_fixture(text)
        changed = deepcopy(self.data)
        changed["value"] += " tambahan"
        with self.assertRaises(ValueError):
            require_message(self.xml_with_value(changed["value"]), changed)

    def test_missing_duplicate_markup_attribute_and_root_changes_are_rejected(self):
        for mutation in ("missing", "duplicate", "markup", "formatted", "translatable", "name", "root"):
            root = ET.fromstring(self.xml)
            node = root.find(f"./string[@name='{KEY}']")
            if mutation == "missing": root.remove(node)
            elif mutation == "duplicate": root.append(deepcopy(node))
            elif mutation == "markup": ET.SubElement(node, "b").text = "extra"
            elif mutation == "formatted": node.set("formatted", "false")
            elif mutation == "translatable": node.set("translatable", "false")
            elif mutation == "name": node.set("name", KEY + "_other")
            else: root.tag = "not-resources"
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
            changed[index], changed[index + 1] = changed[index + 1], changed[index]
            with self.subTest(swapped=index), self.assertRaises(ValueError):
                require_message(self.xml_with_value(r"\n\n".join(changed)), self.data)

    def test_every_reviewed_sentence_remains_required_in_its_paragraph(self):
        for index, sentence in PARAGRAPH_SENTENCES:
            changed = self.value.replace(sentence, "", 1)
            with self.subTest(index=index, sentence=sentence), self.assertRaises(ValueError):
                require_semantics(changed, self.labels)
            paragraphs = self.value.split(r"\n\n")
            paragraphs[index] = paragraphs[index].replace(sentence, "", 1)
            paragraphs[(index + 1) % 8] += " " + sentence
            with self.subTest(moved=sentence), self.assertRaises(ValueError):
                require_semantics(r"\n\n".join(paragraphs), self.labels)

    def test_protected_dimension_normalization_memory_and_credits_cannot_drift(self):
        for index in PROTECTED_PARAGRAPHS:
            paragraphs = self.value.split(r"\n\n")
            paragraphs[index] = paragraphs[index][:-1]
            with self.subTest(index=index), self.assertRaises(ValueError):
                require_semantics(r"\n\n".join(paragraphs), self.labels)

    def test_snap_exact_position_and_conditional_movement_do_not_regress(self):
        changes = (
            ("semitransparan", "buram"),
            ("di kanan menyejajarkan tepi atas", "di kanan menyejajarkan tepi kiri"),
            ("di bawah menyejajarkan tepi kiri", "di bawah menyejajarkan tepi atas"),
            ("Saat menyambungkan gambar, gambar pertama", "Gambar pertama"),
            ("Tumpang tindih ditolak saat menyambungkan gambar.", "Tumpang tindih selalu ditolak."),
            ("koordinat X/Y sudut kiri atasnya", "koordinat X/Y pusatnya"),
            ("bilangan bulat mulai dari nol", "bilangan desimal"),
            ("Gambar lain tetap berada di posisinya dan tumpang tindih diperbolehkan.",
             "Gambar lain bergeser dan tumpang tindih ditolak."),
            ("Gambar yang tersambung dapat bergeser", "Gambar yang tersambung selalu bergeser"),
            ("gambar yang tersambung dapat bergeser untuk mengisi celah", "gambar berikutnya selalu mengisi celah"),
            ("hanya gambar yang dipilih", "semua gambar"),
            ("memperkecil atau memperbesar tampilan", "memperbesar tampilan"),
            ("dimensi hasil tidak berubah", "dimensi hasil berubah"),
            ("jika opsi itu ditawarkan", "tanpa pilihan lain"),
            ("peringatan memori, bukan pilihan ukuran", "pilihan ukuran"),
        )
        for original, replacement in changes:
            self.assertIn(original, self.value)
            changed = self.value.replace(original, replacement, 1)
            with self.subTest(original=original), self.assertRaises(ValueError):
                require_semantics(changed, self.labels)

    def test_all_live_caption_bindings_are_required(self):
        for key, expected, _ in CAPTIONS:
            for mutation in ("missing", "duplicate", "changed"):
                root = ET.fromstring(self.xml)
                node = root.find(f"./string[@name='{key}']")
                if mutation == "missing": root.remove(node)
                elif mutation == "duplicate": root.append(deepcopy(node))
                else: node.text = expected + "?"
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_message(ET.tostring(root, encoding="unicode"), self.data)

    def test_syntax_placeholder_and_legal_identifier_corruption_is_rejected(self):
        changes = (self.value.replace(r"\n", "\n", 1), self.value + r"\q",
                   self.value + "%1$s", self.value + "%", self.value + '"',
                   self.value + "'", self.value + "\ufffd",
                   self.value.replace("Catrobat", "Cat-robat"),
                   self.value.replace("AGPL", "GPL"))
        for value in changes:
            with self.subTest(value=value[-70:]), self.assertRaises(ValueError):
                require_semantics(value, self.labels)

    def test_unrelated_resource_edit_and_xml_formatting_are_allowed(self):
        root = ET.fromstring(self.xml)
        ET.SubElement(root, "string", name="unrelated_regression_probe").text = "Independent change"
        ET.indent(root)
        self.assertEqual(self.value, require_message(ET.tostring(root, encoding="unicode"), self.data))


if __name__ == "__main__":
    unittest.main()
