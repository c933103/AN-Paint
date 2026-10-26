"""Read actual source-bound successful dialog exports; no failure promotion or visual inference."""
from pathlib import Path
import argparse, copy, hashlib, json, sys, zipfile

p = argparse.ArgumentParser()
p.add_argument('--source-root', type=Path, required=True)
p.add_argument('--directory', type=Path, required=True)
p.add_argument('--run-id', type=int, required=True)
p.add_argument('--tested-commit', required=True)
p.add_argument('--core-sha256', required=True)
p.add_argument('--mode', choices=('ordinary', 'optimized'), required=True)
a = p.parse_args()
sys.path.insert(0, str(a.source_root / 'tools'))
import dialog_evidence_transport as d
from run_android_instrumentation import source_tests_sha256

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

r = a.directory
need(sha(r / 'core.zip') == a.core_sha256, 'core archive digest')
digest = source_tests_sha256(a.source_root / 'app/src/androidTest')
identity = json.loads((r / 'core/device-identity.json').read_text())
for key, value in {'commit': a.tested_commit, 'run_id': str(a.run_id), 'run_attempt': '1',
                   'device_sdk': 35, 'group': 'core', 'build_variant': 'debug',
                   'source_tests_sha256': digest, 'apk_sha256': sha(r / 'app-debug.apk'),
                   'source_sha256': sha(r / 'AN-Paint-source.zip')}.items():
    need(identity[key] == value, 'core identity ' + key)
with zipfile.ZipFile(r / 'instrumentation-apks.zip') as z:
    raw = z.read('app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk')
    need(identity['test_apk_sha256'] == hashlib.sha256(raw).hexdigest(), 'executed test APK')
summary = r / 'core/app-dialog/androidTest-results/summary.json'
phase = json.loads(summary.read_text())
need(phase['success'] is True and phase['timed_out'] is False and phase['returncode'] == 0
     and phase['elapsed_seconds'] <= 300 and phase['expected_tests'] == phase['completed_tests'] == 14,
     'complete successful bounded dialog phase')
output = r / ('verified-dialog-' + a.mode)
need(not output.exists(), 'refuse stale extraction')
receipt = d.extract(r / 'core/dialog-export', output, summary)
need(receipt == json.loads((r / 'core/dialog-evidence.json').read_text()), 'host/CI transport receipt mismatch')
need(len(receipt['cases']) == 14 and sum(e['path'].endswith('.png') for c in receipt['cases'] for e in c['files']) == 51,
     'exact successful 14/51 inventory')
new = []; negatives = 0
for method in d.LARGE_COLOUR_IME_METHODS:
    data = json.loads((output / method / 'receipt.json').read_text())
    observations = data['observations']
    def one(kind):
        return d.one(observations, kind)
    ime = [o for o in observations if o['kind'] == 'colour-native-ime-window']
    backs = [o for o in observations if o['kind'].startswith('native-back-')]
    captions = [o for o in observations if o['kind'] == 'colour-2x-caption']
    files = next(c['files'] for c in receipt['cases'] if c['method'] == method)
    new.append({'method': method, 'fixture_elapsed_ms': data['fixture_elapsed_ms'],
                'fixture_elapsed_scope': data['fixture_elapsed_scope'],
                'actual_ime_stable_ms': ime[0]['stable_window_ms'],
                'actual_ime_absent_stable_ms': ime[1]['stable_window_ms'],
                'ime_window_observation': ime[0]['windows'],
                'ime_inset_bottom_observation': ime[0]['ime_inset_bottom'],
                'fullscreen_ime_observation': ime[0]['fullscreen_ime'],
                'activation': one('colour-2x-synthetic-ime-activation'),
                'retained_after_first_back': backs[2]['state'],
                'retained_hidden': one('colour-2x-hidden-retained')['state'],
                'captions': captions,
                'caption_lines': [o for o in observations if o['kind'] == 'colour-2x-caption-line'],
                'native_taps': [o for o in observations if o['kind'] in ('pointer-before', 'pointer-injected')],
                'cancelled': one('colour-2x-cancelled'), 'reopened': one('colour-2x-reopened'),
                'reopened_native_back_after': backs[-1],
                'invalid_rejected': one('colour-2x-invalid-rejected'), 'complete': one('colour-2x-complete'),
                'screenshots': [e for e in files if e['path'].endswith('.png')]})
    mutations = [
        lambda x: next(o for o in x['observations'] if o['kind'] == 'colour-native-ime-window').update(windows=[]),
        lambda x: next(o for o in x['observations'] if o['kind'] == 'native-back-after').update(completed=False),
        lambda x: next(o for o in x['observations'] if o['kind'] == 'native-back-injected')['state'].update(commit_callbacks=1),
        lambda x: d.one(x['observations'], 'colour-2x-hidden-retained')['state'].update(field_id=999),
        lambda x: next(o for o in x['observations'] if o['kind'] == 'colour-2x-caption-line').update(ancestors=[]),
        lambda x: next(o for o in x['observations'] if o['kind'] == 'colour-2x-caption' and o['key'] == 'cancel').update(transformation_method='none'),
        lambda x: next(o for o in x['observations'] if o['kind'] == 'colour-2x-caption' and o['key'] == 'use').update(accessible_text='partial'),
        lambda x: x['screenshots'].pop(),
        lambda x: x.update(source_tests_sha256='f' * 64),
    ]
    for mutation in mutations:
        broken = copy.deepcopy(data); mutation(broken)
        try:
            d.verify_receipt(broken, method, digest)
        except ValueError:
            negatives += 1
        else:
            raise ValueError('Actual-receipt negative mutation accepted')
record = {'run_id': a.run_id, 'tested_commit': a.tested_commit, 'source_tests_sha256': digest,
          'core_archive_sha256': a.core_sha256, 'device_identity': identity, 'dialog_phase_seconds': phase['elapsed_seconds'],
          'dialog_phase_cap_seconds': 300, 'source_enforced_method_deadline_seconds': 45,
          'method_timing_limit': 'Fixture intervals include setup+interaction+teardown and exclude export; no separate interaction interval is invented.',
          'successful_dialog_methods': 14, 'successful_pngs': 51, 'original_methods_preserved': 12,
          'original_pngs_preserved': 39, 'new_method_results': new, 'actual_receipt_negative_mutations_rejected': negatives,
          'initial_native_field_activation': 'not-tested', 'initial_full_hex_visibility': 'not-accepted',
          'simultaneous_ime_field_footer_fit': 'not-accepted',
          'limits': 'Source-bound API35 emulator lifecycle and sequential full native Layout-line/ancestor coverage only. PNG pixels require separate inspection. Not whole-2x, initial native entry, glyph-ink, physical-device, TalkBack, C05, fluency or release acceptance.'}
(r / ('completed-colour-lifecycle-' + a.mode + '.json')).write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'successful_dialog_methods': 14, 'successful_pngs': 51, 'new_methods': len(new), 'negative_mutations_rejected': negatives}))
