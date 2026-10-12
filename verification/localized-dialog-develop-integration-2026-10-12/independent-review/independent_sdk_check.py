import copy, json, pathlib, sys
ROOT=pathlib.Path('/workspace/shared/anpaint-pr52-current-develop-20261012');sys.path.insert(0,str(ROOT/'tools'))
from app_instrumentation_matrix import app_partition, verify_app_reports, PHASE_TIMEOUTS, SELECTED_PHASES, DIALOG
from run_android_instrumentation import declared_tests,source_tests_sha256
from test_ci_timeout_budget import controlled_model,SHELL,RUNNER,WORKFLOW,validate_budget
SOURCE=ROOT/'app/src/androidTest';all_tests=declared_tests(SOURCE);digest=source_tests_sha256(SOURCE)

def demand(ok,text):
    if not ok:raise AssertionError(text)
def denied(f):
    try:f()
    except (ValueError,AssertionError):return True
    raise AssertionError('Malformed receipt was accepted')
summary=[];neg=[]
for sdk in (21,24,30,35):
    expected=declared_tests(SOURCE,sdk_level=sdk);supp=all_tests-expected;parts=app_partition(expected,sdk);reports={}
    for phase,identities in parts.items():
        reports[phase]={'success':True,'device_sdk':sdk,'source_tests_sha256':digest,'sdk_suppressed_tests':[list(x) for x in sorted(supp)],'included_tests':sorted(f'{c}#{m}' for c,m in identities) if phase in SELECTED_PHASES else [],'timeout_seconds':PHASE_TIMEOUTS[phase],'timed_out':False,'returncode':0,'errors':[],'missing':[],'unexpected':[],'leave_target_running':phase=='seed','expected_tests':len(identities),'completed_tests':len(identities),'cases':[{'classname':c,'name':m,'status':'passed'} for c,m in sorted(identities)]}
    result=verify_app_reports(expected,sdk,reports,digest,supp)
    demand(result['declared_tests']==30,'App test inventory')
    demand(result['completed_tests']=={21:0,24:0,30:22,35:30}[sdk],'Completed count')
    demand(len(result['sdk_suppressed_tests'])=={21:28,24:28,30:6,35:0}[sdk],'Suppressed count')
    demand(result['all_app_total_timeout_seconds']=={21:0,24:0,30:630,35:1050}[sdk],'App timeout sum')
    if sdk<30:demand(result['success'] is None and result['execution_status']=='not-run-no-sdk-eligible-selected-tests','Legacy not-run status')
    summary.append(result)
    for phase in parts:
        bad=copy.deepcopy(reports);del bad[phase]
        denied(lambda:verify_app_reports(expected,sdk,bad,digest,supp));neg.append([sdk,'missing_phase',phase])
        for field,value in [('success',False),('device_sdk',True),('device_sdk',sdk+1),('source_tests_sha256','a'*64),('timeout_seconds',PHASE_TIMEOUTS[phase]+1),('timed_out',True),('returncode',1),('errors',['x']),('missing',['x']),('unexpected',['x']),('expected_tests',999),('completed_tests',999),('sdk_suppressed_tests',[['invalid','test']])]:
            bad=copy.deepcopy(reports);bad[phase][field]=value
            denied(lambda:verify_app_reports(expected,sdk,bad,digest,supp));neg.append([sdk,phase,field])
        for name,change in [('missing_case',lambda r:r['cases'].pop()),('duplicate_case',lambda r:r['cases'].append(r['cases'][0].copy())),('failed_case',lambda r:r['cases'][0].update(status='failed')),('skipped_case',lambda r:r['cases'][0].update(status='skipped')),('renamed_case',lambda r:r['cases'][0].update(name='other'))]:
            bad=copy.deepcopy(reports);change(bad[phase])
            denied(lambda:verify_app_reports(expected,sdk,bad,digest,supp));neg.append([sdk,phase,name])
    extra=copy.deepcopy(reports);extra['unknown-phase']={'success':True}
    denied(lambda:verify_app_reports(expected,sdk,extra,digest,supp));neg.append([sdk,'extra_phase'])
    if sdk<35:
        denied(lambda:app_partition(expected|{(DIALOG,'unexpectedEligibleCase')},sdk));neg.append([sdk,'eligible_dialog_not_hidden'])
    if sdk<30:
        denied(lambda:app_partition(expected|{('paint.anpaint.android.FutureTest','eligible')},sdk));neg.append([sdk,'eligible_ordinary_not_hidden'])
        extra=copy.deepcopy(reports);extra['dialog']={'success':True}
        denied(lambda:verify_app_reports(expected,sdk,extra,digest,supp));neg.append([sdk,'stale_dialog_report'])
model,limits,required=validate_budget(WORKFLOW)
demand(model['paths']['api30_five_with_five_recoveries']==1669,'API30 modeled budget')
demand(model['paths']['api35_all_eight_with_four_recoveries']==2482,'API35 envelope')
demand(limits==(43,6,53) and required==43,'Outer policy caps')
(pathlib.Path(__file__).parent/'independent-sdk-receipts.json').write_text(json.dumps({'success':True,'scope':'Synthetic host receipts only; not installed Android execution','source_digest':digest,'sdk_receipts':summary,'negative_controls_rejected':neg,'negative_count':len(neg),'timeout_model':model,'outer_limits':limits},indent=2)+'\n')
print('SDK 21/24/30/35 receipts verified; negative receipt/source mutations rejected:',len(neg));print('Completed counts:',{r['device_sdk']:r['completed_tests'] for r in summary});print('App timeout sums:',{r['device_sdk']:r['all_app_total_timeout_seconds'] for r in summary});print('Outer limits:',limits)
