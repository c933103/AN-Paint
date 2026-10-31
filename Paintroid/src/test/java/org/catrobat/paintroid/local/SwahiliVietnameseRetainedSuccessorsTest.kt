/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Rect
import android.os.Looper
import android.view.View
import android.widget.CheckBox
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
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale
import java.util.UUID
import java.util.concurrent.TimeUnit

/** Exact retained successors and real consumers; no new whole-language or device acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class SwahiliVietnameseRetainedSuccessorsTest {
    private lateinit var previousTag: String
    private lateinit var previousLocale: Locale
    private lateinit var previousResources: Resources
    private val app get()=RuntimeEnvironment.getApplication() as Context
    private fun expected(tag: String,key: String)=PriorityWordingExpectations.resourceText(tag,key)
    private fun plural(tag: String,count: Int)=PriorityWordingExpectations.resources(tag)
        .getQuantityString(R.plurals.ui_crop_preview_images,count,24,16,count)
    @Before fun rememberLanguage() {
        previousTag=AppLanguage.selectedTag(app);previousLocale=Locale.getDefault();previousResources=PaintApplication.currentResources
    }
    @After fun restoreLanguage() {
        AppLanguage.select(app,previousTag);PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }
    private fun editor(tag: String,check: (ClassicPaintActivity)->Unit) {
        app.filesDir.listFiles()?.filter {it.name.startsWith("classic-") }?.forEach {it.delete()}
        app.getSharedPreferences("classic-ui",0).edit().clear().commit()
        AppLanguage.select(app,tag)
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity=controller.setup().get()
        try {
            awaitEditorStartup(activity);shadowOf(Looper.getMainLooper()).idle()
            Locale.setDefault(Locale.US)
            assertEquals(tag,AppLanguage.selectedTag(activity));check(activity)
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            controller.pause().stop()
            val end=System.nanoTime()+15_000_000_000L
            while(activity.busy && System.nanoTime()<end) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
            assertFalse(activity.busy);controller.destroy()
        }
    }

    @Test fun swahiliReturnToDrawingRestoresTheToolWithoutRedrawingOrChangingHistory()=editor("sw") { activity ->
        activity.document.newImage(24,16)
        EditorTestNavigation.click(activity,"tool_BRUSH")
        val before=activity.document.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        val dirty=activity.document.dirty;val undo=activity.document.canUndo;val redo=activity.document.canRedo
        try {
            repeat(2) {
                EditorTestNavigation.click(activity,"tool_ZOOM")
                assertEquals(PaintTool.ZOOM,activity.paintCanvas.tool)
                val back=activity.window.decorView.findViewWithTag<TextView>("navigate_draw")
                assertEquals(expected("sw","ui_draw_again"),back.text.toString())
                EditorTestNavigation.click(activity,"navigate_draw")
                assertEquals(PaintTool.BRUSH,activity.paintCanvas.tool)
                assertTrue(before.sameAs(activity.document.bitmap))
                assertEquals(dirty,activity.document.dirty);assertEquals(undo,activity.document.canUndo);assertEquals(redo,activity.document.canRedo)
            }
        } finally {before.recycle()}
    }

    @Test fun vietnameseMagnifierLabelControlsCursorAndActivePreviewWithoutAStrokeRestriction()=editor("vi") { activity ->
        EditorTestNavigation.command(activity,"View",2)
        EditorTestNavigation.click(activity,"cursor_mode_enabled")
        val cursor=activity.window.decorView.findViewWithTag<CheckBox>("cursor_magnifier_enabled")
        assertEquals(expected("vi","ui_show_magnified_drawing_preview"),cursor.text.toString())
        if(!cursor.isChecked) {assertTrue(cursor.performClick());shadowOf(Looper.getMainLooper()).idle()}
        assertTrue(activity.paintCanvas.cursorMagnifier);assertTrue(activity.paintCanvas.magnifierVisible)
        repeat(2) {
            EditorTestNavigation.command(activity,"View",3)
            val dialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
            val active=dialog.window!!.decorView.findViewWithTag<CheckBox>("magnifier_enabled")
            assertEquals(expected("vi","ui_show_magnified_drawing_preview"),active.text.toString())
            val was=active.isChecked;active.performClick();assertEquals(!was,activity.paintCanvas.cursorMagnifier)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(dialog.isShowing)
            assertEquals(!was,activity.window.decorView.findViewWithTag<CheckBox>("cursor_magnifier_enabled").isChecked)
        }
    }

    @Test fun completeCropPluralChildrenAppearForZeroOneAndManyAndCancelPreservesSources() {
        for(tag in listOf("sw","vi")) {
            AppLanguage.select(app,tag)
            val controller=Robolectric.buildActivity(Activity::class.java)
            val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup();AppLanguage.refresh(activity)
            val directory=File(activity.cacheDir,"retained-crop-${UUID.randomUUID()}").apply {mkdirs()}
            try {
                Locale.setDefault(Locale.US)
                val images=(1..3).map { i ->
                    val file=File(directory,"$i.image").apply {writeText("unchanged source $i")}
                    AssemblyImage("image$i",file,"$i.png",null,ImageDimensions(24,16))
                }
                var applied=false
                val dialog=ImageCropDialog(activity,images,{null}) {applied=true}.show()
                try {
                    val root=dialog.window!!.decorView;shadowOf(Looper.getMainLooper()).idle()
                    fun check(count: Int) {
                        assertEquals(plural(tag,count),root.findViewWithTag<TextView>("crop_status").text.toString())
                        assertEquals(plural(tag,count),uiQuantity(activity.resources,R.plurals.ui_crop_preview_images,count,24,16,count))
                    }
                    check(3);root.findViewWithTag<View>("crop_none").performClick();check(0)
                    root.findViewWithTag<CheckBox>("crop_include_image1").isChecked=true;check(1)
                    root.findViewWithTag<CheckBox>("crop_include_image2").isChecked=true;check(2)
                    dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
                    assertFalse(dialog.isShowing);assertFalse(applied)
                    images.forEachIndexed { index,image ->assertEquals(Rect(0,0,24,16),image.crop);assertEquals("unchanged source ${index+1}",image.file.readText())}
                } finally {dialog.dismiss()}
            } finally {directory.deleteRecursively();controller.pause().stop().destroy()}
        }
    }

    @Test fun actualAttachmentGeometryCanMoveOneChildWhileAnotherStaysAndUndoRestoresBoth() {
        val directory=File(app.cacheDir,"retained-geometry-${UUID.randomUUID()}")
        try {
            val model=ImageAssembly(directory)
            fun item(id: String,w: Int,h: Int): AssemblyImage {
                val file=File(directory,"$id.image")
                val bitmap=Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888)
                try {file.outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {bitmap.recycle()}
                return AssemblyImage(id,file,id,null,ImageDimensions(w,h))
            }
            val parent=item("parent",24,16);val right=item("right",8,8);val bottom=item("bottom",8,8)
            model.add(listOf(parent,right,bottom));model.place(parent.id,Attachment(null,null))
            model.place(right.id,Attachment(parent.id,SnapEdge.RIGHT));model.place(bottom.id,Attachment(parent.id,SnapEdge.BOTTOM))
            val before=model.layout();val bytes=parent.file.readBytes();val bindings=model.images.associate {it.id to it.attachment}
            model.crop(parent.id,Rect(0,0,24,12))
            assertEquals(before[right.id],model.layout()[right.id]);assertNotEquals(before[bottom.id],model.layout()[bottom.id])
            assertEquals(bindings,model.images.associate {it.id to it.attachment});assertArrayEquals(bytes,parent.file.readBytes())
            val cropped=model.layout();model.undo();assertEquals(before,model.layout());model.redo();assertEquals(cropped,model.layout())
        } finally {directory.deleteRecursively()}
    }
}
