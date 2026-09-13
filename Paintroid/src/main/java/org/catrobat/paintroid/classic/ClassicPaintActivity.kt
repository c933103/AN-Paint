/* AN Paint additions, 2026-09-07; layout updated 2026-09-08. GNU AGPL-3.0-or-later; no warranty.
 * A drawing workspace in the modified Catrobat/Paintroid distribution.
 */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.app.AlertDialog
import android.content.ActivityNotFoundException
import android.content.Intent
import android.graphics.*
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.content.res.Configuration
import android.text.TextUtils
import org.json.JSONObject
import org.json.JSONArray
import android.provider.OpenableColumns
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.widget.*
import java.io.File
import java.io.IOException
import java.util.concurrent.Executors

class ClassicPaintActivity : Activity() {
    override fun attachBaseContext(base: android.content.Context) { super.attachBaseContext(AppLanguage.wrap(base)) }
    companion object {
        const val OPEN_IMAGE = 701
        const val IMPORT_IMAGE = 702
        const val SAVE_IMAGE = 703
        const val EXPORT_SOURCE = 704
        const val ASSEMBLY_IMAGE = 705
        const val EXPORT_RECOVERY = 706
        const val GALLERY_IMAGE = 707
        const val SOURCE_ASSET = "local-source/AN-Paint-source.zip"
    }
    lateinit var document: PaintDocument; private set
    lateinit var paintCanvas: PaintCanvas; private set
    private lateinit var root: LinearLayout
    private lateinit var options: LinearLayout
    private lateinit var titleText: TextView
    private lateinit var statusText: TextView
    private var cursorStatusHeight=0
    private lateinit var undoButton: ActionButton
    private lateinit var redoButton: ActionButton
    private lateinit var zoomSlider: SeekBar
    private var syncingZoom = false
    private val toolButtons = linkedMapOf<PaintTool, ToolButton>()
    private val categoryButtons = linkedMapOf<ToolCategory, ToolCategoryButton>()
    private val categoryGroups = linkedMapOf<ToolCategory, View>()
    private val categoryTools = linkedMapOf<ToolCategory, PaintTool>()
    private var expandedCategory: ToolCategory? = null
    private var toolOptionsExpanded = false
    private var activeTab = "View"
    private lateinit var drawingOptionsHost: LinearLayout
    private lateinit var navigationOptionsHost: LinearLayout
    private lateinit var toolOptionsView: View
    private lateinit var tabPanelHost: FrameLayout
    private val tabPanels = linkedMapOf<String, View>()
    private val tabButtons = linkedMapOf<String, Button>()
    private lateinit var editDetails: LinearLayout
    private lateinit var editCommands: View
    private lateinit var toolDrawer: ScrollView
    private var portraitColours: View? = null
    private var filename = ui(R.string.ui_untitled)
    private var exportOptions=ExportOptions()
    private var savedTarget: SavedTarget? = null
    private var isExporting = false
    private var shareAfterSave=false
    private lateinit var recentColours: RecentColours
    private val recentCells=mutableListOf<View>()
    private val customPaletteCells=mutableListOf<SavedColourCell>()
    private var fullscreen=false
    private var afterSave: (() -> Unit)? = null
    private val worker = Executors.newSingleThreadExecutor()
    @Volatile var busy = false; private set
    private var operationsInFlight = 0
    private var resizeDialog: AlertDialog? = null
    private var importSelection: ImportSelection? = null
    private var pendingImportFile: File? = null
    var lastIoError: String? = null; private set
    private var textSettings=TextSettings()
    private lateinit var sidebar: LinearLayout
    private lateinit var colourStatus: ColourStatusButton
    private lateinit var paletteBar: LinearLayout
    private lateinit var sidebarToggle: ActionButton
    private var sidebarExpanded = true
    private var paletteExpanded = true
    private var drawingTool = PaintTool.PENCIL
    private val landscape get() = resources.configuration.orientation == Configuration.ORIENTATION_LANDSCAPE
    private lateinit var autosave: AutosaveStore
    private val autosaveHandler = Handler(Looper.getMainLooper())
    private var draftGeneration = 0L
    @Volatile private var savedDraftGeneration = -1L
    private var failedDraftGeneration = -1L
    var lastAutosaveError: String? = null; private set
    private var autosaveReady = false
    private var autosaveBlocked = false
    private var recoveryNotice: String? = null
    private var recoveryExport: File? = null
    private var autosaving = false
    private var stopped = false
    private var draftStatus = ui(R.string.ui_draft_not_saved_yet)
    private val saveDraft = Runnable { saveDraftIfReady() }
    private val surface = EditorColours.surface
    private val ink = EditorColours.onSurface

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        AppLanguage.refresh(this);filename=ui(R.string.ui_untitled);textSettings=TextSettings()
        autosave=AutosaveStore(filesDir)
        recentColours=RecentColours(this)
        val prefs=getSharedPreferences("classic-ui",MODE_PRIVATE)
        val firstArrowLayout=!prefs.getBoolean("arrow_layout_initialized",false)
        sidebarExpanded=firstArrowLayout || prefs.getBoolean("sidebar_expanded",true)
        paletteExpanded=firstArrowLayout || prefs.getBoolean("palette_expanded",true)
        prefs.edit().putBoolean("arrow_layout_initialized",true).apply()
        document = PaintDocument(historyDirectory = File(cacheDir,"classic-history"),
            allocationGuard = { w,h -> if (::document.isInitialized) checkImageSize(w,h) })
        var recovered: JSONObject?=null
        var restored=false
        if (autosave.exists()) try {
            val draft=autosave.read { w,h -> checkImageSize(w,h) }
            recovered=draft.metadata
            textSettings=TextSettings.read(recovered.optJSONObject("text_settings"))
            savedTarget=SavedTarget.read(recovered.optJSONObject("save_target"))
            document.background=recovered.optInt("background",Color.WHITE)
            document.replace(draft.image)
            draft.floating?.let { image ->
                val r=recovered!!.getJSONArray("floating_rect")
                document.restoreFloatingSelection(image,RectF(r.getDouble(0).toFloat(),r.getDouble(1).toFloat(),r.getDouble(2).toFloat(),r.getDouble(3).toFloat()),recovered!!.optDouble("floating_rotation",0.0).toFloat(),SelectionOutline.read(recovered!!.optJSONArray("selection_outline")))
            }
            filename=recovered.optString("filename",ui(R.string.ui_recovered_image))
            document.foreground=recovered.optInt("foreground",Color.BLACK)
            document.strokeWidth=recovered.optDouble("stroke_width",5.0).toFloat()
            document.cornerRadius=recovered.optDouble("corner_radius",16.0).toFloat().coerceAtLeast(0f)
            document.brushTip=recovered.optInt("brush_tip");document.shapeStyle=recovered.optInt("shape_style")
            document.tolerance=recovered.optDouble("tolerance",0.0).toFloat()
            document.watercolorStrength=recovered.optInt("watercolor_strength",50).coerceIn(1,100)
            document.strokeSmoothing=recovered.optBoolean("stroke_smoothing")
            document.antialiasing=recovered.optBoolean("antialiasing",false)
            document.sprayRadius=recovered.optDouble("spray_radius",document.strokeWidth*2.0).toFloat().coerceIn(1f,100f)
            if (recovered.optBoolean("dirty")) document.edited()
            draftStatus=ui(R.string.ui_draft_restored);restored=true
        } catch (_: Exception) { recovered=null;preserveFailedDraft(ui(R.string.ui_the_previous_draft_could_not_be_restored)) }
          catch (_: OutOfMemoryError) { recovered=null;preserveFailedDraft(ui(R.string.ui_the_previous_draft_needs_more_memory_to_reopen)) }
        if (!restored) {
            val recovery=File(filesDir,"classic-recovery.png")
            if (recovery.isFile) try {
                val bounds=BitmapFactory.Options().apply { inJustDecodeBounds=true }
                BitmapFactory.decodeFile(recovery.path,bounds);checkImageSize(bounds.outWidth,bounds.outHeight)
                BitmapFactory.decodeFile(recovery.path,BitmapFactory.Options().apply { inMutable=true;inScaled=false })?.let {
                    document.replace(it)
                    val old=getSharedPreferences("classic",MODE_PRIVATE)
                    filename=old.getString("filename",ui(R.string.ui_recovered_image)) ?: ui(R.string.ui_recovered_image)
                    if (old.getBoolean("dirty",false)) document.edited()
                    restored=true;draftStatus=ui(R.string.ui_draft_restored)
                }
            } catch (_: Exception) { } catch (_: OutOfMemoryError) { }
        }
        paintCanvas=PaintCanvas(this,document).apply {
            tag="paint_canvas"
            onStatus={ updateStatus(); scheduleAutosave() }
            onPick={ colour -> recentColours.add(colour);refreshRecentColours();updateColours();updateStatus();scheduleAutosave() }
            onText={ x,y -> showTextDialog(x,y) }
            onFill={ x,y -> backgroundEdit { document.fill(x,y) } }
            onError={ editFailed(it) }
        }
        recovered?.optJSONObject("canvas")?.let { paintCanvas.restoreDraft(it) }
        expandedCategory=ToolCategory.forTool(paintCanvas.tool)
        expandedCategory?.let {categoryTools[it]=paintCanvas.tool}
        buildWorkspace()
        if (!restored) paintCanvas.addOnLayoutChangeListener(object : View.OnLayoutChangeListener {
            override fun onLayoutChange(view: View,l: Int,t: Int,r: Int,b: Int,ol: Int,ot: Int,or: Int,ob: Int) {
                if (r-l <= dp(20)+24 || b-t <= dp(20)+24) return
                view.removeOnLayoutChangeListener(this)
                editAction { document.newImage(r-l-dp(20)-24,b-t-dp(20)-24) };paintCanvas.fit()
            }
        })
        document.changed={ runOnUiThread { if (!isDestroyed) { paintCanvas.invalidate();updateStatus();scheduleAutosave() } } }
        autosaveReady=true;scheduleAutosave()
        recoveryNotice?.let { notice -> paintCanvas.post { message(notice) } }
        savedInstanceState?.let {
            exportOptions=ExportOptions(ImageFormat.values().getOrElse(it.getInt("export_format")) {ImageFormat.PNG},it.getInt("export_quality",95),it.getBoolean("export_lossless",true),it.getBoolean("export_dither",true),it.getBoolean("export_tiff_compressed",true),it.getInt("export_ico_size",256),it.getInt("export_ascii_columns",100),it.getBoolean("export_ascii_invert",false))
            shareAfterSave=it.getBoolean("share_after_save");isExporting=it.getBoolean("is_exporting")
        }
        if(savedInstanceState==null) handleExternalImage(intent)
    }

    private fun preserveFailedDraft(reason: String) {
        try {
            autosave.preserveForRecovery()
            recoveryNotice=ui(R.string.ui_a_separate_recovery_copy_has_been_kept_use, reason)
            draftStatus=ui(R.string.ui_previous_draft_kept_for_recovery)
        } catch (_: Exception) {
            autosaveBlocked=true
            lastAutosaveError=ui(R.string.ui_the_previous_draft_could_not_be_preserved_separately)
            draftStatus=ui(R.string.ui_autosave_paused_use_save)
            recoveryNotice=ui(R.string.ui_autosave_is_paused_to_protect_that_draft_use, reason)
        }
    }

    private val panelLimit get() = dp(if (landscape) (resources.configuration.screenHeightDp-96).coerceAtLeast(136) else minOf(256, resources.configuration.screenHeightDp / 3))
    private val sidePanelWidth get() = dp(minOf(248,resources.configuration.screenWidthDp / 3))
    private val toolHeight get() = if (VerticalText.uiVertical()) -2 else dp(64)
    private fun buildWorkspace() {
        paintCanvas.pauseGesture()
        paintCanvas.contentDescription=ui(R.string.ui_drawing_canvas_pinch_and_move_two_fingers_to)
        (paintCanvas.parent as? android.view.ViewGroup)?.removeView(paintCanvas)
        toolButtons.clear();categoryButtons.clear();categoryGroups.clear();recentCells.clear()
        tabPanels.clear();tabButtons.clear();customPaletteCells.clear()
        root=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;setBackgroundColor(surface);fitsSystemWindows=true}
        setContentView(root);makeHeader()
        tabPanelHost=FrameLayout(this).apply {tag="tab_panel_host"}
        val sideRibbon=if(landscape) LinearLayout(this).apply {
            orientation=LinearLayout.HORIZONTAL;isBaselineAligned=false;tag="vertical_ribbon_rail";layoutDirection=View.LAYOUT_DIRECTION_LTR
            addView(VerticalUi.detach(root.findViewWithTag<View>("tabs_row")),LinearLayout.LayoutParams(-2,-1))
            addView(tabPanelHost,LinearLayout.LayoutParams(-2,-1))
        } else null
        if(sideRibbon==null) root.addView(tabPanelHost,LinearLayout.LayoutParams(-1,-2))
        sidebar=RibbonPanel(this,panelLimit,landscape).apply {tag="sidebar"}
        val primary=LinearLayout(this).apply {orientation=if(landscape) LinearLayout.VERTICAL else LinearLayout.HORIZONTAL;isBaselineAligned=false;tag="primary_tools";layoutDirection=View.LAYOUT_DIRECTION_LTR}
        ToolCategory.values().forEach {category ->
            val entry=ToolCategoryButton(this,category,categoryTools[category] ?: category.tools.first(),!landscape).apply {
                tag="category_${category.name}";setOnClickListener {if(!busy) editAction {toggleCategory(category)}}
                categoryButtons[category]=this
            }
            primary.addView(entry,LinearLayout.LayoutParams(-2,toolHeight))
        }
        listOf(PaintTool.ERASER,PaintTool.FILL,PaintTool.PICKER).forEach {
            primary.addView(makeToolButton(it),LinearLayout.LayoutParams(-2,toolHeight))
        }
        if(landscape) {
            for(i in 0 until primary.childCount) primary.getChildAt(i).layoutParams=LinearLayout.LayoutParams(-1,toolHeight)
            sidebar.addView(ScrollView(this).apply {tag="primary_tool_scroll";addView(primary)},LinearLayout.LayoutParams(dp(if(VerticalText.uiVertical()) 132 else 100),-1))
        } else sidebar.addView(HorizontalScrollView(this).apply {tag="primary_tool_scroll";addView(primary)},LinearLayout.LayoutParams(-1,toolHeight))
        val drawerContent=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;setPadding(dp(4),0,dp(4),dp(4))}
        toolDrawer=ScrollView(this).apply {tag="tool_scroll";addView(drawerContent)}
        ToolCategory.values().forEach {category ->
            val group=LinearLayout(this).apply {isBaselineAligned=false;tag="category_tools_${category.name}"}
            category.tools.forEach {group.addView(makeToolButton(it),LinearLayout.LayoutParams(-2,toolHeight))}
            val rail: View=if(landscape) {
                // Wrap the category into tiles above its options, beside the primary tool rail.
                val grid=GridLayout(this).apply {columnCount=2;alignmentMode=GridLayout.ALIGN_BOUNDS}
                while(group.childCount>0) grid.addView(VerticalUi.detach(group.getChildAt(0)),GridLayout.LayoutParams().apply {
                    width=if(VerticalText.uiVertical()) -2 else (sidePanelWidth-dp(8))/2;height=toolHeight
                })
                group.orientation=LinearLayout.VERTICAL;group.addView(grid)
                if(VerticalText.uiVertical()) ColumnScrollView(this).apply {addView(group)} else group
            } else HorizontalScrollView(this).apply {addView(group)}
            categoryGroups[category]=rail;drawerContent.addView(rail)
        }
        options=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;tag="tool_options";setPadding(dp(4),dp(4),dp(4),0)}
        toolOptionsView=if(VerticalText.uiVertical()) ColumnScrollView(this).apply {addView(options)} else options
        drawingOptionsHost=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;addView(toolOptionsView)}
        drawerContent.addView(drawingOptionsHost)
        sidebar.addView(toolDrawer,LinearLayout.LayoutParams(if(landscape) sidePanelWidth else -1,if(landscape) -1 else -2))
        tabPanels["Draw"]=if(landscape) sidebar else LimitedScrollView(this,panelLimit).apply {addView(sidebar)}
        fun commands(name: String): View {
            fun control(index: Int,action: PanelCommand): View {
                if(name=="View" && index==0) return makeToolButton(PaintTool.ZOOM)
                val onClick={action.second();refreshCommandPanel(name)}
                return (action.icon?.let {panelButton(action.first,"command_${name}_$index",it,onClick)}
                    ?: button(action.first,"command_${name}_$index",onClick)).apply {isEnabled=menuActionEnabled();columnHeightDp=112}
            }
            if(VerticalText.uiVertical()) {
                val columns=LinearLayout(this).apply {tag="panel_${name}_commands";isBaselineAligned=false;gravity=Gravity.TOP;orientation=if(landscape) LinearLayout.VERTICAL else LinearLayout.HORIZONTAL;layoutDirection=if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL) View.LAYOUT_DIRECTION_RTL else View.LAYOUT_DIRECTION_LTR}
                menuActions(name).forEachIndexed {index,action ->
                    columns.addView(control(index,action),LinearLayout.LayoutParams(-2,-2).apply {setMargins(dp(3),dp(4),dp(3),dp(4))})
                }
                return ColumnScrollView(this).apply {addView(columns)}
            }
            val available=if(landscape) sidePanelWidth else dp(resources.configuration.screenWidthDp)
            val grid=GridLayout(this).apply {columnCount=if(landscape && name=="File") 1 else maxOf(2,available/dp(112));tag="panel_${name}_commands"}
            menuActions(name).forEachIndexed {index,action ->
                grid.addView(control(index,action),GridLayout.LayoutParams().apply {
                    rowSpec=GridLayout.spec(GridLayout.UNDEFINED,GridLayout.FILL)
                    width=available/grid.columnCount-dp(4);height=if(name=="File") dp(56) else -2
                    setMargins(dp(2),dp(2),dp(2),dp(2))
                })
            }
            return grid
        }
        listOf("File","Edit","View").forEach {name ->
            val body=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL}
            val grid=commands(name);body.addView(grid)
            if(name=="Edit") {
                editCommands=grid
                editDetails=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;visibility=View.GONE;tag="edit_details"}
                body.addView(if(VerticalText.uiVertical()) ColumnScrollView(this).apply {addView(editDetails)} else editDetails)
            }
            if(name=="View") {
                navigationOptionsHost=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;tag="navigation_options"}
                body.addView(navigationOptionsHost)
            }
            tabPanels[name]=LimitedScrollView(this,panelLimit).apply {tag="panel_$name";addView(body)}
        }
        val colours=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;tag="colour_dock"}
        val colourHeader=LinearLayout(this).apply {isBaselineAligned=false;gravity=Gravity.CENTER_VERTICAL;layoutDirection=View.LAYOUT_DIRECTION_LTR}
        colourStatus=ColourStatusButton(this).apply {
            tag="colour_status";editForeground={if(!busy) colourDialog(false)};editBackground={if(!busy) colourDialog(true)}
        }
        colourHeader.addView(colourStatus,LinearLayout.LayoutParams(dp(132),dp(88)))
        colourHeader.addView(panelButton(ui(R.string.ui_swap23),"swap_colours",R.drawable.classic_swap) {val old=document.foreground;document.foreground=document.background;document.background=old;updateColours()},LinearLayout.LayoutParams(-2,toolHeight))
        colourHeader.addView(panelButton(ui(R.string.ui_reset_bw23),"reset_colours",R.drawable.classic_bw) {document.foreground=Color.BLACK;document.background=Color.WHITE;updateColours()},LinearLayout.LayoutParams(-2,toolHeight))
        colourHeader.addView(panelButton(ui(R.string.ui_advanced),"advanced_colour",R.drawable.classic_palette) {colourDialog(false,advanced=true)},LinearLayout.LayoutParams(-2,toolHeight))
        if(landscape) {
            val actions=LinearLayout(this).apply {isBaselineAligned=false}
            while(colourHeader.childCount>1) actions.addView(VerticalUi.detach(colourHeader.getChildAt(1)))
            colourHeader.orientation=LinearLayout.VERTICAL;colourHeader.addView(actions,LinearLayout.LayoutParams(-2,-2))
        }
        colours.addView(HorizontalScrollView(this).apply {addView(colourHeader)})
        makePalette(colours);makeCustomPalette(colours)
        tabPanels["Color"]=LimitedScrollView(this,panelLimit).apply {tag="panel_Color";addView(colours)}
        tabPanels.forEach {(name,panel) ->tabPanelHost.addView(panel,FrameLayout.LayoutParams(if(landscape) {if(name=="Draw") -2 else sidePanelWidth} else -1,if(landscape && name=="Draw") -1 else -2))}
        val workspace=FrameLayout(this).apply {tag="workspace_overlay";layoutDirection=View.LAYOUT_DIRECTION_LTR}
        val canvasArea=if(sideRibbon==null) workspace else FrameLayout(this)
        if(VerticalText.uiVertical()) {
            val canvasRow=LinearLayout(this).apply {isBaselineAligned=false;tag="vertical_workspace"}
            statusText=FlowTextView(this).apply {tag="status_text";textSize=11f;columnHeightDp=600;setPadding(dp(4),dp(8),dp(4),dp(8))}
            val statusRail=HorizontalScrollView(this).apply {tag="vertical_status_rail";addView(statusText,android.view.ViewGroup.LayoutParams(-2,-1))}
            canvasRow.addView(statusRail,LinearLayout.LayoutParams(dp(52),-1))
            canvasRow.addView(paintCanvas,LinearLayout.LayoutParams(0,-1,1f))
            canvasArea.addView(canvasRow,FrameLayout.LayoutParams(-1,-1))
        } else canvasArea.addView(paintCanvas,FrameLayout.LayoutParams(-1,-1))
        if(sideRibbon!=null) {
            val split=LinearLayout(this).apply {isBaselineAligned=false;layoutDirection=View.LAYOUT_DIRECTION_LTR}
            split.addView(sideRibbon,LinearLayout.LayoutParams(-2,-1))
            split.addView(canvasArea,LinearLayout.LayoutParams(0,-1,1f))
            workspace.addView(split,FrameLayout.LayoutParams(-1,-1))
        }
        root.addView(workspace,LinearLayout.LayoutParams(-1,0,1f))
        makeStatus();populateToolOptions(paintCanvas.tool)
        if(paintCanvas.trim!=null) showBoundsOptions()
        syncPanels();updateColours();updateStatus();syncFullscreen()
    }

    private fun selectTab(name: String) {
        activeTab=name;sidebarExpanded=true;syncPanels()
        if(name=="Color") refreshCustomPalette()
    }
    private fun refreshCommandPanel(name: String) {
        menuActions(name).forEachIndexed {index,action ->
            root.findViewWithTag<Button>("command_${name}_$index")?.let {it.text=action.first;it.contentDescription=action.first;it.isEnabled=menuActionEnabled()}
        }
    }

    private fun makeToolButton(tool: PaintTool)=ToolButton(this,tool).apply {
        tag="tool_${tool.name}"
        setOnClickListener {if(!busy) editAction {chooseTool(tool)}}
        setOnLongClickListener {message(tool.label+": "+tool.hint);true}
        toolButtons[tool]=this
    }

    private fun toggleCategory(category: ToolCategory) {
        if(expandedCategory==category) {
            // Opening options is a view change: keep unfinished geometry intact.
            toolOptionsExpanded=!toolOptionsExpanded;syncPanels()
        } else {
            chooseTool(categoryTools[category] ?: category.tools.first())
        }
    }

    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig);AppLanguage.refresh(this, newConfig);buildWorkspace()
    }

    private fun syncPanels() {
        val visible=sidebarExpanded && !fullscreen
        tabPanelHost.visibility=if(visible) View.VISIBLE else View.GONE
        tabPanels.forEach {(name,panel) ->panel.visibility=if(name==activeTab) View.VISIBLE else View.GONE}
        tabButtons.forEach {(name,view) ->view.isSelected=name==activeTab}
        val navigating=paintCanvas.tool==PaintTool.ZOOM
        val host=if(navigating) navigationOptionsHost else drawingOptionsHost
        if(toolOptionsView.parent!==host) host.addView(VerticalUi.detach(toolOptionsView))
        navigationOptionsHost.visibility=if(navigating && toolOptionsExpanded) View.VISIBLE else View.GONE
        toolDrawer.visibility=if(toolOptionsExpanded && !navigating) View.VISIBLE else View.GONE
        categoryGroups.forEach {(category,view) ->view.visibility=if(category==expandedCategory) View.VISIBLE else View.GONE}
        categoryButtons.forEach {(category,view) ->
            view.selectedTool=categoryTools[category] ?: category.tools.first()
            view.expanded=toolOptionsExpanded && expandedCategory==category
            view.isSelected=paintCanvas.tool in category.tools;view.refresh()
        }
        sidebarToggle.isSelected=sidebarExpanded
        sidebarToggle.contentDescription=if(sidebarExpanded) ui(R.string.ui_collapse_toolbox) else ui(R.string.ui_expand_toolbox)
        getSharedPreferences("classic-ui",MODE_PRIVATE).edit().putBoolean("sidebar_expanded",sidebarExpanded).apply()
    }

    private fun dp(value: Int) = (value * resources.displayMetrics.density + .5f).toInt()
    private fun label(value: String, size: Float = 13f) = FlowTextView(this).apply {
        text = value; textSize = size; setTextColor(ink); gravity = Gravity.CENTER_VERTICAL
    }
    private fun button(value: String, tagName: String, action: () -> Unit) = FlowButton(this).apply {
        text = value; tag = tagName; contentDescription = value
        isAllCaps = false; textSize = 13f; minWidth = 0; minimumWidth = 0; minHeight = 0; minimumHeight = 0
        setPadding(dp(8), dp(6), dp(8), dp(6))
        setOnClickListener { if (!busy) editAction(action) else message(ui(R.string.ui_please_wait_for_the_current_operation)) }
    }

    private fun panelButton(value: String,tagName: String,icon: Int,action: () -> Unit)=PanelToolButton(this).apply {
        text=value;contentDescription=value;tag=tagName;labelledIcon(icon)
        if(android.os.Build.VERSION.SDK_INT>=26) tooltipText=value
        setOnClickListener {if(!busy) editAction(action) else message(ui(R.string.ui_please_wait_for_the_current_operation))}
    }

    private fun actionIcon(icon: EditIcon, tagName: String, action: () -> Unit) = ActionButton(this, icon).apply {
        tag = tagName
        setOnClickListener { if (!busy) editAction(action) }
        setOnLongClickListener { Toast.makeText(this@ClassicPaintActivity, icon.label, Toast.LENGTH_SHORT).show(); true }
    }

    private fun makeHeader() {
        titleText=TextView(this).apply {
            text=filename;textSize=13f;tag="document_title";setTextColor(EditorColours.onPrimaryContainer)
            ellipsize=TextUtils.TruncateAt.END;maxLines=1
        }
        val heading=LinearLayout(this).apply {
            orientation=LinearLayout.VERTICAL;gravity=Gravity.CENTER_VERTICAL;tag="document_heading";setPadding(dp(8),0,dp(4),0)
            addView(titleText,LinearLayout.LayoutParams(-1,-2))
            addView(TextView(this@ClassicPaintActivity).apply {
                text="AN Paint";textSize=10f;tag="document_subtitle";setTextColor(EditorColours.onPrimaryContainer);maxLines=1
            },LinearLayout.LayoutParams(-1,-2))
        }
        val bar=LinearLayout(this).apply {tag="header_bar";gravity=Gravity.CENTER_VERTICAL;layoutDirection=View.LAYOUT_DIRECTION_LTR;setBackgroundColor(EditorColours.primaryContainer)}
        bar.addView(heading,LinearLayout.LayoutParams(0,dp(52),1f))
        val quick=LinearLayout(this).apply {isBaselineAligned=false;gravity=Gravity.CENTER_VERTICAL;tag="quick_actions";layoutDirection=View.LAYOUT_DIRECTION_LTR}
        undoButton=actionIcon(EditIcon.UNDO,"undo") {undoEdit()}
        redoButton=actionIcon(EditIcon.REDO,"redo") {redoEdit()}
        listOf(undoButton,redoButton,
            actionIcon(EditIcon.CUT,"clipboard_cut") {cutSelection()},
            actionIcon(EditIcon.COPY,"clipboard_copy") {copySelection()},
            actionIcon(EditIcon.PASTE,"clipboard_paste") {pasteSelection()},
            actionIcon(EditIcon.SAVE,"save_image") {requestSave(false)}).forEach {quick.addView(it,LinearLayout.LayoutParams(dp(44),dp(44)))}
        bar.addView(quick,LinearLayout.LayoutParams(-2,dp(44)))
        root.addView(bar,LinearLayout.LayoutParams(-1,dp(52)))
        val tabs=LinearLayout(this).apply {orientation=if(landscape) LinearLayout.VERTICAL else LinearLayout.HORIZONTAL;isBaselineAligned=false;tag="tabs_row";gravity=Gravity.TOP;layoutDirection=View.LAYOUT_DIRECTION_LTR}
        val row=TabStrip(this,landscape).apply {tag="tab_strip"}
        listOf("View","Draw","File","Edit","Color").forEach {name ->
            val item=RibbonTab(this,landscape).apply {text=menuTitle(name);contentDescription=text;tag="menu_$name";setOnClickListener {selectTab(name)}}
            tabButtons[name]=item
            row.addView(item,LinearLayout.LayoutParams(if(landscape) -1 else -2,-2))
        }
        if(landscape) tabs.addView(ScrollView(this).apply {tag="menu_bar";addView(row)},LinearLayout.LayoutParams(dp(if(VerticalText.uiVertical()) 76 else 84),0,1f))
        else tabs.addView(HorizontalScrollView(this).apply {tag="menu_bar";addView(row)},LinearLayout.LayoutParams(0,-2,1f))
        sidebarToggle=actionIcon(EditIcon.SIDEBAR,"sidebar_toggle") {sidebarExpanded=!sidebarExpanded;syncPanels()}.apply {sideLayout=landscape}
        tabs.addView(sidebarToggle,LinearLayout.LayoutParams(dp(44),dp(44)).apply {gravity=Gravity.END})
        root.addView(tabs,LinearLayout.LayoutParams(if(landscape) -2 else -1,if(landscape) 0 else -2))
    }

    private fun makePalette(editor: LinearLayout) {
        val row = LinearLayout(this).apply { tag="palette_bar"; gravity = Gravity.CENTER_VERTICAL; setPadding(dp(4), dp(2), dp(4), dp(2)) }; paletteBar=row
        val scroll = HorizontalScrollView(this).apply { contentDescription = ui(R.string.ui_colour_palette_tap_for_foreground_hold_for_background) }
        val palette = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        val colours = arrayOf(
            "000000", "808080", "800000", "808000", "008000", "008080", "000080", "800080", "808040", "004040", "0080FF", "004080", "8000FF", "804000",
            "FFFFFF", "C0C0C0", "FF0000", "FFFF00", "00FF00", "00FFFF", "0000FF", "FF00FF", "FFFF80", "00FF80", "80FFFF", "8080FF", "FF0080", "FF8040"
        )
        colours.toList().chunked(14).forEach { values ->
            val strip = LinearLayout(this)
            values.forEach { hex ->
                val colour = Color.parseColor("#$hex")
                val swatch = View(this).apply {
                    tag = "colour_$hex"; contentDescription = ui(R.string.ui_colour_tap_foreground_hold_background, hex)
                    isFocusable = true
                    background = GradientDrawable().apply { setColor(colour); setStroke(dp(2), EditorColours.outline) }
                    setOnClickListener { if (!busy) setColour(colour,false) }
                    setOnLongClickListener { if (!busy) setColour(colour,true); true }
                }
                strip.addView(swatch, LinearLayout.LayoutParams(dp(36), dp(36)).apply { setMargins(dp(1), dp(1), dp(1), dp(1)) })
            }
            palette.addView(strip)
        }
        scroll.addView(palette); row.addView(scroll, LinearLayout.LayoutParams(0, dp(76), 1f))
        // Four extra cells stay at the far right, after the scrolling standard colours.
        val recent=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL;tag="recent_colours" }
        repeat(2) { rowIndex ->
            val pair=LinearLayout(this)
            repeat(2) { column ->
                val index=rowIndex*2+column
                val cell=View(this).apply {
                    tag="recent_colour_$index";isFocusable=true
                    setOnClickListener { recentColours.colours.getOrNull(index)?.let { if(!busy) setColour(it,false) } }
                    setOnLongClickListener { recentColours.colours.getOrNull(index)?.let { if(!busy) setColour(it,true) };true }
                }
                recentCells.add(cell);pair.addView(cell,LinearLayout.LayoutParams(dp(32),dp(36)).apply {setMargins(dp(1),dp(1),dp(1),dp(1))})
            };recent.addView(pair)
        }
        row.addView(recent);refreshRecentColours()
        editor.addView(row,LinearLayout.LayoutParams(-1,dp(88)))
    }

    private fun makeStatus() {
        cursorStatusHeight=0
        val row = LinearLayout(this).apply { gravity = Gravity.CENTER_VERTICAL; setPadding(dp(7), 0, dp(3), 0) }
        if(!VerticalText.uiVertical()) {
            statusText = label(ui(R.string.ui_ready), 11f).apply {tag="status_text";maxLines=2}
            row.addView(statusText, LinearLayout.LayoutParams(0, dp(44), 1f))
        } else row.gravity=Gravity.END
        val zoomRow = LinearLayout(this).apply {isBaselineAligned=false; gravity = Gravity.CENTER_VERTICAL; tag = "zoom_controls" }
        zoomRow.addView(actionIcon(EditIcon.MINUS, "zoom_out") { paintCanvas.zoomStep(1/1.5f) }, LinearLayout.LayoutParams(dp(40), dp(44)))
        zoomSlider = ZoomSeekBar(this).apply {
            tag = "zoom_slider"; contentDescription = ui(R.string.ui_canvas_zoom); max = 1000
            setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
                override fun onProgressChanged(bar: SeekBar?, value: Int, fromUser: Boolean) {
                    if (fromUser && !syncingZoom && !busy) paintCanvas.zoomAt(paintCanvas.zoomForSlider(value))
                }
                override fun onStartTrackingTouch(bar: SeekBar?) = Unit
                override fun onStopTrackingTouch(bar: SeekBar?) = Unit
            })
        }
        zoomRow.addView(zoomSlider, LinearLayout.LayoutParams(dp(108), dp(44)))
        zoomRow.addView(actionIcon(EditIcon.PLUS, "zoom_in") { paintCanvas.zoomStep(1.5f) }, LinearLayout.LayoutParams(dp(40), dp(44)))
        zoomRow.addView((if(VerticalText.uiVertical()) actionIcon(EditIcon.FIT,"zoom_fit_view") {paintCanvas.fit()} else button(ui(R.string.ui_fit),"zoom_fit_view") {paintCanvas.fit()}).apply {
            contentDescription=ui(R.string.ui_fit_entire_canvas_in_view)
        },LinearLayout.LayoutParams(dp(44),dp(44)))
        row.addView(zoomRow)
        root.addView(row)
    }

    private fun updateStatus() {
        if (!::statusText.isInitialized) return
        val normalStatus=ui(R.string.ui_px, paintCanvas.tool.label, paintCanvas.zoomStatusLabel(), document.bitmap.width, document.bitmap.height, draftStatus)
        val shownStatus=if(busy) (if(autosaving) ui(R.string.ui_autosaving_draft) else ui(R.string.ui_working)) else normalStatus
        if(!VerticalText.uiVertical()) {
            statusText.maxLines=if(paintCanvas.cursorMode) Int.MAX_VALUE else 2
            if(paintCanvas.cursorMode) {
                val available=if(statusText.width>0) statusText.width-statusText.compoundPaddingLeft-statusText.compoundPaddingRight
                    else dp((resources.configuration.screenWidthDp-242).coerceAtLeast(32))
                @Suppress("DEPRECATION")
                fun textHeight(value: String)=android.text.StaticLayout(value,statusText.paint,available.coerceAtLeast(1),
                    android.text.Layout.Alignment.ALIGN_NORMAL,statusText.lineSpacingMultiplier,statusText.lineSpacingExtra,statusText.includeFontPadding).height
                // Busy/saved messages must not shrink this area and resize the
                // canvas repeatedly while autosave records its viewport.
                cursorStatusHeight=maxOf(cursorStatusHeight,dp(44),maxOf(textHeight(normalStatus),textHeight(shownStatus))+statusText.compoundPaddingTop+statusText.compoundPaddingBottom)
            } else cursorStatusHeight=0
            val height=if(paintCanvas.cursorMode) cursorStatusHeight else dp(44)
            if(statusText.layoutParams.height!=height) statusText.layoutParams=statusText.layoutParams.apply {this.height=height}
        }
        statusText.text = (if(VerticalText.uiVertical()) filename+"\n" else "") + shownStatus
        if (::zoomSlider.isInitialized) {
            syncingZoom = true; zoomSlider.progress = paintCanvas.sliderForZoom(); syncingZoom = false
            zoomSlider.isEnabled = !busy
            zoomSlider.contentDescription = ui(R.string.ui_canvas_zoom_771f84, paintCanvas.zoomLabel())
        }
        if (::options.isInitialized) options.findViewWithTag<TextView>("selection_dimensions")?.text=document.selection?.let {
            String.format(java.util.Locale.ROOT,ui(R.string.ui_0f_0f_px_1f),it.rect.width(),it.rect.height(),it.rotation)
        } ?: ui(R.string.ui_select_an_area)
        if (::options.isInitialized) root.findViewWithTag<TextView>("trim_dimensions")?.text = paintCanvas.trim?.rect?.let { ui(R.string.ui_px_724eb3, it.width(), it.height()) } ?: ""
        if (::editDetails.isInitialized && paintCanvas.trim==null) {editDetails.visibility=View.GONE;editCommands.visibility=View.VISIBLE}
        titleText.text = "$filename${if (document.dirty) " *" else ""}"
        // Pending geometry can be cancelled; an empty history alone cannot be undone.
        redoButton.isEnabled = !busy && document.canRedo
        undoButton.isEnabled = !busy && (document.canUndo || paintCanvas.hasPendingEdit)
        toolButtons.forEach { (tool, view) -> view.isSelected = tool == paintCanvas.tool; view.invalidate() }
        categoryButtons.forEach {(category,view) ->view.isSelected=paintCanvas.tool in category.tools;view.invalidate()}
        listOf("File","Edit","View").forEach {refreshCommandPanel(it)}
    }

    private fun updateColours(persist: Boolean=true) {
        colourStatus.foreground=document.foreground;colourStatus.backgroundColour=document.background;colourStatus.refresh()
        paintCanvas.invalidate();if(persist) scheduleAutosave()
    }

    private fun chooseTool(tool: PaintTool) {
        activeTab=if(tool==PaintTool.ZOOM) "View" else "Draw";sidebarExpanded=true
        paintCanvas.selectTool(tool)
        showToolOptions(tool)
    }

    private fun showToolOptions(tool: PaintTool) {
        if(tool!=PaintTool.ZOOM) drawingTool=tool
        expandedCategory=ToolCategory.forTool(tool)
        expandedCategory?.let {categoryTools[it]=tool}
        toolOptionsExpanded=true
        populateToolOptions(tool);syncPanels()
        toolDrawer.scrollTo(0,0)
    }

    private fun populateToolOptions(tool: PaintTool) {
        options.removeAllViews()
        options.addView(label(tool.label, 12f).apply { typeface = Typeface.DEFAULT_BOLD })
        when (tool) {
            PaintTool.SELECT, PaintTool.LASSO -> {
                options.addView(label(ui(R.string.ui_corners_and_edges_resize_round_handle_rotates),11f))
                options.addView(label("").apply { tag="selection_dimensions" })
                options.addView(CheckBox(this).apply {
                    tag="selection_lock_aspect";text=ui(R.string.ui_lock_proportions);textSize=11f;isChecked=paintCanvas.lockSelectionAspect
                    setOnCheckedChangeListener { _,checked -> paintCanvas.lockSelectionAspect=checked;scheduleAutosave() }
                },LinearLayout.LayoutParams(-1,dp(48)))

            }
            PaintTool.FILL -> addSlider(ui(R.string.ui_tolerance), document.tolerance.toInt(), 100) { document.tolerance = it.toFloat() }
            PaintTool.ZOOM -> {
                options.addView(label(ui(R.string.ui_pinch_to_zoom_drag_to_pan),12f))
                options.addView(button(ui(R.string.ui_draw_again), "navigate_draw") { chooseTool(drawingTool) },LinearLayout.LayoutParams(-1,dp(48)))
                options.addView(button(ui(R.string.ui_100), "zoom_actual") { paintCanvas.zoomAt(1f) },LinearLayout.LayoutParams(-1,dp(44)))
                options.addView(button(ui(R.string.ui_fit), "zoom_fit") { paintCanvas.fit() }, LinearLayout.LayoutParams(-1, dp(44)))
            }
            PaintTool.PENCIL -> addSlider(ui(R.string.ui_size_px),paintCanvas.pencilSize.toInt(),100,1,"pencil_size") {paintCanvas.pencilSize=it.toFloat()}
            PaintTool.TEXT -> options.addView(label(ui(R.string.ui_tap_canvas_to_type), 12f))
            PaintTool.PICKER -> options.addView(label(ui(R.string.ui_tap_a_pixel), 12f))
            else -> {
                addSlider(ui(R.string.ui_size_px), document.strokeWidth.toInt(), 100, 1, "brush_size") { document.strokeWidth = it.toFloat() }
                if (tool == PaintTool.ROUND_RECT) addSlider(ui(R.string.ui_radius_px),document.cornerRadius.toInt(),
                    maxOf(64,minOf(document.bitmap.width,document.bitmap.height)/2,document.cornerRadius.toInt()),tagName="corner_radius") {
                    document.cornerRadius=it.toFloat();paintCanvas.invalidate()
                }
                if (tool == PaintTool.WATERCOLOR) addSlider(ui(R.string.ui_strength),document.watercolorStrength,100,1,"watercolor_strength") { document.watercolorStrength=it }
                if (tool == PaintTool.SPRAY) addSlider(ui(R.string.ui_spray_radius_px),document.sprayRadius.toInt(),100,1,"spray_radius") { document.sprayRadius=it.toFloat() }
                if (tool in listOf(PaintTool.BRUSH,PaintTool.WATERCOLOR,PaintTool.ERASER,PaintTool.LINE)) {
                    val tips=if(tool==PaintTool.BRUSH) listOf(ui(R.string.ui_round),ui(R.string.ui_square),ui(R.string.ui_calligraphy)) else listOf(ui(R.string.ui_round),ui(R.string.ui_square))
                    addChoice(tips,document.brushTip.coerceIn(tips.indices)) {document.brushTip=it}
                }
                if (tool in listOf(PaintTool.RECTANGLE, PaintTool.POLYGON, PaintTool.ELLIPSE, PaintTool.ROUND_RECT,PaintTool.HEART,PaintTool.STAR,PaintTool.ARROW))
                    addChoice(listOf(ui(R.string.ui_outline), ui(R.string.ui_solid_fill), ui(R.string.ui_fill_line)), document.shapeStyle) { document.shapeStyle = it; paintCanvas.invalidate() }
            }
        }
        if (tool in listOf(PaintTool.POLYGON, PaintTool.CURVE, PaintTool.SELECT, PaintTool.LASSO)) {
            options.addView(button(when (tool) { PaintTool.POLYGON -> ui(R.string.ui_finish_polygon); PaintTool.CURVE -> ui(R.string.ui_finish_curve); else -> ui(R.string.ui_commit_selection) }, "apply") {
                paintCanvas.applyPending()
            }, LinearLayout.LayoutParams(-1, dp(48)))
        }
        if(tool==PaintTool.POLYGON) options.addView(CheckBox(this).apply {
            tag="polygon_close";text=ui(R.string.ui_close_polygon);textSize=11f;isChecked=paintCanvas.closePolygon
            setOnCheckedChangeListener {_,checked -> paintCanvas.closePolygon=checked;paintCanvas.invalidate();scheduleAutosave()}
        })
        options.addView(button(ui(R.string.ui_how_to_use), "tool_help") { message(tool.hint) }, LinearLayout.LayoutParams(-1, dp(48)))
        if(tool in listOf(PaintTool.PENCIL,PaintTool.BRUSH,PaintTool.WATERCOLOR,PaintTool.SPRAY,PaintTool.ERASER,PaintTool.LINE,PaintTool.CURVE)) {
            options.addView(button(ui(R.string.ui_drawing_settings),"drawing_settings") {showDrawingSettings(false)},LinearLayout.LayoutParams(-1,dp(48)))
        }
        if(VerticalText.uiVertical()) VerticalUi.panel(options)
        updateStatus()
    }

    private fun addSlider(name: String, value: Int, maximum: Int, minimum: Int = 0, tagName: String? = null, action: (Int) -> Unit) {
        val control=NumericSlider(this,name,value,minimum,maximum) { action(it);paintCanvas.invalidate();scheduleAutosave() }
        control.slider.tag=tagName
        control.number.tag=tagName?.let { "${it}_value" }
        options.addView(control)
    }

    private fun addChoice(values: List<String>, selected: Int, action: (Int) -> Unit) {
        val choice = button(values[selected], "tool_option") {}
        choice.setOnClickListener {
            EditorDialogBuilder(this).setTitle(ui(R.string.ui_tool_option)).setSingleChoiceItems(values.toTypedArray(), selected) { dialog, which ->
                action(which); choice.text = values[which]; dialog.dismiss()
            }.setNegativeButton(ui(R.string.ui_cancel), null).show()
        }
        options.addView(choice, LinearLayout.LayoutParams(-1, dp(48)))
    }

    private fun menuTitle(name: String): String=ui(when(name) {
        "Draw"->R.string.ui_draw26;"File"->R.string.ui_menu_file;"Edit"->R.string.ui_menu_edit
        "View"->R.string.ui_menu_view;"Color"->R.string.ui_colour_tab23;else->R.string.ui_menu_help
    })
    private data class PanelCommand(val first: String,val second: () -> Unit,val icon: Int?=null)
    private fun command(title: String,icon: Int,action: () -> Unit)=PanelCommand(title,action,icon)
    private fun menuActions(name: String): List<PanelCommand> = when(name) {
        "File"->(listOf<Pair<String,()->Unit>>(
            ui(R.string.ui_new) to {confirmReplacement {dimensionsDialog(false,true)}},
            ui(R.string.ui_load_image) to {confirmReplacement {launchOpen(false)}},
            ui(R.string.ui_save) to {requestSave(false)},
            ui(R.string.save20_title) to {showSaveOptions(savedTarget?.options?.format ?: ImageFormat.PNG)},
            ui(R.string.ui_export_as23) to {showSaveOptions(exportOptions.format,export=true)},
            ui(R.string.ui_save_and_share) to {showSaveOptions(exportOptions.format,true,export=true)},
            ui(R.string.ui_insert_image_into_canvas) to {launchOpen(true)},
            ui(R.string.ui_catrobat_sticker_gallery) to {startActivityForResult(Intent(this,MediaGalleryActivity::class.java),GALLERY_IMAGE)},
            ui(R.string.ui_image_assembly) to {openAssembly()},
            ui(R.string.ui_how_to_use) to {showHelp()},
            ui(R.string.ui_about_credits23) to {showAboutOptions()}
        ) + if(autosaveBlocked || autosave.recoveryCopies().isNotEmpty()) listOf(ui(R.string.ui_export_recovery_copy) to {requestRecoveryExport()}) else emptyList()).map {PanelCommand(it.first,it.second)}
        "Edit"->listOf(
            command(ui(R.string.ui_select_all),R.drawable.breeze_select_all) {selectAll();selectTab("Edit")},
            command(ui(R.string.ui_canvas_bounds),R.drawable.classic_bounds) {trimCanvas()},
            command(ui(R.string.ui_delete_selection),R.drawable.classic_delete) {if(!document.deleteSelection()) message(ui(R.string.ui_select_an_area_first))},
            command(ui(R.string.ui_canvas_size),R.drawable.classic_canvas_size) {dimensionsDialog(false,false)},
            command(ui(R.string.ui_crop_to_selection),R.drawable.classic_crop) {if(document.cropSelection()) paintCanvas.fit() else message(ui(R.string.ui_select_an_area_first))},
            command(ui(R.string.ui_resize_image),R.drawable.classic_resize) {dimensionsDialog(true,false)},
            command(ui(R.string.ui_flip_horizontal),R.drawable.classic_flip_h) {paintCanvas.applyPending();document.transform(Matrix().apply {setScale(-1f,1f)})},
            command(ui(R.string.ui_flip_vertical),R.drawable.classic_flip_v) {paintCanvas.applyPending();document.transform(Matrix().apply {setScale(1f,-1f)})},
            command(ui(R.string.ui_rotate_90_clockwise),R.drawable.classic_rotate90) {paintCanvas.applyPending();document.transform(Matrix().apply {setRotate(90f)});paintCanvas.fit()},
            command(ui(R.string.ui_rotate_180),R.drawable.classic_rotate180) {paintCanvas.applyPending();document.transform(Matrix().apply {setRotate(180f)})},
            command(ui(R.string.ui_invert_colours),R.drawable.classic_invert) {paintCanvas.applyPending();document.invert()},
            command(ui(R.string.ui_clear_image),R.drawable.breeze_eraser) {paintCanvas.applyPending();document.clear()}
        )
        "View"->listOf(
            command(PaintTool.ZOOM.label,R.drawable.breeze_zoom_in) {chooseTool(PaintTool.ZOOM)},
            command((if(paintCanvas.grid) ui(R.string.ui_hide_pixel_grid_800) else ui(R.string.ui_show_pixel_grid_800)),R.drawable.classic_grid) {paintCanvas.grid=!paintCanvas.grid;paintCanvas.invalidate()},
            command((if(paintCanvas.cursorMode) ui(R.string.ui_disable_cursor_drawing) else ui(R.string.ui_enable_cursor_drawing)),R.drawable.classic_cursor) {paintCanvas.setCursorMode(!paintCanvas.cursorMode);if(paintCanvas.cursorMode) chooseTool(paintCanvas.tool)},
            command(ui(R.string.ui_magnified_preview),R.drawable.breeze_zoom_in) {showDrawingSettings(true)},
            command(ui(R.string.ui_languages23),R.drawable.classic_languages) {AppLanguage.showPicker(this) {buildWorkspace()}},
            command((if(fullscreen) ui(R.string.ui_show_editor_controls) else ui(R.string.ui_hide_editor_controls)),R.drawable.classic_fullscreen) {fullscreen=!fullscreen;syncFullscreen()}
        )
        else->emptyList()
    }
    private fun menuActionEnabled()=!busy
    private fun showAboutOptions() {
        val actions=listOf(
            ui(R.string.ui_about_copyright_licence) to {LegalInfo.showAbout(this)},
            ui(R.string.ui_gnu_agpl_licence) to {LegalInfo.showAsset(this,ui(R.string.ui_gnu_affero_general_public_license),"legal/AGPL-3.0.txt")},
            ui(R.string.ui_third_party_notices) to {LegalInfo.showAsset(this,ui(R.string.ui_open_source_credits_and_notices),"legal/THIRD_PARTY_NOTICES.txt")},
            ui(R.string.ui_export_this_version_s_source_code) to {exportSource()},
            ui(R.string.ui_icons_fonts_artwork_credits) to {LegalInfo.showAsset(this,ui(R.string.ui_icons_fonts_artwork_credits),"legal/ASSET_CREDITS.txt")},
            ui(R.string.ui_image_credits) to {showImageCredits()},
            ui(R.string.ui_image_codec_licences) to {LegalInfo.showCodecLicences(this)},
            ui(R.string.ui_font_licences) to {LegalInfo.showAsset(this,ui(R.string.ui_font_licences),"legal/FONT_NOTICES.txt")},
            ui(R.string.ui_icon_licences) to {LegalInfo.showAsset(this,ui(R.string.ui_icon_licences_kde_breeze),"legal/ICON_NOTICES.txt")})
        EditorDialogBuilder(this).setTitle(ui(R.string.ui_about_credits23)).setItems(actions.map {it.first}.toTypedArray()) {_,index->actions[index].second()}
            .setNegativeButton(ui(R.string.ui_done),null).show()
    }

    private fun selectAfterPaste() {
        // Switching to selection before pasting avoids committing a new floating image.
        updateStatus(); paintCanvas.invalidate()
    }

    private fun cutSelection() { if (!document.cutSelection()) message(ui(R.string.ui_select_an_area_first)) }
    private fun copySelection() { if (!document.copySelection()) message(ui(R.string.ui_select_an_area_first)) }
    private fun pasteSelection() {
        chooseTool(PaintTool.SELECT)
        if (document.paste()) selectAfterPaste() else message(ui(R.string.ui_copy_an_area_or_use_file_insert_image))
    }

    private fun editAction(action: () -> Unit): Boolean {
        if (autosaving) { message(ui(R.string.ui_the_draft_is_saving_try_again_shortly));return false }
        try { action();return true }
        catch (error: OutOfMemoryError) { editFailed(error) }
        catch (error: IOException) { editFailed(error) }
        catch (error: IllegalArgumentException) { editFailed(error) }
        return false
    }

    private fun checkImageSize(width: Int, height: Int) {
        ImageMemoryPolicy.forDevice(this).check(width, height, if (::document.isInitialized) document.residentPixels else 0)
    }

    private fun editFailed(error: Throwable) {
        message(if (error is ImageSizeException) error.message!! else if (error is OutOfMemoryError) ui(R.string.ui_there_is_not_enough_memory_for_this_operation)
            else ui(R.string.ui_could_not_complete_the_edit, error.message ?: ui(R.string.ui_please_try_again)))
    }

    private fun backgroundEdit(action: () -> Unit) {
        if (busy) return
        beginIo()
        worker.execute {
            try { action() }
            catch (error: OutOfMemoryError) { runOnUiThread { if (!isDestroyed) editFailed(error) } }
            catch (error: Exception) { runOnUiThread { if (!isDestroyed) editFailed(error) } }
            finally { runOnUiThread { if (!isDestroyed) { endIo(); paintCanvas.invalidate() } } }
        }
    }

    private var colourPreviewOriginal: Pair<Int,Int>?=null
    private fun colourDialog(background: Boolean,advanced: Boolean=false) {
        colourPreviewOriginal=document.foreground to document.background
        AdvancedColourDialog(this,if(background) document.background else document.foreground,background,
            preview={colour ->if(background) document.background=colour else document.foreground=colour;updateColours(false)},
            paletteChanged={refreshCustomPalette()},closed={colourPreviewOriginal=null},initialMode=if(advanced) 1 else 0) {colour ->colourPreviewOriginal=null;setColour(colour,background)}.show()
    }
    private fun makeCustomPalette(parent: LinearLayout) {
        val row=LinearLayout(this).apply {tag="saved_palette_row";gravity=Gravity.CENTER_VERTICAL}
        val strip=LinearLayout(this)
        repeat(16) {index ->
            val cell=SavedColourCell(this).apply {tag="palette_custom_$index";isFocusable=true
                setOnClickListener {if(!busy) {
                    val store=CustomColours(this@ClassicPaintActivity)
                    if(store.has(index)) setColour(store.colour(index),false) else addColour(index)
                }}
                setOnLongClickListener {if(!busy) editPaletteColour(index);true}
            }
            customPaletteCells.add(cell);strip.addView(cell,LinearLayout.LayoutParams(dp(40),dp(40)).apply {setMargins(dp(2),dp(2),dp(2),dp(2))})
        }
        row.addView(HorizontalScrollView(this).apply {addView(strip)},LinearLayout.LayoutParams(0,dp(44),1f))
        row.addView(panelButton(ui(R.string.ui_add_colour26),"add_colour",R.drawable.classic_palette) {addColour()},LinearLayout.LayoutParams(-2,toolHeight))
        parent.addView(label(ui(R.string.ui_saved_palette23)));parent.addView(row);refreshCustomPalette()
    }
    private fun refreshCustomPalette() {
        val palette=CustomColours(this)
        customPaletteCells.forEachIndexed {index,cell ->
            cell.colour=if(palette.has(index)) palette.colour(index) else null
            cell.contentDescription=cell.colour?.let {ui(R.string.ui_colour,String.format(java.util.Locale.ROOT,"#%06X",it and 0xffffff))}
                ?: ui(R.string.ui_empty_palette26,index+1)
        }
    }
    private fun addColour(slot: Int?=null) {
        val store=CustomColours(this)
        val index=slot ?: (0 until 16).firstOrNull {!store.has(it)}
        if(index==null) {
            val entries=store.entries()
            EditorDialogBuilder(this).setTitle(ui(R.string.ui_replace_palette23))
                .setItems(entries.map {String.format(java.util.Locale.ROOT,"#%06X",it.second and 0xffffff)}.toTypedArray()) {_,which ->addColour(entries[which].first)}
                .setNegativeButton(ui(R.string.ui_cancel),null).show()
            return
        }
        colourPreviewOriginal=document.foreground to document.background
        AdvancedColourDialog(this,if(slot!=null && store.has(slot)) store.colour(slot) else document.foreground,false,
            preview={document.foreground=it;updateColours(false)},paletteChanged={refreshCustomPalette()},
            closed={colourPreviewOriginal?.let {document.foreground=it.first;updateColours(false)};colourPreviewOriginal=null},
            initialMode=1,addingToPalette=true,replacingPaletteColour=store.has(index)) {colour ->
                colourPreviewOriginal=null;store.replace(index,colour);refreshCustomPalette();setColour(colour,false)
            }.show()
    }
    private fun editPaletteColour(index: Int) {
        val store=CustomColours(this)
        if(!store.has(index)) {addColour(index);return}
        EditorDialogBuilder(this).setTitle(String.format(java.util.Locale.ROOT,"#%06X",store.colour(index) and 0xffffff))
            .setItems(arrayOf(ui(R.string.ui_background_colour),ui(R.string.ui_edit_colour26),ui(R.string.ui_remove_palette23))) {_,action ->
                when(action) {0->setColour(store.colour(index),true);1->addColour(index);2->{store.remove(index);refreshCustomPalette()}}
            }.setNegativeButton(ui(R.string.ui_cancel),null).show()
    }

    private fun dimensionsDialog(stretch: Boolean, fresh: Boolean) {
        val column = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(20), dp(6), dp(20), dp(6)) }
        val sizing = DimensionControls(this,ImageDimensions(document.bitmap.width,document.bitmap.height),locked = stretch)
        column.addView(sizing)
        column.addView(label(if (stretch) ui(R.string.ui_scales_the_image_unlock_the_ratio_to_stretch) else ui(R.string.ui_keeps_pixels_at_the_top_left_smaller_canvas), 12f))
        column.addView(label(String.format(java.util.Locale.ROOT, ui(R.string.ui_current_safe_budget_2f_mp), ImageMemoryPolicy.forDevice(this).maxPixels(document.residentPixels) / 1_000_000.0), 12f))
        val dialog = EditorDialogBuilder(this).setTitle(if (fresh) ui(R.string.ui_new_image) else if (stretch) ui(R.string.ui_resize_image_ab28be) else ui(R.string.ui_canvas_size_30460e)).setView(ScrollView(this).apply { addView(column) }).setNegativeButton(ui(R.string.ui_cancel), null).setPositiveButton(ui(R.string.ui_apply), null).create()
        dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
            val size = sizing.dimensions
            if (size == null) sizing.widthInput.error = ui(R.string.ui_enter_positive_dimensions)
            else editAction {
                checkImageSize(size.width,size.height); paintCanvas.applyPending()
                if (fresh) { document.newImage(size.width,size.height); filename = ui(R.string.ui_untitled);savedTarget=null } else document.resize(size.width,size.height,stretch)
                paintCanvas.fit(); updateStatus(); dialog.dismiss()
            }
        } }; dialog.show()
    }

    private fun selectAll() {
        chooseTool(PaintTool.SELECT)
        document.select(RectF(0f,0f,document.bitmap.width.toFloat(),document.bitmap.height.toFloat()))
    }
    private fun undoEdit() {
        val resizing = paintCanvas.trim != null
        if (!paintCanvas.cancelPending()) document.undo()
        if (resizing) chooseTool(paintCanvas.tool)
    }
    private fun redoEdit() {
        val resizing = paintCanvas.trim != null
        paintCanvas.cancelPending(); document.redo()
        if (resizing) chooseTool(paintCanvas.tool)
    }
    private fun trimCanvas() {
        paintCanvas.beginTrim(); showBoundsOptions()
    }
    private fun showBoundsOptions() {
        activeTab="Edit";sidebarExpanded=true;editCommands.visibility=View.GONE;editDetails.visibility=View.VISIBLE
        editDetails.removeAllViews()
        editDetails.addView(label(ui(R.string.ui_drag_out_to_expand_in_to_trim_drag),12f))
        editDetails.addView(label("").apply {tag="trim_dimensions"})
        fun finish() {editDetails.visibility=View.GONE;editCommands.visibility=View.VISIBLE;syncPanels()}
        editDetails.addView(button(ui(R.string.ui_apply_bounds),"trim_apply") {paintCanvas.applyTrim();finish()},LinearLayout.LayoutParams(-1,dp(48)))
        editDetails.addView(button(ui(R.string.ui_cancel),"trim_cancel") {paintCanvas.cancelTrim();finish()},LinearLayout.LayoutParams(-1,dp(48)))
        editDetails.addView(button(ui(R.string.ui_fit),"trim_fit") {paintCanvas.fit()},LinearLayout.LayoutParams(-1,dp(48)))
        if(VerticalText.uiVertical()) VerticalUi.panel(editDetails)
        syncPanels();updateStatus()
    }
    override fun onKeyShortcut(keyCode: Int, event: android.view.KeyEvent): Boolean {
        if (event.isCtrlPressed && keyCode == android.view.KeyEvent.KEYCODE_A && !busy) { editAction { selectAll() }; return true }
        return super.onKeyShortcut(keyCode,event)
    }

    private fun showTextDialog(x: Float,y: Float) {
        TextStyleDialog(this,textSettings,document.foreground,document.background) { settings,face ->
            editAction {
                document.text(x,y,settings.text,settings.size,face,settings.box,settings.underline,settings.strike,
                    arrayOf(Paint.Align.LEFT,Paint.Align.CENTER,Paint.Align.RIGHT)[settings.alignment],settings.spacing,settings.direction,settings.glyphOrientation)
                textSettings=settings;scheduleAutosave()
            }
        }.show()
    }

    private fun confirmReplacement(action: () -> Unit) {
        paintCanvas.applyPending()
        if (!document.dirty) { action(); return }
        EditorDialogBuilder(this).setTitle(ui(R.string.ui_save_your_changes)).setMessage(ui(R.string.ui_your_current_image_has_unsaved_changes))
            .setPositiveButton(ui(R.string.ui_save_a5d0d9)) { _, _ -> afterSave = action; requestSave(false) }
            .setNeutralButton(ui(R.string.ui_discard_changes23)) { _, _ -> action() }.setNegativeButton(ui(R.string.ui_keep_editing23), null).show()
    }

    fun launchOpen(import: Boolean) {
        if (busy) return
        launchPicker(Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            // Some otherwise valid images are labelled as generic binary by providers.
            type = "*/*"
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }, if (import) IMPORT_IMAGE else OPEN_IMAGE)
    }

    private fun launchPicker(intent: Intent, request: Int) {
        try { startActivityForResult(intent, request) }
        catch (_: ActivityNotFoundException) {
            if (intent.action == Intent.ACTION_OPEN_DOCUMENT) {
                try { startActivityForResult(Intent(intent).setAction(Intent.ACTION_GET_CONTENT), request); return }
                catch (_: ActivityNotFoundException) { /* Explain the missing picker below. */ }
            }
            afterSave = null
            message(ui(R.string.ui_android_could_not_find_a_file_picker_enable))
        } catch (e: SecurityException) { afterSave = null; message(ui(R.string.ui_android_blocked_the_file_picker, e.message)) }
    }

    private fun requestSave(jpeg: Boolean) {
        if(jpeg) {showSaveOptions(ImageFormat.JPEG,export=true);return}
        val target=savedTarget
        if(target==null) showSaveOptions(ImageFormat.PNG)
        else {exportOptions=target.options;isExporting=false;shareAfterSave=false;writeImage(target.uri)}
    }
    private fun showSaveOptions(format: ImageFormat,share: Boolean=false,export: Boolean=false) {
        val prefs=getSharedPreferences("export",MODE_PRIVATE)
        SaveOptionsDialog(this,ExportOptions(format,prefs.getInt("quality",95),!export,prefs.getBoolean("dither",true),prefs.getBoolean("tiff_compressed",true),prefs.getInt("ico_size",256),prefs.getInt("ascii_columns",100),prefs.getBoolean("ascii_invert",false)),share,
            confirm={request ->
                exportOptions=request.options;shareAfterSave=share;isExporting=export
                prefs.edit().putInt("quality",exportOptions.quality).putBoolean("dither",exportOptions.dither).putBoolean("tiff_compressed",exportOptions.tiffCompressed).putInt("ico_size",exportOptions.icoSize).putInt("ascii_columns",exportOptions.asciiColumns).putBoolean("ascii_invert",exportOptions.asciiInvert).apply()
                chooseSaveLocation(request.fileName)
            },cancel={afterSave=null;shareAfterSave=false},initialFilename=filename,export=export).show()
    }
    private fun chooseSaveLocation(proposedName: String=filename) {
        launchPicker(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE);type=exportOptions.format.mime
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION or Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)
            putExtra(Intent.EXTRA_TITLE,ExportNames.withExtension(proposedName.ifBlank {ui(R.string.ui_untitled)},exportOptions.format))
        },SAVE_IMAGE)
    }
    override fun onNewIntent(intent: Intent) {super.onNewIntent(intent);setIntent(intent);handleExternalImage(intent)}
    private fun handleExternalImage(incoming: Intent) {
        val uri=when(incoming.action) {
            Intent.ACTION_SEND -> incoming.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
            Intent.ACTION_VIEW,Intent.ACTION_EDIT -> incoming.data
            else -> null
        } ?: return
        confirmReplacement {readImage(uri,false)}
    }

    fun exportSource() {
        launchPicker(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE); type = "application/zip"; putExtra(Intent.EXTRA_TITLE, ui(R.string.ui_an_paint_source_zip))
        }, EXPORT_SOURCE)
    }

    private fun requestRecoveryExport() {
        val copies=if (autosaveBlocked) listOf(File(autosave.file.path+".bak").takeIf { it.isFile } ?: autosave.file) else autosave.recoveryCopies()
        fun choose(file: File) {
            recoveryExport=file
            launchPicker(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                addCategory(Intent.CATEGORY_OPENABLE);type="application/zip";putExtra(Intent.EXTRA_TITLE,ui(R.string.ui_an_paint_recovery_zip, file.lastModified()))
            },EXPORT_RECOVERY)
        }
        if (copies.size==1) choose(copies.first()) else if (copies.isNotEmpty()) EditorDialogBuilder(this)
            .setTitle(ui(R.string.ui_export_recovery_copy_144b8a)).setItems(copies.map { java.text.DateFormat.getDateTimeInstance().format(java.util.Date(it.lastModified())) }.toTypedArray()) { _,i -> choose(copies[i]) }
            .setNegativeButton(ui(R.string.ui_cancel),null).show()
    }

    private fun openAssembly() {
        paintCanvas.applyPending()
        startActivityForResult(Intent(this,AssemblyActivity::class.java).putExtra("resident_pixels",document.residentPixels),ASSEMBLY_IMAGE)
    }

    public override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK) { if (requestCode == SAVE_IMAGE) { afterSave = null;shareAfterSave=false }; return }
        if(requestCode==GALLERY_IMAGE) {
            val file=data?.getStringExtra("gallery_file")?.let {File(cacheDir,it)}
            val source=data?.getStringExtra("gallery_source")
            if(file==null || file.parentFile!=cacheDir || !file.name.startsWith("gallery-") || !file.isFile || source==null || !MediaGalleryActivity.allowed(Uri.parse(source))) {message(ui(R.string.ui_the_gallery_image_is_unavailable));return}
            GalleryCredits.remember(this,source)
            readImage(Uri.fromFile(file),true,deleteAfterCopy=true);return
        }
        if (requestCode == ASSEMBLY_IMAGE) {
            val name = data?.getStringExtra("assembly_output")
            val file = name?.let { File(filesDir,it) }
            if (file == null || file.parentFile != filesDir || !file.name.startsWith("assembly-output-") || !file.isFile) { message(ui(R.string.ui_the_assembly_output_is_unavailable_reopen_image_assembly)); return }
            readImage(Uri.fromFile(file),false,asEdit = true,deleteAfterCopy = true); return
        }
        val uri = data?.data ?: data?.clipData?.getItemAt(0)?.uri
        if (uri == null) { message(ui(R.string.ui_the_picker_returned_no_file_please_choose_the)); afterSave = null; return }
        when (requestCode) {
            OPEN_IMAGE, IMPORT_IMAGE -> readImage(uri, requestCode == IMPORT_IMAGE)
            SAVE_IMAGE -> {
                if(!isExporting) try {
                    val flags=(data?.flags ?: 0) and (Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
                    if(flags!=0) contentResolver.takePersistableUriPermission(uri,flags)
                } catch(_: SecurityException) { /* Some providers grant session-only access. */ }
                writeImage(uri)
            }
            EXPORT_SOURCE -> exportSourceTo(uri)
            EXPORT_RECOVERY -> exportRecoveryTo(uri)
        }
    }

    private fun readImage(uri: Uri, import: Boolean, asEdit: Boolean = false, deleteAfterCopy: Boolean = false) {
        beginIo()
        worker.execute {
            var temporary: File? = null
            try {
                val cached = File.createTempFile("classic-import-", ".image", cacheDir)
                temporary = cached
                contentResolver.openInputStream(uri)?.use { ImportFiles.copy(it,cached) }
                    ?: throw IOException(ui(R.string.ui_the_selected_provider_did_not_return_any_image))
                val name=if(asEdit) ui(R.string.ui_assembly_png) else displayName(uri)
                if(deleteAfterCopy) File(uri.path!!).delete()
                temporary=null
                runOnUiThread {
                    if(isDestroyed || isFinishing) cached.delete()
                    else {
                        val selection=ImportSelection(this,worker,{document.residentPixels},
                            selected={source ->
                                importSelection=null;pendingImportFile=source.file
                                val plan=ImportPlan.create(source.dimensions,source.dimensions)
                                if(source.accepts(ImageMemoryPolicy.forDevice(this),plan,document.residentPixels)) decodeImage(source,import,source.dimensions,asEdit)
                                else askToResize(source,import,asEdit=asEdit)
                            },cancelled={importSelection=null;endIo()},failed={error ->
                                importSelection=null;ioFailed(ui(R.string.ui_could_not_open_image),error)
                            })
                        importSelection=selection;selection.start(cached,name)
                    }
                }
            } catch (e: Exception) { ioFailed(ui(R.string.ui_could_not_open_image), e) }
            catch (e: OutOfMemoryError) { ioFailed(ui(R.string.ui_not_enough_memory_to_inspect_this_image), e) }
            finally { temporary?.delete() }
        }
    }

    private fun askToResize(source: ImportedImage, import: Boolean, previousAttempt: ImageDimensions? = null, asEdit: Boolean = false) {
        if (isDestroyed || isFinishing) { source.file.delete(); return }
        resizeDialog = ImageResizeDialog(this,source.dimensions,document.residentPixels,
            { ImageMemoryPolicy.forDevice(this) },previousAttempt,
            resize = { size -> resizeDialog = null; decodeImage(source,import,size,asEdit) },
            cancel = { resizeDialog = null; source.file.delete(); pendingImportFile=null; if (!isDestroyed) endIo() },
            memoryRequirements = source.memoryRequirements
        ).show()
    }

    private fun decodeImage(source: ImportedImage, import: Boolean, target: ImageDimensions, asEdit: Boolean = false) {
        worker.execute {
            try {
                val plan = ImportPlan.create(source.dimensions,target)
                val policy=ImageMemoryPolicy.forDevice(this)
                source.checkImport(policy,plan,document.residentPixels)
                val bitmap = source.decode(plan,policy.workingBytes,document.residentPixels)
                source.file.delete()
                runOnUiThread {
                    pendingImportFile=null
                    if (!isDestroyed && !isFinishing) {
                        try {
                            if (import) { chooseTool(PaintTool.SELECT); document.paste(bitmap, takeOwnership = true) }
                            else { paintCanvas.cancelPending(); document.replace(bitmap,asEdit); filename = source.name;savedTarget=null; paintCanvas.fit() }
                            endIo()
                        } catch (error: Exception) {
                            if (document.bitmap !== bitmap && document.selection?.image !== bitmap) bitmap.recycle()
                            ioFailed(ui(R.string.ui_could_not_open_image), error)
                        } catch (error: OutOfMemoryError) {
                            if (document.bitmap !== bitmap && document.selection?.image !== bitmap) bitmap.recycle()
                            ioFailed(ui(R.string.ui_not_enough_memory_to_finish_opening_this_image), error)
                        }
                    } else bitmap.recycle()
                }
            } catch (_: ImageSizeException) {
                // Device memory may change while the user considers the proposed size.
                runOnUiThread { askToResize(source,import,target,asEdit) }
            } catch (_: OutOfMemoryError) {
                // A budget is an estimate, not a guarantee. Offer a smaller copy after an allocation failure too.
                runOnUiThread { askToResize(source,import,target,asEdit) }
            } catch (e: Exception) { source.file.delete(); ioFailed(ui(R.string.ui_could_not_open_image), e) }
        }
    }

    private fun writeImage(uri: Uri) {
        paintCanvas.applyPending()
        beginIo()
        val snapshot=document.bitmap
        val options=exportOptions;val exporting=isExporting;val sharing=shareAfterSave;shareAfterSave=false
        worker.execute {
            var encoded: File?=null
            try {
                val directory=File(cacheDir,"images").apply {mkdirs()}
                val file=File.createTempFile("AN-Paint-",options.format.extension,directory);encoded=file
                ImageExporter.encode(snapshot,file,options,ImageMemoryPolicy.forDevice(this).workingBytes)
                contentResolver.openOutputStream(uri,"wt")?.use {output -> file.inputStream().use {it.copyTo(output)}}
                    ?: throw IOException(ui(R.string.ui_the_selected_location_is_not_writable))
                val name=displayName(uri)
                if(sharing) encoded=null
                runOnUiThread {if(!isDestroyed) {
                    if(!exporting) {filename=name;savedTarget=SavedTarget(uri,name,options);document.markSaved();scheduleAutosave()};endIo();Toast.makeText(this,ui(R.string.ui_saved, name),Toast.LENGTH_SHORT).show()
                    if(sharing) shareSavedImage(file,options.format)
                    val action=afterSave;afterSave=null
                    if(exporting && action!=null) message(ui(R.string.ui_export_did_not_save23)) else action?.invoke()
                }}
            } catch(error: Exception) {ioFailed(ui(R.string.ui_could_not_save_image),error)}
              catch(error: OutOfMemoryError) {ioFailed(ui(R.string.ui_not_enough_memory_to_save_in_this_format),error)}
            finally {encoded?.delete()}
        }
    }
    private fun shareSavedImage(file: File,format: ImageFormat) {
        try {
            val uri=androidx.core.content.FileProvider.getUriForFile(this,"$packageName.fileprovider",file)
            val send=Intent(Intent.ACTION_SEND).apply {
                type=format.mime;putExtra(Intent.EXTRA_STREAM,uri)
                clipData=android.content.ClipData.newRawUri(ui(R.string.ui_an_paint_image),uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            startActivity(Intent.createChooser(send,ui(R.string.ui_share_saved_image)))
        } catch(error: Exception) {message(ui(R.string.ui_the_image_was_saved_but_android_could_not, error.message))}
    }

    private fun exportSourceTo(uri: Uri) {
        beginIo()
        worker.execute {
            try {
                assets.open(SOURCE_ASSET).use { source -> contentResolver.openOutputStream(uri, "wt")?.use { source.copyTo(it) } ?: throw IOException(ui(R.string.ui_this_location_is_not_writable)) }
                runOnUiThread { if (!isDestroyed) { endIo(); message(ui(R.string.ui_source_code_exported_including_build_scripts_and_licence)) } }
            } catch (e: Exception) { ioFailed(ui(R.string.ui_could_not_export_source_code), e) }
        }
    }

    private fun exportRecoveryTo(uri: Uri) {
        val file=recoveryExport ?: return
        beginIo()
        worker.execute {
            try {
                file.inputStream().use { source -> contentResolver.openOutputStream(uri,"wt")?.use { source.copyTo(it) } ?: throw IOException(ui(R.string.ui_this_location_is_not_writable)) }
                runOnUiThread { if (!isDestroyed) { endIo();message(ui(R.string.ui_recovery_copy_exported_extract_canvas_png_from_the)) } }
            } catch (e: Exception) { ioFailed(ui(R.string.ui_could_not_export_the_recovery_copy),e) }
        }
    }

    private fun displayName(uri: Uri): String {
        try { contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use { cursor ->
            val index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
            if (index >= 0 && cursor.moveToFirst()) return cursor.getString(index) ?: ui(R.string.ui_menu_image)
        } } catch (_: Exception) { /* Display metadata is optional. */ }
        return uri.lastPathSegment?.substringAfterLast('/') ?: ui(R.string.ui_menu_image)
    }
    private fun beginIo() { operationsInFlight++; busy = true; lastIoError = null; paintCanvas.isEnabled = false; updateStatus() }
    private fun endIo() { operationsInFlight = (operationsInFlight - 1).coerceAtLeast(0); busy = operationsInFlight > 0; paintCanvas.isEnabled = !busy; updateStatus(); if (!busy && autosaveReady && draftGeneration != savedDraftGeneration && draftGeneration != failedDraftGeneration) { autosaveHandler.removeCallbacks(saveDraft); autosaveHandler.postDelayed(saveDraft,if (stopped) 0 else 1500) } }
    private fun ioFailed(prefix: String, e: Throwable) {
        runOnUiThread { if (!isDestroyed) { afterSave = null; endIo(); lastIoError = "$prefix. ${e.message ?: ui(R.string.ui_try_a_different_file_or_location)}"; message(lastIoError!!) } }
    }
    private fun setColour(colour: Int,background: Boolean) {
        if(background) document.background=colour else document.foreground=colour
        recentColours.add(colour);refreshRecentColours();updateColours()
    }
    private fun refreshRecentColours() {
        recentCells.forEachIndexed { index,cell ->
            val colour=recentColours.colours.getOrNull(index)
            cell.background=GradientDrawable().apply { setColor(colour ?: EditorColours.surface);setStroke(dp(2),EditorColours.outline) }
            cell.isEnabled=colour!=null
            cell.contentDescription=if(colour==null) ui(R.string.ui_recent_colour_empty, index+1) else String.format(java.util.Locale.ROOT,ui(R.string.ui_recent_colour_d_06x_tap_foreground_hold_background),index+1,colour and 0xffffff)
        }
    }
    private fun showImageCredits() {
        GalleryCredits.showEditor(this)
    }
    private fun showDrawingSettings(preview: Boolean) {
        val column=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;setPadding(dp(18),dp(8),dp(18),dp(8))}
        fun toggle(title: String,value: Boolean,change: (Boolean)->Unit) {
            column.addView(CheckBox(this).apply {text=title;isChecked=value;setOnCheckedChangeListener {_,on -> change(on);paintCanvas.invalidate();scheduleAutosave()} })
        }
        if(preview) {
            toggle(ui(R.string.ui_show_magnified_drawing_preview),paintCanvas.magnifiedPreview) { paintCanvas.magnifiedPreview=it }
            column.addView(NumericSlider(this,ui(R.string.ui_magnification),(paintCanvas.previewMagnification*100).toInt(),100,400) {
                paintCanvas.previewMagnification=it/100f;paintCanvas.invalidate();scheduleAutosave()
            }.apply {tag="preview_magnification"})
        } else {
            toggle(ui(R.string.ui_smooth_freehand_strokes),document.strokeSmoothing) { document.strokeSmoothing=it }
            toggle(ui(R.string.ui_smooth_pixel_edges_anti_aliasing),document.antialiasing) { document.antialiasing=it }
            column.addView(label(ui(R.string.ui_pencil_crisp_adjustable_strokes)))
        }
        EditorDialogBuilder(this).setTitle(if(preview) ui(R.string.ui_magnified_preview_ea9209) else ui(R.string.ui_drawing_settings_d900c6))
            .setView(ScrollView(this).apply {addView(column)}).setPositiveButton(ui(R.string.ui_done),null).show()
    }
    private fun syncFullscreen() {
        if(!::root.isInitialized) return
        for(i in 0 until root.childCount) root.getChildAt(i).let { it.visibility=if(fullscreen && it.tag!="workspace_overlay") View.GONE else View.VISIBLE }
        syncPanels()
        root.findViewWithTag<View>("vertical_status_rail")?.visibility=if(fullscreen) View.GONE else View.VISIBLE
        root.findViewWithTag<View>("vertical_ribbon_rail")?.visibility=if(fullscreen) View.GONE else View.VISIBLE
        sidebarToggle.visibility=if(fullscreen) View.GONE else View.VISIBLE
        val workspace=root.findViewWithTag<FrameLayout>("workspace_overlay")
        workspace.findViewWithTag<View>("leave_fullscreen")?.let {workspace.removeView(it)}
        if(fullscreen) workspace.addView(button(ui(R.string.ui_show_controls),"leave_fullscreen") {fullscreen=false;syncFullscreen()},FrameLayout.LayoutParams(-2,if(VerticalText.uiVertical()) -2 else dp(48),Gravity.TOP or Gravity.END))
        window.decorView.systemUiVisibility=if(fullscreen) View.SYSTEM_UI_FLAG_FULLSCREEN else View.SYSTEM_UI_FLAG_VISIBLE
    }
    private fun showHelp() = message(ui(R.string.ui_help23))
    private fun message(text: String) { if (!isFinishing && !isDestroyed) EditorDialogBuilder(this).setTitle("AN Paint").setMessage(text).setPositiveButton(ui(R.string.ui_ok), null).show() }

    private fun scheduleAutosave() {
        if (!autosaveReady || autosaveBlocked || isDestroyed) return
        draftGeneration++;draftStatus=ui(R.string.ui_draft_pending)
        autosaveHandler.removeCallbacks(saveDraft)
        autosaveHandler.postDelayed(saveDraft,if (stopped) 0 else 1500)
    }
    private fun draftMetadata(): JSONObject = JSONObject().apply {
        put("version",1);put("filename",filename);put("dirty",document.dirty)
        savedTarget?.let {put("save_target",it.json())}
        put("foreground",colourPreviewOriginal?.first ?: document.foreground);put("background",colourPreviewOriginal?.second ?: document.background)
        put("corner_radius",document.cornerRadius.toDouble());put("stroke_width",document.strokeWidth.toDouble());put("brush_tip",document.brushTip);put("shape_style",document.shapeStyle)
        put("tolerance",document.tolerance.toDouble());put("watercolor_strength",document.watercolorStrength)
        put("stroke_smoothing",document.strokeSmoothing);put("antialiasing",document.antialiasing);put("spray_radius",document.sprayRadius.toDouble())
        put("canvas",paintCanvas.draftState());put("text_settings",textSettings.json());put("saved_at",System.currentTimeMillis())
        document.selection?.takeIf { it.floating }?.let { s -> put("floating_rect",JSONArray(listOf(s.rect.left,s.rect.top,s.rect.right,s.rect.bottom)));put("floating_rotation",s.rotation.toDouble());s.outline?.let { put("selection_outline",SelectionOutline.write(it)) } }
    }
    private fun saveDraftIfReady() {
        if (!autosaveReady || autosaveBlocked || isDestroyed || draftGeneration==savedDraftGeneration || draftGeneration==failedDraftGeneration) return
        if (busy || paintCanvas.hasActiveGesture) { autosaveHandler.postDelayed(saveDraft,400);return }
        val generation=draftGeneration
        val image=document.bitmap
        val floating=document.selection?.takeIf { it.floating }?.image
        val metadata=draftMetadata()
        autosaving=true;beginIo()
        worker.execute {
            var error: Throwable?=null
            try {
                autosave.write(image,floating,metadata);savedDraftGeneration=generation
                File(filesDir,"classic-recovery.png").delete()
            } catch (e: Exception) { error=e } catch (e: OutOfMemoryError) { error=e }
            val failure=error
            runOnUiThread { if (!isDestroyed) {
                autosaving=false
                if (failure==null) { draftStatus=ui(R.string.ui_draft_saved);lastAutosaveError=null }
                else { failedDraftGeneration=generation;lastAutosaveError=failure.message;draftStatus=ui(R.string.ui_autosave_failed_use_save) }
                endIo()
            } }
        }
    }
    override fun onSaveInstanceState(outState: Bundle) { outState.putInt("export_format",exportOptions.format.ordinal);outState.putInt("export_quality",exportOptions.quality);outState.putBoolean("export_lossless",exportOptions.lossless);outState.putBoolean("export_dither",exportOptions.dither);outState.putBoolean("export_tiff_compressed",exportOptions.tiffCompressed);outState.putInt("export_ico_size",exportOptions.icoSize);outState.putInt("export_ascii_columns",exportOptions.asciiColumns);outState.putBoolean("export_ascii_invert",exportOptions.asciiInvert);outState.putBoolean("share_after_save",shareAfterSave);outState.putBoolean("is_exporting",isExporting); super.onSaveInstanceState(outState) }
    override fun onStart() { super.onStart();stopped=false }
    override fun onStop() {
        super.onStop();stopped=true
        if (::document.isInitialized && autosaveReady) {
            if (!busy) paintCanvas.pauseGesture()
            scheduleAutosave();autosaveHandler.removeCallbacks(saveDraft);saveDraftIfReady()
        }
    }
    override fun onBackPressed() { if(fullscreen) {fullscreen=false;syncFullscreen()} else if (!busy) confirmReplacement { finish() } }
    override fun onDestroy() {
        importSelection?.dispose();importSelection=null
        resizeDialog?.dismiss();resizeDialog=null;pendingImportFile?.delete();pendingImportFile=null
        autosaveReady=false;autosaveHandler.removeCallbacksAndMessages(null);document.changed={}
        val metadata=draftMetadata();val generation=draftGeneration
        if (!busy && generation==savedDraftGeneration) document.close() else worker.execute {
            try {
                if (!autosaveBlocked && generation!=savedDraftGeneration) autosave.write(document.bitmap,document.selection?.takeIf { it.floating }?.image,metadata)
            } catch (_: Exception) { } catch (_: OutOfMemoryError) { }
            finally { document.close() }
        }
        worker.shutdown();super.onDestroy()
    }
}
