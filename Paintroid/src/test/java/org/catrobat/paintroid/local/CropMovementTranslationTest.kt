/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.AssemblyActivity
import org.catrobat.paintroid.classic.AssemblyImage
import org.catrobat.paintroid.classic.ImageCropDialog
import org.catrobat.paintroid.classic.ImageDimensions
import org.catrobat.paintroid.classic.PaintApplication
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale

/** Whole compiled quantity messages and the production crop-status display path. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CropMovementTranslationTest {
    private val context get() = RuntimeEnvironment.getApplication() as Context
    private val templates = mapOf(
        "lt" to mapOf(
            "one" to "Peržiūra: %1\$d × %2\$d px\nTaikyti %3\$d vaizdui. Apkirpus išdėstytą vaizdą, prie jo prijungti vaizdai gali pasislinkti.",
            "few" to "Peržiūra: %1\$d × %2\$d px\nTaikyti %3\$d vaizdams. Apkirpus išdėstytus vaizdus, prie jų prijungti vaizdai gali pasislinkti.",
            "other" to "Peržiūra: %1\$d × %2\$d px\nTaikyti %3\$d vaizdų. Apkirpus išdėstytus vaizdus, prie jų prijungti vaizdai gali pasislinkti."
        ),
        "ar" to mapOf(
            "zero" to "المعاينة: %1\$d × %2\$d px\nعدد الصور التي سيُطبَّق عليها القص: %3\$d. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
            "one" to "المعاينة: %1\$d × %2\$d px\nعدد الصور التي سيُطبَّق عليها القص: %3\$d. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
            "two" to "المعاينة: %1\$d × %2\$d px\nعدد الصور التي سيُطبَّق عليها القص: %3\$d. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
            "few" to "المعاينة: %1\$d × %2\$d px\nتُطبق على %3\$d صور. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
            "many" to "المعاينة: %1\$d × %2\$d px\nتُطبق على %3\$d صورة. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها.",
            "other" to "المعاينة: %1\$d × %2\$d px\nتُطبق على %3\$d صورة. قد يؤدي قص الصور الموضوعة إلى تحريك الصور المتصلة بها."
        ),
        "ru" to mapOf(
            "one" to "Предпросмотр: %1\$d × %2\$d px\nПрименить к %3\$d изображению. При обрезке размещённых изображений присоединённые к ним изображения могут переместиться.",
            "few" to "Предпросмотр: %1\$d × %2\$d px\nПрименить к %3\$d изображениям. При обрезке размещённых изображений присоединённые к ним изображения могут переместиться.",
            "many" to "Предпросмотр: %1\$d × %2\$d px\nИзображений для обрезки: %3\$d. При обрезке размещённых изображений присоединённые к ним изображения могут переместиться.",
            "other" to "Предпросмотр: %1\$d × %2\$d px\nПрименить к %3\$d изображениям. При обрезке размещённых изображений присоединённые к ним изображения могут переместиться."
        ),
        "ja" to mapOf(
            "other" to "プレビュー: %1\$d × %2\$d px\n%3\$d 枚の画像に適用します。配置済み画像をトリミングすると、接続された画像が移動する場合があります。"
        )
,
        "fi" to mapOf(
            "one" to "Esikatselu: %1\$d × %2\$d px\nKäytä %3\$d kuvaan. Aseteltujen kuvien rajaaminen voi siirtää niihin liitettyjä kuvia.",
            "other" to "Esikatselu: %1\$d × %2\$d px\nKäytä %3\$d kuvaan. Aseteltujen kuvien rajaaminen voi siirtää niihin liitettyjä kuvia."
        ),
        "et" to mapOf(
            "one" to "Eelvaade: %1\$d × %2\$d px\nRakenda %3\$d pildile. Paigutatud piltide kärpimine võib liigutada nende külge kinnitatud pilte.",
            "other" to "Eelvaade: %1\$d × %2\$d px\nRakenda %3\$d pildile. Paigutatud piltide kärpimine võib liigutada nende külge kinnitatud pilte."
        ),
        "lv" to mapOf(
            "one" to "Priekšskatījums: %1\$d × %2\$d px\nLietot %3\$d attēlam. Novietotu attēlu apgriešana var pārvietot tiem piesaistītos attēlus.",
            "other" to "Priekšskatījums: %1\$d × %2\$d px\nLietot %3\$d attēliem. Novietotu attēlu apgriešana var pārvietot tiem piesaistītos attēlus."
        )
    )

    // Independent integer examples. Russian "other" is covered by the XML test;
    // Android getQuantityString cannot select a fractional quantity.
    private val quantities = mapOf(
        "lt" to mapOf("one" to listOf(1, 21, 101), "few" to listOf(2, 3, 9, 22, 102),
            "other" to listOf(0, 10, 11, 19, 20, 111)),
        "ar" to mapOf("zero" to listOf(0), "one" to listOf(1), "two" to listOf(2),
            "few" to listOf(3, 10, 103), "many" to listOf(11, 20, 99, 111),
            "other" to listOf(100, 101, 102)),
        "ru" to mapOf("one" to listOf(1, 21, 101), "few" to listOf(2, 3, 4, 22, 102),
            "many" to listOf(0, 5, 11, 12, 14, 20, 111)),
        "ja" to mapOf("other" to listOf(0, 1, 2, 3, 11, 20, 101)),
        "fi" to mapOf("one" to listOf(1), "other" to listOf(0, 2, 3, 11, 20, 21, 101)),
        "et" to mapOf("one" to listOf(1), "other" to listOf(0, 2, 3, 11, 20, 21, 101)),
        // Latvian zero-category counts below intentionally resolve through Android
        // fallback to the resource other item; they are not all CLDR other.
        "lv" to mapOf("one" to listOf(1, 21, 101), "other" to listOf(0, 2, 3, 10, 11, 20, 111))
    )

    private fun withLanguage(tag: String, check: (AssemblyActivity) -> Unit) {
        val preferences = context.getSharedPreferences("app-language", Context.MODE_PRIVATE)
        val previousTag = preferences.getString("language-tag", null)
        val previousInitialized = if (preferences.contains("platform-initialized"))
            preferences.getBoolean("platform-initialized", false) else null
        val previousResources = PaintApplication.currentResources
        val previousLocale = Locale.getDefault()
        val manager = context.getSystemService(LocaleManager::class.java)!!
        val previousPlatform = manager.applicationLocales
        var controller: ActivityController<AssemblyActivity>? = null
        try {
            File(context.filesDir, "image-assembly").deleteRecursively()
            AppLanguage.select(context, tag)
            val started = Robolectric.buildActivity(AssemblyActivity::class.java)
            controller = started
            val activity = started.setup().get()
            AppLanguage.refresh(activity)
            assertEquals(tag, AppLanguage.selectedTag(activity))
            assertEquals(tag, activity.resources.configuration.locales[0].language)
            check(activity)
        } finally {
            try {
                try { ShadowAlertDialog.getLatestAlertDialog()?.dismiss() }
                finally { controller?.let { if (!it.get().isDestroyed) it.pause().stop().destroy() } }
            } finally {
                try { manager.applicationLocales = previousPlatform }
                finally {
                    try {
                        preferences.edit().apply {
                            if (previousTag == null) remove("language-tag") else putString("language-tag", previousTag)
                            if (previousInitialized == null) remove("platform-initialized")
                            else putBoolean("platform-initialized", previousInitialized)
                        }.commit()
                    } finally {
                        PaintApplication.currentResources = previousResources
                        Locale.setDefault(previousLocale)
                    }
                }
            }
        }
    }

    private fun template(tag: String, count: Int): String {
        val quantity = quantities.getValue(tag).entries.single { count in it.value }.key
        return templates.getValue(tag).getValue(quantity)
    }

    private fun formatted(activity: AssemblyActivity, template: String, height: Int, count: Int) =
        String.format(activity.resources.configuration.locales[0], template, 24, height, count)

    @Test fun compiledResourcesSelectCompletePluralMessagesAndFormatAllThreeArguments() {
        for ((tag, forms) in quantities) withLanguage(tag) { activity ->
            for ((quantity, counts) in forms) for (count in counts) {
                val expected = templates.getValue(tag).getValue(quantity)
                assertEquals(tag + "/" + quantity + "/" + count, expected,
                    activity.resources.getQuantityText(R.plurals.ui_crop_preview_images, count).toString())
                assertEquals(formatted(activity, expected, 16, count),
                    activity.resources.getQuantityString(R.plurals.ui_crop_preview_images, count, 24, 16, count))
            }
        }
    }

    @Test fun actualCropDialogKeepsCompleteWarningsAcrossSelectionTrimAndReset() {
        for (tag in templates.keys) withLanguage(tag) { activity ->
            val images = (0 until 20).map { index ->
                AssemblyImage("crop-" + index, File(activity.cacheDir, "crop-" + index + ".image"),
                    "Image " + index, null, ImageDimensions(24, 16))
            }
            var applied = false
            val dialog = ImageCropDialog(activity, images, { null }) { applied = true }.show()
            val root = dialog.window!!.decorView
            val status = root.findViewWithTag<TextView>("crop_status")
            fun check(count: Int, height: Int = 16) {
                shadowOf(Looper.getMainLooper()).idle()
                assertEquals(tag + "/" + count,
                    formatted(activity, template(tag, count), height, count), status.text.toString())
            }
            // Includes Arabic zero/one/two/few/many and all integer LT/RU forms.
            for (count in listOf(20, 0, 1, 2, 3, 11, 20)) {
                when (count) {
                    0 -> root.findViewWithTag<View>("crop_none").performClick()
                    20 -> root.findViewWithTag<View>("crop_all").performClick()
                    else -> images.forEachIndexed { index, image ->
                        root.findViewWithTag<CheckBox>("crop_include_" + image.id).isChecked = index < count
                    }
                }
                check(count)
            }
            root.findViewWithTag<EditText>("crop_top").setText("4")
            check(20, 12)
            root.findViewWithTag<View>("crop_reset").performClick()
            check(20)
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            assertFalse(applied)
        }
    }

    @Test fun finnishEstonianLatvianCropSideDescriptionsRemainWholeOnEveryUnitSwitch() {
        val expected = mapOf(
            "fi" to mapOf(
                "left" to listOf("Vasen: rajaus pikseleinä", "Vasen: rajaus prosentteina"),
                "top" to listOf("Ylhäällä: rajaus pikseleinä", "Ylhäällä: rajaus prosentteina"),
                "right" to listOf("Oikea: rajaus pikseleinä", "Oikea: rajaus prosentteina"),
                "bottom" to listOf("Alhaalla: rajaus pikseleinä", "Alhaalla: rajaus prosentteina")
            ),
            "et" to mapOf(
                "left" to listOf("Vasak: kärbe pikslites", "Vasak: kärbe protsentides"),
                "top" to listOf("Ülal: kärbe pikslites", "Ülal: kärbe protsentides"),
                "right" to listOf("Parem: kärbe pikslites", "Parem: kärbe protsentides"),
                "bottom" to listOf("All: kärbe pikslites", "All: kärbe protsentides")
            ),
            "lv" to mapOf(
                "left" to listOf("Pa kreisi: apgriešana pikseļos", "Pa kreisi: apgriešana procentos"),
                "top" to listOf("Augšā: apgriešana pikseļos", "Augšā: apgriešana procentos"),
                "right" to listOf("Pa labi: apgriešana pikseļos", "Pa labi: apgriešana procentos"),
                "bottom" to listOf("Apakšā: apgriešana pikseļos", "Apakšā: apgriešana procentos")
            )
        )
        for ((tag, edges) in expected) withLanguage(tag) { activity ->
            val image = AssemblyImage("edge-crop", File(activity.cacheDir, "edge-crop.image"),
                "Image", null, ImageDimensions(24, 16))
            var applied = false
            val dialog = ImageCropDialog(activity, listOf(image), { null }) { applied = true }.show()
            val root = dialog.window!!.decorView
            fun check(unit: Int) {
                shadowOf(Looper.getMainLooper()).idle()
                for ((edge, values) in edges) assertEquals(tag + "/" + edge + "/" + unit,
                    values[unit], root.findViewWithTag<EditText>("crop_" + edge).contentDescription.toString())
            }
            check(0)
            root.findViewWithTag<EditText>("crop_top").setText("4")
            root.findViewWithTag<View>("crop_percent").performClick(); check(1)
            assertEquals("25", root.findViewWithTag<EditText>("crop_top").text.toString())
            root.findViewWithTag<View>("crop_pixels").performClick(); check(0)
            assertEquals("4", root.findViewWithTag<EditText>("crop_top").text.toString())
            root.findViewWithTag<View>("crop_reset").performClick(); check(0)
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            assertFalse(applied)
        }
    }
}
