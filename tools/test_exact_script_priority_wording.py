"""Exact own-script reviewed-value and scoped hold boundary regressions."""
import copy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
import exact_script_priority_expectations as g
ROOT=Path(__file__).resolve().parents[1]
SOURCE_ROOT=ROOT
class ExactScriptPriorityTests(unittest.TestCase):
    def root(self,tag):return E.parse(ROOT/g.bound_fixture(tag)['catalogue_path']).getroot()
    def test_exact_three_catalogues_and_full_source(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);self.assertEqual(341,len(d['priority_identities']));self.assertEqual(361,len(d['rows'])+len(d['held']));g.require_catalogue(tag,self.root(tag));g.require_source(tag,E.parse(SOURCE_ROOT/'Paintroid/src/main/res/values/strings.xml').getroot())
    def test_exact_counts_and_holds(self):
        for tag,edits,holds in [('tt-Latn',335,11),('ain-Latn',17,11),('mn-Mong',21,11)]:
            d=g.bound_fixture(tag);self.assertEqual(edits,sum(r['decision']=='edited' for r in d['rows'].values()));self.assertEqual(holds,len(d['held']));self.assertNotIn('original_catalogue',d)
    def test_every_standalone_reviewed_row_rejects_caller_owned_coordinate_mutant(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);root=self.root(tag)
            for key,row in d['rows'].items():
                with self.subTest(tag=tag,key=key):
                    n=root.find("./*[@name='"+key+"']");g.require_reviewed_resource(tag,key,n,row)
                    bad=copy.deepcopy(row);bad['reviewed_value']='forged';bad['reviewed_display']='forged';n=copy.deepcopy(n);n.clear();n.tag='string';n.set('name',key);n.text='forged'
                    with self.assertRaises(ValueError):g.require_reviewed_resource(tag,key,n,bad)
    def test_supplied_fixture_cannot_coordinate_target_and_root(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);root=self.root(tag);key=next(iter(d['rows']));d['rows'][key]['reviewed_value']='forged';root.find("./*[@name='"+key+"']").text='forged'
            with self.assertRaises(ValueError):g.require_catalogue(tag,root,d)
    def test_mutating_returned_fixture_cannot_change_fresh_binding(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);key=next(iter(d['rows']));d['rows'][key]['reviewed_value']='forged';self.assertNotEqual('forged',g.bound_fixture(tag)['rows'][key]['reviewed_value'])
    def test_every_present_held_value_remains_exact(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);root=self.root(tag)
            for key,held in d['held'].items():
                if held['previous'] is None:continue
                with self.subTest(tag=tag,key=key):
                    n=root.find("./*[@name='"+key+"']");old=n.text;n.text='forged'
                    with self.assertRaises(ValueError):g.require_catalogue(tag,root)
                    n.text=old
    def test_unrelated_valid_values_can_evolve_without_snapshot_reconstruction(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);root=self.root(tag)
            outside=[n for n in root if n.get('name') not in set(d['rows'])|set(d['held'])]
            self.assertTrue(outside)
            for n in outside:
                if n.tag=='string':n.text='Independent unrelated wording change'
                else:
                    for child in n:child.text='Independent unrelated plural change'
            g.require_catalogue(tag,root)
            for n in outside:root.remove(n)
            E.SubElement(root,'string',{'name':'unrelated_new_resource'}).text='New unrelated wording'
            g.require_catalogue(tag,root)
    def test_fixtures_do_not_embed_historical_source_snapshots(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag)
            for key in ('original_catalogue','parent_head','parent_tree','review_sha256','compiled_projection_sha256'):
                self.assertNotIn(key,d)
    def test_wrong_parent_text_attributes_tail_and_identity_rejected(self):
        for tag in g.TAGS:
            root=self.root(tag)
            for mutation in [lambda r:setattr(r,'text','bad'),lambda r:setattr(r,'tail','bad'),lambda r:r.set('extra','bad'),lambda r:setattr(r,'tag','wrong'),lambda r:r.remove(r.find("./*[@name='"+next(iter(g.bound_fixture(tag)['rows']))+"']")),lambda r:r.append(copy.deepcopy(r[0]))]:
                r=copy.deepcopy(root);mutation(r)
                with self.assertRaises(ValueError):g.require_catalogue(tag,r)
    def test_cross_type_same_name_duplicate_rejected(self):
        for tag in g.TAGS:
            r=self.root(tag);n=E.Element('plurals',{'name':r[0].get('name')});r.append(n)
            with self.assertRaises(ValueError):g.require_catalogue(tag,r)
    def test_scalar_children_attributes_and_tail_rejected(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);key=next(k for k,r in d['rows'].items() if r['type']=='string');n=self.root(tag).find("./string[@name='"+key+"']")
            for mutation in [lambda x:x.append(E.Element('b')),lambda x:x.set('formatted','false'),lambda x:setattr(x,'tail','bad'),lambda x:setattr(x,'text','')]:
                bad=copy.deepcopy(n);mutation(bad)
                with self.assertRaises(ValueError):g.require_reviewed_resource(tag,key,bad,d['rows'][key])
    def test_plural_shape_rejects_parent_item_tail_and_extra_forms(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);key='ui_crop_preview_images';n=self.root(tag).find("./plurals[@name='"+key+"']")
            for mutation in [lambda x:setattr(x,'text','bad'),lambda x:setattr(x[0],'tail','bad'),lambda x:x[0].append(E.Element('b')),lambda x:x.append(copy.deepcopy(x[0])),lambda x:x[0].set('quantity','few'),lambda x:x[0].set('extra','bad')]:
                bad=copy.deepcopy(n);mutation(bad)
                with self.assertRaises(ValueError):g.require_reviewed_resource(tag,key,bad,d['rows'][key])
    def test_source_change_and_same_name_wrong_type_rejected(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);key=next(iter(d['rows']));r=E.parse(SOURCE_ROOT/'Paintroid/src/main/res/values/strings.xml').getroot();r.find("./*[@name='"+key+"']").text='changed'
            with self.assertRaises(ValueError):g.require_source(tag,r)
            r=E.parse(SOURCE_ROOT/'Paintroid/src/main/res/values/strings.xml').getroot();r.append(E.Element('plurals',{'name':key}))
            with self.assertRaises(ValueError):g.require_source(tag,r)
    def test_fixture_omitted_added_and_foreign_locale_rejected(self):
        for tag in g.TAGS:
            for mutation in [lambda d:d.pop('held'),lambda d:d.update(extra=True),lambda d:d['rows'].pop(next(iter(d['rows']))),lambda d:d.update(locale='wrong')]:
                d=g.bound_fixture(tag);mutation(d)
                with self.assertRaises(ValueError):g.require_fixture(tag,d)
        with self.assertRaises(ValueError):g.bound_fixture('yue-Hant')
    def test_absent_holds_cannot_be_added_and_present_holds_cannot_disappear(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag)
            for key,h in d['held'].items():
                root=self.root(tag);node=root.find("./*[@name='"+key+"']")
                if h['previous'] is None:
                    from current_localization_contracts import residual_rows
                    if (tag,key) in residual_rows():
                        self.assertIsNotNone(node);node.text='forged'
                    else:
                        self.assertIsNone(node);E.SubElement(root,'string',{'name':key}).text='forged'
                else:
                    self.assertIsNotNone(node);root.remove(node)
                with self.assertRaises(ValueError):g.require_catalogue(tag,root)
    def test_native_text_projection_and_alias_are_exact(self):
        for tag in g.TAGS:
            for key,row in g.bound_fixture(tag)['rows'].items():
                self.assertEqual(row['reviewed_display'],row['compiled_display'])
                bad=copy.deepcopy(row);bad['compiled_display']='forged'
                with self.assertRaises(ValueError):g.require_row(tag,key,bad)
        r=g.bound_fixture('mn-Mong')['rows']['ui_draw26']
        self.assertEqual('@string/ui_drawing23',r['reviewed_value'])
        self.assertEqual(g.bound_fixture('mn-Mong')['rows']['ui_drawing23']['compiled_display'],r['compiled_display'])
    def test_complete_jvm_consumer_source_and_mutations(self):
        text=(ROOT/g.JVM_PATH).read_text();g.require_jvm_source(text)
        self.assertEqual(17,text.count('@Test fun '))
        for before,after in [('requireRow(tag,key,supplied)','supplied'),('exactScriptSameJson(current.get(field),supplied.get(field))','Unit'),('val quantity=if(values.has(selected)) selected else "other"','val quantity="other"'),('assertEquals(expected(tag,"ui_fg"),ui(R.string.ui_fg))','assertTrue(true)'),('assertEquals(description,LocaleTooltip.logicalText(button).toString())','assertTrue(true)'),('assertTrue("Category button attached $tag",button.isAttachedToWindow)','assertTrue(true)'),('if(visible) controller.visible().windowFocusChanged(true)','Unit'),('categoryAccessibilityTracksEveryActualToolAndExpansionState() = forEachLocale(visible=true)','categoryAccessibilityTracksEveryActualToolAndExpansionState() = forEachLocale'),('categoryTooltipChecksRejectCaptionLogicalNativeAndAccessibilityCorruption() = forEachLocale(visible=true)','categoryTooltipChecksRejectCaptionLogicalNativeAndAccessibilityCorruption() = forEachLocale'),('if(vertical) assertNull("No duplicate native tooltip $tag",button.tooltipText)','if(vertical) Unit'),('else assertEquals(description,button.tooltipText.toString())','else Unit'),('assertEquals(description,node.tooltipText.toString())','assertTrue(true)'),('"compiled_display"','"reviewed_display"')]:
            self.assertIn(before,text)
            with self.assertRaises(ValueError):g.require_jvm_source(text.replace(before,after,1))
    def test_main_successor_exact_tatar_complete_branch_and_negatives(self):
        text=(ROOT/g.MAIN_PATH).read_text();g.require_main_successor(text)
        for bad in [text.replace(g.SAVE_BRANCHES,''),text.replace(g.SAVE_BRANCHES,g.SAVE_BRANCHES*2),text.replace('Saqlaw…','forged')]:
            with self.assertRaises(ValueError):g.require_main_successor(bad)
    def test_exact_family_additions_reject_predecessor_source_and_coordinated_rows(self):
        from unittest.mock import patch
        keys=set(g.SVG_KEYS)|{g.TAGGED_KEY}|{k for _,k in g.MEMORY_ADDITIONS}
        for key in keys:
            d=g.bound_fixture('tt-Latn');row=d['rows'][key];source=row['source']['value']
            self.assertEqual(row,g.require_addition('tt-Latn',key,None,source))
            for old in ('',source,row['reviewed_value']):
                with self.assertRaises(ValueError):g.require_addition('tt-Latn',key,old,source)
            with self.assertRaises(ValueError):g.require_addition('tt-Latn',key,None,source+' changed')
            with self.assertRaises(ValueError):g.require_addition('tt-Latn',key,None,source,already_present=True)
            for tag in ('tt-Cyrl','ain-Latn','mn-Mong','unknown'):
                with self.assertRaises(ValueError):g.require_addition(tag,key,None,source)
            for field in ('reviewed_value','compiled_display','source','previous_target','attributes'):
                bad=copy.deepcopy(d);bad['rows'][key][field]='forged'
                with patch.object(g,'bound_fixture',return_value=bad),self.assertRaises(ValueError):
                    g.require_addition('tt-Latn',key,None,source)
        with self.assertRaises(ValueError):g.require_addition('tt-Latn','ui_save',None,'Save')
    def test_exact_tagged_jvm_boundaries_keep_prior_stage_and_reject_missing_consumers(self):
        text=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/TaggedColourImportTest.kt').read_text()
        g.require_tagged_jvm_source(text)
        for before,after in [('exactScriptSameJson(current,row)','Unit'),('assertFalse(expected.has(tag));assertTrue(row.isNull("previous_target"))','assertTrue(true)'),('addExactScript(expected,exactScriptExpectations())',''),('assertEquals(140, expected.length())',''),('assertEquals(141, expected.length())',''),('assertEquals(30, 171 - expected.length())','assertEquals(31, 171 - expected.length())')]:
            self.assertIn(before,text)
            with self.assertRaises(ValueError):g.require_tagged_jvm_source(text.replace(before,after,1))
    def test_readable_fixture_allows_formatting_and_reviewed_value_updates_without_fingerprints(self):
        from tempfile import TemporaryDirectory
        from unittest.mock import patch
        with TemporaryDirectory() as directory:
            root=Path(directory);folder=root/'tools/fixtures/exact_script_priority_wording'
            folder.mkdir(parents=True)
            d=g.bound_fixture('tt-Latn')
            path=folder/'tt-Latn.json'
            path.write_text(json.dumps(d,ensure_ascii=False,sort_keys=True),encoding='utf-8')
            with patch.object(g,'ROOT',root):
                self.assertEqual(d,g.bound_fixture('tt-Latn'))
            # A valid, explicitly changed expectation is not cryptographically frozen.
            # This tests the loader contract, not approval of new linguistic wording.
            key='language20_device_default'
            for field in ('reviewed_value','reviewed_display','compiled_display'):
                d['rows'][key][field]+=' — test-only revision'
            path.write_text(json.dumps(d,ensure_ascii=False,indent=1),encoding='utf-8')
            with patch.object(g,'ROOT',root):
                self.assertEqual(d['rows'][key],g.bound_fixture('tt-Latn')['rows'][key])
                node=E.Element('string',{'name':key});node.text=d['rows'][key]['reviewed_value']
                g.require_reviewed_resource('tt-Latn',key,node)

    def test_schema_rejects_duplicate_json_members_before_parsing_can_hide_them(self):
        with self.assertRaises(ValueError):
            json.loads('{"locale":"tt-Latn","locale":"mn-Mong"}',object_pairs_hook=g._unique_object)

    def test_coordinated_format_corruptions_fail_semantics_without_a_second_oracle(self):
        key='ui_d_d_px_d_pixels_2f_mp'
        original=g.bound_fixture('tt-Latn')
        self.assertIn('%4$.2f',original['rows'][key]['reviewed_value'])
        for replacement in ('%5$.2f','%4$.2s','%4$.1f','%4$f','%4$.2f %4$.2f'):
            d=copy.deepcopy(original)
            for field in ('reviewed_value','reviewed_display','compiled_display'):
                d['rows'][key][field]=d['rows'][key][field].replace('%4$.2f',replacement)
            with self.subTest(replacement=replacement),self.assertRaises(ValueError):
                g.validate_fixture('tt-Latn',d)
        d=copy.deepcopy(original)
        for field in ('reviewed_value','reviewed_display','compiled_display'):
            d['rows'][key][field]+=' 100%'
        with self.assertRaises(ValueError):g.validate_fixture('tt-Latn',d)

    def test_display_transform_keeps_newlines_literal_backslashes_and_mongolian_spaces(self):
        self.assertEqual('line\nnext',g.decode_display(r'line\nnext'))
        self.assertEqual('a\\b',g.decode_display(r'a\\b'))
        self.assertEqual('ᠮᠣᠩᠭᠣᠯ\u202fᠤᠨ',g.decode_display('ᠮᠣᠩᠭᠣᠯ\u202fᠤᠨ'))
        for tag in g.TAGS:
            d=g.bound_fixture(tag);row=d['rows']['language20_translation_note']
            row['compiled_display']=row['compiled_display'].replace('\n',' ')
            row['reviewed_display']=row['compiled_display']
            with self.assertRaises(ValueError):g.validate_fixture(tag,d)

    def test_current_aliases_reject_missing_target_cycle_and_wrong_display(self):
        for raw in ('@string/missing','@string/ui_draw26'):
            d=g.bound_fixture('mn-Mong');row=d['rows']['ui_draw26']
            row['reviewed_value']=raw
            # Keep the retained relationship coherent to reach alias validation.
            row['previous_target']['value']=raw
            with self.subTest(raw=raw),self.assertRaises(ValueError):g.validate_fixture('mn-Mong',d)
        d=g.bound_fixture('mn-Mong');row=d['rows']['ui_draw26']
        row['compiled_display']=row['reviewed_display']='forged'
        with self.assertRaises(ValueError):g.validate_fixture('mn-Mong',d)

    def test_structural_damage_is_rejected_without_a_fixture_fingerprint(self):
        for mutation in (
            lambda d:d['rows']['ui_save'].update(identity='plurals/ui_save'),
            lambda d:d['rows']['ui_save'].update(decision='accepted'),
            lambda d:d['rows']['ui_save']['source'].update(extra=True),
            lambda d:d['priority_identities'].append(d['priority_identities'][0]),
            lambda d:d['priority_identities'].append('string/not_declared'),
            lambda d:d['held']['ui_bg'].update(status='accepted'),
            lambda d:d['rows']['ui_crop_preview_images']['children_attributes'].update(other={'quantity':'one'}),
        ):
            d=g.bound_fixture('tt-Latn');mutation(d)
            with self.assertRaises(ValueError):g.validate_fixture('tt-Latn',d)

    def test_nonbehavioral_scope_note_is_not_a_wording_fingerprint(self):
        d=g.bound_fixture('tt-Latn');d['limits']+=' Caller annotation.'
        g.require_fixture('tt-Latn',d)

    def test_structural_xml_whitespace_is_ascii_not_mongolian_narrow_no_break_space(self):
        for tag in g.TAGS:
            # Pretty-print XML whitespace is valid; U+202F is meaningful text.
            root=self.root(tag);root.text=' \t\r\n';root.tail='\n';root[0].tail='\n  '
            g.require_catalogue(tag,root)
            for mutation in (
                lambda r:setattr(r,'text','\u202f'),
                lambda r:setattr(r,'tail','\u202f'),
                lambda r:setattr(r[0],'tail','\u202f'),
                lambda r:setattr(r.find("./plurals[@name='ui_crop_preview_images']"),'text','\u202f'),
                lambda r:setattr(r.find("./plurals[@name='ui_crop_preview_images']")[0],'tail','\u202f'),
            ):
                changed=copy.deepcopy(root);mutation(changed)
                with self.assertRaises(ValueError):g.require_catalogue(tag,changed)
            row=g.bound_fixture(tag)['rows']['ui_crop_preview_images']
            node=root.find("./plurals[@name='ui_crop_preview_images']")
            for target in ('parent','item'):
                changed=copy.deepcopy(node)
                if target=='parent':changed.text='\u202f'
                else:changed[0].tail='\u202f'
                with self.assertRaises(ValueError):g.require_reviewed_resource(tag,'ui_crop_preview_images',changed,row)
            source=E.parse(SOURCE_ROOT/'Paintroid/src/main/res/values/strings.xml').getroot()
            for location in ('text','tail'):
                changed=copy.deepcopy(source);setattr(changed,location,'\u202f')
                with self.assertRaises(ValueError):g.require_source(tag,changed)

if __name__=='__main__':unittest.main()
