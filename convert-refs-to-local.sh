#!/bin/bash

# Script to convert SwaggerHub external references to local file references
# This allows the OpenAPI specs to work when deployed on GitHub Pages

echo "=========================================="
echo "  Converting SwaggerHub refs to local"
echo "=========================================="
echo ""

# Backup directory
BACKUP_DIR="docs/.backups"
mkdir -p "$BACKUP_DIR"

# Counter for processed files
PROCESSED=0

# Function to calculate relative path (works on macOS and Linux)
get_relative_path() {
    local target=$1
    local base=$2
    python3 -c "import os.path; print(os.path.relpath('$target', '$base'))"
}

# Find all YAML files (excluding docs folder and backups)
find . -name "*.yaml" -o -name "*.yml" | grep -v "./docs/" | grep -v "./.git/" | grep -v "./documentation/" | grep -v "./.github/" | while read file; do

    # Skip if file doesn't contain SwaggerHub references
    if ! grep -q "api.swaggerhub.com" "$file"; then
        continue
    fi

    echo "Processing: $file"

    # Create backup
    BACKUP_NAME=$(echo "$file" | sed 's/[\/.]/_/g')
    cp "$file" "$BACKUP_DIR/${BACKUP_NAME}.bak"

    # Get the directory of the current file
    FILE_DIR=$(dirname "$file")

    # Calculate relative paths
    PART1_REL=$(get_relative_path "Part1-MetaModel-Schemas/openapi.yaml" "$FILE_DIR")
    PART2_REL=$(get_relative_path "Part2-API-Schemas/openapi.yaml" "$FILE_DIR")

    echo "  Part1 ref: $PART1_REL"
    echo "  Part2 ref: $PART2_REL"

    # Create temporary file with replacements
    sed \
        -e "s|https://api.swaggerhub.com/domains/Plattform_i40/Part1-MetaModel-Schemas/V3.2.0#|$PART1_REL#|g" \
        -e "s|https://api.swaggerhub.com/domains/Plattform_i40/Part2-API-Schemas/V3.2.0#|$PART2_REL#|g" \
        "$file" > "$file.tmp"

    # Replace original with modified
    mv "$file.tmp" "$file"

    echo "  ✓ Converted SwaggerHub refs to local paths"
    PROCESSED=$((PROCESSED + 1))
    echo ""

done

echo "=========================================="
echo "  ✅ Conversion Complete!"
echo "=========================================="
echo ""
echo "Files processed: $PROCESSED"
echo "Backups saved to: $BACKUP_DIR"
echo ""
echo "Next steps:"
echo "  1. Test locally:"
echo "     cd docs && python3 -m http.server 8000"
echo "     Visit: http://localhost:8000/"
echo ""
echo "  2. If everything works, commit the changes"
echo ""
echo "To revert all changes:"
echo "  ./restore-from-backup.sh"
echo ""
