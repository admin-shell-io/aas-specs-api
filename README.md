# This is the repository for the AAS API Definitions

[![Creative Commons License](
https://licensebuttons.net/l/by/4.0/88x31.png
)](
https://creativecommons.org/licenses/by/4.0/
)

This repository contains specifications of the Asset Administration Shell API, including in particular the normative OpenAPI files of the AAS REST API.
These API descriptions are derived from the document series, part 2,
["Details of the Asset Administration Shell"](
https://www.plattform-i40.de/PI40/Redaktion/EN/Standardartikel/specification-administrationshell.html
) published by the [Platform Industrie 4.0](http://www.plattform-i40.de) and [IDTA](https://industrialdigitaltwin.org/en/).



## Content
This repository provides the OpenAPI files published in the SwaggerHub organization [Plattform_i40](https://app.swaggerhub.com/search?owner=Plattform_i40).
All published SwaggerHub APIs are synchronized all the time with the respective folders in this repository using the [GitHub Integration](https://support.smartbear.com/swaggerhub/docs/integrations/github-sync.html) feature. In particular, the following APIs are contained:
* [Entire-API-Collection/openapi.yaml](./Entire-API-Collection/openapi.yaml) matches the [Entire-API-Collection API at SwaggerHub](https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection)
* [AssetAdministrationShell-Environment/openapi.yaml](./AssetAdministrationShell-Environment/openapi.yaml) matches the [AssetAdministrationShell-Environment API at SwaggerHub](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdministrationShell-Environment)
* [AssetAdminstrationShell-API/openapi.yaml](./AssetAdminstrationShell-API/openapi.yaml) matches the [AssetAdminstrationShell API at SwaggerHub](https://app.swaggerhub.com/apis/Plattform_i40/AssetAdminstrationShell-API)
* [Submodel-API/openapi.yaml](./Submodel-API/openapi.yaml) matches the [Submodel API at SwaggerHub](https://app.swaggerhub.com/apis/Plattform_i40/Submodel-API)
* [AASX-File-Server/openapi.yaml](./AASX-File-Server/openapi.yaml) matches the [AASX-File-Server API at SwaggerHub](https://app.swaggerhub.com/apis/Plattform_i40/AASX-File-Server)
* [Registry-and-Discovery/openapi.yaml](./Registry-and-Discovery/openapi.yaml) matches the [Registry-and-Discovery API at SwaggerHub](https://app.swaggerhub.com/apis/Plattform_i40/Registry-and-Discovery)

The following *domains* are synchronized manually as domain synchronization is not yet available in SwaggerHub:
* [Part1-MetaModel-Schemas/openapi.yaml](./art1-MetaModel-Schemas/openapi.yaml) matches the [Part1-MetaModel-Schemas Domain at SwaggerHub](https://app.swaggerhub.com/domains/Plattform_i40/Part1-MetaModel-Schemas)
* [Part2-API-Schemas/openapi.yaml](./Part2-API-Schemas/openapi.yaml) matches the [Part2-API-Schemas Domain at SwaggerHub](https://app.swaggerhub.com/domains/Plattform_i40/Part2-API-Schemas)
* [DINSPEC16593-Schemas/openapi.yaml](./DINSPEC16593-Schemas/openapi.yaml) matches the [DINSPEC16593-Schemas Domain at SwaggerHub](https://app.swaggerhub.com/domains/Plattform_i40/DINSPEC16593-Schemas)



## API Versions in GitHub Branches

The `main` branch contains the latest released version of all APIs and Domains. Current and previously released states are tagged with the corresponding release version in this repository, and marked with the `Published` tag in SwaggerHub.
Working versions may be marked as `private` in SwaggerHub and therfore may not be visible to the public audience yet. In this repository, working versions appear as branches named after the target release version. Note: In order to synchronize with the same GitHub branch, all versions should follow the exact same pattern.


## Contributing

Feature requests, reports about inconsistencies, mistakes *etc.* are highly
welcome! Please [submit a new issue](
https://github.com/admin-shell-io/aas-specs-api/issues/new
).

If you want to contribute, see [CONTRIBUTING.md](CONTRIBUTING.md).



## SwaggerHub GitHub Synchronization

SwaggerHub requires a GitHub Access Token with `repo` permissions. It is good practice that the selected token has a defined expiration date. Therefore, at some point in the future when the current token expires, the synchronization will fail and a new token needs to be added through the IDTA repository management team.
