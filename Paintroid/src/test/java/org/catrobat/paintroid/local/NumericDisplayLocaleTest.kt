/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.ActivityManager
import android.app.AlertDialog
import android.content.Context
import android.graphics.RectF
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.Assert.*
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

/** Tests the actual captions, warning and accessibility consumers, not a replacement formatter. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35], qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class NumericDisplayLocaleTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private lateinit var oldLocale: Locale
    private lateinit var oldTag: String
    private val tags=listOf("pt-BR", "de", "en-001", "ar", "ro")

    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        oldLocale=Locale.getDefault(); oldTag=AppLanguage.selectedTag(context)
        listOf("classic-recovery.png", "classic-autosave.zip", "classic-autosave.zip.bak").forEach {File(context.filesDir,it).delete()}
        AutosaveStore(context.filesDir).recoveryCopies().forEach {it.delete()}
        context.getSharedPreferences("classic-ui",Context.MODE_PRIVATE).edit().clear().commit()
        context.getSharedPreferences("recent-colours",Context.MODE_PRIVATE).edit().clear().commit()
        // Three real stored colours leave one empty cell for the contrasting index path.
        RecentColours(context).apply {add(0xffabcdef.toInt());add(0xff00120f.toInt());add(0xfffedcba.toInt())}
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        activity=controller.setup().get(); awaitEditorStartup(activity)
        activity.document.newImage(200,100); activity.paintCanvas.fit()
        // Pin the system-limited budget; JVM heap churn must not change the caption
        // between opening the dialog and observing its actual TextView.
        shadowOf(activity.getSystemService(ActivityManager::class.java)).setMemoryInfo(ActivityManager.MemoryInfo().apply {
            totalMem=1_000_000_000L; availMem=3*(32L*1024*1024+27_000_000L); threshold=0
        })
    }

    @After fun stop() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        controller.pause().stop()
        val deadline=System.nanoTime()+10_000_000_000L
        while(activity.busy && System.nanoTime()<deadline) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
        controller.destroy()
        AppLanguage.select(activity,oldTag);AppLanguage.refresh(activity);Locale.setDefault(oldLocale)
    }

    private fun select(tag: String) {
        AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
        assertEquals(Locale.forLanguageTag(tag).language,activity.resources.configuration.locales[0].language)
        // AppLanguage normally aligns these. Deliberately desynchronize them so a
        // process-default formatter cannot accidentally satisfy these assertions.
        Locale.setDefault(if(tag=="en-001") Locale.GERMANY else Locale.US)
    }
    private fun expected(id: Int,vararg args: Any): String =
        String.format(activity.resources.configuration.locales[0],activity.getString(id),*args)
    private fun policy(pixels: Long): ImageMemoryPolicy {
        val reserve=32L*1024*1024
        return ImageMemoryPolicy.calculate(reserve+pixels*12,0,(reserve+pixels*12)*3,0,false)
    }
    private fun texts(view: View): List<String> = when(view) {
        is TextView -> listOf(view.text.toString())
        is ViewGroup -> (0 until view.childCount).flatMap {texts(view.getChildAt(it))}
        else -> emptyList()
    }

    @Test fun oversizeWarningUsesResourceDigitsAndDecimalsWithoutChangingAdmission() {
        val limit=policy(2_250_000)
        for(tag in tags) {
            select(tag)
            assertEquals(2_250_000L,limit.maxPixels())
            limit.check(1500,1500)
            val failure=assertThrows(ImageSizeException::class.java) {limit.check(1500,2000)}
            assertEquals(tag,expected(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current,1500,2000,3.0,2.25),failure.message)
            if(tag=="pt-BR") {assertTrue(failure.message!!.contains("3,00 MP"));assertTrue(failure.message!!.contains("2,25 MP"))}
            if(tag=="ar") {assertTrue(failure.message!!.contains("١٥٠٠"));assertTrue(failure.message!!.contains("٢٫٢٥"))}
            // Romanian now has its own reviewed warning; keep literal decimal checks
            // independent of the resource formatter and the deliberately US process locale.
            if(tag=="ro") {
                assertTrue(failure.message!!.startsWith("Dimensiunea de 1500 × 2000 pixeli (3,00 MP)"))
                assertTrue(failure.message!!.contains("2,25 MP"))
            }
            assertEquals(2_249_999L,limit.maxPixels(3))
            assertThrows(ImageSizeException::class.java) {limit.check(1500,1500,3)}
            assertThrows(IllegalArgumentException::class.java) {limit.check(0,1)}
        }
    }

    @Test fun resizeBudgetRefreshUsesResourceLocaleAndCancelPreservesInputs() {
        // Literal full captions exercise both formatting layers independently:
        // 27,000,000 bytes = 25.7 MiB; 18,000,000 bytes = 17.2 MiB.
        // Do not compute expectations using the production memoryLabel helper.
        val captions=mapOf(
            "pt-BR" to ("Limite seguro de edição atual: 25,7 MiB · até 2,25 MP antes da sobrecarga do decodificador" to
                "Limite seguro de edição atual: 17,2 MiB · até 1,50 MP antes da sobrecarga do decodificador"),
            "de" to ("Aktuelles sicheres Bearbeitungslimit: 25,7 MiB · bis zu 2,25 MP vor Decoder-Overhead" to
                "Aktuelles sicheres Bearbeitungslimit: 17,2 MiB · bis zu 1,50 MP vor Decoder-Overhead"),
            "en-001" to ("Current safe editing budget: 25.7 MiB · up to 2.25 MP before decoder overhead" to
                "Current safe editing budget: 17.2 MiB · up to 1.50 MP before decoder overhead"),
            "ar" to ("حد التحرير الآمن الحالي: ٢٥٫٧ MiB · حتى ٢٫٢٥ ميغابكسل قبل الحمل الإضافي لفك الترميز" to
                "حد التحرير الآمن الحالي: ١٧٫٢ MiB · حتى ١٫٥٠ ميغابكسل قبل الحمل الإضافي لفك الترميز"),
            "ro" to ("Current safe editing budget: 25,7 MiB · up to 2,25 MP before decoder overhead" to
                "Current safe editing budget: 17,2 MiB · up to 1,50 MP before decoder overhead")
        )
        for(tag in tags) {
            select(tag)
            val (initialCaption,updatedCaption)=captions.getValue(tag)
            var limit=policy(2_250_000)
            var applied=false;var cancelled=false
            val dialog=ImageResizeDialog(activity,ImageDimensions(2000,2000),0,{limit},
                resize={applied=true},cancel={cancelled=true}).show()
            // The production refresh and validating listener are installed by
            // queued OnShow; observe the dialog after that lifecycle callback.
            shadowOf(Looper.getMainLooper()).idle()
            val root=dialog.window!!.decorView
            val label=root.findViewWithTag<TextView>("resize_budget")
            assertEquals(tag,initialCaption,label.text.toString())
            if(tag=="pt-BR") assertTrue(label.text.toString().contains("2,25 MP"))
            if(tag=="ro") assertTrue(label.text.toString().startsWith("Current safe editing budget:"))
            limit=policy(1_500_000)
            root.findViewWithTag<EditText>("resize_width").setText("1000")
            assertEquals(tag,updatedCaption,label.text.toString())
            assertEquals("1000",root.findViewWithTag<EditText>("resize_width").text.toString())
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            shadowOf(Looper.getMainLooper()).idle()
            assertFalse(dialog.isShowing)
            assertTrue(cancelled);assertFalse(applied)
        }
    }

    @Test fun newResizeAndCanvasBudgetCaptionsFollowSelectedLocale() {
        for(tag in tags) {
            select(tag)
            for((tab,index) in listOf("File" to 0,"Edit" to 3,"Edit" to 5)) {
                activity.document.markSaved()
                EditorTestNavigation.command(activity,tab,index)
                val dialog=ShadowAlertDialog.getLatestAlertDialog()
                val budget=ImageMemoryPolicy.forDevice(activity).maxPixels(activity.document.residentPixels)/1_000_000.0
                assertTrue("$tag / $tab $index",texts(dialog.window!!.decorView).contains(expected(R.string.ui_current_safe_budget_2f_mp,budget)))
                if(tag=="ro") assertTrue(texts(dialog.window!!.decorView).any {it.startsWith("Current safe budget:")})
                val original=activity.document.bitmap
                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                assertSame(original,activity.document.bitmap)
            }
        }
    }

    @Test fun selectionCaptionUsesLocalizedRotationAndPreservesGeometry() {
        for(tag in tags) {
            select(tag)
            EditorTestNavigation.click(activity,"tool_SELECT")
            activity.document.select(RectF(10f,10f,160f,90f))
            activity.document.selection!!.rotation=12.5f
            activity.paintCanvas.zoomAt(1f)
            val label=activity.window.decorView.findViewWithTag<TextView>("selection_dimensions")
            assertEquals(tag,expected(R.string.ui_0f_0f_px_1f,150f,80f,12.5f),label.text.toString())
            if(tag=="pt-BR") assertEquals("150 × 80 px\n12,5°",label.text.toString())
            if(tag=="ar") assertTrue(label.text.toString().contains("١٢٫٥°"))
            assertEquals(RectF(10f,10f,160f,90f),activity.document.selection!!.rect)
            assertEquals(12.5f,activity.document.selection!!.rotation,0f)
        }
    }

    @Test fun recentColourIndicesLocalizeWhileHexAndStoredValuesStayInvariant() {
        for(tag in tags) {
            select(tag)
            activity.getSharedPreferences("recent-colours",Context.MODE_PRIVATE).edit().clear().commit()
            RecentColours(activity).apply {add(0xffabcdef.toInt());add(0xff00120f.toInt());add(0xfffedcba.toInt())}
            // Opening a real colour cell refreshes the stored-colour descriptions.
            EditorTestNavigation.click(activity,"menu_Color")
            activity.window.decorView.findViewWithTag<View>("recent_colour_0").performClick()
            val colours=RecentColours(activity).colours
            for(index in 0..3) {
                val cell=activity.window.decorView.findViewWithTag<View>("recent_colour_$index")
                val colour=colours.getOrNull(index)
                val wanted=if(colour==null) expected(R.string.ui_recent_colour_empty,String.format(activity.resources.configuration.locales[0],"%d",index+1))
                    else expected(R.string.ui_recent_colour_d_06x_tap_foreground_hold_background,index+1,colour and 0xffffff)
                assertEquals("$tag / $index",wanted,cell.contentDescription.toString())
                assertEquals(colour!=null,cell.isEnabled)
            }
            val third=activity.window.decorView.findViewWithTag<View>("recent_colour_2").contentDescription.toString()
            assertTrue(third.contains("#ABCDEF"))
            if(tag=="ar") {assertTrue(third.contains("٣"));assertFalse(third.contains(" 3:"))}
            assertEquals(listOf(0xfffedcba.toInt(),0xff00120f.toInt(),0xffabcdef.toInt()),colours)
            val fourth=activity.window.decorView.findViewWithTag<View>("recent_colour_3")
            val emptyCaption=fourth.contentDescription.toString()
            if(tag=="ar") {assertTrue(emptyCaption.contains("٤"));assertFalse(emptyCaption.contains(" 4:"))}
            assertTrue(activity.window.decorView.findViewWithTag<View>("colour_000000").performClick())
            assertTrue(fourth.isEnabled)
            assertEquals(expected(R.string.ui_recent_colour_d_06x_tap_foreground_hold_background,4,0xabcdef),fourth.contentDescription.toString())
            assertTrue(fourth.contentDescription.toString().contains("#ABCDEF"))
            // Model a cleared history, then exercise the same production refresh to
            // verify that a previously populated cell returns to its localized empty state.
            activity.getSharedPreferences("recent-colours",Context.MODE_PRIVATE).edit().clear().commit()
            assertTrue(activity.window.decorView.findViewWithTag<View>("colour_000000").performClick())
            assertFalse(fourth.isEnabled)
            assertEquals(emptyCaption,fourth.contentDescription.toString())
            assertEquals(listOf(0xff000000.toInt()),RecentColours(activity).colours)
        }
    }

    @Test fun zoomLabelAndItsStatusAndAccessibilityConsumersUseSelectedLocale() {
        // A narrow explicit viewport permits the existing low-zoom branch without
        // allocating an oversized bitmap or bypassing the production zoom clamp.
        activity.document.newImage(1000,1000)
        activity.paintCanvas.layout(0,0,120,120)
        for(tag in tags) {
            select(tag)
            for((zoom,wanted) in listOf(.025f to if(tag=="ar") "٢٫٥٠%" else if(tag in listOf("pt-BR","de","ro")) "2,50%" else "2.50%",
                .1f to if(tag=="ar") "١٠%" else "10%",1.234f to if(tag=="ar") "١٢٣%" else "123%")) {
                activity.paintCanvas.zoomAt(zoom)
                assertEquals("$tag clamp",zoom,activity.paintCanvas.zoom,0f)
                assertEquals(tag,wanted,activity.paintCanvas.zoomLabel())
                assertTrue(activity.paintCanvas.zoomStatusLabel().startsWith(wanted))
                assertEquals(expected(R.string.ui_canvas_zoom_771f84,wanted),activity.window.decorView.findViewWithTag<View>("zoom_slider").contentDescription.toString())
            }
        }
    }
}
