#!/usr/bin/env python3
"""Offline evidence audit. Run with --source-root pointing to the pinned checkout.

This verifies source/resource inventory, not Android runtime behavior or fluency.
"""
import argparse,hashlib,json,pathlib,re,sys,unittest,xml.etree.ElementTree as ET
from urllib.parse import urlparse,parse_qs
E=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--source-root',type=pathlib.Path,required=True)
args,rest=parser.parse_known_args();S=args.source_root.resolve()
I=json.loads((E/'inventory.json').read_text());L=json.loads((E/'all-language-dispositions.json').read_text());M=json.loads((E/'source-manifest.json').read_text());P=json.loads((E/'pr34-overlap.json').read_text())
PREFIX='Paintroid/src/main/java/org/catrobat/paintroid/classic/'
def source(name): return (S/PREFIX/name).read_text()
def strings(path):return {n.attrib['name']:''.join(n.itertext()) for n in ET.parse(path).getroot() if n.tag=='string'}
class InventoryTests(unittest.TestCase):
 def test_01_all_199_pinned_source_bytes(self):
  self.assertEqual(199,len(M['source_files']))
  for f in M['source_files']:
   with self.subTest(path=f['path']):
    b=(S/f['path']).read_bytes();self.assertEqual(f['bytes'],len(b));self.assertEqual(f['sha256'],hashlib.sha256(b).hexdigest());self.assertEqual(f['git_blob_sha1'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest())
 def test_02_exact_twelve_literals_and_lines(self):
  self.assertEqual(12,len(I['rows']));self.assertEqual(12,len({r['id'] for r in I['rows']}))
  for r in I['rows']:
   with self.subTest(id=r['id']):
    text=(S/r['file']).read_text();self.assertEqual(1,text.count('"'+r['source_literal']+'"'));self.assertIn('"'+r['source_literal']+'"',text.splitlines()[r['line']-1]);self.assertEqual('application-authored',r['classification'])
 def test_03_trigger_and_route_partition(self):
  self.assertEqual(9,sum(r['reachability']=='both' for r in I['rows']));self.assertEqual(1,sum(r['reachability'].startswith('conditional insertion') for r in I['rows']));self.assertEqual(2,sum('insertion only' in r['reachability'] for r in I['rows']))
  c=source('CommonsAttribution.kt');g=source('MediaGalleryActivity.kt')
  for text in ['if (status != 200)','bytes.size().toLong() + count > MAX_RESPONSE','pages.length() != 1','page.optBoolean("missing") || page.optInt("ns", -1) != 6','html.length > MAX_FIELD']:
   self.assertIn(text,c)
  self.assertIn('provider.isArtworkPage(Uri.parse(page))',g)
  self.assertIn('if(provider!=IllustrationSource.CATROBAT && !provider.isArtworkPage(Uri.parse(page)))',g)
  self.assertEqual(1,g.count('CommonsAttribution.fetch('));self.assertEqual(1,g.count('CommonsAttribution.cache('));self.assertEqual(2,g.count('commonsCredit(uri,page'))
  self.assertIn('Bitmap.CompressFormat.PNG,100,out',source('BlankMapSvg.kt'))
 def test_04_all_140_tags_have_exact_dispositions(self):
  tags=[n.text for n in ET.parse(S/'Paintroid/src/main/res/values/app_language_tags.xml').findall('.//item')]
  self.assertEqual(140,len(tags));self.assertEqual(tags,[x['tag'] for x in L['languages']]);self.assertEqual(59,sum(x['cohort']=='existing scoped 59' for x in L['languages']));self.assertEqual(81,sum(x['cohort']=='other offered 81' for x in L['languages']))
  for x in L['languages']:
   self.assertTrue((S/x['catalogue']).is_file());self.assertEqual([r['id'] for r in I['rows']],x['applicable_message_ids']);self.assertEqual([],x['non_applicable_message_ids']);self.assertEqual([],x['proposed_keys_present'])
 def test_05_no_existing_resource_key_collision(self):
  keys={r['proposed_resource_key'] for r in I['rows']};self.assertEqual(12,len(keys))
  for p in (S/'Paintroid/src/main/res').glob('values*/*.xml'):
   self.assertFalse(keys & {n.attrib.get('name') for n in ET.parse(p).getroot()},p)
 def test_06_placeholder_contract(self):
  for r in I['rows']:
   tokens=re.findall(r'%\d+\$[a-zA-Z]',r['proposed_default']);self.assertEqual(['%1$s'] if r['id']=='M02' else [],tokens)
   self.assertEqual(r['source_literal'].replace('$status','%1$s'),r['proposed_default'])
  self.assertIn('status.toString()',I['rows'][1]['placeholders']['%1$s'])
 def test_07_pr34_overlap_is_explicit(self):
  self.assertEqual('1cd0eeac6bc4a30cb331f3b27cdfa30ff62b97df',P['head']);self.assertEqual(70,P['changed_file_count']);self.assertEqual([],P['reason_sources_changed_by_pr34']);self.assertEqual(61,len(P['production_overlap']));self.assertEqual(1,sum('MediaGalleryActivity' in p for p in P['production_overlap']));self.assertEqual(60,sum('/res/' in p for p in P['production_overlap']));self.assertIn('val reason=error.message?.takeIf {it.isNotBlank()}',P['copy_wrapper_patch']);self.assertFalse(P['held_content_touched'])
 def test_08_current_render_boundaries_and_remote_text(self):
  g=source('MediaGalleryActivity.kt');c=source('CommonsAttribution.kt')
  self.assertIn('showStatus(ui(R.string.ui_could_not_load_gallery_image,error.message))',g)
  self.assertIn('}) else error.message',g);self.assertIn('failure(ui(R.string.ui_could_not_load_gallery_image,reason))',g)
  self.assertIn('.appendQueryParameter("iiextmetadatalanguage", "en")',c)
  self.assertIn('metadata[key]?.takeIf { it.isNotBlank() }?.let { lines.add("$key: $it") }',c)
  self.assertIn('catch (_: Exception) { null }',c)
  self.assertIn('require(title.startsWith("File:") && title.length in 6..1024 && !title.contains(\'|\'))',c)
 def test_09_page_truncation_route_model(self):
  # Pure URL/query model plus exact Kotlin source anchors, not Android execution.
  page='https://commons.wikimedia.org/w/index.php?padding='+'a'*4096+'&title=File%3ATest_map.svg'
  full=urlparse(page);short=urlparse(page[:4096])
  self.assertEqual('/w/index.php',full.path);self.assertTrue(parse_qs(full.query)['title'][0].startswith('File:'));self.assertNotIn('title',parse_qs(short.query))
  g=source('MediaGalleryActivity.kt');self.assertIn('download(uri,page.take(4096),title.take(512),author,licence,authorUrl)',g)
  self.assertIn('uri.getQueryParameter("title")?.startsWith("File:")==true',source('IllustrationSource.kt'))
  self.assertIn('val connection = open(requestUrl(page))',source('CommonsAttribution.kt'))
if __name__=='__main__': unittest.main(argv=[sys.argv[0],*rest])
