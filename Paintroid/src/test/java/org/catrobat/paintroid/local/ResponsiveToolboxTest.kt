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
    private fun click(tag: String) {
        val control=view<View>(tag)
        if(control is android.widget.CompoundButton) {val before=control.isChecked;control.performClick();assertNotEquals(before,control.isChecked)}
        else assertTrue(control.performClick())
        settle()
    }
    private fun bounds(view: View): Rect {
        val pos=IntArray(2);view.getLocationOnScreen(pos)
        return Rect(pos[0],pos[1],pos[0]+view.width,pos[1]+view.height)
    }
    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        context.getSharedPreferences("classic-ui",0).edit().clear().commit()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get();settle()
        activity.document.newImage(160,120);activity.paintCanvas.fit();click("menu_Draw")
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
            if(tool==PaintTool.ZOOM) click("menu_View")
            val item=view<View>("tool_${tool.name}");assertTrue(item.isShown)
            item.requestRectangleOnScreen(Rect(0,0,item.width,item.height),true)
            click("tool_${tool.name}");assertEquals(tool,activity.paintCanvas.tool)
        }
    }
    @Test fun portraitToolsRunAcrossTopAndCategoriesOpenBelowWithoutNarrowingCanvas() {
        val strip=view<LinearLayout>("primary_tools")
        assertEquals(LinearLayout.HORIZONTAL,strip.orientation)
        assertTrue(view<View>("primary_tool_scroll") is HorizontalScrollView)
        open(ToolCategory.BRUSH)
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
        assertTrue(view<View>("primary_tool_scroll") is ScrollView)
        assertNull(root.findViewWithTag<View>("compact_menu"))
        val drawer=view<View>("tool_scroll")
        open(ToolCategory.INSERT);render("tools-landscape-insert.png")
        val rail=bounds(view<View>("primary_tool_scroll"));val panel=bounds(drawer)
        assertEquals(rail.right,panel.left);assertEquals(rail.top,panel.top)
        assertEquals(panel.right,bounds(activity.paintCanvas).left)
        assertTrue(activity.paintCanvas.height>root.height/2)
        val width=activity.paintCanvas.width;val height=activity.paintCanvas.height
        click("category_INSERT")
        assertFalse(drawer.isShown);assertTrue(activity.paintCanvas.width>width)
        assertEquals(height,activity.paintCanvas.height)
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
        EditorTestNavigation.named(activity,"View","Cursor drawing");click("cursor_mode_enabled");settle()
        assertTrue(board.cursorMode);assertEquals(PaintTool.BRUSH,board.tool)
        val category=view<ToolCategoryButton>("category_BRUSH")
        assertTrue(category.expanded);assertTrue(category.isSelected);assertEquals(PaintTool.BRUSH,category.selectedTool)
        assertTrue(view<View>("panel_View_commands").isShown)
        assertTrue(view<View>("cursor_draw_toggle").isShown)
        assertFalse(board.cursorDrawing)
        click("menu_Draw")
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
    private fun checkHeader() {
        val header=bounds(view<View>("header_bar"))
        val title=bounds(view<View>("document_title"))
        val subtitle=view<android.widget.TextView>("document_subtitle")
        assertEquals("AN Paint",subtitle.text.toString())
        assertTrue(bounds(subtitle).top>=title.bottom)
        assertTrue(title.width()>0);assertTrue(header.contains(title));assertTrue(header.contains(bounds(subtitle)))
        val quick=bounds(view<View>("quick_actions"))
        assertEquals(header.right,quick.right);assertTrue(title.right<=quick.left)
        for(tag in listOf("undo","redo","clipboard_cut","clipboard_copy","clipboard_paste","save_image")) {
            val action=view<View>(tag)
            assertTrue("$tag stays in the first header row",header.contains(bounds(action)))
            assertTrue(action is ActionButton);assertTrue(bounds(action).width()>=44*activity.resources.displayMetrics.density)
        }
    }
    @Test fun navigationMovesWithItsOptionsAndCursorReadoutUpdatesBesideZoom()=checkNavigationAndRulers("portrait")
    @Test @Config(qualifiers="w320dp-h640dp-port-xhdpi")
    fun narrowPortraitKeepsTheEntireCursorReadoutVisible()=checkNavigationAndRulers("narrow-portrait")
    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi")
    fun landscapeRulersAndColourControlsRetainTheSideRibbon()=checkNavigationAndRulers("landscape")
    private fun checkNavigationAndRulers(orientation: String) {
        val tabs=view<LinearLayout>("tab_strip")
        assertEquals("menu_View",tabs.getChildAt(0).tag);assertEquals("menu_Draw",tabs.getChildAt(1).tag)
        assertNull(view<View>("primary_tools").findViewWithTag<View>("tool_ZOOM"))
        click("menu_View")
        assertSame(view("tool_ZOOM"),view<android.view.ViewGroup>("panel_View_commands").getChildAt(0))
        click("tool_ZOOM")
        assertTrue(view<View>("navigation_options").isShown);assertTrue(view<View>("zoom_actual").isShown)
        assertFalse(view<View>("sidebar").isShown)
        click("navigate_draw");assertTrue(view<View>("sidebar").isShown);assertFalse(view<View>("navigation_options").isShown)
        assertEquals(PaintTool.PENCIL,activity.paintCanvas.tool)
        EditorTestNavigation.command(activity,"View",1)
        assertTrue(activity.paintCanvas.grid)
        activity.paintCanvas.zoomAt(16f)
        EditorTestNavigation.command(activity,"View",2);click("cursor_mode_enabled")
        val board=activity.paintCanvas
        val start=board.draftState()
        for((action,offset) in listOf(MotionEvent.ACTION_DOWN to 0f,MotionEvent.ACTION_MOVE to 32f)) {
            val event=MotionEvent.obtain(0,20,action,board.width/2f+offset,board.height/2f+offset,0)
            board.dispatchTouchEvent(event);event.recycle()
        }
        val readout=view<android.widget.TextView>("status_text")
        assertTrue(readout.text.contains(board.zoomLabel()+" · x:"))
        assertEquals(start.getDouble("cursor_x")+2,board.draftState().getDouble("cursor_x"),.001)
        render("rulers-cursor-$orientation.png")
        assertEquals(readout.text.length,readout.layout.getLineEnd(readout.layout.lineCount-1))
        assertTrue(readout.layout.height<=readout.height-readout.totalPaddingTop-readout.totalPaddingBottom)
        val cancel=MotionEvent.obtain(0,20,MotionEvent.ACTION_CANCEL,0f,0f,0);board.dispatchTouchEvent(cancel);cancel.recycle()
        click("menu_Color")
        for(i in 0 until 16) assertTrue(view<View>("palette_custom_$i").isShown)
        assertEquals((view<View>("reset_colours").parent as android.view.ViewGroup).indexOfChild(view("reset_colours"))+1,
            (view<View>("advanced_colour").parent as android.view.ViewGroup).indexOfChild(view("advanced_colour")))
        render("palette-slots-$orientation.png")
    }
    @Test fun portraitHeaderKeepsBothTitleLinesAndShortcutsInOneRow() {checkHeader();render("header-portrait.png")}
    @Test @Config(qualifiers="w320dp-h640dp-port-xhdpi")
    fun narrowPortraitKeepsAllSixShortcutsBesideTheTitle() {checkHeader();render("header-narrow-portrait.png")}
    @Test fun allRibbonCaptionsAreCentredAndCommandTilesKeepTheirIcons() {
        fun centred(button: android.widget.Button) {
            assertTrue(button is PanelToolButton)
            val layout=requireNotNull(button.layout)
            for(line in 0 until layout.lineCount) assertEquals("Caption ${button.text}",button.width/2f,button.totalPaddingLeft+(layout.getLineLeft(line)+layout.getLineRight(line))/2f,1f)
            assertNotNull(button.compoundDrawables[1])
        }
        for(tag in listOf("category_BRUSH","category_SELECTION","category_INSERT","tool_ERASER")) centred(view(tag))
        for(tab in listOf("Edit","View")) {
            click("menu_$tab")
            EditorTestNavigation.buttons(view("panel_${tab}_commands")).forEach {
                centred(it)
                assertEquals("Command tiles have the same height as Drawing",view<View>("category_BRUSH").height,it.height)
            }
            assertTrue(view<android.widget.LinearLayout>("panel_${tab}_commands").orientation==android.widget.LinearLayout.HORIZONTAL)
            render("icon-panel-$tab.png")
        }
        click("menu_Color")
        for(tag in listOf("swap_colours","reset_colours","add_colour","advanced_colour")) centred(view(tag))
        render("icon-panel-Color.png")
        click("menu_File")
        assertTrue(EditorTestNavigation.buttons(view("panel_File_commands")).none {it is PanelToolButton})
    }
    @Test fun translatedCommandCaptionsFitInPortrait()=checkTranslatedCommands("portrait")
    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi")
    fun translatedCommandCaptionsFitInLandscape()=checkTranslatedCommands("landscape")
    private fun checkTranslatedCommands(orientation: String) {
        val original=AppLanguage.selectedTag(activity)
        try {
            for(language in listOf("hy","ar","yue-Latn")) {
                AppLanguage.select(activity,language);activity.onConfigurationChanged(activity.resources.configuration);settle()
                for(tab in listOf("Draw","View","Edit")) {
                    click("menu_$tab")
                    val rail=view<View>(if(tab=="Draw") "primary_tools" else "panel_${tab}_commands")
                    EditorTestNavigation.buttons(rail).forEach {button ->
                        val layout=requireNotNull(button.layout)
                        assertEquals("Full caption: $language/$tab/${button.text}",button.text.length,layout.getLineEnd(layout.lineCount-1))
                        assertTrue("Caption fits below the icon: $language/$tab/${button.text}",layout.height<=button.height-button.compoundPaddingTop-button.compoundPaddingBottom)
                    }
                    render("translated-$language-$tab-$orientation.png")
                }
                click("menu_View")
                if(!view<View>("cursor_options").isShown) EditorTestNavigation.command(activity,"View",2)
                assertTrue(view<View>("cursor_settings_panel").isShown);click("cursor_mode_enabled")
                render("translated-$language-cursor-$orientation.png")
                // Avoid resuming cursor ink when changing the interface language.
                activity.paintCanvas.setCursorMode(false)
            }
        } finally {AppLanguage.select(activity,original);AppLanguage.refresh(activity)}
    }

    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi")
    fun landscapeSideTabsRemainVisibleAndFullscreenReturnsTheirSpace() {
        checkHeader()
        var previousBottom=0
        for(name in listOf("View","Draw","File","Edit","Color")) {
            val tab=view<View>("menu_$name");val box=bounds(tab)
            assertTrue(box.top>=previousBottom);previousBottom=box.bottom
            assertTrue(box.right<=bounds(activity.paintCanvas).left)
        }
        EditorTestNavigation.named(activity,"View","Hide editor controls");settle()
        assertFalse(view<View>("vertical_ribbon_rail").isShown)
        assertEquals(root.width,activity.paintCanvas.width)
        click("leave_fullscreen")
        assertTrue(view<View>("vertical_ribbon_rail").isShown)
        assertTrue(activity.paintCanvas.width<root.width);checkHeader()
    }

    private fun render(name: String) {
        settle()
        val image=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
        root.draw(Canvas(image))
        val file=File("build/reports/classic-preview",name);file.parentFile.mkdirs()
        file.outputStream().use {image.compress(Bitmap.CompressFormat.PNG,100,it)};image.recycle()
    }
}
