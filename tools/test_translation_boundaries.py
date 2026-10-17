"""Positive and negative controls for the lexical production source policy."""
from pathlib import Path
import tempfile
import unittest
import check_translation_boundaries as guard


class TranslationBoundaryPolicyTest(unittest.TestCase):
    def test_translated_templates_cannot_reach_raw_formatters(self):
        cases = [
            'String.format(Locale.ROOT, ui(R.string.label), value)',
            'String /* note */ . format(\n Locale.ROOT,\n ui(R.string.label), value\n)',
            'val translated = context.getString(R.string.label)\nString.format(translated, value)',
            'val first = ui(R.string.label); val second = first; String.format(second, value)',
            'ui(R.string.label).format(value)',
            'val translated = ui(R.string.label); translated.format(value)',
            'val translated = ui(R.string.label); translated.formatted(value)',
            '"${ui(R.string.label)}".format(value)',
            '"""$translated""".format(value)',
            '"value: ${String.format(ui(R.string.label), value)}"',
            'import java.lang.String.format as render\nrender(ui(R.string.label), value)',
            'import kotlin.text.format as render\nui(R.string.label).render(value)',
            'val formatter = String::format',
            'val formatter = translated::format',
            'DateFormat.getDateInstance().toString().plus(ui(R.string.label)).format(value)',
            'fun a(locale: Locale) {}\nfun b(locale: String) { String.format(locale, "%s") }',
            'String.format(Locale.getDefault().toString() + ui(R.string.label), "%s")',
            'fun f(locale: Locale) { String.format(locale.toString() + ui(R.string.label), "%s") }',
        ]
        for source in cases:
            with self.subTest(source=source): self.assertTrue(guard.check_source(source, 'app/src/debug/kotlin/elsewhere/View.kt'))

    def test_java_and_static_imports_are_checked(self):
        for source in [
            'String translated = context.getString(R.string.label);\njava.lang.String.format(\n translated, value);',
            'import static java.lang.String.format;\nclass View { String text() { return format(translated, value); } }',
            'import static java.lang.String.*;\nclass View { String text() { return format(translated, value); } }',
            'context.getString(R.string.label, value);',
            'resources.getQuantityString(R.plurals.count, quantity, quantity);',
        ]:
            with self.subTest(source=source): self.assertTrue(guard.check_source(source, 'other/src/release/java/elsewhere/View.java'))

    def test_android_resource_formatting_and_callable_aliases_use_boundary(self):
        for source in [
            'resources.getString(R.string.label, value)',
            'context.getString(\n id,\n *values\n)',
            'getString(id, values)',
            'context.resources.getQuantityString(id, count)',
            'resources.getQuantityText(id, count)',
            'val retrieve = context::getString',
            'fun storage(key: String) {}\nfun display(key: Int) { context.getString(key, value) }',
            'fun storage(key: String) {}\nfun display() { val key = R.string.label; context.getString(key, value) }',
            'context.getString("key".length, value)',
        ]:
            with self.subTest(source=source): self.assertTrue(guard.check_source(source, 'library/src/main/kotlin/View.kt'))
        self.assertFalse(guard.check_source('resources.getString(id, *values)', guard.RESOURCE_BOUNDARY))
        self.assertFalse(guard.check_source('String.format(locale, candidate, *values)', guard.FORMAT_BOUNDARY))
        self.assertTrue(guard.check_source('String.format(locale, candidate, *values)', guard.RESOURCE_BOUNDARY))
        self.assertTrue(guard.check_source('resources.getString(id, *values)', guard.FORMAT_BOUNDARY))
        self.assertTrue(guard.check_source('String.format(candidate, value)', 'app/src/main/kotlin/LocaleText.kt'))

    def test_literals_nonformat_storage_and_other_formatters_remain_allowed(self):
        source = '''
            // String.format(ui(R.string.fake), x)
            /* outer /* nested */ String.format(ui(R.string.fake), x) */
            val example = "String.format(translated, value)"
            val rawExample = """translated.format(value)"""
            val quote = '\"'
            String.format(Locale.ROOT, "#%06X", value)
            String.format(Locale.getDefault(), if (whole) "%.0f" else "%.2f", value)
            String.format("prefix: " + "%s", ui(R.string.label))
            "%02x".format(value)
            "value: ${String.format(Locale.ROOT, "%s", ui(R.string.label))}"
            val KEY = "key"
            fun read(key: String, locale: Locale) {
                preferences.getString(KEY, "")
                preferences.getString(key, null)
                bundle.getString("key", "fallback")
                json.getString("name")
                cursor.getString(columnIndex)
                String.format(locale, "%s", value)
            }
            DateFormat.getDateTimeInstance(DateFormat.SHORT, DateFormat.SHORT).format(Date(time))
            java.text.NumberFormat.getNumberInstance(Locale.ROOT).format(17)
            fun format(value: Double) = String.format(Locale.ROOT, "%.4f", value)
            format(value)
        '''
        self.assertEqual([], guard.check_source(source, 'Paintroid/src/main/java/Example.kt'))
        self.assertEqual([], guard.check_source('String.format(Locale.ROOT, whole ? "%.0f" : "%.2f", value);', 'app/src/main/java/Example.java'))
        self.assertEqual([], guard.check_source('import java.lang.String as JString\nJString.format("%s", ui(R.string.label))', 'app/src/main/java/Example.kt'))

    def test_all_packages_variants_languages_and_generated_sources_are_discovered(self):
        production = [
            'app/src/main/java/example/View.java',
            'Paintroid/src/freeRelease/kotlin/new/package/View.kt',
            'newlibrary/src/debug/java/elsewhere/View.kt',
            'newlibrary/build/generated/source/producer/debug/View.java',
            'newlibrary/custom-source/View.kt',
        ]
        excluded = ['app/src/test/java/View.java', 'Paintroid/src/androidTest/kotlin/View.kt',
                    'Paintroid/src/testFreeRelease/java/View.java', 'tools/Example.java',
                    'newlibrary/build/generated/ksp/debugUnitTest/kotlin/View.kt']
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in production + excluded:
                path = root/name; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('String.format(translated, value)')
            extra = ['newlibrary/custom-source']
            found = {path.relative_to(root).as_posix() for path in guard.production_sources(root, extra)}
            self.assertEqual(set(production), found)
            self.assertEqual(len(production), len(guard.check_repository(root, extra)))
            self.assertIn('Missing explicitly configured source root', guard.check_repository(root,['absent'])[0])
