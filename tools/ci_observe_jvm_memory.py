#!/usr/bin/env python3
"""Read-only Linux JVM-phase memory observer; never launch or signal workloads.

Aggregate RSS is sampled (not an exact kernel peak, and shared pages can be
counted twice). Observed per-process VmHWM is a separate kernel high-water
measurement; short-lived/unobserved processes can be missed. No command lines,
environments or unrelated process data are saved.
"""
import argparse
import json
import os
from pathlib import Path
import select
import signal
import time


def snapshot(proc=Path('/proc')):
    result = {}
    for entry in proc.iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            fields = (entry / 'stat').read_text().rsplit(')', 1)[1].split()
            status = dict(line.split(':', 1) for line in (entry / 'status').read_text().splitlines() if ':' in line)
            result[int(entry.name)] = {
                'parent': int(fields[1]), 'start_ticks': int(fields[19]),
                'rss_kib': int(status.get('VmRSS', '0 kB').split()[0]),
                'hwm_kib': int(status.get('VmHWM', '0 kB').split()[0]),
            }
        except (FileNotFoundError, ProcessLookupError):
            continue  # Normal process-exit race; other failures fail the probe.
    return result


def select_owned(frame, root, known, excluded):
    """Bind PIDs to Linux start ticks, retaining observed detached descendants."""
    selected = {pid for pid, row in frame.items()
                if pid != excluded and known.get(pid) == row['start_ticks']}
    if root in frame and known.get(root) == frame[root]['start_ticks']:
        selected.add(root)
    while True:
        additions = {pid for pid, row in frame.items()
                     if pid != excluded and row['parent'] in selected}
        if additions <= selected:
            break
        selected.update(additions)
    for pid in selected:
        known[pid] = frame[pid]['start_ticks']
    return {pid: frame[pid] for pid in selected if pid != root}


def available_kib(proc=Path('/proc')):
    fields = dict(line.split(':', 1) for line in (proc / 'meminfo').read_text().splitlines())
    return int(fields['MemAvailable'].split()[0])


def save(path, receipt):
    temporary = path.with_suffix(path.suffix + '.partial')
    temporary.write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    temporary.replace(path)


def stop_observer(pid, start_ticks, parent_pid, output):
    """Stop only the identity-bound observer: TERM 1 s, KILL 1 s, no blind wait."""
    receipt = {'cleanup_complete': False, 'forced_kill': False}
    fd = None
    try:
        try:
            fd = os.pidfd_open(pid)
        except ProcessLookupError:
            receipt['cleanup_complete'] = True
            save(output, receipt)
            return 0
        poller = select.poll(); poller.register(fd, select.POLLIN)
        if not poller.poll(0):
            fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
            if int(fields[19]) != start_ticks or int(fields[1]) != parent_pid:
                raise RuntimeError('Observer identity/parent mismatch; no signal sent')
            signal.pidfd_send_signal(fd, signal.SIGTERM)
            if not poller.poll(1000):
                receipt['forced_kill'] = True
                signal.pidfd_send_signal(fd, signal.SIGKILL)
                if not poller.poll(1000):
                    raise RuntimeError('Observer did not exit within bounded cleanup')
        receipt['cleanup_complete'] = True
        save(output, receipt)
        return 0
    except (OSError, ValueError, IndexError, RuntimeError) as error:
        receipt['error'] = str(error)
        save(output, receipt)
        return 125
    finally:
        if fd is not None:
            os.close(fd)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-pid', type=int)
    parser.add_argument('--stop-pid', type=int)
    parser.add_argument('--start-ticks', type=int)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.stop_pid is not None:
        if args.root_pid is not None or args.start_ticks is None:
            parser.error('Stop requires identity only')
        return stop_observer(args.stop_pid, args.start_ticks, os.getppid(), args.output)
    if args.root_pid is None or args.start_ticks is not None:
        parser.error('Observation requires root PID only')
    stopping = []
    signal.signal(signal.SIGTERM, lambda *_: stopping.append(True))
    signal.signal(signal.SIGINT, lambda *_: stopping.append(True))
    receipt = {'kind': 'sampled descendant RSS excluding observer; not exact aggregate peak',
               'interval_seconds': 0.1, 'samples': 0, 'peak_sampled_rss_kib': 0,
               'minimum_host_available_kib': None, 'per_process_hwm_kib': {},
               'completed': False}
    started = time.monotonic()
    try:
        first = snapshot()
        if args.root_pid not in first:
            raise RuntimeError('Measured shell exited before observation started')
        known = {args.root_pid: first[args.root_pid]['start_ticks']}
        while True:
            frame = snapshot()
            selected = select_owned(frame, args.root_pid, known, os.getpid())
            receipt['samples'] += 1
            total = sum(row['rss_kib'] for row in selected.values())
            receipt['peak_sampled_rss_kib'] = max(receipt['peak_sampled_rss_kib'], total)
            available = available_kib()
            previous = receipt['minimum_host_available_kib']
            receipt['minimum_host_available_kib'] = available if previous is None else min(previous, available)
            for pid, row in selected.items():
                key = f"{pid}:{row['start_ticks']}"
                receipt['per_process_hwm_kib'][key] = max(receipt['per_process_hwm_kib'].get(key, 0), row['hwm_kib'])
            receipt['observed_seconds'] = round(time.monotonic() - started, 3)
            if stopping:
                receipt['completed'] = True
                break
            if args.root_pid not in frame or frame[args.root_pid]['start_ticks'] != known[args.root_pid]:
                raise RuntimeError('Measured shell disappeared without stopping observer')
            if receipt['samples'] % 10 == 1:
                save(args.output, receipt)
            time.sleep(.1)
        save(args.output, receipt)
        return 0
    except (OSError, ValueError, KeyError, IndexError, RuntimeError) as error:
        receipt['error'] = str(error)
        save(args.output, receipt)
        return 125


if __name__ == '__main__':
    raise SystemExit(main())
