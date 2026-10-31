"""Shared current-resource checks for Assembly Help semantic regressions."""
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

KEY = 'ui_add_up_to_20_images_with_android_s'

def current_help(directory):
    root = ET.parse(catalogues.RES / directory / 'strings.xml').getroot()
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY} or len(nodes[0]):
        raise ValueError('Expected unique child-free Assembly Help resource')
    text = nodes[0].text or ''
    return text, text.split(r'\n\n')

def check_current_help(test, directory, captions):
    text, paragraphs = current_help(directory)
    test.assertTrue(text)
    test.assertTrue(all(paragraphs))
    test.assertFalse(catalogues.placeholders(text))
    test.assertEqual([], catalogues.android_string_errors(text))
    test.assertNotIn('\ufffd', text)
    test.assertNotIn('\r', text)
    for literal in ('Catrobat', 'AGPL'):
        test.assertIn(literal, text)
    values = catalogues.read_strings(catalogues.RES / directory / 'strings.xml')
    for index, key in captions:
        with test.subTest(caption=key):
            test.assertTrue(values[key])
            test.assertIn(values[key], text if index is None else paragraphs[index])
