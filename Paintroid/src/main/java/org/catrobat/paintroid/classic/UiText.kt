/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Application
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import androidx.annotation.StringRes
import java.text.NumberFormat
import java.text.ParsePosition
import java.util.Locale

/** Framework locale identity and exact-catalogue UI resources follow the live app choice. */
class PaintApplication : Application() {
    // Do not pin the Application to the language that happened to be selected at startup.
    override fun attachBaseContext(base: Context) { super.attachBaseContext(base) }
    override fun getResources(): Resources = AppLanguage.applicationResources(baseContext)
    override fun onCreate() { super.onCreate(); currentResources = AppLanguage.wrap(baseContext).resources }
    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig)
        currentResources = AppLanguage.wrap(baseContext).resources
    }
    companion object { internal lateinit var currentResources: Resources }
}

internal fun ui(@StringRes id: Int, vararg values: Any?): String {
    val resources = PaintApplication.currentResources
    return if (values.isEmpty()) resources.getString(id) else resources.getString(id, *values)
}

/** Accept the device's decimal separator as well as ordinary decimal-dot input. */
internal fun uiNumber(text: String): Double? {
    val value = text.trim()
    value.toDoubleOrNull()?.let { return it.takeIf { n -> n.isFinite() } }
    val position = ParsePosition(0)
    val number = NumberFormat.getNumberInstance(Locale.getDefault()).parse(value, position)
    return number?.toDouble()?.takeIf { position.index == value.length && it.isFinite() }
}
