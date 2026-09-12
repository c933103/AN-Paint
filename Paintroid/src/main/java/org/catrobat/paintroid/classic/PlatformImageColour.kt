/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ColorSpace
import android.os.Build
import org.catrobat.paintroid.R
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.IOException
import java.io.RandomAccessFile
import java.util.zip.InflaterInputStream
import java.util.zip.CRC32

/** Colour metadata is read without allocating the encoded image. Our own ICC/CICP
 * conversion receives unconverted samples, including on old Android versions.
 * The private colour-neutral copy prevents a platform decoder converting twice.
 * Alpha is deliberately kept until the document or assembly composites it.
 */
internal class PlatformImageColour private constructor(
    private val format: String,
    private val omitted: List<LongRange>,
    private val icc: ByteArray?,
    private val cicp: ByteArray?,
    private val pngGamma: Float?,
    private val pngChromaticities: FloatArray?,
    val highDepth: Boolean
) {
    private val explicitConversion get() = icc != null || cicp != null || pngGamma != null || pngChromaticities != null
    val decodedWorkingBytesPerPixel: Int get() =
        (if (highDepth && Build.VERSION.SDK_INT >= 26) 8 else 4) + (if (explicitConversion) 4 else 0)
    // Native colour conversion holds the original profile, its parsed tables and
    // a bounded row, in addition to its output bitmap.
    val metadataWorkingBytes: Long get() = if (explicitConversion) 8L * 1024 * 1024 else 0

    fun options(sample: Int) = BitmapFactory.Options().apply {
        inSampleSize = sample; inScaled = false; inMutable = true
        inPreferredConfig = if (highDepth && Build.VERSION.SDK_INT >= 26) Bitmap.Config.RGBA_F16 else Bitmap.Config.ARGB_8888
        if (Build.VERSION.SDK_INT >= 26) inPreferredColorSpace = ColorSpace.get(ColorSpace.Named.SRGB)
    }

    /** Returns a new bitmap when native conversion is necessary; never recycles input. */
    fun convert(input: Bitmap): Bitmap {
        // An Ultra HDR JPEG contains a fully authored SDR base. Use that rendition
        // for this SDR editor; never leave a stale gain map on edited pixels.
        if (Build.VERSION.SDK_INT >= 34 && input.hasGainmap()) input.setGainmap(null)
        return try { when {
            cicp != null -> HeifCodec.convertCicp(input,cicp[0].toInt() and 255,cicp[1].toInt() and 255)
            icc != null -> HeifCodec.convertIcc(input,icc)
            pngGamma != null || pngChromaticities != null -> HeifCodec.convertPngColour(input,pngGamma ?: 0f,pngChromaticities)
            else -> input
        } } catch (error: LinkageError) {
            // A damaged/unsupported native installation must become the normal
            // visible import error, rather than escaping the worker and leaving
            // the editor permanently busy. Never substitute unconverted pixels.
            throw IOException(ui(R.string.colour_converter_unavailable),error)
        }
    }

    fun <T> withDecodeFile(source: File, action: (File) -> T): T {
        if (!explicitConversion) return action(source)
        val temporary = File.createTempFile("colour-input-", ".img", source.parentFile)
        try {
            RandomAccessFile(source,"r").use { input ->
                RandomAccessFile(temporary,"rw").use { output ->
                    val buffer = ByteArray(64 * 1024)
                    fun copyUntil(end: Long) {
                        while (input.filePointer < end) {
                            val count = input.read(buffer,0,minOf(buffer.size.toLong(),end-input.filePointer).toInt())
                            if (count < 0) throw IOException(ui(R.string.colour_truncated_metadata))
                            output.write(buffer,0,count)
                        }
                    }
                    omitted.sortedBy { it.first }.forEach { range -> copyUntil(range.first); input.seek(range.last+1) }
                    copyUntil(input.length())
                    if (format == "WEBP") {
                        val length=output.length()-8
                        output.seek(4); repeat(4) { output.write((length shr (it*8)).toInt() and 255) }
                        // Clear the VP8X ICC flag when the corresponding chunk is removed.
                        output.seek(12)
                        while(output.filePointer+8 <= output.length()) {
                            val type=ByteArray(4); output.readFully(type);val n=readLittle(output)
                            val start=output.filePointer
                            if(String(type,Charsets.US_ASCII)=="VP8X" && n>=1) {val flags=output.read();output.seek(start);output.write(flags and 0xdf);break}
                            output.seek(start+n+(n and 1))
                        }
                    }
                }
            }
            return action(temporary)
        } finally { temporary.delete() }
    }

    companion object {
        private const val MAX_PROFILE = 4 * 1024 * 1024
        private fun error(): Nothing = throw IOException(ui(R.string.colour_invalid_metadata))
        private fun readLittle(input: RandomAccessFile): Long = (0..3).fold(0L) { result,shift ->
            val value=input.read();if(value<0)error();result or (value.toLong() shl (shift*8))
        }
        private fun bytes(input: RandomAccessFile, length: Long): ByteArray {
            if(length !in 0..MAX_PROFILE.toLong()) error()
            return ByteArray(length.toInt()).also { input.readFully(it) }
        }
        private fun inflate(value: ByteArray,offset: Int): ByteArray =
            InflaterInputStream(ByteArrayInputStream(value,offset,value.size-offset)).use { input ->
                val out=ByteArrayOutputStream();val buffer=ByteArray(8192)
                while(true) {val n=input.read(buffer);if(n<0)break;if(out.size()+n>MAX_PROFILE)error();out.write(buffer,0,n)}
                out.toByteArray()
            }
        fun read(file: File): PlatformImageColour {
            var profile: ByteArray?=null;var cicp: ByteArray?=null;var highDepth=false
            var pngGamma: Double?=null;var pngChromaticities: DoubleArray?=null;var pngSrgb=false
            val removed=mutableListOf<LongRange>();var format=""
            RandomAccessFile(file,"r").use { input ->
                if(input.length()<8) return PlatformImageColour("",emptyList(),null,null,null,null,false)
                val header=bytes(input,minOf(12,input.length()))
                when {
                    header.take(8)==listOf(137,80,78,71,13,10,26,10).map { it.toByte() } -> {
                        format="PNG";input.seek(8)
                        while(input.filePointer+12<=input.length()) {
                            val start=input.filePointer;val length=input.readInt().toLong() and 0xffffffffL
                            val type=String(bytes(input,4),Charsets.US_ASCII);val end=start+12+length
                            if(end>input.length())error()
                            if(type=="IDAT" || type=="IEND")break
                            if(type in setOf("IHDR","iCCP","cICP","gAMA","cHRM","sRGB")) {
                                val data=bytes(input,length)
                                val checksum=input.readInt().toLong() and 0xffffffffL
                                val crc=CRC32().apply { update(type.toByteArray(Charsets.US_ASCII));update(data) }
                                if(crc.value!=checksum)error()
                                input.seek(start+8)
                            }
                            when(type) {
                                "IHDR" -> {if(length!=13L)error();val data=bytes(input,length);highDepth=(data[8].toInt() and 255)>8}
                                "iCCP" -> {
                                    val data=bytes(input,length);val separator=data.indexOf(0)
                                    if(separator !in 1..79 || separator+2>data.size || data[separator+1].toInt()!=0 || profile!=null)error()
                                    profile=inflate(data,separator+2)
                                }
                                "cICP" -> {if(length!=4L || cicp!=null)error();cicp=bytes(input,length)}
                                "gAMA" -> {if(length!=4L || pngGamma!=null)error();pngGamma=(input.readInt().toLong() and 0xffffffffL)/100000.0}
                                "cHRM" -> {if(length!=32L || pngChromaticities!=null)error();pngChromaticities=DoubleArray(8) { (input.readInt().toLong() and 0xffffffffL)/100000.0 }}
                                "sRGB" -> {if(length!=1L || pngSrgb)error();pngSrgb=true}
                            }
                            if(type in setOf("iCCP","cICP","gAMA","cHRM","sRGB"))removed.add(start until end)
                            input.seek(end)
                        }
                    }
                    header[0]==0xff.toByte() && header[1]==0xd8.toByte() -> {
                        format="JPEG";input.seek(2);val parts=mutableMapOf<Int,ByteArray>();var count=0
                        while(input.filePointer+2<=input.length()) {
                            val start=input.filePointer
                            if(input.read()!=255)error()
                            var marker=input.read();while(marker==255)marker=input.read()
                            if(marker==0xda || marker==0xd9)break
                            if(marker in 0xd0..0xd8 || marker==1)continue
                            val length=input.readUnsignedShort();if(length<2)error()
                            val payloadStart=input.filePointer
                            val end=payloadStart+length-2;if(end>input.length())error()
                            if(marker==0xe2 && length>=16) {
                                val id=bytes(input,12)
                                if(String(id,Charsets.US_ASCII)=="ICC_PROFILE\u0000") {
                                    val index=input.read();val total=input.read()
                                    if(index !in 1..total || total==0 || (count!=0 && count!=total) || parts.containsKey(index))error()
                                    count=total;parts[index]=bytes(input,end-input.filePointer);removed.add(start until end)
                                    if(parts.values.sumOf { it.size.toLong() }>MAX_PROFILE)error()
                                }
                            }
                            // Removing ICC changes MPF offsets. This SDR decoder
                            // needs neither XMP nor the HDR secondary-image index.
                            // EXIF APP1 is retained for ordinary decoder compatibility.
                            if(marker==0xe1 && length>=31) {
                                input.seek(payloadStart)
                                val id=String(bytes(input,29),Charsets.US_ASCII)
                                if(id=="http://ns.adobe.com/xap/1.0/\u0000")removed.add(start until end)
                            }
                            if(marker==0xe2 && length>=6) {
                                input.seek(payloadStart)
                                if(String(bytes(input,4),Charsets.US_ASCII)=="MPF\u0000")removed.add(start until end)
                            }
                            input.seek(end)
                        }
                        if(count>0) {if(parts.size!=count)error();profile=ByteArrayOutputStream().apply { (1..count).forEach { write(parts.getValue(it)) } }.toByteArray()}
                    }
                    header.size==12 && String(header,0,4,Charsets.US_ASCII)=="RIFF" && String(header,8,4,Charsets.US_ASCII)=="WEBP" -> {
                        format="WEBP";input.seek(12)
                        while(input.filePointer+8<=input.length()) {
                            val start=input.filePointer;val type=String(bytes(input,4),Charsets.US_ASCII)
                            val length=readLittle(input);val end=start+8+length+(length and 1)
                            if(end>input.length())error()
                            if(type=="ICCP") {if(profile!=null)error();profile=bytes(input,length);removed.add(start until end)}
                            input.seek(end)
                        }
                    }
                }
            }
            val usePngMetadata=format=="PNG" && cicp==null && profile==null && !pngSrgb
            if(usePngMetadata && pngGamma?.let { it<=0 || !it.isFinite() }==true)error()
            cicp?.let {
                // PNG stores full-range RGB. Applying a YUV matrix or silently
                // treating an unknown transfer as sRGB would display false colours.
                if((it[2].toInt() and 255)!=0 || (it[3].toInt() and 255)!=1)error()
            }
            profile?.let {
                if(it.size<128 || String(it,36,4,Charsets.US_ASCII)!="acsp")error()
                if(String(it,16,4,Charsets.US_ASCII) !in setOf("RGB ","GRAY"))
                    throw IOException(ui(R.string.colour_unsupported_icc_model))
            }
            return PlatformImageColour(format,removed,if(cicp==null)profile else null,cicp,
                if(usePngMetadata)pngGamma?.toFloat() else null,
                if(usePngMetadata)pngChromaticities?.map { it.toFloat() }?.toFloatArray() else null,highDepth)
        }
    }
}
