"""F01: exact independently reviewed modal wording for 26 additional catalogues.

These are bounded wording oracles, not a semantic classifier or locale acceptance.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / "Paintroid/src/main/res"
KEY = "formats22_tiff_description"
EXPECTED = {
    "values-ar": "يحفظ صفحة RGB واحدة. قد يقلل الضغط حجم الملف دون تغيير البكسلات؛ عطّله لحفظ TIFF غير مضغوط.",
    "values-b+af": "Stoor een RGB-bladsy. Kompressie kan die lêer verklein sonder om piksels te verander; skakel dit af vir ongekomprimeerde TIFF.",
    "values-b+eo": "Konservas unu RGB-paĝon. Kunpremo povas malgrandigi la dosieron sen ŝanĝi bilderojn; malŝaltu ĝin por nekunpremita TIFF.",
    "values-b+es+419": "Guarda una página RGB. La compresión puede reducir el tamaño del archivo sin cambiar los píxeles; desactívala para un TIFF sin comprimir.",
    "values-b+es+ES": "Guarda una página RGB. La compresión puede reducir el tamaño del archivo sin cambiar los píxeles; desactívala para un TIFF sin comprimir.",
    "values-b+et": "Salvestab ühe RGB-lehe. Tihendus võib vähendada failisuurust piksleid muutmata; tihendamata TIFF-i jaoks lülita see välja.",
    "values-b+ko+KP": "RGB 한 페이지를 보관합니다. 압축은 화소를 바꾸지 않고 파일 크기를 줄일 수 있습니다. 압축하지 않은 TIFF로 보관하려면 끄세요.",
    "values-b+ko+KR": "RGB 한 페이지를 저장합니다. 압축은 픽셀을 바꾸지 않고 파일 크기를 줄일 수 있습니다. 압축하지 않은 TIFF로 저장하려면 끄세요.",
    "values-b+ko+Kore+KR": "RGB 한 페이지를 貯藏합니다. 壓縮은 픽셀을 바꾸지 않고 파일 크기를 줄일 수 있습니다. 壓縮하지 않은 TIFF로 貯藏하려면 끄세요.",
    "values-b+lv": "Saglabā vienu RGB lapu. Saspiešana var samazināt faila izmēru, nemainot pikseļus; izslēdziet to nesaspiestam TIFF.",
    "values-b+pt+PT": "Guarda uma página RGB. A compressão pode reduzir o tamanho do ficheiro sem alterar os píxeis; desative-a para TIFF não comprimido.",
    "values-de": "Speichert eine RGB-Seite. Komprimierung kann die Datei verkleinern, ohne Pixel zu verändern; deaktivieren Sie sie für unkomprimiertes TIFF.",
    "values-el": "Αποθηκεύει μία σελίδα RGB. Η συμπίεση μπορεί να μειώσει το μέγεθος αρχείου χωρίς να αλλάζει pixel· απενεργοποιήστε την για ασυμπίεστο TIFF.",
    "values-fi": "Tallentaa yhden RGB-sivun. Pakkaus voi pienentää tiedostoa muuttamatta pikseleitä; poista se käytöstä pakkaamattomalle TIFF:lle.",
    "values-fr": "Enregistre une page RGB. La compression peut réduire la taille du fichier sans modifier les pixels ; désactivez-la pour un TIFF non compressé.",
    "values-hu": "Egy RGB-oldalt ment. A tömörítés a képpontok módosítása nélkül csökkentheti a fájlméretet; kapcsolja ki tömörítetlen TIFF-hez.",
    "values-in": "Simpan satu halaman RGB. Kompresi dapat mengurangi ukuran berkas tanpa mengubah piksel; nonaktifkan untuk TIFF tanpa kompresi.",
    "values-it": "Salva una pagina RGB. La compressione può ridurre le dimensioni del file senza cambiare i pixel; disattivala per TIFF non compresso.",
    "values-lt": "Išsaugo vieną RGB puslapį. Glaudinimas gali sumažinti failo dydį nekeisdamas pikselių; išjunkite nesuglaudintam TIFF.",
    "values-ms": "Menyimpan satu halaman RGB. Mampatan mungkin mengurangkan saiz fail tanpa mengubah piksel; matikannya untuk TIFF tanpa mampatan.",
    "values-nl": "Slaat één RGB-pagina op. Compressie kan het bestand verkleinen zonder pixels te wijzigen; schakel deze uit voor ongecomprimeerde TIFF.",
    "values-ru": "Сохраняет одну RGB-страницу. Сжатие может уменьшить размер файла без изменения пикселей; отключите его для несжатого TIFF.",
    "values-sw": "Huhifadhi ukurasa mmoja wa RGB. Mgandamizo unaweza kupunguza ukubwa wa faili bila kubadilisha pikseli; uzime kwa TIFF isiyogandamizwa.",
    "values-tl": "Nagse-save ng isang RGB page. Maaaring bawasan ng compression ang laki ng file nang hindi binabago ang pixels; i-off ito para sa uncompressed TIFF.",
    "values-tr": "Tek bir RGB sayfası kaydeder. Sıkıştırma, pikselleri değiştirmeden dosya boyutunu azaltabilir; sıkıştırılmamış TIFF için kapatın.",
    "values-vi": "Lưu một trang RGB. Nén có thể làm giảm kích thước tệp mà không đổi điểm ảnh; tắt để lưu TIFF không nén."
}


class TiffAdditionalLocaleWordingTests(unittest.TestCase):
    def test_every_reviewed_catalogue_matches_its_individual_modal_oracle(self):
        self.assertEqual(26, len(EXPECTED))
        for folder, expected in EXPECTED.items():
            with self.subTest(folder=folder):
                nodes = ET.parse(RES / folder / "strings.xml").findall(f"./string[@name='{KEY}']")
                self.assertEqual(1, len(nodes))
                self.assertEqual(expected, "".join(nodes[0].itertext()))

    def test_reviewed_descriptions_remain_argument_free(self):
        for folder in EXPECTED:
            with self.subTest(folder=folder):
                node = ET.parse(RES / folder / "strings.xml").find(f"./string[@name='{KEY}']")
                self.assertIsNotNone(node)
                self.assertNotIn("%", "".join(node.itertext()))


if __name__ == "__main__":
    unittest.main()
