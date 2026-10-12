#!/usr/bin/env python3
"""Freeze selected current raw evidence once, without APK/source or PNG duplicates."""
import gzip
import hashlib
import io
import json
import pathlib
import tarfile

from audit_natural_artifacts import HEAD, TREE, MERGE, RUN, require

root = pathlib.Path(__file__).resolve().parent
artifacts = root / 'selected-artifacts'
destination = root / 'supporting-evidence.tar.gz'
require(not destination.exists(), 'support archive already frozen')
selected = {}


def add(name, path):
    require(name not in selected and path.is_file(), 'duplicate/missing selected input ' + name)
    selected[name] = path


for name in ('build-job.log', 'api30-job.log', 'api35-job.log', 'source-publication.json',
             'attempt1-final-jobs.json', 'attempt2-jobs-initial.json',
             'api30.metadata.json', 'api35.metadata.json',
             'apk-and-source.metadata.json', 'apk-and-source/build/delivery/build-info.json'):
    add('current-inputs/' + name, artifacts / name)
for api in (30, 35):
    source = artifacts / f'api{api}'
    for path in sorted(source.rglob('*')):
        if not path.is_file(): continue
        rel = path.relative_to(source)
        use = (path.name in ('summary.json', 'instrumentation.log', 'install.log')
               or path.name.startswith('TEST-') and path.suffix == '.xml'
               or path.name == 'logcat.txt'
               or rel.parts[0] == 'vertical-locale-export'
               or str(rel) in ('vertical-locale-export.json', 'vertical-locale-screenshots.json',
                   'vertical-control-reachability.json', 'app/coverage.json',
                   'app/ordinary-gallery-coverage.json', 'app/vertical-coverage.json',
                   'app/accepted-credit-restart/coverage.json',
                   'app/accepted-credit-restart/boundary.log',
                   'app/accepted-credit-restart/verify-status.txt'))
        if use: add(f'current-inputs/api{api}/' + rel.as_posix(), path)
add('attempt1/api30-job.log', root / 'attempt1/api30-job.log')
add('reproduced/native-vertical/result.json', root / 'reproduced/native-vertical/result.json')
rows = []
with destination.open('wb') as output:
    with gzip.GzipFile(filename='', fileobj=output, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tar:
            for name, path in sorted(selected.items()):
                data = path.read_bytes()
                info = tarfile.TarInfo(name); info.size = len(data); info.mode = 0o644
                info.uid = info.gid = info.mtime = 0; info.uname = info.gname = ''
                tar.addfile(info, io.BytesIO(data))
                rows.append(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
data = destination.read_bytes()
report = dict(schema=1, head=HEAD, tree=TREE, merge=MERGE, run_id=int(RUN),
    archive=dict(path=destination.name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()),
    file_count=len(rows), expanded_bytes=sum(row['bytes'] for row in rows), files=rows,
    scope='Current raw phase protocols/summary/XML/install, full logcat/job logs, attempt metadata and native export/geometry inputs. Changed native PNGs occur only within their original native-export ZIPs. No APK, corresponding-source ZIP, original whole CI ZIP or contact-sheet duplicate.',
    reuse='Only four exact-byte Arabic visual inputs reuse the prior e19 visual conclusion. All 192 native images changed and were freshly inspected.',
    limits='Supporting evidence selection, not a new Android run or a full duplicate of prior evidence. Original outer-ZIP/APK/source hash checks are preserved receipts; payloads are intentionally omitted. Coordinator publication/privacy review remains separate.')
(root / 'SUPPORTING-INPUTS.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ('archive', 'file_count', 'expanded_bytes')}, indent=2))
