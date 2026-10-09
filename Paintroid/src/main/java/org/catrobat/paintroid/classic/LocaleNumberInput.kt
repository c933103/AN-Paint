/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.text.InputType
import android.text.method.DigitsKeyListener
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
        val accepted = ("0123456789.+-" + digits + symbols.decimalSeparator + symbols.minusSign)
            .toSet().joinToString("")
        view.keyListener = DigitsKeyListener.getInstance(accepted)
        // The explicit-character listener otherwise requests a text keyboard.
        // Raw input type preserves that listener while retaining the caller's IME mode.
        view.setRawInputType(InputType.TYPE_CLASS_NUMBER or if (decimal) InputType.TYPE_NUMBER_FLAG_DECIMAL else 0)
    }
}
