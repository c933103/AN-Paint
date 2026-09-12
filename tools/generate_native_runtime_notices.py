"""Preserve the licences supplied with the exact NDK used for this APK.

AN Paint, 2026-09-12. AGPL-3.0-or-later.

Run after installing NDK 27.2.12479018 and before generate_legal_notices.py:
  python3 tools/generate_native_runtime_notices.py --ndk "$ANDROID_HOME/ndk/27.2.12479018"

Authoritative package layout: NDK's Clang.install copies the LLVM prebuilt,
including its NOTICE, to toolchains/llvm/prebuilt/<host>. Clang.notices uses
that same NOTICE when creating the package's aggregate NOTICE.toolchain:
https://android.googlesource.com/platform/ndk/+/master/ndk/checkbuild.py

No licences are fetched from a newer LLVM release. The input is the installed
SDK package's actual NOTICE, with its hash and pinned revision recorded.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
NDK_REVISION = '27.2.12479018'


def generate(ndk: Path, destination: Path, report: Path) -> None:
    properties = (ndk / 'source.properties').read_text(encoding='utf-8')
    match = re.search(r'^Pkg\.Revision\s*=\s*(\S+)\s*$', properties, re.MULTILINE)
    if match is None or match.group(1) != NDK_REVISION:
        raise ValueError(f'Expected the pinned Android NDK {NDK_REVISION}; found {match.group(1) if match else "no revision"}')

    # An SDK NDK package contains one host's LLVM prebuilt. Its own NOTICE is
    # narrower than the root NOTICE.toolchain, which also covers host utilities.
    candidates = sorted((ndk / 'toolchains/llvm/prebuilt').glob('*/NOTICE'))
    if len(candidates) != 1:
        raise ValueError(f'Expected one installed LLVM NOTICE, found {len(candidates)}')
    notice_path = candidates[0]
    notice_bytes = notice_path.read_bytes()
    notice = notice_bytes.decode('utf-8')
    # LLVM's runtime licence is Apache-2.0 WITH LLVM-exception. Do not silently
    # substitute plain Apache-2.0 or an unrelated tool's notice if paths change.
    if len(notice_bytes) < 10000 or 'apache license' not in notice.lower() or 'llvm exceptions' not in notice.lower():
        raise ValueError('Installed LLVM NOTICE does not contain the complete expected licence and LLVM exceptions')
    relative = notice_path.relative_to(ndk).as_posix()
    digest = hashlib.sha256(notice_bytes).hexdigest()
    compiler_version = notice_path.parent / 'AndroidVersion.txt'
    compiler_details = compiler_version.read_text(encoding='utf-8').strip() if compiler_version.is_file() else None
    introduction = f'''NATIVE RUNTIME NOTICES — AN Paint

LLVM libc++, libc++abi, libunwind and compiler-rt runtime support
Android NDK {NDK_REVISION}

AN Paint's native image codecs use the LLVM C++ standard library (libc++),
C++ ABI support (libc++abi), exception unwinding (libunwind), and compiler-rt
built-ins supplied by this NDK. Static runtime code is included within the
native libraries; it need not appear as a separate libc++.so file in the APK.

These components are part of the LLVM Project, under the Apache License 2.0
with LLVM Exceptions and the additional notices retained in the supplied
distribution. All copyright notices, complete terms and exceptions in the
NDK's LLVM NOTICE are reproduced verbatim below. This upstream aggregate
also preserves terms for LLVM distribution components beyond these runtimes;
its contents are a licence document, not AN Paint's dependency inventory.

Licence source: installed Android NDK {NDK_REVISION}, {relative}
Source SHA-256: {digest}
Upstream project: https://llvm.org/
Android NDK: https://developer.android.com/ndk
Reproduction: tools/generate_native_runtime_notices.py with this pinned NDK.

--- BEGIN INSTALLED LLVM NOTICE (VERBATIM) ---

'''
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Use bytes to retain the supplied notice exactly, including line endings.
    destination.write_bytes(introduction.encode('utf-8') + notice_bytes +
                            b'\n--- END INSTALLED LLVM NOTICE ---\n')
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({
        'ndk_revision': NDK_REVISION,
        'runtime_components': ['LLVM libc++', 'LLVM libc++abi', 'LLVM libunwind', 'LLVM compiler-rt built-ins'],
        'notice_path': relative,
        'notice_sha256': digest,
        'notice_bytes': len(notice_bytes),
        'android_compiler_version': compiler_details,
        'generated_asset_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
    }, indent=2) + '\n', encoding='utf-8')
    print(f'Preserved Android NDK {NDK_REVISION} LLVM runtime notices: {len(notice_bytes)} bytes, SHA-256 {digest}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ndk', type=Path, required=True, help='Installed Android NDK 27.2.12479018 directory')
    parser.add_argument('--output', type=Path, default=ROOT / 'Paintroid/src/main/assets/legal/NATIVE_RUNTIME_NOTICES.txt')
    parser.add_argument('--report', type=Path, default=ROOT / 'build/reports/native-runtime-notices.json')
    arguments = parser.parse_args()
    generate(arguments.ndk, arguments.output, arguments.report)
