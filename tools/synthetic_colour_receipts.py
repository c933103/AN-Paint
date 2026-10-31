"""Small authored transport models. Never recorded Android evidence or acceptance."""
import copy

from dialog_evidence_transport import (COLOUR_CAPTIONS, COLOUR_CLASS, COLOUR_POINTERS,
                                       COLOUR_SCREENS, LARGE_COLOUR_METHODS, LARGE_COLOUR_CAPTIONS, LARGE_COLOUR_IME_METHODS, OWNER)


def geometry(tag=None, bounds=(10, 20, 110, 60), **changes):
    value = dict(tag=tag, raw=list(bounds), visible=list(bounds), shown=True,
                 scroll_x=0, scroll_y=0, width=bounds[2]-bounds[0], height=bounds[3]-bounds[1],
                 measured_width=bounds[2]-bounds[0], measured_height=bounds[3]-bounds[1])
    value.update(changes)
    return value


def synthetic_colour_endpoint(reached):
    """Authored one-pixel precondition and native-input outcome model."""
    limit = reached['content_height'] - reached['viewport_height']
    controls = copy.deepcopy(reached['controls'])
    sample = copy.deepcopy(reached['sample'])
    controls['scroll_y'] = limit - 1
    sample['raw'] = [v + (1 if i in (1, 3) else 0) for i, v in enumerate(sample['raw'])]
    sample['visible'] = sample['raw'][:]
    sample['visible'][3] -= 1
    return [dict(kind='colour-endpoint-before', setup='synthetic one-pixel offset; reveal uses native input',
                 scroll_limit=limit, framework_can_scroll=False, controls=controls, sample=sample),
            dict(kind='native-scroll-injected', viewport=controls['visible'][:], direction=1, hidden=1),
            dict(kind='colour-endpoint-after', scroll_limit=limit, controls=copy.deepcopy(reached['controls']),
                 sample=copy.deepcopy(reached['sample']), editor=copy.deepcopy(reached['editor']))]


def synthetic_colour_ime_observations(method):
    """Authored bounded positive/negative oracle input, never installed evidence."""
    from dialog_evidence_transport import LARGE_COLOUR_IME_METHODS, LARGE_COLOUR_IME_CAPTIONS
    observations = []
    root_id = 101
    def state(ime=False, showing=True, closes=0, reopened=False):
        return dict(target_attached=showing, target_showing=showing, target_focused=showing,
                    target_insets_available=showing, target_ime_visible=False if showing else None,
                    focused_insets_available=True, focused_app_window_present=True,
                    focused_app_window_is_target=showing, focused_app_window_is_editor=not showing,
                    focused_app_window_ime_visible=False, dialog_showing=showing,
                    commit_callbacks=0, closed_callbacks=closes, value='#13579B',
                    selected_colour=-65536, preview_colour=-65536, selection_start=2, selection_end=5,
                    picker_colour=-15509605, native_ime_present=ime, dialog_id=202 if reopened else 102,
                    root_id=201 if reopened else 101, field_id=103, picker_id=104,
                    same_dialog=True, same_picker=True, same_root=True, same_field=True)
    def chain(root=101):
        return [geometry(bounds=(0, 0, 640, 320), id=7, parent_id=root, is_root=False),
                geometry(bounds=(0, 0, 640, 320), id=root, parent_id=0, is_root=True)]
    def caption(key, root=101, lifecycle=True):
        tag = 'About-row' if key in ('cancel', 'use') else key
        geometry_tag = None if key in ('cancel', 'use') else key
        text = '#13579B' if key == 'colour_hex' else 'Synthetic caption'
        transformed = text
        source_resource, view_id, transformation = 'view-text', -1, 'none'
        if key in ('cancel', 'use'):
            texts = {'en-US': {'cancel': ('Cancel', 'CANCEL'), 'use': ('Use color', 'USE COLOR')},
                     'hu': {'cancel': ('Mégse', 'MÉGSE'), 'use': ('Szín használata', 'SZÍN HASZNÁLATA')}}
            text, transformed = texts[LARGE_COLOUR_IME_METHODS[method]][key]
            source_resource = 'ui_cancel' if key == 'cancel' else 'ui_use_colour'
            view_id = 16908314 if key == 'cancel' else 16908313
            transformation = 'android.text.method.AllCapsTransformationMethod'
        observations.append(dict(kind='intrinsic-caption', tag=tag, lines=1, layout_height=20,
                                 available_text_height=30, caption_length=len(transformed), layout_width=100,
                                 line_metrics=[dict(end=len(transformed), ellipsis=0, left=0, right=99)], geometry=geometry(key)))
        if lifecycle:
            observations.append(dict(kind='colour-2x-caption', key=key, tag=tag, text=text, raw_text_length=len(text),
                                     expected_text=text, source_resource=source_resource, view_id=view_id,
                                     transformation_method=transformation, transformed_text=transformed,
                                     accessible_text=transformed, layout_text=transformed, lines=1,
                                     caption_length=len(transformed), root_id=root, line_ranges=[[0, len(transformed)]]))
            observations.append(dict(kind='colour-2x-caption-line', key=key, line=0,
                                     line_rect=[11, 21, 100, 40], geometry=geometry(geometry_tag), parent_id=7, ancestors=chain(root)))
        else:
            observations.append(dict(kind='caption-line-reached', tag=key, line=0,
                                     geometry=geometry(key), line_rect=[11, 21, 100, 40]))
    def pointer(label):
        caption(label, lifecycle=False)
        observations.extend([dict(kind='pointer-before', label=label, tap=[50, 40], geometry=geometry()),
                             dict(kind='pointer-injected', label=label)])
    windows = [dict(id=5, type=2, package='synthetic.ime', configured_ime=True, root_visible=True,
                    root_children=1, bounds=[0, 0, 640, 320], root_bounds=[0, 0, 640, 320])]
    def ime(showing):
        observations.append(dict(kind='colour-native-ime-window', requested_visible=showing,
                                 condition_passed=True, stable_window_ms=250, ime_visible=False, ime_inset_bottom=0,
                                 fullscreen_ime=True, root_id=101, field_id=103, value='#13579B',
                                 dialog=geometry(), field=geometry('colour_hex'), windows=copy.deepcopy(windows) if showing else []))
    def back(label, before, after):
        observations.extend([
            dict(kind='native-back-before', label=label, state=before, postcondition_met=False),
            dict(kind='native-back-injected', label=label, state=copy.deepcopy(after),
                 route='UiDevice.pressKeyCode(KEYCODE_BACK)', keycode=4, injection_count=1, injected=True),
            dict(kind='native-back-after', label=label, state=after, injected=True, completed=True, postcondition_met=True)])
    observations.append(dict(kind='colour-2x-initial', locale=LARGE_COLOUR_IME_METHODS[method], density=1, font_scale=2,
                             setup='synthetic hex #13579B selection [2,5]; synthetic focus/IME activation; native Back and footer input',
                             initial_native_field_activation='not-tested', initial_full_hex_visibility='not-accepted',
                             display=geometry(bounds=(0, 0, 640, 320)), state=state(), simultaneous_ime_field_footer_fit='not-accepted'))
    observations.append(dict(kind='colour-2x-synthetic-ime-activation',
                             strategy='View.requestFocus + InputMethodManager.showSoftInput(0)',
                             focus_request_returned=True, field_focused=True, ime_request_returned=False, state=state(),
                             initial_native_field_activation='not-tested', initial_full_hex_visibility='not-accepted'))
    ime(True)
    observations.append(dict(kind='colour-2x-ime-occlusion', state=state(ime=True),
                             simultaneous_ime_field_footer_fit='not-accepted',
                             controls=[dict(key=key, geometry=geometry(), parent_id=7, ancestors=chain(),
                                            ime_overlaps=[dict(window_id=5, overlaps=True)]) for key in ('hex', 'cancel', 'use')]))
    back('hide 2x colour IME', state(ime=True), state())
    ime(False)
    observations.append(dict(kind='colour-2x-hidden-retained', state=state()))
    for key in LARGE_COLOUR_IME_CAPTIONS[:-1]:
        caption(key)
    pointer('2x Cancel')
    observations.append(dict(kind='colour-2x-cancelled', commit_callbacks=0, closed_callbacks=1,
                             selected_colour=-65536, preview_colour=-65536, dialog_showing=False, root_attached=False))
    observations.append(dict(kind='colour-2x-reopened', root_id=201, dialog_id=202, value='#FF0000'))
    back('close 2x reopened colour', state(closes=1, reopened=True), state(showing=False, closes=2, reopened=True))
    caption('use', root=301)
    pointer('2x invalid rejected')
    observations.append(dict(kind='colour-2x-invalid-rejected', root_id=301, dialog_id=302, value='#broken',
                             dialog_showing=True, error_present=True, commit_callbacks=0, closed_callbacks=2))
    pointer('2x valid committed')
    observations.append(dict(kind='colour-2x-complete', commit_callbacks=1, closed_callbacks=3,
                             initial_native_field_activation='not-tested', initial_full_hex_visibility='not-accepted',
                             selected_colour=-14391124, dialog_showing=False, root_attached=False,
                             simultaneous_ime_field_footer_fit='not-accepted'))
    return observations


def synthetic_colour_receipt(method, digest):
    """Deliberately invented dimensions/times for validating accepted/rejected schemas."""
    retained = method.startswith('retained')
    normal = method.startswith('normal')
    lifecycle = method in LARGE_COLOUR_IME_METHODS
    large = method in LARGE_COLOUR_METHODS or lifecycle
    scale = 2 if large else 1
    locale = LARGE_COLOUR_IME_METHODS[method] if lifecycle else LARGE_COLOUR_METHODS[method] if large else ('hu' if method.startswith('hungarian') else 'en-US')
    observations = [dict(kind='fixture', locale=locale, font_scale=scale)]
    orientations = [False, True] if normal or large else [False, True, False, True] if retained else [False, True, False]
    for landscape in orientations:
        bounds = (0, 0, 640, 320) if landscape else (0, 0, 320, 640)
        observations.append(dict(kind='orientation', landscape=landscape, font_scale=scale,
                                 root=geometry(bounds=bounds)))
    ready = dict(locale=locale, font_scale=scale, startup_ready=True, window_focus=True,
                 root_attached=True, busy=False, activity_destroyed=False, activity_finishing=False,
                 io_error_present=False, autosave_error_present=False, startup_view_present=False,
                 canvas=geometry('paint_canvas'))
    for stage in ('before-wait', 'passed'):
        observations.append(dict(kind='initial-editor-state', stage=stage, **copy.deepcopy(ready)))

    def caption(tag):
        observations.extend([
            dict(kind='intrinsic-caption', tag=tag, lines=1, layout_height=20,
                 available_text_height=30, caption_length=5, layout_width=100,
                 line_metrics=[dict(end=5, ellipsis=0, left=0, right=99)], geometry=geometry(tag)),
            dict(kind='caption-line-reached', tag=tag, line=0, geometry=geometry(tag), line_rect=[11, 21, 100, 40])])

    for tag in ([] if lifecycle else LARGE_COLOUR_CAPTIONS if large else ['cancel'] if normal else COLOUR_CAPTIONS * (3 if retained else 2)):
        caption(tag)

    def pointer(label):
        observations.extend([dict(kind='pointer-before', label=label, tap=[50, 40], geometry=geometry()),
                             dict(kind='pointer-injected', label=label)])

    if lifecycle:
        observations.extend(synthetic_colour_ime_observations(method))
    elif large:
        observations.extend([
            dict(kind='colour-large-rail-reached', display=geometry(bounds=(0, 0, 640, 320)),
                 density=1, font_scale=2, text_size=24, expected_text_size=24, overflow=True,
                 content_height=190, viewport_height=140, controls=geometry('colour_controls_scroll', (330, 40, 620, 180), scroll_y=50),
                 editor=geometry('colour_editor_scroll', (20, 40, 310, 180)), editor_before=0,
                 add=geometry('add_custom_colour', (430, 90, 620, 170)),
                 selected=geometry('selected_colour_caption', (330, 70, 430, 100)), sample=geometry('new_colour_preview', (330, 156, 394, 180))),
            dict(kind='colour-large-rail-top-reached', heading=geometry('custom_colour_selection', (330, 40, 620, 72)),
                 slot=geometry('custom_colour_0', (330, 72, 374, 116)),
                 controls=geometry('colour_controls_scroll', (330, 40, 620, 180)))])
        observations[-1:-1] = synthetic_colour_endpoint(observations[-2])
        pointer(COLOUR_POINTERS[method][0])
        observations.append(dict(kind='colour-large-cancelled', commit_callbacks=0, closed_callbacks=1,
                                 dialog_attached=False, dialog_showing=False))
    elif normal:
        inner = geometry('colour_editor_scroll', (20, 90, 384, 176))
        fixed = [geometry(tag, (400, 60+i*50, 600, 100+i*50))
                 for i, tag in enumerate(('colour_advanced_tab', 'custom_colours_panel', 'add_custom_colour'))]
        observations.extend([
            dict(kind='colour-pre-assert-allocation', device_sdk=35, font_scale=1,
                 display=geometry(bounds=(0, 0, 640, 320)), dialog=geometry(bounds=(0, 0, 640, 300)),
                 holder=geometry(bounds=(10, 40, 630, 250)), holder_parent=geometry(bounds=(0, 0, 640, 300)),
                 inner=copy.deepcopy(inner), inner_content=geometry(bounds=(20, 90, 384, 560), visible=[20, 90, 384, 176]),
                 visible_display_frame=[0, 0, 640, 320], fixed=copy.deepcopy(fixed)),
            dict(kind='colour-native-scroll-route', viewport=inner['visible'], gutter_pixels=32, x=370, rtl=False),
            dict(kind='colour-finite-bounds', scale=1, inner={**inner, 'scroll_y':44}, fixed=copy.deepcopy(fixed))])
        pointer(COLOUR_POINTERS[method][0])
    elif not retained:
        for landscape in (True, False):
            observations.append(dict(kind='hungarian-colour-captions-fit', landscape=landscape,
                                     inner=geometry('colour_editor_scroll'), add=geometry('add_custom_colour')))
        pointer(COLOUR_POINTERS[method][0])
    else:
        labels = COLOUR_POINTERS[method]
        observations.append(dict(kind='colour-surface-native-drag', before_colour=-15509605,
                                 after_colour=-1234567, scroll_before=0, scroll_after=0))
        pointer(labels[0])

        def ime(showing):
            windows = [dict(type=2, package='synthetic.ime', configured_ime=True, root_visible=True,
                            root_children=1, bounds=[0, 100, 640, 320], root_bounds=[0, 100, 640, 320])] if showing else []
            observations.append(dict(kind='colour-native-ime-window', requested_visible=showing,
                                     condition_passed=True, ime_visible=showing, stable_window_ms=250,
                                     ime_inset_bottom=0, fullscreen_ime=True, value='#13579B',
                                     dialog=geometry(), field=geometry('colour_hex'), windows=windows))

        def state(showing=True, ime_visible=False, closes=0):
            return dict(target_attached=showing, target_showing=showing, target_focused=showing,
                        target_insets_available=showing, target_ime_visible=ime_visible if showing else None,
                        focused_insets_available=True, focused_app_window_present=True,
                        focused_app_window_is_target=showing, focused_app_window_is_editor=not showing,
                        focused_app_window_ime_visible=ime_visible, dialog_showing=showing,
                        commit_callbacks=0, closed_callbacks=closes, value='#13579B', ime_inset_bottom=0,
                        selected_colour=-65536, preview_colour=-65536)

        def back(label, before, after):
            observations.extend([
                dict(kind='native-back-before', label=label, state=before, postcondition_met=False),
                dict(kind='native-back-injected', label=label, state=copy.deepcopy(after),
                     route='UiDevice.pressKeyCode(KEYCODE_BACK)', keycode=4, injection_count=1, injected=True),
                dict(kind='native-back-after', label=label, state=after,
                     injected=True, completed=True, postcondition_met=True)])

        ime(True)
        back('hide colour IME', state(ime_visible=True), state())
        ime(False)
        pointer(labels[1])
        back('close reopened colour picker', state(closes=1), state(False, closes=2))
        pointer(labels[2]); pointer(labels[3])
        observations.append(dict(kind='colour-retained-state-complete', commit_callbacks=1,
                                 closed_callbacks=3, selected='#2468AC'))
    return dict(schema=1, test_class=COLOUR_CLASS, test_method=method, device_sdk=35,
                package=OWNER, outcome='passed', source_tests_sha256=digest,
                source_binding='runner-supplied-needs-host-comparison',
                screenshots=COLOUR_SCREENS[method], observations=observations,
                fixture_started_uptime_ms=1000, fixture_ended_uptime_ms=6000, fixture_elapsed_ms=5000,
                fixture_elapsed_scope='setup+interaction+teardown; excludes export')
