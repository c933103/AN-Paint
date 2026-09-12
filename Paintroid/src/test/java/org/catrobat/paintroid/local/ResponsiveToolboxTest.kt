/* AN Paint responsive tool controls, GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Rect
import android.os.Looper
import android.view.MotionEvent
import android.view.View
import android.widget.EditText
import android.widget.HorizontalScrollView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.SeekBar
import org.catrobat.paintroid.classic.*
import org.junit.*
import org.junit.Assert.*
import org.junit.runner.RunWith
import org.robolectric.*
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowPopupMenu
import java.io.File
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ResponsiveToolboxTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private val root get()=activity.window.decorView
    private fun <T: View> view(tag: String): T=root.findViewWithTag(tag)
    private fun settle()=shadowOf(Looper.getMainLooper()).idleFor(50,TimeUnit.MILLISECONDS)
    private fun click(tag: String) {assertTrue(view<View>(tag).performClick());settle()}
    private fun bounds(view: View): Rect {
        val pos=IntArray(2);view.getLocationOnScreen(pos)
        return Rect(pos[0],pos[1],pos[0]+view.width,pos[1]+view.height)
    }
    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        context.getSharedPreferences("classic-ui",0).edit().clear().commit()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get();settle()
        activity.document.newImage(160,120);activity.paintCanvas.fit()
    }
    @After fun stop() {
        controller.pause().stop()
        val end=System.nanoTime()+15_000_000_000L
        while(activity.busy && System.nanoTime()<end) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
        assertFalse(activity.busy);controller.destroy()
    }
    private fun open(category: ToolCategory) {
        val button=view<ToolCategoryButton>("category_${category.name}")
        if(!button.expanded) click("category_${category.name}")
        assertTrue(button.expanded)
    }
    private fun assertEveryToolReachable() {
        for(category in ToolCategory.values()) {
            open(category)
            for(tool in category.tools) {
                val item=view<View>("tool_${tool.name}")
                assertTrue("Expanded ${category.name} contains $tool",item.isShown)
                item.requestRectangleOnScreen(Rect(0,0,item.width,item.height),true)
                click("tool_${tool.name}")
                assertEquals(tool,activity.paintCanvas.tool)
                assertTrue(item.isSelected)
                assertTrue(view<ToolCategoryButton>("category_${category.name}").isSelected)
                assertEquals(tool,view<ToolCategoryButton>("category_${category.name}").selectedTool)
            }
        }
        for(tool in listOf(PaintTool.ERASER,PaintTool.FILL,PaintTool.PICKER,PaintTool.ZOOM)) {
            val item=view<View>("tool_${tool.name}");assertTrue(item.isShown)
            item.requestRectangleOnScreen(Rect(0,0,item.width,item.height),true)
            click("tool_${tool.name}");assertEquals(tool,activity.paintCanvas.tool)
        }
    }
    @Test fun portraitToolsRunAcrossTopAndCategoriesOpenBelowWithoutNarrowingCanvas() {
        val strip=view<LinearLayout>("primary_tools")
        assertEquals(LinearLayout.HORIZONTAL,strip.orientation)
        assertTrue(view<View>("primary_tool_scroll") is HorizontalScrollView)
        val rail=view<View>("primary_tool_scroll");val drawer=view<ScrollView>("tool_scroll")
        assertEquals(bounds(rail).bottom,bounds(drawer).top)
        assertEquals(bounds(view<View>("sidebar")).bottom,bounds(activity.paintCanvas).top)
        assertEquals(root.width,activity.paintCanvas.width)
        assertTrue(activity.paintCanvas.height>drawer.height)
        render("tools-portrait-brush.png")
        val before=activity.paintCanvas.height
        click("category_BRUSH");assertFalse(drawer.isShown)
        assertTrue(activity.paintCanvas.height>before)
        assertTrue(view<ToolCategoryButton>("category_BRUSH").contentDescription.contains("Expand"))
        open(ToolCategory.INSERT);render("tools-portrait-insert.png")
        assertEveryToolReachable()
    }
    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi")
    fun landscapeCategoriesOpenToTheRightAndCollapseReleasesCanvasWidth() {
        val strip=view<LinearLayout>("primary_tools");assertEquals(LinearLayout.VERTICAL,strip.orientation)
        val sidebar=view<View>("sidebar");val drawer=view<View>("tool_scroll")
        assertEquals(bounds(sidebar).right,bounds(drawer).left)
        assertEquals(bounds(drawer).right,bounds(activity.paintCanvas).left)
        assertEquals(bounds(drawer).top,bounds(activity.paintCanvas).top)
        open(ToolCategory.INSERT);render("tools-landscape-insert.png")
        val width=activity.paintCanvas.width;click("category_INSERT")
        assertFalse(drawer.isShown);assertTrue(activity.paintCanvas.width>width)
        assertEquals(bounds(sidebar).right,bounds(activity.paintCanvas).left)
        render("tools-landscape-collapsed.png")
        assertEveryToolReachable()
    }
    @Test fun categoriesRememberTheirToolAcrossSwitchingAndOrientationChange() {
        click("tool_WATERCOLOR");open(ToolCategory.SELECTION);click("tool_LASSO")
        open(ToolCategory.BRUSH);assertEquals(PaintTool.WATERCOLOR,activity.paintCanvas.tool)
        open(ToolCategory.SELECTION);assertEquals(PaintTool.LASSO,activity.paintCanvas.tool)
        click("category_SELECTION");assertFalse(view<View>("tool_scroll").isShown)
        val config=Configuration(activity.resources.configuration).apply {orientation=Configuration.ORIENTATION_LANDSCAPE}
        activity.resources.updateConfiguration(config,activity.resources.displayMetrics);activity.onConfigurationChanged(config);settle()
        assertFalse(view<View>("tool_scroll").isShown)
        open(ToolCategory.SELECTION);assertEquals(PaintTool.LASSO,activity.paintCanvas.tool)
        open(ToolCategory.BRUSH);assertEquals(PaintTool.WATERCOLOR,activity.paintCanvas.tool)
    }
    @Test fun reopeningOptionsPreservesPendingPolygonAndCursorSwitchShowsBrushCategory() {
        open(ToolCategory.INSERT);click("tool_POLYGON")
        val board=activity.paintCanvas
        for((index,point) in listOf(30f to 30f,120f to 30f,120f to 90f).withIndex()) {
            val p=board.toScreen(point.first,point.second)
            val time=1000L+index*500L
            for(action in listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP)) {
                val event=MotionEvent.obtain(time,time,action,p.x,p.y,0)
                assertTrue(board.dispatchTouchEvent(event));event.recycle()
            }
        }
        settle();assertTrue(board.hasPendingEdit);assertFalse(activity.document.canUndo)
        val vertices=board.draftState().getJSONArray("polygon").toString()
        click("category_INSERT");assertFalse(view<View>("tool_scroll").isShown)
        click("category_INSERT");assertTrue(view<View>("tool_scroll").isShown)
        assertTrue(board.hasPendingEdit);assertFalse(activity.document.canUndo)
        assertEquals(vertices,board.draftState().getJSONArray("polygon").toString())
        click("menu_View")
        val menu=ShadowPopupMenu.getLatestPopupMenu().menu
        val cursor=(0 until menu.size()).map {menu.getItem(it)}.single {it.title.toString()==activity.getString(org.catrobat.paintroid.R.string.ui_enable_cursor_drawing)}
        assertTrue(menu.performIdentifierAction(cursor.itemId,0));settle()
        assertTrue(board.cursorMode);assertEquals(PaintTool.BRUSH,board.tool)
        val category=view<ToolCategoryButton>("category_BRUSH")
        assertTrue(category.expanded);assertTrue(category.isSelected);assertEquals(PaintTool.BRUSH,category.selectedTool)
        assertTrue(view<View>("category_tools_BRUSH").isShown)
        assertFalse(view<View>("category_tools_INSERT").isShown)
    }

    @Test fun pencilNumericWidthAcceptsOneHundredAndRemainsIndependentOfBrush() {
        click("tool_PENCIL");assertEquals(1f,activity.paintCanvas.pencilSize,0f)
        val slider=view<SeekBar>("pencil_size");assertEquals(99,slider.max)
        click("pencil_size_value")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val input=dialog.window!!.decorView.findViewWithTag<EditText>("numeric_input")
        input.setText("101");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();settle()
        assertTrue(dialog.isShowing);assertNotNull(input.error)
        input.setText("100");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();settle()
        assertFalse(dialog.isShowing);assertEquals(100f,activity.paintCanvas.pencilSize,0f)
        click("tool_BRUSH");view<SeekBar>("brush_size").progress=11
        click("tool_PENCIL");assertEquals(100f,activity.paintCanvas.pencilSize,0f)
        assertEquals(99,view<SeekBar>("pencil_size").progress)
    }
    private fun render(name: String) {
        settle()
        val image=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
        root.draw(Canvas(image))
        val file=File("build/reports/classic-preview",name);file.parentFile.mkdirs()
        file.outputStream().use {image.compress(Bitmap.CompressFormat.PNG,100,it)};image.recycle()
    }
}
