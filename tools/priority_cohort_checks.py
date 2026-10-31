"""Strict resource-shape check shared by bounded current product fixtures."""

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
