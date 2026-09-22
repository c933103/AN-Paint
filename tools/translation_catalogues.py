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
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "translations"
RES = ROOT / "Paintroid/src/main/res"

FORMAT_TOKEN = re.compile(
    r"%(?:\\d+\\$)?[-+# 0,(<]*(?:\\d+)?(?:\\.\\d+)?[a-zA-Z%]"
)


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
    return Counter(FORMAT_TOKEN.findall(value))


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

    for name, quantities in plurals.items():
        if name not in default_plurals:
            errors.append(f"{tag}: unknown plural key {name}")
            continue
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
    errors: list[str] = []
    paths = catalogue_paths()
    tags = offered_tags()
    for tag in tags:
        if tag.startswith("en-"):
            continue
        if tag not in paths:
            errors.append(f"{tag}: offered language has no exact canonical catalogue")
            continue
        errors.extend(validate_catalogue(tag, require_complete=require_complete))
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
