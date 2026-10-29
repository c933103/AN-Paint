"""Owned process lifecycle, not a universal runner/kernel liveness claim."""
from pathlib import Path
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
OWNER=ROOT/'tools/ci_run_process_group.py'


class PythonProcessGroupTests(unittest.TestCase):
    def launch(self,root,script,timeout=5,grace=.15,phase='python'):
        return subprocess.Popen([sys.executable,str(OWNER),'--phase',phase,'--timeout-seconds',str(timeout),
            '--kill-after-seconds',str(grace),'--',sys.executable,'-u','-c',script],
            cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

    def finish(self,proc):
        try:return proc.communicate(timeout=10)
        finally:
            if proc.poll() is None:
                proc.send_signal(signal.SIGTERM)
                try:proc.communicate(timeout=3)
                except subprocess.TimeoutExpired:proc.kill();proc.communicate()

    def ready(self,path,proc):
        end=time.monotonic()+5
        while time.monotonic()<end and not path.exists() and proc.poll() is None:time.sleep(.01)
        self.assertTrue(path.exists(), 'Owned child readiness must be observed before signal')

    def gone(self,pid):
        with self.assertRaises(ProcessLookupError):os.kill(pid,0)

    def reports(self,root,status,reason,phase='python'):
        p=Path(root)/'build/reports/ci-phases'
        self.assertIn(f'exit_status={status}\n',(p/f'{phase}.time').read_text())
        for key in ('real_seconds','user_seconds','sys_seconds'):
            self.assertRegex((p/f'{phase}.time').read_text(),key+r'=\d+\.\d+')
        self.assertIn('reason='+reason+'\n',(p/f'{phase}.lifecycle').read_text())
        self.assertIn('owned_children_remaining=0\n',(p/f'{phase}.lifecycle').read_text())
        for name in (f'{phase}.started-at',f'{phase}.ended-at'):
            self.assertRegex((p/name).read_text(),r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\n$')
        return p

    def test_success_and_command_failure_keep_live_raw_output_and_exit(self):
        for status in (0,7):
            with self.subTest(status=status),tempfile.TemporaryDirectory() as root:
                proc=self.launch(root,f'import sys;print("out");print("err",file=sys.stderr);sys.exit({status})')
                out,err=self.finish(proc);self.assertEqual(status,proc.returncode,err)
                p=self.reports(root,status,'completed');self.assertEqual(out,(p/'python.log').read_text())
                self.assertIn('out',out);self.assertIn('err',out)

    def test_deadline_stays_failure_when_term_handler_exits_zero(self):
        with tempfile.TemporaryDirectory() as root:
            script='import signal,time,sys;signal.signal(signal.SIGTERM,lambda *a:sys.exit(0));print("ready",flush=True);time.sleep(10)'
            proc=self.launch(root,script,timeout=.3);out,err=self.finish(proc)
            self.assertEqual(124,proc.returncode,err);self.assertIn('ready',out);self.reports(root,124,'deadline')

    def stubborn_tree(self):
        # Grandchild deliberately escapes the group; subreaping must still own it.
        grand='import os,signal,time;from pathlib import Path;signal.signal(signal.SIGTERM,signal.SIG_IGN);signal.signal(signal.SIGINT,signal.SIG_IGN);Path("grand.pid").write_text(str(os.getpid()));time.sleep(30)'
        return ('import os,signal,time,subprocess,sys;from pathlib import Path;'
                'signal.signal(signal.SIGTERM,signal.SIG_IGN);signal.signal(signal.SIGINT,signal.SIG_IGN);'
                'Path("child.pid").write_text(str(os.getpid()));'
                f'subprocess.Popen([sys.executable,"-u","-c",{grand!r}],start_new_session=True);'
                'print("tree-running",flush=True);time.sleep(30)')

    def test_deadline_kills_and_reaps_stubborn_child_and_escaped_grandchild(self):
        for phase in ('python','jvm'):
            with self.subTest(phase=phase),tempfile.TemporaryDirectory() as root:
                root=Path(root);(root/'tools').mkdir();shutil.copy(OWNER,root/'tools')
                shell=(ROOT/'tools/ci_run_timed.sh').read_text().replace('--timeout-seconds 1800','--timeout-seconds 1').replace('--timeout-seconds 1440','--timeout-seconds 1').replace('--kill-after-seconds 15','--kill-after-seconds .15')
                (root/'tools/ci_run_timed.sh').write_text(shell)
                proc=subprocess.Popen(['bash','tools/ci_run_timed.sh',phase,sys.executable,'-u','-c',self.stubborn_tree()],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                self.ready(root/'grand.pid',proc);out,err=self.finish(proc)
                self.assertEqual(124,proc.returncode,err);p=self.reports(root,124,'deadline',phase)
                self.assertIn('forced_kill=true',(p/f'{phase}.lifecycle').read_text())
                for n in ('child.pid','grand.pid'):self.gone(int((root/n).read_text()))
                # A clean timeout remains failed, but required later checks can run.
                r=subprocess.run(['bash','tools/ci_run_timed.sh','native','true'],cwd=root,capture_output=True,text=True,timeout=5)
                self.assertEqual(0,r.returncode,r.stderr)

    def test_sigterm_and_sigint_to_owner_propagate_and_reap_before_return(self):
        for phase,sig in (('python',signal.SIGTERM),('python',signal.SIGINT),('jvm',signal.SIGTERM),('jvm',signal.SIGINT)):
            with self.subTest(phase=phase,signal=sig),tempfile.TemporaryDirectory() as root:
                proc=self.launch(root,self.stubborn_tree(),phase=phase);self.ready(Path(root)/'grand.pid',proc)
                proc.send_signal(sig);out,err=self.finish(proc)
                self.assertEqual(128+sig,proc.returncode,err);self.reports(root,128+sig,'signal',phase)
                for n in ('child.pid','grand.pid'):self.gone(int((Path(root)/n).read_text()))

    def test_successful_parent_cannot_leave_owned_background_descendant(self):
        with tempfile.TemporaryDirectory() as root:
            script=self.stubborn_tree().replace('print("tree-running",flush=True);time.sleep(30)',
                'print("parent-done",flush=True);time.sleep(.15)')
            proc=self.launch(root,script);out,err=self.finish(proc)
            self.assertEqual(0,proc.returncode,err);self.reports(root,0,'completed')
            for n in ('child.pid','grand.pid'):self.gone(int((Path(root)/n).read_text()))

    def test_cancellation_during_background_cleanup_cannot_be_success(self):
        with tempfile.TemporaryDirectory() as root:
            script=self.stubborn_tree().replace('print("tree-running",flush=True);time.sleep(30)',
                'print("parent-done",flush=True);time.sleep(.1)')
            proc=self.launch(root,script,grace=.6);self.ready(Path(root)/'grand.pid',proc)
            time.sleep(.2);proc.send_signal(signal.SIGTERM);out,err=self.finish(proc)
            self.assertEqual(143,proc.returncode,err);self.reports(root,143,'signal')
            for n in ('child.pid','grand.pid'):self.gone(int((Path(root)/n).read_text()))

    def test_invalid_or_unbounded_deadlines_cannot_launch_command(self):
        for limit in ('0','-1','nan','inf'):
            with self.subTest(limit=limit),tempfile.TemporaryDirectory() as root:
                proc=subprocess.run([sys.executable,str(OWNER),'--timeout-seconds',limit,
                    '--kill-after-seconds','.1','--',sys.executable,'-c','open("bad","w").close()'],
                    cwd=root,capture_output=True,text=True,timeout=5)
                self.assertNotEqual(0,proc.returncode);self.assertFalse((Path(root)/'bad').exists())

    def test_missing_executable_is_failure_with_terminal_receipt(self):
        with tempfile.TemporaryDirectory() as root:
            proc=subprocess.run([sys.executable,str(OWNER),'--timeout-seconds','1','--kill-after-seconds','.1','--','/no/such/ci-command'],cwd=root,capture_output=True,text=True,timeout=5)
            self.assertEqual(125,proc.returncode);self.reports(root,125,'launch-error')

    def test_later_phase_rejects_missing_malformed_failed_or_cross_run_receipt(self):
        good='launch_id='+'a'*32+'\nreason=completed\nforced_kill=false\nowned_children_remaining=0\ncleanup_complete=true\noutput_complete=true\n'
        cases=[None, 'invalid',good.replace('cleanup_complete=true','cleanup_complete=false'),
               good.replace('owned_children_remaining=0','owned_children_remaining=1'),
               good.replace('launch_id='+'a'*32,'launch_id='+'b'*32),
               good+'extra=unreviewed\n',good.replace('output_complete=true','output_complete=false'),
               good.replace('reason=completed','reason=cleanup-error')]
        for previous,following in (('python','jvm'),('jvm','native'),('jvm','lint')):
            for content in cases:
                with self.subTest(previous=previous,following=following,content=content),tempfile.TemporaryDirectory() as root:
                    root=Path(root);(root/'tools').mkdir();shutil.copy(OWNER,root/'tools');shutil.copy(ROOT/'tools/ci_run_timed.sh',root/'tools')
                    reports=root/'build/reports/ci-phases';reports.mkdir(parents=True)
                    (reports/f'{previous}.started-at').write_text('started\n');(reports/f'{previous}.owner').write_text('a'*32+'\n')
                    if content is not None:(reports/f'{previous}.lifecycle').write_text(content)
                    r=subprocess.run(['bash','tools/ci_run_timed.sh',following,sys.executable,'-c','open("launched","w").close()'],cwd=root,capture_output=True,text=True,timeout=5)
                    self.assertEqual(125,r.returncode,r.stderr);self.assertFalse((root/'launched').exists())

    def test_clean_failed_python_allows_required_later_phase_with_distinct_owner(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root);(root/'tools').mkdir();shutil.copy(OWNER,root/'tools');shutil.copy(ROOT/'tools/ci_run_timed.sh',root/'tools')
            proc=self.launch(root,'import sys;sys.exit(7)');self.finish(proc);self.assertEqual(7,proc.returncode)
            r=subprocess.run(['bash','tools/ci_run_timed.sh','jvm',sys.executable,'-c','open("launched","w").close()'],cwd=root,capture_output=True,text=True,timeout=5)
            self.assertEqual(0,r.returncode,r.stderr);self.assertTrue((root/'launched').exists())
            reports=root/'build/reports/ci-phases'
            self.reports(root,7,'completed');self.reports(root,0,'completed','jvm')
            self.assertNotEqual((reports/'python.owner').read_text(),(reports/'jvm.owner').read_text())
            shutil.copy(reports/'python.lifecycle',reports/'jvm.lifecycle')
            r=subprocess.run(['bash','tools/ci_run_timed.sh','native','true'],cwd=root,capture_output=True,text=True,timeout=5)
            self.assertEqual(125,r.returncode,r.stderr)

    def test_unreapable_child_and_stuck_output_have_finite_failure_bound(self):
        import importlib.util
        from unittest.mock import Mock,patch
        spec=importlib.util.spec_from_file_location('ci_owner_under_test',OWNER);owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)
        proc=Mock(pid=999999);proc.poll.return_value=0
        clock=[0.0]
        def tick(seconds):clock[0]+=seconds
        with patch.object(owner,'children',return_value=[888888]),patch.object(owner.os,'waitpid',return_value=(0,0)),patch.object(owner.os,'kill'),patch.object(owner,'signal_group'),patch.object(owner.time,'monotonic',side_effect=lambda:clock[0]),patch.object(owner.time,'sleep',side_effect=tick):
            forced,clean=owner.cleanup(proc,.1,.2)
        self.assertTrue(forced);self.assertFalse(clean);self.assertLess(clock[0],.4)
        thread=Mock();thread.is_alive.return_value=True
        self.assertFalse(owner.finish_pump(thread));thread.join.assert_called_once_with(timeout=2)

    def test_handler_only_records_and_main_forwards_exact_cancellation_signal(self):
        import ast
        syntax=ast.parse(OWNER.read_text())
        handler=next(n for n in ast.walk(syntax) if isinstance(n,ast.FunctionDef) and n.name=='cancelled')
        calls=[ast.unparse(n.func) for n in ast.walk(handler) if isinstance(n,ast.Call)]
        self.assertEqual(['received.append'],calls)
        for sig in (signal.SIGTERM,signal.SIGINT):
            with self.subTest(signal=sig),tempfile.TemporaryDirectory() as root:
                script='import signal,time,sys;from pathlib import Path;'+\
                    'signal.signal(signal.SIGTERM,lambda n,f:(Path("signal").write_text(str(n)),sys.exit(0)));'+\
                    'signal.signal(signal.SIGINT,lambda n,f:(Path("signal").write_text(str(n)),sys.exit(0)));'+\
                    'Path("ready").write_text("yes");time.sleep(30)'
                proc=self.launch(root,script);self.ready(Path(root)/'ready',proc);proc.send_signal(sig)
                out,err=self.finish(proc);self.assertEqual(128+sig,proc.returncode,err)
                self.assertEqual(str(int(sig)),(Path(root)/'signal').read_text());self.reports(root,128+sig,'signal')

    def test_workflow_and_shell_use_exact_owned_deadline_and_unchanged_command(self):
        shell=(ROOT/'tools/ci_run_timed.sh').read_text();workflow=(ROOT/'.github/workflows/android.yml').read_text()
        self.assertIn('exec python3 tools/ci_run_process_group.py --timeout-seconds 1800 --kill-after-seconds 15 -- "$@"',shell)
        self.assertIn("run: bash tools/ci_run_timed.sh python python3 -m unittest discover -s tools -p 'test_*.py'",workflow)
        block=workflow.split('      - name: Run Python contracts\n',1)[1].split('      - name:',1)[0]
        self.assertIn('timeout-minutes: 31',block)
        self.assertIn('exec python3 tools/ci_run_process_group.py --phase jvm --timeout-seconds 1440 --kill-after-seconds 15 -- "$@"',shell)
        jvm=workflow.split('      - name: Run JVM regression tests\n',1)[1].split('      - name:',1)[0]
        self.assertIn('timeout-minutes: 25',jvm)
        import ast
        syntax=ast.parse(OWNER.read_text())
        defs={n.name:n for n in syntax.body if isinstance(n,ast.FunctionDef)}
        cleanup_defaults=dict(zip([a.arg for a in defs['cleanup'].args.args][-len(defs['cleanup'].args.defaults):],map(ast.literal_eval,defs['cleanup'].args.defaults)))
        pump_defaults=dict(zip([a.arg for a in defs['finish_pump'].args.args][-len(defs['finish_pump'].args.defaults):],map(ast.literal_eval,defs['finish_pump'].args.defaults)))
        self.assertEqual(5,cleanup_defaults['reap_grace']);self.assertEqual(2,pump_defaults['seconds'])
        self.assertEqual(1,shell.count('exec python3 tools/ci_run_process_group.py --timeout-seconds'))
        self.assertLess(1800+15+cleanup_defaults['reap_grace']+pump_defaults['seconds'],31*60)
        self.assertLess(1440+15+cleanup_defaults['reap_grace']+pump_defaults['seconds'],25*60)
