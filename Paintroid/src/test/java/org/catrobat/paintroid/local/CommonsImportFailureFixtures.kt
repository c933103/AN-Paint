/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.ContextWrapper
import android.content.SharedPreferences
import android.graphics.Bitmap
import org.robolectric.annotation.Implementation
import org.robolectric.annotation.Implements
import org.robolectric.annotation.RealObject
import org.robolectric.annotation.Resetter
import org.robolectric.shadow.api.Shadow
import org.robolectric.shadows.ShadowNativeBitmap
import org.robolectric.util.ReflectionHelpers.ClassParameter
import java.io.OutputStream

/** Refuse only the metadata cache commit; leave the rest of the gallery/session storage real. */
internal class CommonsCacheFailureContext(base: Context): ContextWrapper(base) {
    var reject=true
    var refusedCommits=0
    override fun getSharedPreferences(name: String,mode: Int): SharedPreferences {
        val actual=super.getSharedPreferences(name,mode)
        if(name!="commons-attribution-v1") return actual
        return object: SharedPreferences by actual {
            override fun edit(): SharedPreferences.Editor {
                val editor=actual.edit()
                return object: SharedPreferences.Editor by editor {
                    // Return this wrapper so the production fluent call cannot bypass commit().
                    override fun putString(key: String,value: String?): SharedPreferences.Editor {
                        editor.putString(key,value);return this
                    }
                    override fun commit(): Boolean {
                        if(reject) {refusedCommits++;return false}
                        return editor.commit()
                    }
                }
            }
        }
    }
}

/** Test-only false PNG result; other Bitmap work uses Robolectric's native implementation. */
@Implements(Bitmap::class,callNativeMethodsByDefault=true)
class CommonsPngFailureShadow: ShadowNativeBitmap() {
    @RealObject private lateinit var bitmap: Bitmap
    @Implementation protected fun compress(format: Bitmap.CompressFormat,quality: Int,stream: OutputStream): Boolean {
        if(reject && format==Bitmap.CompressFormat.PNG) {
            rejectedBitmap=bitmap;rejectedStream=stream;return false
        }
        return Shadow.directlyOn(bitmap,Bitmap::class.java,"compress",
            ClassParameter.from(Bitmap.CompressFormat::class.java,format),
            ClassParameter.from(Int::class.javaPrimitiveType!!,quality),
            ClassParameter.from(OutputStream::class.java,stream))
    }
    companion object {
        @Volatile var reject=false
        @Volatile var rejectedBitmap: Bitmap?=null
        @Volatile var rejectedStream: OutputStream?=null
        @JvmStatic @Resetter fun resetFailure() {reject=false;rejectedBitmap=null;rejectedStream=null}
    }
}
