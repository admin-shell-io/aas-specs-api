import json
import re
import unittest
from pathlib import Path


ROOT_MODULE = Path(__file__).resolve().parents[4]
QUERY_SCHEMA = ROOT_MODULE / "partials" / "query-json-schema.json"
SCHEMA_PAGE = ROOT_MODULE / "pages" / "schema.adoc"
OPENAPI_SCHEMA = ROOT_MODULE.parents[3] / "Part2-API-Schemas" / "openapi.yaml"


def schema_page_pattern(definition):
    lines = SCHEMA_PAGE.read_text(encoding="utf-8-sig").splitlines()
    schema = json.loads("\n".join(lines[1:-1]))
    return schema["definitions"][definition]["pattern"]


def openapi_component_pattern(component):
    lines = OPENAPI_SCHEMA.read_text(encoding="utf-8-sig").splitlines()
    for index, line in enumerate(lines):
        if line.strip() == f"{component}:":
            for candidate_index, candidate in enumerate(lines[index + 1 :], start=index + 1):
                if candidate.strip() == "pattern: >-":
                    return lines[candidate_index + 1].strip()
    raise AssertionError(f"OpenAPI component pattern not found: {component}")


class FieldIdentifierRegexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(QUERY_SCHEMA.read_text(encoding="utf-8-sig"))
        pattern = schema["definitions"]["FieldIdentifier"]["pattern"]
        cls.pattern = pattern
        cls.field_identifier = re.compile(pattern)

    def assert_allowed(self, value):
        self.assertIsNotNone(
            self.field_identifier.fullmatch(value),
            f"Expected FieldIdentifier to allow: {value}",
        )

    def assert_not_allowed(self, value):
        self.assertIsNone(
            self.field_identifier.fullmatch(value),
            f"Expected FieldIdentifier to reject: {value}",
        )

    def test_allowed_field_identifiers(self):
        allowed = [
            "$aas#idShort",
            "$aas#id",
            "$aas#assetInformation.assetKind",
            "$aas#assetInformation.assetType",
            "$aas#assetInformation.globalAssetId",
            "$aas#assetInformation.specificAssetIds[].name",
            "$aas#assetInformation.specificAssetIds[0].name",
            "$aas#assetInformation.specificAssetIds[].value",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.type",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys[].type",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys[0].value",
            "$aas#submodels[]",
            "$aas#submodels[].type",
            "$aas#submodels[].keys[].type",
            "$aas#submodels[0].keys[0].value",
            "$sm#semanticId",
            "$sm#semanticId.type",
            "$sm#semanticId.keys[].type",
            "$sm#semanticId.keys[0].value",
            "$sm#supplementalSemanticIds",
            "$sm#supplementalSemanticIds[]",
            "$sm#supplementalSemanticIds[0]",
            "$sm#supplementalSemanticIds.type",
            "$sm#supplementalSemanticIds[].type",
            "$sm#supplementalSemanticIds[].keys[].type",
            "$sm#supplementalSemanticIds[0].keys[0].value",
            "$sm#idShort",
            "$sm#id",
            "$sme#semanticId",
            "$sme#semanticId.type",
            "$sme#semanticId.keys[].type",
            "$sme#semanticId.keys[0].value",
            "$sme#supplementalSemanticIds",
            "$sme#supplementalSemanticIds[]",
            "$sme#supplementalSemanticIds[0].type",
            "$sme#supplementalSemanticIds[].keys[].type",
            "$sme#supplementalSemanticIds[0].keys[0].value",
            "$sme#idShort",
            "$sme#value",
            "$sme#valueType",
            "$sme#language",
            "$sme.AddressInformation#supplementalSemanticIds",
            "$sme.AddressInformation#supplementalSemanticIds[].keys[].value",
            "$sme.AddressInformation#value",
            "$sme.AddressInformation.Zipcode#value",
            "$sme.AddressInformation[]#value",
            "$sme.AddressInformation[0].Zipcode#value",
            "$cd#idShort",
            "$cd#id",
            "$aasdesc#idShort",
            "$aasdesc#id",
            "$aasdesc#assetKind",
            "$aasdesc#assetType",
            "$aasdesc#globalAssetId",
            "$aasdesc#specificAssetIds[].name",
            "$aasdesc#specificAssetIds[].value",
            "$aasdesc#specificAssetIds[].externalSubjectId",
            "$aasdesc#specificAssetIds[].externalSubjectId.type",
            "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value",
            "$aasdesc#endpoints[].interface",
            "$aasdesc#endpoints[0].protocolinformation.href",
            "$aasdesc#submodelDescriptors[].semanticId",
            "$aasdesc#submodelDescriptors[].semanticId.type",
            "$aasdesc#submodelDescriptors[].semanticId.keys[].value",
            "$aasdesc#submodelDescriptors[].supplementalSemanticIds",
            "$aasdesc#submodelDescriptors[].supplementalSemanticIds[]",
            "$aasdesc#submodelDescriptors[].supplementalSemanticIds[0].type",
            "$aasdesc#submodelDescriptors[].supplementalSemanticIds[].keys[].value",
            "$aasdesc#submodelDescriptors[].idShort",
            "$aasdesc#submodelDescriptors[].id",
            "$aasdesc#submodelDescriptors[].endpoints[].interface",
            "$aasdesc#submodelDescriptors[0].endpoints[0].protocolinformation.href",
            "$smdesc#semanticId",
            "$smdesc#semanticId.type",
            "$smdesc#semanticId.keys[].value",
            "$smdesc#supplementalSemanticIds",
            "$smdesc#supplementalSemanticIds[]",
            "$smdesc#supplementalSemanticIds[0].type",
            "$smdesc#supplementalSemanticIds[].keys[].value",
            "$smdesc#idShort",
            "$smdesc#id",
            "$smdesc#endpoints[].interface",
            "$smdesc#endpoints[0].protocolinformation.href",
        ]

        for value in allowed:
            with self.subTest(value=value):
                self.assert_allowed(value)

    def test_not_allowed_field_identifiers(self):
        not_allowed = [
            "$aas#assetInformation.specificAssetIds",
            "$aas#assetInformation.specificAssetIds[]",
            "$aas#assetInformation.specificAssetIds[01].name",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys[]",
            "$aas#submodels",
            "$aas#submodels[01].type",
            "$aas#submodels[].keys",
            "$aas#submodels[].keys[]",
            "$sm#semanticId.keys",
            "$sm#semanticId.keys[]",
            "$sm#supplementalSemanticIds[01]",
            "$sm#supplementalSemanticIds.keys",
            "$sm#supplementalSemanticIds.keys[]",
            "$sm#supplementalSemanticIds[].keys",
            "$sm#supplementalSemanticIds[].keys[]",
            "$sme",
            "$sme.AddressInformation",
            "$sme.AddressInformation[]",
            "$sme.AddressInformation#id",
            "$sme.AddressInformation#bogus",
            "$sme.AddressInformation#supplementalSemanticIds[01]",
            "$sme.AddressInformation#supplementalSemanticIds.keys",
            "$sme.AddressInformation#supplementalSemanticIds[].keys",
            "$sme.1Invalid#value",
            "$cd",
            "$cd#description",
            "$aasdesc#description",
            "$aasdesc#displayName",
            "$aasdesc#extension",
            "$aasdesc#administration",
            "$aasdesc#specificAssetIds",
            "$aasdesc#specificAssetIds[]",
            "$aasdesc#specificAssetIds[].externalSubjectId.keys",
            "$aasdesc#specificAssetIds[].externalSubjectId.keys[]",
            "$aasdesc#endpoints",
            "$aasdesc#endpoints[]",
            "$aasdesc#endpoints[01].interface",
            "$aasdesc#endpoints[].protocolinformation",
            "$aasdesc#submodelDescriptors",
            "$aasdesc#submodelDescriptors[]",
            "$aasdesc#submodelDescriptors[01].idShort",
            "$aasdesc#submodelDescriptors[].supplementalSemanticIds.keys",
            "$aasdesc#submodelDescriptors[].supplementalSemanticIds[].keys",
            "$aasdesc#submodelDescriptors[].endpoints",
            "$aasdesc#submodelDescriptors[].endpoints[]",
            "$smdesc#semanticId.keys",
            "$smdesc#semanticId.keys[]",
            "$smdesc#supplementalSemanticIds.keys",
            "$smdesc#supplementalSemanticIds[01]",
            "$smdesc#supplementalSemanticIds[].keys",
            "$smdesc#endpoints",
            "$smdesc#endpoints[]",
            "$smdesc#endpoints[01].interface",
            "$smdesc#endpoints[].protocolinformation",
        ]

        for value in not_allowed:
            with self.subTest(value=value):
                self.assert_not_allowed(value)

    def test_documented_field_identifier_patterns_are_in_sync(self):
        self.assertEqual(self.pattern, schema_page_pattern("FieldIdentifier"))
        self.assertEqual(self.pattern, openapi_component_pattern("FieldIdentifier"))


class ReferenceIdentifierRegexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(QUERY_SCHEMA.read_text(encoding="utf-8-sig"))
        pattern = schema["definitions"]["ReferenceIdentifier"]["pattern"]
        cls.pattern = pattern
        cls.reference_identifier = re.compile(pattern)

    def assert_allowed(self, value):
        self.assertIsNotNone(
            self.reference_identifier.fullmatch(value),
            f"Expected ReferenceIdentifier to allow: {value}",
        )

    def assert_not_allowed(self, value):
        self.assertIsNone(
            self.reference_identifier.fullmatch(value),
            f"Expected ReferenceIdentifier to reject: {value}",
        )

    def test_allowed_reference_identifiers(self):
        allowed = [
            '$aas("aas-id")#assetInformation.specificAssetIds[].externalSubjectId.keys[0].value',
            '$sm("SubmodelID")#id',
            '$sm("SubmodelID")#supplementalSemanticIds[].keys[].value',
            '$cd("ConceptDescriptionID")#idShort',
            '$sme("SubmodelID-OperationalData").machineState#value',
            '$sme("SubmodelID").AddressInformation[0].Zipcode#semanticId.keys[].value',
        ]

        for value in allowed:
            with self.subTest(value=value):
                self.assert_allowed(value)

    def test_not_allowed_reference_identifiers(self):
        not_allowed = [
            "$sm#id",
            '$sm("SubmodelID")#bogus',
            '$sm("SubmodelID")#supplementalSemanticIds[01]',
            '$aas("aas-id")#assetInformation.specificAssetIds[]',
            '$cd("ConceptDescriptionID")#description',
            '$sme("SubmodelID").machineState',
            '$sme("SubmodelID").machineState#id',
            '$sme("SubmodelID").1Invalid#value',
            '$aasdesc("aas-id")#idShort',
        ]

        for value in not_allowed:
            with self.subTest(value=value):
                self.assert_not_allowed(value)

    def test_documented_reference_identifier_patterns_are_in_sync(self):
        self.assertEqual(self.pattern, schema_page_pattern("ReferenceIdentifier"))


if __name__ == "__main__":
    unittest.main()
