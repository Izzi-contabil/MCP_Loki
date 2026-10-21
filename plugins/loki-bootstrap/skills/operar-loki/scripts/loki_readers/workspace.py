"""Local inventory and installation diagnostics, with no account configuration."""

import hashlib
import importlib.metadata
import os
import platform
from pathlib import Path
from typing import Any

from .private import ReadError, checked_bytes, private_directory, write_bytes, write_json
from .readers import MAX_BYTES, read_document

FORMATS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".bmp",
    ".webp",
    ".csv",
    ".txt",
    ".md",
    ".json",
    ".xml",
    ".xls",
    ".xlsx",
    ".docx",
    ".odt",
    ".ods",
    ".zip",
}


def inventory(root: Path, output: Path) -> dict[str, Any]:
    if root.is_symlink() or not root.is_dir():
        raise ReadError("inventory_directory_required")
    files = []
    total = 0
    for current, directories, names in os.walk(root, followlinks=False):
        directories[:] = sorted(d for d in directories if not (Path(current) / d).is_symlink())
        for name in sorted(names):
            path = Path(current) / name
            item: dict[str, Any] = {
                "relative_path": str(path.relative_to(root)),
                "status": "pending_harness_reading",
            }
            if path.is_symlink():
                item["status"] = "symlink_not_read"
            elif path.suffix.lower() not in FORMATS:
                item["status"] = "unsupported_format"
            elif path.stat().st_size > MAX_BYTES:
                item["status"] = "oversized_not_read"
            else:
                content = checked_bytes(path, MAX_BYTES)
                total += len(content)
                if total > 1024 * 1024 * 1024:
                    raise ReadError("inventory_size_limit")
                item.update(sha256=hashlib.sha256(content).hexdigest(), size_bytes=len(content))
            files.append(item)
            if len(files) > 10000:
                raise ReadError("inventory_file_limit")
    output = private_directory(output)
    result = {
        "schema_version": "loki.local-inventory/1",
        "root": str(root.absolute()),
        "status": "requires_harness_reading",
        "files": files,
    }
    write_json(output / "inventory.json", result)
    return result


def doctor(output: Path) -> dict[str, Any]:
    from openpyxl import Workbook
    from PIL import Image
    from pypdf import PdfWriter

    output = private_directory(output)
    write_bytes(output / "synthetic.csv", b"field;value\nzero;0\nfalse;false\n")
    read_document(output / "synthetic.csv", output / "csv")
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=150)
    import io

    buffer = io.BytesIO()
    writer.write(buffer)
    write_bytes(output / "synthetic.pdf", buffer.getvalue())
    read_document(output / "synthetic.pdf", output / "pdf")
    workbook = Workbook()
    workbook.active["A1"] = 0
    buffer = io.BytesIO()
    workbook.save(buffer)
    write_bytes(output / "synthetic.xlsx", buffer.getvalue())
    read_document(output / "synthetic.xlsx", output / "xlsx")
    buffer = io.BytesIO()
    Image.new("RGB", (20, 30), "white").save(buffer, format="PNG")
    write_bytes(output / "synthetic.png", buffer.getvalue())
    read_document(output / "synthetic.png", output / "image")
    result = {
        "status": "local_readers_ready",
        "python": platform.python_version(),
        "platform": platform.system(),
        "oauth": "existing_harness_connection_untouched",
        "dependencies": {
            name: importlib.metadata.version(name)
            for name in (
                "pypdf",
                "pypdfium2",
                "pillow",
                "openpyxl",
                "xlrd",
                "defusedxml",
                "jsonschema",
            )
        },
    }
    write_json(output / "doctor.json", result)
    return result
