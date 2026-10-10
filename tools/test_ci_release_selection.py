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
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/android.yml').read_text()
VARIANT = re.search(r'^  BUILD_VARIANT: (.+)$', WORKFLOW, re.M).group(1)
MATRIX = re.search(r'^        api: (.+)$', WORKFLOW, re.M).group(1)
DEVICE_GATES = re.findall(r'^\s+if: (\$\{\{ inputs\.device_tests .+)$', WORKFLOW, re.M)


def evaluate(expression, *, event='pull_request', labels=(), build_type=None,
             device_tests=None, message=''):
    replacements = {
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
        'contains': lambda values, item: item.casefold() in [v.casefold() for v in values],
        'startsWith': lambda value, prefix: value.casefold().startswith(prefix.casefold()),
    }
    values = dict(event=event, labels=labels, build_type=build_type,
                  device_tests=device_tests, message=message, **functions)
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
        self.assertEqual(evaluate(MATRIX, **context), expected_matrix)
        self.assertEqual(len(DEVICE_GATES), 3)  # compile, upload, execute
        for gate in DEVICE_GATES:
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
