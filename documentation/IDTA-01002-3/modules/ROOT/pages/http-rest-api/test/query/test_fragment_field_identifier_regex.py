import json
import re
import unittest
from pathlib import Path


ROOT_MODULE = Path(__file__).resolve().parents[4]
QUERY_SCHEMA = ROOT_MODULE / "partials" / "query-json-schema.json"


class FragmentFieldIdentifierRegexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(QUERY_SCHEMA.read_text(encoding="utf-8-sig"))
        pattern = schema["definitions"]["FragmentFieldIdentifier"]["pattern"]
        cls.fragment_field_identifier = re.compile(pattern)

    def assert_allowed(self, value):
        self.assertIsNotNone(
            self.fragment_field_identifier.fullmatch(value),
            f"Expected FragmentFieldIdentifier to allow: {value}",
        )

    def assert_not_allowed(self, value):
        self.assertIsNone(
            self.fragment_field_identifier.fullmatch(value),
            f"Expected FragmentFieldIdentifier to reject: {value}",
        )

    def test_allowed_fragment_field_identifiers(self):
        allowed = [
            "$aas#idShort",
            "$aas#assetInformation.assetType",
            "$aas#assetInformation.globalAssetId",
            "$aas#assetInformation.specificAssetIds",
            "$aas#assetInformation.specificAssetIds[]",
            "$aas#assetInformation.specificAssetIds[0]",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys[]",
            "$aas#assetInformation.specificAssetIds[].externalSubjectId.keys[0]",
            "$aas#submodels",
            "$aas#submodels[]",
            "$aas#submodels[0]",
            "$aas#submodels[].keys",
            "$aas#submodels[].keys[]",
            "$aas#submodels[].keys[0]",
            "$sm#semanticId",
            "$sm#semanticId.keys",
            "$sm#semanticId.keys[]",
            "$sm#semanticId.keys[0]",
            "$sm#idShort",
            "$sme",
            "$sme.AddressInformation",
            "$sme.AddressInformation[]",
            "$sme.AddressInformation[0]",
            "$sme.AddressInformation.Zipcode",
            "$sme.AddressInformation[]#value",
            "$sme.AddressInformation#semanticId",
            "$sme.AddressInformation#semanticId.keys",
            "$sme.AddressInformation#semanticId.keys[]",
            "$sme#idShort",
            "$sme#value",
            "$sme#valueType",
            "$sme#language",
            "$cd#idShort",
            "$aasdesc#idShort",
            "$aasdesc#description",
            "$aasdesc#displayName",
            "$aasdesc#extension",
            "$aasdesc#administration",
            "$aasdesc#assetKind",
            "$aasdesc#assetType",
            "$aasdesc#globalAssetId",
            "$aasdesc#specificAssetIds",
            "$aasdesc#specificAssetIds[]",
            "$aasdesc#specificAssetIds[].externalSubjectId.keys[]",
            "$aasdesc#endpoints",
            "$aasdesc#endpoints[]",
            "$aasdesc#endpoints[0]",
            "$aasdesc#submodelDescriptors",
            "$aasdesc#submodelDescriptors[]",
            "$aasdesc#submodelDescriptors[0]",
            "$aasdesc#submodelDescriptors[].semanticId",
            "$aasdesc#submodelDescriptors[].semanticId.keys[]",
            "$aasdesc#submodelDescriptors[].idShort",
            "$aasdesc#submodelDescriptors[].endpoints",
            "$aasdesc#submodelDescriptors[].endpoints[]",
            "$smdesc#semanticId",
            "$smdesc#semanticId.keys",
            "$smdesc#semanticId.keys[]",
            "$smdesc#idShort",
            "$smdesc#endpoints",
            "$smdesc#endpoints[]",
        ]

        for value in allowed:
            with self.subTest(value=value):
                self.assert_allowed(value)

    def test_not_allowed_fragment_field_identifiers(self):
        not_allowed = [
            "$aas#id",
            "$aas#assetInformation.assetKind",
            "$aas#assetInformation.specificAssetIds.name",
            "$aas#assetInformation.specificAssetIds[].name",
            "$aas#assetInformation.specificAssetIds[].value",
            "$aas#assetInformation.specificAssetIds.keys[]",
            "$aas#assetInformation.specificAssetIds.externalSubjectId.keys[]",
            "$aas#submodels.keys[]",
            "$aas#submodels[].type",
            "$aas#submodels[].keys[].value",
            "$sm#semanticId.type",
            "$sm#semanticId.keys[].value",
            "$sm#id",
            "$sm#supplementalSemanticIds",
            "$sme.1Invalid",
            "$sme.AddressInformation#id",
            "$sme.AddressInformation#bogus",
            "$sme.AddressInformation#semanticId.type",
            "$sme.AddressInformation#semanticId.keys[].value",
            "$cd#id",
            "$aasdesc#id",
            "$aasdesc#specificAssetIds.name",
            "$aasdesc#specificAssetIds[].name",
            "$aasdesc#endpoints.protocolinformation.href",
            "$aasdesc#submodelDescriptors.endpoints[]",
            "$aasdesc#submodelDescriptors[].id",
            "$aasdesc#submodelDescriptors[].endpoints.protocolinformation.href",
            "$smdesc#id",
            "$smdesc#endpoints.protocolinformation.href",
        ]

        for value in not_allowed:
            with self.subTest(value=value):
                self.assert_not_allowed(value)


if __name__ == "__main__":
    unittest.main()
