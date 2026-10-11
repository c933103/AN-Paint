import json, sys, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,'tools')
import test_app_instrumentation_matrix as app
import test_legacy_compatibility as legacy
source=Path('tools/ci_emulator.sh').read_text()
mutations={
 'restart_allowed_on_api30':('if test "$TEST_API" = 35; then','if (( TEST_API >= 30 )); then','driver'),
 'ultrahdr_exclusion_reversed':('if (( TEST_API < 35 )); then','if (( TEST_API == 35 )); then','driver'),
 'native_phase_deadline_relaxed':('--suite Paintroid --timeout-seconds 180','--suite Paintroid --timeout-seconds 181','driver'),
 'sdk_ineligible_editor_invoked':('if (( TEST_API >= 26 )); then','if (( TEST_API >= 21 )); then','driver'),
 'stale_api30_omission_text':('both phase classes excluded on API %s','both phase classes excluded on API30 %s','driver'),
 'wrong_abi_accepted':('if [[ "$ready_output" != "$emulator_abi" ]]; then','if false; then','startup'),
 'wrong_sdk_accepted':('if [[ "$ready_output" != "$TEST_API" ]]; then','if false; then','startup'),
}
results=[]
original_read=Path.read_text
for name,(old,new,kind) in mutations.items():
 assert source.count(old)==1,(name,source.count(old))
 changed=source.replace(old,new)
 result=unittest.TestResult()
 if kind=='driver':
  def read(path,*args,**kwargs):
   return changed if path.resolve()==(app.ROOT/'tools/ci_emulator.sh').resolve() else original_read(path,*args,**kwargs)
  with patch.object(Path,'read_text',read):
   app.ComposedDriverTest('test_main_schedules_every_distinct_phase_and_preserves_failure_gates').run(result)
 else:
  with patch.object(legacy,'SHELL',changed):
   legacy.LegacyStartupTest('test_mismatched_sdk_or_abi_and_invalid_selection_fail_before_install').run(result)
 caught=bool(result.failures) and not result.errors
 results.append(dict(mutation=name,rejected=caught,assertion_failures=len(result.failures),harness_errors=len(result.errors)))
print(json.dumps(results,indent=2))
raise SystemExit(0 if all(r['rejected'] for r in results) else 1)
