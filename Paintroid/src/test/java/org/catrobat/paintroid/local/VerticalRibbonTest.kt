/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.os.Looper
import android.view.View
import android.widget.Button
import android.widget.Spinner
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.util.Locale

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[28],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class VerticalRibbonTest {
    @Test fun literaryChineseUsesUprightColumnsAndRemainsAccessible()=check("lzh-Hant","天地玄黃\n宇宙洪荒",TextDirection.VERTICAL_RL)
    @Test fun mongolianUsesJoinedVerticalWordsAndLeftToRightColumns()=check("mn-Mong","ᠮᠣᠩᠭᠣᠯ\nAN Paint",TextDirection.VERTICAL_LR)
    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi") fun landscapeMongolianUsesASideRibbonAndLeavesCanvasHeight()=check("mn-Mong","ᠮᠣᠩᠭᠣᠯ",TextDirection.VERTICAL_LR)
    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi") fun landscapeLiteraryChineseUsesASideRibbonAndLeavesCanvasHeight()=check("lzh-Hant","天地玄黃",TextDirection.VERTICAL_RL)
    private fun check(tag: String,text: String,direction: TextDirection) {
        val context=RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        context.getSharedPreferences("classic-ui",0).edit().clear().commit()
        val old=Locale.getDefault();AppLanguage.select(context,tag)
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity=controller.setup().get()
        fun idle()=shadowOf(Looper.getMainLooper()).idle()
        fun render(view: View,name: String) {
            val image=Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888);view.draw(Canvas(image))
            val file=File("build/reports/classic-preview",(if(activity.resources.configuration.orientation==android.content.res.Configuration.ORIENTATION_LANDSCAPE) "landscape-" else "")+name);file.parentFile.mkdirs()
            file.outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))};image.recycle()
        }
        try {
            idle();val root=activity.window.decorView
            assertEquals(direction,VerticalText.uiDirection());assertEquals(PaintTool.ZOOM,activity.paintCanvas.tool)
            assertEquals(if(tag=="lzh-Hant") "總覽" else "ᠭᠣᠤᠯ",root.findViewWithTag<Button>("menu_Main").text.toString())
            for(tab in listOf("Main","File","Edit","View","Color")) {
                val button=root.findViewWithTag<Button>("menu_$tab")
                assertTrue(button.isShown);assertTrue(button.text.isNotBlank());assertTrue(button.contentDescription.isNotBlank())
            }
            assertTrue(activity.paintCanvas.height>root.height/3)
            assertNotNull(root.findViewWithTag<View>("vertical_status_rail"))
            assertTrue(root.findViewWithTag<View>("undo") is ActionButton)
            assertFalse(root.findViewWithTag<View>("undo") is Button)
            assertTrue(root.findViewWithTag<View>("menu_Main") is RibbonTab)
            val navigate=root.findViewWithTag<ToolButton>("tool_ZOOM")
            assertTrue(navigate.height>0);assertTrue(navigate.width>0)
            render(root,"vertical-ui-$tag.png")
            root.findViewWithTag<View>("menu_File").performClick();idle()
            render(root,"vertical-file-$tag.png")
            val save=SaveOptionsDialog(activity,ExportOptions(),confirm={},cancel={},initialFilename=text.substringBefore('\n')).show();idle()
            try {
                assertNotNull(save.window!!.decorView.findViewWithTag<View>("vertical_save_form"))
                assertNotNull(save.window!!.decorView.findViewWithTag<View>("vertical_dialog"))
                val positive=save.getButton(AlertDialog.BUTTON_POSITIVE)
                assertTrue(positive.isShown)
                assertTrue(positive.height>0)
                val format=save.window!!.decorView.findViewWithTag<Spinner>("export_format")
                val selected=format.selectedView as android.widget.TextView
                val requiredWidth=android.text.Layout.getDesiredWidth(selected.text,selected.paint)
                assertTrue("Format caption must fit without clipping",selected.width-selected.paddingLeft-selected.paddingRight>=requiredWidth)
                if(direction==TextDirection.VERTICAL_RL) {
                    val columns=save.window!!.decorView.findViewWithTag<android.widget.HorizontalScrollView>("vertical_dialog_columns")
                    assertEquals((columns.getChildAt(0).width-columns.width).coerceAtLeast(0),columns.scrollX)
                }
                render(selected,"vertical-format-$tag.png")
                render(save.window!!.decorView,"vertical-save-$tag.png")
            } finally {save.dismiss();idle()}
            root.findViewWithTag<View>("menu_Main").performClick();idle()
            val dialog=TextStyleDialog(activity,TextSettings(text),android.graphics.Color.BLACK,android.graphics.Color.WHITE) {_,_->true}.show();idle()
            try {
                assertEquals(direction.ordinal,dialog.window!!.decorView.findViewWithTag<Spinner>("text_direction").selectedItemPosition)
                val preview=dialog.window!!.decorView.findViewWithTag<View>("text_preview")
                preview.measure(View.MeasureSpec.makeMeasureSpec(600,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(400,View.MeasureSpec.EXACTLY));preview.layout(0,0,600,400)
                render(preview,"vertical-text-$tag.png")
                assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isShown)
            } finally {dialog.dismiss();idle()}
        } finally {
            controller.pause().stop()
            val until=System.nanoTime()+10_000_000_000L
            while(activity.busy && System.nanoTime()<until) {idle();Thread.sleep(10)}
            controller.destroy();AppLanguage.select(context,"");Locale.setDefault(old)
        }
    }
}
