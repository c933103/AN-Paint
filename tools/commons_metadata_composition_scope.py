"""Strict projections of the composed M02/M03 delta onto each original producer.

Neither original fixture, pin nor historical whole-file endpoint is changed.
Callbacks shared by both corrections stay in place until the remaining original
producer's reversal is applied. Unknown, absent and repeated edits fail closed.
"""
from commons_metadata_m02_scope import before_m02_producer
from commons_metadata_m03_scope import production_fixture

HTTP_HELPER = '''    /** Do not classify provider/framework exceptions by their text or format their detail twice. */
    private fun commonsMetadataReason(error: Exception): String? =
        if(error is CommonsAttribution.HttpException) ui(R.string.commons_metadata_http_error,error.status.toString())
        else error.message

'''
LIMIT_BRANCH = '        else if(error is CommonsAttribution.ResponseLimitException) ui(R.string.commons_metadata_response_too_large)\n'
COMBINED_HELPER = HTTP_HELPER.replace('        else error.message\n', LIMIT_BRANCH + '        else error.message\n')


def replace_once(path, text, old, new):
    if not old or text.count(old) != 1:
        raise AssertionError(f'{path}: expected one exact composed metadata edit')
    return text.replace(old, new, 1)


def without_m03_production(path, text):
    """Project onto accepted M02 source, keeping its two UI callbacks verbatim."""
    if path.endswith('/CommonsAttribution.kt'):
        row = next(row for row in production_fixture()['entries'] if row['path'] == path)
        for edit in reversed(row['edits']):
            text = replace_once(path, text, edit['after'], edit['before'])
    elif path.endswith('/MediaGalleryActivity.kt'):
        text = replace_once(path, text, COMBINED_HELPER, HTTP_HELPER)
    return text


def without_m02_production(path, text):
    """Project onto merged M03 source, keeping its two UI callbacks verbatim."""
    if path.endswith('/CommonsAttribution.kt'):
        return before_m02_producer(path, text.encode()).decode()
    if path.endswith('/MediaGalleryActivity.kt'):
        text = replace_once(path, text, COMBINED_HELPER, '')
        row = next(row for row in production_fixture()['entries'] if row['path'] == path)
        edit = row['edits'][0]
        text = replace_once(path, text, edit['before'], edit['after'])
    return text
