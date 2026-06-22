#!/bin/bash

# Script to generate resolved (dereferenced) OpenAPI specs
# All $ref references are resolved inline for easier consumption

set -e

RESOLVED_DIR="docs/resolved"
mkdir -p "$RESOLVED_DIR"

echo "Generating resolved OpenAPI specifications..."
echo "This may take a few minutes..."

# Function to bundle a spec
bundle_spec() {
    local input=$1
    local output=$2
    local name=$3

    echo "  Processing: $name"
    if redocly bundle "$input" -o "$output" --dereferenced 2>/dev/null; then
        echo "    ✓ Generated: $output"
    else
        echo "    ✗ Failed: $name (skipping)"
    fi
}

# Entire API Collection
bundle_spec "Entire-API-Collection/V3.2.yaml" "$RESOLVED_DIR/Entire-API-Collection_V3.2_resolved.yaml" "Entire API Collection"

# AAS Registry Service
bundle_spec "AssetAdministrationShellRegistryServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/AAS-Registry_SSP-001_resolved.yaml" "AAS Registry SSP-001"

# AAS Repository Service
bundle_spec "AssetAdministrationShellRepositoryServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/AAS-Repository_SSP-001_resolved.yaml" "AAS Repository SSP-001"

# AAS Service
bundle_spec "AssetAdministrationShellServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/AAS-Service_SSP-001_resolved.yaml" "AAS Service SSP-001"

# Submodel Registry Service
bundle_spec "SubmodelRegistryServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/Submodel-Registry_SSP-001_resolved.yaml" "Submodel Registry SSP-001"

# Submodel Repository Service
bundle_spec "SubmodelRepositoryServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/Submodel-Repository_SSP-001_resolved.yaml" "Submodel Repository SSP-001"

# Submodel Service
bundle_spec "SubmodelServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/Submodel-Service_SSP-001_resolved.yaml" "Submodel Service SSP-001"

# Discovery Service
bundle_spec "DiscoveryServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/Discovery-Service_SSP-001_resolved.yaml" "Discovery Service SSP-001"

# Concept Description Repository
bundle_spec "ConceptDescriptionRepositoryServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/ConceptDescription-Repository_SSP-001_resolved.yaml" "Concept Description Repository SSP-001"

# AASX File Server
bundle_spec "AasxFileServerServiceSpecification/V3.2_SSP-001.yaml" "$RESOLVED_DIR/AASX-FileServer_SSP-001_resolved.yaml" "AASX File Server SSP-001"

# Part 1 - MetaModel Schemas
bundle_spec "Part1-MetaModel-Schemas/openapi_3.2.yaml" "$RESOLVED_DIR/Part1-MetaModel-Schemas_resolved.yaml" "Part 1 MetaModel"

# Part 2 - API Schemas
bundle_spec "Part2-API-Schemas/openapi.yaml" "$RESOLVED_DIR/Part2-API-Schemas_resolved.yaml" "Part 2 API Schemas"

echo ""
echo "✓ Resolved specifications generated in: $RESOLVED_DIR"
echo ""
echo "Note: Resolved specs have all \$ref references inlined."
echo "They are larger but easier to use with tools that don't support external references."
