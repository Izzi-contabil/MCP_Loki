"""Exercise embedded MCP bytes through the shipped CLI, using synthetic PDF only."""

import base64
import hashlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfWriter

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins/loki-bootstrap/skills/operar-loki/scripts/loki_local.py"
)
URI = "loki://cases/CASE-SYNTHETIC/documents/DOC-SYNTHETIC"


def sample():
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=150)
    buffer = io.BytesIO()
    writer.write(buffer)
    content = buffer.getvalue()
    digest = hashlib.sha256(content).hexdigest()
    response = {
        "content": [
            {
                "type": "resource",
                "resource": {
                    "uri": URI,
                    "mimeType": "application/pdf",
                    "blob": base64.b64encode(content).decode(),
                    "_meta": {"sha256": digest, "filename": "../../PRIVATE_SYNTHETIC.pdf"},
                },
            }
        ],
        "structuredContent": {
            "case_id": "CASE-SYNTHETIC",
            "doc_id": "DOC-SYNTHETIC",
            "content_hash": digest,
            "size": len(content),
            "mime_type": "application/pdf",
            "filename": "../../PRIVATE_SYNTHETIC.pdf",
        },
    }
    return content, digest, response


def invoke(tmp_path, response, content, digest, *extra, audited=False):
    source = tmp_path / "response_masked.json"
    source.write_text(json.dumps(response))
    command = [
        str(SCRIPT),
        "mcp-resource",
        str(source),
        str(tmp_path / "private output"),
        "--expected-uri",
        URI,
        "--expected-sha256",
        digest,
        "--expected-size",
        str(len(content)),
        *extra,
    ]
    if audited:
        code = """
import runpy, sys
from pathlib import Path
def audit(event, args):
    if event in {"socket.connect", "socket.getaddrinfo"}:
        raise AssertionError("network_forbidden")
    if event == "open" and any(x in str(args[0]) for x in
        ("auth.json", ".credentials.json", "config.toml")):
        raise AssertionError("credentials_forbidden")
sys.addaudithook(audit)
sys.path.insert(0, str(Path(sys.argv[1]).parent))
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""
        command = ["-c", code, *command]
    return subprocess.run([sys.executable, *command], capture_output=True, text=True, timeout=30)


def test_saves_verified_pdf_privately_and_existing_reader_opens_it_without_network(tmp_path):
    content, digest, response = sample()
    result = invoke(tmp_path, response, content, digest, audited=True)
    assert result.returncode == 0, result.stderr
    manifest_path = tmp_path / "private output/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    artifact = manifest_path.parent / manifest["artifact"]
    assert artifact.read_bytes() == content
    assert manifest["sha256"] == digest
    assert manifest["size_bytes"] == len(content)
    assert manifest["uri"] == URI
    assert manifest["status"] == "saved_not_reviewed"
    assert artifact.name == "document.pdf"
    assert "PRIVATE_SYNTHETIC" not in result.stdout + result.stderr
    if os.name == "posix":
        assert manifest_path.parent.stat().st_mode & 0o777 == 0o700
        assert artifact.stat().st_mode & 0o777 == 0o600
        assert manifest_path.stat().st_mode & 0o777 == 0o600
    read = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "read",
            str(artifact),
            str(tmp_path / "read output"),
            "--expected-sha256",
            digest,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert read.returncode == 0, read.stderr
    reading = json.loads((tmp_path / "read output/manifest.json").read_text())
    assert reading["source"]["sha256"] == digest
    assert len(reading["units"]) > 0
    assert list((tmp_path / "read output").rglob("*.png"))


@pytest.mark.parametrize(
    "corruption",
    [
        "metadata_only",
        "error",
        "base64",
        "hash",
        "size",
        "uri",
        "ambiguous",
        "metadata_hash",
        "metadata_size",
        "metadata_case",
        "metadata_doc",
        "metadata_mime",
        "resource_hash",
        "missing_blob",
        "empty_blob",
        "invalid_expectation",
    ],
)
def test_invalid_or_ambiguous_resource_creates_no_output_and_never_echoes_blob(
    tmp_path, corruption
):
    content, digest, response = sample()
    resource = response["content"][0]["resource"]
    extra = []
    if corruption == "metadata_only":
        response["content"] = []
    elif corruption == "error":
        response["isError"] = True
    elif corruption == "base64":
        resource["blob"] = "PRIVATE_SYNTHETIC%%%"
    elif corruption == "hash":
        extra = ["--expected-sha256", "0" * 64]
    elif corruption == "size":
        extra = ["--expected-size", "1"]
    elif corruption == "uri":
        resource["uri"] = URI + "-other"
    elif corruption == "ambiguous":
        response["content"].append(response["content"][0])
    elif corruption.startswith("metadata_"):
        key, value = {
            "metadata_hash": ("content_hash", "0" * 64),
            "metadata_size": ("size", len(content) + 1),
            "metadata_case": ("case_id", "OTHER"),
            "metadata_doc": ("doc_id", "OTHER"),
            "metadata_mime": ("mime_type", "text/plain"),
        }[corruption]
        response["structuredContent"][key] = value
    elif corruption == "resource_hash":
        resource["_meta"]["sha256"] = "0" * 64
    elif corruption == "missing_blob":
        resource.pop("blob")
    elif corruption == "empty_blob":
        resource["blob"] = ""
    else:
        extra = ["--expected-uri", "https://example.invalid/PRIVATE_SYNTHETIC"]
    result = invoke(tmp_path, response, content, digest, *extra)
    assert result.returncode == 1, result.stderr
    assert json.loads(result.stderr)["error"]
    assert "PRIVATE_SYNTHETIC" not in result.stdout + result.stderr
    assert not (tmp_path / "private output").exists()


def test_existing_destination_is_untouched(tmp_path):
    content, digest, response = sample()
    output = tmp_path / "private output"
    output.mkdir()
    sentinel = output / "sentinel"
    sentinel.write_bytes(b"preserved")
    result = invoke(tmp_path, response, content, digest)
    assert result.returncode == 1
    assert json.loads(result.stderr)["error"] == "output_exists"
    assert list(output.iterdir()) == [sentinel]
    assert sentinel.read_bytes() == b"preserved"


def test_failed_manifest_write_removes_new_artifact_and_directory(tmp_path, monkeypatch):
    sys.path.insert(0, str(SCRIPT.parent))
    from loki_readers import resources

    content, digest, response = sample()
    source = tmp_path / "response_masked.json"
    source.write_text(json.dumps(response))

    def fail_write(*args):
        raise OSError("synthetic_disk_failure")

    monkeypatch.setattr(resources, "write_json", fail_write)
    with pytest.raises(OSError, match="synthetic_disk_failure"):
        resources.save_mcp_resource(
            source,
            tmp_path / "output",
            expected_uri=URI,
            expected_sha256=digest,
            expected_size=len(content),
        )
    assert not (tmp_path / "output").exists()


@pytest.mark.skipif(os.name == "nt", reason="POSIX symlink defense; Windows ACL is separate")
def test_symlink_destination_cannot_escape_into_another_directory(tmp_path):
    content, digest, response = sample()
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / "private output").symlink_to(outside, target_is_directory=True)
    result = invoke(tmp_path, response, content, digest)
    assert result.returncode == 1
    assert json.loads(result.stderr)["error"] == "unsafe_output_symlink"
    assert list(outside.iterdir()) == []
