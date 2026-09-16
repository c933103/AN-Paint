/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.json.JSONObject

/** Add app actions only to artwork links on a source's detail page. No JS/native bridge. */
internal object IllustrationPage {
    const val USE_SCHEME="anpaint-gallery-use"
    fun script(provider: IllustrationSource,useLabel: String,copyLabel: String): String {
        if(provider==IllustrationSource.CATROBAT) return GalleryPage.script(useLabel,copyLabel)
        return """
            (function() {
              var provider=${JSONObject.quote(provider.name)}, use=${JSONObject.quote(useLabel)}, copy=${JSONObject.quote(copyLabel)};
              function url(value) {
                try {
                  var u=new URL(value,location.href);
                  if(u.protocol==='http:' && ['blogger.googleusercontent.com','1.bp.blogspot.com','2.bp.blogspot.com','3.bp.blogspot.com','4.bp.blogspot.com','openclipart.org','www.openclipart.org'].indexOf(u.hostname)>=0) u.protocol='https:';
                  return u;
                } catch(e) { return null; }
              }
              function accepted(u) {
                if(!u || u.protocol!=='https:' || u.username || u.password || (u.port && u.port!=='443')) return false;
                if(provider==='IRASUTOYA') return ['blogger.googleusercontent.com','1.bp.blogspot.com','2.bp.blogspot.com','3.bp.blogspot.com','4.bp.blogspot.com'].indexOf(u.hostname)>=0 && /\.(png|jpe?g|webp|gif)$/i.test(u.pathname);
                return ['openclipart.org','www.openclipart.org'].indexOf(u.hostname)>=0 && /^\/image\/(400|800|2000)px\/[0-9]+\/?${'$'}/.test(u.pathname);
              }
              function add(anchor,title) {
                var u=url(anchor.href); if(!accepted(u)) return;
                var row=anchor.nextElementSibling;
                if(!row || !row.hasAttribute('data-anpaint-actions')) {
                  row=document.createElement('div'); row.setAttribute('data-anpaint-actions','true');
                  row.style.cssText='display:flex;flex-wrap:wrap;gap:8px;margin:10px 0';
                  anchor.insertAdjacentElement('afterend',row);
                }
                [use,copy].forEach(function(label,i) {
                  var link=row.children[i];
                  if(!link) { link=document.createElement('a');link.style.cssText='display:inline-block;padding:12px;background:#e9ddff;color:#21005d;border:1px solid #6750a4;border-radius:4px;font:16px sans-serif';row.appendChild(link); }
                  var target=(i===0?'$USE_SCHEME://insert':'${GalleryPage.CREDIT_SCHEME}://copy')+'?source='+encodeURIComponent(u.href)+'&page='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(title);
                  if(link.getAttribute('href')!==target) link.setAttribute('href',target);
                  if(link.textContent!==label) link.textContent=label;
                });
              }
              function adapt() {
                if(provider==='IRASUTOYA') {
                  if(!/^\/[0-9]{4}\/[0-9]{2}\/[^/]+\.html${'$'}/.test(location.pathname)) return;
                  document.querySelectorAll('.entry a[href],.post-body a[href]').forEach(function(a) {
                    var img=a.querySelector('img');if(img) add(a,img.alt || document.title);
                  });
                } else if(location.pathname.indexOf('/detail/')===0) {
                  var title=document.querySelector('h2');
                  // The publisher's Large PNG action supplies 2000 px, rather than importing an SVG as a bitmap.
                  document.querySelectorAll('a[href*="/image/2000px/"]').forEach(function(a) {add(a,title?title.textContent.trim():document.title);});
                }
              }
              adapt();
              if(window.anPaintIllustrationObserver) window.anPaintIllustrationObserver.disconnect();
              window.anPaintIllustrationObserver=new MutationObserver(adapt);
              window.anPaintIllustrationObserver.observe(document.body,{childList:true,subtree:true});
            })();
        """.trimIndent()
    }

    /** Reuse Irasutoya's own English-search form, including its submit handler and current parameters. */
    fun searchIrasutoya(query: String): String="""
        (function(){var field=document.querySelector('input[placeholder="Search in English"]');
        if(!field || !field.form) return false;
        field.value=${JSONObject.quote(query)};
        var button=field.form.querySelector('button[type="submit"]');
        if(button) button.click();else if(field.form.requestSubmit) field.form.requestSubmit();else field.form.submit();return true;})();
    """.trimIndent()
}
