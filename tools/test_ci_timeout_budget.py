"""Source-bound cancellation arithmetic; it is not a universal liveness proof."""
import ast
import math
from pathlib import Path
import re
import shlex
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/android.yml').read_text()
SHELL = (ROOT / 'tools/ci_emulator.sh').read_text()
RUNNER = (ROOT / 'tools/run_android_instrumentation.py').read_text()
PHASES = {'Paintroid': 180, 'app': 180, 'app-gallery-draft': 90,
          'app-vertical-english-manchu': 180, 'app-vertical-literary-chinese-emoji': 180,
          'app-credit-restart-seed': 60, 'app-credit-restart-verify': 60}


def one(pattern, text):
    matches = re.findall(pattern, text, re.M)
    if len(matches) != 1:
        raise ValueError(f'Expected one source match for {pattern!r}: {matches!r}')
    return matches[0]


def body(shell, name):
    return shell.split(f'{name}() {{', 1)[1].split('\n}\n', 1)[0]


def shell_timeout(text, command):
    grace, deadline = one(r'timeout --kill-after=(\d+)s (\d+)s [^\n]*' + command, text)
    return int(deadline), int(grace)


def job(workflow, name):
    return one(r'^  ' + name + r':\n([\s\S]*?)(?=^  [a-z][\w-]*:|\Z)', workflow)


def step_minutes(block, name):
    step = one(r'^      - name: ' + re.escape(name) + r'\n([\s\S]*?)(?=^      - |\Z)', block)
    return int(one(r'^        timeout-minutes: (\d+)$', step))


def controlled_model(shell, runner):
    """Read configured constants; ordinary local I/O is explicitly outside this sum."""
    joined = shell.replace('\\\n', ' ')
    invocations = re.findall(r'^\s*(?:if ! )?python3 tools/run_android_instrumentation.py ([^\n]+)', joined, re.M)
    phases = {}
    for line in invocations:
        args = shlex.split(line)
        suite = args[args.index('--suite') + 1]
        if suite in phases:
            raise ValueError(f'Duplicate invocation: {suite}')
        phases[suite] = int(args[args.index('--timeout-seconds') + 1])
    if phases != PHASES:
        raise ValueError(f'Inner phase deadlines or invocation inventory changed: {phases}')

    syntax = ast.parse(runner)
    preparation = {}
    for node in ast.walk(syntax):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in {'device_sdk', 'installed', 'instrumentation', 'live'} and isinstance(node.value, ast.Call):
                value = next(k.value for k in node.value.keywords if k.arg == 'timeout')
                preparation[name] = ast.literal_eval(value)
    if set(preparation) != {'device_sdk', 'installed', 'instrumentation', 'live'}:
        raise ValueError('Runner preparation inventory changed')
    calls = [node for node in ast.walk(syntax) if isinstance(node, ast.Call)]
    tail = [ast.literal_eval(k.value) for node in calls if ast.unparse(node.func) == 'process.communicate'
            for k in node.keywords if k.arg == 'timeout']
    exceptional_wait = [ast.literal_eval(k.value) for node in calls if ast.unparse(node.func) == 'process.wait'
                        for k in node.keywords if k.arg == 'timeout' and isinstance(k.value, ast.Constant)]
    recovery = [ast.literal_eval(k.value) for node in calls if ast.unparse(node.func) == 'subprocess.run'
                and "'force-stop'" in ast.unparse(node.args[0])
                for k in node.keywords if k.arg == 'timeout']
    if len(tail) != 1 or len(exceptional_wait) != 1 or len(recovery) != 1:
        raise ValueError('Capture tail/recovery structure changed')
    tail, exceptional_wait, recovery = tail[0], exceptional_wait[0], recovery[0]

    main = body(joined, 'main')
    startup = sum(shell_timeout(main, command)[0] for command in ('avdmanager', 'wait-for-device', 'install -r -t'))
    startup += int(one(r'readiness_deadline=\$\(\(SECONDS \+ (\d+)\)\)', main))
    restart = body(joined, 'run_credit_restart_regression')
    pid = int(one(r"credit_restart_command '[^']*' (\d+) shell", body(joined, 'credit_restart_pid')))
    pid_count = len(re.findall(r'^  credit_restart_pid \|\| return$', restart, re.M))
    boundary_commands = [int(n) for n in re.findall(r'credit_restart_command (?:\x27[^\x27]*\x27|"[^"]*") (\d+)', restart)]
    boundary = sum(boundary_commands) + pid_count * pid
    # Before seed: launcher and first outer PID. All later boundary checks stop on failure.
    before_seed = boundary_commands[0] + pid
    boundary_grace = int(one(r'timeout --kill-after=(\d+)s', body(joined, 'credit_restart_command')))
    reset = shell_timeout(body(joined, 'run_vertical_locale_matrix'), r"shell\s+'?rm -rf")[0]
    cleanup = body(joined, 'cleanup')
    collection = sum(sum(shell_timeout(cleanup, command)) for command in ('logcat -d', 'pull', 'emu kill'))
    collection += int(one(r'for attempt in \$\(seq 1 (\d+)\)', cleanup)) * int(one(r'^      sleep (\d+)$', cleanup))
    prep = preparation['device_sdk'] + preparation['installed'] + preparation['instrumentation']
    seed = prep + phases['app-credit-restart-seed'] + tail + preparation['live']
    verify = prep + phases['app-credit-restart-verify'] + tail
    success = startup + sum(phases.values()) + len(phases) * (prep + tail) + preparation['live'] + boundary + reset + collection
    # Timeout and exceptional-tail suffixes are alternatives, never accumulated together.
    extra_failure = max(tail + recovery, tail + exceptional_wait) - tail
    paths = {
        'api35_success': success,
        'api35_all_seven_with_four_recoveries': success + 4 * extra_failure,
        'api35_ordinary_or_gallery_failure': success - seed - verify - boundary + 5 * extra_failure,
        'api35_seed_failure': success - verify - (boundary - before_seed) + 4 * extra_failure,
        'api35_last_boundary_failure': success - verify + boundary_grace + 3 * extra_failure,
        'api30_five_with_five_recoveries': success - seed - verify - boundary + 5 * extra_failure,
    }
    return dict(startup=startup, instrumentation=sum(phases.values()), preparation=prep * len(phases),
                seed_pid=preparation['live'], boundary=boundary, reset=reset, tails=tail * len(phases),
                cleanup=collection, recovery=4 * extra_failure, paths=paths)


def validate_budget(workflow, shell=SHELL, runner=RUNNER):
    model = controlled_model(shell, runner)
    # Operational reserves, not inner deadlines or an assertion that I/O must finish.
    processing_seconds, job_overhead_minutes = 60, 4
    required_step = math.ceil((max(model['paths'].values()) + processing_seconds) / 60)
    device = job(workflow, 'device')
    step = step_minutes(device, 'Run prebuilt tests with deadlines and live logs')
    image = step_minutes(device, 'Install emulator image')
    outer = int(one(r'^    timeout-minutes: (\d+)$', device))
    if step < required_step or outer < step + image + job_overhead_minutes:
        raise ValueError('Outer cancellation budget does not admit the configured controlled path and allowances')
    return model, (step, image, outer), required_step


class TimeoutBudgetTest(unittest.TestCase):
    def test_actual_source_arithmetic_and_outer_hard_caps(self):
        model, limits, required = validate_budget(WORKFLOW)
        self.assertEqual({k: v for k, v in model.items() if k != 'paths'},
                         dict(startup=270, instrumentation=930, preparation=630, seed_pid=10,
                              boundary=90, reset=10, tails=35, cleanup=54, recovery=40))
        self.assertEqual(limits, (36, 6, 46))
        self.assertEqual(required, 36)

    def test_failure_gates_and_exclusive_tail_paths_are_not_double_counted(self):
        model = controlled_model(SHELL, RUNNER)
        self.assertEqual(model['paths'], {
            'api35_success': 2029, 'api35_all_seven_with_four_recoveries': 2069,
            'api35_ordinary_or_gallery_failure': 1669, 'api35_seed_failure': 1864,
            'api35_last_boundary_failure': 1905, 'api30_five_with_five_recoveries': 1669})
        main = body(SHELL, 'main')
        self.assertIn('if (( editor_failed )); then', main)
        self.assertIn('run_credit_restart_regression || failed=1', main)
        self.assertIn('"${seed_exclude[@]}" || return', SHELL)
        self.assertIn('returncode, timed_out = capture_live(command, log, args.timeout_seconds)', RUNNER)
        self.assertIn('if timed_out and target:', RUNNER)
        self.assertIn('process.wait(timeout=remaining)', RUNNER)

    def test_old_and_near_miss_execution_and_job_caps_fail_closed(self):
        for step in (15, 16, 34, 35):
            with self.subTest(step=step), self.assertRaises(ValueError):
                validate_budget(WORKFLOW.replace('timeout-minutes: 36', f'timeout-minutes: {step}'))
        for outer in (25, 36, 41, 45):
            with self.subTest(job=outer), self.assertRaises(ValueError):
                validate_budget(WORKFLOW.replace('timeout-minutes: 46', f'timeout-minutes: {outer}'))

    def test_phase_deadline_or_invocation_changes_cannot_bypass_model(self):
        for changed in (SHELL.replace('--timeout-seconds 90', '--timeout-seconds 91'),
                        SHELL.replace('--suite app --timeout-seconds 180', '--suite changed --timeout-seconds 180')):
            with self.assertRaises(ValueError):
                validate_budget(WORKFLOW, changed)

    def test_source_preparation_growth_requires_rebudgeting(self):
        changed = RUNNER.replace('capture_output=True, text=True, timeout=60)',
                                 'capture_output=True, text=True, timeout=120)')
        self.assertNotEqual(changed, RUNNER)
        with self.assertRaises(ValueError):
            validate_budget(WORKFLOW, runner=changed)
        changed = SHELL.replace('readiness_deadline=$((SECONDS + 120))',
                                'readiness_deadline=$((SECONDS + 300))')
        with self.assertRaises(ValueError):
            validate_budget(WORKFLOW, shell=changed)

    def test_checks_job_is_an_explicit_aggregate_policy_not_a_sum_bound(self):
        checks = job(WORKFLOW, 'checks')
        self.assertEqual(int(one(r'^    timeout-minutes: (\d+)$', checks)), 22)
        self.assertEqual(step_minutes(checks, 'Run Python contracts'), 4)
        self.assertEqual(sum(int(n) for n in re.findall(r'^        timeout-minutes: (\d+)$', checks, re.M)), 38)
        self.assertNotIn('continue-on-error', checks)


if __name__ == '__main__':
    unittest.main()
