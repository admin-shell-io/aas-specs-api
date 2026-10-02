import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker


ROOT_MODULE = Path(__file__).resolve().parents[4]
QUERY_SCHEMA = ROOT_MODULE / "partials/query-json-schema.json"
TIMESTAMP_FIELDS = [
    f"{prefix}administration.{attribute}"
    for prefix in (
        "$aas#", "$sm#", "$cd#", "$aasdesc#", "$smdesc#",
        "$aasdesc#submodelDescriptors[].",
        "$aasdesc#submodelDescriptors[0].",
        "$aasdesc#submodelDescriptors[12].",
    )
    for attribute in ("createdAt", "updatedAt")
]


class AdministrationTimestampsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(QUERY_SCHEMA.read_text(encoding="utf-8-sig"))
        cls.validator = Draft7Validator(cls.schema, format_checker=FormatChecker())
        cls.patterns = {
            name: re.compile(cls.schema["definitions"][name]["pattern"])
            for name in ("FieldIdentifier", "FragmentFieldIdentifier", "ReferenceIdentifier")
        }

    def assert_valid(self, query):
        errors = list(self.validator.iter_errors(query))
        self.assertEqual([], errors, "\n".join(error.message for error in errors))

    def test_timestamp_fields_and_fragments_are_allowed(self):
        for definition in ("FieldIdentifier", "FragmentFieldIdentifier"):
            for field in TIMESTAMP_FIELDS:
                with self.subTest(definition=definition, field=field):
                    self.assertIsNotNone(self.patterns[definition].fullmatch(field))

    def test_invalid_timestamp_paths_are_rejected(self):
        invalid = [
            f"{prefix}{suffix}"
            for prefix in ("$aas#", "$sm#", "$cd#", "$aasdesc#", "$smdesc#")
            for suffix in (
                "createdAt", "updatedAt", "administration.CreatedAt",
                "administration.updatedat", "administration.createdAt[]",
                "administration.updatedAt.value", "administration.version",
            )
        ]
        invalid += [
            f"{prefix}administration.{attribute}"
            for prefix in (
                "$sme#", "$sme.OperationalData#", "$sme.OperationalData[]#",
                "$aas#assetInformation.", "$aas#submodels[].",
                "$aasdesc#submodelDescriptors.",
                "$aasdesc#submodelDescriptors[01].",
                "$aasdesc#submodelDescriptors[-1].",
                "$aasdesc#endpoints[].",
            )
            for attribute in ("createdAt", "updatedAt")
        ]
        for definition in ("FieldIdentifier", "FragmentFieldIdentifier"):
            for field in invalid:
                with self.subTest(definition=definition, field=field):
                    self.assertIsNone(self.patterns[definition].fullmatch(field))

    def test_timestamp_comparisons_use_existing_datetime_cast(self):
        for field in TIMESTAMP_FIELDS:
            for operator in ("$eq", "$ne", "$gt", "$ge", "$lt", "$le"):
                with self.subTest(field=field, operator=operator):
                    self.assert_valid({
                        "$condition": {operator: [
                            {"$dateTimeCast": {"$field": field}},
                            {"$dateTimeVal": "2026-10-01T00:00:00Z"},
                        ]},
                    })

    def test_timestamp_fragment_filters_are_valid(self):
        for field in TIMESTAMP_FIELDS:
            with self.subTest(field=field):
                self.assert_valid({
                    "$condition": {"$boolean": True},
                    "$filters": [{
                        "$fragment": field,
                        "$condition": {"$boolean": False},
                    }],
                })

    def test_timestamp_references_in_access_rule_formulas(self):
        for root in ("aas", "sm", "cd"):
            for attribute in ("createdAt", "updatedAt"):
                reference = f'${root}("urn:example:object")#administration.{attribute}'
                with self.subTest(reference=reference):
                    self.assertIsNotNone(self.patterns["ReferenceIdentifier"].fullmatch(reference))
                    self.assert_valid({
                        "rules": [{
                            "ACL": {
                                "ATTRIBUTES": [{"CLAIM": "bpn"}],
                                "RIGHTS": ["READ"],
                                "ACCESS": "ALLOW",
                            },
                            "OBJECTS": [{"IDENTIFIABLE": f'${root}("urn:example:object")'}],
                            "FORMULA": {"$ge": [
                                {"$dateTimeCast": {"$attribute": {"REFERENCE": reference}}},
                                {"$dateTimeVal": "2026-10-01T00:00:00Z"},
                            ]},
                        }],
                    })

    def test_timestamp_reference_scope_is_not_widened(self):
        for reference in (
            '$sme("urn:example:object").Temperature#administration.createdAt',
            '$sme("urn:example:object").Temperature#administration.updatedAt',
            '$aasdesc("urn:example:object")#administration.updatedAt',
            '$smdesc("urn:example:object")#administration.updatedAt',
            '$sm("urn:example:object")#createdAt',
            '$sm("urn:example:object")#administration.updatedAt[]',
        ):
            with self.subTest(reference=reference):
                self.assertIsNone(self.patterns["ReferenceIdentifier"].fullmatch(reference))


if __name__ == "__main__":
    unittest.main()
