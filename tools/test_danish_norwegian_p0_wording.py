"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from collections import Counter
from current_localization_contracts import require_string, current_display


FULL_FORMAT_TOKEN = re.compile(
    r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?'
    r'(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')

def full_format_tokens(value):
    """Parse indexed/unindexed and non-argument tokens; reject any leftover %."""
    if '%' in FULL_FORMAT_TOKEN.sub('', value):
        raise ValueError('Invalid or unescaped format token')
    return Counter(FULL_FORMAT_TOKEN.findall(value))

def require_reviewed_string(xml, key, expected, constraints, source):
    """Keep complete text and full token inventory, even with formatted=false."""
    value = require_string(xml, key, expected, constraints)
    if full_format_tokens(value) != full_format_tokens(source):
        raise ValueError(key + ': complete format-token inventory differs')
    return value



class DanishNorwegianP0Tests(unittest.TestCase):

    def test_full_format_tokens_reject_changed_index_type_precision_width_flags_and_literals(self):
        key = 'message'
        source = '%1$d × %2$d pixels (%3$.2f MP), limit %4$.2f MP'
        self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$.2f': 1, '%4$.2f': 1}, full_format_tokens(source))
        mutations = [source.replace('%3$.2f', replacement) for replacement in
                     ('%3$.3f', '%9$.2f', '%3$.2d', '%.2f', '%3$f', '%3$2f', '%3$-10.2f', '%3$', '%3$.f', '%q')]
        mutations += [source + token for token in (' %9$s', ' %n', ' %%', ' %')]
        for changed in mutations:
            node = ET.Element('string', name=key); node.text = changed
            root = ET.Element('resources'); root.append(node)
            with self.subTest(value=changed), self.assertRaises(ValueError):
                require_reviewed_string(ET.tostring(root, encoding='unicode'), key, changed,
                                        {'attributes': {'name': key}}, source)

    def test_formatted_false_rejects_unindexed_non_argument_and_malformed_tokens_with_refreshed_expected(self):
        recognized = ('%s', '%1$s', '%.2f', '%3$-10.2f', '%tY', '%1$tY', '%%', '%n')
        self.assertEqual(Counter(recognized), full_format_tokens(' '.join(recognized)))
        source = 'Saved image; the drawing still has changes.'
        constraints = {'attributes': {'name': 'message', 'formatted': 'false'}}
        suffixes = (' %s', ' %d', ' %.2f', ' %1$s', ' %%', ' %n',
                    ' %', ' %q', ' %1$', ' %.', ' %3$.', ' %3$.f', ' %t')
        for suffix in suffixes:
            changed = source + suffix
            node = ET.Element('string', constraints['attributes']); node.text = changed
            root = ET.Element('resources'); root.append(node)
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                require_reviewed_string(ET.tostring(root, encoding='unicode'), 'message', changed,
                                        constraints, source)


    def test_recovery_compositions_retain_actual_labels_filenames_and_one_optional_selection(self):
        for tag, menu, optional in [('da', 'Filer', 'en eventuel flydende markering'),
                                    ('no', 'Fil', 'et eventuelt flytende utvalg')]:
            value = lambda key: current_display(tag, key)
            recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
            self.assertIn(menu + ' > ' + current_display(tag,'ui_load_image'), recovery)
            self.assertIn('canvas.png', recovery);self.assertIn('ZIP', recovery);self.assertIn(optional, recovery)
            paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
            self.assertIn(menu + ' → ' + value('ui_export_recovery_copy'), paused)
            self.assertIn(menu + ' → ' + current_display(tag, 'save20_title'), paused)
            self.assertIn(current_display(tag,'save20_file_format') + ': PNG / JPEG', paused)
            kept = value('ui_a_separate_recovery_copy_has_been_kept_use')
            self.assertIn(menu + ' > ' + value('ui_export_recovery_copy'), kept)
            self.assertIn('canvas.png', kept);self.assertIn('ZIP', kept)

    def test_save_share_and_error_composition_keeps_command_and_punctuation_contracts(self):
        for tag in ('da', 'no'):
            value = lambda key: current_display(tag, key)
            save = current_display(tag, 'ui_save')
            save_as = current_display(tag, 'save20_title')
            for key in ('ui_export_did_not_save23', 'ui_export_explanation23', 'ui_save_explanation23', 'ui_share_explanation34'):
                self.assertIn(save, value(key))
            self.assertIn(save_as, value('ui_export_did_not_save23'))
            self.assertEqual(value('ui_save_and_share_41edb4') + '…', value('ui_save_and_share'))
            self.assertEqual(value('ui_export_recovery_copy_144b8a') + '…', value('ui_export_recovery_copy'))
            for key in ('ui_could_not_save_image', 'ui_could_not_open_image', 'ui_could_not_export_the_recovery_copy',
                        'ui_not_enough_memory_to_save_in_this_format'):
                self.assertFalse(value(key).endswith(('.', ':', '…')))
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(value('ui_saved')))
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(value('ui_the_image_was_saved_but_android_could_not')))

if __name__ == '__main__':
    unittest.main()
