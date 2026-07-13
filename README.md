# IDTA-01002 - APIs of the Asset Administration Shell

[![Creative Commons License](
https://licensebuttons.net/l/by/4.0/88x31.png
)](
https://creativecommons.org/licenses/by/4.0/
)

This repository contains specifications of the APIs of the Asset Administration Shell (AAS), including the normative OpenAPI files of the AAS HTTP/REST API.

## Industrial Digital Twin Association (IDTA)

Governance of the specification is done in the working group Open Technology of the [IDTA](https://industrialdigitaltwin.org/en/)

The specification number is: **IDTA-01002**

## Content
This repository provides the OpenAPI files published via [GitHub Pages](https://industrialdigitaltwin.io/aas-specs-api/docs/index.html). For legacy reasons, versions up to V3.1.3 are also available in the SwaggerHub organization [Plattform_i40](https://app.swaggerhub.com/search?owner=Plattform_i40). In particular, the following APIs are contained:

|API SPEC|GitHub|GitHub Pages|SwaggerHub [^1] |
|-----------------------------------------------------------------------|------------------------------------------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
|Entire-API-Collection |[Link](./Entire-API-Collection/V3.2.yaml)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../Entire-API-Collection/V3.2.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection)|
|Asset Administration Shell Registry Service Specification|[Link](./AssetAdministrationShellRegistryServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../AssetAdministrationShellRegistryServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShellRegistryServiceSpecification)|
|Asset Administration Shell Repository Service Specification|[Link](./AssetAdministrationShellRepositoryServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../AssetAdministrationShellRepositoryServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShellRepositoryServiceSpecification)|
|Asset Administration Shell Service Specification|[Link](./AssetAdministrationShellServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../AssetAdministrationShellServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShellServiceSpecification)|
|Submodel Registry Service Specification |[Link](./SubmodelRegistryServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../SubmodelRegistryServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/SubmodelRegistryServiceSpecification)|
|Submodel Repository Service Specification|[Link](./SubmodelRepositoryServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../SubmodelRepositoryServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/SubmodelRepositoryServiceSpecification)|
|Submodel Service Specification|[Link](./SubmodelServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../SubmodelServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/SubmodelServiceSpecification)|
|Discovery Service Specification |[Link](./DiscoveryServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../DiscoveryServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/DiscoveryServiceSpecification)|
|Concept Description Repository Service Specification|[Link](./ConceptDescriptionRepositoryServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../ConceptDescriptionRepositoryServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/ConceptDescriptionRepositoryServiceSpecification)|
|Aasx-File-Server Service Specification |[Link](./AasxFileServerServiceSpecification)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../AasxFileServerServiceSpecification/V3.2_SSP-001.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/AasxFileServerServiceSpecification)|

The following *domains* are also published:
|API SPEC|GitHub|GitHub Pages|SwaggerHub [^1] |
|------------------------------------------------------------------------|------------------------------------------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| Part1-MetaModel-Schemas Domain |[Link](./Part1-MetaModel-Schemas/openapi.yaml)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=./Part1-MetaModel-Schemas/openapi_3.2.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/domains/Plattform_i40/Part1-MetaModel-Schemas)|
| Part2-API-Schemas Domain |[Link](./Part2-API-Schemas/openapi.yaml)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../Part2-API-Schemas/openapi.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/domains/Plattform_i40/Part2-API-Schemas)|
| DINSPEC16593-Schemas Domain (Deprecated) |[Link](./DINSPEC16593-Schemas/openapi.yaml)|[Link](https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html?url=../DINSPEC16593-Schemas/openapi.yaml&version=v3.2.0)|[Link](https://app.swaggerhub.com/domains/Plattform_i40/DINSPEC16593-Schemas)|

[^1]: Swaggerhub links are only provided for legacy reasons. Latest OpenAPI versions are only hosted via Github Pages.

The sources of the specification, both website and PDF document, are maintained in the [documentation](./documentation/) folder. The different versions are identified through the respective release tags, while the latest state on the `main` branch always represents a `SNAPSHOT` version.


## API Versions in GitHub Branches

The `main` branch contains the latest released version of all APIs and Domains. Current and previously released states are tagged with the corresponding release version in this repository. Working versions appear as branches named after the target release version.

### Releases

The following versioning scheme is applied for release tags: 'V\<major>.\<minor>.\<patch>'.
Major versions indicate breaking changes while minor updates are backward compatible.
The patch position is increased whenever bugfixes need to be applied.
The following release contains the latest version of the AAS schemas (see also the [releases](https://github.com/admin-shell-io/aas-specs-api/releases) section of this repository):

* [3.2.0](https://github.com/admin-shell-io/aas-specs-api/releases/tag/v3.2.0) is the latest release for the `V3.2.0` version of the AAS APIs, containing the normative specification and schemas of IDTA-01002-3-2.
* *Use this release if you want to work with the latest specified AAS version.*

Previous releases:

* [3.1.3](https://github.com/admin-shell-io/aas-specs-api/releases/tag/v3.1.3) is the latest bugfix release for the `V3.1` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.1.3".

* [3.1.2](https://github.com/admin-shell-io/aas-specs-api/releases/tag/v3.1.2) is a bugfix release for the `V3.1` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.1.2".

* [3.1.1](https://github.com/admin-shell-io/aas-specs-api/releases/tag/v3.1.1) is a bugfix release for the `V3.1` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.1.1".

* [3.1.0](https://github.com/admin-shell-io/aas-specs-api/releases/tag/v3.1.0) is the release for the `V3.1` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.1.0".

* [3.0.4](https://github.com/admin-shell-io/aas-specs-api/releases/tag/v3.0.4) is the latest bugfix release for the `V3.0.4` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.0.4".

* [3.0.3](https://github.com/admin-shell-io/aas-specs-api/releases/tag/V3.0.3) is the bugfix release for the `V3.0.3` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.0.3".

* [3.0.2](https://github.com/admin-shell-io/aas-specs-api/releases/tag/V3.0.2) is the bugfix release for the `V3.0.2` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.0.2".

* [3.0.1](https://github.com/admin-shell-io/aas-specs-api/releases/tag/V3.0.1) is the bugfix release for the `V3.0.1` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.0.1".

* [3.0](https://github.com/admin-shell-io/aas-specs-api/releases/tag/V3.0) is the first major release for the AAS APIs, containing the normative API descriptions for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.0".


## Contributing

Feature requests, reports about inconsistencies, mistakes *etc.* are highly
welcome! Please [submit a new issue](
https://github.com/admin-shell-io/aas-specs-api/issues/new/choose
).

If you want to contribute, see [CONTRIBUTING.md](CONTRIBUTING.md).


