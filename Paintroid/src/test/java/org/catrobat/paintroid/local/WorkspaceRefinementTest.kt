/* AN Paint regression checks, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.content.*
import android.content.res.Configuration
import android.graphics.*
import android.os.Looper
import android.view.*
import android.widget.*
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.*
import org.junit.Assert.*
import org.junit.runner.RunWith
import org.robolectric.*
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.*
import org.robolectric.shadows.*
import java.io.File
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class WorkspaceRefinementTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private val doc get()=activity.document
    private val canvas get()=activity.paintCanvas
    private fun root()=activity.window.decorView
    private fun <T: View> view(tag: String): T = root().findViewWithTag(tag)
    private fun settle() { shadowOf(Looper.getMainLooper()).idleFor(50,TimeUnit.MILLISECONDS) }
    private fun click(tag: String) { EditorTestNavigation.click(activity,tag) }
    private fun screenBounds(view: View): Rect {
        val position=IntArray(2);view.getLocationOnScreen(position)
        return Rect(position[0],position[1],position[0]+view.width,position[1]+view.height)
    }
    private fun assertPaletteBesideIndicator() {
        val indicator=screenBounds(view<View>("colour_status"));val palette=screenBounds(view<View>("palette_bar"))
        assertEquals("Palette must start at the indicator's right edge",indicator.right,palette.left)
        assertEquals("Palette and indicator must share a top edge",indicator.top,palette.top)
        assertEquals("Palette and indicator must share a bottom edge",indicator.bottom,palette.bottom)
        assertEquals("Canvas must end above the palette",screenBounds(canvas).bottom,palette.top)
    }
    private fun waitIo() {
        val end=System.nanoTime()+15_000_000_000L
        do { shadowOf(Looper.getMainLooper()).idle();if (activity.busy) Thread.sleep(10) } while (activity.busy && System.nanoTime()<end)
        assertFalse("Operation did not finish",activity.busy)
    }
    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        listOf("classic-recovery.png","classic-autosave.zip","classic-autosave.zip.bak").forEach { File(context.filesDir,it).deleteRecursively() }
        AutosaveStore(context.filesDir).recoveryCopies().forEach { it.delete() }
        listOf("classic-ui","classic-custom-colours").forEach { context.getSharedPreferences(it,Context.MODE_PRIVATE).edit().clear().commit() }
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get()
        doc.newImage(200,120);canvas.fit();settle()
    }
    @After fun stop() { controller.pause().stop();waitIo();controller.destroy() }
    private fun saveIdle() { shadowOf(Looper.getMainLooper()).idleFor(2,TimeUnit.SECONDS);waitIo();assertTrue(AutosaveStore(activity.filesDir).file.isFile);assertNull(activity.lastAutosaveError) }
    private fun reopen() {
        controller.pause().stop();waitIo();controller.destroy()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get();settle()
    }
    private fun single(action: Int,x: Float,y: Float) {
        val event=MotionEvent.obtain(0,10,action,x,y,0);assertTrue(canvas.dispatchTouchEvent(event));event.recycle()
    }
    private fun tapImage(x: Float,y: Float) { val p=canvas.toScreen(x,y);single(MotionEvent.ACTION_DOWN,p.x,p.y);single(MotionEvent.ACTION_UP,p.x,p.y);settle() }
    private fun two(action: Int,x1: Float,y1: Float,x2: Float,y2: Float) {
        val props=Array(2) { i -> MotionEvent.PointerProperties().apply { id=i;toolType=MotionEvent.TOOL_TYPE_FINGER } }
        val coords=arrayOf(x1 to y1,x2 to y2).map { (px,py) -> MotionEvent.PointerCoords().apply { x=px;y=py;pressure=1f;size=1f } }.toTypedArray()
        val e=MotionEvent.obtain(0,30,action,2,props,coords,0,0,1f,1f,0,0,android.view.InputDevice.SOURCE_TOUCHSCREEN,0)
        assertTrue(canvas.dispatchTouchEvent(e));e.recycle()
    }
    private fun render(v: View,name: String) {
        settle()
        val bitmap=Bitmap.createBitmap(v.width,v.height,Bitmap.Config.ARGB_8888);v.draw(Canvas(bitmap))
        val out=File("build/reports/classic-preview",name);out.parentFile.mkdirs()
        out.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it)) };bitmap.recycle()
    }
    @Test fun autosaveRunsWhileEditingAndRestoresPixelsNameToolAndSettings() {
        doc.foreground=Color.MAGENTA;doc.background=Color.YELLOW;doc.strokeWidth=9f;doc.tolerance=13f
        click("tool_BRUSH");tapImage(40f,30f)
        canvas.zoomAt(2f);val viewport=Triple(canvas.zoom,canvas.draftState().getDouble("centre_x"),canvas.draftState().getDouble("centre_y"))
        val pixels=doc.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        saveIdle();assertTrue(doc.dirty);assertTrue(view<TextView>("document_title").text.endsWith("*"))
        val store=AutosaveStore(activity.filesDir)
        val draft=store.read { w,h -> assertEquals(200,w);assertEquals(120,h) }
        assertTrue(pixels.sameAs(draft.image));assertEquals("Untitled",draft.metadata.getString("filename"));draft.image.recycle()
        reopen();assertTrue(pixels.sameAs(doc.bitmap));pixels.recycle()
        assertEquals(PaintTool.BRUSH,canvas.tool);assertEquals(Color.MAGENTA,doc.foreground);assertEquals(Color.YELLOW,doc.background)
        assertEquals(9f,doc.strokeWidth,0f);assertEquals(13f,doc.tolerance,0f);assertTrue(doc.dirty)
        assertEquals(viewport.first,canvas.zoom,.001f);assertEquals(viewport.second,canvas.draftState().getDouble("centre_x"),.001);assertEquals(viewport.third,canvas.draftState().getDouble("centre_y"),.001)
    }
    @Test fun autosaveDoesNotCommitUnfinishedPolygonAndRestoresItsGeometry() {
        click("tool_POLYGON");doc.shapeStyle=1
        tapImage(10f,10f);tapImage(90f,10f);tapImage(40f,80f)
        val pending=canvas.draftState().getJSONArray("polygon").toString()
        saveIdle();assertTrue(canvas.hasPendingEdit);assertFalse(doc.canUndo);assertEquals(Color.WHITE,doc.bitmap.getPixel(40,30))
        reopen();assertTrue(canvas.hasPendingEdit);assertEquals(pending,canvas.draftState().getJSONArray("polygon").toString())
        click("apply");assertEquals(Color.BLACK,doc.bitmap.getPixel(40,30));assertTrue(doc.canUndo)
    }
    @Test fun autosaveRetainsFloatingSelectionAndCanResumeMovement() {
        Canvas(doc.bitmap).drawRect(10f,10f,30f,30f,Paint().apply { color=Color.BLUE });doc.edited()
        click("tool_SELECT");doc.select(RectF(10f,10f,30f,30f));doc.startMovingSelection();doc.selection!!.rect.offset(40f,30f)
        saveIdle();assertTrue(doc.selection!!.floating);assertEquals(Color.WHITE,doc.bitmap.getPixel(15,15))
        reopen();assertNotNull(doc.selection);assertTrue(doc.selection!!.floating);assertEquals(RectF(50f,40f,70f,60f),doc.selection!!.rect)
        doc.selection!!.rect.offset(5f,0f);click("apply")
        assertEquals(Color.BLUE,doc.bitmap.getPixel(60,45));assertEquals(Color.WHITE,doc.bitmap.getPixel(15,15))
    }
    @Test fun changingOnlyMagnifierScaleAutosavesWithoutLeavingOrEditing() {
        // Finish the startup save first so it cannot hide a missing settings callback.
        saveIdle()
        EditorTestNavigation.command(activity,"View",3);settle()
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val control=dialog.window!!.decorView.findViewWithTag<NumericSlider>("preview_magnification")
        control.slider.progress=225 // 100% minimum + 225 = 325%.
        assertEquals(3.25f,canvas.previewMagnification,0f)
        saveIdle()
        val draft=AutosaveStore(activity.filesDir).read { _,_ -> }
        try {
            assertEquals(3.25,draft.metadata.getJSONObject("canvas").getDouble("preview_magnification"),0.0)
            assertFalse(doc.dirty);assertFalse(doc.canUndo)
        } finally {draft.image.recycle();draft.floating?.recycle()}
        dialog.dismiss()
    }
    @Test fun autosavePreservesUnappliedExpandedBoundsAcrossRestart() {
        click("trim_canvas");canvas.trim!!.set(Rect(-10,-20,230,140));canvas.onStatus()
        saveIdle();assertEquals(200,doc.bitmap.width)
        reopen();assertEquals(Rect(-10,-20,230,140),canvas.trim!!.rect);assertNotNull(view<View>("trim_apply"))
        click("trim_apply");assertEquals(240,doc.bitmap.width);assertEquals(160,doc.bitmap.height)
    }
    @Test fun failedAtomicWriteRetainsThePreviousCompletePixelsAndMetadata() {
        val store=AutosaveStore(File(activity.cacheDir,"atomic-draft-test").apply { mkdirs() })
        val first=Bitmap.createBitmap(4,3,Bitmap.Config.ARGB_8888).apply { eraseColor(Color.RED) }
        store.write(first,null,JSONObject().put("version",1).put("filename","first.png"))
        val bytes=store.file.readBytes()
        val broken=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply { recycle() }
        try { store.write(broken,null,JSONObject().put("version",1).put("filename","bad.png"));fail() } catch (_: Exception) { }
        assertArrayEquals(bytes,store.file.readBytes())
        val recovered=store.read { _,_ -> }
        assertTrue(first.sameAs(recovered.image));assertEquals("first.png",recovered.metadata.getString("filename"))
        first.recycle();recovered.image.recycle()
        var checked=false
        try { store.read { _,_ -> checked=true;throw ImageSizeException("Memory budget exceeded") };fail() } catch (_: ImageSizeException) { }
        assertTrue(checked);assertArrayEquals(bytes,store.file.readBytes())
    }
    @Test fun autosaveExcludesUnconfirmedColorPreviewAndUseColorUpdatesIt() {
        saveIdle();val original=doc.foreground
        click("foreground_colour");val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val body=dialog.window!!.decorView
        body.findViewWithTag<View>("colour_advanced_tab").performClick();settle()
        body.findViewWithTag<EditText>("colour_hex").setText("#123456")
        assertEquals(0xff123456.toInt(),doc.foreground)
        canvas.onStatus();saveIdle()
        var draft=AutosaveStore(activity.filesDir).read {_,_->}
        try {assertEquals(original,draft.metadata.getInt("foreground"))} finally {draft.image.recycle();draft.floating?.recycle()}
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();settle();saveIdle()
        draft=AutosaveStore(activity.filesDir).read {_,_->}
        try {assertEquals(0xff123456.toInt(),draft.metadata.getInt("foreground"))} finally {draft.image.recycle();draft.floating?.recycle()}
    }
    @Test fun leavingDuringBackgroundEditStillSavesItsFinishedPixels() {
        doc.foreground=Color.GREEN;canvas.onFill(20,20)
        controller.pause().stop();waitIo()
        val draft=AutosaveStore(activity.filesDir).read { _,_ -> }
        assertEquals(Color.GREEN,draft.image.getPixel(20,20));draft.image.recycle()
        controller.start().resume().visible()
    }
    @Test fun unreadableDraftIsPreservedAndExportableBeforeNewAutosaves() {
        controller.pause().stop();waitIo();controller.destroy()
        val store=AutosaveStore(activity.filesDir)
        val pixels=Bitmap.createBitmap(4,3,Bitmap.Config.ARGB_8888).apply { eraseColor(Color.MAGENTA) }
        // A valid image with unsupported metadata must still be kept for recovery.
        store.write(pixels,null,JSONObject().put("version",99));pixels.recycle()
        val original=store.file.readBytes()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get();settle()
        assertEquals(1,store.recoveryCopies().size);assertArrayEquals(original,store.recoveryCopies().single().readBytes())
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        doc.newImage(20,10);saveIdle()
        assertArrayEquals(original,store.recoveryCopies().single().readBytes())
        EditorTestNavigation.named(activity,"File","Export recovery copy…")
        val intent=shadowOf(activity).nextStartedActivityForResult
        assertEquals(ClassicPaintActivity.EXPORT_RECOVERY,intent.requestCode);assertEquals(Intent.ACTION_CREATE_DOCUMENT,intent.intent.action)
        val out=File(activity.cacheDir,"recovered-export.zip")
        activity.onActivityResult(ClassicPaintActivity.EXPORT_RECOVERY,android.app.Activity.RESULT_OK,Intent().setData(android.net.Uri.fromFile(out)))
        waitIo();assertArrayEquals(original,out.readBytes());assertTrue(store.recoveryCopies().single().isFile)
    }
    @Test fun pinchAndTwoFingerPanLeaveNoMarkAndKeepExistingRedo() {
        click("tool_PENCIL");tapImage(20f,20f);val painted=doc.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        doc.undo();assertTrue(doc.canRedo);assertFalse(doc.canUndo);assertFalse(painted.sameAs(doc.bitmap))
        val before=doc.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        canvas.zoomAt(2f);val z=canvas.zoom;val x=canvas.panX;val y=canvas.panY
        val centre=canvas.toScreen(80f,50f)
        single(MotionEvent.ACTION_DOWN,centre.x-40,centre.y)
        two(MotionEvent.ACTION_POINTER_DOWN or (1 shl MotionEvent.ACTION_POINTER_INDEX_SHIFT),centre.x-40,centre.y,centre.x+40,centre.y)
        two(MotionEvent.ACTION_MOVE,centre.x-20,centre.y+30,centre.x+100,centre.y+30)
        two(MotionEvent.ACTION_POINTER_UP or (1 shl MotionEvent.ACTION_POINTER_INDEX_SHIFT),centre.x-20,centre.y+30,centre.x+100,centre.y+30)
        single(MotionEvent.ACTION_UP,centre.x-20,centre.y+30)
        assertEquals(z*1.5f,canvas.zoom,.001f);assertTrue(canvas.panX!=x || canvas.panY!=y)
        assertTrue(before.sameAs(doc.bitmap));before.recycle();assertTrue(doc.canRedo);assertFalse(doc.canUndo)
        doc.redo();assertTrue(painted.sameAs(doc.bitmap));painted.recycle()
    }
    @Test fun navigateToolPansWithOneFingerAndSwitchesBackToDrawing() {
        click("tool_BRUSH");click("tool_ZOOM");assertEquals("Navigate",canvas.tool.label)
        canvas.zoomAt(8f);val z=canvas.zoom;val x=canvas.panX
        val p=canvas.toScreen(80f,50f)
        single(MotionEvent.ACTION_DOWN,p.x,p.y);single(MotionEvent.ACTION_MOVE,p.x+25,p.y+20);single(MotionEvent.ACTION_UP,p.x+25,p.y+20)
        assertEquals(x+25,canvas.panX,.001f);assertEquals(z,canvas.zoom,0f);assertFalse(doc.canUndo)
        tapImage(80f,50f);assertEquals(z,canvas.zoom,0f)
        click("navigate_draw");assertEquals(PaintTool.BRUSH,canvas.tool)
    }
    @Test fun twoFingerNavigationCancelsSelectionMovementAndPreservesPendingCurve() {
        Canvas(doc.bitmap).drawRect(20f,20f,50f,50f,Paint().apply { color=Color.BLUE })
        click("tool_SELECT");doc.select(RectF(20f,20f,50f,50f));val original=doc.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        val p=canvas.toScreen(30f,30f)
        single(MotionEvent.ACTION_DOWN,p.x,p.y);single(MotionEvent.ACTION_MOVE,p.x+30,p.y+20)
        assertTrue(doc.selection!!.floating)
        two(MotionEvent.ACTION_POINTER_DOWN or (1 shl MotionEvent.ACTION_POINTER_INDEX_SHIFT),p.x+30,p.y+20,p.x+100,p.y+20)
        single(MotionEvent.ACTION_UP,p.x+30,p.y+20)
        assertTrue(original.sameAs(doc.bitmap));original.recycle();assertFalse(doc.canUndo)
        assertFalse(doc.selection!!.floating);assertEquals(RectF(20f,20f,50f,50f),doc.selection!!.rect)
        click("tool_CURVE")
        val a=canvas.toScreen(20f,20f);val b=canvas.toScreen(80f,70f)
        single(MotionEvent.ACTION_DOWN,a.x,a.y);single(MotionEvent.ACTION_UP,b.x,b.y)
        val curve=canvas.draftState().getJSONArray("curve_points").toString()
        single(MotionEvent.ACTION_DOWN,p.x,p.y)
        two(MotionEvent.ACTION_POINTER_DOWN or (1 shl MotionEvent.ACTION_POINTER_INDEX_SHIFT),p.x,p.y,p.x+100,p.y)
        single(MotionEvent.ACTION_UP,p.x,p.y)
        assertEquals(curve,canvas.draftState().getJSONArray("curve_points").toString());assertTrue(canvas.hasPendingEdit)
    }
    @Test fun colourArrowStartsExpandedStaysPinnedAndRemembersCollapse() {
        assertFalse(view<View>("palette_bar").isShown)
        click("menu_Color");settle()
        val indicator=view<ColourStatusButton>("colour_status")
        assertTrue(indicator.isShown);assertTrue(view<View>("palette_bar").isShown)
        click("colour_FF0000");assertEquals(Color.RED,indicator.foreground)
        view<View>("colour_00FF00").performLongClick();assertEquals(Color.GREEN,indicator.backgroundColour)
        render(root(),"palette-expanded.png")
        click("menu_Draw");settle();assertFalse(view<View>("palette_bar").isShown)
        click("menu_Color");settle();assertEquals(Color.RED,indicator.foreground)
        assertTrue(view<View>("swap_colours").isShown);assertTrue(view<View>("reset_colours").isShown)
    }
    @Test fun wholeSidebarCollapsesBelowToolbarAndSurvivesRotation() {
        click("menu_Draw");settle()
        val toggle=view<View>("sidebar_toggle");val toolbar=view<View>("menu_bar")
        assertTrue(view<View>("sidebar").isShown);assertTrue(toggle.isSelected)
        val arrowPosition=IntArray(2);val toolbarPosition=IntArray(2)
        toggle.getLocationOnScreen(arrowPosition);toolbar.getLocationOnScreen(toolbarPosition)
        assertEquals(toolbarPosition[1],arrowPosition[1])
        val height=canvas.height;click("sidebar_toggle");settle();assertFalse(toggle.isSelected)
        assertFalse(view<View>("sidebar").isShown);assertTrue(canvas.height>height)
        assertTrue(toggle.isShown)
        render(root(),"sidebar-collapsed.png")
        val configuration=Configuration(activity.resources.configuration).apply {orientation=Configuration.ORIENTATION_LANDSCAPE}
        activity.resources.updateConfiguration(configuration,activity.resources.displayMetrics);activity.onConfigurationChanged(configuration);settle()
        assertFalse(view<View>("sidebar").isShown);assertNull(root().findViewWithTag<View>("compact_menu"))
        click("sidebar_toggle");settle();assertTrue(view<View>("sidebar").isShown)
        assertTrue(view<View>("sidebar_toggle").isSelected)
        click("menu_Color");settle();assertTrue(view<View>("palette_bar").isShown)
    }
    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi") fun landscapeHasOneHeaderAndSideTabsWithEveryPanel() {
        assertNotNull(root().findViewWithTag<View>("menu_bar"));assertNull(root().findViewWithTag<View>("compact_menu"))
        assertEquals("Untitled",view<TextView>("document_title").text.toString())
        for(tab in listOf("View","Draw","File","Edit","Color")) {
            click("menu_$tab");settle();assertTrue(view<View>("menu_$tab").isShown)
            val tabs=screenBounds(view<View>("tabs_row"));val panel=screenBounds(view<View>("tab_panel_host"))
            assertEquals(tabs.right,panel.left);assertEquals(tabs.top,panel.top)
            assertEquals(panel.right,screenBounds(canvas).left)
            assertTrue(canvas.height>root().height/2);assertTrue(canvas.width>root().width/3)
            render(root(),"tabs-landscape-$tab.png")
        }
        click("tool_ZOOM");click("zoom_actual");assertEquals(1f,canvas.zoom,0f)
        canvas.fit()
    }
    @Test @Config(qualifiers="w900dp-h360dp-land-xhdpi") fun licenceActionsStayVisibleWhileLongTextScrollsAndCopyEverything() {
        val text="Complete terms\n"+(1..1000).joinToString("\n") { "Clause $it: exact licence text." }
        val dialog=LegalInfo.termsDialog(activity,"Test terms",text);dialog.show();settle()
        val root=dialog.window!!.decorView
        val scroll=root.findViewWithTag<ScrollView>("terms_scroll")
        val actions=root.findViewWithTag<View>("terms_actions");val position=IntArray(2);actions.getLocationOnScreen(position);val top=position[1]
        for (tag in listOf("terms_copy","terms_more","terms_done")) assertTrue(root.findViewWithTag<View>(tag).isShown)
        assertTrue(scroll.height>0);assertTrue(scroll.getChildAt(0).height>scroll.height)
        scroll.fullScroll(View.FOCUS_DOWN);settle();actions.getLocationOnScreen(position);assertEquals(top,position[1])
        root.findViewWithTag<View>("terms_copy").performClick()
        val clipboard=activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        assertEquals(text,clipboard.primaryClip!!.getItemAt(0).text.toString())
        val local=Rect();assertTrue(actions.getGlobalVisibleRect(local));assertEquals(actions.height,local.height())
        render(root,"licence-landscape.png");root.findViewWithTag<View>("terms_done").performClick();assertFalse(dialog.isShowing)
    }
    @Test fun allBundledFontsLoadAndDropdownNamesUseTheirOwnTypeface() {
        val catalog=FontCatalog(activity);assertEquals(11,catalog.fonts.count { it.asset!=null });assertEquals(20,catalog.fonts.size)
        val adapter=catalog.adapter();val parent=LinearLayout(activity)
        val widths=mutableSetOf<Int>()
        for (i in catalog.fonts.indices) {
            val row=adapter.getDropDownView(i,null,parent) as TextView
            assertEquals(catalog.fonts[i].name,row.text.toString());assertSame(catalog.face(i),row.typeface)
            if (catalog.fonts[i].asset!=null) widths.add((Paint().apply { typeface=row.typeface;textSize=50f }.measureText("Sphinx 123")*10).toInt())
        }
        assertTrue("Bundled faces fell back to one font",widths.size>=8)
        val licences=activity.assets.open("legal/FONT_NOTICES.txt").bufferedReader().use { it.readText() }
        catalog.fonts.filter { it.asset!=null }.forEach { assertTrue(licences.contains(it.name)) }
        assertTrue(licences.contains("SIL OPEN FONT LICENSE Version 1.1"))
    }
    @Test fun fontPreviewFormattingAndTextPlacementWorkWithUndo() {
        click("tool_TEXT");tapImage(100f,20f)
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog;val root=dialog.window!!.decorView
        root.findViewWithTag<EditText>("text_content").setText("Paint\nPreview")
        root.findViewWithTag<EditText>("text_size").setText("24")
        root.findViewWithTag<EditText>("text_spacing").setText("150")
        val font=root.findViewWithTag<Spinner>("text_font");val catalog=FontCatalog(activity)
        font.setSelection(catalog.fonts.indexOfFirst { it.id=="lato" });settle()
        listOf("text_bold","text_italic","text_underline","text_strike").forEach { root.findViewWithTag<CheckBox>(it).isChecked=true }
        root.findViewWithTag<Spinner>("text_alignment").setSelection(1);settle()
        val preview=root.findViewWithTag<TextPreview>("text_preview")
        assertEquals(Typeface.BOLD_ITALIC,preview.face.style);assertTrue(preview.underline);assertTrue(preview.strike)
        render(root,"text-options.png")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();assertFalse(dialog.isShowing);assertTrue(doc.canUndo)
        val pixels=IntArray(doc.bitmap.width*doc.bitmap.height);doc.bitmap.getPixels(pixels,0,doc.bitmap.width,0,0,doc.bitmap.width,doc.bitmap.height)
        assertTrue(pixels.count { it!=Color.WHITE }>100);doc.undo();assertEquals(Color.WHITE,doc.bitmap.getPixel(100,30))
    }
    @Test fun customColourDefaultsAreNamedOpaqueAndPreserveUserReplacements() {
        click("foreground_colour")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog;val root=dialog.window!!.decorView
        listOf("Pale Violet" to 0xff5b67ff.toInt(),"Gold" to 0xffffd700.toInt(),"Silver" to 0xffc0c0c0.toInt(),"Copper" to 0xffb87333.toInt()).forEachIndexed { i,(name,colour) ->
            val swatch=root.findViewWithTag<View>("custom_colour_$i");assertTrue(swatch.contentDescription.contains(name));swatch.performClick()
            assertEquals(String.format(java.util.Locale.ROOT,"#%06X",colour and 0xffffff),root.findViewWithTag<EditText>("colour_hex").text.toString())
        }
        assertNull(root.findViewWithTag<View>("colour_a"));assertNull(root.findViewWithTag<View>("colour_alpha_slider"))
        root.findViewWithTag<View>("colour_advanced_tab").performClick();root.findViewWithTag<EditText>("colour_hex").setText("#80808080")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();assertTrue(dialog.isShowing)
        dialog.dismiss()
        activity.getSharedPreferences("classic-custom-colours",Context.MODE_PRIVATE).edit().putInt("colour_0",Color.CYAN).commit()
        click("foreground_colour");val next=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        next.window!!.decorView.findViewWithTag<View>("custom_colour_0").performClick();next.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertEquals(Color.CYAN,doc.foreground)
    }
    @Test fun mainEditorFlattensImportsToBackgroundAndRejectsTranslucentDrawingColours() {
        doc.background=Color.YELLOW
        val image=Bitmap.createBitmap(8,8,Bitmap.Config.ARGB_8888).apply { eraseColor(Color.TRANSPARENT);setPixel(2,3,0x800000ff.toInt()) }
        doc.replace(image)
        assertEquals(Color.YELLOW,doc.bitmap.getPixel(0,0));assertEquals(255,Color.alpha(doc.bitmap.getPixel(2,3)))
        assertTrue(kotlin.math.abs(Color.blue(doc.bitmap.getPixel(2,3))-128)<=1)
        doc.foreground=0x405b67ff;assertEquals(0xff5b67ff.toInt(),doc.foreground)
        doc.background=Color.TRANSPARENT;assertEquals(Color.BLACK,doc.background)
        assertFalse(doc.bitmap.hasAlpha())
    }
}
