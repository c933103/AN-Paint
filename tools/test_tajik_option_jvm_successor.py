"""Source binding for the real public option identity/platform roundtrip checks."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class TajikOptionJvmSuccessorTest(unittest.TestCase):
    def section(self):
        text=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/AppLanguageTest.kt').read_text()
        start=text.index('fun furtherOptionsIncludingPrincipalVarietiesKeepTheirExactIdentityAndPlatformRoundTrip()')
        return text[start:text.index('\n    @Test',start)]


    def test_identity_and_platform_round_trip_assertions_remain(self):
        section=self.section()
        for assertion in ('assertEquals(tag,AppLanguage.selectedTag(wrapped))',
                'assertEquals(tag,wrapped.resources.configuration.locales[0].toLanguageTag())',
                'assertEquals(tag,Locale.getDefault().toLanguageTag())',
                'assertEquals("$name [$tag]",AppLanguage.name(tag))',
                'assertEquals(tag,manager.applicationLocales[0].toLanguageTag())',
                'assertEquals("en-001",AppLanguage.selectedTag(context))',
                'assertEquals(tag,AppLanguage.selectedTag(context))'):
            self.assertIn(assertion,section)

if __name__=='__main__':unittest.main()
