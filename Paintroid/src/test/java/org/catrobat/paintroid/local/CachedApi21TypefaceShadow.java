/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local;

import android.graphics.Typeface;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Map;
import org.robolectric.annotation.Implementation;
import org.robolectric.annotation.Implements;
import org.robolectric.annotation.Resetter;
import org.robolectric.shadows.ShadowLegacyTypeface;

/** API21's real Typeface.create returns the same face for its own style and caches
 * derived styles. The legacy shadow always allocates, making global-layout font
 * installation schedule layouts indefinitely. Preserve the legacy family/style
 * behavior and add only framework identity caching. This is not glyph rendering.
 */
@Implements(value=Typeface.class, isInAndroidSdk=false)
public class CachedApi21TypefaceShadow extends ShadowLegacyTypeface {
    private static final Map<Typeface,Map<Integer,Typeface>> STYLES=new IdentityHashMap<>();

    @Implementation(methodName="create")
    protected static Typeface createCached(Typeface family, int requestedStyle) {
        int style=requestedStyle>=Typeface.NORMAL && requestedStyle<=Typeface.BOLD_ITALIC
                ? requestedStyle : Typeface.NORMAL;
        if(family!=null && family.getStyle()==style) return family;
        return STYLES.computeIfAbsent(family, unused -> new HashMap<>())
                .computeIfAbsent(style, unused -> ShadowLegacyTypeface.create(family,style));
    }

    @Resetter
    public static void resetStyles() {STYLES.clear();}
}
