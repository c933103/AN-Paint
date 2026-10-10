/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.Spinner
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** F01 expansion: actual locale routing and dialog callbacks, not installed visual acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class TiffDescriptionLocaleTest {
    private lateinit var controller: ActivityController<Activity>
    private lateinit var activity: Activity
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private lateinit var previousResources: Resources
    private var currentDialog: AlertDialog? = null
    private val requests = mutableListOf<SaveRequest>()
    private var cancellations = 0

    @Before fun start() {
        controller = Robolectric.buildActivity(Activity::class.java)
        activity = controller.setup().get()
        previousLocale = Locale.getDefault()
        previousTag = AppLanguage.selectedTag(activity)
        previousResources = PaintApplication.currentResources
    }

    @After fun stop() {
        currentDialog?.dismiss(); idle()
        AppLanguage.select(activity, previousTag)
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
        if (!activity.isDestroyed) controller.pause().stop().destroy()
    }

    private fun idle() = shadowOf(Looper.getMainLooper()).idle()

    private fun open(tag: String, compressed: Boolean): AlertDialog {
        assertFalse(currentDialog?.isShowing == true)
        requests.clear(); cancellations = 0
        AppLanguage.select(activity, tag); AppLanguage.refresh(activity)
        assertEquals(tag, AppLanguage.selectedTag(activity))
        return SaveOptionsDialog(activity, ExportOptions(ImageFormat.TIFF, tiffCompressed = compressed),
            confirm = { requests += it }, cancel = { cancellations++ }, initialFilename = "scan.tif")
            .show().also { currentDialog = it; idle() }
    }

    private fun AlertDialog.compression(): CheckBox = window!!.decorView.findViewWithTag("export_tiff_compressed")
    private fun AlertDialog.description(): TextView = window!!.decorView.findViewWithTag("export_description")
    private fun AlertDialog.format(): Spinner = window!!.decorView.findViewWithTag("export_format")

    private fun assertDescription(dialog: AlertDialog, expected: String, compressed: Boolean) {
        assertTrue(dialog.isShowing)
        assertEquals("TIFF", dialog.format().selectedItem.toString())
        assertEquals(expected, ui(R.string.formats22_tiff_description))
        assertEquals(View.VISIBLE, dialog.description().visibility)
        assertEquals(expected, dialog.description().text.toString())
        assertEquals(View.VISIBLE, dialog.compression().visibility)
        assertEquals(compressed, dialog.compression().isChecked)
        assertTrue(requests.isEmpty()); assertEquals(0, cancellations)
    }

    @Test fun allTwentySixLocalesUseTheirQualifiedDescriptionForBothCompressionChoices() {
        assertEquals(26, EXPECTED.size)
        for ((tag, expected) in EXPECTED) for (compressed in listOf(false, true)) {
            val dialog = open(tag, compressed)
            assertDescription(dialog, expected, compressed)
            assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()); idle()
            assertFalse(dialog.isShowing)
            assertEquals(listOf(SaveRequest(ExportOptions(ImageFormat.TIFF, lossless = false,
                tiffCompressed = compressed), "scan.tif")), requests)
            assertEquals(0, cancellations)
        }
    }

    @Test fun allTwentySixLocalesRetainDescriptionThroughToggleFormatSwitchAndCancel() {
        for ((index, entry) in EXPECTED.entries.withIndex()) {
            val (tag, expected) = entry
            val dialog = open(tag, true)
            dialog.compression().performClick(); idle()
            assertDescription(dialog, expected, false)
            EditorTestNavigation.format(dialog.format(), ImageFormat.DIB)
            assertEquals(View.GONE, dialog.compression().visibility)
            assertEquals(ui(R.string.formats22_dib_description), dialog.description().text.toString())
            assertNotEquals(expected, dialog.description().text.toString())
            EditorTestNavigation.format(dialog.format(), ImageFormat.TIFF)
            assertDescription(dialog, expected, false)
            if (index % 2 == 0) dialog.cancel()
            else assertTrue(dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick())
            idle()
            assertFalse(dialog.isShowing)
            assertTrue(requests.isEmpty()); assertEquals(1, cancellations)
        }
    }

    companion object {
        // Independent reviewed wording oracles; do not read expected text back from resources.
        private val EXPECTED = linkedMapOf(
            "ar" to "يحفظ صفحة RGB واحدة. قد يقلل الضغط حجم الملف دون تغيير البكسلات؛ عطّله لحفظ TIFF غير مضغوط.",
            "af" to "Stoor een RGB-bladsy. Kompressie kan die lêer verklein sonder om piksels te verander; skakel dit af vir ongekomprimeerde TIFF.",
            "eo" to "Konservas unu RGB-paĝon. Kunpremo povas malgrandigi la dosieron sen ŝanĝi bilderojn; malŝaltu ĝin por nekunpremita TIFF.",
            "es-419" to "Guarda una página RGB. La compresión puede reducir el tamaño del archivo sin cambiar los píxeles; desactívala para un TIFF sin comprimir.",
            "es-ES" to "Guarda una página RGB. La compresión puede reducir el tamaño del archivo sin cambiar los píxeles; desactívala para un TIFF sin comprimir.",
            "et" to "Salvestab ühe RGB-lehe. Tihendus võib vähendada failisuurust piksleid muutmata; tihendamata TIFF-i jaoks lülita see välja.",
            "ko-KP" to "RGB 한 페이지를 보관합니다. 압축은 화소를 바꾸지 않고 파일 크기를 줄일 수 있습니다. 압축하지 않은 TIFF로 보관하려면 끄세요.",
            "ko-KR" to "RGB 한 페이지를 저장합니다. 압축은 픽셀을 바꾸지 않고 파일 크기를 줄일 수 있습니다. 압축하지 않은 TIFF로 저장하려면 끄세요.",
            "ko-Kore-KR" to "RGB 한 페이지를 貯藏합니다. 壓縮은 픽셀을 바꾸지 않고 파일 크기를 줄일 수 있습니다. 壓縮하지 않은 TIFF로 貯藏하려면 끄세요.",
            "lv" to "Saglabā vienu RGB lapu. Saspiešana var samazināt faila izmēru, nemainot pikseļus; izslēdziet to nesaspiestam TIFF.",
            "pt-PT" to "Guarda uma página RGB. A compressão pode reduzir o tamanho do ficheiro sem alterar os píxeis; desative-a para TIFF não comprimido.",
            "de" to "Speichert eine RGB-Seite. Komprimierung kann die Datei verkleinern, ohne Pixel zu verändern; deaktivieren Sie sie für unkomprimiertes TIFF.",
            "el" to "Αποθηκεύει μία σελίδα RGB. Η συμπίεση μπορεί να μειώσει το μέγεθος αρχείου χωρίς να αλλάζει pixel· απενεργοποιήστε την για ασυμπίεστο TIFF.",
            "fi" to "Tallentaa yhden RGB-sivun. Pakkaus voi pienentää tiedostoa muuttamatta pikseleitä; poista se käytöstä pakkaamattomalle TIFF:lle.",
            "fr" to "Enregistre une page RGB. La compression peut réduire la taille du fichier sans modifier les pixels ; désactivez-la pour un TIFF non compressé.",
            "hu" to "Egy RGB-oldalt ment. A tömörítés a képpontok módosítása nélkül csökkentheti a fájlméretet; kapcsolja ki tömörítetlen TIFF-hez.",
            "id" to "Simpan satu halaman RGB. Kompresi dapat mengurangi ukuran berkas tanpa mengubah piksel; nonaktifkan untuk TIFF tanpa kompresi.",
            "it" to "Salva una pagina RGB. La compressione può ridurre le dimensioni del file senza cambiare i pixel; disattivala per TIFF non compresso.",
            "lt" to "Išsaugo vieną RGB puslapį. Glaudinimas gali sumažinti failo dydį nekeisdamas pikselių; išjunkite nesuglaudintam TIFF.",
            "ms" to "Menyimpan satu halaman RGB. Mampatan mungkin mengurangkan saiz fail tanpa mengubah piksel; matikannya untuk TIFF tanpa mampatan.",
            "nl" to "Slaat één RGB-pagina op. Compressie kan het bestand verkleinen zonder pixels te wijzigen; schakel deze uit voor ongecomprimeerde TIFF.",
            "ru" to "Сохраняет одну RGB-страницу. Сжатие может уменьшить размер файла без изменения пикселей; отключите его для несжатого TIFF.",
            "sw" to "Huhifadhi ukurasa mmoja wa RGB. Mgandamizo unaweza kupunguza ukubwa wa faili bila kubadilisha pikseli; uzime kwa TIFF isiyogandamizwa.",
            "tl" to "Nagse-save ng isang RGB page. Maaaring bawasan ng compression ang laki ng file nang hindi binabago ang pixels; i-off ito para sa uncompressed TIFF.",
            "tr" to "Tek bir RGB sayfası kaydeder. Sıkıştırma, pikselleri değiştirmeden dosya boyutunu azaltabilir; sıkıştırılmamış TIFF için kapatın.",
            "vi" to "Lưu một trang RGB. Nén có thể làm giảm kích thước tệp mà không đổi điểm ảnh; tắt để lưu TIFF không nén."
        )
    }
}
