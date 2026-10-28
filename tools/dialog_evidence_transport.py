#!/usr/bin/env python3
"""Verify exact API35 installed-dialog exports; partial failures remain diagnostics."""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import stat
import hashlib
import struct
import zlib
import tempfile
import zipfile

from vertical_evidence_transport import bounded_digest, require, strict_object

OWNER = 'paint.anpaint.android'
TEST_CLASS = OWNER + '.LocalizedDialogDeviceTest'
COLOUR_CLASS = OWNER + '.ColourViewportDeviceTest'

NOTICE_METHODS = {
    'aboutThirdPartyNoticeRetainsRotationAndNativeFooterFlow': 0,
    'aboutArtworkNoticeCompletesNativeFooterFlow': 1,
    'aboutGimpTranslationNoticeCompletesNativeFooterFlow': 2,
}
KOREAN_METHODS = {
    'northKoreanAttributionAndConditionalCropUseRealConsumers': 'ko-KP',
    'southKoreanAttributionAndConditionalCropUseRealConsumers': 'ko-KR',
    'mixedKoreanAttributionAndConditionalCropUseRealConsumers': 'ko-Kore-KR',
}
KOREAN_EXPECTATIONS = Path(__file__).resolve().parents[1] / 'app/src/androidTest/assets/korean-consumer-expectations.json'
DIALOG_SCREENS = {
    'aboutThirdPartyNoticeRetainsRotationAndNativeFooterFlow': [
        '0-about-portrait.png', '1-about-landscape.png',
        '2-notice-0-initial.png', '3-notice-0-portrait.png'],
    'aboutArtworkNoticeCompletesNativeFooterFlow': ['0-notice-1-initial.png'],
    'aboutGimpTranslationNoticeCompletesNativeFooterFlow': ['0-notice-2-initial.png'],
    'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation': [
        '0-credit-landscape.png', '1-credit-portrait.png'],
}
COLOUR_SCREENS = {
    'normalAdvancedColourKeepsFiniteViewportAndFixedControls': [
        '0-colour-pre-assert-allocation.png', '1-colour-normal-before.png', '2-colour-normal-scrolled.png'],
    'retainedColourStateSurvivesRotationImeCancelAndReopen': [
        '0-retained-landscape.png', '1-retained-portrait.png', '2-retained-landscape.png',
        '3-colour-surface-dragged.png', '4-colour-ime-visible.png', '5-colour-ime-hidden.png',
        '6-colour-ime-hidden-retained.png', '7-colour-reopened-back-closed.png'],
    'hungarianColourCaptionsFitPortraitAndLandscape': [
        '0-hungarian-captions-landscape.png', '1-hungarian-captions-portrait.png'],
}
for method in KOREAN_METHODS:
    DIALOG_SCREENS[method] = ['0-korean-attribution-title.png', '1-korean-attribution-copy.png',
                            '2-korean-crop-one.png', '3-korean-crop-two.png']
LARGE_COLOUR_METHODS = {
    'largeEnglishColourCaptionsAndPreviewRemainReachable': 'en-US',
    'largeHungarianColourCaptionsAndPreviewRemainReachable': 'hu',
}
for method in LARGE_COLOUR_METHODS:
    COLOUR_SCREENS[method] = ['0-colour-large-initial.png', '1-colour-large-preview-reached.png',
                              '2-colour-large-top-reached.png']
LARGE_COLOUR_IME_METHODS = {
    'largeEnglishColourImeBackAndFooterLifecycle': 'en-US',
    'largeHungarianColourImeBackAndFooterLifecycle': 'hu',
}
for method in LARGE_COLOUR_IME_METHODS:
    COLOUR_SCREENS[method] = ['0-colour-2x-initial.png', '1-colour-2x-ime-open.png',
                              '2-colour-2x-ime-hidden.png', '3-colour-2x-cancel-reached.png',
                              '4-colour-2x-reopened.png', '5-colour-2x-use-reached.png']
LARGE_COLOUR_IME_CAPTIONS = ['colour_mode_0', 'colour_mode_3', 'colour_advanced_tab', 'colour_mode_1',
                             'colour_mode_2', 'add_custom_colour', 'selected_colour_caption',
                             'custom_colour_selection', 'colour_hex', 'cancel', 'use']
LARGE_COLOUR_CAPTIONS = ['selected_colour_caption', 'add_custom_colour', 'custom_colour_selection']
METHOD_SCREENS = {**DIALOG_SCREENS, **COLOUR_SCREENS}
# Identity is a method-to-class mapping, never a Cartesian product of two lists.
METHOD_CLASSES = {**dict.fromkeys(DIALOG_SCREENS, TEST_CLASS),
                  **dict.fromkeys(COLOUR_SCREENS, COLOUR_CLASS)}
MAX_FILE = 2 * 1024 * 1024
MAX_CASE = 24 * 1024 * 1024
MAX_TOTAL = 72 * 1024 * 1024  # Unchanged aggregate ceiling; fourteen cases contain 51 PNGs.
MAX_MANIFEST = 64 * 1024
PNG = b'\x89PNG\r\n\x1a\n'


def source_binding(summary):
    require(isinstance(summary, dict) and summary.get('success') is True
            and type(summary.get('device_sdk')) is int and summary.get('device_sdk') == 35 and summary.get('timed_out') is False
            and summary.get('returncode') == 0, 'Successful API35 dedicated dialog report required')
    digest = summary.get('source_tests_sha256')
    require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest),
            'Exact dialog test-source digest required')
    cases = summary.get('cases')
    require(isinstance(cases, list), 'Dialog report cases missing')
    require(all(isinstance(case, dict) for case in cases), 'Malformed dialog report case')
    expected = {(owner, method) for method, owner in METHOD_CLASSES.items()}
    require(len(cases) == len(expected)
            and {(c.get('classname'), c.get('name')) for c in cases} == expected
            and all(c.get('status') == 'passed' for c in cases),
            'All fourteen exact method/class pairs must pass in dedicated dialog report')
    require(type(summary.get('expected_tests')) is int and summary['expected_tests'] == len(METHOD_CLASSES)
            and type(summary.get('completed_tests')) is int and summary['completed_tests'] == len(METHOD_CLASSES)
            and summary.get('missing') == [] and summary.get('unexpected') == [] and summary.get('errors') == []
            and summary.get('included_tests') == sorted(owner + '#' + method for method, owner in METHOD_CLASSES.items()),
            'Exact selected fourteen-method two-class dialog phase required')
    return digest


def rectangle(value):
    require(isinstance(value, list) and len(value) == 4
            and all(type(v) is int for v in value), 'Malformed measured rectangle')
    require(value[2] >= value[0] and value[3] >= value[1], 'Negative rectangle size')
    return value


def contains(outer, inner):
    a, b = rectangle(outer), rectangle(inner)
    return a[0] <= b[0] < b[2] <= a[2] and a[1] <= b[1] < b[3] <= a[3]


def verify_receipt(receipt, method, digest):
    require(method in METHOD_CLASSES, 'Unknown or retired dialog method')
    require(isinstance(receipt, dict) and type(receipt.get('schema')) is int and receipt.get('schema') == 1
            and receipt.get('test_class') == METHOD_CLASSES[method] and receipt.get('test_method') == method
            and type(receipt.get('device_sdk')) is int and receipt.get('device_sdk') == 35 and receipt.get('package') == OWNER
            and receipt.get('outcome') == 'passed' and 'failure' not in receipt,
            'Incomplete or foreign dialog receipt')
    require(receipt.get('source_tests_sha256') == digest and
            receipt.get('source_binding') == 'runner-supplied-needs-host-comparison',
            'Dialog receipt is not bound to exact dialog-phase source')
    require(receipt.get('screenshots') == METHOD_SCREENS[method], 'Incomplete dialog screenshot inventory')
    observations = receipt.get('observations')
    require(isinstance(observations, list) and 0 < len(observations) <= 512,
            'Missing or excessive observations')
    require(all(isinstance(item, dict) for item in observations), 'Malformed observation')
    if method in COLOUR_SCREENS:
        verify_colour_fixture_timing(receipt, observations)
        verify_colour_profile(method, observations)
    else:
        verify_interaction_budget(receipt, observations)
        verify_native_back(method, observations)
        if method in KOREAN_METHODS:
            verify_korean_profile(method, observations)
    lines = [x for x in observations if x.get('kind') == 'caption-line-reached']
    require(lines, 'No measured caption reachability')
    for line in lines:
        require(contains(line['geometry']['visible'], line['line_rect']), 'Caption line is clipped')
    captions = [x for x in observations if x.get('kind') == 'intrinsic-caption']
    require(captions and all(type(c.get('lines')) is int and c['lines'] > 0
            and type(c.get('layout_height')) is int and c['layout_height'] > 0
            and type(c.get('available_text_height')) is int
            and c['layout_height'] <= c['available_text_height'] for c in captions),
            'Intrinsic caption clipping or missing metrics')
    for caption in captions:
        metrics = caption.get('line_metrics')
        require(isinstance(metrics, list) and len(metrics) == caption['lines']
                and type(caption.get('caption_length')) is int and caption['caption_length'] > 0
                and type(caption.get('layout_width')) is int and caption['layout_width'] > 0
                and metrics[-1].get('end') == caption['caption_length'], 'Missing caption line metrics')
        for metric in metrics:
            require(isinstance(metric, dict) and type(metric.get('ellipsis')) is int and metric['ellipsis'] == 0
                    and type(metric.get('left')) in (int, float) and type(metric.get('right')) in (int, float)
                    and -1 <= metric['left'] <= metric['right'] <= caption['layout_width'] + 1,
                    'Ellipsized or horizontally clipped caption')
    before = [x for x in observations if x.get('kind') == 'pointer-before']
    after = [x for x in observations if x.get('kind') == 'pointer-injected']
    require(before and len(before) == len(after) and [x.get('label') for x in before]
            == [x.get('label') for x in after], 'Incomplete pointer observation')
    for pointer in before:
        tap = pointer.get('tap')
        require(isinstance(tap, list) and len(tap) == 2 and all(type(v) is int for v in tap), 'Invalid pointer')
        bounds = rectangle(pointer['geometry']['visible'])
        require(bounds[0] <= tap[0] < bounds[2] and bounds[1] <= tap[1] < bounds[3], 'Pointer outside visible control')
    required = (['notice copy', 'other terms', 'notice done'] if method in NOTICE_METHODS else
                ['korean View tab', 'korean language command', 'korean language row',
                 'korean crop include linked', 'korean crop cancel'] if method in KOREAN_METHODS else
                ['credit save', 'credit copy', 'credit done'] if method ==
                'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation' else COLOUR_POINTERS[method])
    require(set(required) <= {item.get('label') for item in before}, 'Required native footer actions absent')



def korean_captions(tag):
    expected = json.loads(KOREAN_EXPECTATIONS.read_text(encoding='utf-8'))[tag]
    crop = expected['ui_crop_preview_images'].replace('%1$d', '22').replace('%2$d', '16')
    return [(key, expected[key]) for key in ('ui_image_credits', 'gallery_copy_credit')] + [
        ('ui_crop_preview_images', crop.replace('%3$d', str(count))) for count in (1, 2)]


def verify_korean_profile(method, observations):
    tag = KOREAN_METHODS[method]
    selections = [o for o in observations if o.get('kind') == 'korean-picker-selection']
    require(len(selections) == 1, 'Exact Korean picker selection missing')
    choice = selections[0]
    require(choice.get('locale') == choice.get('platform_locale') == tag
            and choice.get('resource_locale') == tag + ('-anpaint' if tag == 'ko-Kore-KR' else '')
            and type(choice.get('expected_index')) is int and choice['expected_index'] > 0
            and type(choice.get('selected_index')) is int and choice['selected_index'] == choice['expected_index'],
            'Wrong Korean public/platform/resource selection')
    captions = [o for o in observations if o.get('kind') == 'korean-consumer-caption']
    require([(o.get('key'), o.get('text')) for o in captions] == korean_captions(tag)
            and all(o.get('accessible_text') == o.get('text') for o in captions),
            'Complete source-bound Korean consumer text/accessibility required')
    # Bind measured native line coverage/reachability to each changed consumer,
    # rather than accepting an unrelated picker row's generic layout metrics.
    for index, caption in enumerate(captions):
        start = observations.index(caption)
        end = observations.index(captions[index + 1]) if index + 1 < len(captions) else len(observations)
        measured = [o for o in observations[start + 1:end] if o.get('kind') == 'intrinsic-caption'
                    and o.get('consumer_key') == caption['key']]
        lines = [o for o in observations[start + 1:end] if o.get('kind') == 'caption-line-reached'
                 and o.get('consumer_key') == caption['key']]
        require(len(measured) == 1 and measured[0].get('caption_length') == len(caption['text'].encode('utf-16-le')) // 2
                and type(measured[0].get('lines')) is int
                and [o.get('line') for o in lines] == list(range(measured[0]['lines'])),
                'Changed Korean caption lacks its own complete measured line coverage')
    states = [o for o in observations if o.get('kind') == 'korean-crop-state']
    require(len(states) == 2 and [o.get('count') for o in states] == [1, 2]
            and all(type(o.get('count')) is int and o.get('width') == 22 and o.get('height') == 16
                    and type(o.get('width')) is int and type(o.get('height')) is int
                    and o.get('placed_reference') is True and o.get('linked_peer') is True
                    and type(o.get('applications')) is int and o['applications'] == 0 for o in states),
            'Missing real conditional crop/count update')
    completed = [o for o in observations if o.get('kind') == 'korean-consumers-complete']
    require(len(completed) == 1 and completed[0].get('locale') == tag
            and completed[0].get('copy_scope') == 'display-accessibility-layout-only'
            and completed[0].get('crop_cancelled') is True
            and type(completed[0].get('applications')) is int and completed[0]['applications'] == 0,
            'Korean scope or cancellation result missing')
    require(observations.index(choice) < observations.index(captions[0])
            < observations.index(states[0]) < observations.index(states[1]) < observations.index(completed[0]),
            'Korean consumer observations must follow real selection')


def verify_interaction_budget(receipt, observations):
    starts = [o for o in observations if o.get('kind') == 'interaction-start']
    ends = [o for o in observations if o.get('kind') == 'interaction-end']
    require(len(starts) == len(ends) == 1, 'One complete interaction interval required')
    start, end = starts[0], ends[0]
    for event, fields in ((start, ('started_uptime_ms', 'deadline_uptime_ms', 'budget_ms')),
                          (end, ('started_uptime_ms', 'ended_uptime_ms', 'deadline_uptime_ms', 'elapsed_ms', 'budget_ms'))):
        require(all(type(event.get(field)) is int and event[field] >= 0 for field in fields),
                'Malformed monotonic interaction timing')
    require(start['budget_ms'] == end['budget_ms'] == 45000
            and start['started_uptime_ms'] == end['started_uptime_ms']
            and start['deadline_uptime_ms'] == end['deadline_uptime_ms'] == start['started_uptime_ms'] + 45000
            and end['elapsed_ms'] == end['ended_uptime_ms'] - start['started_uptime_ms']
            and start['started_uptime_ms'] <= end['ended_uptime_ms'] <= end['deadline_uptime_ms']
            and end.get('within_deadline') is True and end.get('block_completed') is True,
            'Unfinished or over-budget dialog interaction')
    require(observations.index(start) < observations.index(end), 'Interaction timing order changed')
    for field in ('fixture_started_uptime_ms', 'fixture_ended_uptime_ms', 'fixture_elapsed_ms',
                  'fixture_setup_elapsed_ms', 'fixture_teardown_elapsed_ms'):
        require(type(receipt.get(field)) is int and receipt[field] >= 0, 'Missing separate fixture timing')
    require(receipt.get('fixture_elapsed_scope') == 'setup+interaction+teardown; excludes export'
            and receipt['fixture_started_uptime_ms'] <= start['started_uptime_ms']
            and end['ended_uptime_ms'] <= receipt['fixture_ended_uptime_ms']
            and receipt['fixture_elapsed_ms'] == receipt['fixture_ended_uptime_ms'] - receipt['fixture_started_uptime_ms']
            and receipt['fixture_setup_elapsed_ms'] == start['started_uptime_ms'] - receipt['fixture_started_uptime_ms']
            and receipt['fixture_teardown_elapsed_ms'] == receipt['fixture_ended_uptime_ms'] - end['ended_uptime_ms'],
            'Fixture timing does not separate setup, interaction and teardown')


def verify_native_back(method, observations):
    expected = ([f'notice-{NOTICE_METHODS[method]}-{action}' for action in ('nested', 'close')]
                if method in NOTICE_METHODS else
                ['korean-credit-discard'] if method in KOREAN_METHODS else
                ['credit-discard'] if method == 'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation' else [])
    events = [o for o in observations if o.get('kind', '').startswith('native-back-')]
    require([(e.get('kind'), e.get('label')) for e in events] ==
            [(kind, label) for label in expected for kind in ('native-back-before', 'native-back-injected', 'native-back-after')],
            'Exact single-injection Back sequences required')
    start = next(i for i, o in enumerate(observations) if o.get('kind') == 'interaction-start')
    end = next(i for i, o in enumerate(observations) if o.get('kind') == 'interaction-end')
    require(all(start < i < end for i, o in enumerate(observations) if o in events),
            'Back evidence must precede interaction completion and cleanup')
    for offset in range(0, len(events), 3):
        before, injected, after = events[offset:offset + 3]
        a, b = before.get('state'), after.get('state')
        require(isinstance(a, dict) and isinstance(b, dict) and isinstance(injected.get('state'), dict), 'Missing native Back app state')
        for state in (a, injected['state'], b):
            require(all(type(state.get(key)) is bool for key in ('target_insets_available', 'focused_insets_available',
                    'focused_app_window_present', 'focused_app_window_is_target', 'focused_app_window_is_editor')),
                    'Missing focused-window/IME diagnostics')
            for available, visible in (('target_insets_available', 'target_ime_visible'),
                                       ('focused_insets_available', 'focused_app_window_ime_visible')):
                require(visible in state and (type(state[visible]) is bool if state[available] else state[visible] is None),
                        'Malformed IME visibility diagnostic')
        require(all(a.get(key) is True for key in ('target_attached', 'target_showing', 'target_focused'))
                and before.get('postcondition_met') is False, 'Back target not established before injection')
        require(injected.get('route') == 'UiDevice.pressKeyCode(KEYCODE_BACK)' and type(injected.get('keycode')) is int
                and injected['keycode'] == 4 and type(injected.get('injection_count')) is int and injected['injection_count'] == 1
                and injected.get('injected') is True and after.get('injected') is True
                and after.get('completed') is True and after.get('postcondition_met') is True,
                'Native Back injection or app outcome incomplete')
        require(b.get('target_attached') is False and b.get('target_showing') is False,
                'Specific Back window remains attached')
        if before['label'].endswith('-nested'):
            require(a.get('notice_retained') is True and b.get('notice_retained') is True and b.get('notice_focused') is True,
                    'Original notice was not retained and focused after nested Back')
        elif before['label'].endswith('-close'):
            require(a.get('notice_present') is True and b.get('notice_present') is False and b.get('editor_focused') is True,
                    'Notice Back did not return to editor')
        elif method in KOREAN_METHODS:
            require(a.get('synthetic_credit_unchanged') is True and b.get('synthetic_credit_unchanged') is True,
                    'Korean attribution Back changed the synthetic credit')
        else:
            require(a.get('dialog_showing') is True and b.get('dialog_showing') is False
                    and type(a.get('save_calls')) is int and type(b.get('save_calls')) is int
                    and a['save_calls'] == b['save_calls'] == 4
                    and type(a.get('dismiss_calls')) is int and type(b.get('dismiss_calls')) is int
                    and a['dismiss_calls'] == 1 and b['dismiss_calls'] == 2
                    and a.get('saved_draft_unchanged') is True and b.get('saved_draft_unchanged') is True,
                    'Credit Back must discard once without saving, before cleanup')


COLOUR_POINTERS = {
    'normalAdvancedColourKeepsFiniteViewportAndFixedControls': ['colour cancel'],
    'retainedColourStateSurvivesRotationImeCancelAndReopen': [
        'colour hex field', 'colour state cancel', 'invalid colour rejected', 'valid colour committed'],
    'hungarianColourCaptionsFitPortraitAndLandscape': ['Hungarian colour Cancel'],
}
COLOUR_POINTERS.update(dict.fromkeys(LARGE_COLOUR_METHODS, ['large colour Cancel']))
COLOUR_POINTERS.update(dict.fromkeys(LARGE_COLOUR_IME_METHODS,
    ['2x Cancel', '2x invalid rejected', '2x valid committed']))
COLOUR_CAPTIONS = ['colour_mode_0', 'colour_mode_3', 'colour_advanced_tab',
                   'colour_mode_1', 'colour_mode_2', 'add_custom_colour']


def verify_colour_fixture_timing(receipt, observations):
    # Accepted PR51 keeps its original source-enforced 45s deadline. It does not
    # emit PR52 interaction boundaries; do not invent timing evidence or apply
    # that looser profile to the four notice/credit methods.
    require(not any(o.get('kind') in ('interaction-start', 'interaction-end') for o in observations),
            'Colour profile must preserve its original fixture timing schema')
    for field in ('fixture_started_uptime_ms', 'fixture_ended_uptime_ms', 'fixture_elapsed_ms'):
        require(type(receipt.get(field)) is int and receipt[field] >= 0, 'Missing colour fixture timing')
    require(receipt['fixture_elapsed_ms'] == receipt['fixture_ended_uptime_ms'] - receipt['fixture_started_uptime_ms']
            and receipt.get('fixture_elapsed_scope') == 'setup+interaction+teardown; excludes export'
            and 'fixture_setup_elapsed_ms' not in receipt and 'fixture_teardown_elapsed_ms' not in receipt,
            'Colour timing must not claim unobserved interaction boundaries')


def one(observations, kind):
    values = [o for o in observations if o.get('kind') == kind]
    require(len(values) == 1, 'Expected one ' + kind)
    return values[0]


def colour_geometry(value, *, complete=False, tag=None, allocation=False):
    require(isinstance(value, dict), 'Missing native colour geometry')
    raw, visible = rectangle(value.get('raw')), rectangle(value.get('visible'))
    require(raw[2] > raw[0] and raw[3] > raw[1] and value.get('shown') is True,
            'Nonpositive or hidden colour control')
    require(contains(raw, visible), 'Invalid visible colour bounds')
    require(not complete or contains(visible, raw), 'Clipped fixed colour control')
    require(tag is None or value.get('tag') == tag, 'Wrong colour control identity')
    require(all(type(value.get(k)) is int for k in ('scroll_x', 'scroll_y')), 'Missing native scroll position')
    if allocation:
        require(all(type(value.get(k)) is int for k in ('width', 'height', 'measured_width', 'measured_height'))
                and value['width'] == raw[2] - raw[0] and value['height'] == raw[3] - raw[1]
                and value['measured_width'] > 0 and value['measured_height'] > 0,
                'Inconsistent native colour allocation')
    return raw


def verify_colour_profile(method, observations):
    """Validate native PR51 observations; source-bound pass is not universal acceptance.

    Synthetic mutation tests exercise this profile without historical artifacts.
    verify_receipt additionally enforces the composed class, source and timing.
    """
    require(method in COLOUR_SCREENS, 'Unknown colour profile')
    fixture = one(observations, 'fixture')
    lifecycle = method in LARGE_COLOUR_IME_METHODS
    large = method in LARGE_COLOUR_METHODS or lifecycle
    scale = 2 if large else 1
    locale = LARGE_COLOUR_IME_METHODS[method] if lifecycle else LARGE_COLOUR_METHODS[method] if large else ('hu' if method == 'hungarianColourCaptionsFitPortraitAndLandscape' else 'en-US')
    require(fixture.get('locale') == locale and type(fixture.get('font_scale')) in (int, float)
            and fixture['font_scale'] == scale, 'Colour acceptance requires its exact locale and font scale')
    expected_orientations = ([False, True] if large or method.startswith('normal') else
                             [False, True, False, True] if method.startswith('retained') else [False, True, False])
    orientations = [o for o in observations if o.get('kind') == 'orientation']
    require([o.get('landscape') for o in orientations] == expected_orientations
            and all(type(o.get('landscape')) is bool and type(o.get('font_scale')) in (int, float)
                    and o['font_scale'] == scale for o in orientations), 'Incomplete colour rotation coverage')
    for orientation in orientations:
        raw = colour_geometry(orientation.get('root'), complete=True)
        require((raw[2] - raw[0] > raw[3] - raw[1]) == orientation['landscape'],
                'Colour orientation disagrees with native dimensions')
    startup = [o for o in observations if o.get('kind') == 'initial-editor-state']
    require([o.get('stage') for o in startup] == ['before-wait', 'passed'], 'Missing editor readiness observations')
    ready = startup[-1]
    require(all(ready.get(k) is True for k in ('startup_ready', 'window_focus', 'root_attached'))
            and all(ready.get(k) is False for k in ('busy', 'activity_destroyed', 'activity_finishing',
                                                    'io_error_present', 'autosave_error_present', 'startup_view_present'))
            and ready.get('locale') == locale and type(ready.get('font_scale')) in (int, float)
            and ready['font_scale'] == scale, 'Colour fixture editor was not ready')
    colour_geometry(ready.get('canvas'), complete=True, tag='paint_canvas')
    pointers = [o for o in observations if o.get('kind') == 'pointer-before']
    require([o.get('label') for o in pointers] == COLOUR_POINTERS[method], 'Wrong colour native action sequence')
    pointer_events = [o for o in observations if o.get('kind') in ('pointer-before', 'pointer-injected')]
    require([(o.get('kind'), o.get('label')) for o in pointer_events] ==
            [(kind, label) for label in COLOUR_POINTERS[method] for kind in ('pointer-before', 'pointer-injected')],
            'Colour pointer injection order changed')
    for o in pointers:
        colour_geometry(o.get('geometry'))
    for route in [o for o in observations if o.get('kind') == 'colour-native-scroll-route']:
        bounds = rectangle(route.get('viewport'))
        require(bounds[2] - bounds[0] > 8 and bounds[3] - bounds[1] > 16
                and type(route.get('gutter_pixels')) is int and 0 < route['gutter_pixels'] < bounds[2] - bounds[0]
                and type(route.get('x')) is int and type(route.get('rtl')) is bool,
                'Invalid colour native scroll route')
        left, right = ((bounds[0], bounds[0] + route['gutter_pixels']) if route['rtl'] else
                       (bounds[2] - route['gutter_pixels'], bounds[2]))
        require(left <= route['x'] < right, 'Colour scroll must use the native gutter')
    if lifecycle:
        verify_large_colour_ime(method, observations)
    elif large:
        verify_large_colour_rail(method, observations)
    elif method.startswith('normal'):
        verify_colour_allocation(observations)
        require(not any(o.get('kind', '').startswith('native-back-') for o in observations), 'Unexpected colour Back')
    else:
        captions = [o for o in observations if o.get('kind') == 'intrinsic-caption' and o.get('tag') in COLOUR_CAPTIONS]
        require([o.get('tag') for o in captions] == COLOUR_CAPTIONS * (3 if method.startswith('retained') else 2),
                'Missing per-orientation intrinsic colour captions')
        for caption in captions:
            colour_geometry(caption.get('geometry'), complete=not (method.startswith('retained') and
                            caption.get('tag') in ('colour_mode_1', 'colour_mode_2')))
        if method.startswith('retained'):
            verify_colour_state(observations)
        else:
            fits = [o for o in observations if o.get('kind') == 'hungarian-colour-captions-fit']
            require([o.get('landscape') for o in fits] == [True, False]
                    and all(type(o.get('landscape')) is bool for o in fits), 'Missing Hungarian orientation results')
            for fit in fits:
                colour_geometry(fit.get('inner'), complete=True, tag='colour_editor_scroll')
                colour_geometry(fit.get('add'), complete=True, tag='add_custom_colour')
            require(not any(o.get('kind', '').startswith('native-back-') for o in observations), 'Unexpected colour Back')


def verify_large_colour_ime(method, observations):
    """Separate 2x lifecycle profile: IME occlusion is measured, never a failure oracle."""
    initial = one(observations, 'colour-2x-initial')
    require(initial.get('locale') == LARGE_COLOUR_IME_METHODS[method]
            and type(initial.get('font_scale')) in (int, float) and initial['font_scale'] == 2
            and type(initial.get('density')) in (int, float) and initial['density'] == 1
            and initial.get('setup') == 'synthetic hex #13579B selection [2,5]; synthetic focus/IME activation; native Back and footer input',
            'Wrong 2x lifecycle fixture')
    display = colour_geometry(initial.get('display'), complete=True)
    require(display[2] - display[0] == 640 and display[3] - display[1] == 320,
            '2x lifecycle requires 640x320 mdpi')
    identity = initial.get('state', {})
    identity_keys = ('dialog_id', 'root_id', 'field_id', 'picker_id')
    require(all(type(identity.get(k)) is int and identity[k] != 0 for k in identity_keys), 'Missing exact fixture identity')

    def retained(state, ime):
        verify_colour_back_state(state)
        require(all(state.get(k) == identity[k] and type(state.get(k)) is int for k in identity_keys)
                and all(state.get(k) is True for k in ('same_dialog', 'same_picker', 'same_root', 'same_field',
                    'target_attached', 'target_showing', 'dialog_showing'))
                and state.get('value') == '#13579B' and state.get('selection_start') == 2
                and state.get('selection_end') == 5 and state.get('picker_colour') == -15509605
                and state['commit_callbacks'] == state['closed_callbacks'] == 0
                and type(state.get('native_ime_present')) is bool
                and (ime is None or state['native_ime_present'] is ime), '2x draft/selection/root identity or callbacks changed')

    retained(identity, False)
    activation = one(observations, 'colour-2x-synthetic-ime-activation')
    require(activation.get('strategy') == 'View.requestFocus + InputMethodManager.showSoftInput(SHOW_IMPLICIT)'
            and activation.get('focus_request_returned') is True and activation.get('field_focused') is True
            and type(activation.get('ime_request_returned')) is bool,
            'Explicit synthetic focus/IME activation required; request return is not rendered IME evidence')
    retained(activation.get('state'), None)
    occlusion = one(observations, 'colour-2x-ime-occlusion')
    hidden = one(observations, 'colour-2x-hidden-retained')
    retained(occlusion.get('state'), True)
    retained(hidden.get('state'), False)
    require(hidden['state']['target_focused'] is True and hidden['state']['focused_app_window_is_target'] is True,
            'Hidden IME must restore exact dialog focus')
    ime_events = [o for o in observations if o.get('kind') == 'colour-native-ime-window']
    require([o.get('requested_visible') for o in ime_events] == [True, False]
            and all(type(o.get('requested_visible')) is bool for o in ime_events), 'Missing 2x native IME show/hide')
    for event in ime_events:
        require(event.get('condition_passed') is True and type(event.get('stable_window_ms')) is int
                and event['stable_window_ms'] >= 250 and event.get('root_id') == identity['root_id']
                and event.get('field_id') == identity['field_id'] and event.get('value') == '#13579B'
                and type(event.get('ime_visible')) is bool and type(event.get('fullscreen_ime')) is bool
                and type(event.get('ime_inset_bottom')) is int and event['ime_inset_bottom'] >= 0,
                'Unstable or stale-root 2x native IME evidence')
        # Inset visibility/height are observations, not the native-window oracle.
        # In fullscreen extract mode the underlying app can have zero IME inset.
        for key in ('dialog', 'field'):
            observe_colour_geometry(event.get(key))
        windows = event.get('windows')
        require(isinstance(windows, list) and len(windows) <= 16, 'Missing or excessive 2x IME windows')
        for window in windows:
            require(isinstance(window, dict) and type(window.get('id')) is int and type(window.get('type')) is int
                    and window['type'] == 2 and isinstance(window.get('package'), str) and window['package']
                    and type(window.get('root_visible')) is bool and type(window.get('configured_ime')) is bool
                    and type(window.get('root_children')) is int and window['root_children'] >= 0,
                    'Wrong native 2x IME window')
            bounds, root_bounds = rectangle(window.get('bounds')), rectangle(window.get('root_bounds'))
            require(contains(display, bounds) and contains(bounds, root_bounds), 'Empty or out-of-display native IME')
        if event['requested_visible']:
            require(any(w['configured_ime'] and w['root_visible'] and w['root_children'] > 0 for w in windows),
                    'Configured actual IME is absent')
        else:
            require(windows == [], 'Actual IME remains after Back')
    windows = ime_events[0]['windows']
    require(len({w['id'] for w in windows}) == len(windows), 'Duplicate IME window')
    controls = occlusion.get('controls')
    require(isinstance(controls, list) and [v.get('key') for v in controls] == ['hex', 'cancel', 'use'],
            'Missing raw field/footer occlusion observations')
    for control in controls:
        raw = observe_colour_geometry(control.get('geometry'))
        validate_colour_ancestor_chain(control, identity['root_id'], visible_line=False)
        overlaps = control.get('ime_overlaps')
        require(isinstance(overlaps, list) and len(overlaps) == len(windows), 'Missing actual IME overlap observations')
        for overlap, window in zip(overlaps, windows):
            b = window['bounds']
            intersects = (raw[0] < raw[2] and raw[1] < raw[3] and b[0] < b[2] and b[1] < b[3]
                          and raw[0] < b[2] and b[0] < raw[2] and raw[1] < b[3] and b[1] < raw[3])
            require(overlap.get('window_id') == window['id'] and overlap.get('overlaps') is intersects,
                    'IME overlap observation disagrees with raw geometry')
    backs = [o for o in observations if o.get('kind', '').startswith('native-back-')]
    labels = ['hide 2x colour IME', 'close 2x reopened colour']
    require([(o.get('kind'), o.get('label')) for o in backs] ==
            [(kind, label) for label in labels for kind in ('native-back-before', 'native-back-injected', 'native-back-after')],
            'Exactly one native Back per required 2x outcome')
    for offset in (0, 3):
        before, injected, after = backs[offset:offset + 3]
        for event in (before, injected, after):
            verify_colour_back_state(event.get('state'))
        require(before.get('postcondition_met') is False
                and all(before['state'][k] is True for k in ('target_attached', 'target_showing', 'target_focused', 'dialog_showing'))
                and injected.get('route') == 'UiDevice.pressKeyCode(KEYCODE_BACK)'
                and type(injected.get('keycode')) is int and injected['keycode'] == 4
                and type(injected.get('injection_count')) is int and injected['injection_count'] == 1
                and injected.get('injected') is True and after.get('injected') is True
                and after.get('completed') is True and after.get('postcondition_met') is True,
                'Missing actual 2x Back injection/outcome')
    retained(backs[0]['state'], True)
    retained(backs[1]['state'], None)  # IME may be in transition; identity/callbacks may not.
    retained(backs[2]['state'], False)
    require(backs[2]['state']['target_focused'] is True and backs[2]['state']['focused_app_window_is_target'] is True,
            'IME Back did not restore exact dialog focus')
    cancelled = one(observations, 'colour-2x-cancelled')
    require(all(type(cancelled.get(k)) is int for k in ('commit_callbacks', 'closed_callbacks', 'selected_colour', 'preview_colour'))
            and cancelled.get('commit_callbacks') == 0 and cancelled.get('closed_callbacks') == 1
            and cancelled.get('selected_colour') == cancelled.get('preview_colour') == -65536
            and cancelled.get('dialog_showing') is False and cancelled.get('root_attached') is False,
            'Native Cancel must restore original colour once')
    reopened = one(observations, 'colour-2x-reopened')
    require(all(type(reopened.get(k)) is int and reopened[k] != identity[k] for k in ('root_id', 'dialog_id'))
            and reopened.get('value') == '#FF0000', 'Reopened dialog is stale or retains cancelled draft')
    for event in backs[3:]:
        state = event['state']
        require(all(state.get(k) == reopened[k] for k in ('root_id', 'dialog_id')) and state.get('same_root') is True
                and state['commit_callbacks'] == 0 and state['closed_callbacks'] in (1, 2)
                and state.get('selected_colour') == state.get('preview_colour') == -65536,
                'Reopened Back targets stale root, changes colour or reports impossible callback counts')
    require(backs[3]['state']['closed_callbacks'] == 1 and backs[5]['state']['closed_callbacks'] == 2
            and all(backs[5]['state'][k] is False for k in ('target_attached', 'target_showing', 'dialog_showing'))
            and backs[5]['state']['focused_app_window_is_editor'] is True, 'Reopened Back failed to close once')
    invalid = one(observations, 'colour-2x-invalid-rejected')
    require(all(type(invalid.get(k)) is int for k in ('commit_callbacks', 'closed_callbacks'))
            and invalid.get('value') == '#broken' and invalid.get('dialog_showing') is True
            and invalid.get('error_present') is True and invalid.get('commit_callbacks') == 0
            and invalid.get('closed_callbacks') == 2
            and all(type(invalid.get(k)) is int and invalid[k] not in (identity[k], reopened[k]) for k in ('root_id', 'dialog_id')),
            'Invalid hex must remain in a distinct third dialog without callbacks')
    complete = one(observations, 'colour-2x-complete')
    require(type(complete.get('commit_callbacks')) is int and complete['commit_callbacks'] == 1
            and type(complete.get('closed_callbacks')) is int and complete['closed_callbacks'] == 3
            and complete.get('selected_colour') == -14391124 and complete.get('dialog_showing') is False
            and complete.get('root_attached') is False, 'Valid hex must commit exactly once')
    pointers = [o for o in observations if o.get('kind') == 'pointer-before']
    captions = [o for o in observations if o.get('kind') == 'colour-2x-caption']
    require([o.get('key') for o in captions] == LARGE_COLOUR_IME_CAPTIONS, 'Incomplete 2x caption coverage')
    for caption in captions:
        key = caption['key']
        expected_tag = 'About-row' if key in ('cancel', 'use') else key
        require(caption.get('tag') == expected_tag, 'Wrong caption control identity')
        expected_root = invalid['root_id'] if key == 'use' else identity['root_id']
        text = caption.get('text')
        raw_length = len(text.encode('utf-16-le')) // 2 if isinstance(text, str) else 0
        transformed = caption.get('transformed_text')
        length = len(transformed.encode('utf-16-le')) // 2 if isinstance(transformed, str) else 0
        require(raw_length > 0 and caption.get('raw_text_length') == raw_length and caption.get('expected_text') == text
                and isinstance(caption.get('transformation_method'), str) and caption['transformation_method']
                and type(caption.get('view_id')) is int, 'Missing exact raw/source caption or platform transformation')
        if key in ('cancel', 'use'):
            # Bounded en-US/hu fixture resources and actual API35 framework Button transform.
            # This is exact text equality, not a case-insensitive acceptance shortcut.
            expected = {'en-US': {'cancel': ('Cancel', 'CANCEL'), 'use': ('Use color', 'USE COLOR')},
                        'hu': {'cancel': ('Mégse', 'MÉGSE'), 'use': ('Szín használata', 'SZÍN HASZNÁLATA')}}
            require((text, transformed) == expected[LARGE_COLOUR_IME_METHODS[method]][key]
                    and caption.get('source_resource') == ('ui_cancel' if key == 'cancel' else 'ui_use_colour')
                    and caption['view_id'] == (16908314 if key == 'cancel' else 16908313)
                    and caption['transformation_method'] == 'android.text.method.AllCapsTransformationMethod',
                    'Wrong native footer source text, action identity or actual transformation')
        else:
            require(caption.get('source_resource') == 'view-text' and transformed == text,
                    'Unexpected non-footer caption transformation')
        require(length > 0 and caption.get('accessible_text') == transformed and caption.get('caption_length') == length
                and caption.get('root_id') == expected_root and type(caption.get('lines')) is int and caption['lines'] > 0,
                'Incomplete accessible 2x caption or wrong root')
        layout_text = caption.get('layout_text')
        require(layout_text == transformed,
                'Incomplete transformed layout text')
        ranges = caption.get('line_ranges')
        require(isinstance(ranges, list) and len(ranges) == caption['lines'], 'Incomplete layout ranges')
        end = 0
        for interval in ranges:
            require(isinstance(interval, list) and len(interval) == 2 and all(type(v) is int for v in interval)
                    and interval[0] == end and interval[1] > end, 'Skipped UTF-16 caption text')
            end = interval[1]
        require(end == length, 'Incomplete full-text caption layout')
        index = observations.index(caption)
        intrinsic = observations[index - 1]
        require(intrinsic.get('kind') == 'intrinsic-caption' and intrinsic.get('caption_length') == length
                and intrinsic.get('lines') == caption['lines'] and intrinsic.get('tag') == expected_tag,
                'Missing bound intrinsic caption measurement')
        lines = [o for o in observations if o.get('kind') == 'colour-2x-caption-line' and o.get('key') == key]
        require([o.get('line') for o in lines] == list(range(caption['lines']))
                and all(type(o.get('line')) is int for o in lines), 'Missing sequential 2x caption lines')
        boundary = observations.index(pointers[1] if key == 'use' else pointers[0])
        following = [observations.index(c) for c in captions if observations.index(c) > index]
        if following:
            boundary = min(boundary, following[0])
        positions = [observations.index(line) for line in lines]
        require(positions == sorted(set(positions)) and all(index < pos < boundary for pos in positions),
                'Caption reachability must precede its next measurement and native footer action')
        for line in lines:
            require(contains(line['geometry']['visible'], line['line_rect'])
                    and line['geometry'].get('tag') == (None if key in ('cancel', 'use') else key),
                    '2x caption line clipped or belongs to another control')
            validate_colour_ancestor_chain(line, expected_root)
    pointers = [o for o in observations if o.get('kind') == 'pointer-before']
    order = [initial, activation, ime_events[0], occlusion, *backs[:3], ime_events[1], hidden,
             *captions[:-1], pointers[0], cancelled, reopened, *backs[3:], captions[-1], pointers[1], invalid, pointers[2], complete]
    indices = [observations.index(o) for o in order]
    require(indices == sorted(set(indices)), '2x native lifecycle order changed')
    for event in (initial, occlusion, complete):
        require(event.get('simultaneous_ime_field_footer_fit') == 'not-accepted', 'Do not grant IME-open simultaneous fit')
    for event in (initial, activation, complete):
        require(event.get('initial_native_field_activation') == 'not-tested'
                and event.get('initial_full_hex_visibility') == 'not-accepted',
                'Synthetic setup must not masquerade as native initial entry or full hex visibility acceptance')


def observe_colour_geometry(value):
    """Raw/ancestor observations allow empty clipped regions while IME is open."""
    require(isinstance(value, dict), 'Missing observed geometry')
    raw, visible = rectangle(value.get('raw')), rectangle(value.get('visible'))
    require(type(value.get('shown')) is bool
            and all(type(value.get(k)) is int for k in ('scroll_x', 'scroll_y')), 'Malformed observed geometry')
    require(visible[0] == visible[2] or visible[1] == visible[3] or contains(raw, visible),
            'Visible geometry exceeds raw bounds')
    return raw


def validate_colour_ancestor_chain(line, root_id, *, visible_line=True):
    chain = line.get('ancestors')
    require(isinstance(chain, list) and 0 < len(chain) <= 32, 'Missing complete caption ancestor path')
    parent_id = line.get('parent_id')
    require(type(parent_id) is int and parent_id != 0, 'Missing caption parent identity')
    seen = set()
    for index, ancestor in enumerate(chain):
        (colour_geometry if visible_line else observe_colour_geometry)(ancestor)
        require(type(ancestor.get('id')) is int and ancestor['id'] == parent_id and parent_id not in seen
                and (not visible_line or contains(ancestor['visible'], line['line_rect']))
                and ancestor.get('is_root') is (index == len(chain) - 1), 'Incomplete or clipped ancestor chain')
        seen.add(parent_id)
        parent_id = ancestor.get('parent_id')
    require(chain[-1]['id'] == root_id and type(parent_id) is int and parent_id == 0, 'Wrong terminal dialog root')


def verify_large_colour_rail(method, observations):
    captions = [o for o in observations if o.get('kind') == 'intrinsic-caption'
                and o.get('tag') in LARGE_COLOUR_CAPTIONS]
    require([o.get('tag') for o in captions] == LARGE_COLOUR_CAPTIONS, 'Missing large colour captions')
    for caption in captions:
        lines = [o for o in observations if o.get('kind') == 'caption-line-reached'
                 and o.get('tag') == caption['tag']]
        require(all(type(o.get('line')) is int and o.get('geometry', {}).get('tag') == caption['tag'] for o in lines)
                and [o.get('line') for o in lines] == list(range(caption['lines'])),
                'Every large caption line must be reached with native input')
    reached = one(observations, 'colour-large-rail-reached')
    require(type(reached.get('density')) in (int, float) and reached['density'] == 1
            and type(reached.get('font_scale')) in (int, float) and reached['font_scale'] == 2,
            'Large colour fixture must retain 2x at mdpi')
    display = colour_geometry(reached.get('display'), complete=True)
    require(display[2] - display[0] == 640 and display[3] - display[1] == 320,
            'Large colour fixture must be short landscape')
    require(type(reached.get('text_size')) in (int, float) and math.isfinite(reached['text_size']) and reached['text_size'] > 12
            and reached['text_size'] == reached.get('expected_text_size'), 'Scaled 12sp caption changed')
    for key, tag in (('controls', 'colour_controls_scroll'), ('editor', 'colour_editor_scroll'),
                     ('add', 'add_custom_colour'), ('selected', 'selected_colour_caption'),
                     ('sample', 'new_colour_preview')):
        raw = colour_geometry(reached.get(key), complete=True, tag=tag)
        require(contains(display, raw), 'Large rail control outside display')
        if key in ('add', 'selected', 'sample'):
            require(contains(reached['controls']['raw'], raw), 'Large preview control outside its rail')
    add, sample = reached['add']['raw'], reached['sample']['raw']
    controls, editor = reached['controls']['raw'], reached['editor']['raw']
    rail_width = controls[2] - controls[0]
    require(rail_width > 220, 'Large-font rail must be wider than 220px at mdpi')
    require(editor[2] - editor[0] >= rail_width, 'Large-font rail must not starve editor width')
    require(add[3] - add[1] >= 48 and sample[2] - sample[0] == 64 and sample[3] - sample[1] == 24,
            'Large rail must preserve the action and preview sizes')
    require(type(reached.get('content_height')) is int and type(reached.get('viewport_height')) is int
            and reached['viewport_height'] == reached['controls']['raw'][3] - reached['controls']['raw'][1] > 0
            and reached['content_height'] > 0 and type(reached.get('overflow')) is bool
            and reached['overflow'] == (reached['content_height'] > reached['viewport_height']),
            'Invalid large rail allocation')
    require(0 <= reached['controls']['scroll_y'] <= max(0, reached['content_height'] - reached['viewport_height']),
            'Large rail scroll outside its content range')
    require(not reached['overflow'] or reached['controls']['scroll_y'] > 0,
            'Overflow must be reached by native scrolling')
    require(method != 'largeHungarianColourCaptionsAndPreviewRemainReachable' or reached['overflow'],
            'Hungarian long caption must exercise overflow')
    require(type(reached.get('editor_before')) is int
            and reached['editor']['scroll_y'] == reached['editor_before'], 'Rail scroll moved colour editor')
    endpoint_before, endpoint_after = verify_colour_endpoint(observations, reached)
    top = one(observations, 'colour-large-rail-top-reached')
    for key, tag in (('heading', 'custom_colour_selection'), ('slot', 'custom_colour_0'),
                     ('controls', 'colour_controls_scroll')):
        raw = colour_geometry(top.get(key), complete=True, tag=tag)
        require(contains(display, raw) and contains(top['controls']['raw'], raw), 'Large saved controls outside rail/display')
    require(top['controls']['raw'] == reached['controls']['raw'] and top['controls']['scroll_y'] == 0,
            'The same rail must return to its top endpoint')
    cancelled = one(observations, 'colour-large-cancelled')
    require(type(cancelled.get('commit_callbacks')) is int and cancelled['commit_callbacks'] == 0
            and type(cancelled.get('closed_callbacks')) is int and cancelled['closed_callbacks'] == 1
            and cancelled.get('dialog_attached') is False and cancelled.get('dialog_showing') is False,
            'Large colour Cancel must close without committing')
    before, injected = one(observations, 'pointer-before'), one(observations, 'pointer-injected')
    require(observations.index(reached) < observations.index(endpoint_before) < observations.index(endpoint_after)
            < observations.index(top) < observations.index(before)
            < observations.index(injected) < observations.index(cancelled), 'Large rail native outcome order changed')
    require(not any(o.get('kind', '').startswith('native-back-') for o in observations), 'Unexpected colour Back')


def verify_colour_endpoint(observations, reached):
    before, after = (one(observations, 'colour-endpoint-' + stage) for stage in ('before', 'after'))
    limit = reached['content_height'] - reached['viewport_height']
    require(limit > 0 and before.get('setup') == 'synthetic one-pixel offset; reveal uses native input'
            and before.get('framework_can_scroll') is False, 'Missing last-pixel regression precondition')
    for event, offset in ((before, limit - 1), (after, limit)):
        require(type(event.get('scroll_limit')) is int and event['scroll_limit'] == limit,
                'Wrong native rail scroll limit')
        colour_geometry(event.get('controls'), complete=True, tag='colour_controls_scroll')
        require(event['controls']['raw'] == reached['controls']['raw']
                and event['controls']['scroll_y'] == offset, 'Native last-pixel scroll endpoint not reached')
        colour_geometry(event.get('sample'), complete=event is after, tag='new_colour_preview')
    raw = before['sample']['raw']
    visible = before['sample']['visible']
    require(raw == [v + (1 if i in (1, 3) else 0) for i, v in enumerate(after['sample']['raw'])]
            and visible == [raw[0], raw[1], raw[2], raw[3] - 1]
            and raw[3] == before['controls']['raw'][3] + 1,
            'Last-pixel precondition must hide exactly one bottom pixel')
    require(after['sample']['raw'] == reached['sample']['raw'], 'Native endpoint changed preview allocation')
    colour_geometry(after.get('editor'), complete=True, tag='colour_editor_scroll')
    require(after['editor']['raw'] == reached['editor']['raw']
            and after['editor']['scroll_y'] == reached['editor_before'], 'Endpoint gesture moved colour editor')
    gestures = [o for o in observations[observations.index(before) + 1:observations.index(after)]
                if o.get('kind') == 'native-scroll-injected']
    require(len(gestures) == 1 and gestures[0].get('viewport') == before['controls']['visible']
            and type(gestures[0].get('direction')) is int and gestures[0]['direction'] == 1
            and type(gestures[0].get('hidden')) is int and gestures[0]['hidden'] == 1,
            'One native gesture must reveal the last pixel before endpoint acceptance')
    return before, after


def verify_colour_allocation(observations):
    before = one(observations, 'colour-pre-assert-allocation')
    after = one(observations, 'colour-finite-bounds')
    require(type(before.get('device_sdk')) is int and before['device_sdk'] == 35
            and type(before.get('font_scale')) in (int, float) and before['font_scale'] == 1
            and type(after.get('scale')) in (int, float) and after['scale'] == 1, 'Wrong colour allocation scope')
    for key in ('display', 'dialog', 'holder', 'holder_parent', 'inner', 'inner_content'):
        colour_geometry(before.get(key), complete=key != 'inner_content', allocation=True)
    require(contains(before['visible_display_frame'], before['dialog']['raw'])
            and contains(before['dialog']['raw'], before['holder']['raw'])
            and contains(before['holder']['raw'], before['inner']['raw'])
            and before['inner_content']['height'] > before['inner']['height'], 'Colour viewport is not finite and scrollable')
    colour_geometry(after.get('inner'), complete=True, tag='colour_editor_scroll')
    require(after['inner']['raw'] == before['inner']['raw']
            and after['inner']['scroll_y'] > before['inner']['scroll_y'], 'Native colour scroll did not advance the viewport')
    tags = ['colour_advanced_tab', 'custom_colours_panel', 'add_custom_colour']
    for state in (before, after):
        fixed = state.get('fixed')
        require(isinstance(fixed, list) and [o.get('tag') for o in fixed] == tags, 'Missing exact fixed colour controls')
        for geometry in fixed:
            colour_geometry(geometry, complete=True)
            require(contains(before['holder']['raw'], geometry['raw']), 'Fixed colour control outside holder')
    require([g['raw'] for g in before['fixed']] == [g['raw'] for g in after['fixed']], 'Fixed controls moved during native scroll')
    routes = [o for o in observations if o.get('kind') == 'colour-native-scroll-route']
    require(len(routes) == 1 and routes[0].get('viewport') == before['inner']['visible']
            and observations.index(before) < observations.index(routes[0]) < observations.index(after),
            'Missing measured native scroll between allocation and outcome')


def verify_colour_back_state(state):
    require(isinstance(state, dict), 'Missing colour Back state')
    for key in ('target_attached', 'target_showing', 'target_focused', 'target_insets_available',
                'focused_insets_available', 'focused_app_window_present',
                'focused_app_window_is_target', 'focused_app_window_is_editor', 'dialog_showing'):
        require(type(state.get(key)) is bool, 'Missing colour Back focused-window state')
    for available, visible in (('target_insets_available', 'target_ime_visible'),
                               ('focused_insets_available', 'focused_app_window_ime_visible')):
        require(visible in state and (type(state[visible]) is bool if state[available] else state[visible] is None),
                'Malformed colour Back IME state')
    require(all(type(state.get(k)) is int and state[k] >= 0 for k in ('commit_callbacks', 'closed_callbacks')),
            'Missing colour callback state')


def verify_colour_state(observations):
    drag = one(observations, 'colour-surface-native-drag')
    require(all(type(drag.get(k)) is int for k in ('before_colour', 'after_colour', 'scroll_before', 'scroll_after'))
            and drag['before_colour'] != drag['after_colour'] and drag['scroll_before'] == drag['scroll_after'],
            'Native surface drag failed or moved its parent scroll')
    ime = [o for o in observations if o.get('kind') == 'colour-native-ime-window']
    require([o.get('requested_visible') for o in ime] == [True, False]
            and all(type(o.get('requested_visible')) is bool for o in ime), 'Missing native IME show/hide evidence')
    for event in ime:
        showing = event['requested_visible']
        require(event.get('condition_passed') is True and event.get('ime_visible') is showing
                and type(event.get('stable_window_ms')) is int and event['stable_window_ms'] >= 250
                and type(event.get('ime_inset_bottom')) is int and event['ime_inset_bottom'] >= 0
                and type(event.get('fullscreen_ime')) is bool and event.get('value') == '#13579B',
                'Unstable or inconsistent native IME evidence')
        colour_geometry(event.get('dialog'), complete=True)
        colour_geometry(event.get('field'), tag='colour_hex')
        windows = event.get('windows')
        require(isinstance(windows, list) and all(isinstance(w, dict) for w in windows), 'Missing native IME windows')
        if showing:
            require(windows and any(w.get('configured_ime') is True and w.get('root_visible') is True
                    and type(w.get('root_children')) is int and w['root_children'] > 0 for w in windows),
                    'Configured IME window not established')
            for window in windows:
                require(type(window.get('type')) is int and window['type'] == 2
                        and isinstance(window.get('package'), str) and window['package'], 'Wrong native IME window')
                bounds = rectangle(window.get('bounds'))
                root_bounds = rectangle(window.get('root_bounds'))
                display = [o for o in observations if o.get('kind') == 'orientation'][-1]['root']['raw']
                require(contains(display, bounds) and contains(bounds, root_bounds),
                        'Native IME window bounds exceed the observed display')
        else:
            require(windows == [] and event['ime_inset_bottom'] == 0, 'Native IME remains after Back')
    labels = ['hide colour IME', 'close reopened colour picker']
    backs = [o for o in observations if o.get('kind', '').startswith('native-back-')]
    require([(o.get('kind'), o.get('label')) for o in backs] ==
            [(kind, label) for label in labels for kind in ('native-back-before', 'native-back-injected', 'native-back-after')],
            'Exact single-injection colour Back sequences required')
    for offset in (0, 3):
        before, injected, after = backs[offset:offset + 3]
        for event in (before, injected, after):
            verify_colour_back_state(event.get('state'))
        a, b = before['state'], after['state']
        require(all(a[k] is True for k in ('target_attached', 'target_showing', 'target_focused', 'dialog_showing'))
                and before.get('postcondition_met') is False, 'Colour Back target was not established')
        require(injected.get('route') == 'UiDevice.pressKeyCode(KEYCODE_BACK)'
                and type(injected.get('keycode')) is int and injected['keycode'] == 4
                and type(injected.get('injection_count')) is int and injected['injection_count'] == 1
                and injected.get('injected') is True and after.get('injected') is True
                and after.get('completed') is True and after.get('postcondition_met') is True,
                'Native colour Back injection/outcome incomplete')
        require(a['commit_callbacks'] == b['commit_callbacks'] == 0, 'Colour Back committed a draft')
        if offset == 0:
            require(a['target_ime_visible'] is True and b['target_ime_visible'] is False
                    and b['focused_app_window_ime_visible'] is False
                    and all(b[k] is True for k in ('target_attached', 'target_showing', 'target_focused',
                                                  'dialog_showing', 'focused_app_window_is_target'))
                    and a['closed_callbacks'] == b['closed_callbacks'] == 0
                    and a.get('value') == b.get('value') == '#13579B'
                    and type(b.get('ime_inset_bottom')) is int and b['ime_inset_bottom'] == 0,
                    'IME Back must retain the colour draft and dialog')
        else:
            require(all(b[k] is False for k in ('target_attached', 'target_showing', 'dialog_showing'))
                    and b['focused_app_window_is_editor'] is True
                    and a['closed_callbacks'] == 1 and b['closed_callbacks'] == 2
                    and all(type(state.get(k)) is int and state[k] == -65536
                            for state in (a, b) for k in ('selected_colour', 'preview_colour')),
                    'Reopened Back must discard once and restore editor without committing')
    complete = one(observations, 'colour-retained-state-complete')
    require(type(complete.get('commit_callbacks')) is int and complete['commit_callbacks'] == 1
            and type(complete.get('closed_callbacks')) is int and complete['closed_callbacks'] == 3
            and complete.get('selected') == '#2468AC', 'Invalid/valid colour commit outcome missing')
    pointers = [o for o in observations if o.get('kind') == 'pointer-before']
    ordered = [drag, pointers[0], ime[0], *backs[:3], ime[1], pointers[1],
               *backs[3:], pointers[2], pointers[3], complete]
    indices = [observations.index(o) for o in ordered]
    require(indices == sorted(set(indices)), 'Colour native action/outcome order changed')


def verify_png(data):
    """Check the bounded static RGB8/RGBA8 native profile, not general PNG.

    Unsupported encodings/chunks fail explicitly. Pixel interpretation and visual
    acceptance still require review of the original image with a standard decoder.
    """
    require(0 < len(data) <= MAX_FILE and data.startswith(PNG), 'Non-PNG or oversized screenshot')
    offset, compressed, metadata = len(PNG), [], set()
    header_seen = ended = False
    while offset < len(data):
        require(offset + 12 <= len(data), 'Truncated PNG chunk')
        size = struct.unpack('>I', data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        require(kind in (b'IHDR', b'sRGB', b'sBIT', b'IDAT', b'IEND'),
                f'Unsupported native screenshot PNG chunk: {kind!r}')
        end = offset + 12 + size
        require(end <= len(data), 'Truncated PNG payload')
        require(zlib.crc32(data[offset + 4:end - 4]) & 0xffffffff ==
                struct.unpack('>I', data[end - 4:end])[0], 'Corrupt PNG CRC')
        require(header_seen or kind == b'IHDR', 'Missing PNG header')
        value = data[offset + 8:end - 4]
        if kind == b'IHDR':
            require(not header_seen and size == 13, 'Duplicate or invalid PNG header')
            width, height, depth, colour, compression, filtering, interlace = struct.unpack('>IIBBBBB', value)
            require(0 < width <= 4096 and 0 < height <= 4096, 'Invalid screenshot dimensions')
            require(colour in (2, 6) and depth == 8 and compression == filtering == interlace == 0,
                    'Unsupported native screenshot encoding: expected noninterlaced RGB8/RGBA8')
            channels = 3 if colour == 2 else 4
            row_bytes = width * channels
            expected = height * (row_bytes + 1)
            require(expected <= MAX_CASE, 'Oversized decoded screenshot')
            header_seen = True
        elif kind in (b'sRGB', b'sBIT'):
            require(kind not in metadata and not compressed, 'Duplicate or late native screenshot metadata')
            if kind == b'sRGB':
                require(size == 1 and value[0] <= 3, 'Invalid native screenshot sRGB intent')
            else:
                require(size == channels and all(1 <= byte <= 8 for byte in value),
                        'Invalid native screenshot significant bits')
            metadata.add(kind)
        elif kind == b'IDAT':
            compressed.append(value)
        else:
            require(size == 0 and end == len(data), 'Invalid PNG ending or trailing data')
            ended = True
        offset = end
    require(ended and compressed, 'Incomplete PNG screenshot')
    decoder = zlib.decompressobj()
    try:
        pixels = decoder.decompress(b''.join(compressed), expected + 1)
    except zlib.error as error:
        raise ValueError('Corrupt PNG compressed pixels') from error
    require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
            and len(pixels) == expected and all(pixels[i] <= 4 for i in range(0, expected, row_bytes + 1)),
            'Incomplete or invalid PNG scanlines')


def inspect_archive(archive, method, digest):
    require(method in METHOD_CLASSES, 'Unknown or retired dialog method')
    require(not archive.is_symlink() and archive.is_file(), 'Nonregular dialog ZIP')
    size = archive.stat().st_size
    require(0 < size <= MAX_CASE, 'Empty or oversized dialog ZIP')
    with archive.open('rb') as stream:
        archive_digest = bounded_digest(stream, size)
    expected = {'receipt.json', *METHOD_SCREENS[method]}
    with zipfile.ZipFile(archive) as zipped:
        members = zipped.infolist()
        names = [entry.filename for entry in members]
        require(len(names) == len(set(names)) and set(names) == expected | {'manifest.json'},
                'Incomplete, extra or unsafe dialog export members')
        for member in members:
            require(not member.is_dir() and stat.S_IFMT(member.external_attr >> 16) in (0, stat.S_IFREG)
                    and not member.flag_bits & 1 and member.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED),
                    'Nonregular or unsupported dialog ZIP member')
            require(0 < member.file_size <= (MAX_MANIFEST if member.filename == 'manifest.json' else MAX_FILE)
                    and 0 <= member.compress_size <= MAX_CASE, 'Oversized dialog ZIP member')
        require(sum(m.file_size for m in members) <= MAX_CASE, 'Oversized uncompressed dialog case')
        manifest_bytes = zipped.read('manifest.json')
        manifest = json.loads(manifest_bytes, object_pairs_hook=strict_object)
        require(isinstance(manifest, dict) and set(manifest) == {'schema', 'owner', 'method', 'device_sdk', 'test_passed', 'files'}
                and type(manifest['schema']) is int and manifest['schema'] == 1 and manifest['owner'] == OWNER
                and manifest['method'] == method and type(manifest['device_sdk']) is int
                and manifest['device_sdk'] == 35 and manifest['test_passed'] is True,
                'Incomplete or foreign dialog manifest')
        entries = manifest['files']
        require(isinstance(entries, list) and len(entries) == len(expected), 'Missing file records')
        seen = set()
        for entry in entries:
            require(isinstance(entry, dict) and set(entry) == {'path', 'bytes', 'sha256'}, 'Malformed file record')
            name = entry['path']
            require(isinstance(name, str) and name in expected and name not in seen, 'Duplicate or unsafe record path')
            seen.add(name)
            require(type(entry['bytes']) is int and 0 < entry['bytes'] <= MAX_FILE
                    and entry['bytes'] == zipped.getinfo(name).file_size, 'File length mismatch')
            require(isinstance(entry['sha256'], str) and re.fullmatch('[0-9a-f]{64}', entry['sha256']), 'Malformed digest')
            with zipped.open(name) as stream:
                require(bounded_digest(stream, entry['bytes']) == entry['sha256'], 'File digest mismatch')
            if name.endswith('.png'):
                verify_png(zipped.read(name))
        require(seen == expected, 'Missing export records')
        verify_receipt(json.loads(zipped.read('receipt.json'), object_pairs_hook=strict_object), method, digest)
    return {'method': method, 'test_class': METHOD_CLASSES[method],
            'profile': ('colour-2x-ime-lifecycle-original-deadline' if method in LARGE_COLOUR_IME_METHODS else
                        'colour-original-deadline' if method in COLOUR_SCREENS else 'dialog-whole-interaction'),
            'zip_bytes': size, 'zip_sha256': archive_digest,
            'manifest_bytes': len(manifest_bytes), 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
            'files': entries}


def extract(exports, destination, dialog_summary):
    summary_bytes = dialog_summary.read_bytes()
    digest = source_binding(json.loads(summary_bytes, object_pairs_hook=strict_object))
    require(not exports.is_symlink() and exports.is_dir(), 'Missing dialog export directory')
    require({p.name for p in exports.iterdir()} == {m + '.zip' for m in METHOD_SCREENS}, 'Wrong dialog export inventory')
    require(not os.path.lexists(destination), 'Dialog destination must be fresh')
    receipts = [inspect_archive(exports / (method + '.zip'), method, digest) for method in METHOD_SCREENS]
    require(sum(e['bytes'] for r in receipts for e in r['files']) <= MAX_TOTAL, 'Combined dialog evidence oversized')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.dialog-evidence-', dir=destination.parent) as temporary:
        staged = Path(temporary) / 'evidence'
        staged.mkdir()
        (staged / 'source-summary.json').write_bytes(summary_bytes)
        for receipt in receipts:
            archive = exports / (receipt['method'] + '.zip')
            with archive.open('rb') as stream:
                require(bounded_digest(stream, receipt['zip_bytes']) == receipt['zip_sha256'], 'Dialog ZIP changed')
            folder = staged / receipt['method']
            folder.mkdir()
            with zipfile.ZipFile(archive) as zipped:
                manifest_bytes = zipped.read('manifest.json')
                require(hashlib.sha256(manifest_bytes).hexdigest() == receipt['manifest_sha256'], 'Dialog manifest changed')
                (folder / 'manifest.json').write_bytes(manifest_bytes)
                for entry in receipt['files']:
                    with zipped.open(entry['path']) as source, (folder / entry['path']).open('xb') as output:
                        require(bounded_digest(source, entry['bytes'], output) == entry['sha256'], 'Dialog data changed')
        require(not os.path.lexists(destination), 'Destination appeared during validation')
        os.rename(staged, destination)
    return {'success': True, 'scope': ('source-bound-installed-api35-notice-credit-and-normal-font-colour; '
                                     'ko-KP/ko-KR/ko-Kore-KR real-picker attribution-controls and conditional crop status; '
                                     'en-US/hu 2x 640x320 mdpi preview-rail reachability and Cancel only; '
                                     'separate native IME/Back/footer lifecycle; whole-dialog and universal 2x not accepted'),
            'source_tests_sha256': digest, 'source_report': 'dedicated dialog instrumentation summary',
            'source_report_sha256': hashlib.sha256(summary_bytes).hexdigest(), 'device_sdk': 35,
            'cases': receipts, 'normal_font_colour_source_bound_pass': True,
            'large_font_preview_rail_source_bound_pass': True,
            'large_font_ime_footer_lifecycle_source_bound_pass': True,
            'large_font_ime_footer_scope': 'API35 en-US/hu 2x 640x320 mdpi; native IME presence/absence, retained Back, sequential captions/footers and callbacks only',
            'large_font_ime_activation': 'synthetic requestFocus + showSoftInput; actual configured native IME separately required',
            'initial_native_field_activation': 'not-tested',
            'initial_full_hex_visibility': 'not-accepted',
            'large_font_preview_rail_scope': 'API35 en-US/hu 2x 640x320 mdpi, native caption/preview/top reachability and Cancel only',
            'universal_colour_acceptance': False,
            'colour_interaction_timing': 'original source-enforced 45000ms deadline; no exported whole-interval measurement',
            'large_text_short_landscape_advanced_colour': 'not-accepted',
            'simultaneous_ime_field_footer_fit': 'not-accepted',
            'physical_device_or_linguistic_acceptance': False}



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exports', type=Path)
    parser.add_argument('--dialog-summary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    args.receipt.unlink(missing_ok=True)
    result = extract(args.exports, args.output, args.dialog_summary)
    args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'success': True, 'cases': len(result['cases']), 'device_sdk': 35}))


if __name__ == '__main__':
    main()
