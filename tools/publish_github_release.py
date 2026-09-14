"""Publish a completed, fully tested APK with its privately produced public signature."""
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from apk_release_patch import apply, digest


CERT = "f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791"


def run(*args):
    return subprocess.check_output([str(a) for a in args], text=True).strip()


def api(path):
    return json.loads(run("gh", "api", path))


def verify_jobs(workflow, jobs, commit):
    if (workflow["head_sha"] != commit or workflow["conclusion"] != "success"
            or workflow["path"] != ".github/workflows/android.yml"
            or workflow["event"] != "push" or workflow["head_branch"] != "develop"):
        raise ValueError("Release must use the successful develop build of the declared commit")
    required = {"Regression tests and lint", "Build APK and corresponding source", "Emulator API 30", "Emulator API 35"}
    completed = {job["name"] for job in jobs if job["status"] == "completed" and job["conclusion"] == "success"}
    if not required <= completed:
        raise ValueError("Release verification is incomplete: " + ", ".join(sorted(required - completed)))


def main(request_path):
    request = json.loads(request_path.read_text())
    version, commit, run_id = request["version"], request["commit"], int(request["run_id"])
    if not re.fullmatch(r"\d+\.\d+\.\d+", version) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Invalid release identity")
    repo = os.environ["GITHUB_REPOSITORY"]
    endpoint = f"repos/{repo}/actions/runs/{run_id}"
    workflow = api(endpoint)
    jobs = api(endpoint + "/jobs?per_page=100")["jobs"]
    verify_jobs(workflow, jobs, commit)
    base = Path("build/github-release"); base.mkdir(parents=True, exist_ok=True)
    ci = base / "ci"
    run("gh", "run", "download", run_id, "--repo", repo, "--name", f"apk-and-source-{commit}", "--dir", ci)
    info = json.loads((ci / "build/delivery/build-info.json").read_text())
    if info["commit"] != commit or int(info["run_id"]) != run_id or info["build_variant"] != "release":
        raise ValueError("CI artifact identity or release variant mismatch")
    original = (ci / "app/build/outputs/apk/release/app-release.apk").read_bytes()
    if digest(original) != info["apk_sha256"]:
        raise ValueError("Original CI APK hash mismatch")
    patch = json.loads(request_path.with_name(f"{version}-signing.json").read_text())
    signed = apply(original, patch)
    if digest(signed) != request["apk_sha256"]:
        raise ValueError("Requested release APK hash mismatch")
    apk = base / f"AN-Paint-{version}.apk"; apk.write_bytes(signed)
    source = base / f"AN-Paint-{version}-source.zip"
    with zipfile.ZipFile(apk) as archive:
        source.write_bytes(archive.read("assets/local-source/AN-Paint-source.zip"))
        abis = {n.split("/")[1] for n in archive.namelist() if n.startswith("lib/") and n.endswith(".so")}
    if abis != {"arm64-v8a", "armeabi-v7a", "x86_64", "x86"} or digest(source.read_bytes()) != info["source_sha256"]:
        raise ValueError("Universal ABI or matching source verification failed")
    verification = ci / "verification-tools"
    for name in ("zipalign", "aapt2"):
        (verification / name).chmod(0o755)
    signature = run("java", "-jar", verification / "apksigner.jar", "verify", "--verbose", "--print-certs", apk)
    if CERT not in signature:
        raise ValueError("Release is not signed with the existing upgrade certificate")
    run(verification / "zipalign", "-c", "-P", "16", "4", apk)
    metadata = run(verification / "aapt2", "dump", "badging", apk)
    if ("application-debuggable" in metadata or "name='paint.anpaint.android'" not in metadata
            or f"versionName='{version}'" not in metadata or f"versionCode='{request['version_code']}'" not in metadata):
        raise ValueError("Release package, version or debuggability mismatch")
    evidence = base / f"AN-Paint-{version}-verification.json"
    evidence.write_text(json.dumps({**request, "source_sha256": digest(source.read_bytes()),
        "signing_certificate_sha256": CERT, "payload_matches_tested_apk": True,
        "signature_verification": signature, "apk_metadata": metadata,
        "workflow": workflow, "jobs": jobs}, indent=2) + "\n")
    checksums = base / "SHA256SUMS.txt"
    assets = [apk, source, evidence]
    checksums.write_text("".join(f"{digest(p.read_bytes())}  {p.name}\n" for p in assets))
    notes = request_path.with_name(f"{version}-notes.md")
    tag = "v" + version
    run("gh", "release", "create", tag, "--repo", repo, "--target", commit,
        "--title", f"AN Paint {version}", "--notes-file", notes, "--draft")
    run("gh", "release", "upload", tag, "--repo", repo, *assets, checksums)
    run("gh", "release", "edit", tag, "--repo", repo, "--draft=false", "--latest")
    print(run("gh", "release", "view", tag, "--repo", repo, "--json", "url,assets"))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
