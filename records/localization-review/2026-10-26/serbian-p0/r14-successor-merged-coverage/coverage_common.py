"""Source parser/Git verifier reused, no prior workflow verdicts reused."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, 'duplicate JSON key: ' + key)
        value[key] = item
    return value


def read(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(data, kind='blob'):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def emit(folder, name, data):
    (folder / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def file_binding(path, public_name):
    raw = path.read_bytes()
    return {'path': public_name, 'bytes': len(raw), 'sha256': sha(raw), 'git_blob_sha1': git(raw)}


def parse(raw):
    require(b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper(), 'XML entity boundary')
    root = ET.fromstring(raw)
    require(root.tag == 'resources', 'invalid resource root')
    containers, leaves, nodes, names = {}, {}, {}, set()
    for node in root:
        require(node.tag in ('string', 'plurals', 'string-array'), 'unexpected catalogue resource type')
        name = node.get('name')
        require(bool(name) and name not in names, 'missing or duplicate resource name')
        names.add(name)
        identity = node.tag + '/' + name
        nodes[identity] = node
        if node.get('translatable') == 'false':
            continue
        if node.tag == 'string':
            value = ''.join(node.itertext())
            require(bool(value), 'empty string resource: ' + identity)
            containers[identity] = value
            leaves[identity] = value
        else:
            values = {}
            for index, item in enumerate(node):
                require(item.tag == 'item', 'invalid resource child')
                quantity = item.get('quantity') if node.tag == 'plurals' else str(index)
                require(quantity is not None and quantity not in values, 'missing or duplicate resource item')
                if node.tag == 'plurals':
                    require(quantity in {'zero', 'one', 'two', 'few', 'many', 'other'}, 'unknown plural quantity')
                value = ''.join(item.itertext())
                require(bool(value), 'empty resource item')
                values[quantity] = value
                leaves[identity + '[' + quantity + ']'] = value
            require(bool(values), 'empty resource container')
            containers[identity] = values
    return containers, leaves, nodes


def fingerprint(node):
    return node.tag, sorted(node.attrib.items()), node.text, tuple(fingerprint(c) for c in node)


def tokens(text):
    require('%' not in FORMAT_TOKEN.sub('', text), 'invalid/unescaped format token')
    return collections.Counter(FORMAT_TOKEN.findall(text))


def verify_tree(tree, expected_tree):
    require(tree.get('truncated') is False and tree['sha'] == expected_tree, 'wrong/truncated head tree')
    entries = tree['tree']
    bypath = {e['path']: e for e in entries}
    require(len(bypath) == len(entries), 'duplicate tree path')
    children = collections.defaultdict(list)
    for e in entries:
        path = Path(e['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe tree path')
        require(e['type'] in ('blob', 'tree'), 'unsupported tree entry')
        require(e['mode'] in ('100644', '100755', '120000', '040000'), 'unexpected tree mode')
        require(bool(re.fullmatch('[0-9a-f]{40}', e['sha'])), 'malformed tree SHA')
        children[path.parent.as_posix() if path.parent.as_posix() != '.' else ''].append(e)
    for parent, contents in children.items():
        raw = b''
        for e in sorted(contents, key=lambda x: (Path(x['path']).name + ('/' if x['type'] == 'tree' else '')).encode()):
            mode = e['mode'].lstrip('0')
            raw += mode.encode() + b' ' + Path(e['path']).name.encode() + b'\0' + bytes.fromhex(e['sha'])
        expected = expected_tree if not parent else bypath[parent]['sha']
        require(git(raw, 'tree') == expected, 'recursive Git tree hash mismatch: ' + parent)
    return {k: e for k, e in bypath.items() if e['type'] == 'blob'}


FORMAT_TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')
