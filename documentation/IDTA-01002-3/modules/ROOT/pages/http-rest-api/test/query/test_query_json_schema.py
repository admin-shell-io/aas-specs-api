import json
import unittest
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker


ROOT_MODULE = Path(__file__).resolve().parents[4]
QUERY_SCHEMA = ROOT_MODULE / "partials" / "query-json-schema.json"
FORMAT_CHECKER_MESSAGE = 'jsonschema date-time format checking is inactive; install "jsonschema[format]"'


def format_errors(errors):
    return "\n".join(
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in errors
    )


class QueryJsonSchemaValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(QUERY_SCHEMA.read_text(encoding="utf-8-sig"))
        Draft7Validator.check_schema(cls.schema)
        cls.format_checker = FormatChecker()
        cls.ensure_date_time_format_checking_is_active()
        cls.validator = Draft7Validator(cls.schema, format_checker=cls.format_checker)

    @classmethod
    def ensure_date_time_format_checking_is_active(cls):
        validator = Draft7Validator(
            {"type": "string", "format": "date-time"},
            format_checker=cls.format_checker,
        )
        if not list(validator.iter_errors("not-a-date-time")):
            raise RuntimeError(FORMAT_CHECKER_MESSAGE)

    def assert_valid(self, instance):
        errors = sorted(self.validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
        self.assertEqual([], errors, format_errors(errors))

    def assert_invalid(self, instance):
        errors = sorted(self.validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
        self.assertTrue(errors, "Expected schema validation to fail")

    def test_complex_query_payload_is_valid(self):
        query = {
            "$select": "id",
            "$condition": {
                "$and": [
                    {
                        "$match": [
                            {
                                "$eq": [
                                    {"$field": "$sm#supplementalSemanticIds[].keys[].value"},
                                    {"$strVal": "https://example.org/semantic-id"},
                                ]
                            },
                            {
                                "$gt": [
                                    {"$numCast": {"$field": "$sme.OperationalData.Temperature#value"}},
                                    {"$numVal": 42.5},
                                ]
                            },
                        ]
                    },
                    {"$not": {"$boolean": False}},
                ]
            },
            "$filters": [
                {
                    "$fragment": "$aasdesc#submodelDescriptors[].supplementalSemanticIds[].keys[]",
                    "$condition": {
                        "$contains": [
                            {"$field": "$smdesc#semanticId.keys[].value"},
                            {"$strVal": "admin-shell"},
                        ]
                    },
                }
            ],
        }

        self.assert_valid(query)

    def test_access_rule_payload_with_constrained_identifiers_is_valid(self):
        access_rules = {
            "DEFATTRIBUTES": [
                {
                    "name": "timeAttributes",
                    "USEATTRIBUTES": ["baseAttributes"],
                }
            ],
            "rules": [
                {
                    "ACL": {
                        "ATTRIBUTES": [
                            {"CLAIM": "bpn"},
                            {"GLOBAL": "UTCNOW"},
                            {"REFERENCE": '$sm("SubmodelID")#supplementalSemanticIds[].keys[].value'},
                        ],
                        "RIGHTS": ["READ", "UPDATE"],
                        "ACCESS": "ALLOW",
                    },
                    "OBJECTS": [
                        {"IDENTIFIABLE": '$aas("aas-id")'},
                        {"REFERABLE": '$sme("SubmodelID").AddressInformation[]'},
                        {"FRAGMENT": "$aasdesc#submodelDescriptors[].semanticId.keys[]"},
                        {"DESCRIPTOR": '$smdesc("submodel-id")'},
                    ],
                    "FORMULA": {
                        "$eq": [
                            {"$attribute": {"CLAIM": "bpn"}},
                            {"$strVal": "BPNL123"},
                        ]
                    },
                    "FILTERLIST": [
                        {
                            "FRAGMENT": "$sme#value",
                            "CONDITION": {"$boolean": True},
                        },
                        {
                            "FRAGMENT": "$sm#supplementalSemanticIds[]",
                            "USEFORMULA": "predefinedFormula",
                        },
                    ],
                }
            ],
        }

        self.assert_valid(access_rules)

    def test_invalid_query_payloads_are_rejected(self):
        cases = [
            {
                "$condition": {
                    "$eq": [
                        {"$field": "$sm#supplementalSemanticIds[01]"},
                        {"$strVal": "https://example.org/semantic-id"},
                    ]
                }
            },
            {
                "$condition": {
                    "$and": [{"$boolean": True}, {"$boolean": False}],
                    "$or": [{"$boolean": True}, {"$boolean": False}],
                }
            },
            {
                "$condition": {
                    "$eq": [
                        {"$dateTimeVal": "not-a-date-time"},
                        {"$dateTimeVal": "2026-06-29T12:00:00Z"},
                    ]
                }
            },
            {
                "$condition": {"$boolean": True},
                "$filters": [
                    {
                        "$fragment": "$sme#value",
                    }
                ],
            },
            {
                "Query": {
                    "$condition": {"$boolean": True},
                }
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                self.assert_invalid(case)

    def test_invalid_access_rule_identifiers_are_rejected(self):
        cases = [
            {
                "rules": [
                    {
                        "ACL": {
                            "ATTRIBUTES": [{"REFERENCE": "$sm#id"}],
                            "RIGHTS": ["READ"],
                            "ACCESS": "ALLOW",
                        },
                        "OBJECTS": [{"IDENTIFIABLE": '$aas("aas-id")'}],
                        "FORMULA": {"$boolean": True},
                    }
                ]
            },
            {
                "rules": [
                    {
                        "ACL": {
                            "ATTRIBUTES": [{"CLAIM": "bpn"}],
                            "RIGHTS": ["READ"],
                            "ACCESS": "ALLOW",
                        },
                        "OBJECTS": [{"IDENTIFIABLE": '$aasdesc("aas-id")'}],
                        "FORMULA": {"$boolean": True},
                    }
                ]
            },
            {
                "rules": [
                    {
                        "ACL": {
                            "ATTRIBUTES": [{"CLAIM": "bpn"}],
                            "RIGHTS": ["READ"],
                            "ACCESS": "ALLOW",
                        },
                        "OBJECTS": [{"REFERABLE": '$sme("SubmodelID").AddressInformation[01]'}],
                        "FORMULA": {"$boolean": True},
                    }
                ]
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                self.assert_invalid(case)


if __name__ == "__main__":
    unittest.main()
