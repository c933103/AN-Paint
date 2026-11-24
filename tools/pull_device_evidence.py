#!/usr/bin/env python3
"""Collect immutable CI exports with at most one same-session recovery.

The caller retains its 15s timeout/3s kill envelope. This helper shares one
monotonic 15s deadline across every command; it never runs tests or validators.
Failed attempts remain separate raw evidence, never inputs to a later attempt.
"""
import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tarfile
import shutil
import sys
import tempfile
import time

BUDGET_SECONDS = 15
DIALOG_EXPORT = '/sdcard/Download/anpaint-ci-dialog-evidence'
VERTICAL_EXPORT = '/sdcard/Download/anpaint-ci-vertical-evidence'
MAX_ARCHIVE = 72 * 1024 * 1024 + 128 * 1024
MAX_MEMBER = 24 * 1024 * 1024
IDENTITY_COMMAND = ('cat /proc/sys/kernel/random/boot_id && '
                    'getprop ro.build.version.sdk && getprop ro.product.cpu.abi')


class DeadlineExpired(Exception):
    pass


class TransportUnavailable(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unpack_dialog_archive(archive, target, remaining):
    # Shell transport cannot bypass the installed-evidence validator. In this
    # staging parser, allow only bounded, flat regular method ZIPs.
    length = archive.stat().st_size
    require(1024 <= length <= MAX_ARCHIVE and length % 512 == 0,
            'Invalid dialog transfer archive size')
    with archive.open('rb') as stream:
        stream.seek(-1024, os.SEEK_END)
        require(stream.read() == b'\0' * 1024, 'Incomplete dialog transfer archive')
    target.mkdir()
    names = set()
    with tarfile.open(archive, 'r:') as members:
        for member in members:
            remaining()
            if member.name == '.' and member.isdir() and not names:
                continue
            name = member.name.removeprefix('./')
            require(member.isreg() and re.fullmatch(r'[A-Za-z][A-Za-z0-9]{0,127}\.zip', name)
                    and name not in names and len(names) < 32
                    and 0 < member.size <= MAX_MEMBER, 'Unexpected dialog archive member')
            require(member.offset_data + member.size <= length - 1024,
                    'Truncated dialog archive member')
            names.add(name)
            with members.extractfile(member) as stream, (target / name).open('xb') as out:
                shutil.copyfileobj(stream, out, 128 * 1024)
            require((target / name).stat().st_size == member.size, 'Truncated extracted dialog ZIP')
    require(names, 'No dialog ZIPs in transfer archive')
    remaining()


def collect(adb, serial, boot_id, sdk, abi, emulator_pid, remote, output):
    started = time.monotonic()
    deadline = started + BUDGET_SECONDS
    output = Path(output)
    attempts = output.with_name(output.name + '-attempts')
    receipt_path = output.with_name(output.name + '-transfer.json')
    receipt = dict(transport_complete=False, budget_seconds=BUDGET_SECONDS,
                   serial=serial, boot_id=boot_id, device_sdk=sdk, abi=abi,
                   emulator_pid=emulator_pid, commands=[])
    owned = False
    recovered = False

    def record():
        with tempfile.NamedTemporaryFile(mode='w', dir=output.parent,
                                         prefix=receipt_path.name + '.', delete=False) as stream:
            stream.write(json.dumps(receipt, indent=2) + '\n')
            temporary = stream.name
        os.replace(temporary, receipt_path)

    def remaining():
        left = deadline - time.monotonic()
        if left <= 0:
            raise DeadlineExpired('Original collection deadline exhausted')
        return left

    def command(label, args, capture=False, binary=None):
        left = remaining()
        # A replacement device on the same serial must not supply old evidence.
        os.kill(emulator_pid, 0)
        event = dict(command=label, started_seconds=time.monotonic() - started,
                     remaining_seconds=left, exit_status=None)
        receipt['commands'].append(event)
        record()
        log = attempts / (label + '.log')
        try:
            with log.open('w') as stream:
                if binary is not None:
                    with binary.open('xb') as out:
                        result = subprocess.run([adb, '-s', serial, *args], stdout=out,
                                                stderr=stream, timeout=remaining())
                else:
                    result = subprocess.run([adb, '-s', serial, *args],
                                            stdout=subprocess.PIPE if capture else stream,
                                            stderr=stream, text=True, timeout=remaining())
                    if capture:
                        stream.write(result.stdout)
            event['exit_status'] = result.returncode
        except subprocess.TimeoutExpired:
            event['exit_status'] = 124
            raise DeadlineExpired('ADB command consumed the remaining collection deadline')
        finally:
            event['ended_seconds'] = time.monotonic() - started
            record()
        remaining()  # A late successful response cannot override the deadline.
        os.kill(emulator_pid, 0)
        return result

    def identity(label):
        result = command(label, ['shell', IDENTITY_COMMAND], capture=True)
        if result.returncode != 0:
            raise TransportUnavailable('Cannot verify original emulator session')
        expected = [boot_id, str(sdk), abi]
        require(result.stdout.replace('\r', '').splitlines() == expected,
                'Emulator boot/SDK/ABI identity changed or is malformed')

    def recover_transport():
        nonlocal recovered
        require(not recovered, 'Single passive recovery allowance already consumed')
        recovered = True
        ready = command('passive-wait', ['wait-for-device'])
        require(ready.returncode == 0, 'Same-device transport did not recover')
        identity('recovered-identity')

    try:
        require(re.fullmatch(r'emulator-[1-9][0-9]*', serial), 'Explicit emulator serial required')
        require(re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', boot_id),
                'Original emulator boot UUID required')
        require(type(emulator_pid) is int and emulator_pid > 0, 'Original emulator PID required')
        require(sdk in (30, 35) and abi in ('x86', 'x86_64'), 'Expected capture SDK/ABI required')
        require(remote in (DIALOG_EXPORT, VERTICAL_EXPORT), 'Unknown export source')
        require(not os.path.lexists(output) and not os.path.lexists(attempts)
                and not os.path.lexists(receipt_path), 'Collection destinations must be fresh')
        output.parent.mkdir(parents=True, exist_ok=True)
        attempts.mkdir()
        owned = True
        record()
        try:
            identity('initial-identity')
        except TransportUnavailable:
            # A nonzero query may be an already-offline transport. A successful
            # but mismatched identity is never retried or replaced.
            recover_transport()
        for number in (1, 2):
            target = attempts / f'attempt-{number}'
            shell_archive = number == 1 and remote == DIALOG_EXPORT
            label = 'shell-archive-1' if shell_archive else f'pull-{number}'
            if shell_archive:
                # Read existing screenshots on the shell stream first. The
                # original sync protocol remains an isolated second attempt.
                archive = attempts / 'attempt-1.tar'
                result = command(label, ['shell', '-T', 'toybox', 'tar', '-cf', '-', '-C', remote, '.'],
                                 binary=archive)
            else:
                result = command(label, ['pull', remote, str(target)])
            if result.returncode == 0:
                identity(f'after-{label}-identity')
                if shell_archive:
                    unpack_dialog_archive(archive, target, remaining)
                require(target.is_dir() and not target.is_symlink(), 'Missing regular export directory')
                remaining()
                os.kill(emulator_pid, 0)
                os.replace(target, output)
                receipt['transport_complete'] = True
                receipt['accepted_attempt'] = number
                record()
                return 0
            if number == 1 and not recovered:
                # Passive readiness only: no explicit server restart/reconnect,
                # reboot, reinstall, recapture or instrumentation retry commands.
                recover_transport()
            else:
                break
        raise ValueError('Evidence transfer failed; recovery allowance exhausted')
    except (ValueError, OSError, DeadlineExpired, tarfile.TarError) as error:
        receipt['error'] = str(error)
        # Do not overwrite a stale receipt or follow a pre-existing destination.
        if owned:
            record()
        print(str(error), file=sys.stderr)
        return 124 if isinstance(error, DeadlineExpired) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', required=True)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--boot-id', required=True)
    parser.add_argument('--sdk', type=int, required=True)
    parser.add_argument('--abi', required=True)
    parser.add_argument('--emulator-pid', type=int, required=True)
    parser.add_argument('--remote', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # subprocess.run kills/reaps its owned client when this interrupts it; the
    # unchanged outer timeout also kills the process group after its 3s grace.
    def stop(signum, frame):
        raise DeadlineExpired(f'Collection interrupted by signal {signum}')
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    return collect(args.adb, args.serial, args.boot_id, args.sdk, args.abi,
                   args.emulator_pid, args.remote, args.output)


if __name__ == '__main__':
    sys.exit(main())
