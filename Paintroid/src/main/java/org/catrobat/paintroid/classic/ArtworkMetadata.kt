/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

/** Shared DOM extraction for the attribution data published alongside artwork. */
internal object ArtworkMetadata {
    val script = """
        function artworkCredit(scope) {
          function value(node) {return node ? (node.getAttribute('content') || node.textContent || '').trim() : '';}
          var author=scope.querySelector('[rel~="author"],[itemprop="author"],[itemprop="creator"]');
          var licence=scope.querySelector('[rel~="license"],[itemprop="license"]');
          var authorLink=author && (author.href || (author.querySelector('a[href]') || {}).href) || '';
          var licenceText=value(licence), licenceLink=licence && (licence.href || licence.getAttribute('content')) || '';
          return '&author='+encodeURIComponent(value(author).slice(0,1024))+
            '&author_url='+encodeURIComponent(authorLink.slice(0,4096))+
            '&licence='+encodeURIComponent((licenceText+(licenceLink && licenceLink!==licenceText?' '+licenceLink:'')).slice(0,4096));
        }
    """.trimIndent()
}
