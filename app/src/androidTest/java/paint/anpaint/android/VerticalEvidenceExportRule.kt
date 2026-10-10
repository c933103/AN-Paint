/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Instrumentation
import android.content.ContentUris
import android.content.ContentValues
import android.net.Uri
import android.os.Build
import android.provider.MediaStore
import org.json.JSONArray
import org.json.JSONObject
import org.junit.rules.TestRule
import org.junit.runner.Description
import org.junit.runners.model.Statement
import java.io.File
import java.nio.file.Files
import java.security.MessageDigest
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream

/** Export only this rule's synthetic evidence through app-owned Downloads rows.
 * No production permissions, debuggability, shell identity or capture state change.
 */
class VerticalEvidenceExportRule(private val instrumentation: Instrumentation) : TestRule {
    private val context get()=instrumentation.targetContext
    private val resolver get()=context.contentResolver
    private val collection get()=MediaStore.Downloads.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)

    override fun apply(base: Statement,description: Description): Statement=object: Statement() {
        override fun evaluate() {
            val locale=METHOD_LOCALES[description.methodName] ?: error("Unknown evidence test")
            var failure: Throwable?=null
            var prepared=false
            try {prepare(locale);prepared=true;base.evaluate()} catch(error: Throwable) {failure=error}
            if(prepared) try {export(locale,description.methodName,failure==null)} catch(error: Throwable) {
                if(failure==null) failure=error else failure!!.addSuppressed(error)
            }
            failure?.let {throw it}
        }
    }

    private fun source(relative: String): File {
        val external=checkNotNull(context.getExternalFilesDir(null)).canonicalFile
        val directory=File(external,"vertical-locale-evidence")
        check(!Files.isSymbolicLink(directory.toPath()) && directory.canonicalFile==directory.absoluteFile) {"Evidence root symlink"}
        val file=File(directory,relative)
        var component=directory
        for(part in relative.split('/')) {
            component=File(component,part)
            check(!Files.isSymbolicLink(component.toPath())) {"Evidence path symlink"}
        }
        check(file.canonicalFile==file.absoluteFile) {"Evidence symlink or noncanonical path"}
        return file
    }

    private fun prepare(locale: String) {
        check(Build.VERSION.SDK_INT>=29 && context.packageName==OWNER)
        for(relative in paths(locale)) {
            val file=source(relative)
            if(file.exists()) check(file.isFile && file.delete()) {"Could not clear owned evidence"}
        }
        // Host deletion alone can leave MediaStore rows and cause '(1)' renames.
        // The scoped query/deletion selects only this app's exact synthetic export.
        @Suppress("DEPRECATION")
        val includingPending=MediaStore.setIncludePending(collection)
        val selection="${MediaStore.MediaColumns.RELATIVE_PATH} = ? AND ${MediaStore.MediaColumns.DISPLAY_NAME} = ? AND ${MediaStore.MediaColumns.OWNER_PACKAGE_NAME} = ?"
        val ids=mutableListOf<Long>()
        resolver.query(includingPending,arrayOf(MediaStore.MediaColumns._ID),selection,
            arrayOf(RELATIVE_PATH,"$locale.zip",OWNER),null)?.use {cursor ->
            while(cursor.moveToNext()) {
                check(ids.size<16) {"Unexpected duplicate owned export rows"}
                ids.add(cursor.getLong(0))
            }
        } ?: error("Could not query owned export rows")
        for(id in ids) check(resolver.delete(ContentUris.withAppendedId(collection,id),null,null)==1)
    }

    private fun checkRow(uri: Uri,locale: String,pending: Int) {
        val columns=arrayOf(MediaStore.MediaColumns.DISPLAY_NAME,MediaStore.MediaColumns.RELATIVE_PATH,
            MediaStore.MediaColumns.OWNER_PACKAGE_NAME,MediaStore.MediaColumns.IS_PENDING)
        resolver.query(uri,columns,null,null,null)?.use {cursor ->
            check(cursor.count==1 && cursor.moveToFirst()) {"Missing or duplicate export row"}
            check(cursor.getString(0)=="$locale.zip" && cursor.getString(1)==RELATIVE_PATH &&
                cursor.getString(2)==OWNER && cursor.getInt(3)==pending) {"Export ownership/path/pending mismatch"}
        } ?: error("Could not verify export row")
    }

    private fun contentDigest(uri: Uri,expected: Long): ByteArray {
        val digest=MessageDigest.getInstance("SHA-256");var count=0L;val buffer=ByteArray(8192)
        resolver.openInputStream(uri)?.use {input ->
            while(true) {
                val size=input.read(buffer);if(size<0) break
                count+=size;check(count<=expected && count<=MAX_CASE) {"Oversize written export"}
                digest.update(buffer,0,size)
            }
        } ?: error("Could not read back owned export")
        check(count==expected) {"Written export length mismatch"}
        return digest.digest()
    }

    private fun export(locale: String,method: String,testPassed: Boolean) {
        val expected=paths(locale)
        val available=expected.filter {source(it).exists()}
        var total=0L
        for(relative in available) {
            val file=source(relative)
            check(file.isFile && file.length() in 1..MAX_FILE) {"Invalid evidence file size/type"}
            total+=file.length();check(total<=MAX_CASE) {"Oversize evidence case"}
        }
        val complete=testPassed && available.size==expected.size
        val manifest=JSONObject().put("version",1).put("owner",OWNER).put("locale",locale)
            .put("method",method).put("device_sdk",Build.VERSION.SDK_INT).put("complete",complete)
            .put("files",JSONArray())
        val temporary=File.createTempFile("vertical-export-",".zip",context.cacheDir)
        var uri: Uri?=null
        var failure: Throwable?=null
        try {
            ZipOutputStream(temporary.outputStream().buffered()).use {zip ->
                val buffer=ByteArray(8192)
                for(relative in available) {
                    val file=source(relative);val size=file.length();val digest=MessageDigest.getInstance("SHA-256")
                    zip.putNextEntry(ZipEntry(relative));var copied=0L
                    file.inputStream().use {input ->
                        while(true) {
                            val count=input.read(buffer);if(count<0) break
                            copied+=count;check(copied<=size && copied<=MAX_FILE) {"Evidence grew while exporting"}
                            digest.update(buffer,0,count);zip.write(buffer,0,count)
                        }
                    }
                    check(copied==size && file.length()==size) {"Evidence changed while exporting"}
                    zip.closeEntry()
                    manifest.getJSONArray("files").put(JSONObject().put("path",relative).put("bytes",copied)
                        .put("sha256",digest.digest().joinToString("") {"%02x".format(it.toInt() and 255)}))
                }
                val bytes=(manifest.toString()+"\n").toByteArray(Charsets.UTF_8)
                check(bytes.size<=MAX_MANIFEST)
                zip.putNextEntry(ZipEntry("manifest.json"));zip.write(bytes);zip.closeEntry()
            }
            check(temporary.length() in 1..MAX_CASE) {"Oversize export ZIP"}
            val values=ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME,"$locale.zip")
                put(MediaStore.MediaColumns.RELATIVE_PATH,RELATIVE_PATH)
                put(MediaStore.MediaColumns.MIME_TYPE,"application/zip")
                put(MediaStore.MediaColumns.IS_PENDING,1)
            }
            val inserted=resolver.insert(collection,values) ?: error("Could not create owned export")
            uri=inserted;checkRow(inserted,locale,1)
            resolver.openOutputStream(inserted,"w")?.use {output ->
                temporary.inputStream().use {input ->check(input.copyTo(output,8192)==temporary.length())}
            } ?: error("Could not write owned export")
            // Provider SIZE metadata may lag close/scan. Verify actual bytes instead.
            val zipDigest=MessageDigest.getInstance("SHA-256")
            temporary.inputStream().use {input ->
                val buffer=ByteArray(8192)
                while(true) {val size=input.read(buffer);if(size<0) break;zipDigest.update(buffer,0,size)}
            }
            check(contentDigest(inserted,temporary.length()).contentEquals(zipDigest.digest())) {"Written export digest mismatch"}
            checkRow(inserted,locale,1)
            check(resolver.update(inserted,ContentValues().apply {put(MediaStore.MediaColumns.IS_PENDING,0)},null,null)==1)
            checkRow(inserted,locale,0)
            uri=null // Published partial exports remain diagnostic, never complete receipts.
            check(!testPassed || complete) {"Passing test omitted required evidence"}
        } catch(error: Throwable) {
            failure=error
        } finally {
            for(cleanup in listOf<()->Unit>(
                {uri?.let {check(resolver.delete(it,null,null)==1) {"Could not remove failed owned export"}}},
                {check(temporary.delete()) {"Could not remove temporary synthetic export"}})) {
                try {cleanup()} catch(error: Throwable) {
                    if(failure==null) failure=error else failure!!.addSuppressed(error)
                }
            }
        }
        failure?.let {throw it}
    }

    companion object {
        const val OWNER="paint.anpaint.android"
        const val RELATIVE_PATH="Download/anpaint-ci-vertical-evidence/"
        const val MAX_FILE=2L*1024*1024
        const val MAX_CASE=8L*1024*1024
        const val MAX_MANIFEST=64*1024
        val METHOD_LOCALES=mapOf(
            "manchuPickerRibbonToolsAndJpegUseNativeInputInBothOrientations" to "mnc-Mong",
            "literaryChinesePickerRibbonToolsAndJpegUseNativeInputInBothOrientations" to "lzh-Hant",
            "verticalEnglishPickerRibbonToolsAndJpegUseNativeInputInBothOrientations" to "en-XV",
            "verticalEmojiPickerRibbonToolsAndJpegUseNativeInputInBothOrientations" to "qaa-Zsye-XV")
        fun paths(locale: String): List<String> {
            require(locale in METHOD_LOCALES.values)
            return listOf("portrait","landscape").flatMap {orientation ->
                val case="$locale-$orientation"
                listOf("workspace","save-initial","format-popup","jpeg-quality").map {"$case-$it.png"}+
                    listOf("before","minimum","maximum","filename","description","cancel-ready","choose-ready","returned")
                        .map {"reachability/$case-$it.png"}+"reachability/$case.json"
            }.sorted()
        }
    }
}
