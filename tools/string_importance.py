#!/usr/bin/env python3
"""Validate AN Paint translation priorities and report direct key presence.

This never rewrites canonical Android resources. Priority is independent of
linguistic review, translation quality, or Android's inherited locale fallback.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import translation_catalogues as catalogues

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "translations/string-importance.json"
SOURCE = "Paintroid/src/main/res/values/strings.xml"
TIERS = ("P0", "P1", "P2", "P3")
RESOURCE_TAGS = frozenset(("string", "plurals", "string-array"))
RESOURCE_NAME = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")


def resource_identities(path: Path, *, translatable_only: bool = True) -> set[tuple[str, str]]:
    """Read typed Android identities; plural and array each count as one."""
    result: set[tuple[str, str]] = set()
    for element in ET.parse(path).getroot():
        if element.tag not in RESOURCE_TAGS:
            continue
        if translatable_only and element.get("translatable") == "false":
            continue
        name = element.get("name")
        if not name or not RESOURCE_NAME.fullmatch(name):
            raise ValueError(f"{path}: malformed resource name {name!r}")
        identity = (element.tag, name)
        if identity in result:
            raise ValueError(f"{path}: duplicate resource {element.tag}/{name}")
        result.add(identity)
    return result


def resource_names(path: Path, *, translatable_only: bool = True) -> set[str]:
    return {name for _, name in resource_identities(path, translatable_only=translatable_only)}


def default_resource_types() -> dict[str, str]:
    """Resolve manifest names to types, rejecting ambiguous canonical names."""
    resources: dict[str, str] = {}
    for path in sorted((catalogues.RES / "values").glob("*.xml")):
        for kind, name in sorted(resource_identities(path)):
            if name in resources:
                if resources[name] == kind:
                    raise ValueError(f"{path}: duplicate default resource {kind}/{name}")
                raise ValueError(f"{path}: ambiguous default key {name}: "
                                 "bare-name manifest cannot represent multiple resource types")
            resources[name] = kind
    return resources


def default_resource_names() -> set[str]:
    """Find every translatable default entry, not only entries in strings.xml."""
    return set(default_resource_types())


def load_manifest(path: Path = MANIFEST) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate(manifest: dict, source: set[str] | None = None) -> list[str]:
    """Fail closed on missing, duplicate, stale, out-of-order or malformed tiers."""
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["priority manifest must be an object"]
    if set(manifest) != {"schema_version", "source_catalogue", "tiers"}:
        errors.append("priority manifest has unexpected or missing top-level fields")
    if type(manifest.get("schema_version")) is not int or manifest.get("schema_version") != 1:
        errors.append("unsupported priority manifest schema_version")
    if manifest.get("source_catalogue") != SOURCE:
        errors.append("source_catalogue must point to the canonical English strings.xml")
    tiers = manifest.get("tiers")
    if not isinstance(tiers, list) or len(tiers) != len(TIERS):
        return errors + ["tiers must be a four-element list (P0, P1, P2, P3)"]
    if source is None:
        source = default_resource_names()
    if not isinstance(source, set) or not all(isinstance(s, str) for s in source):
        return errors + ["source resource names must be a set of strings"]

    seen: dict[str, str] = {}
    for index, tier in enumerate(tiers):
        if not isinstance(tier, dict) or set(tier) != {"id", "title", "scope", "keys"}:
            errors.append(f"tier {index}: malformed tier record")
            continue
        ident = tier["id"]
        if ident != TIERS[index]:
            errors.append(f"tier {index}: expected id {TIERS[index]!r}, got {ident!r}")
        if not all(isinstance(tier[x], str) and tier[x].strip() for x in ("title", "scope")):
            errors.append(f"tier {index}: title and scope must be nonempty strings")
        keys = tier["keys"]
        if not isinstance(keys, list) or not keys or not all(isinstance(k, str) for k in keys):
            errors.append(f"tier {index}: keys must be a nonempty list of strings")
            continue
        if keys != sorted(keys):
            errors.append(f"tier {index}: keys must be alphabetically sorted")
        for key in keys:
            if not RESOURCE_NAME.fullmatch(key):
                errors.append(f"tier {index}: invalid resource key {key!r}")
                continue
            if key in seen:
                errors.append(f"{key}: assigned to both {seen[key]} and {ident}")
            else:
                seen[key] = str(ident)

    missing = source - seen.keys()
    stale = seen.keys() - source
    if missing:
        errors.append(f"{len(missing)} unclassified translatable keys: {', '.join(sorted(missing))}")
    if stale:
        errors.append(f"{len(stale)} unknown/nontranslatable keys: {', '.join(sorted(stale))}")
    return errors


def tier_counts(manifest: dict) -> dict[str, int]:
    return {tier["id"]: len(tier["keys"]) for tier in manifest["tiers"]}


def locale_coverage(manifest: dict, tag: str, include_missing: bool = False) -> dict:
    """Count explicit same-tag entries only (not translated or reviewed status)."""
    if tag not in catalogues.offered_tags():
        raise ValueError(f"Unknown offered locale {tag!r}")
    path = catalogues.catalogue_paths().get(tag)
    if path is None:
        raise ValueError(f"No exact canonical catalogue for {tag!r}")
    identities = resource_identities(path, translatable_only=False)
    source_types = default_resource_types()
    present = {name for name, kind in source_types.items() if (kind, name) in identities}
    result = {}
    for tier in manifest["tiers"]:
        keys = set(tier["keys"])
        missing = sorted(keys - present)
        row = {"present": len(keys) - len(missing), "missing": len(missing), "total": len(keys)}
        if include_missing:
            row["missing_keys"] = missing
        result[tier["id"]] = row
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--locale", metavar="BCP47", help="direct coverage of one offered locale")
    scope.add_argument("--all-locales", action="store_true", help="direct coverage of all offered locales")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--missing-keys", action="store_true", help="show missing keys (requires --locale)")
    args = parser.parse_args()
    if args.missing_keys and not args.locale:
        parser.error("--missing-keys requires --locale")
    try:
        manifest = load_manifest()
        source = default_resource_names()
        errors = validate(manifest, source)
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        if args.locale:
            result = {args.locale: locale_coverage(manifest, args.locale, args.missing_keys)}
        elif args.all_locales:
            result = {tag: locale_coverage(manifest, tag) for tag in catalogues.offered_tags()}
        else:
            result = {"source_entries": len(source), "tier_counts": tier_counts(manifest)}
    except (OSError, ValueError, ET.ParseError, json.JSONDecodeError) as exc:
        print("ERROR:", exc)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.locale or args.all_locales:
        for tag, tiers in result.items():
            print(f"{tag} — direct catalogue presence only (not translation quality/review)")
            for ident in TIERS:
                entry = tiers[ident]
                print(f"  {ident}: {entry['present']}/{entry['total']} present; {entry['missing']} missing")
                if args.missing_keys:
                    for key in entry["missing_keys"]:
                        print(f"    {key}")
    else:
        print(f"{result['source_entries']} translatable source entries, classified exactly once")
        for ident, count in result["tier_counts"].items():
            print(f"  {ident}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
