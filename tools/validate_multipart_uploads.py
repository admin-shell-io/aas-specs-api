#!/usr/bin/env python3
"""Validate multipart file-upload contracts in the V3.2 OpenAPI files."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised in CI setup failures.
    print("Missing dependency: PyYAML. Install it with: python -m pip install PyYAML")
    raise SystemExit(2) from exc


ROOT = Path(__file__).resolve().parents[1]
OPENAPI_FILES = (
    ROOT / "Entire-API-Collection/V3.2.yaml",
    *sorted(ROOT.glob("*ServiceSpecification/V3.2*.yaml")),
)
HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")


def load_openapi(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - keep parser detail in output.
        errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        return None

    if not isinstance(document, dict) or not isinstance(document.get("paths"), dict):
        errors.append(f"{path.relative_to(ROOT)}: missing or invalid paths object")
        return None
    return document


def validate_uploads() -> list[str]:
    errors: list[str] = []
    uploads_found = 0

    for openapi_path in OPENAPI_FILES:
        document = load_openapi(openapi_path, errors)
        if document is None:
            continue

        for path, path_item in document["paths"].items():
            if not isinstance(path_item, dict):
                continue
            for method in HTTP_METHODS:
                operation = path_item.get(method)
                if not isinstance(operation, dict):
                    continue

                request_body = operation.get("requestBody")
                content = request_body.get("content") if isinstance(request_body, dict) else None
                multipart = content.get("multipart/form-data") if isinstance(content, dict) else None
                schema = multipart.get("schema") if isinstance(multipart, dict) else None
                properties = schema.get("properties") if isinstance(schema, dict) else None
                if not isinstance(properties, dict) or "file" not in properties:
                    continue

                uploads_found += 1
                location = f"{openapi_path.relative_to(ROOT)}: {method.upper()} {path}"
                if "fileName" in properties:
                    errors.append(f"{location} declares a separate fileName multipart part")

                required = schema.get("required")
                if not isinstance(required, list) or "file" not in required:
                    errors.append(f"{location} does not require the binary file part")

                file_schema = properties["file"]
                if not isinstance(file_schema, dict):
                    errors.append(f"{location} has an invalid file schema")
                    continue
                if file_schema.get("type") != "string" or file_schema.get("format") != "binary":
                    errors.append(f"{location} file part is not a binary string")

                description = file_schema.get("description")
                if (
                    not isinstance(description, str)
                    or "filename" not in description
                    or "Content-Disposition" not in description
                ):
                    errors.append(
                        f"{location} does not document the standard multipart filename parameter"
                    )

    if uploads_found == 0:
        errors.append("no multipart file uploads found")
    return errors


def main() -> int:
    errors = validate_uploads()
    if errors:
        print("Specification artifact validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: multipart file-upload validation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
