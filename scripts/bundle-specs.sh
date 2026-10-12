#!/usr/bin/env bash
# bundle-specs.sh — Bundle all v3.2 SSP YAMLs using Redocly CLI.
#
# Produces a bundled-<original>.yaml alongside each source V3.2_SSP-*.yaml so
# that Swagger UI can resolve all $ref pointers within a single document and
# eliminate cross-document resolver errors.
#
# Usage:
#   npm run bundle        (via package.json)
#   bash scripts/bundle-specs.sh
#
# Requirements: @redocly/cli must be installed (npm install).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REDOCLY="${REPO_ROOT}/node_modules/.bin/redocly"

if [[ ! -x "${REDOCLY}" ]]; then
  echo "ERROR: redocly CLI not found at ${REDOCLY}" >&2
  echo "       Run 'npm install' first." >&2
  exit 1
fi

# All 9 service specification directories that have v3.2 SSP YAMLs
SERVICE_DIRS=(
  AasxFileServerServiceSpecification
  AssetAdministrationShellRegistryServiceSpecification
  AssetAdministrationShellRepositoryServiceSpecification
  AssetAdministrationShellServiceSpecification
  ConceptDescriptionRepositoryServiceSpecification
  DiscoveryServiceSpecification
  SubmodelRegistryServiceSpecification
  SubmodelRepositoryServiceSpecification
  SubmodelServiceSpecification
)

total=0
bundled=0

for dir in "${SERVICE_DIRS[@]}"; do
  abs_dir="${REPO_ROOT}/${dir}"
  if [[ ! -d "${abs_dir}" ]]; then
    echo "WARN: Directory not found, skipping: ${dir}" >&2
    continue
  fi

  # Find all V3.2_SSP-*.yaml source files in this directory (not bundled- ones)
  while IFS= read -r -d '' src; do
    total=$((total + 1))
    filename="$(basename "${src}")"
    out_file="${abs_dir}/bundled-${filename}"

    echo "Bundling ${dir}/${filename} → bundled-${filename}"
    # --force: allow bundling despite pre-existing broken $refs in source files
    # (e.g. Part2-API-Schemas references RecentChangeType which is missing in Part1).
    # These broken refs existed before this change; --force ensures they do not
    # block generation of the bundled files that fix the cross-document resolver errors.
    "${REDOCLY}" bundle "${src}" -o "${out_file}" --force 2>&1

    bundled=$((bundled + 1))
  done < <(find "${abs_dir}" -maxdepth 1 -name "V3.2_SSP-*.yaml" -not -name "bundled-*" -print0 | sort -z)
done

echo ""
echo "Done. Bundled ${bundled}/${total} SSP files."
