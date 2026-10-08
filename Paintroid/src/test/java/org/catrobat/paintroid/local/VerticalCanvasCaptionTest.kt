/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.LocaleManager
import android.content.Context
import android.content.res.Resources
import android.graphics.*
import android.os.LocaleList
import android.view.View
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.util.Locale
import kotlin.math.max
import kotlin.math.min

/** Native pixels from the real Views, compared with a renderer independent of the caption helper. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w420dp-h680dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class VerticalCanvasCaptionTest {
    private val verticalTags=listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")
    private val horizontalTags=listOf("en-001","ar","vi-Hani","wuu-Hans")
    private lateinit var application: Context
    private lateinit var originalLocale: Locale
    private lateinit var originalResources: Resources
    private lateinit var originalApplicationLocales: LocaleList
    private lateinit var originalPreferences: Map<String,*>
    private val directories=mutableListOf<File>()

    @Before fun rememberLanguageState() {
        application=RuntimeEnvironment.getApplication()
        originalLocale=Locale.getDefault()
        originalResources=PaintApplication.currentResources
        originalApplicationLocales=requireNotNull(application.getSystemService(LocaleManager::class.java)).applicationLocales
        originalPreferences=application.getSharedPreferences("app-language",0).all.toMap()
    }

    @After fun restoreLanguageState() {
        requireNotNull(application.getSystemService(LocaleManager::class.java)).applicationLocales=originalApplicationLocales
        val edit=application.getSharedPreferences("app-language",0).edit().clear()
        originalPreferences.forEach { (key,value) -> when(value) {
            is String -> edit.putString(key,value)
            is Boolean -> edit.putBoolean(key,value)
            is Int -> edit.putInt(key,value)
            is Long -> edit.putLong(key,value)
            is Float -> edit.putFloat(key,value)
            is Set<*> -> edit.putStringSet(key,value.filterIsInstance<String>().toSet())
            else -> Unit
        } }
        edit.commit()
        PaintApplication.currentResources=originalResources
        Locale.setDefault(originalLocale)
        directories.forEach {it.deleteRecursively()}
    }

    private fun language(tag: String): Context {
        AppLanguage.select(application,tag)
        val context=AppLanguage.wrap(application)
        PaintApplication.currentResources=context.resources
        assertEquals(Locale.forLanguageTag(tag),Locale.getDefault())
        assertEquals(Locale.forLanguageTag(tag),context.resources.configuration.locales[0])
        assertEquals(context.getString(R.string.ui_rotate),ui(R.string.ui_rotate))
        return context
    }

    private fun directory(): File=File.createTempFile("vertical-caption-","",application.cacheDir).also {
        assertTrue(it.delete());assertTrue(it.mkdir());directories.add(it)
    }

    @Test fun emptyAssemblyUsesNativeVerticalColumnsInPortraitAndShallowLandscape() {
        for(tag in verticalTags) {
            val context=language(tag)
            for((width,height) in listOf(420 to 680,780 to 180)) {
                val assembly=ImageAssembly(directory())
                val board=AssemblyCanvas(context,assembly) {null}.apply {layout(0,0,width,height)}
                val actual=render(board)
                val expected=assemblyReference(board,false)
                val oldHorizontal=assemblyReference(board,true)
                try {
                    assertPixels("assembly-$tag-$width-$height",expected,actual)
                    savePreview("assembly-$tag-$width-$height",actual)
                    assertFalse("$tag must reject the old horizontal instruction",actual.sameAs(oldHorizontal))
                    assertTrue("Instruction must contain visible ink",pixels(actual).any {it!=EditorColours.surfaceDim})
                    // Empty-state text is viewport UI, before the assembly's pan and zoom.
                    setFloat(board,"panX",-9000f);setFloat(board,"panY",5000f);setFloat(board,"zoom",.000001f)
                    val moved=render(board)
                    try {assertPixels("assembly-fixed-$tag-$width",actual,moved)} finally {moved.recycle()}
                    assertTrue(assembly.images.isEmpty());assertFalse(assembly.canUndo);assertFalse(assembly.canRedo)
                } finally {actual.recycle();expected.recycle();oldHorizontal.recycle()}
            }
        }
    }

    @Test fun horizontalAssemblyAndRotationCaptionsKeepTheirLegacyNativePixels() {
        for(tag in horizontalTags) {
            val context=language(tag)
            assertEquals(TextDirection.HORIZONTAL,VerticalText.uiDirection())
            val board=AssemblyCanvas(context,ImageAssembly(directory())) {null}.apply {layout(0,0,720,420)}
            val actual=render(board);val expected=assemblyReference(board,true)
            try {assertPixels("horizontal-assembly-$tag",expected,actual)} finally {actual.recycle();expected.recycle()}
            withDocument(context) {canvas,document ->
                document.select(RectF(80f,70f,240f,160f));canvas.fit()
                assertCanvasReference("horizontal-rotation-$tag",canvas,legacyCaption=true)
            }
        }
    }

    @Test fun assemblyInstructionFollowsEmptyUnplacedSelectedPlacedAndClearedStates() {
        val context=language("mnc-Mong")
        val assembly=ImageAssembly(directory())
        val thumbnail=Bitmap.createBitmap(40,30,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.GREEN)}
        val board=AssemblyCanvas(context,assembly) {thumbnail}.apply {layout(0,0,420,680)}
        val empty=render(board)
        try {
            val file=File(assembly.directory,"source.image")
            file.outputStream().use {assertTrue(thumbnail.compress(Bitmap.CompressFormat.PNG,100,it))}
            assembly.add(listOf(AssemblyImage("one",file,"one.png",null,ImageDimensions(40,30))))
            board.refresh()
            val unplaced=render(board)
            try {assertPixels("assembly-unplaced",empty,unplaced)} finally {unplaced.recycle()}
            board.select("one")
            assertNotNull(board.selectedId);assertTrue(assembly.layout().isEmpty())
            assertAssemblyDrawingDoesNotChangeState(board)
            assertAssemblyHasNoInstruction(board,"selected")
            assembly.place("one",Attachment(null,null));board.select(null)
            assertFalse(assembly.layout().isEmpty())
            assertAssemblyDrawingDoesNotChangeState(board)
            assertAssemblyHasNoInstruction(board,"placed")
            assembly.clear();board.refresh()
            assertNull(board.selectedId)
            val cleared=render(board)
            try {assertPixels("assembly-cleared",empty,cleared)} finally {cleared.recycle()}
        } finally {empty.recycle();thumbnail.recycle()}
    }

    @Test fun everyVerticalRotationProfileMatchesTheNativeReferenceAtFitWithoutEditingTheDocument() {
        for(tag in verticalTags) withDocument(language(tag)) {board,document ->
            document.select(RectF(80f,70f,240f,160f));board.fit()
            assertCanvasReference("rotation-fit-$tag",board,saveSuccess=true)
        }
    }

    @Test fun rotationCaptionsStayInScreenPixelsAtBothSidesAndAllViewportEdges() {
        // Five useful scenes per direction, rather than a locale x edge x zoom x grid product.
        val scenes=listOf(Triple("centre",.25f,false),Triple("left",1f,true),Triple("right",2f,false),
            Triple("top",4f,true),Triple("bottom",.5f,true))
        for(tag in listOf("en-XV","qaa-Zsye-XV")) withDocument(language(tag)) {board,document ->
            document.select(RectF(80f,70f,240f,160f))
            val referenceSize=caption(board).bounds
            for((edge,zoom,grid) in scenes) {
                board.grid=grid;board.zoomAt(zoom)
                val d=board.resources.displayMetrics.density
                val right=board.width-20*d;val bottom=board.height-20*d
                val screen=when(edge) {
                    "left" -> PointF(22*d,bottom/2)
                    "right" -> PointF(right-22*d,bottom/2)
                    "top" -> PointF(right/2,22*d)
                    "bottom" -> PointF(right/2,bottom-22*d)
                    else -> PointF(right/2,bottom/2)
                }
                val top=board.toImage(screen.x,screen.y+34*d)
                document.selection!!.rect.set(top.x-50*d/board.zoom,top.y,top.x+50*d/board.zoom,top.y+60*d/board.zoom)
                val measured=caption(board)
                assertEquals(referenceSize.width(),measured.bounds.width(),.001f)
                assertEquals(referenceSize.height(),measured.bounds.height(),.001f)
                val viewport=captionViewport(board)
                val grip=screenGrip(board)
                val origin=referenceOrigin(measured,grip,viewport,10*d)
                assertTrue("$tag/$edge horizontal containment",origin.x>=viewport.left-.001f && origin.x+measured.bounds.width()<=viewport.right+.001f)
                assertTrue("$tag/$edge vertical containment",origin.y>=viewport.top-.001f && origin.y+measured.bounds.height()<=viewport.bottom+.001f)
                assertCanvasReference("rotation-$tag-$edge-$zoom-grid-$grid",board)
            }
        }
    }

    @Test(timeout=20000) fun minimumZoomFixtureStillUsesFiniteOrdinaryPixelCaptionMetrics() {
        // Inject only the viewport scale; never allocate a billion-pixel source to reach this path.
        for(tag in listOf("mnc-Mong","qaa-Zsye-XV")) withDocument(language(tag),4,4) {board,document ->
            document.select(RectF(0f,0f,4f,4f))
            setFloat(board,"zoom",1e-9f);setFloat(board,"panX",200f);setFloat(board,"panY",340f)
            assertEquals(1e-9f,board.zoom,0f)
            val measured=caption(board)
            assertTrue(measured.bounds.width().isFinite());assertTrue(measured.bounds.height().isFinite())
            assertTrue(measured.paint.textSize in 1f..100f)
            assertCanvasReference("rotation-low-zoom-$tag",board,checkResizeHits=false)
        }
    }

    private data class Caption(val label: String,val paint: Paint,val direction: TextDirection,val bounds: RectF)

    private fun referenceCaption(text: String,source: Paint,height: Float,direction: TextDirection): Caption {
        val paint=Paint(source).apply {textAlign=Paint.Align.LEFT}
        val label=VerticalText.wrapLabel(text,paint,max(height,paint.fontSpacing),direction)
        return Caption(label,paint,direction,VerticalText.bounds(label,paint,direction,GlyphOrientation.MIXED,1f))
    }

    private fun drawReferenceCaption(canvas: Canvas,caption: Caption,left: Float,top: Float) {
        canvas.save();canvas.translate(left,top)
        VerticalText.draw(canvas,caption.label,caption.paint,caption.direction,GlyphOrientation.MIXED)
        canvas.restore()
    }

    private fun referenceOrigin(caption: Caption,grip: PointF,viewport: RectF,gap: Float): PointF {
        val width=caption.bounds.width();val height=caption.bounds.height()
        val candidates=if(caption.direction==TextDirection.VERTICAL_LR) listOf(grip.x+gap,grip.x-gap-width)
            else listOf(grip.x-gap-width,grip.x+gap)
        val x=if(width>viewport.width()) viewport.centerX()-width/2 else
            candidates.firstOrNull {it>=viewport.left && it+width<=viewport.right}
                ?: max(viewport.left,min(viewport.right-width,candidates.first()))
        val y=if(height>viewport.height()) viewport.centerY()-height/2 else max(viewport.top,min(viewport.bottom-height,grip.y-height/2))
        return PointF(x,y)
    }

    private fun assemblyReference(board: AssemblyCanvas,legacy: Boolean): Bitmap {
        val bitmap=Bitmap.createBitmap(board.width,board.height,Bitmap.Config.ARGB_8888)
        val canvas=Canvas(bitmap);canvas.drawColor(EditorColours.surfaceDim)
        val density=board.resources.displayMetrics.density
        val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color=EditorColours.onSurface;textSize=16*density;textAlign=Paint.Align.CENTER;typeface=VerticalText.uiTypeface(board.context)
        }
        val text=ui(R.string.ui_add_images_then_drag_a_thumbnail_here)
        if(legacy) canvas.drawText(text,board.width/2f,board.height/2f,paint)
        else {
            val caption=referenceCaption(text,paint,board.height-32*density,VerticalText.uiDirection())
            drawReferenceCaption(canvas,caption,(board.width-caption.bounds.width())/2,(board.height-caption.bounds.height())/2)
        }
        return bitmap
    }

    private fun captionViewport(board: PaintCanvas): RectF {
        val d=board.resources.displayMetrics.density
        return RectF(board.rulerInset+4*d,board.rulerInset+4*d,board.width-24*d,board.height-24*d)
    }

    private fun caption(board: PaintCanvas): Caption {
        val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color=EditorColours.primary;textSize=11*board.resources.displayMetrics.scaledDensity;typeface=VerticalText.uiTypeface(board.context)
        }
        return referenceCaption(ui(R.string.ui_rotate),paint,captionViewport(board).height(),VerticalText.uiDirection())
    }

    private fun grip(board: PaintCanvas): PointF=PaintCanvas::class.java.getDeclaredMethod("rotationHandle",PaintDocument.Selection::class.java)
        .apply {isAccessible=true}.invoke(board,board.document.selection) as PointF
    private fun screenGrip(board: PaintCanvas): PointF=grip(board).let {board.toScreen(it.x,it.y)}
    private fun hit(board: PaintCanvas,point: PointF): Int=PaintCanvas::class.java.getDeclaredMethod("hitSelection",PaintDocument.Selection::class.java,PointF::class.java)
        .apply {isAccessible=true}.invoke(board,board.document.selection,point) as Int

    private fun assertCanvasReference(name: String,board: PaintCanvas,legacyCaption: Boolean=false,checkResizeHits: Boolean=true,saveSuccess: Boolean=false) {
        val document=board.document;val selection=document.selection!!
        val source=pixels(document.bitmap);val selectedPixels=pixels(selection.image)
        val rect=RectF(selection.rect);val rotation=selection.rotation;val floating=selection.floating
        val undo=history(document,"undo");val redo=history(document,"redo")
        val draft=board.draftState().toString();val dirty=document.dirty
        val handles=selection.geometry.resizeHandles();val originalGrip=grip(board)
        val density=board.resources.displayMetrics.density
        val ideal=selection.geometry.rotationHandle(34*density/board.zoom)
        val expectedScreen=board.toScreen(ideal.x,ideal.y)
        expectedScreen.x=expectedScreen.x.coerceIn(min(22*density,(board.width-20*density)/2),max(22*density,board.width-42*density))
        expectedScreen.y=expectedScreen.y.coerceIn(min(22*density,(board.height-20*density)/2),max(22*density,board.height-42*density))
        assertEquals("$name must preserve the existing grip geometry",board.toImage(expectedScreen.x,expectedScreen.y),originalGrip)
        assertEquals(4,hit(board,originalGrip))
        val hits=handles.mapValues {hit(board,it.value)}
        if(checkResizeHits) hits.forEach {(index,actual)->assertEquals("$name hit $index",index,actual)}
        val expected=canvasReference(board,legacyCaption)
        val actual=render(board)
        try {
            assertPixels(name,expected,actual)
            if(!legacyCaption) {
                val old=canvasReference(board,true)
                try {assertFalse("$name must reject the original horizontal caption",actual.sameAs(old))} finally {old.recycle()}
            }
            assertSame(selection,document.selection);assertEquals(rect,selection.rect);assertEquals(rotation,selection.rotation,0f)
            assertEquals(floating,selection.floating);assertArrayEquals(source,pixels(document.bitmap));assertArrayEquals(selectedPixels,pixels(selection.image))
            assertEquals(undo,history(document,"undo"));assertEquals(redo,history(document,"redo"));assertEquals(dirty,document.dirty)
            assertEquals(draft,board.draftState().toString());assertEquals(originalGrip,grip(board))
            assertEquals(handles,selection.geometry.resizeHandles());assertEquals(hits,handles.mapValues {hit(board,it.value)})
            if(saveSuccess) savePreview(name,actual)
        } finally {expected.recycle();actual.recycle()}
    }

    private fun canvasReference(board: PaintCanvas,legacyCaption: Boolean): Bitmap {
        val selection=board.document.selection!!
        // Capture the real viewport/background with the nonfloating selection temporarily hidden.
        // No gesture or document operation is invoked, and the exact selection object is restored.
        assertFalse(selection.floating)
        val field=PaintDocument::class.java.getDeclaredField("selection").apply {isAccessible=true}
        val bitmap=try {field.set(board.document,null);render(board)} finally {field.set(board.document,selection)}
        val canvas=Canvas(bitmap);val density=board.resources.displayMetrics.density;val d=density/board.zoom
        canvas.save();canvas.clipRect(board.rulerInset,board.rulerInset,board.width-20*density,board.height-20*density)
        canvas.translate(board.panX,board.panY);canvas.scale(board.zoom,board.zoom)
        val corners=selection.geometry.corners()
        val outline=Path().apply {moveTo(corners[0].x,corners[0].y);corners.drop(1).forEach {lineTo(it.x,it.y)};close()}
        canvas.drawPath(outline,Paint().apply {
            color=EditorColours.primary;style=Paint.Style.STROKE;strokeWidth=1.5f/board.zoom
            pathEffect=DashPathEffect(floatArrayOf(5f/board.zoom,4f/board.zoom),0f)
        })
        val edge=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=EditorColours.primary;style=Paint.Style.STROKE;strokeWidth=1.5f*d}
        val fill=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=Color.WHITE}
        val grip=grip(board);val top=selection.geometry.point(selection.rect.centerX(),selection.rect.top)
        canvas.drawLine(top.x,top.y,grip.x,grip.y,edge)
        canvas.drawCircle(grip.x,grip.y,7*d,fill);canvas.drawCircle(grip.x,grip.y,7*d,edge)
        if(legacyCaption) {
            val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply {
                color=edge.color;textSize=11*board.resources.displayMetrics.scaledDensity/board.zoom;typeface=VerticalText.uiTypeface(board.context)
            }
            canvas.drawText(ui(R.string.ui_rotate),grip.x+10*d,grip.y+4*d,paint)
        } else {
            val caption=caption(board);val screen=board.toScreen(grip.x,grip.y)
            val origin=referenceOrigin(caption,screen,captionViewport(board),10*density)
            canvas.save();canvas.translate(grip.x,grip.y);canvas.scale(1/board.zoom,1/board.zoom)
            drawReferenceCaption(canvas,caption,origin.x-screen.x,origin.y-screen.y);canvas.restore()
        }
        selection.geometry.resizeHandles().values.forEach {point ->
            val rect=RectF(point.x-5*d,point.y-5*d,point.x+5*d,point.y+5*d)
            canvas.drawRect(rect,fill);canvas.drawRect(rect,edge)
        }
        canvas.restore()
        // Production draws rulers after selection controls, including their half-pixel boundary ink.
        if(board.grid) PaintCanvas::class.java.getDeclaredMethod("drawRulers",Canvas::class.java).apply {isAccessible=true}.invoke(board,canvas)
        return bitmap
    }

    private fun withDocument(context: Context,width: Int=320,height: Int=240,block: (PaintCanvas,PaintDocument)->Unit) {
        val document=PaintDocument(width,height,directory())
        try {
            // Both stacks are nonempty, so a draw cannot silently clear an existing redo branch.
            document.checkpoint();document.bitmap.eraseColor(Color.MAGENTA)
            document.checkpoint();document.bitmap.eraseColor(Color.YELLOW);document.undo()
            assertTrue(document.canUndo);assertTrue(document.canRedo)
            block(PaintCanvas(context,document).apply {layout(0,0,420,680)},document)
        } finally {document.close()}
    }

    private fun assertAssemblyHasNoInstruction(board: AssemblyCanvas,state: String) {
        val actual=render(board)
        language("en-001")
        val horizontal=try {render(board)} finally {language("mnc-Mong")}
        try {assertPixels("assembly-no-caption-$state",horizontal,actual)} finally {actual.recycle();horizontal.recycle()}
    }

    private fun assertAssemblyDrawingDoesNotChangeState(board: AssemblyCanvas) {
        val model=board.assembly;val images=model.images.toList();val layout=model.layout()
        val undo=history(model,"undo");val redo=history(model,"redo");val selected=board.selectedId
        val saved=File(model.directory,"project.json").readBytes()
        val before=board.toScreen(20f,30f);val image=render(board)
        try {
            assertEquals(images,model.images);assertEquals(layout,model.layout());assertEquals(selected,board.selectedId)
            assertEquals(undo,history(model,"undo"));assertEquals(redo,history(model,"redo"))
            assertArrayEquals(saved,File(model.directory,"project.json").readBytes());assertEquals(before,board.toScreen(20f,30f))
        } finally {image.recycle()}
    }

    private fun history(target: Any,name: String): List<*> = (target.javaClass.getDeclaredField(name).apply {isAccessible=true}.get(target) as Collection<*>).toList()
    private fun setFloat(target: Any,name: String,value: Float) {target.javaClass.getDeclaredField(name).apply {isAccessible=true}.setFloat(target,value)}
    private fun render(view: View)=Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888).also {view.draw(Canvas(it))}
    private fun pixels(bitmap: Bitmap)=IntArray(bitmap.width*bitmap.height).also {bitmap.getPixels(it,0,bitmap.width,0,0,bitmap.width,bitmap.height)}
    private fun savePreview(name: String,bitmap: Bitmap) {
        val directory=File("build/reports/classic-preview/vertical-canvas-captions").apply {mkdirs()}
        File(directory,"$name.png").outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}
    }
    private fun assertPixels(name: String,expected: Bitmap,actual: Bitmap) {
        if(!expected.sameAs(actual)) {
            val directory=File("build/reports/classic-preview/vertical-canvas-captions").apply {mkdirs()}
            for((kind,image) in listOf("expected" to expected,"actual" to actual))
                File(directory,"$name-$kind.png").outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))}
            fail("$name: native pixels differ; expected and actual PNGs saved under $directory")
        }
    }
}
