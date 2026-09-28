#!/usr/bin/env python3
"""Read and validate AN Paint's canonical Android translation catalogues.

Localized Paintroid/src/main/res/values*/strings.xml files are source files,
not generated output. Files under translations/ are provenance/reference
material only.
"""
from __future__ import annotations

from collections import Counter
import pathlib
import re
import unicodedata
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "translations"
RES = ROOT / "Paintroid/src/main/res"

FORMAT_TOKEN = re.compile(
    r"(?:%\d+\$[-+# 0,(<]*(?:\d+)?(?:\.\d+)?[bBhHsScCdoxXeEfgGaAtT%n]|%%)"
)

# These are syntax/licence identifiers, not prose to be translated.
LITERAL_TOKENS = ("data:image/png;base64,", "CC BY-SA 4.0")
GIF_LIMIT = re.compile(r"(?<!\d)65(?:[,.'’\u066c\u0020\u00a0\u202f\u2009]?535)(?!\d)")


def android_string_errors(value: str) -> list[str]:
    """Check Android quoting after XML entities have been decoded.

    A literal apostrophe is legal inside Android double quotes, or when escaped.
    XML &apos; alone does not escape it for the Android resource compiler.
    """
    quoted = False
    escaped = False
    errors = []
    for char in value:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            quoted = not quoted
        elif char == "'" and not quoted:
            errors.append("unescaped Android apostrophe")
    return sorted(set(errors))


def format_string_errors(value: str, formatted: bool = True) -> list[str]:
    """Require explicit literal-percent handling before AAPT or String.format.

    formatted=false bypasses AAPT's check, not runtime formatting. A value with
    argument placeholders must still escape literal percent signs as %%.
    """
    if "%" not in FORMAT_TOKEN.sub("", value):
        return []
    if placeholders(value):
        return ["literal percent in a format string must use %%"]
    if formatted:
        return ['literal percent requires formatted="false"']
    return []


def resource_configuration(folder: str) -> tuple[str, ...]:
    """Normalize legacy and BCP-47 Android locale directory equivalents.

    Non-language qualifiers remain part of the configuration: values-fr-night
    must not collide with values-fr. Android's legacy language aliases are
    normalized too (in/id, iw/he and ji/yi).
    """
    parts = folder.split("-")[1:]
    aliases = {"in": "id", "iw": "he", "ji": "yi"}
    if parts and parts[0].startswith("b+"):
        locale = parts.pop(0)[2:].split("+")
        language = aliases.get(locale[0].lower(), locale[0].lower())
        return ("locale=" + "-".join([language, *locale[1:]]).lower(), *parts)
    if parts and re.fullmatch(r"[a-z]{2,3}", parts[0]) and parts[0] not in ("car",):
        language = parts.pop(0)
        language = aliases.get(language, language)
        locale = [language]
        if parts and re.fullmatch(r"r(?:[A-Z]{2}|\d{3})", parts[0]):
            locale.append(parts.pop(0)[1:])
        return ("locale=" + "-".join(locale).lower(), *parts)
    return tuple(parts)


def validate_resource_directories() -> list[str]:
    """Reject ambiguous canonical directories before catalogue_paths can hide one."""
    seen = {}
    errors = []
    for folder in sorted(RES.glob("values*")):
        if not folder.is_dir() or not (folder / "strings.xml").is_file():
            continue
        config = resource_configuration(folder.name)
        if config in seen:
            errors.append(f"equivalent resource directories: {seen[config]} and {folder.name}")
        else:
            seen[config] = folder.name
    return errors


def validate_android_strings() -> list[str]:
    """Check every string, plural form and string-array, including unoffered locales."""
    errors = []
    for path in sorted(RES.glob("values*/*.xml")):
        for node in ET.parse(path).getroot():
            if node.tag == "string":
                values = [(node.get("name"), "".join(node.itertext()), node.get("formatted") != "false")]
            elif node.tag in ("plurals", "string-array"):
                values = [
                    (f"{node.get('name')}[{item.get('quantity', str(i))}]", "".join(item.itertext()),
                     item.get("formatted", node.get("formatted")) != "false")
                    for i, item in enumerate(node.findall("item"))
                ]
            else:
                continue
            for key, value, formatted in values:
                for error in android_string_errors(value) + format_string_errors(value, formatted):
                    errors.append(f"{path.parent.name}/{key}: {error}")
    return errors


def literal_token_errors(key: str, value: str, source: str) -> list[str]:
    errors = [f"missing literal {token!r}" for token in LITERAL_TOKENS
              if token in source and token not in value]
    if key == "save20_gif_size_limit":
        # Keep the value exact while accepting local digits and grouping styles.
        digits = "".join(str(unicodedata.decimal(c)) if c.isdecimal() else c for c in value)
        if not GIF_LIMIT.search(digits):
            errors.append("GIF limit must be the intact number 65535 (localized grouping is allowed)")
    return errors


def read_strings(path: pathlib.Path) -> dict[str, str]:
    """Return string resources from one XML file."""
    return {
        node.get("name"): "".join(node.itertext())
        for node in ET.parse(path).getroot()
        if node.tag == "string"
    }


def read_plurals(path: pathlib.Path) -> dict[str, dict[str, str]]:
    """Return plural resources from one XML file."""
    return {
        node.get("name"): {
            item.get("quantity"): "".join(item.itertext())
            for item in node.findall("item")
        }
        for node in ET.parse(path).getroot()
        if node.tag == "plurals"
    }


def default_resources():
    """Return the canonical English resource set and translatability metadata."""
    strings: dict[str, str] = {}
    plurals: dict[str, dict[str, str]] = {}
    translatable_strings: set[str] = set()
    translatable_plurals: set[str] = set()
    for path in sorted((RES / "values").glob("*.xml")):
        root = ET.parse(path).getroot()
        for node in root:
            name = node.get("name")
            if node.tag == "string":
                strings[name] = "".join(node.itertext())
                if node.get("translatable") != "false":
                    translatable_strings.add(name)
            elif node.tag == "plurals":
                plurals[name] = {
                    item.get("quantity"): "".join(item.itertext())
                    for item in node.findall("item")
                }
                if node.get("translatable") != "false":
                    translatable_plurals.add(name)
    return strings, plurals, translatable_strings, translatable_plurals


def tag_from_qualifier(name: str) -> str | None:
    if name == "values":
        return None
    if name.startswith("values-b+"):
        return name.removeprefix("values-b+").replace("+", "-")
    raw = name.removeprefix("values-")
    raw = raw.replace("-r", "-")
    return {"in": "id", "iw": "he"}.get(raw, raw)


def catalogue_paths() -> dict[str, pathlib.Path]:
    """Map exact BCP-47 tags to the active canonical strings.xml."""
    result: dict[str, pathlib.Path] = {}
    for folder in sorted(RES.glob("values*")):
        if not folder.is_dir():
            continue
        path = folder / "strings.xml"
        if not path.is_file():
            continue
        tag = tag_from_qualifier(folder.name)
        if tag:
            if tag not in result or folder.name.startswith("values-b+"):
                result[tag] = path
    return result


def qualifier_for_tag(tag: str) -> str:
    """Return the preferred Android BCP-47 resource directory for a new locale."""
    return "values-b+" + tag.replace("-", "+")


def offered_tags() -> list[str]:
    return [
        node.text
        for node in ET.parse(RES / "values/app_language_tags.xml").findall(".//item")
    ]


def placeholders(value: str) -> Counter[str]:
    # %% produces a literal character and consumes no argument. A translation
    # may use a percent sign where English spells out the word (or vice versa).
    return Counter(token for token in FORMAT_TOKEN.findall(value) if not token.endswith(("%", "n")))


def validate_catalogue(tag: str, require_complete: bool = False) -> list[str]:
    """Return validation errors for one canonical locale catalogue."""
    paths = catalogue_paths()
    path = paths.get(tag)
    if path is None:
        return [f"{tag}: no strings.xml catalogue"]

    defaults, default_plurals, translatable, translatable_plurals = default_resources()
    strings = read_strings(path)
    plurals = read_plurals(path)
    errors: list[str] = []

    unknown = sorted(set(strings) - set(defaults))
    if unknown:
        errors.append(f"{tag}: unknown string keys: {', '.join(unknown)}")

    if require_complete:
        missing = sorted(translatable - set(strings))
        if missing:
            errors.append(f"{tag}: missing {len(missing)} strings: {', '.join(missing[:20])}")
        missing_plurals = sorted(translatable_plurals - set(plurals))
        if missing_plurals:
            errors.append(f"{tag}: missing plural resources: {', '.join(missing_plurals)}")

    for key, value in strings.items():
        if key not in defaults:
            continue
        if placeholders(value) != placeholders(defaults[key]):
            errors.append(
                f"{tag}/{key}: format placeholders {dict(placeholders(value))} "
                f"!= English {dict(placeholders(defaults[key]))}"
            )
        for error in literal_token_errors(key, value, defaults[key]):
            errors.append(f"{tag}/{key}: {error}")

    for name, quantities in plurals.items():
        if name not in default_plurals:
            errors.append(f"{tag}: unknown plural key {name}")
            continue
        if "other" not in quantities:
            errors.append(f"{tag}/{name}: missing required Android other plural quantity")
        for quantity in quantities:
            if quantity not in {"zero", "one", "two", "few", "many", "other"}:
                errors.append(f"{tag}/{name}: invalid plural quantity {quantity!r}")
        english_tokens = Counter()
        for value in default_plurals[name].values():
            english_tokens |= placeholders(value)
        for quantity, value in quantities.items():
            if placeholders(value) != english_tokens:
                errors.append(
                    f"{tag}/{name}[{quantity}]: format placeholders "
                    f"{dict(placeholders(value))} != English {dict(english_tokens)}"
                )

    return errors


def validate_all(require_complete: bool = False) -> list[str]:
    errors = validate_resource_directories() + validate_android_strings()
    paths = catalogue_paths()
    tags = offered_tags()
    for tag in tags:
        if tag not in paths:
            errors.append(f"{tag}: offered language has no exact canonical catalogue")
            continue
        errors.extend(validate_catalogue(tag, require_complete=require_complete))
    for tag in sorted(set(paths) - set(tags)):
        errors.extend(validate_catalogue(tag, require_complete=False))
    return errors


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--complete", action="store_true",
                        help="also require every translatable English key in every offered locale")
    args = parser.parse_args()
    failures = validate_all(require_complete=args.complete)
    if failures:
        raise SystemExit("\n".join(failures))
    print("Canonical translation catalogues are structurally valid"
          + (" and complete" if args.complete else ""))
