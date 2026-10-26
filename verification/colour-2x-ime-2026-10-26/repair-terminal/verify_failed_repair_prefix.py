#!/usr/bin/env python3
"""Verify the failed repair cohort through pre-footer caption coverage, never whole-case acceptance."""
import argparse, copy, hashlib, json, sys, zipfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--source-root', type=Path, required=True)
p.add_argument('--directory', type=Path, required=True)
a = p.parse_args()
sys.path.insert(0, str(a.source_root / 'tools'))
import dialog_evidence_transport as d
from run_android_instrumentation import source_tests_sha256

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

digest = source_tests_sha256(a.source_root / 'app/src/androidTest')
need(digest == 'a72527573d094d16746a19a19f066923a5bad9869b92fa46ae896913447d59ec', 'wrong successor source')

def verify_prefix(receipt, method):
    need(receipt['test_method'] == method and receipt['source_tests_sha256'] == digest
         and receipt['outcome'] == 'failed' and receipt['failure'] ==
         ('org.junit.ComparisonFailure: Complete accessible caption expected:<M[égse]> but was:<M[ÉGSE]>' if method.startswith('largeHungarian') else 'org.junit.ComparisonFailure: Complete accessible caption expected:<C[ancel]> but was:<C[ANCEL]>'), 'wrong failed receipt')
    obs = receipt['observations']
    need(len(obs) <= 512 and len(receipt['screenshots']) <= 20, 'evidence bounds')
    initial = d.one(obs, 'colour-2x-initial')
    identity = initial['state']
    need(initial['locale'] == d.LARGE_COLOUR_IME_METHODS[method] and initial['font_scale'] == 2
         and initial['density'] == 1 and initial['display']['raw'] == [0, 0, 640, 320], 'fixture')
    keys = ('dialog_id', 'root_id', 'field_id', 'picker_id')
    def retained(state, ime=None):
        d.verify_colour_back_state(state)
        need(all(type(state.get(k)) is int and state[k] == identity[k] != 0 for k in keys)
             and all(state.get(k) is True for k in ('same_dialog', 'same_picker', 'same_root', 'same_field',
                       'target_attached', 'target_showing', 'dialog_showing'))
             and state['value'] == '#13579B' and state['selection_start'] == 2 and state['selection_end'] == 5
             and state['picker_colour'] == -15509605 and state['commit_callbacks'] == state['closed_callbacks'] == 0
             and type(state['native_ime_present']) is bool
             and (ime is None or state['native_ime_present'] is ime), 'retained identity/value/selection/callbacks')
    retained(identity, False)
    activation = d.one(obs, 'colour-2x-synthetic-ime-activation')
    need(activation['strategy'] == 'View.requestFocus + InputMethodManager.showSoftInput(SHOW_IMPLICIT)'
         and activation['focus_request_returned'] is True and activation['field_focused'] is True
         and type(activation['ime_request_returned']) is bool, 'synthetic activation')
    retained(activation['state'])
    for event in (initial, activation):
        need(event['initial_native_field_activation'] == 'not-tested'
             and event['initial_full_hex_visibility'] == 'not-accepted', 'scope')
    ime = [o for o in obs if o['kind'] == 'colour-native-ime-window']
    need(len(ime) == 2 and [o['requested_visible'] for o in ime] == [True, False], 'IME show/hide')
    for event in ime:
        need(event['condition_passed'] is True and type(event['stable_window_ms']) is int
             and event['stable_window_ms'] >= 250 and event['root_id'] == identity['root_id']
             and event['field_id'] == identity['field_id'] and event['value'] == '#13579B', 'native IME binding')
        for window in event['windows']:
            need(window['type'] == 2 and window['configured_ime'] is True and window['root_visible'] is True
                 and window['root_children'] > 0 and window['package'] == 'com.google.android.inputmethod.latin'
                 and d.contains(initial['display']['raw'], window['bounds'])
                 and d.contains(window['bounds'], window['root_bounds'])
                 and window['root_bounds'][2] > window['root_bounds'][0]
                 and window['root_bounds'][3] > window['root_bounds'][1], 'configured rendered native IME')
    need(bool(ime[0]['windows']) and ime[1]['windows'] == [], 'real IME present then absent')
    occlusion = d.one(obs, 'colour-2x-ime-occlusion')
    retained(occlusion['state'], True)
    need([c['key'] for c in occlusion['controls']] == ['hex', 'cancel', 'use'], 'occlusion controls')
    for control in occlusion['controls']:
        raw = d.observe_colour_geometry(control['geometry'])
        d.validate_colour_ancestor_chain(control, identity['root_id'], visible_line=False)
        need(len(control['ime_overlaps']) == len(ime[0]['windows']), 'overlap coverage')
        for overlap, window in zip(control['ime_overlaps'], ime[0]['windows']):
            b = window['bounds']
            intersect = raw[0] < raw[2] and raw[1] < raw[3] and raw[0] < b[2] and b[0] < raw[2] and raw[1] < b[3] and b[1] < raw[3]
            need(overlap['window_id'] == window['id'] and overlap['overlaps'] is intersect, 'observed overlap')
    backs = [o for o in obs if o['kind'].startswith('native-back-')]
    need([o['kind'] for o in backs] == ['native-back-before', 'native-back-injected', 'native-back-after']
         and all(o['label'] == 'hide 2x colour IME' for o in backs), 'exact one Back prefix')
    before, injected, after = backs
    need(before['postcondition_met'] is False and injected['route'] == 'UiDevice.pressKeyCode(KEYCODE_BACK)'
         and injected['keycode'] == 4 and injected['injection_count'] == 1 and injected['injected'] is True
         and after['injected'] is True and after['completed'] is True and after['postcondition_met'] is True, 'Back injection/outcome')
    retained(before['state'], True); retained(injected['state']); retained(after['state'], False)
    hidden = d.one(obs, 'colour-2x-hidden-retained'); retained(hidden['state'], False)
    need(after['state']['target_focused'] is True and after['state']['focused_app_window_is_target'] is True
         and hidden['state']['target_focused'] is True and hidden['state']['focused_app_window_is_target'] is True, 'restored focus')
    order = [initial, activation, ime[0], occlusion, *backs, ime[1], hidden]
    indices = [obs.index(o) for o in order]
    need(indices == sorted(set(indices)), 'prefix lifecycle order')
    need(not any(o['kind'] in ('pointer-before', 'pointer-injected', 'colour-2x-cancelled', 'colour-2x-reopened',
                              'colour-2x-invalid-rejected', 'colour-2x-complete') for o in obs), 'unreached footer stages')
    captions = [o for o in obs if o['kind'] == 'colour-2x-caption']
    need([o['key'] for o in captions] == d.LARGE_COLOUR_IME_CAPTIONS[:-2], 'nine completed non-footer captions')
    need(all(obs.index(c) > obs.index(hidden) for c in captions), 'post-hide captions')
    for index, caption in enumerate(captions):
        text = caption['text']; length = len(text.encode('utf-16-le')) // 2
        need(caption['accessible_text'] == caption['layout_text'] == text and caption['caption_length'] == length
             and caption['root_id'] == identity['root_id'], 'complete exact pre-footer text')
        position = obs.index(caption); intrinsic = obs[position-1]
        need(intrinsic['kind'] == 'intrinsic-caption' and intrinsic['tag'] == caption['tag']
             and intrinsic['caption_length'] == length and intrinsic['lines'] == caption['lines'], 'bound intrinsic text')
        need(intrinsic['layout_height'] <= intrinsic['available_text_height'], 'intrinsic height')
        need(len(intrinsic['line_metrics']) == caption['lines'] and all(x['ellipsis'] == 0
             and -1 <= x['left'] <= x['right'] <= intrinsic['layout_width']+1 for x in intrinsic['line_metrics']), 'intrinsic width')
        lines = [o for o in obs if o['kind'] == 'colour-2x-caption-line' and o['key'] == caption['key']]
        need([o['line'] for o in lines] == list(range(caption['lines'])), 'complete sequential line coverage')
        ranges = caption['line_ranges']; end = 0
        for interval in ranges:
            need(interval[0] == end and interval[1] > end, 'contiguous text ranges'); end = interval[1]
        need(len(ranges) == caption['lines'] and end == length, 'complete full text')
        boundary = obs.index(captions[index+1]) if index+1 < len(captions) else len(obs)-1
        for line in lines:
            need(position < obs.index(line) < boundary, 'line coverage before next caption')
            d.validate_colour_ancestor_chain(line, identity['root_id'])
            need(d.contains(line['geometry']['visible'], line['line_rect']), 'complete visible caption line')
    terminal = obs[-1]
    need(terminal['kind'] == 'intrinsic-caption' and terminal['tag'] == 'About-row'
         and terminal['caption_length'] == (5 if method.startswith('largeHungarian') else 6) and terminal['lines'] == 1
         and terminal['layout_height'] <= terminal['available_text_height'], 'footer intrinsic boundary')
    return {'method': method, 'classification': 'failed/partial, not successful inventory',
            'actual_ime_shown_stable_ms': ime[0]['stable_window_ms'], 'actual_ime_absent_stable_ms': ime[1]['stable_window_ms'],
            'ime_inset_bottom_observation': ime[0]['ime_inset_bottom'], 'fullscreen_ime_observation': ime[0]['fullscreen_ime'],
            'native_back_injections': 1, 'exact_state_and_zero_callbacks_retained': True,
            'completed_nonfooter_captions': [c['key'] for c in captions],
            'completed_caption_lines': sum(c['lines'] for c in captions),
            'terminal_failure': receipt['failure'], 'footer_stages_reached': False,
            'footer_intrinsic_measured': True, 'footer_full_line_receipt_or_native_tap_reached': False,
            'interpretation': 'Raw mixed-case resource text was compared to native uppercase accessibility text. Actual transformation class/output were not recorded by this old helper; successor must record and verify them.',
            'initial_native_field_activation': 'not-tested', 'initial_full_hex_visibility': 'not-accepted',
            'simultaneous_ime_field_footer_fit': 'not-accepted'}

r = a.directory
need(sha((r/'core.zip').read_bytes()) == '3ee44f8ad4dd0adae97cf0373a48da1b9c1b0d362df3343b4e6e000286fd05fc', 'core archive digest')
identity = json.loads((r/'core/device-identity.json').read_bytes())
for key, value in {'commit':'2f7ce0477f41848c1af2f92a1587c29c10b553df', 'run_id':'40409092554', 'run_attempt':'1',
                   'source_tests_sha256':digest, 'apk_sha256':sha((r/'app-debug.apk').read_bytes()),
                   'source_sha256':sha((r/'AN-Paint-source.zip').read_bytes()), 'device_sdk':35, 'group':'core'}.items():
    need(identity[key] == value, 'device identity '+key)
with zipfile.ZipFile(r/'instrumentation-apks.zip') as z:
    need(identity['test_apk_sha256'] == sha(z.read('app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk')), 'test APK identity')
summary = json.loads((r/'core/app-dialog/androidTest-results/summary.json').read_bytes())
need(summary['source_tests_sha256'] == digest and summary['expected_tests'] == summary['completed_tests'] == 14
     and summary['returncode'] == 0 and summary['timed_out'] is False and not summary['success'], 'failed dialog phase')
original = []; failed = []; negative_probes = 0
for method in d.METHOD_SCREENS:
    archive = r/'core/dialog-export'/(method+'.zip')
    if method not in d.LARGE_COLOUR_IME_METHODS:
        original.append(d.inspect_archive(archive, method, digest)); continue
    with zipfile.ZipFile(archive) as z:
        manifest = json.loads(z.read('manifest.json')); receipt = json.loads(z.read('receipt.json'))
        expected = ['0-colour-2x-initial.png','1-colour-2x-ime-open.png','2-colour-2x-ime-hidden.png',
                    '3-colour-2x-failed-before-dismiss.png','4-failure-before-restoration.png','5-failure.png']
        need(manifest['test_passed'] is False and manifest['owner'] == d.OWNER and manifest['method'] == method
             and manifest['device_sdk'] == 35 and receipt['screenshots'] == expected, 'failed manifest')
        need(set(z.namelist()) == set(expected+['receipt.json','manifest.json']) and len(z.namelist()) == 8, 'partial archive inventory')
        need(len(manifest['files']) == 7 and {e['path'] for e in manifest['files']} == set(expected+['receipt.json']), 'manifest records')
        for entry in manifest['files']:
            data = z.read(entry['path']); need(len(data) == entry['bytes'] and sha(data) == entry['sha256'], 'file digest')
            if entry['path'].endswith('.png'): d.verify_png(data)
    outcome = verify_prefix(receipt, method)
    for mutate in [lambda x: next(o for o in x['observations'] if o['kind']=='colour-native-ime-window' and o['requested_visible']).update(windows=[]),
                   lambda x: d.one(x['observations'],'native-back-injected')['state'].update(commit_callbacks=1),
                   lambda x: d.one(x['observations'],'native-back-after')['state'].update(field_id=999),
                   lambda x: d.one(x['observations'],'colour-2x-hidden-retained')['state'].update(selection_end=6),
                   lambda x: d.one(x['observations'],'native-back-after').update(completed=False),
                   lambda x: next(o for o in x['observations'] if o['kind']=='colour-2x-caption').update(accessible_text='partial'),
                   lambda x: next(o for o in x['observations'] if o['kind']=='colour-2x-caption-line').update(ancestors=[])]:
        changed = copy.deepcopy(receipt); mutate(changed)
        try: verify_prefix(changed, method)
        except ValueError: negative_probes += 1
        else: raise ValueError('partial-prefix negative control accepted')
    try: d.inspect_archive(archive, method, digest)
    except ValueError: outcome['full_success_validator_rejected_actual_failed_archive'] = True
    else: raise ValueError('failed actual case promoted to success')
    outcome.update(zip_sha256=sha(archive.read_bytes()), files=manifest['files'])
    failed.append(outcome)
out = {'source_tests_sha256':digest, 'device_identity':identity, 'original_successful_methods':len(original),
       'original_successful_pngs':sum(e['path'].endswith('.png') for case in original for e in case['files']),
       'original_successful_exports':original, 'failed_partial_cases':failed, 'new_successful_methods':0,
       'new_successful_pngs':0, 'raw_partial_new_pngs':12, 'negative_probes_rejected':negative_probes,
       'dialog_phase_seconds':summary['elapsed_seconds'], 'dialog_phase_timed_out':False,
       'limits':'Observed failed-case prefix only. No whole lifecycle, footer, whole2x, current later develop, physical-device, glyph-ink or C05 acceptance.'}
(r/'failed-repair-prefix-verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'original_success':len(original), 'original_pngs':out['original_successful_pngs'],
                  'failed_prefixes':len(failed), 'new_success':0, 'negative_probes':negative_probes},indent=2))
