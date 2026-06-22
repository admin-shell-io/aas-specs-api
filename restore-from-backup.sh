#!/bin/bash

# Script to restore YAML files from backups

BACKUP_DIR="docs/.backups"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ No backup directory found at $BACKUP_DIR"
    exit 1
fi

echo "=========================================="
echo "  Restoring from backups"
echo "=========================================="
echo ""

# Count backups
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.bak 2>/dev/null | wc -l)

if [ "$BACKUP_COUNT" -eq 0 ]; then
    echo "❌ No backup files found"
    exit 1
fi

echo "Found $BACKUP_COUNT backup files"
echo ""

# Restore each backup
for backup in "$BACKUP_DIR"/*.bak; do
    # Get original filename from backup name
    basename=$(basename "$backup" .bak)

    # Try to find the original file
    original=$(find . -name "*.yaml" -o -name "*.yml" | grep -v "./docs/" | grep -v "./.git/" | while read file; do
        backup_name=$(echo "$file" | sed 's/[\/.]/_/g')
        if [ "$backup_name" = "$basename" ]; then
            echo "$file"
            break
        fi
    done)

    if [ -n "$original" ]; then
        cp "$backup" "$original"
        echo "✓ Restored: $original"
    else
        echo "⚠ Could not find original file for: $basename"
    fi
done

echo ""
echo "=========================================="
echo "  ✅ Restore Complete!"
echo "=========================================="
echo ""
