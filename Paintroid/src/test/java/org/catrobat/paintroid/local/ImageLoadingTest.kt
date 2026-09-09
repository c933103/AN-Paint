/*
 * Added for Pocket Paint Local, 2026-09-07.
 * Licensed under GNU AGPL version 3 or (at your option) any later version.
 * See LICENSE at the project root. Distributed without any warranty.
 */
package org.catrobat.paintroid.local

import android.app.ActivityManager
import android.app.Activity
import android.content.Intent
import android.content.ContentProvider
import android.content.ContentValues
import android.content.Context
import android.content.pm.ProviderInfo
import android.database.Cursor
import android.database.MatrixCursor
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Looper
import android.os.ParcelFileDescriptor
import android.provider.OpenableColumns
import androidx.test.espresso.idling.CountingIdlingResource
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import org.catrobat.paintroid.command.implementation.DefaultCommandManager
import org.catrobat.paintroid.command.implementation.DefaultCommandFactory
import org.catrobat.paintroid.FileIO
import org.catrobat.paintroid.MainActivity
import org.catrobat.paintroid.command.serialization.CommandSerializer
import org.catrobat.paintroid.common.CommonFactory
import org.catrobat.paintroid.common.LOAD_IMAGE_DEFAULT
import org.catrobat.paintroid.common.REQUEST_CODE_LOAD_PICTURE
import org.catrobat.paintroid.iotasks.BitmapReturnValue
import org.catrobat.paintroid.iotasks.LoadImage
import org.catrobat.paintroid.model.LayerModel
import org.catrobat.paintroid.model.MainActivityModel
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.Robolectric
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowContentResolver
import java.io.File
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream
import com.esotericsoftware.kryo.io.Output

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ImageLoadingTest {
    private lateinit var context: Context
    private lateinit var provider: ImageProvider

    @Before fun prepareProvider() {
        context = RuntimeEnvironment.getApplication()
        provider = ImageProvider()
        provider.attachInfo(context, ProviderInfo().apply { authority = "local.image.fixture" })
        ShadowContentResolver.registerProviderInternal("local.image.fixture", provider)
        val manager = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
        Shadows.shadowOf(manager).setMemoryInfo(ActivityManager.MemoryInfo().apply {
            availMem = 1_000_000_000L
            threshold = 10_000_000L
        })
    }

    private fun image(format: Bitmap.CompressFormat, mime: String?, name: String): Uri {
        val bitmap = Bitmap.createBitmap(24, 48, Bitmap.Config.ARGB_8888)
        bitmap.eraseColor(Color.BLUE)
        val file = File(context.cacheDir, "picker-image.bin")
        file.outputStream().use { assertTrue(bitmap.compress(format, 100, it)) }
        bitmap.recycle()
        provider.file = file
        provider.mime = mime
        provider.displayName = name
        return Uri.parse("content://local.image.fixture/document/12345")
    }

    private fun load(uri: Uri): BitmapReturnValue? {
        var completed = false
        var result: BitmapReturnValue? = null
        val failures = mutableListOf<Throwable>()
        val scope = CoroutineScope(SupervisorJob() + Dispatchers.Unconfined + CoroutineExceptionHandler { _, error ->
            failures.add(error)
        })
        val busy = CountingIdlingResource("load-image-test")
        val callback = object : LoadImage.LoadImageCallback {
            override val contentResolver get() = context.contentResolver
            override val isFinishing = false
            override fun onLoadImagePreExecute(requestCode: Int) = Unit
            override fun onLoadImagePostExecute(requestCode: Int, uri: Uri?, value: BitmapReturnValue?) {
                assertEquals(LOAD_IMAGE_DEFAULT, requestCode)
                completed = true
                result = value
            }
        }
        val serializer = CommandSerializer(context, DefaultCommandManager(CommonFactory(), LayerModel()), MainActivityModel())
        try {
            LoadImage(callback, LOAD_IMAGE_DEFAULT, uri, context, false, serializer, scope, busy).execute()
            Shadows.shadowOf(Looper.getMainLooper()).idle()
            assertTrue("Uncaught loading exception: $failures", failures.isEmpty())
            assertTrue("The load callback must complete", completed)
            assertTrue("Loading must release its busy state", busy.isIdleNow)
            assertTrue("Temporary import files must be removed", context.cacheDir.listFiles()!!.none {
                it.name.startsWith("paint-import-")
            })
            return result
        } finally {
            scope.cancel()
        }
    }

    private fun assertPortraitLoads(format: Bitmap.CompressFormat, mime: String?, name: String) {
        val result = load(image(format, mime, name))
        assertNotNull("A valid $name image must load when reported as $mime", result)
        assertNotNull(result!!.bitmap)
        val bitmap = result.bitmap!!
        assertFalse(bitmap.isRecycled)
        assertTrue(bitmap.isMutable)
        assertEquals(24, bitmap.width)
        assertEquals(48, bitmap.height)
        assertTrue(Color.blue(bitmap.getPixel(10, 10)) >= 250)
    }

    @Test fun pngFromDocumentProviderLoads() =
        assertPortraitLoads(Bitmap.CompressFormat.PNG, "image/png", "portrait.png")

    @Test fun jpegFromDocumentProviderLoads() =
        assertPortraitLoads(Bitmap.CompressFormat.JPEG, "image/jpeg", "portrait.jpg")

    @Test fun pngReportedAsGenericBinaryStillLoads() =
        assertPortraitLoads(Bitmap.CompressFormat.PNG, "application/octet-stream", "portrait.png")

    @Test fun jpegReportedAsGenericBinaryStillLoads() =
        assertPortraitLoads(Bitmap.CompressFormat.JPEG, "application/octet-stream", "portrait.jpg")

    @Test fun webpReportedAsGenericBinaryStillLoads() =
        assertPortraitLoads(Bitmap.CompressFormat.WEBP_LOSSLESS, "application/octet-stream", "portrait.webp")

    @Test fun extensionlessImageWithUnknownTypeLoads() =
        assertPortraitLoads(Bitmap.CompressFormat.PNG, null, "picture")

    @Test fun imageProviderIsOnlyOpenedOnce() {
        val uri = image(Bitmap.CompressFormat.PNG, "application/octet-stream", "portrait.png")
        provider.openLimit = 1
        assertNotNull(load(uri)!!.bitmap)
        assertEquals(1, provider.opens)
    }

    @Test fun revokedReadAccessReportsFailureAndReleasesBusyState() {
        val uri = image(Bitmap.CompressFormat.PNG, "image/png", "portrait.png")
        provider.denyAccess = true
        assertNull(load(uri))
    }

    @Test fun corruptSavedProjectReportsFailureAndReleasesBusyState() {
        val uri = image(Bitmap.CompressFormat.PNG, "application/octet-stream", "damaged.catrobat-image")
        Output(provider.file.outputStream()).use { it.writeString(CommandSerializer.MAGIC_VALUE) }
        assertNull(load(uri))
    }

    @Test fun savedProjectStillLoadsWhenMimeTypeIsUnknown() {
        val uri = image(Bitmap.CompressFormat.PNG, null, "drawing.catrobat-image")
        val manager = DefaultCommandManager(CommonFactory(), LayerModel())
        manager.setInitialStateCommand(DefaultCommandFactory().createInitCommand(24, 48))
        manager.reset()
        CommandSerializer(context, manager, MainActivityModel()).writeToInternalMemory(provider.file.outputStream())
        val result = load(uri)
        assertNotNull(result!!.model)
    }

    @Test fun openRasterStillLoadsWhenMimeTypeIsUnknown() {
        val uri = image(Bitmap.CompressFormat.PNG, null, "drawing.ora")
        val png = provider.file.readBytes()
        ZipOutputStream(provider.file.outputStream()).use { zip ->
            zip.putNextEntry(ZipEntry("mimetype"))
            zip.write("image/openraster".toByteArray())
            zip.closeEntry()
            zip.putNextEntry(ZipEntry("data/layer0.png"))
            zip.write(png)
            zip.closeEntry()
        }
        val result = load(uri)
        assertEquals(1, result!!.layerList!!.size)
        assertEquals(Color.BLUE, result.layerList!![0].bitmap.getPixel(10, 10))
    }

    @Test fun insufficientMemoryRequestsScalingBeforeDecodingFullBitmap() {
        val uri = image(Bitmap.CompressFormat.PNG, "image/png", "portrait.png")
        Shadows.shadowOf(context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager)
            .setMemoryInfo(ActivityManager.MemoryInfo().apply { availMem = 1; threshold = 0 })
        val result = load(uri)
        assertTrue(result!!.toBeScaled)
        assertNull(result.bitmap)
    }

    @Test fun zeroDegreeOrientationKeepsImmutableImageUsable() {
        val bitmap = Bitmap.createBitmap(24, 48, Bitmap.Config.ARGB_8888)
        bitmap.eraseColor(Color.BLUE)
        val immutable = bitmap.copy(Bitmap.Config.ARGB_8888, false)
        val result = FileIO.getOrientedBitmap(immutable, 0f)!!
        assertFalse(result.isRecycled)
        assertEquals(Color.BLUE, result.getPixel(10, 10))
    }

    @Test fun pickerResultWithGenericMimeReachesEditorCanvas() {
        val uri = image(Bitmap.CompressFormat.PNG, "application/octet-stream", "portrait.png")
        val controller = Robolectric.buildActivity(MainActivity::class.java, Intent(Intent.ACTION_MAIN))
        try {
            val activity = controller.create().start().resume().visible().get()
            activity.onActivityResult(REQUEST_CODE_LOAD_PICTURE, Activity.RESULT_OK, Intent().setData(uri))
            val deadline = System.nanoTime() + 5_000_000_000L
            while ((activity.layerModel.width != 24 || activity.layerModel.height != 48) && System.nanoTime() < deadline) {
                Shadows.shadowOf(Looper.getMainLooper()).idle()
                Thread.sleep(10)
            }
            Shadows.shadowOf(Looper.getMainLooper()).idle()
            assertEquals(24, activity.layerModel.width)
            assertEquals(48, activity.layerModel.height)
            assertEquals(Color.BLUE, activity.layerModel.currentLayer!!.bitmap.getPixel(10, 10))
        } finally {
            controller.pause().stop().destroy()
        }
    }

    class ImageProvider : ContentProvider() {
        lateinit var file: File
        var mime: String? = null
        var displayName = "picture"
        var openLimit = Int.MAX_VALUE
        var opens = 0
        var denyAccess = false
        override fun onCreate() = true
        override fun getType(uri: Uri): String? = mime
        override fun openFile(uri: Uri, mode: String): ParcelFileDescriptor {
            if (denyAccess) throw SecurityException("Read grant revoked")
            check(++opens <= openLimit) { "This provider cannot be opened again" }
            return ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
        }
        override fun query(uri: Uri, projection: Array<out String>?, selection: String?, selectionArgs: Array<out String>?, sortOrder: String?): Cursor {
            val columns = projection ?: arrayOf(OpenableColumns.DISPLAY_NAME, OpenableColumns.SIZE)
            return MatrixCursor(columns).apply {
                addRow(columns.map { if (it == OpenableColumns.DISPLAY_NAME) displayName else file.length() }.toTypedArray())
            }
        }
        override fun insert(uri: Uri, values: ContentValues?): Uri? = null
        override fun update(uri: Uri, values: ContentValues?, selection: String?, selectionArgs: Array<out String>?) = 0
        override fun delete(uri: Uri, selection: String?, selectionArgs: Array<out String>?) = 0
    }
}
