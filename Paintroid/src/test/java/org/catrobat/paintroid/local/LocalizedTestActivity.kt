/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.Context
import org.catrobat.paintroid.classic.AppLanguage

/** Match the editor's locale override, keeping its UI owner distinct from Application. */
class LocalizedTestActivity : Activity() {
    override fun attachBaseContext(base: Context) {
        super.attachBaseContext(AppLanguage.wrap(base))
    }
}
