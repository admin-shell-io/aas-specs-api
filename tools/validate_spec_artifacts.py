#!/usr/bin/env python3
"""Validate synchronized specification artifacts and normative mappings."""

from __future__ import annotations

import json
import re
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised in CI setup failures.
    print("Missing dependency: PyYAML. Install it with: python -m pip install PyYAML")
    raise SystemExit(2) from exc

try:
    from jsonschema import Draft7Validator, FormatChecker

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from jsonschema import RefResolver
except ImportError as exc:  # pragma: no cover - exercised in CI setup failures.
    print('Missing dependency: jsonschema. Install it with: python -m pip install "jsonschema[format]"')
    raise SystemExit(2) from exc


ROOT = Path(__file__).resolve().parents[1]
ROOT_MODULE = ROOT / "documentation/IDTA-01002-3/modules/ROOT"
QUERY_SCHEMA = ROOT_MODULE / "partials/query-json-schema.json"
SCHEMA_PAGE = ROOT_MODULE / "pages/schema.adoc"
GRAMMAR_FILES = [
    ROOT_MODULE / "partials/bnf/grammar.bnf",
    ROOT_MODULE / "pages/json-grammar.txt",
]
OPENAPI_SCHEMA = ROOT / "Part2-API-Schemas/openapi.yaml"
COMBINED_OPENAPI = ROOT / "Entire-API-Collection/V3.2.yaml"
OPERATION_RIGHT_MAPPING = ROOT_MODULE / "pages/annex/operation-to-right-mapping.adoc"
QUERY_EXAMPLES = [
    ROOT_MODULE / "pages/http-rest-api/test/query/test1.json",
]
FORMAT_CHECKER_MESSAGE = 'jsonschema date-time format checking is inactive; install "jsonschema[format]"'

RULE_RE = re.compile(r"^\s*<([^<>]+)>\s*::=\s*(.*)$")
REF_RE = re.compile(r"<([^<>]+)>")
OPENAPI_HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")
RIGHT_MAPPING_ROW_RE = re.compile(
    r'^\| (?P<operation_id>[^|]+?) \| (?P<method>GET|PUT|POST|DELETE|OPTIONS|HEAD|PATCH|TRACE) '
    r'\| (?P<path>[^|]+?) \| (?P<right>VIEW|READ|CREATE(?: or UPDATE)?|UPDATE|DELETE|EXECUTE|originating RIGHT) '
    r'\| "(?P<route>[^"]+)"\s*$'
)


@dataclass(frozen=True)
class BnfRule:
    name: str
    path: Path
    line: int
    rhs: str


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def fail(self, path: Path | str, message: str) -> None:
        self.errors.append(f"{display_path(path)}: {message}")

    def assert_ok(self) -> None:
        if not self.errors:
            return
        print("Validation failed:")
        for error in self.errors:
            print(f"  - {error}")
        raise SystemExit(1)


def display_path(path: Path | str) -> str:
    path = Path(path)
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path, validation: Validation) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - keep parser detail in output.
        validation.fail(path, f"invalid JSON: {exc}")
        return None


def schema_page_json(validation: Validation) -> dict[str, Any] | None:
    try:
        lines = SCHEMA_PAGE.read_text(encoding="utf-8-sig").splitlines()
    except Exception as exc:  # noqa: BLE001
        validation.fail(SCHEMA_PAGE, f"could not read schema page: {exc}")
        return None

    if len(lines) < 3 or lines[0] != "...." or lines[-1] != "....":
        validation.fail(SCHEMA_PAGE, "expected schema page to be wrapped in .... delimiters")
        return None

    try:
        return json.loads("\n".join(lines[1:-1]))
    except Exception as exc:  # noqa: BLE001
        validation.fail(SCHEMA_PAGE, f"invalid embedded JSON schema: {exc}")
        return None


def iter_refs(node: Any) -> Iterable[str]:
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            yield ref
        for value in node.values():
            yield from iter_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_refs(value)


def resolve_pointer(document: Any, pointer: str) -> Any:
    current = document
    if pointer in ("", "/"):
        return current
    for raw_part in pointer.lstrip("/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        current = current[part]
    return current


def validate_json_schema(validation: Validation) -> dict[str, Any] | None:
    schema = load_json(QUERY_SCHEMA, validation)
    if not isinstance(schema, dict):
        validation.fail(QUERY_SCHEMA, "schema root is not an object")
        return None

    try:
        Draft7Validator.check_schema(schema)
    except Exception as exc:  # noqa: BLE001 - keep schema detail in output.
        validation.fail(QUERY_SCHEMA, f"invalid draft-07 schema: {exc}")

    for ref in iter_refs(schema):
        if not ref.startswith("#/"):
            validation.fail(QUERY_SCHEMA, f"unexpected external $ref: {ref}")
            continue
        try:
            resolve_pointer(schema, ref[1:])
        except Exception as exc:  # noqa: BLE001
            validation.fail(QUERY_SCHEMA, f"unresolved $ref {ref}: {exc}")

    embedded_schema = schema_page_json(validation)
    if embedded_schema is not None and embedded_schema != schema:
        validation.fail(SCHEMA_PAGE, "embedded schema differs from partials/query-json-schema.json")

    format_checker = active_format_checker(validation)
    validate_query_examples(schema, validation, format_checker)
    validate_schema_smoke_tests(schema, validation, format_checker)
    validate_openapi_pattern_sync(schema, validation)
    return schema


def active_format_checker(validation: Validation) -> FormatChecker:
    format_checker = FormatChecker()
    validator = Draft7Validator(
        {"type": "string", "format": "date-time"},
        format_checker=format_checker,
    )
    if not list(validator.iter_errors("not-a-date-time")):
        validation.fail(QUERY_SCHEMA, FORMAT_CHECKER_MESSAGE)
    return format_checker


def schema_validator(schema: dict[str, Any], ref: str, format_checker: FormatChecker) -> Draft7Validator:
    resolver = RefResolver(base_uri=QUERY_SCHEMA.resolve().as_uri(), referrer=schema)
    return Draft7Validator({"$ref": ref}, resolver=resolver, format_checker=format_checker)


def definition_validator(
    schema: dict[str, Any],
    definition_name: str,
    format_checker: FormatChecker,
) -> Draft7Validator:
    return schema_validator(schema, f"#/definitions/{definition_name}", format_checker)


def validate_query_examples(schema: dict[str, Any], validation: Validation, format_checker: FormatChecker) -> None:
    validator = Draft7Validator(schema, format_checker=format_checker)
    for path in QUERY_EXAMPLES:
        data = load_json(path, validation)
        if data is None:
            continue
        errors = sorted(validator.iter_errors(data), key=lambda error: list(error.absolute_path))
        for error in errors:
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            validation.fail(path, f"{location}: {error.message}")


def validate_schema_smoke_tests(schema: dict[str, Any], validation: Validation, format_checker: FormatChecker) -> None:
    cases = [
        ("FieldIdentifier", "$aas#submodels[]", True),
        ("FieldIdentifier", "$aas#submodels[01]", False),
        ("FieldIdentifier", "$sm#supplementalSemanticIds[]", True),
        ("FieldIdentifier", "$sm#supplementalSemanticIds[01]", False),
        ("FragmentFieldIdentifier", "$sm#supplementalSemanticIds[]", True),
        ("FragmentFieldIdentifier", "$sm#supplementalSemanticIds[0].keys[]", True),
        ("FragmentFieldIdentifier", "$sm#supplementalSemanticIds[01]", False),
        ("ReferenceIdentifier", '$sm("SubmodelID")#id', True),
        ("ReferenceIdentifier", '$sm("urn:example:日本")#id', True),
        ("ReferenceIdentifier", '$sme("SubmodelID").machineState#value', True),
        ("ReferenceIdentifier", "$sm#id", False),
        ("ReferenceIdentifier", '$sm("SubmodelID")#bogus', False),
        ("IdentifiableIdentifier", '$aas("aas-id")', True),
        ("IdentifiableIdentifier", '$aas("urn:example:\\"quoted\\"\\\\path")', True),
        ("IdentifiableIdentifier", '$aas("urn:example:\\q")', False),
        ("IdentifiableIdentifier", '$aasdesc("aas-id")', False),
        ("ReferableIdentifier", '$sme("submodel-id").AddressInformation[]', True),
        ("ReferableIdentifier", '$sme("submodel-id").AddressInformation[01]', False),
        ("DescriptorIdentifier", '$aasdesc("aas-id")', True),
        ("DescriptorIdentifier", '$aas("aas-id")', False),
    ]

    validators: dict[str, Draft7Validator] = {}
    for definition_name, value, should_pass in cases:
        validators.setdefault(definition_name, definition_validator(schema, definition_name, format_checker))
        is_valid = validators[definition_name].is_valid(value)
        if is_valid != should_pass:
            expected = "valid" if should_pass else "invalid"
            validation.fail(QUERY_SCHEMA, f"{definition_name} smoke test expected {expected}: {value}")


def openapi_component_pattern(component: str, validation: Validation) -> str | None:
    lines = OPENAPI_SCHEMA.read_text(encoding="utf-8-sig").splitlines()
    for index, line in enumerate(lines):
        if line.strip() != f"{component}:":
            continue
        for candidate_index, candidate in enumerate(lines[index + 1 :], start=index + 1):
            if candidate.strip() == "pattern: >-":
                return lines[candidate_index + 1].strip()
        break
    validation.fail(OPENAPI_SCHEMA, f"OpenAPI component pattern not found: {component}")
    return None


def validate_openapi_pattern_sync(schema: dict[str, Any], validation: Validation) -> None:
    for definition_name in ["FieldIdentifier", "FragmentFieldIdentifier"]:
        expected = schema["definitions"][definition_name]["pattern"]
        actual = openapi_component_pattern(definition_name, validation)
        if actual is not None and actual != expected:
            validation.fail(OPENAPI_SCHEMA, f"{definition_name} pattern differs from query-json-schema.json")


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def without_quoted_literals(text: str) -> tuple[str, bool]:
    result: list[str] = []
    in_string = False
    for index, char in enumerate(text):
        if char == '"' and not is_escaped(text, index):
            in_string = not in_string
            result.append(" ")
        elif in_string:
            result.append(" ")
        else:
            result.append(char)
    return "".join(result), in_string


def validate_balanced_delimiters(path: Path, text: str, validation: Validation) -> None:
    stack: list[tuple[str, int, int]] = []
    opening = {"(": ")", "[": "]"}
    closing = {")": "(", "]": "["}

    for line_number, line in enumerate(text.splitlines(), start=1):
        clean_line, unclosed_string = without_quoted_literals(line)
        if unclosed_string:
            validation.fail(path, f"line {line_number}: unclosed quoted literal")

        for column, char in enumerate(clean_line, start=1):
            if char in opening:
                stack.append((char, line_number, column))
            elif char in closing:
                if not stack or stack[-1][0] != closing[char]:
                    validation.fail(path, f"line {line_number}: unmatched {char}")
                    continue
                stack.pop()

    for char, line_number, column in stack:
        validation.fail(path, f"line {line_number}, column {column}: unmatched {char}")


def parse_bnf_rules(path: Path, validation: Validation) -> list[BnfRule]:
    rules: list[BnfRule] = []
    seen_in_file: dict[str, int] = {}
    current_name: str | None = None
    current_line = 0
    current_rhs: list[str] = []

    def finish_current() -> None:
        nonlocal current_name, current_line, current_rhs
        if current_name is None:
            return
        rhs = "\n".join(current_rhs).strip()
        if not rhs:
            validation.fail(path, f"line {current_line}: rule <{current_name}> has no production")
        rules.append(BnfRule(current_name, path, current_line, rhs))
        current_name = None
        current_line = 0
        current_rhs = []

    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue

        match = RULE_RE.match(line)
        if match:
            finish_current()
            current_name = match.group(1).strip()
            current_line = line_number
            current_rhs = [match.group(2)]
            previous_line = seen_in_file.get(current_name)
            if previous_line is not None:
                validation.fail(
                    path,
                    f"line {line_number}: duplicate rule <{current_name}> previously defined on line {previous_line}",
                )
            seen_in_file[current_name] = line_number
            continue

        if "::=" in line:
            validation.fail(path, f"line {line_number}: malformed rule definition")
        elif current_name is None:
            validation.fail(path, f"line {line_number}: content before first rule")
        else:
            current_rhs.append(line)

    finish_current()
    return rules


def validate_bnf_grammar_files(validation: Validation) -> None:
    for path in GRAMMAR_FILES:
        text = path.read_text(encoding="utf-8-sig")
        validate_balanced_delimiters(path, text, validation)
        rules = parse_bnf_rules(path, validation)
        defined_rules = {rule.name for rule in rules}
        for rule in rules:
            for referenced_rule in sorted(set(REF_RE.findall(rule.rhs))):
                if referenced_rule not in defined_rules:
                    validation.fail(
                        rule.path,
                        f"line {rule.line}: <{rule.name}> references undefined <{referenced_rule}>",
                    )


def parse_combined_openapi_operations(
    validation: Validation,
) -> dict[str, tuple[str, str]]:
    operations: dict[str, tuple[str, str]] = {}
    try:
        document = yaml.safe_load(COMBINED_OPENAPI.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - keep parser detail in output.
        validation.fail(COMBINED_OPENAPI, f"invalid YAML: {exc}")
        return operations

    if not isinstance(document, dict) or not isinstance(document.get("paths"), dict):
        validation.fail(COMBINED_OPENAPI, "missing or invalid paths object")
        return operations

    for path, path_item in document["paths"].items():
        if not isinstance(path, str) or not isinstance(path_item, dict):
            validation.fail(COMBINED_OPENAPI, f"invalid Path Item for {path!r}")
            continue

        for method in OPENAPI_HTTP_METHODS:
            operation = path_item.get(method)
            if operation is None:
                continue
            if not isinstance(operation, dict):
                validation.fail(COMBINED_OPENAPI, f"invalid {method.upper()} operation for {path!r}")
                continue

            operation_id = operation.get("operationId")
            if not isinstance(operation_id, str) or not operation_id:
                validation.fail(
                    COMBINED_OPENAPI,
                    f"{method.upper()} {path} has no non-empty operationId",
                )
                continue

            previous = operations.get(operation_id)
            if previous is not None:
                validation.fail(
                    COMBINED_OPENAPI,
                    f"duplicate operationId {operation_id!r}; used by "
                    f"{previous[0]} {previous[1]} and {method.upper()} {path}",
                )
            operations[operation_id] = (method.upper(), path)

    if not operations:
        validation.fail(COMBINED_OPENAPI, "no operations found")
    return operations


def validate_operation_right_mapping(validation: Validation) -> None:
    operations = parse_combined_openapi_operations(validation)
    rows: dict[str, tuple[str, str, str, str, int]] = {}

    for line_number, line in enumerate(
        OPERATION_RIGHT_MAPPING.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        if not line.startswith("| ") or line.startswith("| Operation Name"):
            continue

        row_match = RIGHT_MAPPING_ROW_RE.match(line)
        if not row_match:
            validation.fail(OPERATION_RIGHT_MAPPING, f"line {line_number}: malformed mapping row")
            continue

        operation_id = row_match.group("operation_id")
        previous = rows.get(operation_id)
        if previous is not None:
            validation.fail(
                OPERATION_RIGHT_MAPPING,
                f"line {line_number}: duplicate mapping for {operation_id!r} "
                f"previously defined on line {previous[4]}",
            )
        rows[operation_id] = (
            row_match.group("method"),
            row_match.group("path"),
            row_match.group("right"),
            row_match.group("route"),
            line_number,
        )

    for operation_id in sorted(operations.keys() - rows.keys()):
        validation.fail(OPERATION_RIGHT_MAPPING, f"missing mapping for {operation_id!r}")
    for operation_id in sorted(rows.keys() - operations.keys()):
        validation.fail(OPERATION_RIGHT_MAPPING, f"unknown operationId {operation_id!r}")

    for operation_id in sorted(operations.keys() & rows.keys()):
        expected_method, expected_path = operations[operation_id]
        method, path, _, route, line_number = rows[operation_id]
        if method != expected_method:
            validation.fail(
                OPERATION_RIGHT_MAPPING,
                f"line {line_number}: {operation_id!r} uses {method}, expected {expected_method}",
            )
        if path != expected_path:
            validation.fail(
                OPERATION_RIGHT_MAPPING,
                f"line {line_number}: {operation_id!r} uses path {path!r}, expected {expected_path!r}",
            )

        expected_route = expected_path
        parameter_start = expected_path.find("{")
        if parameter_start >= 0:
            expected_route = f"{expected_path[:parameter_start]}*"
        if route != expected_route:
            validation.fail(
                OPERATION_RIGHT_MAPPING,
                f"line {line_number}: {operation_id!r} uses ROUTE {route!r}, expected {expected_route!r}",
            )


def main() -> int:
    validation = Validation()
    validate_json_schema(validation)
    validate_bnf_grammar_files(validation)
    validate_operation_right_mapping(validation)
    validation.assert_ok()
    print("OK: spec artifact validation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
