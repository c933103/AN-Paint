/* Pocket Paint Local additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.Manifest
import android.content.Intent
import org.catrobat.paintroid.MainActivity
import org.catrobat.paintroid.R
import org.catrobat.paintroid.common.REQUEST_CODE_LOAD_PICTURE
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class PickerLaunchTest {
    @Test fun openMenuLaunchesPickerWithPhotoPermissionDenied() {
        val controller = Robolectric.buildActivity(MainActivity::class.java, Intent(Intent.ACTION_MAIN))
        try {
            val activity = controller.setup().get()
            shadowOf(activity.application).denyPermissions(Manifest.permission.READ_MEDIA_IMAGES)
            while (shadowOf(activity).nextStartedActivityForResult != null) { /* Drain first-run help. */ }
            shadowOf(activity).clickMenuItem(R.id.pocketpaint_replace_image)
            val launch = shadowOf(activity).nextStartedActivityForResult
            assertNotNull("Open must launch a picker without a photo-library permission grant", launch)
            assertEquals(REQUEST_CODE_LOAD_PICTURE, launch.requestCode)
            assertEquals(Intent.ACTION_OPEN_DOCUMENT, launch.intent.action)
            assertTrue(launch.intent.hasCategory(Intent.CATEGORY_OPENABLE))
            assertEquals(0, launch.intent.flags and Intent.FLAG_ACTIVITY_NEW_DOCUMENT)
        } finally { controller.pause().stop().destroy() }
    }
}
