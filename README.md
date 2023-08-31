# This is the repository for the AAS API Definitions

[![Creative Commons License](
https://licensebuttons.net/l/by/4.0/88x31.png
)](
https://creativecommons.org/licenses/by/4.0/
)

This repository contains specifications of the Asset Administration Shell APIs, including in particular the normative OpenAPI files of the AAS HTTP/REST API.
These API descriptions are derived from the document series, part 2,
["Specification of the Asset Administration Shell - Part 2"](
https://industrialdigitaltwin.org/en/content-hub/
) published by the [IDTA](https://industrialdigitaltwin.org/en/).



## Content
This repository provides the OpenAPI files published in the SwaggerHub organization [Plattform_i40](https://app.swaggerhub.com/search?owner=Plattform_i40).
All published SwaggerHub APIs are synchronized all the time with the respective folders in this repository using the [GitHub Integration](https://support.smartbear.com/swaggerhub/docs/integrations/github-sync.html) feature. In particular, the following APIs are contained:

|API SPEC|GitHub|SwaggerHub|
|-----------------------------------------------------------------------|-----------------------------------------------------------------|----------------------------------------------------|
| Entire-API-Collection API |[Link](./Entire-API-Collection/openapi.yaml)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection)|
| Asset Administration Shell Registry Service Specification|[Link](./AssetAdministrationShellRegistryServiceSpecification)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShellRegistryServiceSpecification)|
| Asset Administration Shell Repository Service Specification|[Link](./AssetAdministrationShellRepositoryServiceSpecification)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShellRepositoryServiceSpecification)|
| Asset Administration Shell Service Specification|[Link](./AssetAdministrationShellServiceSpecification)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShellServiceSpecification)|
| Submodel Registry Service Specification |[Link](./SubmodelRegistryServiceSpecification)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/SubmodelRegistryServiceSpecification)|
| Submodel Repository Service Specification|[Link](./SubmodelRepositoryServiceSpecification)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/SubmodelRepositoryServiceSpecification)|
| Submodel Service Specification|[Link](./SubmodelServiceSpecification)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/SubmodelServiceSpecification)|
| Discovery Service Description API |[Link](./DiscoveryServiceDescription)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/DiscoveryServiceDescription)|
| AASX-File-Server API |[Link](./AASX-File-Server/openapi.yaml)|[Link](https://app.swaggerhub.com/apis/Plattform_i40/AASX-File-Server)|

The following *domains* are synchronized manually as domain synchronization is not yet available in SwaggerHub:
|API SPEC|GitHub|SwaggerHub|
|------------------------------------------------------------------------|-----------------------------------------------------------------|----------------------------------------------------|
| Part1-MetaModel-Schemas Domain |[Link](./Part1-MetaModel-Schemas/openapi.yaml)|[Link](https://app.swaggerhub.com/domains/Plattform_i40/Part1-MetaModel-Schemas)|
| Part2-API-Schemas Domain |[Link](./Part2-API-Schemas/openapi.yaml)|[Link](https://app.swaggerhub.com/domains/Plattform_i40/Part2-API-Schemas)|
| DINSPEC16593-Schemas Domain |[Link](./DINSPEC16593-Schemas/openapi.yaml)|[Link](https://app.swaggerhub.com/domains/Plattform_i40/DINSPEC16593-Schemas)|

## API Versions in GitHub Branches

The `main` branch contains the latest released version of all APIs and Domains. Current and previously released states are tagged with the corresponding release version in this repository, and marked with the `Published` tag in SwaggerHub.
Working versions may be marked as `private` in SwaggerHub and therfore may not be visible to the public audience yet. In this repository, working versions appear as branches named after the target release version.  
**Note:** In order to synchronize with the same GitHub branch, all versions should follow the exact same pattern.

### Releases

The following versioning scheme is applied for release tags: 'V\<major>.\<minor>.\<patch>'. 
Major versions indicate breaking changes while minor updates are backward compatible.
The patch position is increased whenever bugfixes need to be applied. 
The following release contains the latest version of the AAS schemas (see also the [releases](https://github.com/admin-shell-io/aas-specs-api/releases) section of this repository):
* [3.0.1](https://github.com/admin-shell-io/aas-specs/releases/tag/V3.0.1) is the corresponding release for the `V3.0.1` version of the AAS APIs, containing the normative schemas for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - **Version 3.0.1**". *Use this release if you want to work with the latest specified AAS version.*

Previous releases (deprecated by [3.0.1](https://github.com/admin-shell-io/aas-specs/releases/tag/V3.0.1)):
* [3.0](https://github.com/admin-shell-io/aas-specs/releases/tag/V3.0) is the first major release for the AAS APIs, containing the normative API descriptions for the published document "Specification of the Asset Administration Shell - Part 2: Application Programming Interfaces - Version 3.0".


## Contributing

Feature requests, reports about inconsistencies, mistakes *etc.* are highly
welcome! Please [submit a new issue](
https://github.com/admin-shell-io/aas-specs-api/issues/new/choose
).

If you want to contribute, see [CONTRIBUTING.md](CONTRIBUTING.md).



## SwaggerHub GitHub Synchronization

SwaggerHub requires a GitHub Access Token with `repo` permissions. It is good practice that the selected token has a defined expiration date. Therefore, at some point in time when the current token expires, the synchronization will fail and a new token needs to be added through the IDTA repository management team.
