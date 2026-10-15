/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.content.res.Resources
import android.os.LocaleList
import android.view.View
import android.view.ViewGroup
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
import org.robolectric.RuntimeEnvironment
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale

/** Compiled Japanese resources and the real picker/assembly-help display paths. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class JapaneseActiveGuidanceTest {
    private val context get() = RuntimeEnvironment.getApplication() as Context
    private lateinit var controller: ActivityController<AssemblyActivity>
    private lateinit var activity: AssemblyActivity
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousPlatform: LocaleList
    private var previousTag: String? = null
    private var previousInitialized: Boolean? = null

    @Before fun start() {
        val preferences = context.getSharedPreferences("app-language", Context.MODE_PRIVATE)
        previousTag = preferences.getString("language-tag", null)
        previousInitialized = if (preferences.contains("platform-initialized"))
            preferences.getBoolean("platform-initialized", false) else null
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        previousPlatform = context.getSystemService(LocaleManager::class.java)!!.applicationLocales
        File(context.filesDir, "image-assembly").deleteRecursively()
        AppLanguage.select(context, "ja")
        controller = Robolectric.buildActivity(AssemblyActivity::class.java)
        activity = controller.setup().get()
        AppLanguage.refresh(activity)
        assertEquals("ja", AppLanguage.selectedTag(activity))
        assertEquals("ja", PaintApplication.currentResources.configuration.locales[0].language)
    }

    @After fun stop() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        if (::activity.isInitialized && !activity.isDestroyed) controller.pause().stop().destroy()
        context.getSystemService(LocaleManager::class.java)!!.applicationLocales = previousPlatform
        context.getSharedPreferences("app-language", Context.MODE_PRIVATE).edit().apply {
            if (previousTag == null) remove("language-tag") else putString("language-tag", previousTag)
            if (previousInitialized == null) remove("platform-initialized")
            else putBoolean("platform-initialized", previousInitialized!!)
        }.commit()
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    @Test fun pendingDraftLabelUsesANaturalPendingSaveStatus() {
        assertEquals("下書きの保存待ち", ui(R.string.ui_draft_pending))
    }

    @Test fun actualLanguagePickerShowsMaintenanceAndEnglishFallbackWithoutChangingSelection() {
        val expected = "アプリの言語\n\n翻訳は AN Paint の言語リソースで管理されています。新しいテキストや未翻訳のテキストは英語で表示されます。"
        val dialog = AppLanguage.showPicker(activity) {}
        fun visibleTexts(view: View): List<String> {
            val own = if (view is TextView) listOf(view.text.toString()) else emptyList()
            return own + if (view is ViewGroup)
                (0 until view.childCount).flatMap { visibleTexts(view.getChildAt(it)) } else emptyList()
        }
        assertEquals(expected, ui(R.string.language20_translation_note))
        assertTrue(visibleTexts(dialog.window!!.decorView).contains(expected))
        dialog.dismiss()
        assertEquals("ja", AppLanguage.selectedTag(activity))
    }

    @Test fun actualAssemblyHelpPreservesAllParagraphsAndQualifiesOnlyOptionalDataAndMovement() {
        assertTrue(activity.window.decorView.findViewWithTag<View>("assembly_help").performClick())
        val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val shown = dialog.findViewById<TextView>(android.R.id.message).text.toString()
        assertEquals(ui(R.string.ui_add_up_to_20_images_with_android_s), shown)
        assertEquals(7, shown.split("\n\n").size)
        assertTrue(shown.contains("下部のトレイには、サムネイル、ファイル名、トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法が表示されます。提供元からファイル更新日時を取得できる場合は、その日時も表示されます。"))
        assertTrue(shown.contains("親画像をトリミングすると、そこに接続した画像も移動する場合があります。"))
        assertFalse(shown.contains("下部のトレイには、提供元から取得できる場合、"))
        assertFalse(shown.contains("親画像をトリミングすると、そこに接続した画像も移動します。"))
    }
}
