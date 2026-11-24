/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.AlertDialog
import android.app.LocaleManager
import android.graphics.Rect
import android.icu.text.PluralRules
import android.os.LocaleList
import android.view.View
import android.widget.TextView
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AssemblyImage
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ImageCropDialog
import org.catrobat.paintroid.classic.ImageDimensions
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.util.Locale

/** Installed-resource routing and the Batch Crop dialog consumer, not locale fluency
 * or physical input/layout acceptance. Synthetic image metadata; no files opened. */
@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=35,maxSdkVersion=35)
class CropSelectionCountDeviceTest {
    @Test fun brazilianPortugueseCropSelectionCountIsExposedAtZeroOneAndTwo() {
        val instrumentation=InstrumentationRegistry.getInstrumentation()
        val context=instrumentation.targetContext
        val prefs=context.getSharedPreferences("app-language",0)
        val savedTag=prefs.getString("language-tag",null)
        val platformKey="platform-initialized"
        val savedPlatform=if(prefs.contains(platformKey)) prefs.getBoolean(platformKey,false) else null
        val manager=context.getSystemService(LocaleManager::class.java)
        val savedLocales=manager.applicationLocales
        val savedDefault=Locale.getDefault()
        val tag="pt-BR"
        val locale=Locale.forLanguageTag(tag)

        try {
            instrumentation.runOnMainSync {
                prefs.edit().putString("language-tag",tag).putBoolean(platformKey,true).commit()
                manager.applicationLocales=LocaleList.forLanguageTags(tag)
            }
            instrumentation.waitForIdleSync()
            val launch=checkNotNull(context.packageManager.getLaunchIntentForPackage(context.packageName))
            ActivityScenario.launch<ClassicPaintActivity>(launch).use { scenario ->
                lateinit var dialog: AlertDialog
                lateinit var inputs: List<AssemblyImage>
                var applications=0
                scenario.onActivity { activity ->
                    assertEquals(tag,activity.resources.configuration.locales[0].toLanguageTag())
                    assertEquals("one",PluralRules.forLocale(locale).select(0.0))
                    assertEquals("one",PluralRules.forLocale(locale).select(1.0))
                    assertEquals("other",PluralRules.forLocale(locale).select(2.0))
                    // The shared zero/one quantity must use a count label, not a
                    // singular command at zero. Do not freeze the localized prose.
                    assertEquals(activity.resources.getQuantityString(R.plurals.ui_crop_preview_images,2),
                        activity.resources.getQuantityString(R.plurals.ui_crop_preview_images,0))
                    inputs=(1..2).map { index ->
                        AssemblyImage("crop-$index",File(context.cacheDir,"unopened-crop-$index.png"),
                            "Fixture $index.png",null,ImageDimensions(24,16))
                    }
                    dialog=ImageCropDialog(activity,inputs,{null},{applications++}).show()
                }
                instrumentation.waitForIdleSync()
                scenario.onActivity { activity ->
                    try {
                        val root=checkNotNull(dialog.window).decorView
                        val status=root.findViewWithTag<TextView>("crop_status")
                        fun verify(count: Int) {
                            val expected=activity.resources.getQuantityString(R.plurals.ui_crop_preview_images,count,24,16,count)
                            assertEquals("Visible crop count $count",expected,status.text.toString())
                            val node=status.createAccessibilityNodeInfo()
                            try { assertEquals("Accessible crop count $count",expected,node.text.toString()) }
                            finally { node.recycle() }
                        }
                        verify(2)
                        root.findViewWithTag<View>("crop_none").performClick()
                        verify(0)
                        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
                        assertTrue("No selected target leaves the dialog open",dialog.isShowing)
                        assertEquals(activity.getString(R.string.ui_choose_at_least_one_image),status.text.toString())
                        root.findViewWithTag<View>("crop_include_crop-1").performClick()
                        verify(1)
                        root.findViewWithTag<View>("crop_all").performClick()
                        verify(2)
                        assertEquals(0,applications)
                        assertEquals(listOf(Rect(0,0,24,16),Rect(0,0,24,16)),inputs.map { it.crop })
                    } finally {dialog.dismiss()}
                }
            }
        } finally {
            instrumentation.runOnMainSync {
                val edit=prefs.edit()
                if(savedTag==null) edit.remove("language-tag") else edit.putString("language-tag",savedTag)
                if(savedPlatform==null) edit.remove(platformKey) else edit.putBoolean(platformKey,savedPlatform)
                edit.commit()
                manager.applicationLocales=savedLocales
                Locale.setDefault(savedDefault)
            }
            instrumentation.waitForIdleSync()
        }
    }
}
