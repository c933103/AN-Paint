"""Strict shared checks for the eight reviewed priority-cohort fixture families.

Cohort modules pass current scope, digests, loader and validators at invocation;
cohort-specific successor and display contracts remain local.
"""
import hashlib
import json


def require_fixture_binding(tag, data, tags, fixture_digests):
    if tag not in tags:
        raise ValueError('Outside exact locale set')
    try:
        raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    except (TypeError, ValueError) as error:
        raise ValueError('Malformed review fixture') from error
    if hashlib.sha256(raw).hexdigest() != fixture_digests[tag]:
        raise ValueError('Complete canonical review fixture differs: ' + tag)
    return data


def bound_fixture(tag, tags, family, fixture, require_fixture_binding):
    if tag not in tags:
        raise ValueError('Outside exact locale set')
    return require_fixture_binding(tag, fixture(family + '/' + tag + '.json'))


def require_resource_shape(element, kind, expected):
    if element is None or element.tag != kind or element.attrib != expected['attributes']:
        raise ValueError('Exact resource type/attributes differ')
    if (element.tail or '').strip():
        raise ValueError('Unexpected resource tail')
    if kind == 'string':
        if list(element) or element.text != expected['value']:
            raise ValueError('Exact child-free string differs')
    elif kind == 'plurals':
        values = expected['value']
        attrs = expected['children_attributes']
        if (element.text or '').strip() or len(element) != len(values):
            raise ValueError('Plural parent text/count differs')
        quantities = [node.get('quantity') for node in element]
        if len(set(quantities)) != len(quantities) or set(quantities) != set(values):
            raise ValueError('Exact plural quantity set differs')
        for node in element:
            q = node.get('quantity')
            if node.tag != 'item' or node.attrib != attrs[q] or list(node) or (node.tail or '').strip() or (node.text != values[q]):
                raise ValueError('Exact child-free plural item/attributes/tail differs')
    else:
        raise ValueError('Unexpected resource type')


def require_edited_resource(tag, key, element, data, bound_fixture, require_fixture_binding, require_resource_shape):
    data = bound_fixture(tag) if data is None else require_fixture_binding(tag, data)
    if key not in data['values']:
        raise ValueError('Outside exact reviewed edit set')
    row = data['values'][key]
    from current_localization_contracts import residual_rows, RESIDUAL_KEYS
    successor = residual_rows().get((tag, key)) if key in RESIDUAL_KEYS.get(tag, ()) else None
    if successor is not None:
        if row['type'] != 'string' or successor['previous_target'] != row['reviewed_value'] or successor['source'] != row['source']['value']:
            raise ValueError('Exact edited successor predecessor/source differs')
        require_resource_shape(element, 'string', {'value': successor['target'], 'attributes': successor['attributes']})
        return
    expected = {'value': row['reviewed_value'], 'attributes': row['reviewed_attributes']}
    if row['type'] == 'plurals':
        expected['children_attributes'] = row['reviewed_children_attributes']
    require_resource_shape(element, row['type'], expected)


def require_catalogue(tag, root, data, bound_fixture, require_fixture_binding, require_resource_shape):
    from current_localization_contracts import residual_rows
    data = bound_fixture(tag) if data is None else require_fixture_binding(tag, data)
    if root.tag != 'resources' or root.attrib or (root.text or '').strip() or (root.tail or '').strip():
        raise ValueError('Malformed resource root')
    successors = {key: row for (locale, key), row in residual_rows().items() if locale == tag}
    expected = set(data['original_catalogue']) | set(data['values']) | set(successors)
    names = [node.get('name') for node in root]
    if len(set(names)) != len(names) or set(names) != expected:
        raise ValueError('Exact complete catalogue identity set differs')
    for node in root:
        key = node.get('name')
        if key in successors:
            row = successors[key]
            old = data['original_catalogue'].get(key)
            previous = data['values'][key]['reviewed_value'] if key in data['values'] else old['value'] if old else None
            if row['previous_target'] != previous:
                raise ValueError('Exact catalogue successor predecessor differs')
            # Retain the catalogue's strict tail/child/type checks for additions too.
            require_resource_shape(node, 'string', {'value': row['target'], 'attributes': row['attributes']})
        elif key in data['values']:
            row = data['values'][key]
            value = {'value': row['reviewed_value'], 'attributes': row['reviewed_attributes']}
            if row['type'] == 'plurals':
                value['children_attributes'] = row['reviewed_children_attributes']
            require_resource_shape(node, row['type'], value)
        else:
            old = data['original_catalogue'][key]
            require_resource_shape(node, 'plurals' if isinstance(old['value'], dict) else 'string', old)
    return root
