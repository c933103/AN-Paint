/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import org.catrobat.paintroid.R
import java.io.File
import java.io.IOException

/** All formats encode the same opaque document; the source bitmap is never modified. */
object ImageExporter {
    fun encode(image: Bitmap,file: File,options: ExportOptions,budget: Long) {
        when(options.format) {
            ImageFormat.JPEG_XL -> JxlCodec.encode(image,file,options.quality,options.lossless,budget)
            ImageFormat.WEBP -> WebpCodec.encode(image,file,options.quality,options.lossless,budget)
            ImageFormat.HEIC -> HeifCodec.encode(image,file,"heic",options.quality,false,budget)
            ImageFormat.AVIF -> HeifCodec.encode(image,file,"avif",options.quality,options.lossless,budget)
            ImageFormat.BMP,ImageFormat.GIF -> BitmapFileCodec.encode(image,file,options.format==ImageFormat.GIF,options.dither,budget)
            ImageFormat.DIB -> DibCodec.encode(image,file,budget)
            ImageFormat.TIFF -> TiffCodec.encode(image,file,options.tiffCompressed,budget)
            ImageFormat.ICO -> IcoCodec.encode(image,file,options.icoSize,budget)
            ImageFormat.BASE64 -> TextImageCodec.encodeBase64(image,file,budget)
            ImageFormat.ASCII_ART -> TextImageCodec.encodeAscii(image,file,options.asciiColumns,options.asciiInvert,budget)
            ImageFormat.PNG,ImageFormat.JPEG -> file.outputStream().use {
                val format=if(options.format==ImageFormat.JPEG) Bitmap.CompressFormat.JPEG else Bitmap.CompressFormat.PNG
                if(!image.compress(format,options.quality.coerceIn(1,100),it)) throw IOException(ui(R.string.ui_the_encoder_did_not_finish))
            }
        }
    }
}
