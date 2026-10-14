/* AN Paint regression checks, 2026-10-14. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Rect
import android.view.MotionEvent
import android.view.View
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.util.UUID

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33],shadows = [PixelRegionDecoderShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AssemblyRendererTest {
    private lateinit var context: Context
    private lateinit var model: ImageAssembly

    @Before fun start() {
        context = RuntimeEnvironment.getApplication()
        model = ImageAssembly(File(context.cacheDir,"assembly-render-${UUID.randomUUID()}"))
    }

    private fun source(bitmap: Bitmap): AssemblyImage {
        val id = UUID.randomUUID().toString()
        val file = File(model.directory,"$id.image")
        file.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it)) }
        return AssemblyImage(id,file,id,null,ImageDimensions(bitmap.width,bitmap.height))
    }

    private fun solid(w: Int,h: Int,color: Int) = Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888).apply { eraseColor(color) }

    @Test fun unevenSnapRowsReconstructEveryOriginalPixelWithoutResizing() {
        val original = Bitmap.createBitmap(11,10,Bitmap.Config.ARGB_8888)
        for (y in 0 until original.height) for (x in 0 until original.width) {
            original.setPixel(x,y,Color.rgb((x*83+y*47)%256,(x*31+y*113)%256,(x*197+y*71)%256))
        }
        val regions = listOf(Rect(0,0,4,3),Rect(4,0,11,3),Rect(0,3,11,5),
            Rect(0,5,3,10),Rect(3,5,8,10),Rect(8,5,11,10))
        val pieces = regions.map { r ->
            val bitmap = Bitmap.createBitmap(original,r.left,r.top,r.width(),r.height())
            try { source(bitmap) } finally { bitmap.recycle() }
        }
        model.add(pieces)
        model.place(pieces[0].id,Attachment(null,null))
        model.place(pieces[1].id,Attachment(pieces[0].id,SnapEdge.RIGHT))
        model.place(pieces[2].id,Attachment(pieces[0].id,SnapEdge.BOTTOM))
        model.place(pieces[3].id,Attachment(pieces[2].id,SnapEdge.BOTTOM))
        model.place(pieces[4].id,Attachment(pieces[3].id,SnapEdge.RIGHT))
        model.place(pieces[5].id,Attachment(pieces[4].id,SnapEdge.RIGHT))
        assertEquals(ImageDimensions(original.width,original.height),model.size())
        pieces.zip(regions).forEach { (image,rect) -> assertEquals(rect,model.layout()[image.id]) }
        val output = AssemblyRenderer(context,model.images,model.layout(),0).render(model.size()!!)
        try {
            val expected = IntArray(original.width*original.height)
            val actual = IntArray(expected.size)
            original.getPixels(expected,0,original.width,0,0,original.width,original.height)
            output.getPixels(actual,0,output.width,0,0,output.width,output.height)
            assertArrayEquals("Every source pixel must survive splitting and assembly",expected,actual)
        } finally { output.recycle(); original.recycle() }
    }

    @Test fun positionedLayersBlendSourceAlphaOverEarlierImagesAndOneWhiteBackground() {
        val base = solid(20,20,Color.RED)
        val overlay = solid(10,10,0x800000ff.toInt()).apply { setPixel(4,4,Color.TRANSPARENT) }
        val images = listOf(source(base),source(overlay))
        model.add(images)
        model.position(images[0].id,0,0)
        model.position(images[1].id,4,4)
        val output = AssemblyRenderer(context,model.images,model.layout(),0).render(model.size()!!)
        val view = measuredCanvas(images.zip(listOf(base,overlay)).associate { it.first.id to it.second })
        val preview = Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888)
        try {
            view.draw(Canvas(preview))
            assertEquals(Color.RED,output.getPixel(8,8))
            assertEquals(0xff7f0080.toInt(),output.getPixel(9,9))
            for ((x,y) in listOf(8 to 8,9 to 9,2 to 2)) {
                val screen = view.toScreen(x+.5f,y+.5f)
                assertEquals("Preview and export at $x,$y",output.getPixel(x,y),preview.getPixel(screen.x.toInt(),screen.y.toInt()))
            }
        } finally { preview.recycle(); output.recycle(); base.recycle(); overlay.recycle() }
    }

    @Test fun previewAndTouchUseExportLayerOrderWhenAttachmentResolutionChangesMapOrder() {
        val child = solid(2,2,Color.GREEN)
        val middle = solid(4,4,Color.BLUE)
        val last = solid(6,6,Color.RED)
        val images = listOf(source(child),source(middle),source(last))
        model.add(images)
        model.position(images[2].id,0,0)
        model.position(images[1].id,1,1)
        model.place(images[0].id,Attachment(images[2].id,SnapEdge.RIGHT))
        assertNotEquals(model.images.map { it.id },model.layout().keys.toList())
        val view = measuredCanvas(images.zip(listOf(child,middle,last)).associate { it.first.id to it.second })
        val preview = Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888)
        val output = AssemblyRenderer(context,model.images,model.layout(),0).render(model.size()!!)
        val screen = view.toScreen(2.5f,2.5f)
        try {
            view.draw(Canvas(preview))
            assertEquals(Color.RED,output.getPixel(2,2))
            assertEquals(output.getPixel(2,2),preview.getPixel(screen.x.toInt(),screen.y.toInt()))
            for (action in listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP)) {
                val event = MotionEvent.obtain(0,0,action,screen.x,screen.y,0)
                try { view.onTouchEvent(event) } finally { event.recycle() }
            }
            assertEquals("The last exported layer is the topmost selectable image",images[2].id,view.selectedId)
        } finally { output.recycle(); preview.recycle(); child.recycle(); middle.recycle(); last.recycle() }
    }

    private fun measuredCanvas(previews: Map<String,Bitmap>) = AssemblyCanvas(context,model) { previews[it] }.apply {
        measure(View.MeasureSpec.makeMeasureSpec(400,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(400,View.MeasureSpec.EXACTLY))
        layout(0,0,400,400)
    }
}
