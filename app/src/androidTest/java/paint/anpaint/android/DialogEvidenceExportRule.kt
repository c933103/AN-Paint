/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Instrumentation
import android.content.ContentUris
import android.content.ContentValues
import android.os.Build
import android.os.SystemClock
import android.provider.MediaStore
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.uiautomator.UiDevice
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

/** Bounded, app-owned synthetic CI evidence, including partial failures.
 * A source digest supplied by the runner is a binding, not proof of a passing test.
 * The host collector must compare it with its exact-source instrumentation report.
 */
class DialogEvidenceExportRule(private val instrumentation: Instrumentation): TestRule {
    private val context get()=instrumentation.targetContext
    private val resolver get()=context.contentResolver
    private val collection get()=MediaStore.Downloads.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
    private lateinit var cacheRoot: File
    private lateinit var directory: File
    private lateinit var receipt: JSONObject
    private var captureIndex=0

    override fun apply(base: Statement,description: Description): Statement=object: Statement() {
        override fun evaluate() {
            check(context.packageName==OWNER && Build.VERSION.SDK_INT==35)
            check(description.className=="paint.anpaint.android.LocalizedDialogDeviceTest")
            check(description.methodName in METHODS)
            // Android may return /data/user/0/... while its canonical cache is
            // /data/data/.... Normalize this trusted platform root ONLY; aliases
            // in our controlled descendants must still fail closed.
            val requestedCache=context.cacheDir.absoluteFile
            cacheRoot=requestedCache.canonicalFile
            check(cacheRoot.isDirectory) {"Missing Android cache: requested=$requestedCache canonical=$cacheRoot"}
            android.util.Log.i("LocalizedDialogDeviceTest",JSONObject().put("kind","evidence-cache-root")
                .put("requested",requestedCache.path).put("canonical",cacheRoot.path).toString())
            directory=File(cacheRoot,"dialog-evidence/${description.methodName}")
            checkEvidenceDirectory()
            clearEvidenceDirectory()
            check(directory.mkdirs()) {"Cannot create owned evidence directory: $directory"}
            checkEvidenceDirectory()
            val supplied=InstrumentationRegistry.getArguments().getString("anpaint_source_tests_sha256")
            check(supplied==null || supplied.matches(Regex("[0-9a-f]{64}")))
            val info=context.packageManager.getPackageInfo(OWNER,0)
            receipt=JSONObject().put("schema",1).put("test_class",description.className)
                .put("test_method",description.methodName).put("device_sdk",Build.VERSION.SDK_INT)
                .put("fingerprint",Build.FINGERPRINT).put("package",OWNER)
                .put("version_name",info.versionName).put("version_code",info.longVersionCode)
                .put("source_tests_sha256",supplied ?: JSONObject.NULL)
                .put("source_binding",if(supplied==null) "unbound-needs-host-summary" else "runner-supplied-needs-host-comparison")
                .put("observations",JSONArray()).put("screenshots",JSONArray()).put("outcome","running")
            val started=SystemClock.uptimeMillis()
            var failure: Throwable?=null
            try {base.evaluate();receipt.put("outcome","passed")} catch(error: Throwable) {
                failure=error;receipt.put("outcome","failed").put("failure",error.toString())
                try {capture("failure")} catch(capture: Throwable) {error.addSuppressed(capture)}
            }
            receipt.put("fixture_elapsed_ms",SystemClock.uptimeMillis()-started)
            try {write();export(description.methodName)} catch(error: Throwable) {
                if(failure==null) failure=error else failure!!.addSuppressed(error)
            }
            // No test data is left in internal cache after the immutable export.
            try {clearEvidenceDirectory()} catch(error: Throwable) {
                if(failure==null) failure=error else failure!!.addSuppressed(error)
            }
            failure?.let {throw it}
        }
    }

    fun observe(value: JSONObject) {
        check(receipt.getJSONArray("observations").length()<512)
        receipt.getJSONArray("observations").put(value);write()
        android.util.Log.i("LocalizedDialogDeviceTest",value.toString())
    }
    fun capture(label: String) {
        check(label.matches(Regex("[A-Za-z0-9_-]+")) && captureIndex<20)
        val name="${captureIndex++}-$label.png"
        val file=evidenceFile(name)
        check(UiDevice.getInstance(instrumentation).takeScreenshot(file) && file.length() in 1..MAX_FILE)
        receipt.getJSONArray("screenshots").put(name);write()
    }
    private fun write() {evidenceFile("receipt.json").writeText(receipt.toString(2)+"\n")}

    private fun checkConfined(file: File) {
        val expected=file.absoluteFile
        val actual=file.canonicalFile
        check(!Files.isSymbolicLink(file.toPath()) && actual==expected &&
            actual.toPath().startsWith(cacheRoot.toPath()) && actual!=cacheRoot) {
            "Noncanonical or linked evidence descendant: expected=$expected actual=$actual root=$cacheRoot"
        }
    }
    private fun checkEvidenceDirectory() {
        // Check both components, including dangling links and links that resolve
        // back inside cacheRoot. Canonicalizing the final child would hide these.
        checkConfined(File(cacheRoot,"dialog-evidence"));checkConfined(directory)
    }
    private fun evidenceFile(name: String): File {
        check(name=="receipt.json" || name.matches(Regex("[0-9]+-[A-Za-z0-9_-]+\\.png")))
        checkEvidenceDirectory()
        return File(directory,name).also {checkConfined(it)}
    }
    private fun evidenceFiles(): List<File> {
        checkEvidenceDirectory()
        val files=checkNotNull(directory.listFiles()) {"Cannot list owned evidence directory: $directory"}.sortedBy {it.name}
        check(files.size<=21 && files.sumOf {it.length()}<=MAX_CASE) {"Unbounded owned evidence directory: $directory"}
        for(file in files) {
            check(file==evidenceFile(file.name) && file.isFile && file.length() in 0..MAX_FILE) {
                "Nonregular or oversized evidence child: $file"
            }
        }
        return files
    }
    private fun clearEvidenceDirectory() {
        checkEvidenceDirectory()
        if(!directory.exists()) return
        // Never recurse through a descendant. Validate the complete bounded,
        // app-owned flat inventory before deleting any of its regular files.
        val files=evidenceFiles()
        files.forEach {check(it.delete()) {"Cannot clear owned evidence file: $it"}}
        check(directory.delete()) {"Cannot clear owned evidence directory: $directory"}
    }

    private fun export(method: String) {
        val selection="${MediaStore.MediaColumns.RELATIVE_PATH} = ? AND ${MediaStore.MediaColumns.DISPLAY_NAME} = ? AND ${MediaStore.MediaColumns.OWNER_PACKAGE_NAME} = ?"
        @Suppress("DEPRECATION") val pending=MediaStore.setIncludePending(collection)
        val ids=mutableListOf<Long>()
        resolver.query(pending,arrayOf(MediaStore.MediaColumns._ID),selection,
            arrayOf(RELATIVE_PATH,"$method.zip",OWNER),null)?.use {cursor ->
            while(cursor.moveToNext()) {check(ids.size<16);ids.add(cursor.getLong(0))}
        } ?: error("Cannot query owned dialog export")
        ids.forEach {check(resolver.delete(ContentUris.withAppendedId(collection,it),null,null)==1)}
        val files=evidenceFiles()
        check(files.size in 1..21 && files.sumOf {it.length()}<=MAX_CASE)
        val manifest=JSONObject().put("schema",1).put("owner",OWNER).put("method",method)
            .put("device_sdk",Build.VERSION.SDK_INT).put("test_passed",receipt.getString("outcome")=="passed")
            .put("files",JSONArray())
        val temporary=File.createTempFile("dialog-export-",".zip",cacheRoot)
        var uri: android.net.Uri?=null
        try {
            ZipOutputStream(temporary.outputStream().buffered()).use {zip ->
                for(file in files) {
                    check(!Files.isSymbolicLink(file.toPath()) && file.isFile && file.length() in 1..MAX_FILE)
                    val bytes=file.readBytes();check(bytes.size.toLong()==file.length())
                    val digest=sha256(bytes)
                    zip.putNextEntry(ZipEntry(file.name));zip.write(bytes);zip.closeEntry()
                    manifest.getJSONArray("files").put(JSONObject().put("path",file.name)
                        .put("bytes",bytes.size).put("sha256",digest))
                }
                zip.putNextEntry(ZipEntry("manifest.json"));zip.write((manifest.toString()+"\n").toByteArray());zip.closeEntry()
            }
            check(temporary.length() in 1..MAX_CASE)
            val inserted=resolver.insert(collection,ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME,"$method.zip")
                put(MediaStore.MediaColumns.RELATIVE_PATH,RELATIVE_PATH)
                put(MediaStore.MediaColumns.MIME_TYPE,"application/zip")
                put(MediaStore.MediaColumns.IS_PENDING,1)
            }) ?: error("Cannot insert owned dialog export")
            uri=inserted
            fun verifyRow(expectedPending: Int) {
                resolver.query(inserted,arrayOf(MediaStore.MediaColumns.DISPLAY_NAME,MediaStore.MediaColumns.RELATIVE_PATH,
                    MediaStore.MediaColumns.OWNER_PACKAGE_NAME,MediaStore.MediaColumns.IS_PENDING),null,null,null)?.use {
                    check(it.count==1 && it.moveToFirst() && it.getString(0)=="$method.zip" &&
                        it.getString(1)==RELATIVE_PATH && it.getString(2)==OWNER && it.getInt(3)==expectedPending)
                } ?: error("Cannot verify owned export")
            }
            verifyRow(1)
            resolver.openOutputStream(inserted,"w")?.use {out ->
                temporary.inputStream().use {check(it.copyTo(out)==temporary.length())}
            } ?: error("Cannot write owned dialog export")
            val expected=sha256(temporary.readBytes())
            val actual=resolver.openInputStream(inserted)?.use {input ->
                val digest=MessageDigest.getInstance("SHA-256");val buffer=ByteArray(8192);var count=0L
                while(true) {val n=input.read(buffer);if(n<0) break;count+=n;check(count<=temporary.length());digest.update(buffer,0,n)}
                check(count==temporary.length());hex(digest.digest())
            }
            check(actual==expected)
            check(resolver.update(inserted,ContentValues().apply {put(MediaStore.MediaColumns.IS_PENDING,0)},null,null)==1)
            verifyRow(0);uri=null
        } finally {
            try {uri?.let {check(resolver.delete(it,null,null)==1)}} finally {check(temporary.delete())}
        }
    }
    private fun sha256(bytes: ByteArray)=hex(MessageDigest.getInstance("SHA-256").digest(bytes))
    private fun hex(bytes: ByteArray)=bytes.joinToString("") {"%02x".format(it.toInt() and 255)}
    companion object {
        const val OWNER="paint.anpaint.android"
        const val RELATIVE_PATH="Download/anpaint-ci-dialog-evidence/"
        const val MAX_FILE=2L*1024*1024
        const val MAX_CASE=24L*1024*1024
        val METHODS=setOf("normalAdvancedColourKeepsFiniteViewportAndFixedControls")
    }
}
