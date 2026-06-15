import json
import re
import unittest
from pathlib import Path


ROOT_MODULE = Path(__file__).resolve().parents[4]
QUERY_SCHEMA = ROOT_MODULE / "partials" / "query-json-schema.json"


class FieldIdentifierRegexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(QUERY_SCHEMA.read_text(encoding="utf-8-sig"))
        pattern = schema["definitions"]["FieldIdentifier"]["pattern"]
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
            "$aas#submodels[].type",
            "$aas#submodels[].keys[].type",
            "$aas#submodels[0].keys[0].value",
            "$sm#semanticId",
            "$sm#semanticId.type",
            "$sm#semanticId.keys[].type",
            "$sm#semanticId.keys[0].value",
            "$sm#idShort",
            "$sm#id",
            "$sme#semanticId",
            "$sme#semanticId.type",
            "$sme#semanticId.keys[].type",
            "$sme#semanticId.keys[0].value",
            "$sme#idShort",
            "$sme#value",
            "$sme#valueType",
            "$sme#language",
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
            "$aasdesc#submodelDescriptors[].idShort",
            "$aasdesc#submodelDescriptors[].id",
            "$aasdesc#submodelDescriptors[].endpoints[].interface",
            "$aasdesc#submodelDescriptors[0].endpoints[0].protocolinformation.href",
            "$smdesc#semanticId",
            "$smdesc#semanticId.type",
            "$smdesc#semanticId.keys[].value",
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
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys[]",
            "$aas#submodels",
            "$aas#submodels[]",
            "$aas#submodels[].keys",
            "$aas#submodels[].keys[]",
            "$sm#semanticId.keys",
            "$sm#semanticId.keys[]",
            "$sm#supplementalSemanticIds",
            "$sme",
            "$sme.AddressInformation",
            "$sme.AddressInformation[]",
            "$sme.AddressInformation#id",
            "$sme.AddressInformation#bogus",
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
            "$aasdesc#endpoints[].protocolinformation",
            "$aasdesc#submodelDescriptors",
            "$aasdesc#submodelDescriptors[]",
            "$aasdesc#submodelDescriptors[].endpoints",
            "$aasdesc#submodelDescriptors[].endpoints[]",
            "$smdesc#semanticId.keys",
            "$smdesc#semanticId.keys[]",
            "$smdesc#endpoints",
            "$smdesc#endpoints[]",
            "$smdesc#endpoints[].protocolinformation",
        ]

        for value in not_allowed:
            with self.subTest(value=value):
                self.assert_not_allowed(value)


if __name__ == "__main__":
    unittest.main()
