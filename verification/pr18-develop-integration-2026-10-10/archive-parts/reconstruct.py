#!/usr/bin/env python3
"""Reconstruct the exact original API35 artifact from its verified binary parts."""
import argparse
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("output", nargs="?", type=Path, default=root.parent / "api35-original.zip")
args = parser.parse_args()
manifest = json.loads((root / "manifest.json").read_text())
chunks = []
for entry in manifest["parts"]:
    data = (root / entry["name"]).read_bytes()
    if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise ValueError("Part integrity mismatch: " + entry["name"])
    git_sha = hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()
    if git_sha != entry["git_blob"]:
        raise ValueError("Part Git identity mismatch: " + entry["name"])
    chunks.append(data)
data = b"".join(chunks)
if len(data) != manifest["bytes"] or hashlib.sha256(data).hexdigest() != manifest["sha256"]:
    raise ValueError("Reconstructed artifact mismatch")
if args.output.exists() and args.output.read_bytes() != data:
    raise FileExistsError("Refusing to overwrite a different file: " + str(args.output))
args.output.write_bytes(data)
print(str(args.output), len(data), manifest["sha256"])
