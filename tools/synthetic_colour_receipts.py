"""Small authored transport models. Never recorded Android evidence or acceptance."""
import copy

from dialog_evidence_transport import (COLOUR_CAPTIONS, COLOUR_CLASS, COLOUR_POINTERS,
                                       COLOUR_SCREENS, LARGE_COLOUR_METHODS, LARGE_COLOUR_CAPTIONS, OWNER)


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


def synthetic_colour_receipt(method, digest):
    """Deliberately invented dimensions/times for validating accepted/rejected schemas."""
    retained = method.startswith('retained')
    normal = method.startswith('normal')
    large = method in LARGE_COLOUR_METHODS
    scale = 2 if large else 1
    locale = LARGE_COLOUR_METHODS[method] if large else ('hu' if method.startswith('hungarian') else 'en-US')
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

    for tag in (LARGE_COLOUR_CAPTIONS if large else ['cancel'] if normal else COLOUR_CAPTIONS * (3 if retained else 2)):
        caption(tag)

    def pointer(label):
        observations.extend([dict(kind='pointer-before', label=label, tap=[50, 40], geometry=geometry()),
                             dict(kind='pointer-injected', label=label)])

    if large:
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
