#!/usr/bin/env python3
"""Linux CI Python owner: deadline, live logs, and bounded TERM/KILL cleanup.

The shell execs this owner, so cancellation reaches the process that owns the
child session. Subreaping also collects grandchildren after their parents exit.
No deadline result is rewritten as the child's later successful exit.
"""
import argparse
import ctypes
import datetime
import errno
import os
from pathlib import Path
import resource
import re
import signal
import subprocess
import sys
import threading
import time
import uuid


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def children():
    # Only direct children of this single-command subreaper; never unrelated PIDs.
    path=Path(f'/proc/self/task/{os.getpid()}/children')
    try:return [int(x) for x in path.read_text().split()]
    except FileNotFoundError:
        # Some Linux container proc mounts omit the children extension.
        result=[]
        for entry in Path('/proc').iterdir():
            if not entry.name.isdecimal():continue
            try:fields=(entry/'stat').read_text().rsplit(')',1)[1].split()
            except OSError as error:
                if error.errno in (errno.ENOENT,errno.ESRCH):continue
                raise
            if int(fields[1])==os.getpid():result.append(int(entry.name))
        return result


def signal_group(pgid, signum):
    try:os.killpg(pgid,signum)
    except ProcessLookupError:pass


def cleanup(proc, grace, reap_grace=5, already_signalled=False):
    """Return only after the owned group and adopted descendants are reaped.

    Signal the session group only while its unreaped leader remains owned; after
    leader exit, signal/reap adopted children rather than a recyclable PGID.
    """
    if not already_signalled and proc.poll() is None:signal_group(proc.pid,signal.SIGTERM)
    end=time.monotonic()+grace
    forced=False
    hard_end=end+reap_grace
    while True:
        proc.poll()  # Popen remains the sole reaper for its direct command.
        owned=children()
        for pid in owned:
            if pid==proc.pid:continue
            try:
                waited,_=os.waitpid(pid,os.WNOHANG)
                if not waited:os.kill(pid,signal.SIGKILL if forced else signal.SIGTERM)
            except ProcessLookupError:pass
            except ChildProcessError:pass
        if not children():return forced,True
        if time.monotonic()>=end:
            forced=True
            if proc.poll() is None:signal_group(proc.pid,signal.SIGKILL)
            for pid in children():
                try:os.kill(pid,signal.SIGKILL)
                except ProcessLookupError:pass
        if time.monotonic()>=hard_end:return forced,False
        time.sleep(.02)


def verify_completion(path):
    try:
        lines=Path(path).read_text().splitlines()
        pairs=[line.split('=',1) for line in lines]
        if any(len(pair)!=2 for pair in pairs):return False
        data=dict(pairs)
        if len(data)!=len(pairs) or set(data)!={'launch_id','reason','forced_kill','owned_children_remaining','cleanup_complete','output_complete'}:return False
        owner=(Path(path).parent/'python.owner').read_text().strip()
        if not re.fullmatch('[0-9a-f]{32}',owner) or data['launch_id']!=owner:return False
        if data['reason'] not in {'completed','signal','deadline','launch-error'}:return False
        if data['forced_kill'] not in {'true','false'} or data['output_complete'] not in {'true','false'}:return False
        return data['cleanup_complete']=='true' and data['output_complete']=='true' and data['owned_children_remaining']=='0'
    except (OSError,UnicodeError,ValueError):return False


def finish_pump(thread,seconds=2):
    thread.join(timeout=seconds)
    return not thread.is_alive()


def main(argv=None):
    argv=sys.argv[1:] if argv is None else argv
    if argv[:1]==['--verify-completion']:
        return 0 if len(argv)==2 and verify_completion(argv[1]) else 125
    parser=argparse.ArgumentParser()
    parser.add_argument('--timeout-seconds',type=float,required=True)
    parser.add_argument('--kill-after-seconds',type=float,required=True)
    parser.add_argument('command',nargs=argparse.REMAINDER)
    args=parser.parse_args(argv)
    command=args.command[1:] if args.command[:1]==['--'] else args.command
    if not command or not 0<args.timeout_seconds<float('inf') or not 0<args.kill_after_seconds<float('inf'):
        parser.error('Expected finite positive deadlines and a command')
    libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(36,1,0,0,0)!=0: # PR_SET_CHILD_SUBREAPER, Linux runner contract.
        raise OSError(ctypes.get_errno(),'Could not become CI child subreaper')
    children()  # Fail before launching if owned-child discovery is unavailable.
    directory=Path('build/reports/ci-phases');directory.mkdir(parents=True,exist_ok=True)
    for name in ('python.lifecycle','python.ended-at','python.time'):
        (directory/name).unlink(missing_ok=True)
    launch_id=uuid.uuid4().hex
    owner=directory/'python.owner.partial';owner.write_text(launch_id+'\n');owner.replace(directory/'python.owner')
    (directory/'python.started-at').write_text(stamp()+'\n')
    started=time.monotonic();usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    received=[];pump_errors=[];proc=None
    def cancelled(signum,frame):
        if not received:received.append(signum)
    for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,cancelled)
    status=125;reason='launch-error';forced=False;clean=True;output_complete=True;forwarded=False
    with (directory/'python.log').open('wb') as log:
        try:
            proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
        except OSError as error:
            message=(str(error)+'\n').encode();log.write(message);sys.stderr.buffer.write(message)
        else:
            def pump():
                while True:
                    try:
                        chunk=proc.stdout.read1(65536)
                        if not chunk:break
                        log.write(chunk);log.flush()
                        sys.stdout.buffer.write(chunk);sys.stdout.buffer.flush()
                    except (OSError,ValueError) as error:
                        pump_errors.append(str(error))
                        break
            thread=threading.Thread(target=pump,daemon=True)
            deadline=started+args.timeout_seconds
            try:
                thread.start()
                while True:
                    if received:
                        status=128+received[0];reason='signal'
                        if proc.poll() is None:
                            signal_group(proc.pid,received[0]);forwarded=True
                        break
                    if pump_errors:status=125;reason='logging-error';break
                    result=proc.poll()
                    if result is not None:status=result if result>=0 else 128-result;reason='completed';break
                    if time.monotonic()>=deadline:status=124;reason='deadline';break
                    time.sleep(.02)
            except (OSError,RuntimeError) as error:
                pump_errors.append(str(error));status=125;reason='logging-error'
            finally:
                forced,clean=cleanup(proc,args.kill_after_seconds,already_signalled=forwarded)
                output_complete=finish_pump(thread) if thread.ident is not None else False
            if not clean:status=125;reason='cleanup-error'
            elif pump_errors or not output_complete:status=125;reason='logging-error'
            elif received and reason=='completed':status=128+received[0];reason='signal'
    remaining=len(children())
    clean=clean and remaining==0
    if not clean:status=125;reason='cleanup-error'
    elapsed=time.monotonic()-started;after=resource.getrusage(resource.RUSAGE_CHILDREN)
    (directory/'python.time').write_text(f'real_seconds={elapsed:.3f}\nuser_seconds={after.ru_utime-usage.ru_utime:.3f}\nsys_seconds={after.ru_stime-usage.ru_stime:.3f}\nexit_status={status}\n')
    (directory/'python.ended-at').write_text(stamp()+'\n')
    marker=directory/'python.lifecycle.partial'
    marker.write_text(f'launch_id={launch_id}\nreason={reason}\nforced_kill={str(forced).lower()}\nowned_children_remaining={remaining}\ncleanup_complete={str(clean).lower()}\noutput_complete={str(output_complete).lower()}\n')
    marker.replace(directory/'python.lifecycle')
    return status


if __name__=='__main__':raise SystemExit(main())
