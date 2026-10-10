"""Synthetic transport corruption controls; installed MediaStore behavior needs CI."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile

from vertical_evidence_transport import (MAX_CASE, MAX_FILE, METHODS, extract, paths)
from vertical_locale_matrix import LOCALES, VERTICAL_METHODS

ROOT = Path(__file__).resolve().parents[1]


def export_fixture(directory, sdk=35, source=None):
    directory.mkdir(parents=True, exist_ok=True)
    for locale in LOCALES:
        data = {name: ((source/name).read_bytes() if source else name.encode())
                for name in paths(locale) if source is None or (source/name).is_file()}
        manifest = dict(version=1, owner='paint.anpaint.android', locale=locale,
                        method=METHODS[locale], device_sdk=sdk, complete=len(data)==26,
                        files=[dict(path=name, bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
                               for name, content in sorted(data.items())])
        with zipfile.ZipFile(directory/f'{locale}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
            for name, content in data.items(): z.writestr(name, content)
            z.writestr('manifest.json', json.dumps(manifest))


def rewrite(archive, change):
    with zipfile.ZipFile(archive) as z:
        data = {name: z.read(name) for name in z.namelist()}
    change(data)
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, content in data.items(): z.writestr(name, content)


def manifest_change(archive, change):
    def alter(data):
        report = json.loads(data['manifest.json'])
        change(report)
        data['manifest.json'] = json.dumps(report)
    rewrite(archive, alter)


class VerticalEvidenceTransportTest(unittest.TestCase):
    def test_exact_sdk_inventory_and_bytes_survive_atomic_extraction(self):
        self.assertEqual(set(METHODS.values()), VERTICAL_METHODS)
        for sdk in (30, 35):
            with self.subTest(sdk=sdk), tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary); export_fixture(root/'exports',sdk)
                result=extract(root/'exports',root/'evidence',sdk)
                self.assertTrue(result['success']);self.assertEqual(result['data_files'],104)
                actual={p.relative_to(root/'evidence').as_posix() for p in (root/'evidence').rglob('*') if p.is_file()}
                expected=set().union(*(paths(locale) for locale in LOCALES))
                self.assertEqual(actual,expected)
                for name in expected:self.assertEqual((root/'evidence'/name).read_bytes(),name.encode())
                self.assertFalse(list(root.glob('.vertical-evidence-*')))

    def test_missing_extra_renamed_or_swapped_locale_archives_rejected(self):
        changes=[lambda p:(p/'mnc-Mong.zip').unlink(),
                 lambda p:shutil.copyfile(p/'mnc-Mong.zip',p/'extra.zip'),
                 lambda p:(p/'mnc-Mong.zip').rename(p/'mnc-Mong (1).zip'),
                 lambda p:shutil.copyfile(p/'en-XV.zip',p/'mnc-Mong.zip')]
        for change in changes:
            with self.subTest(change=change),tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);export_fixture(root/'exports');change(root/'exports')
                with self.assertRaises(ValueError):extract(root/'exports',root/'evidence',35)
                self.assertFalse((root/'evidence').exists())

    def test_incomplete_wrong_owner_sdk_method_version_and_duplicate_records_fail(self):
        changes=[lambda r:r.update(complete=False),lambda r:r.update(device_sdk=30),
                 lambda r:r.update(device_sdk=True),lambda r:r.update(version=True),
                 lambda r:r.update(version=2),lambda r:r.update(owner='foreign'),
                 lambda r:r.update(method=METHODS['en-XV']),lambda r:r.update(locale='en-XV'),
                 lambda r:r.update(extra='field'),lambda r:r.pop('owner'),
                 lambda r:r['files'].pop(),lambda r:r['files'].__setitem__(1,copy.deepcopy(r['files'][0])),
                 lambda r:r['files'][0].update(path='../escape'),
                 lambda r:r['files'][0].update(bytes=True),lambda r:r['files'][0].update(bytes=MAX_FILE+1),
                 lambda r:r['files'][0].update(sha256='0'*64)]
        for change in changes:
            with self.subTest(change=change),tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);export_fixture(root/'exports');manifest_change(root/'exports/mnc-Mong.zip',change)
                with self.assertRaises(ValueError):extract(root/'exports',root/'evidence',35)
                self.assertFalse((root/'evidence').exists())

    def test_duplicate_json_keys_and_corrupt_or_truncated_content_fail(self):
        changes=[lambda d:d.__setitem__('manifest.json',d['manifest.json'].replace(b'"version": 1',b'"version": 1, "version": 1')),
                 lambda d:d.__setitem__(next(n for n in d if n!='manifest.json'),b'corrupt'),
                 lambda d:d.pop(next(n for n in d if n!='manifest.json'))]
        for change in changes:
            with self.subTest(change=change),tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);export_fixture(root/'exports');rewrite(root/'exports/mnc-Mong.zip',change)
                with self.assertRaises((ValueError,zipfile.BadZipFile)):extract(root/'exports',root/'evidence',35)
                self.assertFalse((root/'evidence').exists())
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);export_fixture(root/'exports');p=root/'exports/mnc-Mong.zip';p.write_bytes(p.read_bytes()[:-12])
            with self.assertRaises(zipfile.BadZipFile):extract(root/'exports',root/'evidence',35)

    def test_unsafe_extra_duplicate_directory_symlink_and_encrypted_members_fail(self):
        for fault in ('traversal','absolute','duplicate','directory','symlink','encrypted','compression'):
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);export_fixture(root/'exports');archive=root/'exports/mnc-Mong.zip'
                with zipfile.ZipFile(archive) as z: data={n:z.read(n) for n in z.namelist()}
                name=next(n for n in data if n!='manifest.json')
                with warnings.catch_warnings(),zipfile.ZipFile(archive,'w') as z:
                    warnings.simplefilter('ignore',UserWarning)
                    for n,content in data.items():
                        member=zipfile.ZipInfo(n)
                        if n==name and fault=='symlink':member.create_system=3;member.external_attr=(stat.S_IFLNK|0o777)<<16
                        if n==name and fault=='compression':member.compress_type=zipfile.ZIP_BZIP2
                        z.writestr(member,content)
                    if fault in ('traversal','absolute','duplicate','directory'):
                        z.writestr({'traversal':'../escape','absolute':'/escape','duplicate':name,'directory':'directory/'}[fault],b'x')
                if fault=='encrypted':
                    raw=bytearray(archive.read_bytes());start=0
                    while True:
                        start=raw.find(b'PK\x01\x02',start)
                        if start<0:break
                        raw[start+8]|=1;start+=4
                    archive.write_bytes(raw)
                with self.assertRaises(ValueError):extract(root/'exports',root/'evidence',35)
                self.assertFalse((root/'evidence').exists());self.assertFalse((root/'escape').exists())

    def test_zip_and_member_size_caps_are_checked_before_content_allocation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);export_fixture(root/'exports');archive=root/'exports/mnc-Mong.zip'
            with archive.open('wb') as f:f.seek(MAX_CASE);f.write(b'x')
            with mock.patch('vertical_evidence_transport.zipfile.ZipFile',side_effect=AssertionError('opened oversize ZIP')):
                with self.assertRaises(ValueError):extract(root/'exports',root/'evidence',35)
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);export_fixture(root/'exports');archive=root/'exports/mnc-Mong.zip'
            rewrite(archive,lambda d:d.__setitem__(next(n for n in d if n!='manifest.json'),b'x'*(MAX_FILE+1)))
            with mock.patch.object(zipfile.ZipFile,'read',side_effect=AssertionError('allocated before size check')):
                with self.assertRaises(ValueError):extract(root/'exports',root/'evidence',35)

    def test_fresh_destination_required_and_symlink_archives_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);export_fixture(root/'exports');(root/'evidence').mkdir();(root/'evidence/stale').write_text('retained')
            with self.assertRaises(ValueError):extract(root/'exports',root/'evidence',35)
            self.assertEqual((root/'evidence/stale').read_text(),'retained')
            archive=root/'exports/mnc-Mong.zip';archive.rename(root/'real.zip');archive.symlink_to(root/'real.zip')
            with self.assertRaises(ValueError):extract(root/'exports',root/'new',35)
            self.assertFalse((root/'new').exists())

    def test_case_manifest_and_combined_size_limits_reject_before_extraction(self):
        for fault in ('case','manifest','combined'):
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);export_fixture(root/'exports');archive=root/'exports/mnc-Mong.zip'
                if fault=='case':
                    def oversize(data):
                        for name in list(n for n in data if n!='manifest.json')[:5]:data[name]=b'x'*MAX_FILE
                    rewrite(archive,oversize)
                elif fault=='manifest':rewrite(archive,lambda d:d.__setitem__('manifest.json',b' '*(64*1024+1)))
                if fault=='combined':
                    with mock.patch('vertical_evidence_transport.MAX_TOTAL',1):
                        with self.assertRaises(ValueError):extract(root/'exports',root/'evidence',35)
                else:
                    with mock.patch.object(zipfile.ZipFile,'read',side_effect=AssertionError('allocated before size check')):
                        with self.assertRaises(ValueError):extract(root/'exports',root/'evidence',35)
                self.assertFalse((root/'evidence').exists())

    def test_cli_optimized_modes_remove_stale_receipt_on_failure(self):
        for mode in ('normal','flag','environment'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);export_fixture(root/'exports',30);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
                if mode=='environment':env['PYTHONOPTIMIZE']='1'
                command=[sys.executable,*(['-O'] if mode=='flag' else []),str(ROOT/'tools/vertical_evidence_transport.py'),
                         str(root/'exports'),'--output',str(root/'evidence'),'--receipt',str(root/'receipt.json'),'--sdk','30']
                run=subprocess.run(command,env=env,capture_output=True,text=True,timeout=10)
                self.assertEqual(run.returncode,0,run.stderr)
                shutil.rmtree(root/'evidence');manifest_change(root/'exports/mnc-Mong.zip',lambda r:r.update(complete=False))
                run=subprocess.run(command,env=env,capture_output=True,text=True,timeout=10)
                self.assertNotEqual(run.returncode,0);self.assertFalse((root/'receipt.json').exists());self.assertFalse((root/'evidence').exists())

    def test_instrumentation_owner_limits_pending_lifecycle_and_original_identity_contracts(self):
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/VerticalEvidenceExportRule.kt').read_text()
        self.assertEqual(set(re.findall(r'"(\w+BothOrientations)" to',source)),VERTICAL_METHODS)
        for required in ('MediaStore.Downloads.getContentUri','OWNER_PACKAGE_NAME} = ?',
                         'MediaStore.setIncludePending(collection)','resolver.delete(ContentUris.withAppendedId',
                         'put(MediaStore.MediaColumns.IS_PENDING,1)','put(MediaStore.MediaColumns.IS_PENDING,0)',
                         'contentDigest(inserted,temporary.length())','failure!!.addSuppressed(error)',
                         'copied<=size && copied<=MAX_FILE','total<=MAX_CASE','file.canonicalFile==file.absoluteFile',
                         'const val MAX_FILE=2L*1024*1024','const val MAX_CASE=8L*1024*1024'):
            self.assertIn(required,source)
        for forbidden in ('adoptShellPermissionIdentity','grantRuntimePermission','executeShellCommand','MANAGE_EXTERNAL_STORAGE','WRITE_EXTERNAL_STORAGE'):
            self.assertNotIn(forbidden,source)
        shell=(ROOT/'tools/ci_emulator.sh').read_text()
        self.assertIn('timeout --kill-after=3s 15s "$adb" pull',shell)
        self.assertIn("rm -rf /sdcard/Download/anpaint-ci-vertical-evidence && test ! -e /sdcard/Download/anpaint-ci-vertical-evidence",shell)
        self.assertNotIn('/sdcard/Android/data/paint.anpaint.android/files/vertical-locale-evidence',shell)

    def test_java_file_boundary_rejects_symlinked_evidence_root_directory_and_file(self):
        # Exercise the helper's java.io.File operations on the host JDK. This is
        # a path-contract test, not installed Kotlin/MediaStore validation.
        source=(ROOT/'app/src/androidTest/java/paint/anpaint/android/VerticalEvidenceExportRule.kt').read_text()
        ordered=['val external=checkNotNull(context.getExternalFilesDir(null)).canonicalFile',
                 'val directory=File(external,"vertical-locale-evidence")',
                 'check(!Files.isSymbolicLink(directory.toPath()) && directory.canonicalFile==directory.absoluteFile)',
                 'val file=File(directory,relative)',
                 'check(!Files.isSymbolicLink(component.toPath()))',
                 'check(file.canonicalFile==file.absoluteFile)']
        offsets=[source.index(text) for text in ordered]
        self.assertEqual(offsets,sorted(offsets))
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);outside=root/'outside';outside.mkdir();(outside/'sample.png').write_bytes(b'synthetic')
            cases=[]
            for kind in ('regular','root-link','directory-link','file-link','root-dangling','directory-dangling','file-dangling'):
                external=root/kind;external.mkdir();directory=external/'vertical-locale-evidence'
                target=outside if not kind.endswith('dangling') else root/'missing'
                if kind.startswith('root-'):directory.symlink_to(target,target_is_directory=True)
                else:
                    directory.mkdir()
                    if kind.startswith('directory-'):(directory/'reachability').symlink_to(target,target_is_directory=True)
                    elif kind.startswith('file-'):(directory/'sample.png').symlink_to(target/'sample.png')
                cases.extend([str(external),'reachability/sample.png' if kind.startswith('directory-') else 'sample.png'])
            probe=root/'CanonicalProbe.java'
            probe.write_text('''import java.io.File;
import java.nio.file.Files;
class CanonicalProbe {
  public static void main(String[] args) throws Exception {
    for(int i=0;i<args.length;i+=2) {
      File external=new File(args[i]).getCanonicalFile();
      File directory=new File(external,"vertical-locale-evidence");
      File file=new File(directory,args[i+1]);
      boolean accepted=!Files.isSymbolicLink(directory.toPath())
          && directory.getCanonicalFile().equals(directory.getAbsoluteFile())
          && file.getCanonicalFile().equals(file.getAbsoluteFile());
      File component=directory;
      for(String part:args[i+1].split("/")) {
        component=new File(component,part);
        accepted=accepted && !Files.isSymbolicLink(component.toPath());
      }
      System.out.println(accepted);
    }
    // Negative control: canonicalizing the child first hides a root link.
    File oldDirectory=new File(new File(args[2]),"vertical-locale-evidence").getCanonicalFile();
    File oldFile=new File(oldDirectory,args[3]);
    System.out.println(oldFile.getCanonicalFile().equals(oldFile.getAbsoluteFile()));
    // The canonical-only root check also accepts a dangling link.
    File dangling=new File(new File(args[8]),"vertical-locale-evidence");
    System.out.println(dangling.getCanonicalFile().equals(dangling.getAbsoluteFile()));
  }
}
''')
            run=subprocess.run(['java',str(probe),*cases],text=True,capture_output=True,timeout=15)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            self.assertEqual(run.stdout.splitlines(),['true',*(['false']*6),'true','true'])


if __name__=='__main__':unittest.main()
