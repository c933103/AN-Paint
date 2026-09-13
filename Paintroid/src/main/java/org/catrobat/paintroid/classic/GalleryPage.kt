/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.json.JSONObject

/** Adapt only the gallery's WordPress image-download actions, not its artwork names or prose. */
internal object GalleryPage {
    const val CREDIT_SCHEME="anpaint-gallery-credit"
    fun script(useLabel: String, copyLabel: String): String = """
        (function() {
          var useLabel=${JSONObject.quote(useLabel)}, copyLabel=${JSONObject.quote(copyLabel)};
          function adapt() {
            document.querySelectorAll('a.wp-block-file__button[download]').forEach(function(link) {
              var url; try { url=new URL(link.href); } catch(e) { return; }
              if(url.protocol!=='https:' || ['catrobat.org','www.catrobat.org','catrobatblog.files.wordpress.com','catrobatblog.wpcomstaging.com'].indexOf(url.hostname)<0 || !/\.(png|jpe?g|webp|gif|jxl|bmp|dib|ico|tiff?|heic|avif)$/i.test(url.pathname)) return;
              if(link.textContent!==useLabel) link.textContent=useLabel;
              link.setAttribute('aria-label',useLabel);
              var copy=link.parentElement.querySelector('[data-anpaint-credit]');
              if(!copy) {
                copy=document.createElement('a');copy.setAttribute('data-anpaint-credit','true');
                copy.className=link.className;
                copy.style.marginLeft='0.5em';link.insertAdjacentElement('afterend',copy);
              }
              var titleNode=document.getElementById(link.getAttribute('aria-describedby'));
              var title=titleNode ? titleNode.textContent.trim() : url.pathname.split('/').pop();
              var target='$CREDIT_SCHEME://copy?source='+encodeURIComponent(url.href)+'&title='+encodeURIComponent(title);
              if(copy.getAttribute('href')!==target) copy.setAttribute('href',target);
              if(copy.textContent!==copyLabel) copy.textContent=copyLabel;
            });
          }
          adapt();
          if(window.anPaintGalleryObserver) window.anPaintGalleryObserver.disconnect();
          window.anPaintGalleryObserver=new MutationObserver(adapt);
          window.anPaintGalleryObserver.observe(document.body,{childList:true,subtree:true});
        })();
    """.trimIndent()
}
