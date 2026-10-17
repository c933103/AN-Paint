#!/usr/bin/env python3
"""Conservative source guard for Android text/printf boundaries (no dependencies).

Scan every production src/<source-set> Kotlin/Java tree, regardless of package,
and present build/generated trees. --source-root includes additional configured
or generated roots outside those conventions. This is a lexical policy check,
not a Kotlin/Java type checker or a proof about reflection, native code or HTML.

Outside the two reviewed boundary files, printf templates must be direct code
literals (or literal-only conditional branches). Dynamic aliases are rejected
without attempting fragile interprocedural taint inference. Comments, multiline
calls, imports and Kotlin interpolation bodies are tokenized. Unknown .format
receivers fail closed; explicit java.text date/number formatter factories are
different APIs. getString's String-key storage overloads remain permitted.
"""
import argparse
import os
from pathlib import Path
import re
from typing import NamedTuple

CLASSIC = 'Paintroid/src/main/java/org/catrobat/paintroid/classic/'
RESOURCE_BOUNDARY = CLASSIC + 'UiText.kt'
FORMAT_BOUNDARY = CLASSIC + 'LocaleText.kt'
TEST_SET = re.compile(r'(?:(?:test|androidTest|testFixtures)(?:[A-Z].*)?|.*(?:UnitTest|AndroidTest|TestFixtures))$')


class Token(NamedTuple):
    value: str
    kind: str
    offset: int


def tokenize(source, kotlin=True):
    """Return outer tokens and separately checked ${expression} token streams."""
    embedded = []

    def read(start=0, interpolation=False):
        result, i, depth = [], start, 0
        while i < len(source):
            begin, c = i, source[i]
            if c.isspace(): i += 1; continue
            if source.startswith('//', i):
                end = source.find('\n', i); i = len(source) if end < 0 else end; continue
            if source.startswith('/*', i):
                i += 2; comments = 1
                while i < len(source) and comments:
                    if source.startswith('/*', i) and kotlin: comments += 1; i += 2
                    elif source.startswith('*/', i): comments -= 1; i += 2
                    else: i += 1
                continue
            if interpolation and c == '}' and depth == 0: return result, i + 1
            if c in '\"\'':
                quote = '"""' if source.startswith('"""', i) else c
                i += len(quote); dynamic = False
                while i < len(source) and not source.startswith(quote, i):
                    if source[i] == '\\' and len(quote) == 1: i += 2; continue
                    if kotlin and c == '"' and source.startswith('${', i):
                        nested, i = read(i + 2, True); embedded.append(nested); dynamic = True
                    elif kotlin and c == '"' and source[i] == '$' and i + 1 < len(source) and (source[i+1].isalpha() or source[i+1] == '_'):
                        dynamic = True; i += 1
                    else: i += 1
                i += len(quote)
                result.append(Token(source[begin:i], 'dynamic' if dynamic else ('string' if c == '"' else 'char'), begin)); continue
            if c == '`':
                end = source.find('`', i+1)
                i = len(source) if end < 0 else end+1
                result.append(Token(source[begin+1:i-1], 'word', begin)); continue
            if c.isalnum() or c in '_$':
                i += 1
                while i < len(source) and (source[i].isalnum() or source[i] in '_$'): i += 1
                result.append(Token(source[begin:i], 'word', begin)); continue
            if c == '{': depth += 1
            elif c == '}': depth -= 1
            result.append(Token(c, 'symbol', begin)); i += 1
        return result, i

    outer, _ = read()
    return [outer, *embedded]


def matching(tokens, start):
    pair = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for i in range(start, len(tokens)):
        value = tokens[i].value
        if value in pair: stack.append(pair[value])
        elif stack and value == stack[-1]:
            stack.pop()
            if not stack: return i
    return len(tokens)-1


def split_top(tokens, separator):
    result, start, i = [], 0, 0
    while i < len(tokens):
        if tokens[i].value in ('(', '[', '{'): i = matching(tokens, i)
        elif tokens[i].value == separator: result.append(tokens[start:i]); start = i+1
        i += 1
    return [*result, tokens[start:]]


def code_literal(tokens):
    while tokens and tokens[0].value in ('(', '{') and matching(tokens, 0) == len(tokens)-1:
        tokens = tokens[1:-1]
    if len(tokens) == 1: return tokens[0].kind == 'string'
    if not tokens: return False
    if tokens[0].value == 'if' and len(tokens) > 2 and tokens[1].value == '(':
        branches = split_top(tokens[matching(tokens, 1)+1:], 'else')
        return len(branches) == 2 and all(code_literal(part) for part in branches)
    choices = split_top(tokens, '?')
    if len(choices) == 2:
        branches = split_top(choices[1], ':')
        return len(branches) == 2 and all(code_literal(part) for part in branches)
    parts = split_top(tokens, '+')
    return len(parts) > 1 and all(code_literal(part) for part in parts)


def receiver(tokens, method):
    """The immediately preceding member receiver, including chained calls."""
    end = method-1
    if end < 0 or tokens[end].value != '.': return []
    start = end-1
    while start >= 0:
        if tokens[start].value in (')', ']'):
            closing = tokens[start].value; opening = '(' if closing == ')' else '['; depth = 1; start -= 1
            while start >= 0 and depth:
                if tokens[start].value == closing: depth += 1
                elif tokens[start].value == opening: depth -= 1
                start -= 1
            if start >= 0 and tokens[start].kind == 'word': continue
            break
        if start > 0 and tokens[start-1].value == '.': start -= 2; continue
        start -= 1; break
    return tokens[start+1:end]


def factory_name(tokens):
    opening = next((i for i,t in enumerate(tokens) if t.value == '('), None)
    return ''.join(t.value for t in tokens[:opening]) if opening is not None and matching(tokens,opening)==len(tokens)-1 else ''


def check_source(source, path):
    path = Path(path).as_posix(); problems = []
    streams = tokenize(source, path.endswith('.kt'))
    # Import aliases are code tokens, so comments and quoted examples cannot
    # add exceptions or hide imported static/extension formatters.
    outer = streams[0]; aliases = {'format', 'formatted'}; static_import = False
    string_classes = {'String','java.lang.String','String.Companion'}
    for i, token in enumerate(outer):
        if token.value != 'import': continue
        end = i+1
        while end < len(outer) and '\n' not in source[outer[end-1].offset:outer[end].offset] and outer[end].value != ';': end += 1
        declaration = ''.join(t.value for t in outer[i+1:end])
        if re.match(r'(?:static)?(?:java\.lang\.String|kotlin\.text)\.(?:format|\*)', declaration):
            static_import = True
            renamed = re.search(r'as(\w+)$', declaration)
            if renamed: aliases.add(renamed.group(1))
        renamed_class = re.fullmatch(r'(?:java\.lang\.String|kotlin\.String)as(\w+)', declaration)
        if renamed_class: string_classes.add(renamed_class.group(1))

    def report(token, message):
        problems.append(f'{path}:{source.count(chr(10), 0, token.offset)+1}: {message}')

    # Typed String parameters/locals and inferred String constants distinguish
    # Bundle/SharedPreferences keys from Android's integer resource IDs. This
    # inventory is used only for overload discrimination, never to authorize a
    # dynamic printf template.
    types = {}
    def declare(name, kind): types.setdefault(name, set()).add(kind)
    for tokens in streams:
        for i in range(len(tokens)-2):
            a,b,c = tokens[i:i+3]
            if b.value == ':' and c.kind == 'word': declare(a.value, c.value)
            if a.value in ('String','Locale','int','long','Integer','Long') and b.kind == 'word' and c.value in ('=', ',', ')', ';'):
                declare(b.value, a.value)
            if a.value in ('val','var') and b.kind == 'word' and c.value == '=' and i+3 < len(tokens):
                declare(b.value, 'String' if tokens[i+3].kind in ('string','dynamic') else 'unknown')
    # Conflicting declarations/shadowing remove an exemption; they never grant
    # a String/Locale type to another scope with the same spelling.
    string_names = {name for name, kinds in types.items() if kinds == {'String'}}
    locale_names = {name for name, kinds in types.items() if kinds == {'Locale'}}

    for tokens in streams:
        for i, token in enumerate(tokens):
            name = token.value
            if name not in aliases | {'getString','getQuantityString','getQuantityText'}: continue
            if i >= 2 and tokens[i-2].value == ':' and tokens[i-1].value == ':':
                allowed = FORMAT_BOUNDARY if name in aliases else RESOURCE_BOUNDARY
                if path != allowed: report(token, 'Do not alias a raw formatting/resource callable; use ui/uiText.')
                continue
            if i+1 >= len(tokens) or tokens[i+1].value != '(': continue
            if i and tokens[i-1].value == 'fun': continue
            args = split_top(tokens[i+2:matching(tokens, i+1)], ',')
            target = receiver(tokens, i)
            factory = factory_name(target)
            if name.startswith('getQuantity'):
                if path != RESOURCE_BOUNDARY: report(token, 'Raw plural access bypasses uiQuantity/uiText.')
            elif name == 'getString':
                first = args[0] if args else []
                string_key = len(first)==1 and (first[0].kind in ('string','dynamic') or first[0].value in string_names)
                preferences = factory.endswith('.getSharedPreferences')
                if path != RESOURCE_BOUNDARY and len(args) > 1 and not (string_key or preferences):
                    report(token, 'Formatted Android getString must use ui/uiText.')
            elif target or static_import:
                if path == FORMAT_BOUNDARY: continue
                qualified = ''.join(t.value for t in target)
                # These APIs format Date/Number values; they do not interpret a
                # translated String as a printf template. Unknown receivers are
                # deliberately not exempted by variable names such as "formatter".
                if re.fullmatch(r'(?:java\.text\.)?(?:DateFormat|NumberFormat)\.get\w*Instance', factory): continue
                if qualified in string_classes or not target:
                    first = args[0] if args else []
                    locale = ((len(first)==1 and first[0].value in locale_names | {'null'}) or
                              re.fullmatch(r'(?:java\.util\.)?Locale\.[A-Z_]+', ''.join(t.value for t in first)) or
                              factory_name(first) in ('Locale.getDefault','java.util.Locale.getDefault','Locale.forLanguageTag','java.util.Locale.forLanguageTag','Locale','java.util.Locale'))
                    template = args[1] if locale and len(args)>1 else first
                else: template = target
                if not code_literal(template): report(token, 'Raw formatter requires a code literal template; translated/aliased templates must use ui/uiText.')
    return problems


def production_sources(root, source_roots=()):
    root = Path(root)
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('.git','.gradle','.cxx','node_modules','__pycache__')]
        relative = Path(base).relative_to(root).parts
        if 'build' in relative and 'generated' not in relative[relative.index('build')+1:]:
            dirs[:] = [d for d in dirs if d == 'generated']; continue
        if 'build' in relative and any(TEST_SET.fullmatch(part) for part in relative[relative.index('build')+1:]):
            dirs[:] = []; continue
        source_set = relative[relative.index('src')+1] if 'src' in relative and len(relative)>relative.index('src')+1 else None
        if source_set and TEST_SET.fullmatch(source_set): dirs[:] = []; continue
        included = source_set is not None or ('build' in relative and 'generated' in relative)
        included = included or any(Path(base).is_relative_to(root / extra) for extra in source_roots)
        if included:
            for name in sorted(files):
                if Path(name).suffix in ('.kt','.java'): yield Path(base)/name


def check_repository(root, source_roots=()):
    root = Path(root)
    missing = [f'{extra}: Missing explicitly configured source root' for extra in source_roots if not (root/extra).is_dir()]
    return missing + [problem for path in production_sources(root, source_roots)
            for problem in check_source(path.read_text(), path.relative_to(root))]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--source-root', action='append', default=[], help='Additional configured/generated source root, relative to repository')
    args = parser.parse_args()
    failures = check_repository(args.repository, args.source_root)
    if failures: print('\n'.join(failures))
    else: print('Translation formatter/resource boundary check passed.')
    raise SystemExit(bool(failures))
