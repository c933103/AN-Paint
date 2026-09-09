/*
 * Paintroid: An image manipulation application for Android.
 *  Copyright (C) 2010-2022 The Catrobat Team
 * (<http://developer.catrobat.org/credits>)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
package org.catrobat.paintroid.iotasks

import android.content.ContentResolver
import android.content.Context
import android.net.Uri
import android.util.Log
import com.esotericsoftware.kryo.KryoException
import com.esotericsoftware.kryo.io.Output
import java.io.File
import androidx.test.espresso.idling.CountingIdlingResource
import java.io.IOException
import java.lang.ref.WeakReference
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.catrobat.paintroid.FileIO
import org.catrobat.paintroid.command.serialization.CommandSerializer

class LoadImage(
    callback: LoadImageCallback,
    private val requestCode: Int,
    private val uri: Uri?,
    context: Context,
    private val scaleImage: Boolean,
    private val commandSerializer: CommandSerializer,
    private val scopeIO: CoroutineScope,
    private val idlingResource: CountingIdlingResource
) {
    private val callbackRef: WeakReference<LoadImageCallback> = WeakReference(callback)
    private val context: WeakReference<Context> = WeakReference(context)

    private fun getBitmapReturnValue(
        uri: Uri,
        resolver: ContentResolver
    ): BitmapReturnValue {
        // Local fix, 2026-09-07: provider MIME types can be generic or incorrect.
        // Copy once so bounds, pixels and EXIF can be read from the same bytes.
        val appContext = context.get() ?: throw IOException("Image-loading context is no longer available")
        val cachedFile = File.createTempFile("paint-import-", ".image", appContext.cacheDir)
        try {
            val source = resolver.openInputStream(uri) ?: throw IOException("Cannot open selected file")
            source.use { input -> cachedFile.outputStream().use { output -> input.copyTo(output) } }
            val cachedUri = Uri.fromFile(cachedFile)
            val projectMagic = Output(32).use { output ->
                output.writeString(CommandSerializer.MAGIC_VALUE)
                output.toBytes()
            }
            val header = cachedFile.inputStream().use { input ->
                val buffer = ByteArray(projectMagic.size)
                var count = 0
                while (count < buffer.size) {
                    val read = input.read(buffer, count, buffer.size - count)
                    if (read == -1) break
                    count += read
                }
                buffer.copyOf(count)
            }
            return if (header.contentEquals(projectMagic)) {
                val fileContent = commandSerializer.readFromFile(cachedUri)
                BitmapReturnValue(fileContent.commandModel, fileContent.colorHistory)
            } else if (header.size >= 4 && header[0] == 0x50.toByte() && header[1] == 0x4b.toByte() &&
                header[2] == 0x03.toByte() && header[3] == 0x04.toByte()) {
                OpenRasterFileFormatConversion.importOraFile(resolver, cachedUri)
            } else if (scaleImage) {
                FileIO.getScaledBitmapFromUri(resolver, cachedUri, appContext)
            } else {
                FileIO.getBitmapReturnValueFromUri(resolver, cachedUri, appContext)
            }
        } finally {
            cachedFile.delete()
        }
    }

    @SuppressWarnings("TooGenericExceptionCaught")
    fun execute() {
        val callback = callbackRef.get()
        if (callback == null || callback.isFinishing) {
            return
        }
        callback.onLoadImagePreExecute(requestCode)

        var returnValue: BitmapReturnValue? = null
        scopeIO.launch {
            idlingResource.increment()
            try {
                if (uri == null) {
                    Log.e(TAG, "Can't load image file, uri is null")
                } else try {
                    val resolver = callback.contentResolver
                    FileIO.filename = "image"
                    returnValue = getBitmapReturnValue(uri, resolver)
                } catch (e: IOException) {
                    Log.e(TAG, "Can't load image file", e)
                } catch (e: NullPointerException) {
                    Log.e(TAG, "Can't load image file", e)
                } catch (e: SecurityException) {
                    Log.e(TAG, "Permission to read the selected image is unavailable", e)
                } catch (e: KryoException) {
                    Log.e(TAG, "Saved project is invalid or incomplete", e)
                } catch (e: CommandSerializer.NotCatrobatImageException) {
                    Log.e(TAG, "Saved project has an invalid header", e)
                }
                withContext(Dispatchers.Main) {
                    if (!callback.isFinishing) {
                        callback.onLoadImagePostExecute(requestCode, uri, returnValue)
                    }
                }
            } finally {
                idlingResource.decrement()
            }
        }
    }

    interface LoadImageCallback {
        fun onLoadImagePostExecute(requestCode: Int, uri: Uri?, result: BitmapReturnValue?)
        fun onLoadImagePreExecute(requestCode: Int)
        val contentResolver: ContentResolver
        val isFinishing: Boolean
    }

    companion object {
        private val TAG = LoadImage::class.java.simpleName
    }
}
