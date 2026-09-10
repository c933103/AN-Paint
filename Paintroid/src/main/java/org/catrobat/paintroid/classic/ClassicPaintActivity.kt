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
    private lateinit var foregroundButton: Button
    private lateinit var backgroundButton: Button
    private lateinit var undoButton: ActionButton
    private lateinit var redoButton: ActionButton
    private lateinit var zoomSlider: SeekBar
    private var syncingZoom = false
    private val toolButtons = linkedMapOf<PaintTool, ToolButton>()
    private var filename = ui(R.string.ui_untitled)
    private var exportOptions=ExportOptions()
    private var shareAfterSave=false
    private lateinit var recentColours: RecentColours
    private val recentCells=mutableListOf<View>()
    private var fullscreen=false
    private var afterSave: (() -> Unit)? = null
    private val worker = Executors.newSingleThreadExecutor()
    @Volatile var busy = false; private set
    private var operationsInFlight = 0
    private var resizeDialog: AlertDialog? = null
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
    private val cream = 0xffe8e7df.toInt()
    private val ink = 0xff233b4d.toInt()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
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
            document.antialiasing=recovered.optBoolean("antialiasing",true)
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
            exportOptions=ExportOptions(ImageFormat.values().getOrElse(it.getInt("export_format")) {ImageFormat.PNG},it.getInt("export_quality",95),it.getBoolean("export_lossless",true))
            shareAfterSave=it.getBoolean("share_after_save")
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

    private fun buildWorkspace() {
        (paintCanvas.parent as? android.view.ViewGroup)?.removeView(paintCanvas)
        toolButtons.clear();recentCells.clear()
        root=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL;setBackgroundColor(cream);fitsSystemWindows=true }
        setContentView(root);makeHeader()
        val workspace=FrameLayout(this).apply { tag="workspace_overlay" }
        root.addView(workspace,LinearLayout.LayoutParams(-1,0,1f))
        val work=LinearLayout(this).apply { orientation=LinearLayout.HORIZONTAL;tag="editor_workspace" }
        workspace.addView(work,FrameLayout.LayoutParams(-1,-1))
        sidebar=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL;tag="sidebar" }
        work.addView(sidebar,LinearLayout.LayoutParams(dp(104),-1))
        // Keep tools clear of the arrow; the canvas retains its full height.
        sidebar.addView(Space(this),LinearLayout.LayoutParams(-1,dp(48)))
        val rail=ScrollView(this).apply { tag="tool_scroll";contentDescription=ui(R.string.ui_toolbox_and_tool_options_scroll_for_more) }
        sidebar.addView(rail,LinearLayout.LayoutParams(-1,0,1f))
        val content=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL;setPadding(dp(3),dp(4),dp(3),dp(8)) }
        rail.addView(content)
        for (row in PaintTool.values().toList().chunked(2)) {
            val pair=LinearLayout(this)
            row.forEach { tool ->
                val item=ToolButton(this,tool).apply {
                    tag="tool_${tool.name}"
                    setOnClickListener { if (!busy) editAction { chooseTool(if (tool==PaintTool.ZOOM && paintCanvas.tool==tool) drawingTool else tool) } }
                    setOnLongClickListener { message(tool.label+": "+tool.hint);true }
                }
                toolButtons[tool]=item;pair.addView(item,LinearLayout.LayoutParams(0,dp(48),1f))
            };content.addView(pair)
        }
        options=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL;setPadding(dp(3),dp(7),dp(3),0) };content.addView(options)
        colourStatus=ColourStatusButton(this).apply { tag="colour_status";setOnClickListener { togglePalette() } }
        sidebar.addView(colourStatus,LinearLayout.LayoutParams(-1,dp(80)))
        // The palette opens beside the pinned indicator, never below the sidebar.
        val editor=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL;tag="canvas_and_palette" }
        work.addView(editor,LinearLayout.LayoutParams(0,-1,1f))
        editor.addView(paintCanvas,LinearLayout.LayoutParams(-1,0,1f))
        sidebarToggle=actionIcon(EditIcon.SIDEBAR,"sidebar_toggle") { sidebarExpanded=!sidebarExpanded;syncPanels() }
        workspace.addView(sidebarToggle,FrameLayout.LayoutParams(dp(48),dp(48),Gravity.TOP or Gravity.LEFT))
        makePalette(editor);makeStatus();populateToolOptions(paintCanvas.tool)
        if (paintCanvas.trim != null) showBoundsOptions()
        syncPanels();updateColours();updateStatus();syncFullscreen()
    }

    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig);buildWorkspace()
    }

    private fun togglePalette() {
        paletteExpanded=!paletteExpanded
        if (paletteExpanded) sidebarExpanded=true
        syncPanels()
    }
    private fun syncPanels() {
        sidebar.visibility=if (sidebarExpanded) View.VISIBLE else View.GONE
        paletteBar.visibility=if (sidebarExpanded && paletteExpanded) View.VISIBLE else View.GONE
        sidebarToggle.isSelected=sidebarExpanded
        sidebarToggle.contentDescription=if (sidebarExpanded) ui(R.string.ui_collapse_toolbox) else ui(R.string.ui_expand_toolbox)
        if (android.os.Build.VERSION.SDK_INT >= 26) sidebarToggle.tooltipText=sidebarToggle.contentDescription
        colourStatus.expanded=paletteExpanded;colourStatus.refresh()
        getSharedPreferences("classic-ui",MODE_PRIVATE).edit().putBoolean("sidebar_expanded",sidebarExpanded).putBoolean("palette_expanded",paletteExpanded).apply()
    }

    private fun dp(value: Int) = (value * resources.displayMetrics.density + .5f).toInt()
    private fun label(value: String, size: Float = 13f) = TextView(this).apply {
        text = value; textSize = size; setTextColor(ink); gravity = Gravity.CENTER_VERTICAL
    }
    private fun button(value: String, tagName: String, action: () -> Unit) = Button(this).apply {
        text = value; tag = tagName; contentDescription = value
        isAllCaps = false; textSize = 13f; minWidth = 0; minimumWidth = 0; minHeight = 0; minimumHeight = 0
        setPadding(dp(5), 0, dp(5), 0)
        setOnClickListener { if (!busy) editAction(action) else message(ui(R.string.ui_please_wait_for_the_current_operation)) }
    }

    private fun actionIcon(icon: EditIcon, tagName: String, action: () -> Unit) = ActionButton(this, icon).apply {
        tag = tagName
        setOnClickListener { if (!busy) editAction(action) }
        setOnLongClickListener { Toast.makeText(this@ClassicPaintActivity, icon.label, Toast.LENGTH_SHORT).show(); true }
    }

    private fun makeHeader() {
        undoButton=actionIcon(EditIcon.UNDO,"undo") { undoEdit() }
        redoButton=actionIcon(EditIcon.REDO,"redo") { redoEdit() }
        titleText=label("AN Paint",15f).apply { tag="document_title";setTextColor(Color.WHITE);ellipsize=TextUtils.TruncateAt.END;maxLines=if (landscape) 1 else 2 }
        if (landscape) {
            val bar=FrameLayout(this).apply { tag="header_bar";setBackgroundColor(0xff1559a6.toInt()) }
            val left=LinearLayout(this).apply { gravity=Gravity.CENTER_VERTICAL }
            val menu=button(ui(R.string.ui_menu),"compact_menu") {}
            menu.setOnClickListener {
                if (busy) return@setOnClickListener
                val popup=PopupMenu(this,menu)
                val commands=mutableMapOf<Int,() -> Unit>()
                listOf("File","Edit","View","Image","Colors","Help").forEachIndexed { group,name ->
                    val submenu=popup.menu.addSubMenu(0,group,group,menuTitle(name))
                    menuActions(name).forEachIndexed { index,action ->
                        val id=(group+1)*1000+index
                        submenu.add(group+1,id,index,action.first).isEnabled=menuActionEnabled(name,index)
                        commands[id]=action.second
                    }
                }
                popup.setOnMenuItemClickListener { item ->
                    val command=commands[item.itemId]
                    if (command==null) false else { if (!busy) editAction(command);true }
                };popup.show()
            }
            left.addView(menu,LinearLayout.LayoutParams(dp(60),dp(48)))
            bar.addView(left,FrameLayout.LayoutParams(-2,-1,Gravity.START))
            val right=LinearLayout(this).apply { gravity=Gravity.CENTER_VERTICAL }
            right.addView(undoButton,LinearLayout.LayoutParams(dp(44),dp(48)))
            right.addView(redoButton,LinearLayout.LayoutParams(dp(44),dp(48)))
            right.addView(button(ui(R.string.ui_save),"save_image") { requestSave(false) },LinearLayout.LayoutParams(dp(56),dp(48)))
            bar.addView(right,FrameLayout.LayoutParams(-2,-1,Gravity.END))
            titleText.gravity=Gravity.CENTER
            bar.addView(titleText,FrameLayout.LayoutParams(-1,-1).apply { leftMargin=dp(150);rightMargin=dp(150) })
            root.addView(bar,LinearLayout.LayoutParams(-1,dp(48)))
        } else {
            val bar=LinearLayout(this).apply { tag="header_bar";gravity=Gravity.CENTER_VERTICAL;setPadding(dp(2),0,dp(2),0);setBackgroundColor(0xff1559a6.toInt()) }
            bar.addView(titleText,LinearLayout.LayoutParams(0,dp(52),1f))
            bar.addView(undoButton,LinearLayout.LayoutParams(dp(44),dp(48)))
            bar.addView(redoButton,LinearLayout.LayoutParams(dp(44),dp(48)))
            bar.addView(button(ui(R.string.ui_save),"save_image") { requestSave(false) },LinearLayout.LayoutParams(dp(54),dp(48)))
            root.addView(bar)
            val scroll=HorizontalScrollView(this).apply { tag="menu_bar";isHorizontalScrollBarEnabled=false }
            val menus=LinearLayout(this)
            listOf("File","Edit","View","Image","Colors","Help").forEach { name ->
                val item=button(menuTitle(name),"menu_$name") {};item.setOnClickListener { if (!busy) showMenu(name,item) }
                menus.addView(item,LinearLayout.LayoutParams(dp(if (name=="Colors") 66 else 56),dp(44)))
            }
            scroll.addView(menus);root.addView(scroll,LinearLayout.LayoutParams(-1,dp(44)))
        }
    }

    private fun makePalette(editor: LinearLayout) {
        val row = LinearLayout(this).apply { tag="palette_bar"; gravity = Gravity.CENTER_VERTICAL; setPadding(dp(4), dp(2), dp(4), dp(2)) }; paletteBar=row
        val swatches = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        foregroundButton = button(ui(R.string.ui_fg), "foreground_colour") { colourDialog(false) }
        backgroundButton = button(ui(R.string.ui_bg), "background_colour") { colourDialog(true) }
        swatches.addView(foregroundButton, LinearLayout.LayoutParams(dp(48), dp(36)))
        swatches.addView(backgroundButton, LinearLayout.LayoutParams(dp(48), dp(36)))
        row.addView(swatches)
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
                    background = GradientDrawable().apply { setColor(colour); setStroke(dp(2), 0xffa0a49f.toInt()) }
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
        editor.addView(row,LinearLayout.LayoutParams(-1,dp(80)))
    }

    private fun makeStatus() {
        val row = LinearLayout(this).apply { gravity = Gravity.CENTER_VERTICAL; setPadding(dp(7), 0, dp(3), 0) }
        statusText = label(ui(R.string.ui_ready), 11f).apply { maxLines = 2 }
        row.addView(statusText, LinearLayout.LayoutParams(0, dp(44), 1f))
        val zoomRow = LinearLayout(this).apply { gravity = Gravity.CENTER_VERTICAL; tag = "zoom_controls" }
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
        zoomRow.addView(button(ui(R.string.ui_fit),"zoom_fit_view") { paintCanvas.fit() }.apply {
            contentDescription=ui(R.string.ui_fit_entire_canvas_in_view)
        },LinearLayout.LayoutParams(dp(44),dp(44)))
        row.addView(zoomRow)
        root.addView(row)
    }

    private fun updateStatus() {
        if (!::statusText.isInitialized) return
        statusText.text = if (busy) (if (autosaving) ui(R.string.ui_autosaving_draft) else ui(R.string.ui_working)) else ui(R.string.ui_px, paintCanvas.tool.label, paintCanvas.zoomLabel(), document.bitmap.width, document.bitmap.height, draftStatus)
        if (::zoomSlider.isInitialized) {
            syncingZoom = true; zoomSlider.progress = paintCanvas.sliderForZoom(); syncingZoom = false
            zoomSlider.isEnabled = !busy
            zoomSlider.contentDescription = ui(R.string.ui_canvas_zoom_771f84, paintCanvas.zoomLabel())
        }
        if (::options.isInitialized) options.findViewWithTag<TextView>("selection_dimensions")?.text=document.selection?.let {
            String.format(java.util.Locale.ROOT,ui(R.string.ui_0f_0f_px_1f),it.rect.width(),it.rect.height(),it.rotation)
        } ?: ui(R.string.ui_select_an_area)
        if (::options.isInitialized) options.findViewWithTag<TextView>("trim_dimensions")?.text = paintCanvas.trim?.rect?.let { ui(R.string.ui_px_724eb3, it.width(), it.height()) } ?: ""
        titleText.text = "${if (landscape) "" else "AN Paint\n"}$filename${if (document.dirty) " *" else ""}"
        // Pending geometry can be cancelled; an empty history alone cannot be undone.
        redoButton.isEnabled = !busy && document.canRedo
        undoButton.isEnabled = !busy && (document.canUndo || paintCanvas.hasPendingEdit)
        toolButtons.forEach { (tool, view) -> view.isSelected = tool == paintCanvas.tool; view.invalidate() }
    }

    private fun updateColours() {
        listOf(foregroundButton to document.foreground, backgroundButton to document.background).forEach { (view, colour) ->
            view.backgroundTintList = android.content.res.ColorStateList.valueOf(colour)
            view.setTextColor(if (Color.red(colour) * .299 + Color.green(colour) * .587 + Color.blue(colour) * .114 > 150) Color.BLACK else Color.WHITE)
        }
        foregroundButton.contentDescription = ui(R.string.ui_foreground_edit_colour, String.format("#%06X", document.foreground and 0xffffff))
        backgroundButton.contentDescription = ui(R.string.ui_background_edit_colour, String.format("#%06X", document.background and 0xffffff))
        colourStatus.foreground=document.foreground;colourStatus.backgroundColour=document.background;colourStatus.refresh()
        paintCanvas.invalidate();scheduleAutosave()
    }

    private fun chooseTool(tool: PaintTool) {
        if (tool != PaintTool.ZOOM) drawingTool=tool
        paintCanvas.selectTool(tool)
        populateToolOptions(tool)
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
            PaintTool.PENCIL -> options.addView(label(ui(R.string.ui_1_px), 12f))
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
                if (tool == PaintTool.BRUSH) addChoice(listOf(ui(R.string.ui_round), ui(R.string.ui_square), ui(R.string.ui_calligraphy)), document.brushTip) { document.brushTip = it }
                if (tool in listOf(PaintTool.RECTANGLE, PaintTool.POLYGON, PaintTool.ELLIPSE, PaintTool.ROUND_RECT,PaintTool.HEART,PaintTool.STAR,PaintTool.ARROW))
                    addChoice(listOf(ui(R.string.ui_outline), ui(R.string.ui_solid_fill), ui(R.string.ui_fill_line)), document.shapeStyle) { document.shapeStyle = it; paintCanvas.invalidate() }
            }
        }
        if (tool in listOf(PaintTool.POLYGON, PaintTool.CURVE, PaintTool.SELECT, PaintTool.LASSO)) {
            options.addView(button(when (tool) { PaintTool.POLYGON -> ui(R.string.ui_finish_polygon); PaintTool.CURVE -> ui(R.string.ui_finish_curve); else -> ui(R.string.ui_commit_selection) }, "apply") {
                paintCanvas.applyPending()
            }, LinearLayout.LayoutParams(-1, dp(48)))
        }
        options.addView(button(ui(R.string.ui_how_to_use), "tool_help") { message(tool.hint) }, LinearLayout.LayoutParams(-1, dp(48)))
        listOf(
            actionIcon(EditIcon.CUT,"clipboard_cut") { cutSelection() },
            actionIcon(EditIcon.COPY,"clipboard_copy") { copySelection() },
            actionIcon(EditIcon.PASTE,"clipboard_paste") { pasteSelection() },
            actionIcon(EditIcon.SELECT_ALL,"select_all") { selectAll() }
        ).chunked(2).forEachIndexed { index, pair ->
            val row = LinearLayout(this).apply { tag = "clipboard_row_$index" }
            pair.forEach { row.addView(it,LinearLayout.LayoutParams(0,dp(48),1f)) }
            options.addView(row,LinearLayout.LayoutParams(-1,dp(48)))
        }
        options.addView(button(ui(R.string.ui_canvas_bounds),"trim_canvas") { trimCanvas() },LinearLayout.LayoutParams(-1,dp(48)))
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
            AlertDialog.Builder(this).setTitle(ui(R.string.ui_tool_option)).setSingleChoiceItems(values.toTypedArray(), selected) { dialog, which ->
                action(which); choice.text = values[which]; dialog.dismiss()
            }.setNegativeButton(ui(R.string.ui_cancel), null).show()
        }
        options.addView(choice, LinearLayout.LayoutParams(-1, dp(48)))
    }

    private fun menuTitle(name: String): String = ui(when(name) {
        "File" -> R.string.ui_menu_file
        "Edit" -> R.string.ui_menu_edit
        "View" -> R.string.ui_menu_view
        "Image" -> R.string.ui_menu_image
        "Colors" -> R.string.ui_menu_colours
        else -> R.string.ui_menu_help
    })

    private fun menuActions(name: String): List<Pair<String, () -> Unit>> = when (name) {
            "File" -> listOf(
                ui(R.string.ui_new) to { confirmReplacement { dimensionsDialog(false, true) } },
                ui(R.string.ui_load_image) to { confirmReplacement { launchOpen(false) } },
                ui(R.string.ui_insert_image_into_canvas) to { launchOpen(true) },
                ui(R.string.ui_catrobat_sticker_gallery) to {startActivityForResult(Intent(this,MediaGalleryActivity::class.java),GALLERY_IMAGE)},
                ui(R.string.ui_save_as_png) to { requestSave(false) },
                ui(R.string.ui_save_as_jpeg) to { requestSave(true) },
                ui(R.string.ui_save_as_jpeg_xl) to { showSaveOptions(ImageFormat.JPEG_XL) },
                ui(R.string.ui_save_and_share) to { showSaveOptions(exportOptions.format,true) },
                ui(R.string.ui_image_assembly) to { openAssembly() }
            ) + if (autosaveBlocked || autosave.recoveryCopies().isNotEmpty()) listOf(ui(R.string.ui_export_recovery_copy) to { requestRecoveryExport() }) else emptyList()
            "Edit" -> listOf(
                ui(R.string.ui_undo) to { undoEdit() },
                ui(R.string.ui_redo) to { redoEdit() },
                ui(R.string.ui_cut) to { cutSelection() },
                ui(R.string.ui_copy) to { copySelection() },
                ui(R.string.ui_paste) to { pasteSelection() },
                ui(R.string.ui_delete_selection) to { if (!document.deleteSelection()) message(ui(R.string.ui_select_an_area_first)) },
                ui(R.string.ui_select_all) to { selectAll() }
            )
            "View" -> listOf(
                ui(R.string.ui_zoom_in) to { paintCanvas.zoomStep(2f) },
                ui(R.string.ui_zoom_out) to { paintCanvas.zoomStep(.5f) },
                ui(R.string.ui_actual_size_100) to { paintCanvas.zoomAt(1f) },
                ui(R.string.ui_fit_image) to { paintCanvas.fit() },
                (if (paintCanvas.grid) ui(R.string.ui_hide_pixel_grid_800) else ui(R.string.ui_show_pixel_grid_800)) to { paintCanvas.grid = !paintCanvas.grid; paintCanvas.invalidate() },
                (if(paintCanvas.cursorMode) ui(R.string.ui_disable_cursor_drawing) else ui(R.string.ui_enable_cursor_drawing)) to { paintCanvas.setCursorMode(!paintCanvas.cursorMode);populateToolOptions(paintCanvas.tool) },
                ui(R.string.ui_magnified_preview) to { showDrawingSettings(true) },
                ui(R.string.ui_drawing_settings) to { showDrawingSettings(false) },
                (if(fullscreen) ui(R.string.ui_show_editor_controls) else ui(R.string.ui_hide_editor_controls)) to { fullscreen=!fullscreen;syncFullscreen() },
                ui(R.string.ui_image_assembly) to { openAssembly() },
                (if(sidebarExpanded) ui(R.string.ui_collapse_toolbox) else ui(R.string.ui_expand_toolbox)) to { sidebarExpanded=!sidebarExpanded;syncPanels() },
                (if(paletteExpanded) ui(R.string.ui_collapse_colour_palette) else ui(R.string.ui_expand_colour_palette)) to { togglePalette() },
                ui(R.string.ui_pinch_and_pan_mode) to { chooseTool(PaintTool.ZOOM) }
            )
            "Image" -> listOf(
                ui(R.string.ui_crop_to_selection) to { if (document.cropSelection()) paintCanvas.fit() else message(ui(R.string.ui_select_an_area_first)) },
                ui(R.string.ui_resize_image) to { dimensionsDialog(true, false) },
                ui(R.string.ui_canvas_size) to { dimensionsDialog(false, false) },
                ui(R.string.ui_flip_horizontal) to { paintCanvas.applyPending(); document.transform(Matrix().apply { setScale(-1f, 1f) }) },
                ui(R.string.ui_flip_vertical) to { paintCanvas.applyPending(); document.transform(Matrix().apply { setScale(1f, -1f) }) },
                ui(R.string.ui_rotate_90_clockwise) to { paintCanvas.applyPending(); document.transform(Matrix().apply { setRotate(90f) }); paintCanvas.fit() },
                ui(R.string.ui_rotate_180) to { paintCanvas.applyPending(); document.transform(Matrix().apply { setRotate(180f) }) },
                ui(R.string.ui_invert_colours) to { paintCanvas.applyPending(); document.invert() },
                ui(R.string.ui_clear_image) to { paintCanvas.applyPending(); document.clear() },
                ui(R.string.ui_trim_expand_canvas_by_touch) to { trimCanvas() }
            )
            "Colors" -> listOf(
                ui(R.string.ui_edit_foreground) to { colourDialog(false) },
                ui(R.string.ui_edit_background) to { colourDialog(true) },
                ui(R.string.ui_swap_foreground_background) to { val old = document.foreground; document.foreground = document.background; document.background = old; updateColours() },
                ui(R.string.ui_reset_to_black_white) to { document.foreground = Color.BLACK; document.background = Color.WHITE; updateColours() }
            )
            else -> listOf(
                ui(R.string.ui_how_to_use) to { showHelp() },
                ui(R.string.ui_about_copyright_licence) to { LegalInfo.showAbout(this) },
                "GNU AGPL licence" to { LegalInfo.showAsset(this, ui(R.string.ui_gnu_affero_general_public_license), "legal/AGPL-3.0.txt") },
                ui(R.string.ui_third_party_notices) to { LegalInfo.showAsset(this, ui(R.string.ui_open_source_credits_and_notices), "legal/THIRD_PARTY_NOTICES.txt") },
                ui(R.string.ui_export_this_version_s_source_code) to { exportSource() },
                ui(R.string.ui_icons_fonts_artwork_credits) to { LegalInfo.showAsset(this, ui(R.string.ui_icons_fonts_artwork_credits), "legal/ASSET_CREDITS.txt") },
                ui(R.string.ui_image_credits) to {showImageCredits()},
                "JPEG XL codec licences" to {LegalInfo.showAsset(this,"JPEG XL codec licences","legal/JPEG_XL_NOTICES.txt")},
                ui(R.string.ui_font_licences) to { LegalInfo.showAsset(this,ui(R.string.ui_font_licences),"legal/FONT_NOTICES.txt") },
                ui(R.string.ui_icon_licences) to { LegalInfo.showAsset(this,ui(R.string.ui_icon_licences_kde_breeze),"legal/ICON_NOTICES.txt") }
            )
        }
    private fun menuActionEnabled(name: String,index: Int) = name!="Edit" || when (index) {
        0 -> document.canUndo || paintCanvas.hasPendingEdit
        1 -> document.canRedo
        else -> true
    }
    private fun showMenu(name: String, anchor: View) {
        val actions=menuActions(name)
        val menu = PopupMenu(this, anchor)
        actions.forEachIndexed { index, action -> menu.menu.add(0, index, index, action.first).isEnabled=menuActionEnabled(name,index) }
        menu.setOnMenuItemClickListener { if (!busy) editAction(actions[it.itemId].second); true }; menu.show()
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

    private fun colourDialog(background: Boolean) {
        AdvancedColourDialog(this, if (background) document.background else document.foreground, background) { colour ->
            setColour(colour,background)
        }.show()
    }

    private fun dimensionsDialog(stretch: Boolean, fresh: Boolean) {
        val column = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(20), dp(6), dp(20), dp(6)) }
        val sizing = DimensionControls(this,ImageDimensions(document.bitmap.width,document.bitmap.height),locked = stretch)
        column.addView(sizing)
        column.addView(label(if (stretch) ui(R.string.ui_scales_the_image_unlock_the_ratio_to_stretch) else ui(R.string.ui_keeps_pixels_at_the_top_left_smaller_canvas), 12f))
        column.addView(label(String.format(java.util.Locale.ROOT, ui(R.string.ui_current_safe_budget_2f_mp), ImageMemoryPolicy.forDevice(this).maxPixels(document.residentPixels) / 1_000_000.0), 12f))
        val dialog = AlertDialog.Builder(this).setTitle(if (fresh) ui(R.string.ui_new_image) else if (stretch) ui(R.string.ui_resize_image_ab28be) else ui(R.string.ui_canvas_size_30460e)).setView(ScrollView(this).apply { addView(column) }).setNegativeButton(ui(R.string.ui_cancel), null).setPositiveButton(ui(R.string.ui_apply), null).create()
        dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
            val size = sizing.dimensions
            if (size == null) sizing.widthInput.error = ui(R.string.ui_enter_positive_dimensions)
            else editAction {
                checkImageSize(size.width,size.height); paintCanvas.applyPending()
                if (fresh) { document.newImage(size.width,size.height); filename = ui(R.string.ui_untitled) } else document.resize(size.width,size.height,stretch)
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
        options.removeAllViews()
        options.addView(label(ui(R.string.ui_canvas_bounds),13f))
        options.addView(label(ui(R.string.ui_drag_out_to_expand_in_to_trim_drag),12f))
        options.addView(label("").apply { tag = "trim_dimensions" })
        options.addView(button(ui(R.string.ui_apply_bounds),"trim_apply") { paintCanvas.applyTrim(); chooseTool(paintCanvas.tool) },LinearLayout.LayoutParams(-1,dp(48)))
        options.addView(button(ui(R.string.ui_cancel),"trim_cancel") { paintCanvas.cancelTrim(); chooseTool(paintCanvas.tool) },LinearLayout.LayoutParams(-1,dp(48)))
        options.addView(button(ui(R.string.ui_fit),"trim_fit") { paintCanvas.fit() },LinearLayout.LayoutParams(-1,dp(48))); updateStatus()
    }
    override fun onKeyShortcut(keyCode: Int, event: android.view.KeyEvent): Boolean {
        if (event.isCtrlPressed && keyCode == android.view.KeyEvent.KEYCODE_A && !busy) { editAction { selectAll() }; return true }
        return super.onKeyShortcut(keyCode,event)
    }

    private fun showTextDialog(x: Float,y: Float) {
        TextStyleDialog(this,textSettings,document.foreground,document.background) { settings,face ->
            editAction {
                document.text(x,y,settings.text,settings.size,face,settings.box,settings.underline,settings.strike,
                    arrayOf(Paint.Align.LEFT,Paint.Align.CENTER,Paint.Align.RIGHT)[settings.alignment],settings.spacing)
                textSettings=settings;scheduleAutosave()
            }
        }.show()
    }

    private fun confirmReplacement(action: () -> Unit) {
        paintCanvas.applyPending()
        if (!document.dirty) { action(); return }
        AlertDialog.Builder(this).setTitle(ui(R.string.ui_save_your_changes)).setMessage(ui(R.string.ui_your_current_image_has_unsaved_changes))
            .setPositiveButton(ui(R.string.ui_save_a5d0d9)) { _, _ -> afterSave = action; requestSave(false) }
            .setNeutralButton(ui(R.string.ui_discard)) { _, _ -> action() }.setNegativeButton(ui(R.string.ui_cancel), null).show()
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
        if(jpeg) showSaveOptions(ImageFormat.JPEG) else {
            shareAfterSave=false;exportOptions=ExportOptions(ImageFormat.PNG);chooseSaveLocation()
        }
    }
    private fun showSaveOptions(format: ImageFormat,share: Boolean=false) {
        val prefs=getSharedPreferences("export",MODE_PRIVATE)
        SaveOptionsDialog(this,ExportOptions(format,prefs.getInt("quality",95),prefs.getBoolean("lossless",true)),share,
            confirm={options ->
                exportOptions=options;shareAfterSave=share
                prefs.edit().putInt("quality",options.quality).putBoolean("lossless",options.lossless).apply()
                chooseSaveLocation()
            },cancel={afterSave=null;shareAfterSave=false}).show()
    }
    private fun chooseSaveLocation() {
        paintCanvas.applyPending()
        val stem=filename.substringBeforeLast('.',filename).ifBlank {ui(R.string.ui_untitled)}
        launchPicker(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE);type=exportOptions.format.mime
            putExtra(Intent.EXTRA_TITLE,stem+exportOptions.format.extension)
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
        if (copies.size==1) choose(copies.first()) else if (copies.isNotEmpty()) AlertDialog.Builder(this)
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
            getSharedPreferences("image-credits",MODE_PRIVATE).edit().putStringSet("sources",(getSharedPreferences("image-credits",MODE_PRIVATE).getStringSet("sources",emptySet()) ?: emptySet())+source).apply()
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
            SAVE_IMAGE -> writeImage(uri)
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
                contentResolver.openInputStream(uri)?.use { source -> cached.outputStream().use { dest ->
                    val buffer = ByteArray(64 * 1024)
                    while (true) {
                        val count = source.read(buffer); if (count < 0) break
                        dest.write(buffer, 0, count)
                    }
                } } ?: throw IOException(ui(R.string.ui_the_selected_provider_did_not_return_any_image))
                val source = ImportedImage(cached,if (asEdit) ui(R.string.ui_assembly_png) else displayName(uri))
                if (deleteAfterCopy) File(uri.path!!).delete()
                temporary = null // The UI/import continuation now owns this cached file.
                runOnUiThread {
                    if (isDestroyed || isFinishing) source.file.delete()
                    else {
                        val plan = ImportPlan.create(source.dimensions,source.dimensions)
                        if (ImageMemoryPolicy.forDevice(this).accepts(plan,document.residentPixels)) decodeImage(source,import,source.dimensions,asEdit)
                        else askToResize(source,import,asEdit = asEdit)
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
            cancel = { resizeDialog = null; source.file.delete(); if (!isDestroyed) endIo() }
        ).show()
    }

    private fun decodeImage(source: ImportedImage, import: Boolean, target: ImageDimensions, asEdit: Boolean = false) {
        worker.execute {
            try {
                val plan = ImportPlan.create(source.dimensions,target)
                ImageMemoryPolicy.forDevice(this).checkImport(plan,document.residentPixels)
                val bitmap = source.decode(plan)
                source.file.delete()
                runOnUiThread {
                    if (!isDestroyed && !isFinishing) {
                        try {
                            if (import) { chooseTool(PaintTool.SELECT); document.paste(bitmap, takeOwnership = true) }
                            else { paintCanvas.cancelPending(); document.replace(bitmap,asEdit); filename = source.name; paintCanvas.fit() }
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
        beginIo()
        val snapshot=document.bitmap
        val options=exportOptions;val sharing=shareAfterSave;shareAfterSave=false
        worker.execute {
            var encoded: File?=null
            try {
                val directory=File(cacheDir,"images").apply {mkdirs()}
                val file=File.createTempFile("AN-Paint-",options.format.extension,directory);encoded=file
                if(options.format==ImageFormat.JPEG_XL) JxlCodec.encode(snapshot,file,options.quality,options.lossless,
                    ImageMemoryPolicy.forDevice(this).workingBytes)
                else file.outputStream().use {
                    if(!snapshot.compress(if(options.format==ImageFormat.JPEG) Bitmap.CompressFormat.JPEG else Bitmap.CompressFormat.PNG,options.quality,it)) throw IOException(ui(R.string.ui_the_encoder_did_not_finish))
                }
                contentResolver.openOutputStream(uri,"wt")?.use {output -> file.inputStream().use {it.copyTo(output)}}
                    ?: throw IOException(ui(R.string.ui_the_selected_location_is_not_writable))
                val name=displayName(uri)
                if(sharing) encoded=null
                runOnUiThread {if(!isDestroyed) {
                    filename=name;document.markSaved();endIo();Toast.makeText(this,ui(R.string.ui_saved, name),Toast.LENGTH_SHORT).show()
                    if(sharing) shareSavedImage(file,options.format)
                    val action=afterSave;afterSave=null;action?.invoke()
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
            if (index >= 0 && cursor.moveToFirst()) return cursor.getString(index) ?: "Image"
        } } catch (_: Exception) { /* Display metadata is optional. */ }
        return uri.lastPathSegment?.substringAfterLast('/') ?: "Image"
    }
    private fun beginIo() { operationsInFlight++; busy = true; lastIoError = null; paintCanvas.isEnabled = false; updateStatus() }
    private fun endIo() { operationsInFlight = (operationsInFlight - 1).coerceAtLeast(0); busy = operationsInFlight > 0; paintCanvas.isEnabled = !busy; updateStatus(); if (!busy && autosaveReady && draftGeneration != savedDraftGeneration && draftGeneration != failedDraftGeneration) { autosaveHandler.removeCallbacks(saveDraft); autosaveHandler.postDelayed(saveDraft,if (stopped) 0 else 1500) } }
    private fun ioFailed(prefix: String, e: Throwable) {
        runOnUiThread { if (!isDestroyed) { afterSave = null; endIo(); lastIoError = "$prefix. ${e.message ?: "Please try a different file or location."}"; message(lastIoError!!) } }
    }
    private fun setColour(colour: Int,background: Boolean) {
        if(background) document.background=colour else document.foreground=colour
        recentColours.add(colour);refreshRecentColours();updateColours()
    }
    private fun refreshRecentColours() {
        recentCells.forEachIndexed { index,cell ->
            val colour=recentColours.colours.getOrNull(index)
            cell.background=GradientDrawable().apply { setColor(colour ?: 0xffe8e7df.toInt());setStroke(dp(2),0xffa0a49f.toInt()) }
            cell.isEnabled=colour!=null
            cell.contentDescription=if(colour==null) ui(R.string.ui_recent_colour_empty, index+1) else String.format(java.util.Locale.ROOT,ui(R.string.ui_recent_colour_d_06x_tap_foreground_hold_background),index+1,colour and 0xffffff)
        }
    }
    private fun showImageCredits() {
        val sources=getSharedPreferences("image-credits",MODE_PRIVATE).getStringSet("sources",emptySet()).orEmpty()
        val text=if(sources.isEmpty()) ui(R.string.ui_no_gallery_images_have_been_inserted) else
            ui(R.string.ui_gallery_artwork_catrobat_and_its_credited_creators_cc)+sources.sorted().joinToString("\n\n")+"\n\n"+MediaGalleryActivity.LICENCE
        LegalInfo.termsDialog(this,ui(R.string.ui_image_credits),text).show()
    }
    private fun showDrawingSettings(preview: Boolean) {
        val column=LinearLayout(this).apply {orientation=LinearLayout.VERTICAL;setPadding(dp(18),dp(8),dp(18),dp(8))}
        fun toggle(title: String,value: Boolean,change: (Boolean)->Unit) {
            column.addView(CheckBox(this).apply {text=title;isChecked=value;setOnCheckedChangeListener {_,on -> change(on);paintCanvas.invalidate();scheduleAutosave()} })
        }
        if(preview) {
            toggle(ui(R.string.ui_show_magnified_drawing_preview),paintCanvas.magnifiedPreview) { paintCanvas.magnifiedPreview=it }
            column.addView(NumericSlider(this,ui(R.string.ui_magnification),(paintCanvas.previewMagnification*100).toInt(),100,400) {paintCanvas.previewMagnification=it/100f})
        } else {
            toggle(ui(R.string.ui_smooth_freehand_strokes),document.strokeSmoothing) { document.strokeSmoothing=it }
            toggle(ui(R.string.ui_smooth_pixel_edges_anti_aliasing),document.antialiasing) { document.antialiasing=it }
            column.addView(label(ui(R.string.ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing)))
        }
        AlertDialog.Builder(this).setTitle(if(preview) ui(R.string.ui_magnified_preview_ea9209) else ui(R.string.ui_drawing_settings_d900c6))
            .setView(ScrollView(this).apply {addView(column)}).setPositiveButton(ui(R.string.ui_done),null).show()
    }
    private fun syncFullscreen() {
        if(!::root.isInitialized) return
        for(i in 0 until root.childCount) root.getChildAt(i).let { it.visibility=if(fullscreen && it.tag!="workspace_overlay") View.GONE else View.VISIBLE }
        sidebar.visibility=if(!fullscreen && sidebarExpanded) View.VISIBLE else View.GONE
        paletteBar.visibility=if(!fullscreen && sidebarExpanded && paletteExpanded) View.VISIBLE else View.GONE
        sidebarToggle.visibility=if(fullscreen) View.GONE else View.VISIBLE
        val workspace=root.findViewWithTag<FrameLayout>("workspace_overlay")
        workspace.findViewWithTag<View>("leave_fullscreen")?.let {workspace.removeView(it)}
        if(fullscreen) workspace.addView(button(ui(R.string.ui_show_controls),"leave_fullscreen") {fullscreen=false;syncFullscreen()},FrameLayout.LayoutParams(-2,dp(48),Gravity.TOP or Gravity.END))
        window.decorView.systemUiVisibility=if(fullscreen) View.SYSTEM_UI_FLAG_FULLSCREEN else View.SYSTEM_UI_FLAG_VISIBLE
    }
    private fun showHelp() = message(ui(R.string.ui_the_arrow_on_the_left_directly_below_the))
    private fun message(text: String) { if (!isFinishing && !isDestroyed) AlertDialog.Builder(this).setTitle("AN Paint").setMessage(text).setPositiveButton(ui(R.string.ui_ok), null).show() }

    private fun scheduleAutosave() {
        if (!autosaveReady || autosaveBlocked || isDestroyed) return
        draftGeneration++;draftStatus=ui(R.string.ui_draft_pending)
        autosaveHandler.removeCallbacks(saveDraft)
        autosaveHandler.postDelayed(saveDraft,if (stopped) 0 else 1500)
    }
    private fun draftMetadata(): JSONObject = JSONObject().apply {
        put("version",1);put("filename",filename);put("dirty",document.dirty)
        put("foreground",document.foreground);put("background",document.background)
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
    override fun onSaveInstanceState(outState: Bundle) { outState.putInt("export_format",exportOptions.format.ordinal);outState.putInt("export_quality",exportOptions.quality);outState.putBoolean("export_lossless",exportOptions.lossless);outState.putBoolean("share_after_save",shareAfterSave); super.onSaveInstanceState(outState) }
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
        resizeDialog?.dismiss();resizeDialog=null
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
