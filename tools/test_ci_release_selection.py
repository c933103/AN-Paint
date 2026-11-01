"""Evaluate the workflow's bounded selection expressions, not a duplicate policy.

This adapter covers only the operators/functions used by these expressions; it
is not a general GitHub Actions interpreter or a substitute for an actual run.
Missing event inputs are null. The tested strings are nonempty, so Python's
short-circuit operand selection matches the relevant Actions truthiness rules.
"""
import ast
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/android.yml').read_text()
VARIANT = re.search(r'^  BUILD_VARIANT: (.+)$', WORKFLOW, re.M).group(1)


def one(pattern, text):
    matches = re.findall(pattern, text, re.M)
    if len(matches) != 1:
        raise AssertionError(f'Expected one named selection source for {pattern!r}: {matches!r}')
    return matches[0]


def job(name):
    return one(r'^  ' + re.escape(name) + r':\n([\s\S]*?)(?=^  [a-z][\w-]*:|\Z)', WORKFLOW)


def step(block, marker):
    matches = [part for part in re.split(r'(?=^      - )', block, flags=re.M) if marker in part]
    if len(matches) != 1:
        raise AssertionError(f'Expected one named step for {marker!r}')
    return matches[0]


DEVICE_JOBS = {name: job(name) for name in ('device', 'position', 'device-union')}
MATRICES = {name: one(r'^        api: (.+)$', block) for name, block in DEVICE_JOBS.items()}
BUILD = job('build')
DEVICE_GATES = {
    'compile': one(r'^        if: (.+)$', step(BUILD, '- name: Compile test APKs once for all emulator jobs')),
    'upload': one(r'^        if: (.+)$', step(BUILD, 'name: instrumentation-apks-${{ github.sha }}')),
    **{name: one(r'^    if: (.+)$', block) for name, block in DEVICE_JOBS.items()},
}


def evaluate(expression, *, event='pull_request', labels=(), build_type=None,
             device_tests=None, message='', reused=None):
    replacements = {
        'needs.prior-evidence.outputs.reused': 'reused',
        'github.event.pull_request.labels.*.name': 'labels',
        'github.event.head_commit.message': 'message',
        'github.event_name': 'event',
        'inputs.build_type': 'build_type',
        'inputs.device_tests': 'device_tests',
    }
    source = expression.removeprefix('${{').removesuffix('}}').strip()
    for original, replacement in replacements.items():
        source = source.replace(original, replacement)
    source = source.replace('&&', ' and ').replace('||', ' or ')
    parsed = ast.parse(source, mode='eval')
    allowed = (ast.Expression, ast.BoolOp, ast.And, ast.Or, ast.Compare, ast.Eq,
               ast.NotEq, ast.Call, ast.Name, ast.Load, ast.Constant)
    functions = {
        'fromJSON': json.loads,
        'always': lambda: True,
        'contains': lambda values, item: item.casefold() in [v.casefold() for v in values],
        'startsWith': lambda value, prefix: value.casefold().startswith(prefix.casefold()),
    }
    values = dict(event=event, labels=labels, build_type=build_type,
                  device_tests=device_tests, message=message, reused=reused, **functions)
    for node in ast.walk(parsed):
        if not isinstance(node, allowed):
            raise AssertionError(f'Unmodelled expression syntax: {type(node).__name__}')
        if isinstance(node, ast.Name) and node.id not in values:
            raise AssertionError(f'Unmodelled expression name: {node.id}')
        if isinstance(node, ast.Call) and (not isinstance(node.func, ast.Name)
                                        or node.func.id not in functions):
            raise AssertionError('Unmodelled expression function')
    return eval(compile(parsed, '<workflow-selection>', 'eval'), {'__builtins__': {}}, values)


class ReleaseSelectionContracts(unittest.TestCase):
    def assert_selection(self, expected_variant, expected_matrix, expected_devices=True, **context):
        self.assertEqual(evaluate(VARIANT, **context), expected_variant)
        self.assertEqual(set(MATRICES), {'device', 'position', 'device-union'})
        self.assertEqual(set(DEVICE_GATES), {'compile', 'upload', 'device', 'position', 'device-union'})
        for name, matrix in MATRICES.items():
            with self.subTest(matrix=name):
                self.assertEqual(evaluate(matrix, **context), expected_matrix)
        for name, gate in DEVICE_GATES.items():
            with self.subTest(gate=name):
                self.assertEqual(evaluate(gate, **context), expected_devices)

    def test_unlabeled_and_full_only_prs_remain_debug(self):
        self.assert_selection('debug', [35])
        self.assert_selection('debug', [35], labels=['unrelated'])
        self.assert_selection('debug', [30, 35], labels=['ci:full-android'])

    def test_release_pr_label_alone_selects_release_and_both_devices(self):
        self.assert_selection('release', [30, 35], labels=['ci:release-android'])
        self.assert_selection('release', [30, 35],
                              labels=['ci:full-android', 'ci:release-android'])

    def test_existing_develop_push_selection_is_preserved(self):
        self.assert_selection('debug', [35], event='push', message='Fix a regression')
        self.assert_selection('release', [30, 35], event='push', message='Release 0.0.38')
        self.assert_selection('debug', [35], event='push', message='Prepare Release 0.0.38')

    def test_explicit_dispatch_variant_and_coverage_are_preserved(self):
        for build_type in ('debug', 'release'):
            for device_tests in ('current', 'full', 'none'):
                with self.subTest(build_type=build_type, device_tests=device_tests):
                    full = build_type == 'release' or device_tests == 'full'
                    devices = build_type == 'release' or device_tests != 'none'
                    self.assert_selection(build_type, [30, 35] if full else [35], devices,
                                          event='workflow_dispatch', build_type=build_type,
                                          device_tests=device_tests)

    def test_release_label_is_scoped_to_pr_events(self):
        # Even a synthetic non-PR payload carrying labels must not select release.
        self.assert_selection('debug', [35], event='push', labels=['ci:release-android'])
        self.assert_selection('debug', [35], event='workflow_dispatch',
                              labels=['ci:release-android'], build_type='debug')

    def test_union_runs_after_dependency_failures_but_requires_both_successes(self):
        union = DEVICE_JOBS['device-union']
        self.assertEqual(one(r'^    needs: (.+)$', union), '[prior-evidence, device, position]')
        self.assertIn('always()', DEVICE_GATES['device-union'])
        guard = step(union, '- name: Require both complete emulator jobs')
        self.assertIn('CORE_RESULT: ${{ needs.device.result }}', guard)
        self.assertIn('POSITION_RESULT: ${{ needs.position.result }}', guard)
        command = one(r'^        run: (.+)$', guard)
        for core in ('success', 'failure', 'cancelled', 'skipped'):
            for position in ('success', 'failure', 'cancelled', 'skipped'):
                with self.subTest(core=core, position=position):
                    result = subprocess.run(['bash', '-c', command], capture_output=True, text=True,
                                            env={'CORE_RESULT': core, 'POSITION_RESULT': position}, timeout=5)
                    self.assertEqual(result.returncode == 0, core == position == 'success')

    def test_only_verified_equivalence_suppresses_full_roots_and_union(self):
        gates = [one(r'^    if: (.+)$', job(name))
                 for name in ('checks', 'exact-script-resources', 'build', 'device-union')]
        for value in (None, '', 'false', 'failure'):
            for gate in gates: self.assertTrue(evaluate(gate, event='push', reused=value))
        for gate in gates: self.assertFalse(evaluate(gate, event='push', reused='true'))
        preflight = job('prior-evidence')
        self.assertIn('permissions:\n      contents: read\n      actions: read', preflight)
        self.assertIn('--equivalence-preflight', preflight)
        self.assertNotIn('continue-on-error', preflight)
        observation = step(job('checks'), '- name: Record observed prior-run environment')
        command = observation.split('        run: |\n', 1)[1]
        command = '\n'.join(line.removeprefix('          ') for line in command.splitlines())
        self.assertIn('timeout --kill-after=5s 45s', command)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root/'tools').mkdir()
            (root/'tools/ci_prepare_build.sh').write_text('mkdir -p "$(dirname "$2")"; echo stale > "$2"; exit 7\n')
            result = subprocess.run(['bash','-e','-c',command],cwd=root,capture_output=True,text=True,timeout=5)
            self.assertEqual(result.returncode, 0)
            self.assertFalse((root/'build/reports/ci-phases/observed-inputs.json').exists())

    def test_label_alone_cannot_trigger_or_publish_or_expand_permissions(self):
        triggers = WORKFLOW.split('\nenv:\n', 1)[0]
        self.assertNotIn('labeled', triggers)
        self.assertNotIn('unlabeled', triggers)
        self.assertNotIn('pull_request_target', WORKFLOW)
        self.assertIn('permissions:\n  contents: read\n', WORKFLOW)
        self.assertNotIn('contents: write', WORKFLOW)
        self.assertNotIn('secrets.', WORKFLOW)
        publisher = (ROOT / '.github/workflows/publish-release.yml').read_text()
        self.assertIn("    branches: [develop]\n    paths: ['verification/releases/request.json']", publisher)
        self.assertIn('  workflow_dispatch:\n', publisher)
        self.assertNotIn('pull_request', publisher)
        self.assertNotIn('ci:release-android', publisher)
        self.assertIn('python3 tools/publish_github_release.py verification/releases/request.json', publisher)

    def test_release_build_and_instrumentation_keep_existing_ci_signing_path(self):
        self.assertEqual(WORKFLOW.count('-PciReleaseSigning'), 2)
        self.assertIn(':app:assemble${BUILD_VARIANT^} -PciReleaseSigning', WORKFLOW)
        self.assertIn(':Paintroid:assemble${BUILD_VARIANT^}AndroidTest '
                      ':app:assemble${BUILD_VARIANT^}AndroidTest -PciReleaseSigning', WORKFLOW)
        self.assertIn("'build_variant': variant", WORKFLOW)
        self.assertIn('CI debug key. Upgrade signing remains a separate private packaging step.', WORKFLOW)
        for module in ('app', 'Paintroid'):
            gradle = (ROOT / module / 'build.gradle').read_text()
            self.assertIn('if (project.hasProperty("ciReleaseSigning")) signingConfig = signingConfigs.debug', gradle)
            self.assertIn('System.getenv("BUILD_VARIANT") ?: "debug"', gradle)


if __name__ == '__main__':
    unittest.main()
