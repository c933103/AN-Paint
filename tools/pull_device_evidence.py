#!/usr/bin/env python3
"""Re-pull immutable CI exports once after passive same-session ADB recovery.

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
import sys
import tempfile
import time

BUDGET_SECONDS = 15
IDENTITY_COMMAND = ('cat /proc/sys/kernel/random/boot_id && '
                    'getprop ro.build.version.sdk && getprop ro.product.cpu.abi')


class DeadlineExpired(Exception):
    pass


class TransportUnavailable(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


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

    def command(label, args, capture=False):
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
        require(remote in ('/sdcard/Download/anpaint-ci-dialog-evidence',
                           '/sdcard/Download/anpaint-ci-vertical-evidence'), 'Unknown export source')
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
            result = command(f'pull-{number}', ['pull', remote, str(target)])
            if result.returncode == 0:
                identity(f'after-pull-{number}-identity')
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
    except (ValueError, OSError, DeadlineExpired) as error:
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
