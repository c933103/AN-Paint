"""Execute the production JDK generator; source derivation is not linguistic acceptance."""
from pathlib import Path
import copy
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'tools/SourceTextResources.java'
PREFIX='anpaint_source_'


class SourceTextResourcesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary=tempfile.TemporaryDirectory(prefix='anpaint-source-text-')
        cls.classes=Path(cls.temporary.name)/'classes'
        cls.java=shutil.which('java')
        if cls.java is None: raise RuntimeError('Java is required for source text generation')
        subprocess.run([cls.java,'-m','jdk.compiler/com.sun.tools.javac.Main','-d',str(cls.classes),str(SOURCE)],check=True,capture_output=True)

    @classmethod
    def tearDownClass(cls): cls.temporary.cleanup()

    def run_generator(self,res,output,*overlays):
        return subprocess.run([self.java,'-cp',str(self.classes),'SourceTextResources',str(res),str(output),*[str(path) for path in overlays]],capture_output=True,text=True,timeout=30)

    def test_actual_catalogue_has_complete_text_and_exact_source_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'output'
            result=self.run_generator(ROOT/'Paintroid/src/main/res',output)
            self.assertEqual(0,result.returncode,result.stderr)
            original=ET.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot()
            generated=ET.parse(output/'values/source_text.xml').getroot()
            self.assertEqual(len(original),len(generated))
            for source,actual in zip(original,generated):
                expected=copy.deepcopy(source)
                expected.set('name',PREFIX+source.get('name'))
                expected.set('translatable','false')
                for node in expected.iter():
                    if node.text and node.text.strip().startswith('@string/'):
                        node.text=node.text.replace('@string/','@string/'+PREFIX,1)
                self.assertEqual(ET.canonicalize(ET.tostring(expected,encoding="unicode")),
                                 ET.canonicalize(ET.tostring(actual,encoding="unicode")),source.get('name'))
            import verify_exact_script_generation as probe
            # The independent derivation also checks every generated format flag.
            with tempfile.TemporaryDirectory() as check:
                root=Path(check)
                shutil.copytree(ROOT/'Paintroid/src/main/res/values',root/'Paintroid/src/main/res/values')
                shutil.copytree(output,root/probe.SOURCE_GENERATED)
                probe.source_text_hashes(root)
            (output/'stale.xml').write_text('<resources/>')
            self.assertEqual(0,self.run_generator(ROOT/'Paintroid/src/main/res',output).returncode)
            self.assertFalse((output/'stale.xml').exists())

    def test_generation_probe_rejects_missing_changed_or_stale_source_output(self):
        import verify_exact_script_generation as probe
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);res=root/'Paintroid/src/main/res';(res/'values').mkdir(parents=True)
            source=res/'values/strings.xml'
            source.write_text('<resources><string name="a">Complete warning. Keep the image unchanged.</string></resources>')
            output=root/probe.SOURCE_GENERATED
            self.assertEqual(0,self.run_generator(res,output).returncode)
            probe.source_text_hashes(root)
            generated=output/'values/source_text.xml';original=generated.read_bytes()
            generated.write_bytes(original.replace(b'Keep the image unchanged.',b''))
            with self.assertRaises(AssertionError):probe.source_text_hashes(root)
            generated.write_bytes(original)
            metadata=output/'values/source_text_contracts.xml'
            contract=metadata.read_bytes()
            metadata.write_bytes(contract.replace(b'true',b'false'))
            with self.assertRaises(AssertionError):probe.source_text_hashes(root)
            metadata.write_bytes(contract)
            (output/'stale.xml').write_text('<resources/>')
            with self.assertRaises(AssertionError):probe.source_text_hashes(root)
            (output/'stale.xml').unlink();generated.unlink()
            with self.assertRaises(AssertionError):probe.source_text_hashes(root)
        good=f'> Task {probe.SOURCE_GENERATOR}\n> Task {probe.MERGES[0]}\n'
        probe.require_generation_before(good,[probe.MERGES[0]],generator=probe.SOURCE_GENERATOR)
        with self.assertRaises(AssertionError):
            probe.require_generation_before(good.replace(probe.SOURCE_GENERATOR,probe.GENERATOR),[probe.MERGES[0]],generator=probe.SOURCE_GENERATOR)

    def test_aliases_plural_references_and_source_input_regeneration(self):
        with tempfile.TemporaryDirectory() as tmp:
            res=Path(tmp)/'res';output=Path(tmp)/'output';(res/'values').mkdir(parents=True)
            source=res/'values/strings.xml'
            source.write_text('<resources><string name="one">One %1$s</string><string name="other" formatted="false">Many %1$s</string><string name="alias">@string/one</string><string name="plain_alias">@string/other</string><string name="forced_plain_alias" formatted="false">@string/one</string><plurals name="count"><item quantity="one">@string/alias</item><item quantity="other">@string/other</item></plurals></resources>')
            self.assertEqual(0,self.run_generator(res,output).returncode)
            root=ET.parse(output/'values/source_text.xml').getroot()
            self.assertEqual('@string/anpaint_source_alias',root.find('plurals/item').text)
            self.assertEqual('@string/anpaint_source_one',root.find("string[@name='anpaint_source_alias']").text)
            contracts=ET.parse(output/'values/source_text_contracts.xml').getroot()
            flags={entry.get('name'): ''.join(entry.itertext()) for entry in contracts}
            self.assertEqual('true',flags['anpaint_source_contract_string_alias'])
            self.assertEqual('false',flags['anpaint_source_contract_string_other'])
            self.assertEqual('false',flags['anpaint_source_contract_string_plain_alias'])
            self.assertEqual('false',flags['anpaint_source_contract_string_forced_plain_alias'])
            self.assertEqual(['true','false'],[item.text for item in contracts.find('plurals')])
            source.write_text(source.read_text().replace('Many %1$s','Many: %1$s. Keep the document unchanged.'))
            self.assertEqual(0,self.run_generator(res,output).returncode)
            self.assertIn('Keep the document unchanged.',(output/'values/source_text.xml').read_text())

    def test_invalid_inputs_fail_without_replacing_previous_output(self):
        bad=[
            '<string name="a">@string/missing</string>',
            '<string name="a">@string/b</string><string name="b">@string/a</string>',
            '<string name="a">@string/a</string>',
            '<string name="a">%1$999999999s</string>',
            '<string name="a">%1$.999999999f</string>',
            '<string name="a">%1$--s</string>',
            '<string name="a">%1$q</string>',
            '<string name="a">100% done</string>',
            '<string name="a">%s</string>',
            '<string name="a">One</string><string name="contract_string_a">collision</string>',
            '<string name="a">%1$'+'0'*60000+'!</string>',
            '<string name="a">%1$.'+'0'*60000+'!</string>',
            '<string name="a">%1$d %1$s</string>',
            '<plurals name="p"><item quantity="other">@string/missing</item><item quantity="one">One</item></plurals>',
            '<plurals name="p"><item quantity="other">Other</item></plurals>',
            '<string name="a">broken & XML</string>',
        ]
        with tempfile.TemporaryDirectory() as tmp:
            res=Path(tmp)/'res';output=Path(tmp)/'output';(res/'values').mkdir(parents=True);output.mkdir()
            sentinel=output/'previous';sentinel.write_text('unchanged')
            for content in bad:
                (res/'values/strings.xml').write_text('<resources>'+content+'</resources>')
                result=self.run_generator(res,output)
                self.assertNotEqual(0,result.returncode,content)
                self.assertEqual('unchanged',sentinel.read_text())
            (res/'values/strings.xml').write_text('<resources><string name="a">Good</string></resources>')
            for name in ['anpaint_source_a','anpaint_source_contract_string_a']:
                for quote in ['"',"'"]:
                    (res/'values-en-rUS').mkdir(exist_ok=True)
                    (res/'values-en-rUS/strings.xml').write_text(f'<resources><string name={quote}{name}{quote}>false</string></resources>')
                    self.assertNotEqual(0,self.run_generator(res,output).returncode)
                    self.assertEqual('unchanged',sentinel.read_text())

    def test_application_and_library_variant_overlays_cannot_override_reserved_resources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);res=root/'Paintroid/src/main/res';output=root/'build/generated/sourceTextResources'
            (res/'values').mkdir(parents=True)
            (res/'values/strings.xml').write_text('<resources><string name="a">Source</string></resources>')
            app=root/'app/src/debug/res';library=root/'Paintroid/src/release/res';absent=root/'app/src/flavorDebug/res'
            for overlay in (app,library): (overlay/'values-en-rUS').mkdir(parents=True)
            # Empty/absent configured roots and the generator's own output work.
            self.assertEqual(0,self.run_generator(res,output,app,library,absent,output).returncode)
            previous=(output/'values/source_text.xml').read_bytes()
            for overlay in (app,library):
                candidate=overlay/'values-en-rUS/override.xml'
                for name in ('anpaint_source_a','anpaint_source_contract_string_a'):
                    candidate.write_text(f'<resources><string name="{name}">bad</string></resources>')
                    result=self.run_generator(res,output,app,library,absent,output)
                    self.assertNotEqual(0,result.returncode)
                    self.assertIn('Reserved source-text name',result.stderr)
                    self.assertIn(str(candidate),result.stderr)
                    self.assertEqual(previous,(output/'values/source_text.xml').read_bytes())
                candidate.unlink()
            # A root absent during configuration can later add a translated file.
            (absent/'values-fr').mkdir(parents=True)
            (absent/'values-fr/strings.xml').write_text('<resources><string name="anpaint_source_a">bad</string></resources>')
            self.assertNotEqual(0,self.run_generator(res,output,app,library,absent,output).returncode)

    def test_android_unicode_format_escapes_validate_without_rewriting_xml(self):
        valid = [
            (r'Value \u00251\u0024\u0030\u0036X', True),
            (r'Value %1$\u002e\u0032f', True),
            (r'Value \u00251$d\u0025\u0025', True),
            (r'Literal \u00251$999999999s', False),
            (r'Literal \\u00251$999999999s', True),
            (r'Literal \u005cu00251$999999999s', True),
        ]
        invalid = [
            r'Value \u00251$999999999s',
            r'Value %\u0031\u0024\u0039\u0039\u0039\u0039s',
            r'Value %1$\u002e\u0031\u0032\u0039f',
            r'Value \u00250$s',
            r'Value \u00251$q',
            r'Value \u00g0',
            r'Value \u002',
            r'\u00251$s' * 129,
        ]
        with tempfile.TemporaryDirectory() as tmp:
            res=Path(tmp)/'res';output=Path(tmp)/'output';(res/'values').mkdir(parents=True)
            source=res/'values/strings.xml'
            for text,formatted in valid:
                source.write_text(f'<resources><string name="a" formatted="{str(formatted).lower()}">{text}</string></resources>')
                result=self.run_generator(res,output)
                self.assertEqual(0,result.returncode,result.stderr)
                self.assertEqual(text,ET.parse(output/'values/source_text.xml').getroot()[0].text)
                self.assertEqual(str(formatted).lower(),ET.parse(output/'values/source_text_contracts.xml').getroot()[0].text)
            previous=(output/'values/source_text.xml').read_bytes()
            for text in invalid:
                source.write_text(f'<resources><string name="a">{text}</string></resources>')
                self.assertNotEqual(0,self.run_generator(res,output).returncode,text)
                self.assertEqual(previous,(output/'values/source_text.xml').read_bytes())

    def test_all_translated_formatter_consumers_use_the_guarded_boundary(self):
        java=ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        import check_translation_boundaries as guard
        self.assertTrue(list(guard.production_sources(ROOT)), 'No production source files discovered')
        self.assertEqual([],guard.check_repository(ROOT))
        build=(ROOT/'Paintroid/build.gradle').read_text()
        self.assertIn("tasks.register('generateSourceTextResources', Exec)",build)
        self.assertIn("tasks.named('preBuild').configure { dependsOn(generateSourceTextResources) }",build)
        self.assertIn('android.sourceSets.main.res.srcDir(sourceTextDirectory)',build)
        self.assertIn('gradle.projectsEvaluated {',build)
        self.assertIn('rootProject.allprojects.findAll',build)
        self.assertIn("hasPlugin('com.android.application')",build)
        self.assertIn("hasPlugin('com.android.library')",build)
        self.assertIn("sourceSets.collectMany { it.res.srcDirs }",build)
        self.assertIn('findAll { it != ownOutput }',build)
        self.assertIn("inputs.property('sourceResourceRoots'",build)
        self.assertIn('inputs.files(resourceRoots.collect',build)
        self.assertIn('dependsOn(generateExactScriptResources)',build)
        self.assertNotIn('label.lowercase', (java/'NormalizeImagesDialog.kt').read_text())
