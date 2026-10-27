"""Current English expectations and the pending two-term review queue.

Historical paired-language fixtures stay unchanged. Default-English and explicitly receipt-bound current successors are selected here;
no historical fixture or receipt is rewritten.
"""
import json
from kazakh_tajik_pashto_priority_expectations import require_shared_row as kk_tg_ps_shared_row
from basque_frisian_uzbek_priority_expectations import require_shared_row
from galician_priority_expectations import MEMORY_ADDITIONS as GL_ADDITIONS, current_row as gl_row, MEMORY_CORRECTIONS as NL_DE_MEMORY_CORRECTIONS, wording_successor as nl_de_successor
from maori_samoan_kinyarwanda_priority_expectations import MEMORY_ADDITIONS as MI_SM_RW_ADDITIONS, current_row as mi_sm_rw_row
from current_localization_contracts import fixture
from cebuano_low_german_kashubian_priority_expectations import require_shared_row as ceb_nds_csb_shared_row
from walloon_northern_sami_sanskrit_priority_expectations import require_shared_row as wa_se_sa_shared_row
from memory_warning_successors import current_warning_expectation
from pathlib import Path
from irish_gaelic_welsh_priority_expectations import MEMORY_ADDITIONS as GA_GD_CY_ADDITIONS, current_row as ga_gd_cy_row
from somali_wolof_haitian_creole_priority_expectations import MEMORY_ADDITIONS as SO_WO_HT_ADDITIONS, current_row as so_wo_ht_row, require_addition as require_so_wo_ht_addition
from breton_asturian_occitan_priority_expectations import MEMORY_ADDITIONS as BR_AST_OC_ADDITIONS, require_addition as br_ast_oc_addition
from interlingua_latin_kurdish_priority_expectations import MEMORY_ADDITIONS as IA_LA_KU_ADDITIONS, require_addition as ia_la_ku_addition
from kabyle_hmong_daw_maithili_priority_expectations import MEMORY_ADDITIONS as KAB_MWW_MAI_ADDITIONS, require_addition as kab_mww_mai_addition
from yoruba_zulu_xhosa_priority_expectations import MEMORY_ADDITIONS as YO_ZU_XH_ADDITIONS, current_row as yo_zu_xh_row
from hausa_igbo_lingala_priority_expectations import MEMORY_ADDITIONS as HA_IG_LN_ADDITIONS, current_row as ha_ig_ln_row
from javanese_sundanese_kyrgyz_priority_expectations import MEMORY_ADDITIONS as JV_SU_KY_ADDITIONS, current_row as jv_su_ky_row
from assamese_khmer_lao_priority_expectations import MEMORY_ADDITIONS as AS_KM_LO_ADDITIONS, current_row as as_km_lo_row
from nepali_punjabi_priority_expectations import MEMORY_ADDITIONS as NE_PA_ADDITIONS, current_row as ne_pa_row
from kannada_malayalam_filipino_priority_expectations import MEMORY_ADDITIONS as KN_ML_ADDITIONS, current_row as kn_ml_row
from marathi_tamil_telugu_priority_expectations import MEMORY_ADDITIONS as MR_TA_TE_ADDITIONS, current_row as mr_ta_te_row

RECORD = Path(__file__).resolve().parents[1] / 'translations/source-review/memory-warnings-20261021.json'
KEYS = {'ui_no_resize_fits_decoder_memory', 'ui_assembly_source_memory_floor'}
PRIORITY_TAGS = frozenset({'bg', 'bn'})
PRIORITY_ADDITIONS = frozenset({('uk','ui_assembly_source_memory_floor'),
    ('uk','ui_no_resize_fits_decoder_memory'),('ro','ui_no_resize_fits_decoder_memory')})
SK_SL_CA_ADDITIONS = frozenset((tag, 'ui_no_resize_fits_decoder_memory') for tag in ('sk','sl','ca'))
KA_HY_AZ_ADDITIONS = frozenset((tag,key) for tag in ('ka','hy','az') for key in KEYS)
EU_FY_UZ_ADDITIONS = frozenset((tag,key) for tag in ('eu-ES','fy','uz-Latn') for key in KEYS)
KK_TG_PS_ADDITIONS = frozenset((tag,key) for tag in ('kk','tg','ps') for key in KEYS)
CEB_NDS_CSB_ADDITIONS = frozenset((tag,key) for tag in ('nds', 'csb') for key in KEYS)
WA_SE_SA_ADDITIONS = frozenset((tag,key) for tag in ('wa', 'se', 'sa') for key in KEYS)
SINGLE_KEY_FIXTURES = {
    'nn': 'nynorsk_p0_remaining_wording.json',
    'da': 'danish_norwegian_p0_wording.json',
    'no': 'danish_norwegian_p0_wording.json',
    'ca': 'catalan_romanian_completion_wording.json',
    'ro': 'catalan_romanian_completion_wording.json',
    'sk': 'slovak_slovenian_p0_wording.json',
    'sl': 'slovak_slovenian_p0_wording.json',
    'sr-Cyrl': 'serbian_p0_wording.json',
    'sr-Latn': 'serbian_p0_wording.json',
    'hr': 'croatian_bosnian_p0_wording.json',
    'bs': 'croatian_bosnian_p0_wording.json',
}
SINGLE_KEY_EXPECTATIONS = frozenset(
    (tag, 'ui_assembly_source_memory_floor') for tag in SINGLE_KEY_FIXTURES)


def review_record():
    return json.loads(RECORD.read_text(encoding='utf-8'))


def current_source_expectation(key, tag, historical_value):
    """Keep historical evidence; select only explicitly bound current expectations.

Reject a changed historical English pair instead of letting the correction hide
fixture corruption. This selects explicitly bound paired and single-key
expectations, not a catalogue generator, review result or reconstruction of an
old source snapshot.
"""
    if (tag,key) in NL_DE_MEMORY_CORRECTIONS:
        return nl_de_successor(tag,key,historical_value)
    if key not in KEYS:
        return historical_value
    if (tag,key) in EU_FY_UZ_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=require_shared_row(tag,key,fixture('basque_frisian_uzbek_priority_wording/'+tag+'.json'),historical_value=historical_value)
        if historical_value is not None or old is not None or 'previous_target' not in row or row['previous_target'] is not None:
            raise ValueError('EU/FY/UZ historical warning addition must be absent: '+tag+'/'+key)
        if row['source']!={'value':queue['keys'][key]['corrected_english'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
            raise ValueError('EU/FY/UZ warning source or attributes differ: '+tag+'/'+key)
        return row['reviewed_value']
    if (tag,key) in KK_TG_PS_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=kk_tg_ps_shared_row(tag,key,fixture('kazakh_tajik_pashto_priority_wording/'+tag+'.json'),historical_value=historical_value)
        if historical_value is not None or old is not None or 'previous_target' not in row or row['previous_target'] is not None:
            raise ValueError('KK/TG/PS historical warning addition must be absent: '+tag+'/'+key)
        if row['source']!={'value':queue['keys'][key]['corrected_english'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
            raise ValueError('KK/TG/PS warning source or attributes differ: '+tag+'/'+key)
        return row['reviewed_value']
    if (tag,key) in GA_GD_CY_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=ga_gd_cy_row(tag,key)
        if historical_value is not None or old is not None:
            raise ValueError('Historical GA/GD/CY warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english']:
            raise ValueError('GA/GD/CY warning source differs: '+tag+'/'+key)
        return row['target']
    if (tag, key) in KA_HY_AZ_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        current=fixture('georgian_armenian_azerbaijani_priority_wording.json')
        row=current['locales'][tag]['values'][key]
        if historical_value is not None or old is not None or row['previous'] is not None:
            raise ValueError('Historical KA/HY/AZ addition must be absent: '+tag+'/'+key)
        if current['sources'][key]['value'] != queue['keys'][key]['corrected_english'] or row['attributes'] != {'name':key}:
            raise ValueError('KA/HY/AZ source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag,key) in GL_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=gl_row(tag,key)
        if historical_value is not None or old is not None:
            raise ValueError('Historical Galician warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english']:
            raise ValueError('Galician warning source differs: '+tag+'/'+key)
        return row['target']
    if (tag,key) in MI_SM_RW_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=mi_sm_rw_row(tag,key)
        if historical_value is not None or old is not None:
            raise ValueError('Historical MI/SM/RW warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english']:
            raise ValueError('MI/SM/RW warning source differs: '+tag+'/'+key)
        return row['target']
    if (tag,key) in CEB_NDS_CSB_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=ceb_nds_csb_shared_row(tag,key,fixture('cebuano_low_german_kashubian_priority_wording/'+tag+'.json'),historical_value=historical_value)
        if historical_value is not None or old is not None or 'previous_target' not in row or row['previous_target'] is not None:
            raise ValueError('CEB/NDS/CSB historical warning addition must be absent: '+tag+'/'+key)
        if row['source']!={'value':queue['keys'][key]['corrected_english'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
            raise ValueError('CEB/NDS/CSB warning source or attributes differ: '+tag+'/'+key)
        return row['reviewed_value']
    if (tag,key) in WA_SE_SA_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=wa_se_sa_shared_row(tag,key,fixture('walloon_northern_sami_sanskrit_priority_wording/'+tag+'.json'),historical_value=historical_value)
        if historical_value is not None or old is not None or 'previous_target' not in row or row['previous_target'] is not None:
            raise ValueError('WA/SE/SA historical warning addition must be absent: '+tag+'/'+key)
        if row['source']!={'value':queue['keys'][key]['corrected_english'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
            raise ValueError('WA/SE/SA warning source or attributes differ: '+tag+'/'+key)
        return row['reviewed_value']
    if (tag,key) in KN_ML_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=kn_ml_row(tag,key)
        if historical_value is not None or old is not None or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Historical Kannada/Malayalam warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english'] or row['attributes']!={'name':key}:
            raise ValueError('Kannada/Malayalam warning source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag,key) in AS_KM_LO_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=as_km_lo_row(tag,key)
        if historical_value is not None or old is not None or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Historical Assamese/Khmer/Lao warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english'] or row['attributes']!={'name':key}:
            raise ValueError('Assamese/Khmer/Lao warning source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag,key) in JV_SU_KY_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=jv_su_ky_row(tag,key)
        if historical_value is not None or old is not None or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Historical Javanese/Sundanese/Kyrgyz warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english'] or row['attributes']!={'name':key}:
            raise ValueError('Javanese/Sundanese/Kyrgyz warning source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag,key) in HA_IG_LN_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=ha_ig_ln_row(tag,key)
        if historical_value is not None or old is not None or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Historical Hausa/Igbo/Lingala warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english'] or row['attributes']!={'name':key}:
            raise ValueError('Hausa/Igbo/Lingala warning source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag,key) in YO_ZU_XH_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=yo_zu_xh_row(tag,key)
        if historical_value is not None or old is not None or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Historical Yoruba/Zulu/Xhosa warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english'] or row['attributes']!={'name':key}:
            raise ValueError('Yoruba/Zulu/Xhosa warning source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag,key) in SO_WO_HT_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=so_wo_ht_row(tag,key)
        return require_so_wo_ht_addition(tag,key,queue['keys'][key]['corrected_english'],
            historical_value=historical_value,already_present=old is not None,row=row)
    if (tag,key) in NE_PA_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=ne_pa_row(tag,key)
        if historical_value is not None or old is not None or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Historical Nepali/Punjabi warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english'] or row['attributes']!={'name':key}:
            raise ValueError('Nepali/Punjabi warning source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag,key) in MR_TA_TE_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        row=mr_ta_te_row(tag,key)
        if historical_value is not None or old is not None or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Historical Marathi/Tamil/Telugu warning addition must be absent: '+tag+'/'+key)
        if row['source']!=queue['keys'][key]['corrected_english'] or row['attributes']!={'name':key}:
            raise ValueError('Marathi/Tamil/Telugu warning source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag,key) in BR_AST_OC_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        if old is not None:raise ValueError('Historical BR/AST/OC queue value must be absent')
        return br_ast_oc_addition(tag,key,queue['keys'][key]['corrected_english'],historical_value)
    if (tag,key) in IA_LA_KU_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        if old is not None:raise ValueError('Historical IA/LA/KU queue value must be absent')
        return ia_la_ku_addition(tag,key,queue['keys'][key]['corrected_english'],historical_value)
    if (tag,key) in KAB_MWW_MAI_ADDITIONS:
        queue=review_record()
        old=next(o for o in queue['options'] if o['tag']==tag)['terms'][key]['value']
        if old is not None:raise ValueError('Historical KAB/MWW/MAI queue value must be absent')
        return kab_mww_mai_addition(tag,key,queue['keys'][key]['corrected_english'],historical_value)
    if (tag, key) in SK_SL_CA_ADDITIONS:
        queue = review_record()
        old = next(o for o in queue['options'] if o['tag'] == tag)['terms'][key]['value']
        row = fixture('slovak_slovenian_catalan_priority_wording.json')['locales'][tag]['values'][key]
        if historical_value is not None or old is not None or row['previous_target'] is not None:
            raise ValueError('Historical priority addition must be absent: '+tag+'/'+key)
        if row['source'] != queue['keys'][key]['corrected_english'] or row['attributes'] != {'name':key}:
            raise ValueError('Priority addition source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag, key) in PRIORITY_ADDITIONS:
        queue = review_record()
        old = next(o for o in queue['options'] if o['tag'] == tag)['terms'][key]['value']
        row = fixture('ukrainian_lithuanian_romanian_priority_wording.json')['locales'][tag]['values'][key]
        if historical_value is not None or old is not None or row['previous_target'] is not None:
            raise ValueError('Historical priority addition must be absent: '+tag+'/'+key)
        if row['source'] != queue['keys'][key]['corrected_english'] or row['attributes'] != {'name':key}:
            raise ValueError('Priority addition source or attributes differ: '+tag+'/'+key)
        return row['target']
    if (tag, key) in SINGLE_KEY_EXPECTATIONS:
        # Explicit P0-only reviews. The paired oracle and missing P1
        # companion retain their separate scope and frozen historical absence.
        queue = review_record()
        old = next(o for o in queue['options'] if o['tag'] == tag)['terms'][key]['value']
        if historical_value is not None or old is not None:
            raise ValueError('Historical single-key warning was absent: ' + tag + '/' + key)
        data = fixture(SINGLE_KEY_FIXTURES[tag])
        if data['values'][key]['default'] != queue['keys'][key]['corrected_english']:
            raise ValueError('Single-key warning source differs: ' + key)
        return data['values'][key][tag]
    if tag in PRIORITY_TAGS:
        # These four newly translated values have qualified priority review,
        # not entries in the separately accepted-warning inventory. Keep the
        # initial queue's absence intact and reject a forged historical pair.
        if historical_value is not None:
            raise ValueError('Historical priority warning was absent: ' + tag + '/' + key)
        data = fixture('bulgarian_bengali_priority_wording.json')
        if data['values'][key]['default'] != review_record()['keys'][key]['corrected_english']:
            raise ValueError('Priority warning source differs: ' + key)
        return data['values'][key][tag]
    if tag != 'default':
        return current_warning_expectation(key, tag, historical_value)
    correction = review_record()['keys'][key]
    if historical_value != correction['old_english']:
        raise ValueError('Historical English binding differs: ' + key)
    return correction['corrected_english']
