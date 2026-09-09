/* AN Paint additions, 2026-09-07; layout updated 2026-09-08. GNU AGPL-3.0-or-later; no warranty.
 * A drawing workspace in the modified Catrobat/Paintroid distribution.
 */
package org.catrobat.paintroid.classic

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
import org.catrobat.paintroid.MainActivity
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
    private var filename = "Untitled"
    private var saveJpeg = false
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
    private var draftStatus = "Draft not saved yet"
    private val saveDraft = Runnable { saveDraftIfReady() }
    private val cream = 0xffe8e7df.toInt()
    private val ink = 0xff233b4d.toInt()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        autosave=AutosaveStore(filesDir)
        val prefs=getSharedPreferences("classic-ui",MODE_PRIVATE)
        val firstArrowLayout=!prefs.getBoolean("arrow_layout_initialized",false)
        sidebarExpanded=firstArrowLayout || prefs.getBoolean("sidebar_expanded",true)
        paletteExpanded=firstArrowLayout || prefs.getBoolean("palette_expanded",true)
        prefs.edit().putBoolean("arrow_layout_initialized",true).apply()
        document = PaintDocument(historyDirectory = File(cacheDir,"classic-history"), opaqueCanvas=true,
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
            filename=recovered.optString("filename","Recovered image")
            document.foreground=recovered.optInt("foreground",Color.BLACK)
            document.strokeWidth=recovered.optDouble("stroke_width",5.0).toFloat()
            document.cornerRadius=recovered.optDouble("corner_radius",16.0).toFloat().coerceAtLeast(0f)
            document.brushTip=recovered.optInt("brush_tip");document.shapeStyle=recovered.optInt("shape_style")
            document.tolerance=recovered.optDouble("tolerance",0.0).toFloat()
            document.transparentSelection=recovered.optBoolean("skip_background")
            if (recovered.optBoolean("dirty")) document.edited()
            draftStatus="Draft restored";restored=true
        } catch (_: Exception) { recovered=null;preserveFailedDraft("The previous draft could not be restored.") }
          catch (_: OutOfMemoryError) { recovered=null;preserveFailedDraft("The previous draft needs more memory to reopen.") }
        if (!restored) {
            val recovery=File(filesDir,"classic-recovery.png")
            if (recovery.isFile) try {
                val bounds=BitmapFactory.Options().apply { inJustDecodeBounds=true }
                BitmapFactory.decodeFile(recovery.path,bounds);checkImageSize(bounds.outWidth,bounds.outHeight)
                BitmapFactory.decodeFile(recovery.path,BitmapFactory.Options().apply { inMutable=true;inScaled=false })?.let {
                    document.replace(it)
                    val old=getSharedPreferences("classic",MODE_PRIVATE)
                    filename=old.getString("filename","Recovered image") ?: "Recovered image"
                    if (old.getBoolean("dirty",false)) document.edited()
                    restored=true;draftStatus="Draft restored"
                }
            } catch (_: Exception) { } catch (_: OutOfMemoryError) { }
        }
        paintCanvas=PaintCanvas(this,document).apply {
            tag="paint_canvas"
            onStatus={ updateStatus(); scheduleAutosave() }
            onPick={ updateColours();updateStatus();scheduleAutosave() }
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
        savedInstanceState?.let { saveJpeg=it.getBoolean("save_jpeg",false) }
    }

    private fun preserveFailedDraft(reason: String) {
        try {
            autosave.preserveForRecovery()
            recoveryNotice="$reason A separate recovery copy has been kept. Use File > Export recovery copy to save its ZIP. Extract canvas.png from it and load that image to use the normal resize options if needed."
            draftStatus="Previous draft kept for recovery"
        } catch (_: Exception) {
            autosaveBlocked=true
            lastAutosaveError="The previous draft could not be preserved separately."
            draftStatus="Autosave paused · use Save"
            recoveryNotice="$reason Autosave is paused to protect that draft. Use File > Export recovery copy to keep it, and Save as PNG/JPEG to save your current work."
        }
    }

    private fun buildWorkspace() {
        (paintCanvas.parent as? android.view.ViewGroup)?.removeView(paintCanvas)
        toolButtons.clear()
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
        val rail=ScrollView(this).apply { tag="tool_scroll";contentDescription="Toolbox and tool options. Scroll for more." }
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
        syncPanels();updateColours();updateStatus()
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
        sidebarToggle.contentDescription=if (sidebarExpanded) "Collapse toolbox" else "Expand toolbox"
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
        setOnClickListener { if (!busy) editAction(action) else message("Please wait for the current operation.") }
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
            val menu=button("Menu","compact_menu") {}
            menu.setOnClickListener {
                if (busy) return@setOnClickListener
                val popup=PopupMenu(this,menu)
                val commands=mutableMapOf<Int,() -> Unit>()
                listOf("File","Edit","View","Image","Colors","Help").forEachIndexed { group,name ->
                    val submenu=popup.menu.addSubMenu(0,group,group,name)
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
            right.addView(button("Save","save_image") { requestSave(false) },LinearLayout.LayoutParams(dp(56),dp(48)))
            bar.addView(right,FrameLayout.LayoutParams(-2,-1,Gravity.END))
            titleText.gravity=Gravity.CENTER
            bar.addView(titleText,FrameLayout.LayoutParams(-1,-1).apply { leftMargin=dp(150);rightMargin=dp(150) })
            root.addView(bar,LinearLayout.LayoutParams(-1,dp(48)))
        } else {
            val bar=LinearLayout(this).apply { tag="header_bar";gravity=Gravity.CENTER_VERTICAL;setPadding(dp(2),0,dp(2),0);setBackgroundColor(0xff1559a6.toInt()) }
            bar.addView(titleText,LinearLayout.LayoutParams(0,dp(52),1f))
            bar.addView(undoButton,LinearLayout.LayoutParams(dp(44),dp(48)))
            bar.addView(redoButton,LinearLayout.LayoutParams(dp(44),dp(48)))
            bar.addView(button("Save","save_image") { requestSave(false) },LinearLayout.LayoutParams(dp(54),dp(48)))
            root.addView(bar)
            val scroll=HorizontalScrollView(this).apply { tag="menu_bar";isHorizontalScrollBarEnabled=false }
            val menus=LinearLayout(this)
            listOf("File","Edit","View","Image","Colors","Help").forEach { name ->
                val item=button(name,"menu_$name") {};item.setOnClickListener { if (!busy) showMenu(name,item) }
                menus.addView(item,LinearLayout.LayoutParams(dp(if (name=="Colors") 66 else 56),dp(44)))
            }
            scroll.addView(menus);root.addView(scroll,LinearLayout.LayoutParams(-1,dp(44)))
        }
    }

    private fun makePalette(editor: LinearLayout) {
        val row = LinearLayout(this).apply { tag="palette_bar"; gravity = Gravity.CENTER_VERTICAL; setPadding(dp(4), dp(2), dp(4), dp(2)) }; paletteBar=row
        val swatches = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        foregroundButton = button("FG", "foreground_colour") { colourDialog(false) }
        backgroundButton = button("BG", "background_colour") { colourDialog(true) }
        swatches.addView(foregroundButton, LinearLayout.LayoutParams(dp(48), dp(36)))
        swatches.addView(backgroundButton, LinearLayout.LayoutParams(dp(48), dp(36)))
        row.addView(swatches)
        val scroll = HorizontalScrollView(this).apply { contentDescription = "Colour palette. Tap for foreground; hold for background. Scroll for more colours." }
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
                    tag = "colour_$hex"; contentDescription = "Colour #$hex. Tap foreground, hold background."
                    isFocusable = true
                    background = GradientDrawable().apply { setColor(colour); setStroke(dp(2), 0xffa0a49f.toInt()) }
                    setOnClickListener { if (!busy) { document.foreground = colour; updateColours() } }
                    setOnLongClickListener { if (!busy) { document.background = colour; updateColours() }; true }
                }
                strip.addView(swatch, LinearLayout.LayoutParams(dp(36), dp(36)).apply { setMargins(dp(1), dp(1), dp(1), dp(1)) })
            }
            palette.addView(strip)
        }
        scroll.addView(palette); row.addView(scroll, LinearLayout.LayoutParams(0, dp(76), 1f))
        editor.addView(row,LinearLayout.LayoutParams(-1,dp(80)))
    }

    private fun makeStatus() {
        val row = LinearLayout(this).apply { gravity = Gravity.CENTER_VERTICAL; setPadding(dp(7), 0, dp(3), 0) }
        statusText = label("Ready", 11f).apply { maxLines = 2 }
        row.addView(statusText, LinearLayout.LayoutParams(0, dp(44), 1f))
        val zoomRow = LinearLayout(this).apply { gravity = Gravity.CENTER_VERTICAL; tag = "zoom_controls" }
        zoomRow.addView(actionIcon(EditIcon.MINUS, "zoom_out") { paintCanvas.zoomStep(1/1.5f) }, LinearLayout.LayoutParams(dp(40), dp(44)))
        zoomSlider = ZoomSeekBar(this).apply {
            tag = "zoom_slider"; contentDescription = "Canvas zoom"; max = 1000
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
        zoomRow.addView(button("Fit","zoom_fit_view") { paintCanvas.fit() }.apply {
            contentDescription="Fit entire canvas in view"
        },LinearLayout.LayoutParams(dp(44),dp(44)))
        row.addView(zoomRow)
        root.addView(row)
    }

    private fun updateStatus() {
        if (!::statusText.isInitialized) return
        statusText.text = if (busy) (if (autosaving) "Autosaving draft…" else "Working…") else "${paintCanvas.tool.label} · ${paintCanvas.zoomLabel()}\n${document.bitmap.width} × ${document.bitmap.height} px · $draftStatus"
        if (::zoomSlider.isInitialized) {
            syncingZoom = true; zoomSlider.progress = paintCanvas.sliderForZoom(); syncingZoom = false
            zoomSlider.isEnabled = !busy
            zoomSlider.contentDescription = "Canvas zoom ${paintCanvas.zoomLabel()}"
        }
        if (::options.isInitialized) options.findViewWithTag<TextView>("selection_dimensions")?.text=document.selection?.let {
            String.format(java.util.Locale.ROOT,"%.0f × %.0f px\n%.1f°",it.rect.width(),it.rect.height(),it.rotation)
        } ?: "Select an area"
        if (::options.isInitialized) options.findViewWithTag<TextView>("trim_dimensions")?.text = paintCanvas.trim?.rect?.let { "${it.width()} × ${it.height()} px" } ?: ""
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
        foregroundButton.contentDescription = "Foreground ${String.format("#%06X", document.foreground and 0xffffff)}. Edit colour."
        backgroundButton.contentDescription = "Background ${String.format("#%06X", document.background and 0xffffff)}. Edit colour."
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
                options.addView(label("Corners and edges resize. Round handle rotates.",11f))
                options.addView(label("").apply { tag="selection_dimensions" })
                options.addView(CheckBox(this).apply {
                    tag="selection_lock_aspect";text="Lock proportions";textSize=11f;isChecked=paintCanvas.lockSelectionAspect
                    setOnCheckedChangeListener { _,checked -> paintCanvas.lockSelectionAspect=checked;scheduleAutosave() }
                },LinearLayout.LayoutParams(-1,dp(48)))
                options.addView(button(if (document.transparentSelection) "Skip BG colour ✓" else "Include BG colour ✓", "selection_mode") {
                    document.transparentSelection = !document.transparentSelection
                    // Do not change tools here: a floating selection must remain editable.
                    (options.findViewWithTag<View>("selection_mode") as Button).text = if (document.transparentSelection) "Skip BG colour ✓" else "Include BG colour ✓"
                    paintCanvas.invalidate()
                }, LinearLayout.LayoutParams(-1, dp(52)))
            }
            PaintTool.FILL -> addSlider("Tolerance", document.tolerance.toInt(), 100) { document.tolerance = it.toFloat() }
            PaintTool.ZOOM -> {
                options.addView(label("Pinch to zoom. Drag to pan.",12f))
                options.addView(button("Draw again", "navigate_draw") { chooseTool(drawingTool) },LinearLayout.LayoutParams(-1,dp(48)))
                options.addView(button("100%", "zoom_actual") { paintCanvas.zoomAt(1f) },LinearLayout.LayoutParams(-1,dp(44)))
                options.addView(button("Fit", "zoom_fit") { paintCanvas.fit() }, LinearLayout.LayoutParams(-1, dp(44)))
            }
            PaintTool.PENCIL -> options.addView(label("1 px", 12f))
            PaintTool.TEXT -> options.addView(label("Tap canvas\nto type", 12f))
            PaintTool.PICKER -> options.addView(label("Tap a pixel", 12f))
            else -> {
                addSlider("Size (px)", document.strokeWidth.toInt(), 64, 1) { document.strokeWidth = it.toFloat() }
                if (tool == PaintTool.ROUND_RECT) addSlider("Radius (px)",document.cornerRadius.toInt(),
                    maxOf(64,minOf(document.bitmap.width,document.bitmap.height)/2,document.cornerRadius.toInt()),tagName="corner_radius") {
                    document.cornerRadius=it.toFloat();paintCanvas.invalidate()
                }
                if (tool == PaintTool.BRUSH) addChoice(listOf("Round", "Square", "Calligraphy"), document.brushTip) { document.brushTip = it }
                if (tool in listOf(PaintTool.RECTANGLE, PaintTool.POLYGON, PaintTool.ELLIPSE, PaintTool.ROUND_RECT))
                    addChoice(listOf("Outline", "Solid fill", "Fill + line"), document.shapeStyle) { document.shapeStyle = it; paintCanvas.invalidate() }
            }
        }
        if (tool in listOf(PaintTool.POLYGON, PaintTool.CURVE, PaintTool.SELECT, PaintTool.LASSO)) {
            options.addView(button(when (tool) { PaintTool.POLYGON -> "Finish polygon"; PaintTool.CURVE -> "Finish curve"; else -> "Commit selection" }, "apply") {
                paintCanvas.applyPending()
            }, LinearLayout.LayoutParams(-1, dp(48)))
        }
        options.addView(button("How to use", "tool_help") { message(tool.hint) }, LinearLayout.LayoutParams(-1, dp(48)))
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
        options.addView(button("Canvas bounds","trim_canvas") { trimCanvas() },LinearLayout.LayoutParams(-1,dp(48)))
        updateStatus()
    }

    private fun addSlider(name: String, value: Int, maximum: Int, minimum: Int = 0, tagName: String? = null, action: (Int) -> Unit) {
        val readout = label("$name: $value", 11f); options.addView(readout)
        options.addView(SeekBar(this).apply {
            tag=tagName;contentDescription = name; max = maximum - minimum; progress = value - minimum
            setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
                override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) { readout.text = "$name: ${progress + minimum}"; action(progress + minimum);paintCanvas.invalidate();scheduleAutosave() }
                override fun onStartTrackingTouch(seekBar: SeekBar?) = Unit
                override fun onStopTrackingTouch(seekBar: SeekBar?) = Unit
            })
        }, LinearLayout.LayoutParams(-1, dp(44)))
    }
    private fun addChoice(values: List<String>, selected: Int, action: (Int) -> Unit) {
        val choice = button(values[selected], "tool_option") {}
        choice.setOnClickListener {
            AlertDialog.Builder(this).setTitle("Tool option").setSingleChoiceItems(values.toTypedArray(), selected) { dialog, which ->
                action(which); choice.text = values[which]; dialog.dismiss()
            }.setNegativeButton("Cancel", null).show()
        }
        options.addView(choice, LinearLayout.LayoutParams(-1, dp(48)))
    }

    private fun menuActions(name: String): List<Pair<String, () -> Unit>> = when (name) {
            "File" -> listOf(
                "New…" to { confirmReplacement { dimensionsDialog(false, true) } },
                "Load image…" to { confirmReplacement { launchOpen(false) } },
                "Paste from image…" to { launchOpen(true) },
                "Save as PNG…" to { requestSave(false) },
                "Save as JPEG…" to { requestSave(true) },
                "Image assembly…" to { openAssembly() }
            ) + if (autosaveBlocked || autosave.recoveryCopies().isNotEmpty()) listOf("Export recovery copy…" to { requestRecoveryExport() }) else emptyList()
            "Edit" -> listOf(
                "Undo" to { undoEdit() },
                "Redo" to { redoEdit() },
                "Cut" to { cutSelection() },
                "Copy" to { copySelection() },
                "Paste" to { pasteSelection() },
                "Delete selection" to { if (!document.deleteSelection()) message("Select an area first.") },
                "Select all" to { selectAll() }
            )
            "View" -> listOf(
                "Zoom in" to { paintCanvas.zoomStep(2f) },
                "Zoom out" to { paintCanvas.zoomStep(.5f) },
                "Actual size (100%)" to { paintCanvas.zoomAt(1f) },
                "Fit image" to { paintCanvas.fit() },
                "${if (paintCanvas.grid) "Hide" else "Show"} pixel grid (800%+)" to { paintCanvas.grid = !paintCanvas.grid; paintCanvas.invalidate() },
                "Original Pocket Paint editor…" to { showOriginalEditor() },
                "Image assembly…" to { openAssembly() },
                "${if (sidebarExpanded) "Collapse" else "Expand"} toolbox" to { sidebarExpanded=!sidebarExpanded;syncPanels() },
                "${if (paletteExpanded) "Collapse" else "Expand"} colour palette" to { togglePalette() },
                "Pinch and pan mode" to { chooseTool(PaintTool.ZOOM) }
            )
            "Image" -> listOf(
                "Crop to selection" to { if (document.cropSelection()) paintCanvas.fit() else message("Select an area first.") },
                "Resize image…" to { dimensionsDialog(true, false) },
                "Canvas size…" to { dimensionsDialog(false, false) },
                "Flip horizontal" to { paintCanvas.applyPending(); document.transform(Matrix().apply { setScale(-1f, 1f) }) },
                "Flip vertical" to { paintCanvas.applyPending(); document.transform(Matrix().apply { setScale(1f, -1f) }) },
                "Rotate 90° clockwise" to { paintCanvas.applyPending(); document.transform(Matrix().apply { setRotate(90f) }); paintCanvas.fit() },
                "Rotate 180°" to { paintCanvas.applyPending(); document.transform(Matrix().apply { setRotate(180f) }) },
                "Invert colours" to { paintCanvas.applyPending(); document.invert() },
                "Clear image" to { paintCanvas.applyPending(); document.clear() },
                "Trim / expand canvas by touch…" to { trimCanvas() }
            )
            "Colors" -> listOf(
                "Edit foreground…" to { colourDialog(false) },
                "Edit background…" to { colourDialog(true) },
                "Swap foreground / background" to { val old = document.foreground; document.foreground = document.background; document.background = old; updateColours() },
                "Reset to black / white" to { document.foreground = Color.BLACK; document.background = Color.WHITE; updateColours() }
            )
            else -> listOf(
                "How to use" to { showHelp() },
                "About, copyright & licence" to { LegalInfo.showAbout(this) },
                "GNU AGPL licence" to { LegalInfo.showAsset(this, "GNU Affero General Public License", "legal/AGPL-3.0.txt") },
                "Third-party notices" to { LegalInfo.showAsset(this, "Open-source credits and notices", "legal/THIRD_PARTY_NOTICES.txt") },
                "Export this version's source code…" to { exportSource() },
                "Icons, fonts & artwork credits" to { LegalInfo.showAsset(this, "Icons, fonts & artwork credits", "legal/ASSET_CREDITS.txt") },
                "Font licences" to { LegalInfo.showAsset(this,"Font licences","legal/FONT_NOTICES.txt") },
                "Icon licences" to { LegalInfo.showAsset(this,"Icon licences — KDE Breeze","legal/ICON_NOTICES.txt") }
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

    private fun cutSelection() { if (!document.cutSelection()) message("Select an area first.") }
    private fun copySelection() { if (!document.copySelection()) message("Select an area first.") }
    private fun pasteSelection() {
        chooseTool(PaintTool.SELECT)
        if (document.paste()) selectAfterPaste() else message("Copy an area or use File › Paste from image.")
    }

    private fun editAction(action: () -> Unit): Boolean {
        if (autosaving) { message("The draft is saving. Try again shortly.");return false }
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
        message(if (error is ImageSizeException) error.message!! else if (error is OutOfMemoryError) "There is not enough memory for this operation at the original resolution. No automatic resizing was applied."
            else "Could not complete the edit. ${error.message ?: "Please try again."}")
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
            if (background) document.background = colour else document.foreground = colour
            updateColours()
        }.show()
    }

    private fun dimensionsDialog(stretch: Boolean, fresh: Boolean) {
        val column = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(20), dp(6), dp(20), dp(6)) }
        val sizing = DimensionControls(this,ImageDimensions(document.bitmap.width,document.bitmap.height),locked = stretch)
        column.addView(sizing)
        column.addView(label(if (stretch) "Scales the image. Unlock the ratio to stretch width and height independently." else "Keeps pixels at the top left. Smaller canvas dimensions discard pixels beyond the right/bottom edge; Undo restores them.", 12f))
        column.addView(label(String.format(java.util.Locale.ROOT, "Current safe budget: %.2f MP.", ImageMemoryPolicy.forDevice(this).maxPixels(document.residentPixels) / 1_000_000.0), 12f))
        val dialog = AlertDialog.Builder(this).setTitle(if (fresh) "New image" else if (stretch) "Resize image" else "Canvas size").setView(ScrollView(this).apply { addView(column) }).setNegativeButton("Cancel", null).setPositiveButton("Apply", null).create()
        dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
            val size = sizing.dimensions
            if (size == null) sizing.widthInput.error = "Enter positive dimensions."
            else editAction {
                checkImageSize(size.width,size.height); paintCanvas.applyPending()
                if (fresh) { document.newImage(size.width,size.height); filename = "Untitled" } else document.resize(size.width,size.height,stretch)
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
        options.addView(label("Canvas bounds",13f))
        options.addView(label("Drag out to expand, in to trim. Drag inside to move the bounds. Pinch or Fit for more space. BG fills new space.",12f))
        options.addView(label("").apply { tag = "trim_dimensions" })
        options.addView(button("Apply bounds","trim_apply") { paintCanvas.applyTrim(); chooseTool(paintCanvas.tool) },LinearLayout.LayoutParams(-1,dp(48)))
        options.addView(button("Cancel","trim_cancel") { paintCanvas.cancelTrim(); chooseTool(paintCanvas.tool) },LinearLayout.LayoutParams(-1,dp(48)))
        options.addView(button("Fit","trim_fit") { paintCanvas.fit() },LinearLayout.LayoutParams(-1,dp(48))); updateStatus()
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
        AlertDialog.Builder(this).setTitle("Save your changes?").setMessage("Your current image has unsaved changes.")
            .setPositiveButton("Save…") { _, _ -> afterSave = action; requestSave(false) }
            .setNeutralButton("Discard") { _, _ -> action() }.setNegativeButton("Cancel", null).show()
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
            message("Android could not find a file picker. Enable the Files or Documents app in Android settings, then try again.")
        } catch (e: SecurityException) { afterSave = null; message("Android blocked the file picker: ${e.message}") }
    }

    private fun requestSave(jpeg: Boolean) {
        paintCanvas.applyPending(); saveJpeg = jpeg
        val stem = filename.substringBeforeLast('.', filename).ifBlank { "Untitled" }
        launchPicker(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE); type = if (jpeg) "image/jpeg" else "image/png"
            putExtra(Intent.EXTRA_TITLE, stem + if (jpeg) ".jpg" else ".png")
        }, SAVE_IMAGE)
    }

    fun exportSource() {
        launchPicker(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE); type = "application/zip"; putExtra(Intent.EXTRA_TITLE, "AN-Paint-source.zip")
        }, EXPORT_SOURCE)
    }

    private fun requestRecoveryExport() {
        val copies=if (autosaveBlocked) listOf(File(autosave.file.path+".bak").takeIf { it.isFile } ?: autosave.file) else autosave.recoveryCopies()
        fun choose(file: File) {
            recoveryExport=file
            launchPicker(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                addCategory(Intent.CATEGORY_OPENABLE);type="application/zip";putExtra(Intent.EXTRA_TITLE,"AN-Paint-recovery-${file.lastModified()}.zip")
            },EXPORT_RECOVERY)
        }
        if (copies.size==1) choose(copies.first()) else if (copies.isNotEmpty()) AlertDialog.Builder(this)
            .setTitle("Export recovery copy").setItems(copies.map { java.text.DateFormat.getDateTimeInstance().format(java.util.Date(it.lastModified())) }.toTypedArray()) { _,i -> choose(copies[i]) }
            .setNegativeButton("Cancel",null).show()
    }

    private fun openAssembly() {
        paintCanvas.applyPending()
        startActivityForResult(Intent(this,AssemblyActivity::class.java).putExtra("resident_pixels",document.residentPixels),ASSEMBLY_IMAGE)
    }

    public override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK) { if (requestCode == SAVE_IMAGE) afterSave = null; return }
        if (requestCode == ASSEMBLY_IMAGE) {
            val name = data?.getStringExtra("assembly_output")
            val file = name?.let { File(filesDir,it) }
            if (file == null || file.parentFile != filesDir || !file.name.startsWith("assembly-output-") || !file.isFile) { message("The assembly output is unavailable. Reopen Image assembly and try again."); return }
            readImage(Uri.fromFile(file),false,asEdit = true,deleteAfterCopy = true); return
        }
        val uri = data?.data ?: data?.clipData?.getItemAt(0)?.uri
        if (uri == null) { message("The picker returned no file. Please choose the file again."); afterSave = null; return }
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
                } } ?: throw IOException("The selected provider did not return any image data.")
                val source = ImportedImage(cached,if (asEdit) "Assembly.png" else displayName(uri))
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
            } catch (e: Exception) { ioFailed("Could not open image", e) }
            catch (e: OutOfMemoryError) { ioFailed("Not enough memory to inspect this image", e) }
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
                            ioFailed("Could not open image", error)
                        } catch (error: OutOfMemoryError) {
                            if (document.bitmap !== bitmap && document.selection?.image !== bitmap) bitmap.recycle()
                            ioFailed("Not enough memory to finish opening this image", error)
                        }
                    } else bitmap.recycle()
                }
            } catch (_: ImageSizeException) {
                // Device memory may change while the user considers the proposed size.
                runOnUiThread { askToResize(source,import,target,asEdit) }
            } catch (_: OutOfMemoryError) {
                // A budget is an estimate, not a guarantee. Offer a smaller copy after an allocation failure too.
                runOnUiThread { askToResize(source,import,target,asEdit) }
            } catch (e: Exception) { source.file.delete(); ioFailed("Could not open image", e) }
        }
    }

    private fun writeImage(uri: Uri) {
        if (saveJpeg) { try { checkImageSize(document.bitmap.width, document.bitmap.height) } catch (error: ImageSizeException) { afterSave = null; editFailed(error); return } }
        beginIo()
        val snapshot = document.bitmap // Editing stays locked until encoding completes.
        worker.execute {
            var outputImage: Bitmap? = null
            try {
                outputImage = if (saveJpeg) Bitmap.createBitmap(snapshot.width, snapshot.height, Bitmap.Config.ARGB_8888).apply {
                    eraseColor(Color.WHITE); Canvas(this).drawBitmap(snapshot, 0f, 0f, null)
                } else snapshot
                contentResolver.openOutputStream(uri, "wt")?.use {
                    if (!outputImage!!.compress(if (saveJpeg) Bitmap.CompressFormat.JPEG else Bitmap.CompressFormat.PNG, 95, it)) throw IOException("The encoder did not finish.")
                } ?: throw IOException("The selected location is not writable.")
                val name = displayName(uri)
                runOnUiThread { if (!isDestroyed) {
                    filename = name; document.markSaved(); endIo(); Toast.makeText(this, "Saved $name", Toast.LENGTH_SHORT).show()
                    val action = afterSave; afterSave = null; action?.invoke()
                } }
            } catch (e: Exception) { ioFailed("Could not save image", e) }
            catch (e: OutOfMemoryError) { ioFailed("Not enough memory to save in this format. Try PNG", e) }
            finally { if (outputImage !== snapshot) outputImage?.recycle() }
        }
    }

    private fun exportSourceTo(uri: Uri) {
        beginIo()
        worker.execute {
            try {
                assets.open(SOURCE_ASSET).use { source -> contentResolver.openOutputStream(uri, "wt")?.use { source.copyTo(it) } ?: throw IOException("This location is not writable.") }
                runOnUiThread { if (!isDestroyed) { endIo(); message("Source code exported, including build scripts and licence notices.") } }
            } catch (e: Exception) { ioFailed("Could not export source code", e) }
        }
    }

    private fun exportRecoveryTo(uri: Uri) {
        val file=recoveryExport ?: return
        beginIo()
        worker.execute {
            try {
                file.inputStream().use { source -> contentResolver.openOutputStream(uri,"wt")?.use { source.copyTo(it) } ?: throw IOException("This location is not writable.") }
                runOnUiThread { if (!isDestroyed) { endIo();message("Recovery copy exported. Extract canvas.png from the ZIP and open it with File > Load image. The ZIP also contains draft settings and any floating selection.") } }
            } catch (e: Exception) { ioFailed("Could not export the recovery copy",e) }
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
    private fun showOriginalEditor() {
        AlertDialog.Builder(this).setTitle("Original Pocket Paint editor")
            .setMessage("Opens the retained editor with layers, extra brushes and Pocket Paint / OpenRaster projects. To edit this canvas there, save it first, then load the saved image in that editor.")
            .setPositiveButton("Open editor") { _, _ -> startActivity(Intent(this, MainActivity::class.java)) }.setNegativeButton("Cancel", null).show()
    }
    private fun showHelp() = message("The arrow on the left directly below the toolbar collapses or restores the sidebar: up to collapse, down to expand. Both panels start expanded on the first launch of this layout; later choices are remembered. In landscape, the top controls share one row with the filename centred; Menu opens File, Edit, View, Image, Colors and Help, each with an Android submenu arrow.\n\nThe FG/BG colour indicator stays fixed at the bottom of the sidebar. The palette opens directly to its right on the same row. Its arrow is on the right edge: left to collapse the palette, right to expand it. Collapsing gives the canvas more height without moving the indicator. Tapping the colour box also toggles the palette. Tap a swatch for foreground or hold for background. FG/BG opens Palette, Honeycomb and Advanced. Advanced has spectrum, wheel, RGB, HSV, HSL and six-digit hex controls. Custom colours start with Pale Violet #5B67FF, Gold #FFD700, Silver #C0C0C0 and Copper #B87333. Hold a custom swatch to replace it. The main editor uses opaque colours; transparent imports are placed onto the current BG colour. Original source files are unchanged.\n\nNavigate replaces the magnifying-glass tool: drag with one finger to pan, pinch with two fingers to zoom and pan. Tap Navigate again or Draw again to return to drawing. Two-finger navigation also works in drawing tools without leaving paint marks. The bottom-right slider has a centre line at 100%. Zoom in/out buttons stop at 100% when a step would cross it; press again to continue. The adjacent Fit button fits the canvas into the view. View also provides 100% and a pixel grid.\n\nAutosave records the current draft after a short editing pause, and when you leave the app. The status shows Draft saved or an autosave error. Reopening restores the draft, filename, tool settings, floating selection and unfinished geometry. Autosave keeps a private working draft. File > Save as PNG/JPEG exports a file to your chosen location; the filename star means that exported file has unsaved changes. Source images are never overwritten by autosave.\n\nSelections: draw a rectangle or free-form outline. Drag inside to move, drag a square corner or edge midpoint to resize, or drag the round Rotate handle to rotate. Lock proportions is on by default; switch it off to stretch width and height independently. Edge handles resize along the selected side. Free-form selections keep their selected shape within the transform box, including after rotation and autosave. The dimensions and angle appear in the sidebar. Commit selection applies the result as one undoable selection edit; autosave retains unfinished transforms. Copy, Cut and Crop to selection use the transformed image. Select all is in the second row of edit icons, and Ctrl+A works on an external keyboard. Cut/Copy and Paste/Select all form two rows below How to use. Include BG colour / Skip BG colour controls the classic background-colour selection mode.\n\nCanvas bounds: drag handles inward to trim or outward to expand on any side, then Apply bounds. New space uses BG; existing pixels are not scaled. Cancel and Undo are available. Resize image, Canvas size and New image also accept Pixels or Percent with an optional aspect lock.\n\nCurve: draw a line and drag twice to bend it. Polygon: tap vertices, then double-tap the final vertex to close it, or use Finish polygon. Rounded rectangle: set Radius (px) with its slider; each shape limits the radius to half its shorter side. Text: tap the canvas, choose a font displayed in its own style and use the live preview. Options include size, bold, italic, underline, strikethrough, alignment, line spacing and a BG text box. Ten additional fonts are bundled; Font licences has their credits and full terms.\n\nFile loads images through Android's picker. Images within the device memory budget load at original resolution. If needed, a resize-choice dialog shows dimensions, pixel count and memory estimates, with Pixels/Percent sizing and optional aspect lock. The original file stays unchanged.\n\nFile or View > Image assembly opens a separate workspace for up to 20 images. Sort thumbnails by filename or time. Crop one image or batch-crop several. Same width / Same height normalizes all loaded images while preserving aspect ratios. Drag thumbnails or placed images to snap right/top aligned or bottom/left aligned. Unplace removes just the selected placement and closes the gap. Show all changes view zoom. Save PNG exports the assembly; Edit in Paint transfers it as an undoable edit. The original Pocket Paint editor remains under View for layers and project formats.\n\nHelp includes original copyright, asset/font credits, full licence text and this version's complete source. Licence text scrolls independently of the fixed Copy all, Other terms and Done buttons.")
    private fun message(text: String) { if (!isFinishing && !isDestroyed) AlertDialog.Builder(this).setTitle("AN Paint").setMessage(text).setPositiveButton("OK", null).show() }

    private fun scheduleAutosave() {
        if (!autosaveReady || autosaveBlocked || isDestroyed) return
        draftGeneration++;draftStatus="Draft pending"
        autosaveHandler.removeCallbacks(saveDraft)
        autosaveHandler.postDelayed(saveDraft,if (stopped) 0 else 1500)
    }
    private fun draftMetadata(): JSONObject = JSONObject().apply {
        put("version",1);put("filename",filename);put("dirty",document.dirty)
        put("foreground",document.foreground);put("background",document.background)
        put("corner_radius",document.cornerRadius.toDouble());put("stroke_width",document.strokeWidth.toDouble());put("brush_tip",document.brushTip);put("shape_style",document.shapeStyle)
        put("tolerance",document.tolerance.toDouble());put("skip_background",document.transparentSelection)
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
                if (failure==null) { draftStatus="Draft saved";lastAutosaveError=null }
                else { failedDraftGeneration=generation;lastAutosaveError=failure.message;draftStatus="Autosave failed · use Save" }
                endIo()
            } }
        }
    }
    override fun onSaveInstanceState(outState: Bundle) { outState.putBoolean("save_jpeg", saveJpeg); super.onSaveInstanceState(outState) }
    override fun onStart() { super.onStart();stopped=false }
    override fun onStop() {
        super.onStop();stopped=true
        if (::document.isInitialized && autosaveReady) {
            if (!busy) paintCanvas.pauseGesture()
            scheduleAutosave();autosaveHandler.removeCallbacks(saveDraft);saveDraftIfReady()
        }
    }
    override fun onBackPressed() { if (!busy) confirmReplacement { finish() } }
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
