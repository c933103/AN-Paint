"""Finite accepted ordinary/sparse packets, not a whole-language review claim."""
from current_localization_contracts import residual_rows, require_residual_or_previous
from priority_cohort_checks import require_resource_shape

TAGS = frozenset({'tt-Cyrl','tt-Latn','br','sv','shn','yua','ang','non'})
COUNTS = {'tt-Cyrl':11,'tt-Latn':11,'br':10,'sv':1,'shn':148,'yua':60,'ang':244,'non':254}
EXISTING = {('br','ui_drawing_canvas_pinch_and_move_two_fingers_to'),('shn','ui_brush')}


def rows():
    result={i:r for i,r in residual_rows().items() if i[0] in TAGS}
    if {tag:sum(i[0]==tag for i in result) for tag in TAGS} != COUNTS:
        raise ValueError('Accepted packet counts differ')
    if {i for i,r in result.items() if r['previous_target'] is not None} != EXISTING:
        raise ValueError('Accepted replacement identities differ')
    return result


def require_historical_catalogue(tag,root):
    if tag not in ('ang','non'):
        raise ValueError('Not a historical packet locale')
    accepted={key:r for (locale,key),r in rows().items() if locale==tag}
    if (root.tag!='resources' or root.attrib or (root.text or '').strip()
            or (root.tail or '').strip() or len(root)!=len(accepted)
            or {n.get('name') for n in root}!=set(accepted)):
        raise ValueError('Historical catalogue scope or root differs')
    for key,row in accepted.items():
        require_residual_or_previous(root,tag,key)
        require_resource_shape(root.find(f"./string[@name='{key}']"),'string',
                               {'value':row['target'],'attributes':row['attributes']})
    return root
