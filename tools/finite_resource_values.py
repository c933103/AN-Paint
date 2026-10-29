"""Stateless typed-value and XML-shape checks shared by finite localization oracles."""
import xml.etree.ElementTree as ET


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _same_type_and_value(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_same_type_and_value(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_same_type_and_value(x, y) for x, y in zip(a, b))
    return a == b


def _blank(text):
    return text is None or not text.strip()


def typed(element):
    require(element.tag in {'string', 'plurals'}, 'Unexpected resource type')
    require(_blank(element.tail), 'Unexpected resource tail text')
    if element.tag == 'string':
        require(len(element) == 0, 'Unexpected string markup')
    else:
        require(_blank(element.text), 'Unexpected plural container text')
        for child in element:
            require(child.tag == 'item' and len(child) == 0, 'Unexpected plural item markup')
            require(_blank(child.tail), 'Unexpected plural item tail text')
    return {
        'type': element.tag,
        'attributes': dict(element.attrib),
        'value': element.text if element.tag == 'string' else [
            {'type': child.tag, 'attributes': dict(child.attrib), 'value': child.text}
            for child in element
        ],
    }


def _resource_map(path, expected_identities):
    root = ET.parse(path).getroot()
    require(root.tag == 'resources' and not root.attrib, 'Unexpected resource root')
    require(_blank(root.text) and _blank(root.tail), 'Unexpected resource root text')
    expected_names = {identity.split('/', 1)[1] for identity in expected_identities}
    result = {}
    seen_names = set()
    for element in root:
        require(_blank(element.tail), 'Unexpected resource tail text')
        name = element.get('name')
        if name not in expected_names:
            continue  # Unrelated resource types/values are not this finite oracle's scope.
        require(name not in seen_names, 'Duplicate reviewed name across resource types: ' + name)
        seen_names.add(name)
        identity = element.tag + '/' + name
        require(identity in expected_identities, 'Wrong type for reviewed resource: ' + name)
        result[identity] = typed(element)
    return result
