#!/usr/bin/env python3
"""Execute pinned Gradle resource-generation probes in a disposable worktree.

This is an Android-toolchain check, not a source-contract substitute. Native
source bundling alone is excluded: the ordinary build separately verifies that
unrelated graph. Resource producers/consumers and their dependencies are intact.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

CANONICAL = Path('Paintroid/src/main/res/values-b+ko+Kore+KR')
GENERATED = Path('Paintroid/build/generated/exactScriptResources')
QUALIFIER = 'values-b+ko+Kore+KR+anpaint'
GENERATOR = ':Paintroid:generateExactScriptResources'
MERGES = (':Paintroid:mergeDebugResources', ':Paintroid:mergeReleaseResources')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def mirror_hashes(root):
    inputs = {p.name: p.read_bytes() for p in (root / CANONICAL).glob('*.xml')}
    if not inputs:
        raise AssertionError('Canonical XML inputs are missing')
    output = root / GENERATED
    actual = {p.relative_to(output).as_posix(): p.read_bytes()
              for p in output.rglob('*') if p.is_file()}
    expected = {f'{QUALIFIER}/{name}': data for name, data in inputs.items()}
    if actual != expected:
        raise AssertionError(f'Generated XML differs or contains stale files: '
                             f'expected={sorted(expected)}, actual={sorted(actual)}')
    return {name: sha(data) for name, data in sorted(expected.items())}


def task_outcomes(log):
    return re.findall(r'^> Task (:[^\s]+)([^\n]*)$', log, re.MULTILINE)


def require_generation_before(log, consumers, *, up_to_date=False):
    tasks = task_outcomes(log)
    names = [name for name, _ in tasks]
    if names.count(GENERATOR) != 1:
        raise AssertionError(f'Expected exactly one generator execution: {tasks}')
    position = names.index(GENERATOR)
    state = tasks[position][1].strip()
    expected = 'UP-TO-DATE' if up_to_date else ''
    if state != expected:
        raise AssertionError(f'Generator outcome {state!r}, expected {expected!r}')
    for consumer in consumers:
        if names.count(consumer) != 1 or names.index(consumer) <= position:
            raise AssertionError(f'Generator did not precede {consumer}: {tasks}')


def run_probes(repository, output):
    repository = repository.resolve()
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repository, text=True).strip()
    tree = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], cwd=repository, text=True).strip()
    report = {'commit': commit, 'tree': tree, 'success': False, 'probes': [],
              'excluded_task': ':Paintroid:bundleCorrespondingSource',
              'scope': 'Pinned Gradle resource graph; ordinary CI separately builds APK/source.'}
    summary = output / 'summary.json'
    summary.write_text(json.dumps(report, indent=2) + '\n')
    with tempfile.TemporaryDirectory(prefix='anpaint-resource-probe-') as temporary:
        worktree = Path(temporary) / 'source'
        subprocess.run(['git', 'worktree', 'add', '--detach', str(worktree), commit],
                       cwd=repository, check=True)
        try:
            wrapper = (worktree / 'gradle/wrapper/gradle-wrapper.properties').read_bytes()
            build = (worktree / 'build.gradle').read_bytes()
            if b'gradle-8.13-bin.zip' not in wrapper or b'version \'8.13.0\'' not in build:
                raise AssertionError('Update probe provenance when the pinned toolchain changes')
            report['wrapper_sha256'] = sha(wrapper)
            report['root_build_sha256'] = sha(build)
            original = {p.name: p.read_bytes() for p in (worktree / CANONICAL).glob('*.xml')}
            if not original:
                raise AssertionError('Missing canonical resource inputs')

            def gradle(label, tasks):
                command = ['bash', 'gradlew', '--no-daemon', '--max-workers=2', '--parallel',
                           '--console=plain', '-PnativeAbis=x86_64',
                           '-x', ':Paintroid:bundleCorrespondingSource', *tasks]
                log_path = output / f'{label}.log'
                with log_path.open('w') as log:
                    result = subprocess.run(command, cwd=worktree, stdout=log,
                                            stderr=subprocess.STDOUT, timeout=360)
                text = log_path.read_text()
                print(text, flush=True)
                record = {'name': label, 'command': command, 'exit_code': result.returncode,
                          'log_sha256': sha(log_path.read_bytes()), 'tasks': task_outcomes(text)}
                report['probes'].append(record)
                if result.returncode:
                    raise AssertionError(f'{label} failed; see {log_path.name}')
                return text, record

            gradle('01-clean', [':Paintroid:clean'])
            if (worktree / GENERATED).exists():
                raise AssertionError('Clean left generated resources behind')
            log, record = gradle('02-clean-debug-release', list(MERGES))
            require_generation_before(log, MERGES)
            record['generated_sha256'] = mirror_hashes(worktree)
            log, _ = gradle('03-unchanged', [GENERATOR])
            require_generation_before(log, (), up_to_date=True)

            canonical = worktree / CANONICAL / sorted(original)[0]
            canonical.write_bytes(original[canonical.name] + b'\n<!-- isolated incremental resource probe -->\n')
            stale = worktree / GENERATED / QUALIFIER / 'stale_probe.xml'
            stale.write_text('<resources/>\n')
            log, record = gradle('04-input-change-and-stale-output', [MERGES[0]])
            require_generation_before(log, [MERGES[0]])
            record['generated_sha256'] = mirror_hashes(worktree)
            if stale.exists():
                raise AssertionError('Sync did not remove stale output')
            canonical.write_bytes(original[canonical.name])
            log, record = gradle('05-restored-input-release', [MERGES[1]])
            require_generation_before(log, [MERGES[1]])
            record['generated_sha256'] = mirror_hashes(worktree)

            gradle('06-second-clean', [':Paintroid:clean'])
            log, record = gradle('07-release-first-after-clean', [MERGES[1]])
            require_generation_before(log, [MERGES[1]])
            record['generated_sha256'] = mirror_hashes(worktree)
            if {p.name: p.read_bytes() for p in (worktree / CANONICAL).glob('*.xml')} != original:
                raise AssertionError('Canonical input was not restored byte-for-byte')
            subprocess.run(['git', 'diff', '--exit-code'], cwd=worktree, check=True)
            report['success'] = True
        except Exception as error:
            report['success'] = False
            report['error'] = f'{type(error).__name__}: {error}'
            raise
        finally:
            try:
                subprocess.run(['git', 'worktree', 'remove', '--force', str(worktree)],
                               cwd=repository, check=True)
            except Exception as error:
                report['success'] = False
                report['cleanup_error'] = f'{type(error).__name__}: {error}'
                raise
            finally:
                summary.write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, default=Path('build/reports/exact-script-generation'))
    args = parser.parse_args()
    print(json.dumps(run_probes(args.repository, args.output), indent=2))


if __name__ == '__main__':
    main()
