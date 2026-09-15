#!/usr/bin/env python3
"""Rebuild audited shared vocabulary from exact, pinned Paintroid translation XML."""
import argparse
import gimp_translations
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


def qualifier_for_tag(tag):
    """Use an unambiguous Android BCP-47 directory for a language tag."""
    return "values-b+" + tag.replace("-", "+")


def generate():
    index = json.loads((DATA / "upstream-index.json").read_text())
    mapping = json.loads((DATA / "common-terms.json").read_text())
    base = read_strings(DATA / "upstream/values.xml")
    android = json.loads((DATA / "android-actions.json").read_text())["locales"]
    reviewed = json.loads((DATA / "reviewed-actions.json").read_text())["locales"]
    local = json.loads((DATA / "local-translations.json").read_text())
    defaults = {}
    for path in sorted((RES / "values").glob("*.xml")):
        defaults.update(read_strings(path))
    def normal(value):
        return value.strip().strip('"').replace("\\'", "'").rstrip(":：").casefold()
    gimp = gimp_translations.load(defaults)
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
        terms.update(gimp.get(tag, {}))
        terms.update({key: corrected for key, (_, corrected) in corrections.items()})
        android_terms = android.get(tag, {}).get("strings", {})
        terms.update(android_terms)
        terms.update(reviewed.get(tag, {}))
        terms.update(local.get(tag, {}))
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
        distinct += sum(1 for key in set(reviewed.get(tag, {})) | set(local.get(tag, {}))
                        if key not in mapping and normal(terms[key]) != normal(defaults.get(key, "")))
        included = distinct > 0 or tag.startswith("en-")
        record = {"original_qualifier": qualifier, "language_tag": tag,
                  "reused_entries": sum(1 for key in terms if key in mapping and key not in corrections and key not in gimp.get(tag, {}) and key not in android_terms and key not in reviewed.get(tag, {}) and key not in local.get(tag, {})),
                  "gimp_translation_entries": len(gimp.get(tag, {})),
                  "local_translation_entries": len(local.get(tag, {})),
                  "android_action_entries": len(android_terms), "reviewed_action_entries": len(reviewed.get(tag, {})), "entries_different_from_upstream_english": distinct,
                  "offered_in_app": included, "blob_sha": digest,
                  "source_sha256": hashlib.sha256(raw).hexdigest()}
        if corrections:
            record["locally_corrected_entries"] = list(corrections)
        if included:
            tags.append(tag)
            lines = ['<?xml version="1.0" encoding="utf-8"?>',
                     '<!-- Shared vocabulary: Paintroid (AGPL-3.0+) and GIMP translators (GPL-3.0+).',
                     'Generated by tools/reuse_upstream_translations.py. See translations/README.md. -->',
                     '<resources>']
            for key, value in terms.items():
                # Android's numeric slider already supplies its own punctuation.
                if key == "ui_quality":
                    value = value.rstrip().rstrip(":：").rstrip()
                value = value.replace("'", "\\'") if "\\'" not in value else value
                lines.append(f'    <string name="{key}">{escape(value)}</string>')
            lines += ['</resources>', '']
            target = RES / output_qualifier / "strings.xml"
            results[target] = "\n".join(lines)
            record["generated_resource"] = str(target.relative_to(ROOT))
        coverage.append(record)
    # Additional locally maintained script/locale foundations.
    for qualifier, tag in (("values-b+lzh+Hant", "lzh-Hant"), ("values-b+mn+Mong", "mn-Mong"), ("values-zh-rHK", "zh-HK"), ("values-b+mn+Cyrl+MN", "mn-Cyrl-MN")):
        tags.append(tag)
        lines = ['<?xml version="1.0" encoding="utf-8"?>',
                 '<!-- Locally maintained translation foundation; see translations/README.md. -->',
                 '<resources>']
        for key, value in {**gimp.get(tag, {}), **local[tag]}.items():
            value = value.replace("'", "\\'") if "\\'" not in value else value
            lines.append(f'    <string name="{key}">{escape(value)}</string>')
        results[RES / qualifier / "strings.xml"] = '\n'.join(lines + ['</resources>', ''])
        coverage.append({"language_tag": tag, "local_translation_entries": len(local[tag]),
                         "entries_different_from_upstream_english": sum(normal(v) != normal(defaults.get(k, "")) for k,v in local[tag].items()),
                         "generated_resource": str((RES / qualifier / "strings.xml").relative_to(ROOT)),
                         "catalogue_source": "translations/local-translations.json"})
    catalogue = json.loads((DATA / "language-options.json").read_text())
    options = {item["tag"]: item for item in catalogue["options"]}
    basic = json.loads((DATA / "basic-translations.json").read_text())
    transcription = json.loads((DATA / "tatar-transcription.json").read_text())["cyrillic_to_latin"]
    basic["tt-Latn"] = {key: transcription[value] for key, value in basic["tt"].items()}
    for tag, terms in basic.items():
        if tag in tags:
            raise ValueError(f"Basic translation duplicates an existing catalogue: {tag}")
        basic_option = options.get(tag) or next((item for item in options.values() if item.get("translation_base") == tag), None)
        if basic_option is None:
            raise ValueError(f"Basic translation is not offered: {tag}")
        if (not terms and not basic_option.get("name_only")) or any(not value.strip() for value in terms.values()):
            raise ValueError(f"Basic translation is empty: {tag}")
        tags.append(tag)
        lines = ['<?xml version="1.0" encoding="utf-8"?>',
                 '<!-- Starter translation; native-speaker review is welcome. See translations/README.md. -->',
                 '<resources>']
        rendered_terms = {**terms, **gimp.get(tag, {})}
        if "ui_save" in rendered_terms:
            rendered_terms["ui_save_a5d0d9"] = "@string/ui_save"
        if "ui_discard_changes23" in rendered_terms and "ui_keep_editing23" not in rendered_terms:
            rendered_terms["ui_keep_editing23"] = rendered_terms.get("ui_cancel", "Cancel")
        for key, value in rendered_terms.items():
            if key not in defaults:
                raise ValueError(f"Unknown basic translation resource: {tag}/{key}")
            value = value.replace("'", "\\'") if "\\'" not in value else value
            lines.append(f'    <string name="{key}">{escape(value)}</string>')
        target = RES / qualifier_for_tag(tag) / "strings.xml"
        results[target] = '\n'.join(lines + ['</resources>', ''])
        record = next((row for row in coverage if row["language_tag"] == tag), None)
        if record is None:
            record = {"language_tag": tag}
            coverage.append(record)
        record.update({"starter_translation_entries": len(terms), "gimp_translation_entries": len(gimp.get(tag, {})),
                       "entries_different_from_upstream_english": sum(normal(v) != normal(defaults[k]) for k,v in terms.items()),
                       "generated_resource": str(target.relative_to(ROOT)),
                       "catalogue_source": "translations/tatar-transcription.json" if tag == "tt-Latn" else "translations/basic-translations.json",
                       "name_only": bool(basic_option.get("name_only"))})
    # GIMP-only languages use their selected catalogue directly; no unrelated
    # starter vocabulary or claimed full-interface translation is synthesized.
    for tag, terms in gimp.items():
        if tag in tags or tag not in options:
            continue
        tags.append(tag)
        rendered_terms = dict(terms)
        if "ui_save" in terms:
            rendered_terms["ui_save_a5d0d9"] = "@string/ui_save"
        if "ui_discard_changes23" in terms and "ui_keep_editing23" not in terms:
            rendered_terms["ui_keep_editing23"] = terms.get("ui_cancel", "Cancel")
        lines = ['<?xml version="1.0" encoding="utf-8"?>',
                 '<!-- Selected GIMP vocabulary, GPL-3.0-or-later; see translations/README.md. -->', '<resources>']
        for key, value in rendered_terms.items():
            lines.append(f'    <string name="{key}">{escape(value)}</string>')
        target = RES / qualifier_for_tag(tag) / "strings.xml"
        results[target] = '\n'.join(lines + ['</resources>', ''])
        coverage.append({"language_tag": tag, "entries_different_from_upstream_english":
                         sum(normal(v) != normal(defaults.get(k, "")) for k,v in terms.items()),
                         "generated_resource": str(target.relative_to(ROOT)),
                         "catalogue_source": "translations/gimp-catalogues.json"})
    # Complete only the requested menu surface, with explicit regional/script
    # resources. Keep the existing vocabulary for the rest of each interface.
    menu_catalogue = json.loads((DATA / "main-menu-translations.json").read_text())
    for tag, menu_terms in menu_catalogue["locales"].items():
        if not set(menu_catalogue["required_keys"]) <= set(menu_terms):
            raise ValueError(f"Incomplete menu translation: {tag}")
        if not set(menu_terms) <= set(defaults):
            raise ValueError(f"Unknown menu resource: {tag}/{set(menu_terms)-set(defaults)}")
        record = next((row for row in coverage if row["language_tag"] == tag), None)
        base_tag = options[tag].get("translation_base", tag)
        base_record = next((row for row in coverage if row["language_tag"] == base_tag), None)
        target = ROOT / record["generated_resource"] if record else RES / qualifier_for_tag(tag) / "strings.xml"
        inherited = results.get(ROOT / base_record["generated_resource"], "<resources/>") if base_record else "<resources/>"
        terms = {node.get("name"): "".join(node.itertext()) for node in ET.fromstring(inherited)}
        for key, value in menu_terms.items():
            if not value.strip():
                raise ValueError(f"Empty menu translation: {tag}/{key}")
            terms[key] = value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        terms["ui_save_a5d0d9"] = "@string/ui_save"
        lines = ['<?xml version="1.0" encoding="utf-8"?>',
                 '<!-- Generated menu completion plus retained vocabulary; see translations/README.md. -->', '<resources>']
        for key, value in terms.items():
            literal = ' formatted="false"' if key in menu_terms else ''
            lines.append(f'    <string name="{key}"{literal}>{escape(value)}</string>')
        results[target] = '\n'.join(lines + ['</resources>', ''])
        if record is None:
            record = {"language_tag": tag, "inherited_translation_base": base_tag}
            coverage.append(record)
            tags.append(tag)
        record.update({"generated_resource": str(target.relative_to(ROOT)),
                       "menu_translation_entries": len(menu_terms), "main_menu_complete": True,
                       "entries_different_from_upstream_english": sum(normal(v) != normal(defaults.get(k, "")) for k,v in terms.items())})
        options[tag]["translation_base"] = tag
    translated = set(tags)
    for tag, item in options.items():
        if not item.get("name_only") and item.get("translation_base", tag) not in translated:
            raise ValueError(f"Language option has no translation base: {tag}")
    tags = [catalogue["pinned_first"]] + sorted(set(options) - {catalogue["pinned_first"]}, key=str.casefold)
    for record in coverage:
        available_gimp = gimp.get(record["language_tag"], {})
        record["gimp_available_entries"] = len(available_gimp)
        rendered_path = ROOT / record.get("generated_resource", "")
        rendered = {node.get("name"): "".join(node.itertext()) for node in ET.fromstring(results[rendered_path])} if rendered_path in results else {}
        record["gimp_translation_entries"] = sum(rendered.get(key) == value for key, value in available_gimp.items())
        record["offered_tags"] = [tag for tag in tags if options[tag].get("translation_base", tag) == record["language_tag"]]
        record["offered_in_app"] = bool(record["offered_tags"])
    # New regional English choices inherit the same UI, with explicit spelling
    # rather than depending on Android's region fallback order.
    english_overrides = {node.get("name") for q in ("values-en-rAU", "values-en-rCA", "values-en-rGB")
                         for node in ET.fromstring(results[RES / q / "strings.xml"])}
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
        results[RES / qualifier / "strings.xml"] = '\n'.join(lines + ['</resources>', ''])
        coverage.append({"language_tag": tag, "english_variant": True,
                         "offered_tags": [tag], "offered_in_app": True,
                         "generated_resource": str((RES / qualifier / "strings.xml").relative_to(ROOT))})
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
