from sinhala_burmese_zhuang_priority_expectations import ADDITION_TAGS as SI_MY_TAGS, current_row as si_my_row, display as si_my_display
from persian_hebrew_urdu_priority_expectations import TAGS as FA_HE_UR_TAGS, require_addition as fa_he_ur_row, display as fa_he_ur_display
from nynorsk_belarusian_albanian_priority_expectations import TAGS as NN_BE_SQ_TAGS, COLOUR_TAGS as NN_BE_SQ_COLOUR_TAGS, require_addition as nn_be_sq_row, display as nn_be_sq_display
from thai_priority_expectations import TAGS as THAI_TAGS, current_row as thai_row, display as thai_display
from hindi_gujarati_priority_expectations import TAGS as HI_GU_TAGS, current_row as hi_gu_row, display as hi_gu_display
"""Current wording, syntax, fallback and Unicode contracts, not linguistic certification."""
from nordic_priority_expectations import TAGS as NORDIC_TAGS, current_row as nordic_row, display as nordic_display
NORDIC_COLOUR_TAGS = {"is"}
from pathlib import Path
import hr_bs_mk_priority_expectations as hr_bs_mk
import serbian_priority_delta_expectations as serbian_delta
import json
from exact_script_priority_expectations import require_addition as exact_script_addition, bound_fixture as exact_script_fixture
EXACT_SCRIPT_ADDITION_TAGS={"tt-Latn"}
from sindhi_nigerian_pidgin_tok_pisin_priority_expectations import require_shared_row as sd_pcm_tpi_shared_row
from sorani_uyghur_tatar_priority_expectations import require_shared_row as ckb_ug_tt_shared_row
from moroccan_arabic_mongolian_toki_pona_priority_expectations import ADDITION_TAGS as ARY_MN_TOK_TAGS, require_addition as ary_mn_tok_addition, display as ary_mn_tok_display
from kazakh_tajik_pashto_priority_expectations import require_shared_row as kk_tg_ps_shared_row
from basque_frisian_uzbek_priority_expectations import require_shared_row
import re
import unittest
import unicodedata
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape, require_locale_scope
import translation_catalogues as catalogues
from galician_priority_expectations import TAGS as GL_TAGS, current_row as gl_row, display as gl_display
from cebuano_low_german_kashubian_priority_expectations import require_shared_row as ceb_nds_csb_shared_row, decode_android
from maori_samoan_kinyarwanda_priority_expectations import TAGS as MI_SM_RW_TAGS, current_row as mi_sm_rw_row, display as mi_sm_rw_display
from walloon_northern_sami_sanskrit_priority_expectations import require_shared_row as wa_se_sa_shared_row, decode_android
from tibetan_dzongkha_valencian_priority_expectations import require_shared_row as bo_dz_val_shared_row, decode_android
from chhattisgarhi_yiddish_hong_kong_priority_expectations import require_shared_row as hne_yi_hk_shared_row, decode_android
from test_translations import SCOPED_TAGS
from language_option_additions import ADDED_TAGS
from irish_gaelic_welsh_priority_expectations import TAGS as GA_GD_CY_TAGS, current_row as ga_gd_cy_row, display as ga_gd_cy_display
from somali_wolof_haitian_creole_priority_expectations import TAGS as SO_WO_HT_TAGS, current_row as so_wo_ht_row, display as so_wo_ht_display, require_addition as require_so_wo_ht_addition, display_row as so_wo_ht_display_row
from breton_asturian_occitan_priority_expectations import TAGS as BR_AST_OC_TAGS, require_addition as br_ast_oc_addition, display as br_ast_oc_display
from interlingua_latin_kurdish_priority_expectations import TAGS as IA_LA_KU_TAGS, require_addition as ia_la_ku_addition, display as ia_la_ku_display
from kabyle_hmong_daw_maithili_priority_expectations import TAGS as KAB_MWW_MAI_TAGS, require_addition as kab_mww_mai_addition, display as kab_mww_mai_display
from yoruba_zulu_xhosa_priority_expectations import TAGS as YO_ZU_XH_TAGS, current_row as yo_zu_xh_row, display as yo_zu_xh_display
from hausa_igbo_lingala_priority_expectations import TAGS as HA_IG_LN_TAGS, current_row as ha_ig_ln_row, display as ha_ig_ln_display
from javanese_sundanese_kyrgyz_priority_expectations import TAGS as JV_SU_KY_TAGS, current_row as jv_su_ky_row, display as jv_su_ky_display
from assamese_khmer_lao_priority_expectations import TAGS as AS_KM_LO_TAGS, current_row as as_km_lo_row, display as as_km_lo_display
from nepali_punjabi_priority_expectations import TAGS as NE_PA_TAGS, current_row as ne_pa_row, display as ne_pa_display
from kannada_malayalam_filipino_priority_expectations import ADDITION_TAGS as KN_ML_TAGS, current_row as kn_ml_row, display as kn_ml_display
from marathi_tamil_telugu_priority_expectations import TAGS as MR_TA_TE_TAGS, current_row as mr_ta_te_row, display as mr_ta_te_display

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = ('commons_metadata_current_wording.json', 'commons_copy_credit_current_wording.json',
            'commons_svg_current_wording.json', 'hungarian_attribution_current_wording.json')

EXPECTED_KEYS = {
    FAMILIES[0]: {'commons_metadata_http_error','commons_metadata_response_too_large','commons_metadata_query_failed'},
    FAMILIES[1]: {'commons_credit_copy_failed','commons_credit_copy_failed_reason','commons_credit_copy_out_of_memory'},
    FAMILIES[2]: {'commons_svg_original_size_unavailable','commons_svg_original_size_too_large'},
    FAMILIES[3]: {'gallery_copy_credit','gallery_description','gallery_edit_credits','gallery_credit_copied',
        'gallery_credit_saved','ui_image_credits','ui_about_credits23','ui_credits_terms','ui_icons_fonts_artwork_credits',
        'ui_open_source_credits_and_notices','ui_gimp_translations31','ui_catrobat_s_own_artwork_uses_cc_by_sa',
        'ui_irasutoya_help34','ui_openclipart_help34','ui_help23','ui_add_up_to_20_images_with_android_s',
        'ui_the_arrow_on_the_left_directly_below_the'},
}


# Additions are message-family-specific. Czech and Swedish have independently reviewed metadata/copy-credit values.
KA_HY_AZ_TAGS = {'ka', 'hy', 'az'}
CEB_NDS_CSB_TAGS = {'csb', 'nds'}
WA_SE_SA_TAGS = {'se', 'sa', 'wa'}
BO_DZ_VAL_TAGS = {'ca-ES-valencia'}
HNE_YI_HK_TAGS = {'yi', 'hne'}
EU_FY_UZ_TAGS = {'eu-ES','fy','uz-Latn'}
KK_TG_PS_TAGS = {'kk','tg','ps'}
SD_PCM_TPI_TAGS = {'sd','pcm','tpi'}
CKB_UG_TT_TAGS = {'ckb','ug','tt-Cyrl'}
FAMILY_EXTRA_TAGS = {FAMILIES[0]: {'cs', 'sv'}, FAMILIES[1]: {'cs', 'sv'}, FAMILIES[2]: {'am', 'cs', 'pl', 'sv', 'bg', 'bn', 'uk', 'ro', 'sk', 'sl', 'ca'} | MR_TA_TE_TAGS | KN_ML_TAGS | NORDIC_TAGS | NN_BE_SQ_TAGS | FA_HE_UR_TAGS | HI_GU_TAGS | THAI_TAGS | SI_MY_TAGS | NE_PA_TAGS | YO_ZU_XH_TAGS | HA_IG_LN_TAGS | JV_SU_KY_TAGS | AS_KM_LO_TAGS | EU_FY_UZ_TAGS | set(SO_WO_HT_TAGS) | set(KK_TG_PS_TAGS) | set(CEB_NDS_CSB_TAGS) | set(WA_SE_SA_TAGS) | set(KA_HY_AZ_TAGS) | set(BR_AST_OC_TAGS) | set(IA_LA_KU_TAGS) | set(KAB_MWW_MAI_TAGS) | set(SD_PCM_TPI_TAGS) | set(CKB_UG_TT_TAGS) | set(ARY_MN_TOK_TAGS) | set(HNE_YI_HK_TAGS) | BO_DZ_VAL_TAGS | EXACT_SCRIPT_ADDITION_TAGS}

FAMILY_EXTRA_TAGS[FAMILIES[2]] |= set(GA_GD_CY_TAGS) | set(hr_bs_mk.TAGS) | set(serbian_delta.TAGS)

FAMILY_EXTRA_TAGS[FAMILIES[2]] |= set(GL_TAGS)

FAMILY_EXTRA_TAGS[FAMILIES[2]] |= set(MI_SM_RW_TAGS)


def wording_tags(name):
    return {'hu'} if name == FAMILIES[3] else {'default'} | SCOPED_TAGS | FAMILY_EXTRA_TAGS.get(name, set())


def wording_fixture(name):
    data=fixture(name)
    if name == FAMILIES[2]:
        for key in EXPECTED_KEYS[name]:
            row=exact_script_addition('tt-Latn',key,None,data['values'][key]['default'],already_present='tt-Latn' in data['values'][key])
            data['values'][key]['tt-Latn']=row['reviewed_value']
        data['additional_reviewed_tags'].append('tt-Latn')
        data['additional_locale_review_status']['tt-Latn']='independent_model_static_own_script_review; no cross-script/native/runtime certification'
        current=fixture('ukrainian_lithuanian_romanian_priority_wording.json')['locales']
        for tag in ('uk','ro'):
            for key in EXPECTED_KEYS[name]:
                row=current[tag]['values'][key]
                if row['previous_target'] is not None or row['source'] != data['values'][key]['default']:
                    raise ValueError('SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        current=fixture('slovak_slovenian_catalan_priority_wording.json')['locales']
        for tag in ('sk','sl','ca'):
            for key in EXPECTED_KEYS[name]:
                row=current[tag]['values'][key]
                if (tag in data['values'][key] or row['previous_target'] is not None
                        or row['source'] != data['values'][key]['default'] or row['attributes'] != {'name':key}):
                    raise ValueError('SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(GA_GD_CY_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=ga_gd_cy_row(tag,key)
                if tag in data['values'][key] or row['source']!=data['values'][key]['default']:
                    raise ValueError('GA/GD/CY SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(GL_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=gl_row(tag,key)
                if tag in data['values'][key] or row['source']!=data['values'][key]['default']:
                    raise ValueError('Galician SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(MI_SM_RW_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=mi_sm_rw_row(tag,key)
                if tag in data['values'][key] or row['source']!=data['values'][key]['default']:
                    raise ValueError('MI/SM/RW SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(MR_TA_TE_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=mr_ta_te_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Marathi/Tamil/Telugu SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(KN_ML_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=kn_ml_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Kannada/Malayalam SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(THAI_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=thai_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Thai replacement SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(SI_MY_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=si_my_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Sinhala/Burmese replacement SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(HI_GU_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=hi_gu_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Hindi/Gujarati SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(NORDIC_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=nordic_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Nordic SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(NN_BE_SQ_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=nn_be_sq_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('NN/BE/SQ SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(FA_HE_UR_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=fa_he_ur_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('FA/HE/UR SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(NE_PA_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=ne_pa_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Nepali/Punjabi SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(AS_KM_LO_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=as_km_lo_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Assamese/Khmer/Lao SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(JV_SU_KY_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=jv_su_ky_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Javanese/Sundanese/Kyrgyz SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(HA_IG_LN_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=ha_ig_ln_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Hausa/Igbo/Lingala SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(YO_ZU_XH_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=yo_zu_xh_row(tag,key)
                if (tag in data['values'][key] or row['previous_target'] is not None or not row['changed']
                        or row['source']!=data['values'][key]['default'] or row['attributes']!={'name':key}):
                    raise ValueError('Yoruba/Zulu/Xhosa SVG addition binding differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        current=fixture('georgian_armenian_azerbaijani_priority_wording.json')
        for tag in ('ka','hy','az'):
            for key in EXPECTED_KEYS[name]:
                row=current['locales'][tag]['values'][key]
                if (tag in data['values'][key] or row['previous'] is not None
                        or current['sources'][key]['value'] != data['values'][key]['default'] or row['attributes'] != {'name':key}):
                    raise ValueError('KA/HY/AZ SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['target']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(SO_WO_HT_TAGS):
            for key in EXPECTED_KEYS[name]:
                row=so_wo_ht_row(tag,key)
                data['values'][key][tag]=require_so_wo_ht_addition(tag,key,data['values'][key]['default'],
                    already_present=tag in data['values'][key],row=row)
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(BR_AST_OC_TAGS):
            for key in EXPECTED_KEYS[name]:
                data['values'][key][tag]=br_ast_oc_addition(tag,key,data['values'][key]['default'],already_present=tag in data['values'][key])
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(IA_LA_KU_TAGS):
            for key in EXPECTED_KEYS[name]:
                data['values'][key][tag]=ia_la_ku_addition(tag,key,data['values'][key]['default'],already_present=tag in data['values'][key])
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(KAB_MWW_MAI_TAGS):
            for key in EXPECTED_KEYS[name]:
                data['values'][key][tag]=kab_mww_mai_addition(tag,key,data['values'][key]['default'],already_present=tag in data['values'][key])
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
        for tag in sorted(ARY_MN_TOK_TAGS):
            for key in EXPECTED_KEYS[name]:
                data['values'][key][tag]=ary_mn_tok_addition(tag,key,data['values'][key]['default'],already_present=tag in data['values'][key])
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in ('eu-ES','fy','uz-Latn'):
            current=fixture('basque_frisian_uzbek_priority_wording/'+tag+'.json')
            for key in EXPECTED_KEYS[name]:
                row=require_shared_row(tag,key,current,already_present=tag in data['values'][key])
                if tag in data['values'][key] or 'previous_target' not in row or row['previous_target'] is not None or row['source']!={'value':data['values'][key]['default'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
                    raise ValueError('EU/FY/UZ SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['reviewed_value']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in ('kk','tg','ps'):
            current=fixture('kazakh_tajik_pashto_priority_wording/'+tag+'.json')
            for key in EXPECTED_KEYS[name]:
                row=kk_tg_ps_shared_row(tag,key,current,already_present=tag in data['values'][key])
                if tag in data['values'][key] or 'previous_target' not in row or row['previous_target'] is not None or row['source']!={'value':data['values'][key]['default'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
                    raise ValueError('KK/TG/PS SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['reviewed_value']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in ('nds', 'csb'):
            current=fixture('cebuano_low_german_kashubian_priority_wording/'+tag+'.json')
            for key in EXPECTED_KEYS[name]:
                row=ceb_nds_csb_shared_row(tag,key,current,already_present=tag in data['values'][key])
                if tag in data['values'][key] or 'previous_target' not in row or row['previous_target'] is not None or row['source']!={'value':data['values'][key]['default'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
                    raise ValueError('CEB/NDS/CSB SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['reviewed_value']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in ('wa', 'se', 'sa'):
            current=fixture('walloon_northern_sami_sanskrit_priority_wording/'+tag+'.json')
            for key in EXPECTED_KEYS[name]:
                row=wa_se_sa_shared_row(tag,key,current,already_present=tag in data['values'][key])
                if tag in data['values'][key] or 'previous_target' not in row or row['previous_target'] is not None or row['source']!={'value':data['values'][key]['default'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
                    raise ValueError('WA/SE/SA SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['reviewed_value']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in ('sd','pcm','tpi'):
            current=fixture('sindhi_nigerian_pidgin_tok_pisin_priority_wording/'+tag+'.json')
            for key in EXPECTED_KEYS[name]:
                row=sd_pcm_tpi_shared_row(tag,key,current,already_present=tag in data['values'][key])
                if tag in data['values'][key] or 'previous_target' not in row or row['previous_target'] is not None or row['source']!={'value':data['values'][key]['default'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
                    raise ValueError('SD/PCM/TPI SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['reviewed_value']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in ('ckb','ug','tt-Cyrl'):
            current=fixture('sorani_uyghur_tatar_priority_wording/'+tag+'.json')
            for key in EXPECTED_KEYS[name]:
                row=ckb_ug_tt_shared_row(tag,key,current,already_present=tag in data['values'][key])
                if tag in data['values'][key] or 'previous_target' not in row or row['previous_target'] is not None or row['source']!={'value':data['values'][key]['default'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
                    raise ValueError('CKB/UG/TT SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['reviewed_value']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in ('ca-ES-valencia',):
            current=fixture('tibetan_dzongkha_valencian_priority_wording/'+tag+'.json')
            for key in EXPECTED_KEYS[name]:
                row=bo_dz_val_shared_row(tag,key,current,already_present=tag in data['values'][key])
                if tag in data['values'][key] or 'previous_target' not in row or row['previous_target'] is not None or row['source']!={'value':data['values'][key]['default'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
                    raise ValueError('BO/DZ/Valencian SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['reviewed_value']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in ('hne', 'yi'):
            current=fixture('chhattisgarhi_yiddish_hong_kong_priority_wording/'+tag+'.json')
            for key in EXPECTED_KEYS[name]:
                row=hne_yi_hk_shared_row(tag,key,current,already_present=tag in data['values'][key])
                if tag in data['values'][key] or 'previous_target' not in row or row['previous_target'] is not None or row['source']!={'value':data['values'][key]['default'],'attributes':{'name':key}} or row['reviewed_attributes']!={'name':key}:
                    raise ValueError('HNE/YI/HK SVG addition precondition differs: '+tag+'/'+key)
                data['values'][key][tag]=row['reviewed_value']
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in sorted(hr_bs_mk.TAGS):
            for key in EXPECTED_KEYS[name]:
                if tag in data['values'][key]:raise ValueError('HR/BS/MK SVG must be a new addition')
                data['values'][key][tag]=hr_bs_mk.addition(tag,key,data['values'][key]['default'],None)
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_priority_review; no native-human or runtime/layout certification'
    if name == FAMILIES[2]:
        for tag in sorted(serbian_delta.TAGS):
            for key in EXPECTED_KEYS[name]:
                if tag in data['values'][key]:raise ValueError('Serbian SVG must be a new addition')
                data['values'][key][tag]=serbian_delta.addition(tag,key,data['values'][key]['default'],None)
            data['additional_reviewed_tags'].append(tag)
            data['additional_locale_review_status'][tag]='independent_model_static_delta_review; not full-P1 or native-human/runtime/layout certification'
    return require_wording_shape(data, EXPECTED_KEYS[name], wording_tags(name))


TAGGED_COLOUR_KEY = 'save20_unsupported_image_colour'
TAGGED_COLOUR_EXTRA_TAGS = {'mk', 'am', 'cs', 'pl', 'sv', 'bg', 'bn', 'nn', 'da', 'no', 'ca', 'ro', 'sk', 'sl', 'sr-Cyrl', 'sr-Latn', 'hr', 'bs', 'uk'} | MR_TA_TE_TAGS | KN_ML_TAGS | NORDIC_TAGS | NN_BE_SQ_TAGS | FA_HE_UR_TAGS | HI_GU_TAGS | THAI_TAGS | SI_MY_TAGS | NE_PA_TAGS | YO_ZU_XH_TAGS | HA_IG_LN_TAGS | JV_SU_KY_TAGS | AS_KM_LO_TAGS | EU_FY_UZ_TAGS
TAGGED_COLOUR_EXTRA_TAGS |= set(GA_GD_CY_TAGS) | set(KK_TG_PS_TAGS) | set(KA_HY_AZ_TAGS) | set(BR_AST_OC_TAGS) | set(IA_LA_KU_TAGS) | set(KAB_MWW_MAI_TAGS) | set(SD_PCM_TPI_TAGS) | set(CKB_UG_TT_TAGS) | set(ARY_MN_TOK_TAGS) | set(HNE_YI_HK_TAGS) | BO_DZ_VAL_TAGS | EXACT_SCRIPT_ADDITION_TAGS | set(SO_WO_HT_TAGS) | set(CEB_NDS_CSB_TAGS) | set(WA_SE_SA_TAGS)
TAGGED_COLOUR_EXTRA_TAGS |= set(GL_TAGS)
TAGGED_COLOUR_EXTRA_TAGS |= set(MI_SM_RW_TAGS)
# Explicit runtime parent inheritance, not an additional reviewed catalogue.
TAGGED_COLOUR_INHERITED_CATALOGUES = {'ca-ES-valencia': 'ca', 'fa-IR': 'fa'}


def current_tagged_colour_data():
    data=json.loads((ROOT / 'Paintroid/src/test/resources/tagged-colour/expected.json').read_text())
    row=fixture('ukrainian_lithuanian_romanian_priority_wording.json')['locales']['uk']['values'][TAGGED_COLOUR_KEY]
    if 'uk' in data or row['previous_target'] is not None:
        raise ValueError('Ukrainian tagged-colour addition must be absent in prior fixture')
    data['uk']=row['display']
    for tag in sorted(GA_GD_CY_TAGS):
        if tag in data:raise ValueError('GA/GD/CY tagged-colour addition must be absent: '+tag)
        data[tag]=ga_gd_cy_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(GL_TAGS):
        if tag in data:raise ValueError('Galician tagged-colour addition must be absent: '+tag)
        data[tag]=gl_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(MI_SM_RW_TAGS):
        if tag in data:raise ValueError('MI/SM/RW tagged-colour addition must be absent: '+tag)
        data[tag]=mi_sm_rw_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(MR_TA_TE_TAGS):
        row=mr_ta_te_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Marathi/Tamil/Telugu tagged colour predecessor differs: '+tag)
        data[tag]=mr_ta_te_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(KN_ML_TAGS):
        row=kn_ml_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Kannada/Malayalam tagged colour predecessor differs: '+tag)
        data[tag]=kn_ml_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(THAI_TAGS):
        row=thai_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Thai replacement tagged colour predecessor differs: '+tag)
        data[tag]=thai_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(SI_MY_TAGS):
        row=si_my_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Sinhala/Burmese replacement tagged colour predecessor differs: '+tag)
        data[tag]=si_my_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(HI_GU_TAGS):
        row=hi_gu_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Hindi/Gujarati tagged colour predecessor differs: '+tag)
        data[tag]=hi_gu_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(NORDIC_COLOUR_TAGS):
        row=nordic_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Nordic tagged colour predecessor differs: '+tag)
        data[tag]=nordic_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(NN_BE_SQ_COLOUR_TAGS):
        row=nn_be_sq_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('NN/BE/SQ tagged-colour predecessor differs: '+tag)
        data[tag]=nn_be_sq_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(FA_HE_UR_TAGS):
        row=fa_he_ur_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('FA/HE/UR tagged-colour predecessor differs: '+tag)
        data[tag]=fa_he_ur_display(tag,TAGGED_COLOUR_KEY)

    for tag in sorted(NE_PA_TAGS):
        row=ne_pa_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Nepali/Punjabi tagged colour predecessor differs: '+tag)
        data[tag]=ne_pa_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(AS_KM_LO_TAGS):
        row=as_km_lo_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Assamese/Khmer/Lao tagged colour predecessor differs: '+tag)
        data[tag]=as_km_lo_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(JV_SU_KY_TAGS):
        row=jv_su_ky_row(tag,TAGGED_COLOUR_KEY)
        if tag in data or row['previous_target'] is not None or not row['changed']:
            raise ValueError('Javanese/Sundanese/Kyrgyz tagged colour predecessor differs: '+tag)
        data[tag]=jv_su_ky_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(HA_IG_LN_TAGS):
        row=ha_ig_ln_row(tag,TAGGED_COLOUR_KEY)
        if (tag in data or row['previous_target'] is not None or not row['changed']
                or row['source'] != ET.parse(catalogues.RES / 'values/strings.xml').find("./string[@name='"+TAGGED_COLOUR_KEY+"']").text or row['attributes'] != {'name':TAGGED_COLOUR_KEY}):
            raise ValueError('Hausa/Igbo/Lingala tagged colour predecessor/source/attributes differ: '+tag)
        data[tag]=ha_ig_ln_display(tag,TAGGED_COLOUR_KEY)
    for tag in sorted(YO_ZU_XH_TAGS):
        row=yo_zu_xh_row(tag,TAGGED_COLOUR_KEY)
        if (tag in data or row['previous_target'] is not None or not row['changed']
                or row['source'] != ET.parse(catalogues.RES / 'values/strings.xml').find("./string[@name='"+TAGGED_COLOUR_KEY+"']").text or row['attributes'] != {'name':TAGGED_COLOUR_KEY}):
            raise ValueError('Yoruba/Zulu/Xhosa tagged colour predecessor/source/attributes differ: '+tag)
        data[tag]=yo_zu_xh_display(tag,TAGGED_COLOUR_KEY)
    reviewed={tag:fixture('basque_frisian_uzbek_priority_wording/'+tag+'.json') for tag in ('eu-ES','fy','uz-Latn')}
    add_eu_fy_uz_tagged_colour(data,reviewed)
    for tag in sorted(SO_WO_HT_TAGS):
        row=so_wo_ht_row(tag,TAGGED_COLOUR_KEY)
        source=ET.parse(catalogues.RES/'values/strings.xml').find("./string[@name='"+TAGGED_COLOUR_KEY+"']")
        if source.attrib!={'name':TAGGED_COLOUR_KEY}:raise ValueError('Actual tagged colour source attributes differ')
        require_so_wo_ht_addition(tag,TAGGED_COLOUR_KEY,source.text,already_present=tag in data,row=row)
        data[tag]=so_wo_ht_display_row(row)
    current=fixture('georgian_armenian_azerbaijani_priority_wording.json')
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[TAGGED_COLOUR_KEY]
    for tag in ('ka','hy','az'):
        row=current['locales'][tag]['values'][TAGGED_COLOUR_KEY]
        if (tag in data or row['previous'] is not None or row['attributes'] != {'name':TAGGED_COLOUR_KEY}
                or current['sources'][TAGGED_COLOUR_KEY]['value'] != english):
            raise ValueError('KA/HY/AZ tagged-colour addition precondition differs: '+tag)
        data[tag]=row['display']
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[TAGGED_COLOUR_KEY]
    for tag in sorted(BR_AST_OC_TAGS):
        br_ast_oc_addition(tag,TAGGED_COLOUR_KEY,english,already_present=tag in data)
        data[tag]=br_ast_oc_display(tag,TAGGED_COLOUR_KEY)
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[TAGGED_COLOUR_KEY]
    for tag in sorted(IA_LA_KU_TAGS):
        ia_la_ku_addition(tag,TAGGED_COLOUR_KEY,english,already_present=tag in data)
        data[tag]=ia_la_ku_display(tag,TAGGED_COLOUR_KEY)
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[TAGGED_COLOUR_KEY]
    for tag in sorted(KAB_MWW_MAI_TAGS):
        kab_mww_mai_addition(tag,TAGGED_COLOUR_KEY,english,already_present=tag in data)
        data[tag]=kab_mww_mai_display(tag,TAGGED_COLOUR_KEY)
    reviewed={tag:fixture('kazakh_tajik_pashto_priority_wording/'+tag+'.json') for tag in ('kk','tg','ps')}
    add_kk_tg_ps_tagged_colour(data,reviewed)
    reviewed={tag:fixture('cebuano_low_german_kashubian_priority_wording/'+tag+'.json') for tag in ('nds', 'csb')}
    add_ceb_nds_csb_tagged_colour(data,reviewed)
    reviewed={tag:fixture('walloon_northern_sami_sanskrit_priority_wording/'+tag+'.json') for tag in ('wa', 'se', 'sa')}
    add_wa_se_sa_tagged_colour(data,reviewed)
    reviewed={tag:fixture('sindhi_nigerian_pidgin_tok_pisin_priority_wording/'+tag+'.json') for tag in ('sd','pcm','tpi')}
    add_sd_pcm_tpi_tagged_colour(data,reviewed)
    reviewed={tag:fixture('sorani_uyghur_tatar_priority_wording/'+tag+'.json') for tag in ('ckb','ug','tt-Cyrl')}
    add_ckb_ug_tt_tagged_colour(data,reviewed)
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[TAGGED_COLOUR_KEY]
    for tag in sorted(ARY_MN_TOK_TAGS):
        ary_mn_tok_addition(tag,TAGGED_COLOUR_KEY,english,already_present=tag in data)
        data[tag]=ary_mn_tok_display(tag,TAGGED_COLOUR_KEY)
    reviewed={tag:fixture('tibetan_dzongkha_valencian_priority_wording/'+tag+'.json') for tag in ('ca-ES-valencia',)}
    add_bo_dz_val_tagged_colour(data,reviewed)
    reviewed={tag:fixture('chhattisgarhi_yiddish_hong_kong_priority_wording/'+tag+'.json') for tag in ('hne', 'yi')}
    add_hne_yi_hk_tagged_colour(data,reviewed)
    row=exact_script_addition('tt-Latn',TAGGED_COLOUR_KEY,None,english,already_present='tt-Latn' in data)
    data['tt-Latn']=row['compiled_display']
    if 'mk' in data:raise ValueError('Macedonian tagged-colour must be a new addition')
    hr_bs_mk.addition('mk',TAGGED_COLOUR_KEY,english,None)
    data['mk']=hr_bs_mk.current_display('mk',TAGGED_COLOUR_KEY)
    return data


def add_eu_fy_uz_tagged_colour(data,reviewed):
    """Finite new additions: never overwrite a predecessor or invent its absence."""
    key=TAGGED_COLOUR_KEY
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[key]
    for tag in ('eu-ES','fy','uz-Latn'):
        row=require_shared_row(tag,key,reviewed[tag],already_present=tag in data)
        raw=row['reviewed_value']
        if (tag in data or 'previous_target' not in row or row['previous_target'] is not None
                or row['type']!='string' or row['source']!={'value':english,'attributes':{'name':key}}
                or row['reviewed_attributes']!={'name':key} or not isinstance(raw,str)
                or not raw.startswith('"') or not raw.endswith('"') or chr(92) in raw[1:-1]
                or row['display']!=raw[1:-1]):
            raise ValueError('EU/FY/UZ tagged-colour source/attributes/display/predecessor differs: '+tag)
        data[tag]=row['display']
    return data


def add_ceb_nds_csb_tagged_colour(data,reviewed):
    """Finite new additions: never overwrite a predecessor or invent its absence."""
    key=TAGGED_COLOUR_KEY
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[key]
    for tag in ('nds', 'csb'):
        row=ceb_nds_csb_shared_row(tag,key,reviewed[tag],already_present=tag in data)
        raw=row['reviewed_value']
        if (tag in data or 'previous_target' not in row or row['previous_target'] is not None
                or row['type']!='string' or row['source']!={'value':english,'attributes':{'name':key}}
                or row['reviewed_attributes']!={'name':key} or not isinstance(raw,str)
                or row['display']!=decode_android(raw)):
            raise ValueError('CEB/NDS/CSB tagged-colour source/attributes/display/predecessor differs: '+tag)
        data[tag]=row['display']
    return data


def add_wa_se_sa_tagged_colour(data,reviewed):
    """Finite new additions: never overwrite a predecessor or invent its absence."""
    key=TAGGED_COLOUR_KEY
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[key]
    for tag in ('wa', 'se', 'sa'):
        row=wa_se_sa_shared_row(tag,key,reviewed[tag],already_present=tag in data)
        raw=row['reviewed_value']
        if (tag in data or 'previous_target' not in row or row['previous_target'] is not None
                or row['type']!='string' or row['source']!={'value':english,'attributes':{'name':key}}
                or row['reviewed_attributes']!={'name':key} or not isinstance(raw,str)
                or row['display']!=decode_android(raw)):
            raise ValueError('WA/SE/SA tagged-colour source/attributes/display/predecessor differs: '+tag)
        data[tag]=row['display']
    return data


def add_kk_tg_ps_tagged_colour(data,reviewed):
    """Finite new additions: never overwrite a predecessor or invent its absence."""
    key=TAGGED_COLOUR_KEY
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[key]
    for tag in ('kk','tg','ps'):
        row=kk_tg_ps_shared_row(tag,key,reviewed[tag],already_present=tag in data)
        raw=row['reviewed_value']
        if (tag in data or 'previous_target' not in row or row['previous_target'] is not None
                or row['type']!='string' or row['source']!={'value':english,'attributes':{'name':key}}
                or row['reviewed_attributes']!={'name':key} or not isinstance(raw,str)
                or not raw.startswith('"') or not raw.endswith('"') or chr(92) in raw[1:-1]
                or row['display']!=raw[1:-1]):
            raise ValueError('KK/TG/PS tagged-colour source/attributes/display/predecessor differs: '+tag)
        data[tag]=row['display']
    return data




def add_bo_dz_val_tagged_colour(data,reviewed):
    """Finite new additions: never overwrite a predecessor or invent its absence."""
    key=TAGGED_COLOUR_KEY
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[key]
    for tag in ('ca-ES-valencia',):
        row=bo_dz_val_shared_row(tag,key,reviewed[tag],already_present=tag in data)
        raw=row['reviewed_value']
        if (tag in data or 'previous_target' not in row or row['previous_target'] is not None
                or row['type']!='string' or row['source']!={'value':english,'attributes':{'name':key}}
                or row['reviewed_attributes']!={'name':key} or not isinstance(raw,str)
                or row['display']!=decode_android(raw)):
            raise ValueError('BO/DZ/Valencian tagged-colour source/attributes/display/predecessor differs: '+tag)
        data[tag]=row['display']
    return data


def add_hne_yi_hk_tagged_colour(data,reviewed):
    """Finite new additions: never overwrite a predecessor or invent its absence."""
    key=TAGGED_COLOUR_KEY
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[key]
    for tag in ('hne', 'yi'):
        row=hne_yi_hk_shared_row(tag,key,reviewed[tag],already_present=tag in data)
        raw=row['reviewed_value']
        if (tag in data or 'previous_target' not in row or row['previous_target'] is not None
                or row['type']!='string' or row['source']!={'value':english,'attributes':{'name':key}}
                or row['reviewed_attributes']!={'name':key} or not isinstance(raw,str)
                or row['display']!=decode_android(raw)):
            raise ValueError('HNE/YI/HK tagged-colour source/attributes/display/predecessor differs: '+tag)
        data[tag]=row['display']
    return data




def add_sd_pcm_tpi_tagged_colour(data,reviewed):
    """Finite new additions: never overwrite a predecessor or invent its absence."""
    key=TAGGED_COLOUR_KEY
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[key]
    for tag in ('sd','pcm','tpi'):
        row=sd_pcm_tpi_shared_row(tag,key,reviewed[tag],already_present=tag in data)
        raw=row['reviewed_value']
        if (tag in data or 'previous_target' not in row or row['previous_target'] is not None
                or row['type']!='string' or row['source']!={'value':english,'attributes':{'name':key}}
                or row['reviewed_attributes']!={'name':key} or not isinstance(raw,str)
                or raw.startswith('"') or raw.endswith('"') or chr(92) in raw
                or row['display']!=raw):
            raise ValueError('SD/PCM/TPI tagged-colour source/attributes/display/predecessor differs: '+tag)
        data[tag]=row['display']
    return data


def add_ckb_ug_tt_tagged_colour(data,reviewed):
    """Finite new additions: never overwrite a predecessor or invent its absence."""
    key=TAGGED_COLOUR_KEY
    english=catalogues.read_strings(catalogues.RES/'values/strings.xml')[key]
    for tag in ('ckb','ug','tt-Cyrl'):
        row=ckb_ug_tt_shared_row(tag,key,reviewed[tag],already_present=tag in data)
        raw=row['reviewed_value']
        if (tag in data or 'previous_target' not in row or row['previous_target'] is not None
                or row['type']!='string' or row['source']!={'value':english,'attributes':{'name':key}}
                or row['reviewed_attributes']!={'name':key} or not isinstance(raw,str)
                or raw.startswith('"') or raw.endswith('"') or chr(92) in raw
                or row['display']!=raw):
            raise ValueError('CKB/UG/TT tagged-colour source/attributes/display/predecessor differs: '+tag)
        data[tag]=row['display']
    return data


def tagged_colour_expectations(data):
    if set(data) != SCOPED_TAGS | TAGGED_COLOUR_EXTRA_TAGS:
        raise ValueError('Tagged-colour family locale inventory differs')
    if not all(isinstance(value, str) and value for value in data.values()):
        raise ValueError('Tagged-colour expectations must be complete nonempty strings')
    if data['mk'] != hr_bs_mk.current_display('mk',TAGGED_COLOUR_KEY):raise ValueError('Macedonian tagged-colour differs')
    for tag, name in [('cs', 'czech'), ('pl', 'polish'), ('sv', 'swedish')]:
        suffix = '_priority_current_wording.json' if tag == 'sv' else '_priority_draft_wording.json'
        reviewed = fixture(name + suffix)['values'][TAGGED_COLOUR_KEY][tag]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed complete pair: ' + tag)
    for tag in ('bg', 'bn'):
        reviewed = fixture('bulgarian_bengali_priority_wording.json')['values'][TAGGED_COLOUR_KEY][tag]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour priority expectation differs: ' + tag)
    reviewed_am = fixture('amharic_priority.json')['values'][TAGGED_COLOUR_KEY]['expected'][1:-1]
    if data['am'] != reviewed_am:
        raise ValueError('Tagged-colour expectation differs from reviewed Amharic value')
    reviewed_nn = fixture('nynorsk_p0_remaining_wording.json')['values'][TAGGED_COLOUR_KEY]['nn'][1:-1]
    if data['nn'] != reviewed_nn:
        raise ValueError('Tagged-colour expectation differs from reviewed Nynorsk value')
    for tag in ('da', 'no'):
        reviewed = fixture('danish_norwegian_p0_wording.json')['values'][TAGGED_COLOUR_KEY][tag][1:-1]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed DA/NO value: ' + tag)
    for tag in ('ca', 'ro'):
        reviewed = fixture('catalan_romanian_import_wording.json')['values'][TAGGED_COLOUR_KEY][tag][1:-1]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed CA/RO value: ' + tag)
    for tag in ('sk', 'sl'):
        reviewed = fixture('slovak_slovenian_p0_wording.json')['values'][TAGGED_COLOUR_KEY][tag]
        if reviewed.startswith('"') and reviewed.endswith('"'):
            reviewed = reviewed[1:-1]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed SK/SL value: ' + tag)
    for tag in ('sr-Cyrl', 'sr-Latn'):
        reviewed = fixture('serbian_p0_wording.json')['values'][TAGGED_COLOUR_KEY][tag]
        if reviewed.startswith('"') and reviewed.endswith('"'):
            reviewed = reviewed[1:-1]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed Serbian value: ' + tag)
    for tag in ('hr', 'bs'):
        reviewed = fixture('croatian_bosnian_p0_wording.json')['values'][TAGGED_COLOUR_KEY][tag]
        if reviewed.startswith('"') and reviewed.endswith('"'):
            reviewed = reviewed[1:-1]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour differs from reviewed Croatian/Bosnian value: ' + tag)
    for tag in GA_GD_CY_TAGS:
        if data[tag]!=ga_gd_cy_display(tag,TAGGED_COLOUR_KEY):raise ValueError('GA/GD/CY tagged-colour expectation differs: '+tag)
    for tag in GL_TAGS:
        if data[tag]!=gl_display(tag,TAGGED_COLOUR_KEY):raise ValueError('Galician tagged-colour expectation differs: '+tag)
    for tag in MI_SM_RW_TAGS:
        if data[tag]!=mi_sm_rw_display(tag,TAGGED_COLOUR_KEY):raise ValueError('MI/SM/RW tagged-colour expectation differs: '+tag)
    reviewed_uk = fixture('ukrainian_lithuanian_romanian_priority_wording.json')['locales']['uk']['values'][TAGGED_COLOUR_KEY]['display']
    if data['uk'] != reviewed_uk:
        raise ValueError('Tagged-colour differs from reviewed Ukrainian value')
    for tag in MR_TA_TE_TAGS:
        if data[tag]!=mr_ta_te_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Marathi/Tamil/Telugu value: '+tag)
    for tag in KN_ML_TAGS:
        if data[tag]!=kn_ml_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Kannada/Malayalam value: '+tag)
    for tag in THAI_TAGS:
        if data[tag]!=thai_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Thai replacement value: '+tag)
    for tag in SI_MY_TAGS:
        if data[tag]!=si_my_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Sinhala/Burmese replacement value: '+tag)
    for tag in HI_GU_TAGS:
        if data[tag]!=hi_gu_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Hindi/Gujarati value: '+tag)
    for tag in NORDIC_COLOUR_TAGS:
        if data[tag]!=nordic_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Nordic value: '+tag)
    for tag in NN_BE_SQ_COLOUR_TAGS:
        if data[tag]!=nn_be_sq_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete NN/BE/SQ value: '+tag)
    for tag in FA_HE_UR_TAGS:
        if data[tag]!=fa_he_ur_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete FA/HE/UR value: '+tag)
    for tag in NE_PA_TAGS:
        if data[tag]!=ne_pa_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Nepali/Punjabi value: '+tag)
    for tag in AS_KM_LO_TAGS:
        if data[tag]!=as_km_lo_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Assamese/Khmer/Lao value: '+tag)
    for tag in JV_SU_KY_TAGS:
        if data[tag]!=jv_su_ky_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Javanese/Sundanese/Kyrgyz value: '+tag)
    for tag in HA_IG_LN_TAGS:
        if data[tag]!=ha_ig_ln_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Hausa/Igbo/Lingala value: '+tag)
    for tag in YO_ZU_XH_TAGS:
        if data[tag]!=yo_zu_xh_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Yoruba/Zulu/Xhosa value: '+tag)
    for tag in ('ka','hy','az'):
        row=fixture('georgian_armenian_azerbaijani_priority_wording.json')['locales'][tag]['values'][TAGGED_COLOUR_KEY]
        if data[tag] != row['display']:
            raise ValueError('KA/HY/AZ tagged-colour expectation differs: '+tag)
    for tag in BR_AST_OC_TAGS:
        if data[tag]!=br_ast_oc_display(tag,TAGGED_COLOUR_KEY):raise ValueError('Tagged-colour differs from complete BR/AST/OC value: '+tag)
    for tag in IA_LA_KU_TAGS:
        if data[tag]!=ia_la_ku_display(tag,TAGGED_COLOUR_KEY):raise ValueError('Tagged-colour differs from complete IA/LA/KU value: '+tag)
    for tag in KAB_MWW_MAI_TAGS:
        if data[tag]!=kab_mww_mai_display(tag,TAGGED_COLOUR_KEY):raise ValueError('Tagged-colour differs from complete KAB/MWW/MAI value: '+tag)
    for tag in ('eu-ES','fy','uz-Latn'):
        reviewed=require_shared_row(tag,TAGGED_COLOUR_KEY,fixture('basque_frisian_uzbek_priority_wording/'+tag+'.json'))['display']
        if data[tag]!=reviewed:
            raise ValueError('Tagged-colour differs from reviewed EU/FY/UZ value: '+tag)
    for tag in SO_WO_HT_TAGS:
        if data[tag]!=so_wo_ht_display(tag,TAGGED_COLOUR_KEY):
            raise ValueError('Tagged-colour differs from complete Somali/Wolof/Haitian Creole value: '+tag)
    for tag in ('kk','tg','ps'):
        reviewed=kk_tg_ps_shared_row(tag,TAGGED_COLOUR_KEY,fixture('kazakh_tajik_pashto_priority_wording/'+tag+'.json'))['display']
        if data[tag]!=reviewed:
            raise ValueError('Tagged-colour differs from reviewed KK/TG/PS value: '+tag)
    for tag in ('nds', 'csb'):
        reviewed=ceb_nds_csb_shared_row(tag,TAGGED_COLOUR_KEY,fixture('cebuano_low_german_kashubian_priority_wording/'+tag+'.json'))['display']
        if data[tag]!=reviewed:
            raise ValueError('Tagged-colour differs from reviewed CEB/NDS/CSB value: '+tag)
    for tag in ('wa', 'se', 'sa'):
        reviewed=wa_se_sa_shared_row(tag,TAGGED_COLOUR_KEY,fixture('walloon_northern_sami_sanskrit_priority_wording/'+tag+'.json'))['display']
        if data[tag]!=reviewed:
            raise ValueError('Tagged-colour differs from reviewed WA/SE/SA value: '+tag)
    for tag in ('sd','pcm','tpi'):
        reviewed=sd_pcm_tpi_shared_row(tag,TAGGED_COLOUR_KEY,fixture('sindhi_nigerian_pidgin_tok_pisin_priority_wording/'+tag+'.json'))['display']
        if data[tag]!=reviewed:
            raise ValueError('Tagged-colour differs from reviewed SD/PCM/TPI value: '+tag)
    for tag in ('ckb','ug','tt-Cyrl'):
        reviewed=ckb_ug_tt_shared_row(tag,TAGGED_COLOUR_KEY,fixture('sorani_uyghur_tatar_priority_wording/'+tag+'.json'))['display']
        if data[tag]!=reviewed:
            raise ValueError('Tagged-colour differs from reviewed CKB/UG/TT value: '+tag)
    for tag in ARY_MN_TOK_TAGS:
        if data[tag]!=ary_mn_tok_display(tag,TAGGED_COLOUR_KEY):raise ValueError('Tagged-colour differs from complete ARY/MN/TOK value: '+tag)
    for tag in ('ca-ES-valencia',):
        reviewed=bo_dz_val_shared_row(tag,TAGGED_COLOUR_KEY,fixture('tibetan_dzongkha_valencian_priority_wording/'+tag+'.json'))['display']
        if data[tag]!=reviewed:
            raise ValueError('Tagged-colour differs from reviewed BO/DZ/Valencian value: '+tag)
    for tag in ('hne', 'yi'):
        reviewed=hne_yi_hk_shared_row(tag,TAGGED_COLOUR_KEY,fixture('chhattisgarhi_yiddish_hong_kong_priority_wording/'+tag+'.json'))['display']
        if data[tag]!=reviewed:
            raise ValueError('Tagged-colour differs from reviewed HNE/YI/HK value: '+tag)
    for tag in ('tt-Latn',):
        if data[tag]!=exact_script_fixture(tag)['rows'][TAGGED_COLOUR_KEY]['compiled_display']:
            raise ValueError('Exact-script complete tagged value differs: '+tag)
    return data


def require_tagged_colour_resolution(data, strings, offered, english):
    """Model direct values and the one explicit parent fallback, checked by Android too."""
    data = tagged_colour_expectations(data)
    if TAGGED_COLOUR_INHERITED_CATALOGUES != {'ca-ES-valencia':'ca', 'fa-IR':'fa'}:
        raise ValueError('Finite tagged-colour parent mapping differs')
    if not (set(TAGGED_COLOUR_INHERITED_CATALOGUES) |
            set(TAGGED_COLOUR_INHERITED_CATALOGUES.values())) <= set(offered):
        raise ValueError('Tagged-colour inheritance uses an unoffered catalogue')
    for tag in offered:
        parent = None if tag in BO_DZ_VAL_TAGS else TAGGED_COLOUR_INHERITED_CATALOGUES.get(tag)
        if parent is not None and (tag in data or parent not in data or
                                   TAGGED_COLOUR_KEY in strings[tag]):
            raise ValueError('Explicit tagged-colour parent inheritance differs: ' + tag)
        catalogue = parent or tag
        expected = data[catalogue] if catalogue in data else english
        # Catalogue values retain Android apostrophe escapes; this family uses no other escapes.
        actual = strings[catalogue].get(TAGGED_COLOUR_KEY, english).replace("\\'", "'")
        if (catalogue in ('am', 'nn', 'da', 'no', 'ca', 'ro', 'sk', 'sl', 'sr-Cyrl', 'sr-Latn', 'hr', 'bs', 'uk', 'ga', 'gd', 'cy', 'eu-ES', 'fy', 'uz-Latn', 'ka', 'hy', 'az', 'gl', 'kk', 'tg', 'ps', 'br', 'ast', 'oc', 'nds', 'csb', 'ia', 'la', 'ku', 'mi', 'sm', 'rw', 'wa', 'se', 'sa', 'kab', 'mww', 'mai', 'sd', 'pcm', 'tpi', 'ckb', 'ug', 'tt-Cyrl', 'ary', 'mn-Cyrl-MN', 'tok', 'ca-ES-valencia', 'hne', 'yi', 'tt-Latn') or catalogue in SO_WO_HT_TAGS or catalogue in NORDIC_COLOUR_TAGS or catalogue in NN_BE_SQ_COLOUR_TAGS or catalogue in FA_HE_UR_TAGS or catalogue == 'mk' or catalogue in HI_GU_TAGS or catalogue in THAI_TAGS or catalogue in SI_MY_TAGS) and actual.startswith('"') and actual.endswith('"'):
            actual = actual[1:-1]  # Android removes the reviewed outer quoting.
        if actual != expected:
            raise ValueError('Tagged-colour message or explicit English fallback differs: ' + tag)


def paths():
    return {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}


class CurrentLocalizationContracts(unittest.TestCase):
    def test_message_family_keys_and_nonempty_locale_contracts_are_required(self):
        from copy import deepcopy
        for name in FAMILIES:
            original=wording_fixture(name)
            tags=wording_tags(name)
            for key in EXPECTED_KEYS[name]:
                for mutation in ('missing-key','empty-values','missing-locale','empty-text','missing-constraint'):
                    data=deepcopy(original)
                    if mutation=='missing-key': del data['values'][key]
                    if mutation=='empty-values': data['values'][key]={}
                    if mutation=='missing-locale': data['values'][key].pop(next(iter(tags)))
                    if mutation=='empty-text': data['values'][key][next(iter(tags))]=''
                    if mutation=='missing-constraint': del data['constraints'][key]
                    with self.subTest(name=name,key=key,mutation=mutation),self.assertRaises(ValueError):
                        require_wording_shape(data,EXPECTED_KEYS[name],tags)
            data=deepcopy(original);data['values']={}
            with self.assertRaises(ValueError): require_wording_shape(data,EXPECTED_KEYS[name],tags)

    def test_each_message_family_has_only_its_explicitly_reviewed_additions(self):
        svg = wording_fixture(FAMILIES[2])
        extra_tags = set(serbian_delta.TAGS) | set(hr_bs_mk.TAGS) | {'am', 'cs', 'pl', 'sv', 'bg', 'bn', 'uk', 'ro', 'sk', 'sl', 'ca'} | MR_TA_TE_TAGS | KN_ML_TAGS | NORDIC_TAGS | NN_BE_SQ_TAGS | FA_HE_UR_TAGS | HI_GU_TAGS | THAI_TAGS | SI_MY_TAGS | NE_PA_TAGS | YO_ZU_XH_TAGS | HA_IG_LN_TAGS | JV_SU_KY_TAGS | AS_KM_LO_TAGS | EU_FY_UZ_TAGS | set(GA_GD_CY_TAGS) | set(KA_HY_AZ_TAGS) | set(GL_TAGS) | set(SO_WO_HT_TAGS) | set(KK_TG_PS_TAGS) | set(BR_AST_OC_TAGS) | set(CEB_NDS_CSB_TAGS) | set(IA_LA_KU_TAGS) | set(MI_SM_RW_TAGS) | set(WA_SE_SA_TAGS) | set(KAB_MWW_MAI_TAGS) | set(SD_PCM_TPI_TAGS) | set(CKB_UG_TT_TAGS) | set(ARY_MN_TOK_TAGS) | set(HNE_YI_HK_TAGS) | BO_DZ_VAL_TAGS | EXACT_SCRIPT_ADDITION_TAGS
        self.assertEqual({'cs', 'pl'}, set(svg['additional_draft_tags']))
        self.assertEqual(set(serbian_delta.TAGS) | set(hr_bs_mk.TAGS) | {'am', 'sv', 'bg', 'bn', 'uk', 'ro', 'sk', 'sl', 'ca'} | MR_TA_TE_TAGS | KN_ML_TAGS | NORDIC_TAGS | NN_BE_SQ_TAGS | FA_HE_UR_TAGS | HI_GU_TAGS | THAI_TAGS | SI_MY_TAGS | NE_PA_TAGS | YO_ZU_XH_TAGS | HA_IG_LN_TAGS | JV_SU_KY_TAGS | AS_KM_LO_TAGS | EU_FY_UZ_TAGS | set(GA_GD_CY_TAGS) | set(KA_HY_AZ_TAGS) | set(GL_TAGS) | set(SO_WO_HT_TAGS) | set(KK_TG_PS_TAGS) | set(BR_AST_OC_TAGS) | set(CEB_NDS_CSB_TAGS) | set(IA_LA_KU_TAGS) | set(MI_SM_RW_TAGS) | set(WA_SE_SA_TAGS) | set(KAB_MWW_MAI_TAGS) | set(SD_PCM_TPI_TAGS) | set(CKB_UG_TT_TAGS) | set(ARY_MN_TOK_TAGS) | set(HNE_YI_HK_TAGS) | BO_DZ_VAL_TAGS | EXACT_SCRIPT_ADDITION_TAGS, set(svg['additional_reviewed_tags']))
        self.assertEqual(extra_tags, FAMILY_EXTRA_TAGS[FAMILIES[2]])
        self.assertEqual(extra_tags, set(svg['additional_locale_review_status']))
        self.assertTrue(extra_tags.isdisjoint(SCOPED_TAGS))
        for name in FAMILIES[:2]:
            self.assertTrue({'pl'}.isdisjoint(wording_tags(name)))
            self.assertEqual({'default'} | SCOPED_TAGS | {'cs', 'sv'}, wording_tags(name))
            self.assertEqual(['cs', 'sv'], wording_fixture(name)['additional_reviewed_tags'])
        self.assertEqual({'hu'}, wording_tags(FAMILIES[3]))
        self.assertEqual({'default'} | SCOPED_TAGS | extra_tags, wording_tags(FAMILIES[2]))
        amharic = fixture('amharic_priority.json')
        for key, values in svg['values'].items():
            self.assertEqual(amharic['values'][key]['expected'], values['am'])
        swedish = fixture('swedish_remaining_p1_wording.json')
        for key, values in svg['values'].items():
            self.assertEqual(swedish['values'][key]['sv'], values['sv'])
            for tag in ('bg', 'bn'):
                self.assertEqual(fixture('bulgarian_bengali_priority_wording.json')['values'][key][tag], values[tag])

    def test_combined_priority_colour_additions_are_disjoint_and_cover_the_final_union(self):
        cohorts = (NORDIC_COLOUR_TAGS, HI_GU_TAGS, NN_BE_SQ_COLOUR_TAGS, THAI_TAGS, {'mk'})
        additions = set().union(*cohorts)
        self.assertEqual({'is', 'hi', 'gu', 'be', 'sq', 'th', 'mk'}, additions)
        self.assertEqual(sum(map(len, cohorts)), len(additions))
        data = tagged_colour_expectations(current_tagged_colour_data())
        self.assertTrue(additions.issubset(data))
        historical = set(data) - set(SI_MY_TAGS)
        self.assertEqual(141 + len(additions), len(historical - FA_HE_UR_TAGS))
        self.assertEqual(151, len(historical))
        offered = set(catalogues.offered_tags())
        self.assertEqual(171, len(offered))
        self.assertEqual(20, len(offered - historical))
        self.assertTrue(set(SI_MY_TAGS).isdisjoint(historical))
        self.assertEqual(historical | set(SI_MY_TAGS), set(data))
        self.assertEqual(153, len(data))
        self.assertEqual(18, len(offered - set(data)))

    def test_tagged_colour_family_resolves_complete_extra_values_and_exact_english_fallbacks(self):
        data = current_tagged_colour_data()
        strings = {tag: catalogues.read_strings(path) for tag, path in paths().items()}
        offered = set(catalogues.offered_tags())
        english = strings['default'][TAGGED_COLOUR_KEY]
        self.assertEqual(77+len(set(GA_GD_CY_TAGS) | set(MR_TA_TE_TAGS) | set(KN_ML_TAGS) | NORDIC_COLOUR_TAGS | NN_BE_SQ_COLOUR_TAGS | FA_HE_UR_TAGS | {'mk'} | set(HI_GU_TAGS) | set(THAI_TAGS) | set(SI_MY_TAGS) | set(NE_PA_TAGS) | set(YO_ZU_XH_TAGS) | set(HA_IG_LN_TAGS) | set(JV_SU_KY_TAGS) | set(AS_KM_LO_TAGS) | set(EU_FY_UZ_TAGS) | set(KA_HY_AZ_TAGS) | set(GL_TAGS) | set(SO_WO_HT_TAGS) | set(KK_TG_PS_TAGS) | set(BR_AST_OC_TAGS) | set(CEB_NDS_CSB_TAGS) | set(IA_LA_KU_TAGS) | set(MI_SM_RW_TAGS) | set(WA_SE_SA_TAGS) | set(KAB_MWW_MAI_TAGS) | set(SD_PCM_TPI_TAGS) | set(CKB_UG_TT_TAGS) | set(ARY_MN_TOK_TAGS) | set(HNE_YI_HK_TAGS) | BO_DZ_VAL_TAGS | EXACT_SCRIPT_ADDITION_TAGS), len(data))
        self.assertEqual(94-len(set(GA_GD_CY_TAGS) | set(MR_TA_TE_TAGS) | set(KN_ML_TAGS) | NORDIC_COLOUR_TAGS | NN_BE_SQ_COLOUR_TAGS | FA_HE_UR_TAGS | {'mk'} | set(HI_GU_TAGS) | set(THAI_TAGS) | set(SI_MY_TAGS) | set(NE_PA_TAGS) | set(YO_ZU_XH_TAGS) | set(HA_IG_LN_TAGS) | set(JV_SU_KY_TAGS) | set(AS_KM_LO_TAGS) | set(EU_FY_UZ_TAGS) | set(KA_HY_AZ_TAGS) | set(GL_TAGS) | set(SO_WO_HT_TAGS) | set(KK_TG_PS_TAGS) | set(BR_AST_OC_TAGS) | set(CEB_NDS_CSB_TAGS) | set(IA_LA_KU_TAGS) | set(MI_SM_RW_TAGS) | set(WA_SE_SA_TAGS) | set(KAB_MWW_MAI_TAGS) | set(SD_PCM_TPI_TAGS) | set(CKB_UG_TT_TAGS) | set(ARY_MN_TOK_TAGS) | set(HNE_YI_HK_TAGS) | BO_DZ_VAL_TAGS | EXACT_SCRIPT_ADDITION_TAGS), len(offered - set(data)))  # Missing direct values, not all English at runtime.
        self.assertEqual({'ca-ES-valencia': 'ca', 'fa-IR': 'fa'}, TAGGED_COLOUR_INHERITED_CATALOGUES)
        self.assertEqual(93-len(set(GA_GD_CY_TAGS) | set(MR_TA_TE_TAGS) | set(KN_ML_TAGS) | NORDIC_COLOUR_TAGS | NN_BE_SQ_COLOUR_TAGS | FA_HE_UR_TAGS | {'mk'} | set(HI_GU_TAGS) | set(THAI_TAGS) | set(SI_MY_TAGS) | set(NE_PA_TAGS) | set(YO_ZU_XH_TAGS) | set(HA_IG_LN_TAGS) | set(JV_SU_KY_TAGS) | set(AS_KM_LO_TAGS) | set(EU_FY_UZ_TAGS) | set(KA_HY_AZ_TAGS) | set(GL_TAGS) | set(SO_WO_HT_TAGS) | set(KK_TG_PS_TAGS) | set(BR_AST_OC_TAGS) | set(CEB_NDS_CSB_TAGS) | set(IA_LA_KU_TAGS) | set(MI_SM_RW_TAGS) | set(WA_SE_SA_TAGS) | set(KAB_MWW_MAI_TAGS) | set(SD_PCM_TPI_TAGS) | set(CKB_UG_TT_TAGS) | set(ARY_MN_TOK_TAGS) | set(HNE_YI_HK_TAGS) | BO_DZ_VAL_TAGS | EXACT_SCRIPT_ADDITION_TAGS), len(offered - set(data) - (set(TAGGED_COLOUR_INHERITED_CATALOGUES)-BO_DZ_VAL_TAGS)))
        self.assertTrue(TAGGED_COLOUR_EXTRA_TAGS.isdisjoint(SCOPED_TAGS))
        require_tagged_colour_resolution(data, strings, offered, english)
        for tag in TAGGED_COLOUR_EXTRA_TAGS:
            self.assertNotEqual(english, data[tag])

    def test_tagged_colour_oracle_rejects_missing_localization_and_arbitrary_defaults(self):
        data = current_tagged_colour_data()
        strings = {tag: catalogues.read_strings(path) for tag, path in paths().items()}
        offered = set(catalogues.offered_tags())
        english = strings['default'][TAGGED_COLOUR_KEY]
        for tag in TAGGED_COLOUR_EXTRA_TAGS:
            for mutation in ('missing-resource', 'english-resource', 'arbitrary-resource',
                             'missing-oracle', 'english-oracle', 'arbitrary-oracle'):
                changed_data = dict(data)
                changed_strings = dict(strings)
                changed_strings[tag] = dict(strings[tag])
                if mutation == 'missing-resource': changed_strings[tag].pop(TAGGED_COLOUR_KEY)
                elif mutation == 'english-resource': changed_strings[tag][TAGGED_COLOUR_KEY] = english
                elif mutation == 'arbitrary-resource': changed_strings[tag][TAGGED_COLOUR_KEY] = 'arbitrary default'
                elif mutation == 'missing-oracle': changed_data.pop(tag)
                elif mutation == 'english-oracle': changed_data[tag] = english
                else: changed_data[tag] = 'arbitrary default'
                with self.subTest(tag=tag, mutation=mutation), self.assertRaises(ValueError):
                    require_tagged_colour_resolution(changed_data, changed_strings, offered, english)
        fallback = sorted(offered - set(data) - set(TAGGED_COLOUR_INHERITED_CATALOGUES))[0]
        changed_strings = dict(strings)
        changed_strings[fallback] = dict(strings[fallback])
        changed_strings[fallback][TAGGED_COLOUR_KEY] = english
        require_tagged_colour_resolution(data, changed_strings, offered, english)
        changed_strings[fallback][TAGGED_COLOUR_KEY] = 'arbitrary default'
        with self.assertRaises(ValueError):
            require_tagged_colour_resolution(data, changed_strings, offered, english)

    def test_tagged_colour_parent_inheritance_stays_separate_and_rejects_overrides(self):
        data = current_tagged_colour_data()
        strings = {tag: catalogues.read_strings(path) for tag, path in paths().items()}
        offered = set(catalogues.offered_tags())
        english = strings['default'][TAGGED_COLOUR_KEY]
        child, parent = 'ca-ES-valencia', 'ca'
        self.assertIn(child, data)
        reviewed = fixture("tibetan_dzongkha_valencian_priority_wording/ca-ES-valencia.json")
        self.assertNotIn(TAGGED_COLOUR_KEY, reviewed["original_catalogue"])
        bo_dz_val_shared_row(child,TAGGED_COLOUR_KEY,reviewed)
        self.assertEqual(data[child],decode_android(strings[child][TAGGED_COLOUR_KEY]))
        self.assertEqual(data[parent], fixture('catalan_romanian_import_wording.json')['values'][TAGGED_COLOUR_KEY][parent][1:-1])
        require_tagged_colour_resolution(data, strings, offered, english)
        for value in (english, 'arbitrary override', strings[parent][TAGGED_COLOUR_KEY]):
            changed = dict(strings)
            changed[child] = dict(strings[child], **{TAGGED_COLOUR_KEY: value})
            with self.subTest(override=value), self.assertRaises(ValueError):
                require_tagged_colour_resolution(data, changed, offered, english)
        for missing in (child, parent):
            with self.subTest(unoffered=missing), self.assertRaises(ValueError):
                require_tagged_colour_resolution(data, strings, offered - {missing}, english)
        changed_data = dict(data, **{child: data[parent]})
        with self.assertRaises(ValueError):
            require_tagged_colour_resolution(changed_data, strings, offered, english)

    def test_persian_regional_inheritance_is_not_direct_or_english_acceptance(self):
        from unittest.mock import patch
        data=current_tagged_colour_data()
        strings={tag:catalogues.read_strings(path) for tag,path in paths().items()}
        offered=set(catalogues.offered_tags());english=strings['default'][TAGGED_COLOUR_KEY]
        self.assertNotIn('fa-IR',data);self.assertNotIn(TAGGED_COLOUR_KEY,strings['fa-IR'])
        self.assertEqual(fa_he_ur_display('fa',TAGGED_COLOUR_KEY),data['fa'])
        require_tagged_colour_resolution(data,strings,offered,english)
        for override in (strings['fa'][TAGGED_COLOUR_KEY],english,'invented direct acceptance'):
            changed={**strings,'fa-IR':{**strings['fa-IR'],TAGGED_COLOUR_KEY:override}}
            with self.assertRaises(ValueError):require_tagged_colour_resolution(data,changed,offered,english)
        with self.assertRaises(ValueError):require_tagged_colour_resolution({**data,'fa-IR':data['fa']},strings,offered,english)
        for parent in ('he','ur','missing'):
            with patch.dict(TAGGED_COLOUR_INHERITED_CATALOGUES,{'fa-IR':parent}),self.assertRaises(ValueError):
                require_tagged_colour_resolution(data,strings,offered,english)
        for missing in ('fa','fa-IR'):
            with self.assertRaises(ValueError):require_tagged_colour_resolution(data,strings,offered-{missing},english)

    def test_explicit_scope_and_open_fallbacks_match_current_picker(self):
        scope = fixture('locale_contract_scope.json')
        scoped, fallback = require_locale_scope(scope, SCOPED_TAGS, catalogues.offered_tags())
        self.assertEqual(59, len(scoped))
        self.assertEqual(112, len(fallback))
        self.assertEqual(27, len(ADDED_TAGS))
        self.assertLessEqual(ADDED_TAGS, fallback)
        self.assertEqual(fallback - {'cs', 'sv'}, set(fixture('commons_import_current_wording.json')['remaining_other_offered_locales']))
        source = (ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsCopyCreditTranslationTest.kt').read_text()
        declaration = re.search(r'private val fallbackTags=setOf\((.*?)\n    \)', source, re.S)
        self.assertIsNotNone(declaration)
        runtime_fallbacks = re.findall(r'"([\w-]+)"', declaration.group(1))
        self.assertEqual(len(fallback - {'cs', 'sv'}), len(runtime_fallbacks))
        self.assertEqual(fallback - {'cs', 'sv'}, set(runtime_fallbacks))

    def test_missing_duplicate_overlapping_or_unknown_scope_tags_are_rejected(self):
        from copy import deepcopy
        original = fixture('locale_contract_scope.json')
        offered = catalogues.offered_tags()
        for field in ('scoped_tags', 'fallback_tags'):
            for mutation in ('missing-group', 'empty-group', 'missing-tag', 'duplicate-tag', 'unknown-tag'):
                data = deepcopy(original)
                if mutation == 'missing-group': del data[field]
                if mutation == 'empty-group': data[field] = []
                if mutation == 'missing-tag': data[field].pop()
                if mutation == 'duplicate-tag': data[field].append(data[field][0])
                if mutation == 'unknown-tag': data[field][0] = 'zz-unknown'
                with self.subTest(field=field, mutation=mutation), self.assertRaises(ValueError):
                    require_locale_scope(data, SCOPED_TAGS, offered)
        data = deepcopy(original)
        data['fallback_tags'].append(data['scoped_tags'][0])
        with self.assertRaises(ValueError): require_locale_scope(data, SCOPED_TAGS, offered)
        for tag in ADDED_TAGS:
            data = deepcopy(original); data['fallback_tags'].remove(tag)
            with self.subTest(missing_added=tag), self.assertRaises(ValueError):
                require_locale_scope(data, SCOPED_TAGS, offered)
        with self.assertRaises(ValueError): require_locale_scope(original, SCOPED_TAGS, offered + [offered[0]])

    def test_all_current_values_attributes_placeholders_and_legal_literals(self):
        xml = {tag: path.read_text() for tag, path in paths().items()}
        for name in FAMILIES:
            data = wording_fixture(name)
            for key, values in data['values'].items():
                for tag, expected in values.items():
                    with self.subTest(family=name, key=key, tag=tag):
                        require_string(xml[tag], key, expected, data['constraints'][key])

    def test_whole_message_families_have_exact_localized_scope_and_no_english_filled_fallbacks(self):
        xml = {tag: ET.parse(path).getroot() for tag, path in paths().items()}
        for name in FAMILIES[:3]:
            data = wording_fixture(name)
            for key, values in data['values'].items():
                self.assertEqual(wording_tags(name), set(values))
                for tag, root in xml.items():
                    with self.subTest(key=key, tag=tag):
                        self.assertEqual(int(tag in values), len(root.findall(f"./string[@name='{key}']")))

    def test_metadata_english_identity_and_language_specific_normalization(self):
        data = wording_fixture(FAMILIES[0])
        for key, expected in data['values'].items():
            equal = set(data['constraints'][key]['default_equal_tags']) | {'default'}
            for tag, value in expected.items():
                self.assertEqual(tag in equal, value == expected['default'], (key, tag))
        for key, tags in data['nfc_and_no_category_C_required'].items():
            for tag in tags:
                value = catalogues.read_strings(paths()[tag])[key]
                self.assertEqual(value, unicodedata.normalize('NFC', value))
                self.assertFalse(any(unicodedata.category(c).startswith('C') for c in value))

    def test_script_controls_and_variation_selectors_are_retained(self):
        for name in FAMILIES[:3]:
            for key, tags in wording_fixture(name).get('special_codepoint_counts', {}).items():
                for tag, counts in tags.items():
                    value = catalogues.read_strings(paths()[tag])[key]
                    for point, count in counts.items():
                        self.assertEqual(count, value.count(chr(int(point[2:], 16))), (key, tag, point))

    def test_hungarian_instructions_reference_current_labels(self):
        data = wording_fixture('hungarian_attribution_current_wording.json')
        values = catalogues.read_strings(paths()['hu'])
        for key, labels in data['label_references'].items():
            for label in labels:
                self.assertIn(values[label], values[key], (key, label))

    def test_missing_duplicate_changed_and_wrong_format_resources_fail(self):
        for name in FAMILIES:
            data = wording_fixture(name)
            for key, values in data['values'].items():
                for tag, expected in values.items():
                    node = ET.parse(paths()[tag]).getroot().find(f"./string[@name='{key}']")
                    line = ET.tostring(node, encoding='unicode')
                    constraints = data['constraints'][key]
                    require_string('<resources>'+line+'</resources>', key, expected, constraints)
                    for broken in ('', line+line, line.replace('</string>', '? </string>'), line.replace('</string>', '%1$d</string>')):
                        with self.subTest(key=key, tag=tag), self.assertRaises(ValueError):
                            require_string('<resources>'+broken+'</resources>', key, expected, constraints)

    def test_independent_unrelated_resource_or_formatting_edits_are_allowed(self):
        xml = '<resources>\n<!-- ordinary refactor -->\n<string name="target">Commons</string><string name="other">New</string></resources>'
        self.assertEqual('Commons', require_string(xml, 'target', 'Commons'))

    def test_unicode_control_removal_is_rejected(self):
        data = wording_fixture(FAMILIES[0]); key = 'commons_metadata_query_failed'
        for tag, control in [('mn-Mong', '\u202f'), ('mnc-Mong', '\u180e')]:
            expected = data['values'][key][tag]
            self.assertIn(control, expected)
            xml = '<resources><string name="'+key+'">'+expected.replace(control, '')+'</string></resources>'
            with self.assertRaises(ValueError):
                require_string(xml, key, expected, data['constraints'][key])


class ReviewedResidualSuccessorTests(unittest.TestCase):
    """The finite review receipt supersedes holds, not whole-language acceptance."""
    def test_current_cohort_catalogues_keep_strict_successor_shape_and_predecessors(self):
        from copy import deepcopy
        from unittest.mock import patch
        from current_localization_contracts import residual_rows
        import basque_frisian_uzbek_priority_expectations as uz
        import sorani_uyghur_tatar_priority_expectations as ckb
        rows = residual_rows()
        for tag, module, count in [('uz-Latn', uz, 10), ('ckb', ckb, 11)]:
            data = module.bound_fixture(tag)
            original = ET.parse(ROOT / data['catalogue_path']).getroot()
            module.require_catalogue(tag, original)
            keys = {key for locale, key in rows if locale == tag}
            self.assertEqual(count, len(keys))
            self.assertFalse(keys & (set(data['original_catalogue']) | set(data['values'])))
            for key in keys:
                for mutation in ('missing', 'duplicate', 'type', 'value', 'attribute', 'child', 'tail', 'unreviewed'):
                    root = deepcopy(original); node = root.find(f"./string[@name='{key}']")
                    if mutation == 'missing': root.remove(node)
                    elif mutation == 'duplicate': root.append(deepcopy(node))
                    elif mutation == 'type': node.tag = 'plurals'
                    elif mutation == 'value': node.text += ' forged'
                    elif mutation == 'attribute': node.set('formatted', 'false')
                    elif mutation == 'child': ET.SubElement(node, 'b')
                    elif mutation == 'tail': node.tail = 'unreviewed'
                    else: node.set('name', 'unreviewed')
                    with self.subTest(tag=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                        module.require_catalogue(tag, root)
                changed = deepcopy(rows); changed[(tag, key)]['previous_target'] = 'forged'
                with patch('current_localization_contracts.residual_rows', return_value=changed):
                    with self.subTest(tag=tag, key=key, mutation='predecessor'), self.assertRaises(ValueError):
                        module.require_catalogue(tag, original)

    def test_complete_reviewed_successors_and_predecessors(self):
        from current_localization_contracts import residual_rows, require_residual_or_previous
        rows = residual_rows()
        english = ET.parse(catalogues.RES/'values/strings.xml').getroot()
        roots = {tag: ET.parse(catalogues.catalogue_paths()[tag]).getroot() for tag, _ in rows}
        self.assertEqual(320, sum(r['previous_target'] is None for r in rows.values()))
        self.assertEqual({('gl','ui_discard'),('gl','ui_bg'),('gl','ui_fg'), ('xh','ui_free_form_select'),('xh','ui_palette'),('xh','ui_preview'),('xh','ui_rotate'),('sr-Cyrl','ui_discard'),('sr-Latn','ui_discard')},
                         {identity for identity,r in rows.items() if r['previous_target'] is not None})
        for (tag,key),row in rows.items():
            with self.subTest(tag=tag,key=key):
                require_string(ET.tostring(english,encoding='unicode'),key,row['source'],{'attributes':row['attributes']})
                require_residual_or_previous(roots[tag],tag,key,row['previous_target'])
                self.assertEqual([],catalogues.android_string_errors(row['target']))

    def test_unchanged_main_acceptances_have_zero_presence_and_no_regional_credit(self):
        data = fixture('reviewed_residuals_20261030.json')
        rows = data['unchanged_acceptances']
        self.assertEqual({('fa','ui_main23'),('he','ui_main23')}, {(r['locale'],r['key']) for r in rows})
        self.assertEqual(2,len(rows))
        for row in rows:
            self.assertEqual(row['target'],row['previous_target'])
            self.assertEqual(0,row['presence_delta'])
            self.assertEqual('accepted_unchanged',row['disposition'])
            self.assertFalse(row['regional_direct_acceptance'])
            held=fixture('persian_hebrew_urdu_priority_wording.json')['locales'][row['locale']]['held_present'][row['key']]
            self.assertEqual(held,{'attributes':row['attributes'],'value':row['target']})
            require_string(catalogues.catalogue_paths()[row['locale']].read_text(),row['key'],row['target'],{'attributes':row['attributes']})
        regional=fixture('regional_persian_japanese_french_wording.json')['locales']['fa-IR']['rows']['string/ui_main23']
        self.assertEqual('hold_preserved',regional['disposition'])
        self.assertIsNone(regional['effective'])
        require_string(catalogues.catalogue_paths()['fa-IR'].read_text(),'ui_main23',regional['direct']['value'],{'attributes':regional['direct']['attributes']})

    def test_each_successor_rejects_missing_duplicate_wrong_type_and_full_message_corruption(self):
        from current_localization_contracts import residual_rows, require_residual_or_previous
        from copy import deepcopy
        for (tag,key),row in residual_rows().items():
            for mutation in ('missing','duplicate','type','truncate','argument','markup','attribute','predecessor'):
                root=ET.Element('resources');node=ET.SubElement(root,'string',row['attributes']);node.text=row['target']
                if mutation=='missing':root.remove(node)
                elif mutation=='duplicate':root.append(deepcopy(node))
                elif mutation=='type':node.tag='plurals'
                elif mutation=='truncate':node.text=node.text[:-1]
                elif mutation=='argument':node.text+=' %9$s'
                elif mutation=='markup':ET.SubElement(node,'b').text='extra'
                elif mutation=='attribute':node.set('translatable','false')
                elif row['previous_target'] is None:root.remove(node)
                else:node.text=row['previous_target']
                with self.subTest(tag=tag,key=key,mutation=mutation),self.assertRaises(ValueError):
                    require_residual_or_previous(root,tag,key,row['previous_target'])
        with self.assertRaises(ValueError):
            require_residual_or_previous(ET.fromstring('<resources><string name="ui_save_as">unreviewed</string></resources>'),'sq','ui_save_as')


if __name__ == '__main__': unittest.main()
