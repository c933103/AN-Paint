"""Transfer public APK signing/alignment bytes without transferring a signing key.

The small JSON patch copies unchanged compressed ZIP payloads from the CI APK.
It carries only the remaining public APK bytes. Both whole-file hashes and every
non-signature ZIP entry must match; this cannot silently replace application code.
"""
import argparse
import base64
import hashlib
import io
import json
import re
import struct
import zipfile
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def same_payload(before, after):
    signature = re.compile(r"META-INF/(MANIFEST\.MF|[^/]+\.(SF|RSA|DSA|EC))$")
    def entries(data):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if len(archive.namelist()) != len(set(archive.namelist())):
                raise ValueError("Duplicate APK entries")
            return {n: digest(archive.read(n)) for n in archive.namelist() if not signature.fullmatch(n)}
    if entries(before) != entries(after):
        raise ValueError("The signed APK changed application payload")


def compressed_range(data, entry):
    start = entry.header_offset
    if data[start:start + 4] != b"PK\x03\x04":
        raise ValueError("Invalid local ZIP header")
    name, extra = struct.unpack_from("<HH", data, start + 26)
    start += 30 + name + extra
    return start, start + entry.compress_size


def create(before, after):
    same_payload(before, after)
    parts = []
    def literal(data):
        if data:
            parts.append({"data": base64.b64encode(data).decode("ascii")})
    with zipfile.ZipFile(io.BytesIO(before)) as old, zipfile.ZipFile(io.BytesIO(after)) as new:
        previous = {entry.filename: entry for entry in old.infolist()}
        cursor = 0
        for entry in sorted(new.infolist(), key=lambda e: e.header_offset):
            start, end = compressed_range(after, entry)
            original = previous.get(entry.filename)
            if original is None:
                continue
            old_start, old_end = compressed_range(before, original)
            if end > start and after[start:end] == before[old_start:old_end]:
                literal(after[cursor:start])
                parts.append({"copy": [old_start, old_end - old_start]})
                cursor = end
        literal(after[cursor:])
    result = {"format": 1, "input_sha256": digest(before), "output_sha256": digest(after),
              "output_bytes": len(after), "parts": parts}
    if len(json.dumps(result)) > 2_000_000:
        raise ValueError("Signing patch unexpectedly large; inspect APK changes")
    return result


def apply(before, patch):
    if patch["format"] != 1 or digest(before) != patch["input_sha256"]:
        raise ValueError("Patch does not match the original CI APK")
    output = bytearray()
    for part in patch["parts"]:
        if set(part) == {"copy"}:
            start, length = part["copy"]
            if start < 0 or length < 0 or start + length > len(before):
                raise ValueError("Copy outside original APK")
            output.extend(before[start:start + length])
        elif set(part) == {"data"}:
            output.extend(base64.b64decode(part["data"], validate=True))
        else:
            raise ValueError("Invalid patch operation")
        if len(output) > patch["output_bytes"]:
            raise ValueError("Patch exceeds declared output size")
    output = bytes(output)
    if len(output) != patch["output_bytes"] or digest(output) != patch["output_sha256"]:
        raise ValueError("Signed APK hash mismatch")
    same_payload(before, output)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("signed", type=Path)
    parser.add_argument("patch", type=Path)
    args = parser.parse_args()
    original, signed = args.original.read_bytes(), args.signed.read_bytes()
    patch = create(original, signed)
    assert apply(original, patch) == signed
    args.patch.write_text(json.dumps(patch, separators=(",", ":")) + "\n")
    print(f"Verified public signing patch: {args.patch.stat().st_size} bytes")
