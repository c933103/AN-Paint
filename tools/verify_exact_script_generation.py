#!/usr/bin/env python3
"""Execute pinned Gradle resource-generation probes in a disposable worktree.

This is an Android-toolchain check, not a source-contract substitute. Native
source bundling alone is excluded: the ordinary build separately verifies that
unrelated graph. Resource producers/consumers and their dependencies are intact.
"""
import argparse
import copy
import xml.etree.ElementTree as ET
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

GENERATED = Path('Paintroid/build/generated/exactScriptResources')
MIRRORS = {
    Path('Paintroid/src/main/res/values-b+ko+Kore+KR'): 'values-b+ko+Kore+KR+anpaint',
    Path('Paintroid/src/main/res/values-b+qaa+Zsye+XV'): 'values-b+en+Zsye+XV+anpaint',
}
GENERATOR = ':Paintroid:generateExactScriptResources'
SOURCE_GENERATOR = ':Paintroid:generateSourceTextResources'
SOURCE_GENERATED = Path('Paintroid/build/generated/sourceTextResources')
MERGES = (':Paintroid:mergeDebugResources', ':Paintroid:mergeReleaseResources')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def mirror_hashes(root):
    expected = {}
    for canonical, qualifier in MIRRORS.items():
        inputs = {p.name: p.read_bytes() for p in (root / canonical).glob('*.xml')}
        if not inputs:
            raise AssertionError(f'Canonical XML inputs are missing: {canonical}')
        expected.update({f'{qualifier}/{name}': data for name, data in inputs.items()})
    output = root / GENERATED
    actual = {p.relative_to(output).as_posix(): p.read_bytes()
              for p in output.rglob('*') if p.is_file()}
    if actual != expected:
        raise AssertionError(f'Generated XML differs or contains stale files: '
                             f'expected={sorted(expected)}, actual={sorted(actual)}')
    return {name: sha(data) for name, data in sorted(expected.items())}


def source_text_hashes(root):
    """Exact source text, non-translatable IDs, aliases and formatting metadata."""
    source = ET.parse(root / 'Paintroid/src/main/res/values/strings.xml').getroot()
    output = root / SOURCE_GENERATED
    files = sorted(p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file())
    if files != ['values/source_text.xml', 'values/source_text_contracts.xml']:
        raise AssertionError(f'Missing or stale generated source text: {files}')
    generated = ET.parse(output / files[0]).getroot()
    expected = copy.deepcopy(source)
    for entry in expected:
        entry.set('name', 'anpaint_source_' + entry.get('name'))
        entry.set('translatable', 'false')
        for node in entry.iter():
            if node.text and node.text.strip().startswith('@string/'):
                node.text = node.text.replace('@string/', '@string/anpaint_source_', 1)
    canonical = lambda node: ET.canonicalize(ET.tostring(node, encoding='unicode'))
    if canonical(expected) != canonical(generated):
        raise AssertionError('Generated fallback differs from complete source text')
    entries = {entry.tag + '/' + entry.get('name'): entry for entry in source}
    def formatted(entry, value):
        if entry.get('formatted') == 'false': return False
        text = ''.join(value.itertext()).strip()
        if text.startswith('@string/'):
            target = entries[text[1:]]
            return formatted(target, target)
        return True
    contracts = ET.Element('resources')
    for key, entry in entries.items():
        contract = ET.SubElement(contracts, entry.tag, {
            'name': 'anpaint_source_contract_' + key.replace('/', '_'),
            'translatable': 'false', 'formatted': 'false'})
        if entry.tag == 'string': contract.text = str(formatted(entry, entry)).lower()
        else:
            for value in entry:
                ET.SubElement(contract, 'item', {'quantity': value.get('quantity')}).text = str(formatted(entry, value)).lower()
    actual_contracts = ET.parse(output / files[1]).getroot()
    if canonical(contracts) != canonical(actual_contracts):
        raise AssertionError('Generated formatting metadata differs from the source contract')
    return {name: sha((output / name).read_bytes()) for name in files}


def task_outcomes(log):
    return re.findall(r'^> Task (:[^\s]+)([^\n]*)$', log, re.MULTILINE)


def require_generation_before(log, consumers, *, up_to_date=False, generator=GENERATOR):
    tasks = task_outcomes(log)
    names = [name for name, _ in tasks]
    if names.count(generator) != 1:
        raise AssertionError(f'Expected exactly one generator execution: {tasks}')
    position = names.index(generator)
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
            original = {canonical: {p.name: p.read_bytes()
                        for p in (worktree / canonical).glob('*.xml')} for canonical in MIRRORS}
            if not all(original.values()):
                raise AssertionError('Missing canonical resource inputs')

            def gradle(label, tasks, *, expect_success=True):
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
                          'log_sha256': sha(log_path.read_bytes()), 'tasks': task_outcomes(text),
                          'expected_success': expect_success}
                report['probes'].append(record)
                if (result.returncode == 0) != expect_success:
                    raise AssertionError(f'{label} had unexpected exit {result.returncode}; see {log_path.name}')
                return text, record

            gradle('01-clean', [':Paintroid:clean'])
            if (worktree / GENERATED).exists():
                raise AssertionError('Clean left generated resources behind')
            log, record = gradle('02-clean-debug-release', list(MERGES))
            require_generation_before(log, MERGES)
            record['generated_sha256'] = mirror_hashes(worktree)
            require_generation_before(log, MERGES, generator=SOURCE_GENERATOR)
            record['source_text_sha256'] = source_text_hashes(worktree)
            log, _ = gradle('03-unchanged', [GENERATOR, SOURCE_GENERATOR])
            require_generation_before(log, (), up_to_date=True)
            require_generation_before(log, (), up_to_date=True, generator=SOURCE_GENERATOR)

            for index, (source, qualifier) in enumerate(MIRRORS.items(), 1):
                canonical = worktree / source / sorted(original[source])[0]
                canonical.write_bytes(original[source][canonical.name] +
                                      b'\n<!-- isolated incremental resource probe -->\n')
                stale = worktree / GENERATED / qualifier / 'stale_probe.xml'
                stale.write_text('<resources/>\n')
                log, record = gradle(f'04-{index}-input-change-and-stale-output', [MERGES[0]])
                require_generation_before(log, [MERGES[0]])
                record['generated_sha256'] = mirror_hashes(worktree)
                if stale.exists():
                    raise AssertionError('Sync did not remove stale output')
                canonical.write_bytes(original[source][canonical.name])
                log, record = gradle(f'05-{index}-restored-input-release', [MERGES[1]])
                require_generation_before(log, [MERGES[1]])
                record['generated_sha256'] = mirror_hashes(worktree)

            source = worktree / 'Paintroid/src/main/res/values/strings.xml'
            original_source = source.read_bytes()
            source.write_bytes(original_source + b'\n<!-- isolated source fallback regeneration probe -->\n')
            stale = worktree / SOURCE_GENERATED / 'stale_probe.xml'
            stale.write_text('<resources/>\n')
            log, record = gradle('05-source-change-and-stale-output', [MERGES[0]])
            require_generation_before(log, [MERGES[0]], generator=SOURCE_GENERATOR)
            record['source_text_sha256'] = source_text_hashes(worktree)
            source.write_bytes(original_source)
            overlay = worktree / 'app/src/debug/res/values-en-rUS/source_namespace_probe.xml'
            overlay.parent.mkdir(parents=True, exist_ok=True)
            try:
                overlay.write_text('<resources><string name="anpaint_source_ui_help23">forbidden override</string></resources>')
                log, record = gradle('06-reserved-app-variant-rejected', [MERGES[0]], expect_success=False)
                if 'Reserved source-text name' not in log or 'source_namespace_probe.xml' not in log:
                    raise AssertionError('Expected source-set namespace rejection was not observed')
                if not any(name == SOURCE_GENERATOR and state.strip() == 'FAILED' for name, state in task_outcomes(log)):
                    raise AssertionError('The source generator did not reject the app variant overlay')
            finally:
                overlay.unlink(missing_ok=True)
            gradle('06-second-clean', [':Paintroid:clean'])
            log, record = gradle('07-release-first-after-clean', [MERGES[1]])
            require_generation_before(log, [MERGES[1]])
            record['generated_sha256'] = mirror_hashes(worktree)
            require_generation_before(log, [MERGES[1]], generator=SOURCE_GENERATOR)
            record['source_text_sha256'] = source_text_hashes(worktree)
            if {canonical: {p.name: p.read_bytes() for p in (worktree / canonical).glob('*.xml')}
                    for canonical in MIRRORS} != original:
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
