"""Exact successor scope for M02; historical Copy-credit/F01 guards stay pinned."""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_SHA256 = "a2358aca0d192313bc554269f2f2a03fc0dc07267f4e5f735920a01a86b5249a"


def fixture():
    raw = (ROOT / "tools/fixtures/commons_metadata_http_scope.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != FIXTURE_SHA256:
        raise AssertionError("The pinned M02 single-message scope changed")
    return json.loads(raw)


def before_m02_catalogue(path, text):
    entries = {row["path"]: row for row in fixture()["entries"]}
    if path not in entries:
        return text
    line = entries[path]["line"]
    if text.count(line) != 1:
        raise AssertionError(f"{path}: expected exactly one approved M02 addition")
    return text.replace(line, "", 1)


def before_m02_producer(path, content):
    if path.endswith("/CommonsAttribution.kt"):
        text = content.decode()
        declaration = "    /** Application-owned metadata status only; localize at the alive UI boundary. */\n    class HttpException(val status: Int): IOException()\n\n"
        if text.count(declaration) != 1 or text.count("throw HttpException(status)") != 1:
            raise AssertionError("Expected the exact M02 producer delta")
        return text.replace(declaration, "", 1).replace("throw HttpException(status)", 'throw IOException("Commons metadata: HTTP $status")', 1).encode()
    return content
