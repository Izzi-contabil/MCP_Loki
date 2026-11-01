"""Save an embedded case resource offline; metadata never substitutes for bytes."""

import base64
import binascii
import hashlib
import re
import shutil
from pathlib import Path
from typing import Any

from .private import (
    ReadError,
    checked_bytes,
    private_directory,
    strict_json,
    write_bytes,
    write_json,
)
from .readers import MAX_BYTES


def save_mcp_resource(
    source: Path,
    output: Path,
    *,
    expected_uri: str,
    expected_sha256: str,
    expected_size: int,
) -> dict[str, Any]:
    identity = re.fullmatch(
        r"loki://cases/([A-Za-z0-9_-]+)/documents/([A-Za-z0-9_-]+)", expected_uri
    )
    if (
        identity is None
        or re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is None
        or type(expected_size) is not int
        or not 0 < expected_size <= MAX_BYTES
    ):
        raise ReadError("invalid_resource_expectation")
    response_bytes = checked_bytes(source, MAX_BYTES * 2)
    response = strict_json(response_bytes.decode("utf-8-sig"))
    if not isinstance(response, dict) or response.get("isError", False) is not False:
        raise ReadError("mcp_response_error")
    blocks = response.get("content")
    if not isinstance(blocks, list):
        raise ReadError("mcp_resource_missing")
    candidates = [
        block["resource"]
        for block in blocks
        if isinstance(block, dict)
        and block.get("type") == "resource"
        and isinstance(block.get("resource"), dict)
        and block["resource"].get("uri") == expected_uri
    ]
    if len(candidates) != 1:
        raise ReadError("mcp_resource_missing_or_ambiguous")
    resource = candidates[0]
    blob = resource.get("blob")
    if not isinstance(blob, str) or not blob:
        raise ReadError("mcp_resource_blob_missing")
    if len(blob) > ((MAX_BYTES + 2) // 3) * 4:
        raise ReadError("size_limit")
    try:
        content = base64.b64decode(blob, validate=True)
    except (ValueError, binascii.Error):
        raise ReadError("mcp_resource_base64_invalid") from None
    if base64.b64encode(content).decode("ascii") != blob:
        raise ReadError("mcp_resource_base64_invalid")
    digest = hashlib.sha256(content).hexdigest()
    if len(content) != expected_size:
        raise ReadError("mcp_resource_size_mismatch")
    if digest != expected_sha256:
        raise ReadError("mcp_resource_hash_mismatch")
    mime = resource.get("mimeType")
    if not isinstance(mime, str) or not mime:
        raise ReadError("mcp_resource_mime_missing")
    meta = resource.get("_meta", {})
    if not isinstance(meta, dict) or ("sha256" in meta and meta["sha256"] != digest):
        raise ReadError("mcp_resource_metadata_mismatch")
    metadata = response.get("structuredContent", {})
    if not isinstance(metadata, dict):
        raise ReadError("mcp_resource_metadata_mismatch")
    checks = {
        "case_id": identity[1],
        "doc_id": identity[2],
        "content_hash": digest,
        "size": len(content),
        "mime_type": mime,
    }
    for key, expected in checks.items():
        if key in metadata and (
            metadata[key] != expected or (key == "size" and type(metadata[key]) is not int)
        ):
            raise ReadError("mcp_resource_metadata_mismatch")
    # No remote filename or identifier participates in local path construction.
    extension = {
        "application/pdf": ".pdf",
        "application/xml": ".xml",
        "text/xml": ".xml",
        "text/plain": ".txt",
        "text/csv": ".csv",
        "application/json": ".json",
        "image/png": ".png",
        "image/jpeg": ".jpg",
    }.get(mime, ".bin")
    manifest: dict[str, Any] = {
        "schema_version": "loki.local-mcp-resource/1",
        "uri": expected_uri,
        "sha256": digest,
        "size_bytes": len(content),
        "mime_type": mime,
        "artifact": "document" + extension,
        "response_sha256": hashlib.sha256(response_bytes).hexdigest(),
        "status": "saved_not_reviewed",
    }
    output = private_directory(output)
    try:
        write_bytes(output / manifest["artifact"], content)
        write_json(output / "manifest.json", manifest)
    except Exception:
        shutil.rmtree(output)
        raise
    return manifest
