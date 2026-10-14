/* AN Paint regression checks, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.*
import androidx.exifinterface.media.ExifInterface
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
class AssemblyModelTest {
    private lateinit var context: Context
    private lateinit var model: ImageAssembly
    @Before fun start() {
        context = RuntimeEnvironment.getApplication()
        model = ImageAssembly(File(context.cacheDir,"assembly-model-${UUID.randomUUID()}"))
    }
    private fun item(name: String,w: Int = 100,h: Int = 100,time: Long? = null,color: Int = Color.RED): AssemblyImage {
        val id = UUID.randomUUID().toString(); val file = File(model.directory,"$id.image")
        val bitmap = Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888); bitmap.eraseColor(color)
        file.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it)) }; bitmap.recycle()
        return AssemblyImage(id,file,name,time,ImageDimensions(w,h))
    }
    @Test fun attachToAnyPlacedImageWithExactTopOrLeftAlignmentAndPreventOverlap() {
        val a=item("a"); val b=item("b",60,100); val c=item("c",100,60); val d=item("d",50,50)
        model.add(listOf(a,b,c,d)); model.place(a.id,Attachment(null,null))
        model.place(b.id,Attachment(a.id,SnapEdge.RIGHT)); model.place(c.id,Attachment(a.id,SnapEdge.BOTTOM)); model.place(d.id,Attachment(c.id,SnapEdge.RIGHT))
        assertEquals(Rect(100,0,160,100),model.layout()[b.id]); assertEquals(Rect(0,100,100,160),model.layout()[c.id]); assertEquals(Rect(100,100,150,150),model.layout()[d.id])
        val before=model.layout()
        assertThrows(IllegalArgumentException::class.java) { model.place(d.id,Attachment(a.id,SnapEdge.RIGHT)) }; assertEquals(before,model.layout())
        assertThrows(IllegalArgumentException::class.java) { model.place(a.id,Attachment(a.id,SnapEdge.BOTTOM)) }; assertEquals(before,model.layout())
        assertTrue(model.targets(d.id).any { it.attachment.anchor == b.id && it.attachment.edge == SnapEdge.RIGHT })
    }
    @Test fun cropReflowsAttachmentsAndAnInvalidBatchIsAtomicWithUndoRedoAndPersistence() {
        val a=item("a"); val b=item("b",60,100); val c=item("c",100,60); val d=item("d",50,50)
        model.add(listOf(a,b,c,d)); model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.RIGHT)); model.place(c.id,Attachment(a.id,SnapEdge.BOTTOM)); model.place(d.id,Attachment(c.id,SnapEdge.RIGHT))
        val attachments=model.images.associate { it.id to it.attachment }
        val source=a.file.readBytes(); model.crop(a.id,Rect(0,0,50,100))
        assertEquals(Rect(50,0,110,100),model.layout()[b.id]); assertArrayEquals(source,a.file.readBytes())
        // The child image moves; its anchor/edge relationship does not change.
        assertEquals(attachments,model.images.associate { it.id to it.attachment })
        val snapshot=model.layout(); val saved=File(model.directory,"project.json").readBytes()
        assertThrows(IllegalArgumentException::class.java) { model.crop(mapOf(a.id to Rect(0,0,100,50),b.id to Rect(0,0,60,100))) }
        assertEquals(snapshot,model.layout()); assertArrayEquals(saved,File(model.directory,"project.json").readBytes())
        model.undo(); assertEquals(Rect(100,0,160,100),model.layout()[b.id]); model.redo(); assertEquals(snapshot,model.layout())
        val reloaded=ImageAssembly(model.directory); assertEquals(snapshot,reloaded.layout()); assertEquals(Rect(0,0,50,100),reloaded.image(a.id).crop)
        reloaded.unplace(a.id); assertEquals(3,reloaded.layout().size); assertNull(reloaded.image(a.id).attachment); assertEquals(4,reloaded.images.size)
    }
    @Test fun sortByNameOrRealModificationTimeDoesNotChangePlacementAndUnknownTimesStayLast() {
        val a=item("b.png",time=1000); val b=item("a.png",time=3000); val c=item("c.png")
        model.add(listOf(a,b,c)); model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.RIGHT))
        val original=model.layout()
        assertEquals(listOf(b,a,c),model.sorted(AssemblySort.NAME_ASC).map { it.copy(attachment=null) })
        assertEquals(listOf(a.id,b.id,c.id),model.sorted(AssemblySort.OLDEST).map { it.id })
        assertEquals(listOf(b.id,a.id,c.id),model.sorted(AssemblySort.NEWEST).map { it.id }); assertEquals(original,model.layout())
    }
    @Test fun batchMarginsUseEachOriginalSizeAndTwentyImageCapPreservesExistingItems() {
        val items=(1..20).map { item("$it.png",100+it,200+it) }; model.add(items)
        assertThrows(IllegalArgumentException::class.java) { model.add(listOf(item("extra"))) }; assertEquals(20,model.images.size)
        model.crop(items.map { it.id }.toSet(),CropMargins(10.0,20.0,10.0,0.0,true))
        assertEquals(Rect(10,40,91,201),model.image(items[0].id).crop)
        assertEquals(Rect(12,44,108,220),model.image(items[19].id).crop)
        model.undo(); assertEquals(Rect(0,0,101,201),model.image(items[0].id).crop)
        assertThrows(IllegalArgumentException::class.java) { model.crop(items.map { it.id }.toSet(),CropMargins(50.0,0.0,50.0,0.0,true)) }
    }
    @Test fun exportUsesCroppedOriginalPixelsAndFlattensImportsAndEmptySpaceOnWhite() {
        val a=item("red",10,8,color=Color.RED); val b=item("green",8,12,color=0x8000ff00.toInt()); val c=item("blue",12,6,color=Color.BLUE)
        model.add(listOf(a,b,c)); model.crop(b.id,Rect(2,2,8,10))
        model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.RIGHT)); model.place(c.id,Attachment(a.id,SnapEdge.BOTTOM))
        val image=AssemblyRenderer(context,model.images,model.layout(),0).render(model.size()!!)
        assertEquals(16,image.width); assertEquals(14,image.height)
        assertEquals(Color.RED,image.getPixel(9,7)); assertEquals(0xff7fff7f.toInt(),image.getPixel(10,7)); assertEquals(Color.BLUE,image.getPixel(11,8)); assertEquals(Color.WHITE,image.getPixel(15,13)); image.recycle()
    }
    @Test fun regionCropUsesOrientedCoordinatesForRotatedAndMirroredPhotos() {
        for (orientation in listOf(ExifInterface.ORIENTATION_ROTATE_90,ExifInterface.ORIENTATION_FLIP_HORIZONTAL,ExifInterface.ORIENTATION_TRANSVERSE)) {
            val item=item("photo",80,60); val bitmap=Bitmap.createBitmap(80,60,Bitmap.Config.ARGB_8888)
            val canvas=Canvas(bitmap); val paint=Paint()
            paint.color=Color.RED; canvas.drawRect(0f,0f,40f,30f,paint); paint.color=Color.BLUE; canvas.drawRect(40f,0f,80f,30f,paint)
            paint.color=Color.GREEN; canvas.drawRect(0f,30f,40f,60f,paint); paint.color=Color.YELLOW; canvas.drawRect(40f,30f,80f,60f,paint)
            writeSrgbFixture(bitmap,item.file,Bitmap.CompressFormat.JPEG); bitmap.recycle()
            ExifInterface(item.file.path).apply { setAttribute(ExifInterface.TAG_ORIENTATION,orientation.toString()); saveAttributes() }
            val source=ImportedImage(item.file,"photo"); val full=source.decode(ImportPlan.create(source.dimensions,source.dimensions))
            val crop=Rect(5,5,source.dimensions.width-5,source.dimensions.height-5)
            val modified=item.copy(dimensions=source.dimensions,crop=crop,attachment=Attachment(null,null))
            val renderer=AssemblyRenderer(context,listOf(modified),mapOf(modified.id to Rect(0,0,crop.width(),crop.height())),0)
            val region=renderer.render(ImageDimensions(crop.width(),crop.height()))
            for (point in listOf(10 to 10,region.width-10 to 10,10 to region.height-10)) {
                val expected=full.getPixel(point.first+5,point.second+5); val actual=region.getPixel(point.first,point.second)
                for (channel in listOf<(Int)->Int>(Color::red,Color::green,Color::blue,Color::alpha)) assertTrue("orientation=$orientation at $point: $expected vs $actual",kotlin.math.abs(channel(expected)-channel(actual)) <= 3)
            }
            full.recycle(); region.recycle()
        }
    }
    @Test fun unplaceClosesHorizontalAndVerticalGapsWithoutUnplacingSuccessors() {
        for (edge in SnapEdge.values()) {
            model.clear()
            val a=item("first",20,20); val b=item("middle",20,20); val c=item("last",20,20)
            model.add(listOf(a,b,c)); model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,edge)); model.place(c.id,Attachment(b.id,edge))
            val before=model.layout(); model.unplace(b.id)
            assertEquals(2,model.layout().size); assertNull(model.image(b.id).attachment)
            assertEquals(Attachment(a.id,edge),model.image(c.id).attachment)
            assertEquals(if (edge==SnapEdge.RIGHT) Rect(20,0,40,20) else Rect(0,20,20,40),model.layout()[c.id])
            model.undo(); assertEquals(before,model.layout()); model.redo(); assertEquals(2,model.layout().size)
            model.unplace(a.id); assertEquals(Rect(0,0,20,20),model.layout()[c.id]); assertEquals(1,model.layout().size)
        }
    }
    @Test fun movingFirstImageAfterItsFormerSuccessorsKeepsEveryOtherImagePlaced() {
        val a=item("first",20,20); val b=item("middle",20,20); val c=item("last",20,20)
        model.add(listOf(a,b,c)); model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.BOTTOM)); model.place(c.id,Attachment(b.id,SnapEdge.BOTTOM))
        val before=model.layout()
        assertTrue(model.targets(a.id).any { it.attachment==Attachment(c.id,SnapEdge.BOTTOM) })
        model.place(a.id,Attachment(c.id,SnapEdge.BOTTOM))
        assertEquals(Rect(0,0,20,20),model.layout()[b.id]); assertEquals(Rect(0,20,20,40),model.layout()[c.id]); assertEquals(Rect(0,40,20,60),model.layout()[a.id])
        model.undo(); assertEquals(before,model.layout())
    }
    @Test fun normalizationPreservesEachAspectRatioCropsAndProjectPersistence() {
        val a=item("a",120,80); val b=item("b",60,180); val c=item("c",200,50)
        model.add(listOf(a,b,c)); val original=b.file.readBytes()
        model.normalize(NormalizeAxis.WIDTH,60)
        assertEquals(ImageDimensions(60,40),model.image(a.id).placedSize); assertEquals(ImageDimensions(60,180),model.image(b.id).placedSize); assertEquals(ImageDimensions(60,15),model.image(c.id).placedSize)
        model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.BOTTOM)); model.place(c.id,Attachment(b.id,SnapEdge.BOTTOM))
        assertEquals(ImageDimensions(60,235),model.size())
        model.normalize(NormalizeAxis.HEIGHT,40); assertEquals(ImageDimensions(160,120),model.size())
        model.crop(b.id,Rect(0,0,30,180)); assertEquals(ImageDimensions(7,40),model.image(b.id).placedSize)
        val reloaded=ImageAssembly(model.directory)
        assertEquals(model.layout(),reloaded.layout()); assertEquals(model.image(b.id).normalization,reloaded.image(b.id).normalization)
        assertArrayEquals(original,b.file.readBytes())
        model.resetSizes(); assertNull(model.image(a.id).normalization); assertEquals(ImageDimensions(30,180),model.image(b.id).placedSize)
        model.undo(); assertEquals(ImageDimensions(7,40),model.image(b.id).placedSize)
        val before=model.images
        assertThrows(IllegalArgumentException::class.java) { model.normalize(NormalizeAxis.WIDTH,Int.MAX_VALUE) }; assertEquals(before,model.images)
    }
    @Test fun normalizedExportUsesOriginalImagesAndFlattensAlphaAtTheSharedEdge() {
        val a=item("a",40,20,color=Color.RED); val b=item("b",20,40,color=0x8000ff00.toInt())
        model.add(listOf(a,b)); model.normalize(NormalizeAxis.WIDTH,80); model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.BOTTOM))
        val result=AssemblyRenderer(context,model.images,model.layout(),0).render(model.size()!!)
        assertEquals(80,result.width); assertEquals(200,result.height)
        assertEquals(Color.RED,result.getPixel(79,39)); assertEquals(0xff7fff7f.toInt(),result.getPixel(79,40)); assertEquals(0xff7fff7f.toInt(),result.getPixel(0,199)); result.recycle()
    }
    @Test fun removingBranchRootAndNormalizationKeepAllOtherImagesWithoutOverlap() {
        val a=item("a",80,60); val b=item("b",40,80); val c=item("c",60,40); val d=item("d",20,20)
        model.add(listOf(a,b,c,d)); model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.RIGHT)); model.place(c.id,Attachment(a.id,SnapEdge.BOTTOM)); model.place(d.id,Attachment(c.id,SnapEdge.BOTTOM))
        model.remove(a.id); assertEquals(3,model.images.size); assertEquals(3,model.layout().size)
        model.normalize(NormalizeAxis.HEIGHT,100); assertEquals(3,model.layout().size)
        val rects=model.layout().values.toList()
        for (i in rects.indices) for (j in i+1 until rects.size) assertFalse(Rect.intersects(rects[i],rects[j]))
    }

    @Test fun absoluteCoordinatesPlaceImagesBelowAnUnequalHeightRowWithoutResizing() {
        val a=item("a",10,50); val b=item("b",20,100); val c=item("c",30,20); model.add(listOf(a,b,c))
        model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.RIGHT))
        assertThrows(IllegalArgumentException::class.java) { model.place(c.id,Attachment(a.id,SnapEdge.BOTTOM)) }
        model.position(c.id,0,100)
        assertEquals(Rect(0,0,10,50),model.layout()[a.id]); assertEquals(Rect(10,0,30,100),model.layout()[b.id])
        assertEquals(Rect(0,100,30,120),model.layout()[c.id]); assertEquals(ImageDimensions(30,120),model.size())
        model.images.forEach { assertEquals(it.dimensions,it.placedSize); assertNull(it.normalization) }
    }

    @Test fun absoluteCoordinatesPreserveChosenCropsAndNormalization() {
        val a=item("a",20,10); val b=item("b",10,20); model.add(listOf(a,b))
        model.crop(a.id,Rect(5,0,15,10)); model.normalize(NormalizeAxis.HEIGHT,10)
        val before=model.images.associate { it.id to (it.crop to it.normalization) }
        model.position(a.id,3,4); model.position(b.id,13,4)
        assertEquals(before,model.images.associate { it.id to (it.crop to it.normalization) })
        assertEquals(Rect(3,4,13,14),model.layout()[a.id]); assertEquals(Rect(13,4,18,14),model.layout()[b.id])
    }

    @Test fun absoluteCoordinatesAllowIntentionalOverlapsAndPersistWithUndoRedo() {
        val a=item("a",10,10); val b=item("b",6,6); model.add(listOf(a,b)); model.place(a.id,Attachment(null,null))
        model.position(b.id,5,5)
        assertTrue(model.image(b.id).isPlaced); assertNull(model.image(b.id).attachment)
        assertEquals(ImagePosition(5,5),model.image(b.id).position); assertEquals(Rect(5,5,11,11),model.layout()[b.id])
        assertEquals(ImageDimensions(11,11),model.size()); val snapshot=model.layout()
        assertEquals(snapshot,ImageAssembly(model.directory).layout())
        model.undo(); assertFalse(model.image(b.id).isPlaced); model.redo(); assertEquals(snapshot,model.layout())
        model.unplace(b.id); assertFalse(model.image(b.id).isPlaced); model.undo(); assertEquals(snapshot,model.layout())
    }

    @Test fun changingExactCoordinatesOfASnapRootOrMiddleMovesOnlyThatImage() {
        val a=item("a",10,10); val b=item("b",10,10); val c=item("c",10,10); model.add(listOf(a,b,c))
        model.place(a.id,Attachment(null,null)); model.place(b.id,Attachment(a.id,SnapEdge.BOTTOM)); model.place(c.id,Attachment(b.id,SnapEdge.BOTTOM))
        val before=model.layout()
        model.position(b.id,7,3)
        assertEquals(Rect(7,3,17,13),model.layout()[b.id]); assertEquals(before[a.id],model.layout()[a.id]); assertEquals(before[c.id],model.layout()[c.id])
        assertEquals(ImagePosition(0,20),model.image(c.id).position)
        model.undo(); assertEquals(before,model.layout()); model.position(a.id,50,50)
        assertEquals(Rect(50,50,60,60),model.layout()[a.id]); assertEquals(before[b.id],model.layout()[b.id]); assertEquals(before[c.id],model.layout()[c.id])
        assertEquals(ImagePosition(0,10),model.image(b.id).position); assertEquals(Attachment(b.id,SnapEdge.BOTTOM),model.image(c.id).attachment)
        assertEquals(model.layout(),ImageAssembly(model.directory).layout())
    }

    @Test fun snapsToExplicitAnchorsStillPreventCollisionsAndClearAbsoluteCoordinates() {
        val a=item("a",10,10); val b=item("b",5,5); val c=item("c",5,5); model.add(listOf(a,b,c))
        model.position(a.id,20,30); model.position(b.id,30,30); model.position(c.id,0,0)
        val before=model.layout()
        assertThrows(IllegalArgumentException::class.java) { model.place(c.id,Attachment(a.id,SnapEdge.RIGHT)) }
        assertEquals(before,model.layout()); assertFalse(model.targets(c.id).any { it.attachment == Attachment(a.id,SnapEdge.RIGHT) })
        model.place(c.id,Attachment(b.id,SnapEdge.RIGHT))
        assertNull(model.image(c.id).position); assertEquals(Rect(35,30,40,35),model.layout()[c.id])
    }

    @Test fun removingExplicitAnchorPreservesItsSnappedSuccessorsAtTheirExactCoordinates() {
        val a=item("a",10,10); val b=item("b",4,4); val c=item("c",3,3); model.add(listOf(a,b,c))
        model.position(a.id,25,30); model.place(b.id,Attachment(a.id,SnapEdge.RIGHT)); model.place(c.id,Attachment(b.id,SnapEdge.RIGHT))
        val before=model.layout(); model.unplace(a.id)
        assertFalse(model.image(a.id).isPlaced); assertEquals(before[b.id],model.layout()[b.id]); assertEquals(before[c.id],model.layout()[c.id])
        assertEquals(ImagePosition(35,30),model.image(b.id).position); assertEquals(Attachment(b.id,SnapEdge.RIGHT),model.image(c.id).attachment)
        model.undo(); assertEquals(before,model.layout()); model.remove(a.id)
        assertEquals(before.filterKeys { it != a.id },model.layout()); assertEquals(model.layout(),ImageAssembly(model.directory).layout())
    }

    @Test fun invalidCoordinatesAreAtomicAndDoNotConsumeUndo() {
        val a=item("a",1,1); val b=item("b",1,1); model.add(listOf(a,b))
        model.position(a.id,0,0); model.position(b.id,1,0)
        val before=model.images; val saved=File(model.directory,"project.json").readBytes()
        for ((x,y) in listOf(-1 to 0,0 to -1,Int.MAX_VALUE to 0,0 to Int.MAX_VALUE)) {
            assertThrows(IllegalArgumentException::class.java) { model.position(a.id,x,y) }
        }
        assertThrows(IllegalArgumentException::class.java) { model.position("missing-source",0,0) }
        assertEquals(before,model.images); assertArrayEquals(saved,File(model.directory,"project.json").readBytes())
        model.undo(); assertEquals(setOf(a.id),model.layout().keys); assertFalse(model.image(b.id).isPlaced)
        model.clear()
        val huge=a.copy(dimensions=ImageDimensions(Int.MAX_VALUE,1),crop=Rect(0,0,Int.MAX_VALUE,1),attachment=null,position=null)
        model.add(listOf(huge,b)); val unplaced=model.images
        assertThrows(IllegalArgumentException::class.java) { model.position(huge.id,1,0) }; assertEquals(unplaced,model.images)
    }

    @Test fun legacyAttachmentsStillLoadAndMalformedStoredPositionsAreRejected() {
        val a=item("a",2,2); model.add(listOf(a)); model.place(a.id,Attachment(null,null))
        val file=File(model.directory,"project.json")
        val legacy=org.json.JSONObject(file.readText()).put("version",3)
        file.writeText(legacy.toString()); assertEquals(model.layout(),ImageAssembly(model.directory).layout())
        for (coordinates in listOf(listOf<Any>(-1,0),listOf<Any>(Int.MAX_VALUE.toLong()+1,0),listOf<Any>(0.5,0),listOf<Any>("0",0),listOf<Any>(0))) {
            val malformed=org.json.JSONObject(legacy.toString())
            malformed.getJSONArray("images").getJSONObject(0).remove("placed")
            malformed.getJSONArray("images").getJSONObject(0).put("position",org.json.JSONArray(coordinates))
            file.writeText(malformed.toString())
            assertThrows(IllegalArgumentException::class.java) { ImageAssembly(model.directory) }
        }
    }

}
