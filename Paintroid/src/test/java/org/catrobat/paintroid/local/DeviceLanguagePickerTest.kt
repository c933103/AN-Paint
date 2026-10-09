/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.app.LocaleManager
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Canvas
import android.os.Build
import android.os.Looper
import android.text.Spanned
import android.text.style.ReplacementSpan
import android.widget.ArrayAdapter
import android.widget.CheckedTextView
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale

/** System resources are controlled here; Android's global language setting is not changed. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35], qualifiers="en-rUS-w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class DeviceLanguagePickerTest {
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    @Suppress("DEPRECATION")
    private fun locale(config: Configuration)=if(Build.VERSION.SDK_INT>=24) config.locales[0] else config.locale
    private fun spans(row: TextView)=(row.text as? Spanned)
        ?.getSpans(0,row.text.length,ReplacementSpan::class.java).orEmpty()

    @Suppress("DEPRECATION")
    private fun withActivity(check: (Activity) -> Unit) {
        val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        val system=Resources.getSystem()
        val oldSystem=Configuration(system.configuration)
        val controller=Robolectric.buildActivity(Activity::class.java)
        val activity=controller.get()
        activity.setTheme(R.style.ClassicPaintTheme)
        controller.setup()
        val oldActivity=Configuration(activity.resources.configuration)
        val manager=if(Build.VERSION.SDK_INT>=33) activity.getSystemService(LocaleManager::class.java) else null
        val oldPlatformLocales=manager?.applicationLocales
        try {check(activity)} finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss();idle()
            controller.pause().stop().destroy()
            system.updateConfiguration(oldSystem,system.displayMetrics)
            activity.resources.updateConfiguration(oldActivity,activity.resources.displayMetrics)
            activity.getSharedPreferences("app-language",0).edit().clear().commit()
            if(oldPlatformLocales!=null) manager.applicationLocales=oldPlatformLocales
            PaintApplication.currentResources=oldResources
            Locale.setDefault(oldLocale)
        }
    }

    @Suppress("DEPRECATION")
    private fun languages(activity: Activity,deviceTag: String,appTag: String) {
        val system=Resources.getSystem()
        system.updateConfiguration(Configuration(system.configuration).apply {
            val locale=Locale.forLanguageTag(deviceTag);setLocale(locale);setLayoutDirection(locale)
        },system.displayMetrics)
        AppLanguage.select(activity,appTag)
        AppLanguage.refresh(activity)
        assertEquals(appTag,AppLanguage.selectedTag(activity))
        assertEquals(deviceTag,locale(system.configuration).toLanguageTag())
    }

    private fun expectedLabel(activity: Activity,deviceTag: String): String =
        activity.createConfigurationContext(Configuration().apply {
            fontScale=0f
            val locale=Locale.forLanguageTag(deviceTag);setLocale(locale);setLayoutDirection(locale)
        }).getString(R.string.language20_device_default)

    private fun checkRow(activity: Activity,row: TextView,tag: String,label: String) {
        val locale=Locale.forLanguageTag(tag)
        assertEquals(tag,locale,row.textLocale)
        assertEquals(tag,label,row.text.toString())
        val vertical=VerticalText.uiDirection(locale)!=TextDirection.HORIZONTAL
        assertEquals(tag,if(vertical) 1 else 0,spans(row).size)
        if(!vertical) LocaleTypography.typeface(activity,locale)?.let {assertSame(tag,it,row.typeface)}
        assertTrue(tag,row is CheckedTextView)
    }

    private fun checkAccessibility(row: TextView,tag: String,label: String) {
        val info=row.createAccessibilityNodeInfo()
        try {
            assertEquals(tag,label,info.text.toString())
            assertTrue(tag,info.isCheckable)
        } finally {info.recycle()}
    }

    private fun firstMountedRow(picker: AlertDialog): TextView {
        // Opening a single-choice list scrolls to the checked app override, not row 0.
        picker.listView.setSelectionFromTop(0,0);idle()
        assertEquals(0,picker.listView.firstVisiblePosition)
        return picker.listView.getChildAt(0) as TextView
    }

    @Test fun originalFirstRowSequenceLeavesDeviceScriptUnformatted()=withActivity { activity ->
        for(tag in listOf("mn-Mong","mnc-Mong","lzh-Hant")) {
            languages(activity,tag,"en-001")
            val expected=expectedLabel(activity,tag)
            assertNotEquals("Control must use the device catalogue",activity.getString(R.string.language20_device_default),expected)
            val picker=AppLanguage.showPicker(activity) {}
            try {
                // Exact pre-fix row-0 sequence: native adapter + textLocale only.
                val control=ArrayAdapter(activity,android.R.layout.simple_list_item_single_choice,listOf(expected))
                    .getView(0,null,picker.listView) as TextView
                control.textLocale=Locale.forLanguageTag(tag)
                assertEquals(expected,control.text.toString())
                assertTrue("The original row has no vertical span",spans(control).isEmpty())
                val repaired=picker.listView.adapter.getView(0,null,picker.listView) as TextView
                checkRow(activity,repaired,tag,expected)
                checkAccessibility(repaired,tag,expected)
            } finally {picker.dismiss();idle()}
        }
    }

    @Test @Config(sdk=[21,25]) @GraphicsMode(GraphicsMode.Mode.LEGACY)
    fun legacyDeviceRowsUseDeviceResourcesAndSharedTypographyWithoutAppOverrideLeakage()=withActivity { activity ->
        for(tag in listOf("en-US","ar","vi-Hani","wuu-Hans","mn-Mong","mnc-Mong","lzh-Hant","zz-Zzzz-ZZ")) {
            for(appTag in listOf("ja","en-001")) {
                languages(activity,tag,appTag)
                val picker=AppLanguage.showPicker(activity) {}
                try {
                    val row=picker.listView.adapter.getView(0,null,picker.listView) as TextView
                    checkRow(activity,row,tag,expectedLabel(activity,tag))
                    // API21 node initialization dereferences real attachment state.
                    val mounted=firstMountedRow(picker)
                    checkRow(activity,mounted,tag,expectedLabel(activity,tag))
                    checkAccessibility(mounted,tag,expectedLabel(activity,tag))
                    if(tag=="mn-Mong" || tag=="mnc-Mong")
                        assertNotEquals(activity.getString(R.string.language20_device_default),row.text.toString())
                    assertEquals(appTag,AppLanguage.selectedTag(activity))
                } finally {picker.dismiss();idle()}
            }
        }
    }

    @Test fun everyOfferedDeviceLocaleUsesTheSameFormattingAsExplicitChoices()=withActivity { activity ->
        val tags=AppLanguage.tags(activity)
        assertEquals(140,tags.size)
        for(tag in tags) {
            languages(activity,tag,"ja")
            val picker=AppLanguage.showPicker(activity) {}
            try {
                val list=picker.listView
                val explicit=list.adapter.getView(tags.indexOf(tag)+1,null,list) as TextView
                checkRow(activity,explicit,tag,AppLanguage.name(tag))
                checkAccessibility(explicit,tag,AppLanguage.name(tag))
                // The adapter deliberately does not recycle script-specific row geometry.
                val first=list.adapter.getView(0,explicit,list) as TextView
                assertNotSame(tag,explicit,first)
                checkRow(activity,first,tag,expectedLabel(activity,tag))
                checkAccessibility(first,tag,expectedLabel(activity,tag))
                assertEquals(tag,"ja",AppLanguage.selectedTag(activity))
            } finally {picker.dismiss();idle()}
        }
    }

    @Test fun regionalAndUnsupportedDeviceTagsRetainFrameworkResourceFallback()=withActivity { activity ->
        for(tag in listOf("fr-CA","ja-JP","ar-EG","mn-Cyrl-CN","zz-Zzzz-ZZ")) {
            languages(activity,tag,"ja")
            val picker=AppLanguage.showPicker(activity) {}
            try {
                val row=picker.listView.adapter.getView(0,null,picker.listView) as TextView
                checkRow(activity,row,tag,expectedLabel(activity,tag))
                checkAccessibility(row,tag,expectedLabel(activity,tag))
                assertEquals("ja",AppLanguage.selectedTag(activity))
                if(tag=="zz-Zzzz-ZZ") assertEquals("Use device language",picker.listView.adapter.getItem(0))
            } finally {picker.dismiss();idle()}
        }
    }

    // Literal source-catalogue oracles must not share the production context-resolution path.
    private val deviceLabels=mapOf(
        "en-US" to "Use device language", "ar" to "استخدام لغة النظام",
        "vi-Hani" to "用 言語 系統", "wuu-Hans" to "使用系统语言",
        "mn-Mong" to "ᠲᠥᠬᠥᠭᠡᠷᠦᠮᠵᠢ ᠶᠢᠨ ᠬᠡᠯᠡ ᠶᠢ ᠠᠰᠢᠭᠯᠠᠬᠤ",
        "mnc-Mong" to "ᠠᡤᡡᡵᠠ ᡳ ᡤᡳᠰᡠᠨ ᠪᡝ ᠪᠠᡳᡨᠠᠯᠠᡵᠠ",
        "lzh-Hant" to "從系統之語言", "en-XV" to "Use device language",
        "qaa-Zsye-XV" to "🌐 Use device language"
    )

    @Test fun realEditorOverrideSwitchesKeepTheIndependentEnglishDeviceLabel() {
        val context=org.robolectric.RuntimeEnvironment.getApplication<android.app.Application>()
        val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        AppLanguage.select(context,"en-001")
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity=controller.get()
        try {
            awaitEditorStartup(activity)
            assertEquals("en-US",locale(Resources.getSystem().configuration).toLanguageTag())
            for(appTag in listOf("ja","ar","en-001")) {
                AppLanguage.select(activity,appTag);AppLanguage.refresh(activity)
                val picker=AppLanguage.showPicker(activity) {}
                try {
                    val row=firstMountedRow(picker)
                    checkRow(activity,row,"en-US","Use device language")
                    checkAccessibility(row,"en-US","Use device language")
                } finally {picker.dismiss();idle()}
            }
        } finally {
            controller.pause().stop()
            val until=System.nanoTime()+10_000_000_000L
            while(activity.busy && System.nanoTime()<until) {idle();Thread.sleep(10)}
            controller.destroy()
            AppLanguage.select(context,"")
            context.getSharedPreferences("app-language",0).edit().clear().commit()
            PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)
        }
    }

    @Test fun repeatedOpenAndAppOverrideSwitchKeepMountedLabelsAccessibleAndTouchSized()=withActivity { activity ->
        for(tag in listOf("en-US","ar","vi-Hani","wuu-Hans","mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) {
            for((index,appTag) in listOf("ja","ar","en-001").withIndex()) {
                languages(activity,tag,appTag)
                val picker=AppLanguage.showPicker(activity) {}
                try {
                    val row=firstMountedRow(picker)
                    row.textSize=if(index==1) 24f else 16f
                    idle()
                    val label=deviceLabels.getValue(tag)
                    checkRow(activity,row,tag,label)
                    checkAccessibility(row,tag,label)
                    assertSame("Measured row must remain mounted",row,picker.listView.getChildAt(0))
                    assertTrue("$tag/$appTag row must retain a 48dp touch target",row.height>=48*activity.resources.displayMetrics.density)
                    val layout=requireNotNull(row.layout)
                    assertEquals(label.length,layout.getLineEnd(layout.lineCount-1))
                    assertEquals(0,layout.getEllipsisCount(layout.lineCount-1))
                    assertTrue("$tag/$appTag layout ${layout.height} in row ${row.height}",layout.height<=row.height-row.totalPaddingTop-row.totalPaddingBottom)
                    if(index==1) {
                        val image=Bitmap.createBitmap(row.width,row.height,Bitmap.Config.ARGB_8888)
                        try {
                            row.draw(Canvas(image))
                            val file=File("build/reports/classic-preview/device-language-$tag-api${Build.VERSION.SDK_INT}.png")
                            requireNotNull(file.parentFile).mkdirs();file.outputStream().use {image.compress(Bitmap.CompressFormat.PNG,100,it)}
                        } finally {image.recycle()}
                    }
                } finally {picker.dismiss();idle()}
            }
        }
    }

    @Test fun cancelDefaultAndExplicitSelectionsKeepTheirOriginalMeaning()=withActivity { activity ->
        languages(activity,"mnc-Mong","ja")
        var changed=0
        var picker=AppLanguage.showPicker(activity) {changed++}
        picker.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
        assertEquals(0,changed);assertEquals("ja",AppLanguage.selectedTag(activity))
        picker=AppLanguage.showPicker(activity) {changed++}
        picker.listView.performItemClick(picker.listView.adapter.getView(0,null,picker.listView),0,0)
        idle()
        assertFalse(picker.isShowing);assertEquals(1,changed)
        assertEquals("",AppLanguage.selectedTag(activity))
        assertEquals("mnc-Mong",activity.resources.configuration.locales[0].toLanguageTag())
        picker=AppLanguage.showPicker(activity) {changed++}
        picker.listView.performItemClick(picker.listView.adapter.getView(0,null,picker.listView),0,0)
        idle();assertEquals(1,changed)
        picker=AppLanguage.showPicker(activity) {changed++}
        val index=AppLanguage.tags(activity).indexOf("en-001")+1
        picker.listView.performItemClick(picker.listView.adapter.getView(index,null,picker.listView),index,index.toLong())
        idle()
        assertFalse(picker.isShowing);assertEquals(2,changed)
        assertEquals("en-001",AppLanguage.selectedTag(activity))
    }
}
