/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Resources
import android.graphics.Rect
import android.os.Looper
import android.view.View
import android.view.ViewGroup
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
import org.robolectric.RuntimeEnvironment
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale

/** One conditional companion correction; actual count, apply/undo and attachment consumers. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class IndonesianCropFollowthroughTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private fun expected(tag: String,key: String)=PriorityWordingExpectations.resourceText(tag,key)
    private fun formatted(tag: String,key: String,vararg args: Any)=String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    @Before fun remember() {
        previousResources=PaintApplication.currentResources;previousLocale=Locale.getDefault()
        previousTag=AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }
    @After fun restore() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }
    private fun inLocale(tag: String,run: (Activity)->Unit) {
        val controller=Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity=controller.setup().get()
        try {
            AppLanguage.select(activity,tag);AppLanguage.refresh(activity);Locale.setDefault(Locale.US)
            assertEquals(tag,AppLanguage.selectedTag(activity));run(activity)
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss();idle()
            controller.pause().stop().destroy()
        }
    }
    private fun texts(view: View): List<String> = when(view) {
        is ViewGroup -> (0 until view.childCount).flatMap { texts(view.getChildAt(it)) }
        is TextView -> listOf(view.text.toString())
        else -> emptyList()
    }

    @Test fun actualCropDialogSelectsCountsRejectsEmptyAndAppliesUndoableCrop()=inLocale("id") { activity ->
        val directory=File(activity.cacheDir,"indonesian-crop-dialog").apply {mkdirs()}
        val assembly=ImageAssembly(directory)
        val images=listOf("parent","child").map { id ->
            AssemblyImage(id,File(directory,"$id.image").apply {writeBytes(byteArrayOf(1,2,3))},id,null,ImageDimensions(24,16))
        }
        assembly.add(images);assembly.place("parent",Attachment(null,null));assembly.place("child",Attachment("parent",SnapEdge.RIGHT))
        val before=assembly.layout();val originalCrops=assembly.images.map {Rect(it.crop)}
        var applications=0
        val dialog=ImageCropDialog(activity,assembly.images,{null}) {crops -> assembly.crop(crops);applications++}.show()
        try {
            idle();val root=dialog.window!!.decorView;val status=root.findViewWithTag<TextView>("crop_status")
            fun check(count: Int,width: Int=24) {
                assertEquals(activity.resources.getQuantityString(R.plurals.ui_crop_preview_images,count,width,16,count),status.text.toString())
            }
            check(2);root.findViewWithTag<CheckBox>("crop_include_child").performClick();idle();check(1)
            root.findViewWithTag<View>("crop_none").performClick();dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
            assertEquals(0,applications);assertTrue(dialog.isShowing)
            assertEquals(expected("id","ui_choose_at_least_one_image"),status.text.toString())
            root.findViewWithTag<CheckBox>("crop_include_parent").performClick();idle();check(1)
            root.findViewWithTag<android.widget.EditText>("crop_right").setText("12");idle();check(1,12)
            assertEquals(before,assembly.layout());assertEquals(originalCrops,assembly.images.map {it.crop})
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
            assertEquals(1,applications);assertFalse(dialog.isShowing)
            assertEquals(Rect(0,0,12,16),assembly.image("parent").crop)
            assertEquals(Rect(0,0,24,16),assembly.image("child").crop)
            assertEquals(12,assembly.layout().getValue("child").left)
            assertEquals(Attachment("parent",SnapEdge.RIGHT),assembly.image("child").attachment)
            assembly.undo();assertEquals(before,assembly.layout());assertEquals(originalCrops,assembly.images.map {it.crop})
            images.forEach {assertArrayEquals(byteArrayOf(1,2,3),it.file.readBytes())}
        } finally {dialog.dismiss();idle();directory.deleteRecursively()}
    }

}
