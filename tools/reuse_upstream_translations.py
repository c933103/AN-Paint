#!/usr/bin/env python3
"""Rebuild audited shared vocabulary from exact, pinned Paintroid translation XML."""
import argparse
import hashlib
import json
import pathlib
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "translations"
RES = ROOT / "Paintroid/src/main/res"

# Correct reviewed upstream mistakes without changing the pinned source files.
# Each tuple records the expected upstream value and AN Paint's replacement.
LOCAL_CORRECTIONS = {
    "ja": {
        "ui_flip_horizontal": ("上下反転", "左右反転"),
        "ui_flip_vertical": ("左右反転", "上下反転"),
    },
}


def read_strings(path):
    return {node.get("name"): "".join(node.itertext()) for node in ET.parse(path).getroot() if node.tag == "string"}


def qualifier_and_tag(qualifier):
    # Crowdin's historical region labels encode Serbian scripts, not territories.
    special = {"values-sr-rCS": ("values-b+sr+Latn", "sr-Latn"),
               "values-sr-rSP": ("values-b+sr+Cyrl", "sr-Cyrl")}
    if qualifier in special:
        return special[qualifier]
    tag = qualifier.removeprefix("values-").replace("-r", "-")
    tag = {"iw": "he", "in": "id"}.get(tag, tag)
    return qualifier, tag


def generate():
    index = json.loads((DATA / "upstream-index.json").read_text())
    mapping = json.loads((DATA / "common-terms.json").read_text())
    base = read_strings(DATA / "upstream/values.xml")
    android = json.loads((DATA / "android-actions.json").read_text())["locales"]
    reviewed = json.loads((DATA / "reviewed-actions.json").read_text())["locales"]
    defaults = {}
    for path in sorted((RES / "values").glob("*.xml")):
        defaults.update(read_strings(path))
    def normal(value):
        return value.strip().strip('"').replace("\\'", "'").rstrip(":：").casefold()
    results = {}
    coverage = []
    tags = ["en"]
    for item in index["files"]:
        qualifier = pathlib.PurePosixPath(item["path"]).parent.name
        source = DATA / "upstream" / (qualifier + ".xml")
        raw = source.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if digest != item["blob_sha"]:
            raise ValueError(f"Upstream source bytes changed: {source}")
        if qualifier == "values":
            continue
        strings = read_strings(source)
        terms = {key: strings[old] for key, old in mapping.items()
                 if strings.get(old) and not strings[old].startswith("@")}
        output_qualifier, tag = qualifier_and_tag(qualifier)
        corrections = LOCAL_CORRECTIONS.get(tag, {})
        for key, (original, corrected) in corrections.items():
            if terms.get(key) != original:
                raise ValueError(f"Review local correction after upstream change: {tag}/{key}")
            terms[key] = corrected
        # Use Android's context-specific clipboard and Cancel terms, then apply
        # editor-context corrections. Exact pinned Paintroid sources stay untouched.
        android_terms = android.get(tag, {}).get("strings", {})
        terms.update(android_terms)
        terms.update(reviewed.get(tag, {}))
        if normal(terms.get("ui_discard", "")) == normal(terms.get("ui_cancel", "")):
            terms["ui_discard"] = "Discard changes"
        terms["ui_discard_changes23"] = terms.get("ui_discard_changes23", terms.get("ui_discard", "Discard changes"))
        terms["ui_keep_editing23"] = terms.get("ui_keep_editing23", terms.get("ui_cancel", "Cancel"))
        terms["ui_save_a5d0d9"] = terms.get("ui_save", "Save")
        if tag.startswith("en-"):
            for key in ("ui_discard_changes23", "ui_keep_editing23"):
                terms[key] = defaults[key]
        if not tag.startswith("en-") and terms.get("ui_drawing23"):
            terms["ui_draw26"] = terms["ui_drawing23"]
        distinct = sum(1 for key in terms if key in mapping and normal(terms[key]) != normal(base.get(mapping[key], "")))
        distinct += sum(1 for key in reviewed.get(tag, {}) if key not in mapping and normal(terms[key]) != normal(defaults.get(key, "")))
        included = distinct > 0 or tag.startswith("en-")
        record = {"original_qualifier": qualifier, "language_tag": tag,
                  "reused_entries": sum(1 for key in terms if key in mapping and key not in corrections and key not in android_terms and key not in reviewed.get(tag, {})),
                  "android_action_entries": len(android_terms), "reviewed_action_entries": len(reviewed.get(tag, {})), "entries_different_from_upstream_english": distinct,
                  "offered_in_app": included, "blob_sha": digest,
                  "source_sha256": hashlib.sha256(raw).hexdigest()}
        if corrections:
            record["locally_corrected_entries"] = list(corrections)
        if included:
            tags.append(tag)
            lines = ['<?xml version="1.0" encoding="utf-8"?>',
                     '<!-- Shared vocabulary: Catrobat/Paintroid translators; AGPL-3.0-or-later.',
                     'Generated by tools/reuse_upstream_translations.py. See translations/README.md. -->',
                     '<resources>']
            for key, value in terms.items():
                # Android's numeric slider already supplies its own punctuation.
                if key == "ui_quality":
                    value = value.rstrip().rstrip(":：").rstrip()
                value = value.replace("'", "\\'") if "\\'" not in value else value
                lines.append(f'    <string name="{key}">{escape(value)}</string>')
            lines += ['</resources>', '']
            target = RES / output_qualifier / "strings_upstream.xml"
            results[target] = "\n".join(lines)
            record["generated_resource"] = str(target.relative_to(ROOT))
        coverage.append(record)
    # Additional locally maintained script/locale foundations.
    for qualifier, tag in (("values-b+lzh+Hant", "lzh-Hant"), ("values-b+mn+Mong", "mn-Mong"), ("values-zh-rHK", "zh-HK"), ("values-b+mn+Cyrl+MN", "mn-Cyrl-MN")):
        path = RES / qualifier / "strings23.xml"
        if not path.is_file():
            raise ValueError(f"Missing local translation foundation: {path}")
        tags.append(tag)
    catalogue = json.loads((DATA / "language-options.json").read_text())
    options = {item["tag"]: item for item in catalogue["options"]}
    translated = set(tags)
    for tag, item in options.items():
        if not item.get("name_only") and item.get("translation_base", tag) not in translated:
            raise ValueError(f"Language option has no translation base: {tag}")
    tags = [catalogue["pinned_first"]] + sorted(set(options) - {catalogue["pinned_first"]}, key=str.casefold)
    for record in coverage:
        record["offered_tags"] = [tag for tag in tags if not options[tag].get("name_only")
                                  and options[tag].get("translation_base", tag) == record["language_tag"]]
        record["offered_in_app"] = bool(record["offered_tags"])
    # New regional English choices inherit the same UI, with explicit spelling
    # rather than depending on Android's region fallback order.
    english_overrides = {node.get("name") for q in ("values-en-rAU", "values-en-rCA", "values-en-rGB")
                         for node in ET.fromstring(results[RES / q / "strings_upstream.xml"])}
    for tag, qualifier in (("en-001", "values-b+en+001"), ("en-US", "values-en-rUS"),
                           ("en-SG", "values-en-rSG"), ("en-IN", "values-en-rIN")):
        lines = ['<?xml version="1.0" encoding="utf-8"?>',
                 '<!-- Generated English spelling variants; see translations/README.md. -->', '<resources>']
        for key, value in sorted(defaults.items()):
            # Cover existing regional overrides as well as spelling-sensitive
            # strings, so Android cannot pick another English region's commands.
            if key in english_overrides or re.search(r'(?i)\b(?:water)?colou?rs?\b', value):
                def spelling(match):
                    word = match.group()
                    return re.sub('(?i)colour', lambda m: 'Color' if m.group()[0].isupper() else 'color', word) if tag == 'en-US' else re.sub('(?i)color', lambda m: 'Colour' if m.group()[0].isupper() else 'colour', word)
                value = re.sub(r'(?i)\b(?:water)?colou?rs?\b', spelling, value)
                value = value.replace("'", "\\'") if "\\'" not in value else value
                lines.append(f'    <string name="{key}">{escape(value)}</string>')
        results[RES / qualifier / "strings_english.xml"] = '\n'.join(lines + ['</resources>', ''])
    results[DATA / "coverage.json"] = json.dumps({"revision": index["revision"],
        "mapped_common_terms": len(mapping), "offered_language_count_including_english": len(tags),
        "name_only_options": [tag for tag in tags if options[tag].get("name_only")],
        "coverage": coverage}, indent=2, ensure_ascii=False) + "\n"
    results[RES / "values/app_language_tags.xml"] = (
        '<?xml version="1.0" encoding="utf-8"?>\n<!-- Generated; see translations/README.md. -->\n'
        '<resources>\n    <string-array name="app_language_tags" translatable="false">\n' +
        ''.join(f'        <item>{tag}</item>\n' for tag in tags) +
        '    </string-array>\n</resources>\n')
    arrays = {
        "app_language_names": [options[tag]["name"] for tag in tags],
        "app_language_name_only": [tag for tag in tags if options[tag].get("name_only")],
        "app_language_aliases": list(catalogue["aliases"]),
        "app_language_alias_targets": list(catalogue["aliases"].values()),
    }
    results[RES / "values/app_language_names.xml"] = (
        '<?xml version="1.0" encoding="utf-8"?>\n<!-- Generated names only; no translation coverage is implied. -->\n<resources>\n' +
        ''.join(f'    <string-array name="{key}" translatable="false">\n' +
                ''.join('        <item>' + escape(value).replace("'", "\\'") + '</item>\n' for value in values) +
                '    </string-array>\n' for key, values in arrays.items()) + '</resources>\n')
    results[RES / "xml/app_locales.xml"] = (
        '<?xml version="1.0" encoding="utf-8"?>\n<!-- Partial vocabulary; see translations/README.md. -->\n'
        '<locale-config xmlns:android="http://schemas.android.com/apk/res/android">\n' +
        ''.join(f'    <locale android:name="{tag}"/>\n' for tag in tags) + '</locale-config>\n')
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = generate()
    for path, expected in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text() != expected:
                raise SystemExit(f"Generated translation differs: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
    print(f"{'Verified' if args.check else 'Generated'} {len(outputs)} translation/language files")
