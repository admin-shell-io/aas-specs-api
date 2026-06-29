#!/usr/bin/env python3
"""Validate the query grammar, JSON schema, and synchronized schema copies."""

from __future__ import annotations

import json
import re
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from jsonschema import Draft7Validator, FormatChecker

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from jsonschema import RefResolver
except ImportError as exc:  # pragma: no cover - exercised in CI setup failures.
    print("Missing dependency: jsonschema. Install it with: python -m pip install jsonschema")
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
QUERY_EXAMPLES = [
    ROOT_MODULE / "pages/http-rest-api/test/query/test1.json",
]

RULE_RE = re.compile(r"^\s*<([^<>]+)>\s*::=\s*(.*)$")
REF_RE = re.compile(r"<([^<>]+)>")


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

    validate_query_examples(schema, validation)
    validate_schema_smoke_tests(schema, validation)
    validate_openapi_pattern_sync(schema, validation)
    return schema


def schema_validator(schema: dict[str, Any], ref: str) -> Draft7Validator:
    resolver = RefResolver(base_uri=QUERY_SCHEMA.resolve().as_uri(), referrer=schema)
    return Draft7Validator({"$ref": ref}, resolver=resolver, format_checker=FormatChecker())


def definition_validator(schema: dict[str, Any], definition_name: str) -> Draft7Validator:
    return schema_validator(schema, f"#/definitions/{definition_name}")


def validate_query_examples(schema: dict[str, Any], validation: Validation) -> None:
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    for path in QUERY_EXAMPLES:
        data = load_json(path, validation)
        if data is None:
            continue
        errors = sorted(validator.iter_errors(data), key=lambda error: list(error.absolute_path))
        for error in errors:
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            validation.fail(path, f"{location}: {error.message}")


def validate_schema_smoke_tests(schema: dict[str, Any], validation: Validation) -> None:
    cases = [
        ("FieldIdentifier", "$aas#submodels[]", True),
        ("FieldIdentifier", "$aas#submodels[01]", False),
        ("FieldIdentifier", "$sm#supplementalSemanticIds[]", True),
        ("FieldIdentifier", "$sm#supplementalSemanticIds[01]", False),
        ("FragmentFieldIdentifier", "$sm#supplementalSemanticIds[]", True),
        ("FragmentFieldIdentifier", "$sm#supplementalSemanticIds[0].keys[]", True),
        ("FragmentFieldIdentifier", "$sm#supplementalSemanticIds[01]", False),
        ("ReferenceIdentifier", '$sm("SubmodelID")#id', True),
        ("ReferenceIdentifier", '$sme("SubmodelID").machineState#value', True),
        ("ReferenceIdentifier", "$sm#id", False),
        ("ReferenceIdentifier", '$sm("SubmodelID")#bogus', False),
        ("IdentifiableIdentifier", '$aas("aas-id")', True),
        ("IdentifiableIdentifier", '$aasdesc("aas-id")', False),
        ("ReferableIdentifier", '$sme("submodel-id").AddressInformation[]', True),
        ("ReferableIdentifier", '$sme("submodel-id").AddressInformation[01]', False),
        ("DescriptorIdentifier", '$aasdesc("aas-id")', True),
        ("DescriptorIdentifier", '$aas("aas-id")', False),
    ]

    validators: dict[str, Draft7Validator] = {}
    for definition_name, value, should_pass in cases:
        validators.setdefault(definition_name, definition_validator(schema, definition_name))
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


def main() -> int:
    validation = Validation()
    validate_json_schema(validation)
    validate_bnf_grammar_files(validation)
    validation.assert_ok()
    print("OK: spec artifact validation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
