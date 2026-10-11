/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.app.Dialog
import android.app.LocaleManager
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Rect
import android.os.Build
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowDialog
import org.robolectric.shadows.ShadowToast
import java.io.File
import java.util.Locale

/** C05 exact labels and real actions, not native-language or physical-device acceptance.
 * Captures explicitly record text-fit failures; behavioral passes never certify those captures. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class HungarianAttributionC05Test {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val expected=mapOf(
        R.string.gallery_copy_credit to "Forrásmegjelölés másolása",
        R.string.gallery_edit_credits to "Forrásmegjelölések szerkesztése",
        R.string.gallery_credit_copied to "Forrásmegjelölés másolva",
        R.string.gallery_credit_saved to "A forrásmegjelölés szövege mentve",
        R.string.ui_image_credits to "Képek forrásmegjelölései",
        R.string.ui_about_credits23 to "Névjegy, licencek és forrásmegjelölések",
        R.string.ui_credits_terms to "Forrásmegjelölések és feltételek",
        R.string.ui_icons_fonts_artwork_credits to "Ikonok, betűtípusok és alkotások forrásmegjelölései",
        R.string.ui_open_source_credits_and_notices to "Nyílt forráskódú összetevők forrásmegjelölései és közleményei",
        R.string.ui_gimp_translations31 to "Fordítások forrásmegjelölései és licencei"
    )
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    private fun texts(view: View): List<TextView> =
        (if(view is TextView) listOf(view) else emptyList()) +
            (if(view is ViewGroup) (0 until view.childCount).flatMap {texts(view.getChildAt(it))} else emptyList())

    private fun withHungarian(check: ()->Unit) {
        val preferences=context.getSharedPreferences("app-language",Context.MODE_PRIVATE)
        val oldPreferences=preferences.all
        val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        val manager=if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java) else null
        val oldPlatform=manager?.applicationLocales
        try {
            AppLanguage.select(context,"hu")
            PaintApplication.currentResources=AppLanguage.wrap(context).resources
            assertEquals("hu",AppLanguage.selectedTag(context))
            check()
        } finally {
            idle()
            oldPlatform?.let {manager?.applicationLocales=it}
            preferences.edit().clear().apply {
                oldPreferences.forEach {(key,value)->when(value) {
                    is String -> putString(key,value)
                    is Boolean -> putBoolean(key,value)
                    else -> error("Unexpected language preference type: $key")
                }}
            }.commit()
            PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)
        }
    }

    @Test fun compiledLabelsAndBothRetainedGuidesUseTheAttributionFamily()=withHungarian {
        val resources=AppLanguage.wrap(context).resources
        expected.forEach {(key,value)->assertEquals(resources.getResourceEntryName(key),value,resources.getString(key))}
        for(key in listOf(R.string.gallery_description,R.string.ui_catrobat_s_own_artwork_uses_cc_by_sa,
            R.string.ui_irasutoya_help34,R.string.ui_openclipart_help34,R.string.ui_the_arrow_on_the_left_directly_below_the)) {
            val text=resources.getString(key)
            assertTrue(text.contains(expected.getValue(R.string.ui_about_credits23)))
            assertTrue(text.contains(expected.getValue(R.string.ui_image_credits)))
            assertFalse(text.lowercase(Locale.forLanguageTag("hu")).contains("jóváírás"))
        }
        for(key in listOf(R.string.ui_help23,R.string.ui_add_up_to_20_images_with_android_s))
            assertTrue(resources.getString(key).contains(expected.getValue(R.string.ui_about_credits23)))
        assertTrue(resources.getString(R.string.gallery_description).contains(expected.getValue(R.string.gallery_copy_credit)))
        assertTrue(resources.getString(R.string.gallery_description).contains(expected.getValue(R.string.gallery_edit_credits)))
    }

    @Test @Config(fontScale=1f)
    fun realEditorCopySaveAndReopenPreserveRawCreditAtNormalText()=editor(1f)

    @Test @Config(fontScale=2f)
    fun realEditorCopySaveAndReopenPreserveRawCreditAtLargeText()=editor(2f)

    private fun editor(scale: Float)=withHungarian {
        assertEquals(scale,Resources.getSystem().configuration.fontScale,0f)
        val original=ImageCredit("https://example.org/c05-fixture.png","Fixture author\nCC BY 4.0\nhttps://example.org/source")
        val launch=Intent(context,MediaGalleryActivity::class.java)
            .putExtra("document_image_credits",ImageCredit.write(listOf(original)).toString())
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,launch).setup().visible().windowFocusChanged(true)
        val activity=controller.get()
        var token: String?=null
        var accepted: String?=null
        try {
            assertEquals(scale,activity.resources.configuration.fontScale,0f)
            val open=activity.window.decorView.findViewWithTag<TextView>("gallery_edit_credits")
            assertEquals(expected.getValue(R.string.gallery_edit_credits),open.text.toString())
            assertTrue(open.performClick());idle()
            val dialog=ShadowAlertDialog.getLatestAlertDialog()
            assertTrue(dialog.isShowing)
            assertTrue(texts(dialog.window!!.decorView).any {it.text.toString()==expected.getValue(R.string.ui_image_credits)})
            val copy=dialog.window!!.decorView.findViewWithTag<TextView>("gallery_credit_copy")
            assertEquals(expected.getValue(R.string.gallery_copy_credit),copy.text.toString())
            val field=dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")
            assertEquals(original.text,field.text.toString())
            val edited="Creator 100% %1\$s\nEdited: cropped\nhttps://example.org/source?x=a&y=b\nCC BY 4.0"
            field.setText(edited)
            capture(dialog,"editor",scale,listOf(copy,
                dialog.window!!.decorView.findViewWithTag<TextView>("gallery_credit_save"),
                dialog.window!!.decorView.findViewWithTag<TextView>("gallery_credit_done")),expected.getValue(R.string.ui_image_credits))
            ShadowToast.reset();assertTrue(copy.performClick());idle()
            val clipboard=activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
            assertEquals(edited,clipboard.primaryClip!!.getItemAt(0).text.toString())
            assertEquals(expected.getValue(R.string.ui_image_credits),clipboard.primaryClip!!.description.label.toString())
            assertEquals(expected.getValue(R.string.gallery_credit_copied),ShadowToast.getTextOfLatestToast())
            assertTrue(dialog.isShowing)
            val saved=edited+"\nFurther unchanged provider text: Jóváírás"
            field.setText(saved)
            ShadowToast.reset();assertTrue(dialog.window!!.decorView.findViewWithTag<View>("gallery_credit_save").performClick());idle()
            assertEquals(expected.getValue(R.string.gallery_credit_saved),ShadowToast.getTextOfLatestToast())
            assertEquals(edited,clipboard.primaryClip!!.getItemAt(0).text.toString())
            assertEquals(saved,field.text.toString())
            assertTrue(dialog.window!!.decorView.findViewWithTag<View>("gallery_credit_done").performClick());idle()
            assertFalse(dialog.isShowing)
            val result=shadowOf(activity).resultIntent!!
            token=result.getStringExtra(CreditEditSession.EXTRA_SESSION)
            val session=CreditEditSession.open(context.filesDir,token!!)
            accepted=session.acceptedSnapshot
            assertEquals(listOf(original.copy(text=saved)),session.credits)
            assertTrue(open.performClick());idle()
            val reopened=ShadowAlertDialog.getLatestAlertDialog()
            assertEquals(saved,reopened.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
            reopened.cancel();idle()
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.takeIf {it.isShowing}?.dismiss()
            controller.pause().stop().destroy();idle()
            token?.let {CreditEditSession.open(context.filesDir,it).discard()}
            accepted?.let {ImageCreditArchive.releaseAccepted(context,it)}
        }
    }

    @Test @Config(fontScale=2f)
    fun realAboutChooserAndThreeNoticeRoutesKeepVerbatimBodiesAtLargeText()=withHungarian {
        assertEquals(2f,Resources.getSystem().configuration.fontScale,0f)
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup().visible().windowFocusChanged(true)
        val activity=controller.get()
        try {
            awaitEditorStartup(activity)
            assertEquals(2f,activity.resources.configuration.fontScale,0f)
            val notices=listOf(
                Triple(R.string.ui_icons_fonts_artwork_credits,R.string.ui_icons_fonts_artwork_credits,"legal/ASSET_CREDITS.txt"),
                Triple(R.string.ui_third_party_notices,R.string.ui_open_source_credits_and_notices,"legal/THIRD_PARTY_NOTICES.txt"),
                Triple(R.string.ui_gimp_translations31,R.string.ui_gimp_translations31,"legal/GIMP_TRANSLATION_NOTICES.txt"))
            for((menuKey,titleKey,asset) in notices) {
                EditorTestNavigation.named(activity,"File",expected.getValue(R.string.ui_about_credits23))
                val chooser=ShadowAlertDialog.getLatestAlertDialog()
                assertTrue(chooser.isShowing)
                capture(chooser,"about-$titleKey",2f,emptyList(),expected.getValue(R.string.ui_about_credits23))
                val adapter=chooser.listView.adapter
                val index=(0 until adapter.count).single {adapter.getItem(it).toString()==activity.getString(menuKey)}
                assertTrue(chooser.listView.performItemClick(null,index,index.toLong()));idle()
                val notice=ShadowDialog.getLatestDialog()
                assertTrue(notice.isShowing)
                val body=notice.window!!.decorView.findViewWithTag<TextView>("terms_text")
                assertEquals(activity.assets.open(asset).bufferedReader().use {it.readText()},body.text.toString())
                assertTrue(texts(notice.window!!.decorView).any {it.text.toString()==expected.getValue(titleKey)})
                capture(notice,"notice-$titleKey",2f,emptyList(),expected.getValue(titleKey))
                assertTrue(notice.window!!.decorView.findViewWithTag<View>("terms_done").performClick());idle()
                assertFalse(notice.isShowing)
            }
        } finally {
            ShadowDialog.getLatestDialog()?.takeIf {it.isShowing}?.dismiss()
            controller.pause().stop().destroy();idle()
        }
    }

    /** Retain actual geometry, including clipping. Do not force child sizes or waive fit failures. */
    private fun capture(dialog: Dialog,phase: String,scale: Float,actions: List<TextView>,title: String) {
        idle()
        val root=dialog.window!!.decorView
        assertTrue(root.width>0 && root.height>0)
        val views=texts(root).filter {it.text.toString()==title}+actions
        assertTrue("The actual title must be present",views.isNotEmpty())
        val rows=JSONArray()
        for(view in views) {
            val layout=requireNotNull(view.layout)
            val visible=Rect();val intersects=view.getLocalVisibleRect(visible)
            val transformed=view.transformationMethod?.getTransformation(view.text,view)?.toString() ?: view.text.toString()
            val fits=layout.getLineEnd(layout.lineCount-1)==transformed.length &&
                (0 until layout.lineCount).all {layout.getEllipsisCount(it)==0 && layout.getLineLeft(it)>=-1 && layout.getLineRight(it)<=layout.width+1} &&
                layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom &&
                intersects && visible.width()==view.width && visible.height()==view.height
            rows.put(JSONObject().put("text",view.text.toString()).put("transformed",transformed)
                .put("width",view.width).put("height",view.height).put("layout_height",layout.height)
                .put("last_character",layout.getLineEnd(layout.lineCount-1)).put("complete_fit",fits))
        }
        val directory=File("build/reports/hungarian-attribution-c05").apply {mkdirs()}
        val name="api${RuntimeEnvironment.getApiLevel()}-font$scale-$phase"
        val image=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
        try {root.draw(Canvas(image));File(directory,"$name.png").outputStream().use {
            assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))
        }} finally {image.recycle()}
        File(directory,"$name.json").writeText(JSONObject()
            .put("evidence_kind","Robolectric NATIVE geometry/capture, not installed-device or linguistic acceptance")
            .put("behavioral_test_is_not_text_fit_acceptance",true)
            .put("text_fit_accepted",(0 until rows.length()).all {rows.getJSONObject(it).getBoolean("complete_fit")})
            .put("font_scale",scale).put("measurements",rows).toString(2)+"\n")
    }
}
