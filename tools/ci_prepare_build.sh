#!/usr/bin/env bash
# Prepare dependencies and sources; the build workflow separately manages ccache.
# Never restore compiled app classes, APKs or CMake build directories.
set -euo pipefail
# Observation only: this never installs tools or claims fresh-environment equivalence.
if [[ "${1:-}" == --record-inputs ]]; then
  python3 - "${2:?output path required}" <<'PYINPUTS'
import hashlib, json, os, pathlib, subprocess, sys, xml.etree.ElementTree as ET

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()

def command(*args):
    return subprocess.check_output(args, stderr=subprocess.STDOUT, text=True, timeout=15).strip()

sdk = pathlib.Path(os.environ['ANDROID_HOME'])
packages = {}
for p in sorted(sdk.glob('**/package.xml')):
    revision = next((e for e in ET.parse(p).iter() if e.tag.rsplit('}', 1)[-1] == 'revision'), None)
    packages[str(p.relative_to(sdk))] = dict(sha256=digest(p),
        revision={part.tag.rsplit('}', 1)[-1]: part.text for part in revision} if revision is not None else {})
rows = []
inventory = pathlib.Path('app/build/runtime-dependencies.json')
if inventory.exists():
    cache = pathlib.Path.home()/'.gradle/caches/modules-2/files-2.1'
    for dependency in json.loads(inventory.read_text()):
        relative = pathlib.Path(dependency['group'])/dependency['name']/dependency['version']
        files = sorted(p for p in (cache/relative).glob('*/*') if p.is_file())
        rows.append(dict(**dependency, files={str(p.relative_to(cache)): digest(p) for p in files}))
native = {str(p): p.read_text() for p in pathlib.Path('Paintroid/build').glob('*-source/**/.anpaint-revision') if p.stat().st_size <= 4096}
record = dict(native_revision_inputs=native, commit=command('git', 'rev-parse', 'HEAD'),
    tree=command('git', 'rev-parse', 'HEAD^{tree}'),
    run_id=os.environ['GITHUB_RUN_ID'], attempt=os.environ['GITHUB_RUN_ATTEMPT'],
    job=os.environ['GITHUB_JOB'], image_os=os.environ.get('ImageOS'),
    image_version=os.environ.get('ImageVersion'), java=command('java', '-version'),
    sdk_packages=packages, runtime_dependencies=rows,
    gradle_wrapper_properties_sha256=digest(pathlib.Path('gradle/wrapper/gradle-wrapper.properties')))
out = pathlib.Path(sys.argv[1]); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(record, sort_keys=True, indent=2)+'\n')
PYINPUTS
  exit 0
fi
export JAVA_HOME="$JAVA_HOME_17_X64"
export PATH="$JAVA_HOME/bin:$PATH"
echo "JAVA_HOME=$JAVA_HOME" >> "$GITHUB_ENV"
echo "$JAVA_HOME/bin" >> "$GITHUB_PATH"
timeout --kill-after=15s 5m "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" \
  'platforms;android-35' 'build-tools;35.0.0' 'ndk;27.2.12479018' 'cmake;3.22.1'
chmod +x gradlew
./gradlew --no-daemon --max-workers=2 --console=plain :app:writeDependencyInventory
python3 tools/generate_native_runtime_notices.py --ndk "$ANDROID_HOME/ndk/27.2.12479018"
python3 tools/generate_tiff_notices.py
python3 tools/generate_legal_notices.py
# The source ZIP contains the working tree. Generated legal assets must already
# match the recorded commit so release source verification can compare every blob.
git diff --exit-code -- Paintroid/src/main/assets/legal
mkdir -p verification-tools/lib64
cp "$ANDROID_HOME/build-tools/35.0.0/lib/apksigner.jar" verification-tools/
cp "$ANDROID_HOME/build-tools/35.0.0/zipalign" verification-tools/
cp "$ANDROID_HOME/build-tools/35.0.0/aapt2" verification-tools/
cp "$ANDROID_HOME/build-tools/35.0.0/lib64/libc++.so" verification-tools/lib64/
