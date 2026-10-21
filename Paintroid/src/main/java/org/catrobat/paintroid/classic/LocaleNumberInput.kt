/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.text.InputType
import android.text.method.NumberKeyListener
import android.widget.EditText
import java.text.DecimalFormatSymbols

/** Keep selected-locale numeric syntax intact until the caller validates its value. */
internal object LocaleNumberInput {
    fun configure(view: EditText, decimal: Boolean = false) {
        @Suppress("DEPRECATION")
        val symbols = DecimalFormatSymbols(view.resources.configuration.locale)
        val digits = (0..9).map { (symbols.zeroDigit.code + it).toChar() }.joinToString("")
        // Even integer fields retain pasted fractions/signs so whole-number and
        // range checks can reject them instead of silently turning 12,5 into 125
        // or -12 into 12. This does not change a caller's parser or valid range.
        // A pasted Unicode minus must also survive in locales with ASCII minus.
        // The caller may reject that spelling, but must not receive a positive value.
        val accepted = ("0123456789.+-" + '\u2212' + digits + symbols.decimalSeparator + symbols.minusSign)
            .toSet().toCharArray()
        val keyboardType = InputType.TYPE_CLASS_NUMBER or if (decimal) InputType.TYPE_NUMBER_FLAG_DECIMAL else 0
        // TextView restarts an active IME while assigning the listener. Report
        // the final keyboard type then, not through a later setRawInputType call.
        view.keyListener = object : NumberKeyListener() {
            override fun getAcceptedChars() = accepted
            override fun getInputType() = keyboardType
        }
    }
}
