#!/usr/bin/env bash
# bundle-specs.sh — Bundle all SSP YAMLs using Redocly CLI.
#
# Produces a bundled-<original>.yaml alongside each source V<ver>_SSP-*.yaml so
# that Swagger UI can resolve all $ref pointers within a single document and
# eliminate cross-document resolver errors.
#
# Version-agnostic: picks up any V<ver>_SSP-<n>.yaml source file in the 9
# service directories (v3.2, v3.3, v4.0, etc.). When new versions land on the
# github-pages branch, running this script bundles them automatically with
# no code changes required.
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

# All 9 service specification directories that may contain SSP YAMLs.
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

  # Find all V<ver>_SSP-*.yaml source files in this directory (not bundled- ones).
  # Pattern matches V3.2_SSP-001.yaml, V3.3_SSP-001.yaml, V4.0_SSP-001.yaml, etc.
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
  done < <(find "${abs_dir}" -maxdepth 1 -name "V*_SSP-*.yaml" -not -name "bundled-*" -print0 | sort -z)
done

echo ""
echo "Done. Bundled ${bundled}/${total} SSP files."
