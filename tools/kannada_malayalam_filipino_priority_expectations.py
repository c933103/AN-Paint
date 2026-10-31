"""Bounded current expectations; complete original evidence stays on its immutable ref."""
import re
from current_localization_contracts import fixture
import priority_cohort_checks as _cohort_checks

NAME='kannada_malayalam_filipino_priority_wording.json'
TAGS=frozenset({'kn','ml-IN','fil'})
ADDITION_TAGS=frozenset({'kn','ml-IN'})
MEMORY_ADDITIONS=frozenset((tag,key) for tag in ADDITION_TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=ADDITION_TAGS
SVG_ADDITIONS=frozenset((tag,key) for tag in ADDITION_TAGS for key in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))


def current_row(tag,key):
    return _cohort_checks.current_row(tag, key, NAME, TAGS, fixture)


def display(tag,key):
    value=current_row(tag,key)['target']
    if isinstance(value,dict):return {quantity:_display(text) for quantity,text in value.items()}
    if value.startswith('@string/'):
        if (tag,key,value)!=('fil','ui_save_a5d0d9','@string/ui_save'):
            raise ValueError('Only exact preserved Filipino Save alias is accepted')
        return _display(current_row('fil','ui_save')['target'])
    return _display(value)


def _display(value):
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m.group(1),m.group(1)),value)
