# Reference Conversion Documentation

## What Was Done

All OpenAPI YAML specification files have been converted from using external SwaggerHub references to local file references.

### Before
```yaml
$ref: 'https://api.swaggerhub.com/domains/Plattform_i40/Part2-API-Schemas/V3.2.0#/components/parameters/Limit'
```

### After
```yaml
$ref: '../Part2-API-Schemas/openapi.yaml#/components/parameters/Limit'
```

## Why This Was Necessary

The original YAML files referenced schema definitions hosted on SwaggerHub. This approach:
- ❌ Requires internet connection to view docs
- ❌ Doesn't work offline or in restricted networks
- ❌ Depends on external service availability
- ❌ May have latency issues

With local references:
- ✅ Works offline
- ✅ Faster loading (no external HTTP requests)
- ✅ Self-contained repository
- ✅ Works on GitHub Pages immediately

## Files Converted

Total: **36 YAML files** across all specifications:

- Asset Administration Shell Registry Service (5 files)
- Asset Administration Shell Repository Service (6 files)
- Asset Administration Shell Service (2 files)
- Submodel Registry Service (4 files)
- Submodel Repository Service (7 files)
- Submodel Service (3 files)
- Discovery Service (2 files)
- Concept Description Repository (3 files)
- AASX File Server (2 files)
- Entire API Collection (1 file)
- Part2 API Schemas (1 file)

## Backups

All original files were backed up to `docs/.backups/` before conversion.

## Reverting Changes

If you need to revert to the original SwaggerHub references:

```bash
./restore-from-backup.sh
```

This will restore all files from the backups.

## Impact on SwaggerHub Sync

⚠️ **Important**: If you sync these files back to SwaggerHub, the references will be local paths instead of SwaggerHub URLs. 

**Options:**
1. **Keep both versions**: Maintain SwaggerHub with external refs, GitHub with local refs
2. **One-way sync**: Only sync from SwaggerHub → GitHub, convert after each sync
3. **Update SwaggerHub**: Accept local refs in SwaggerHub (they still work there)

## Testing

Test the converted files:

```bash
cd docs
python3 -m http.server 8000
# Visit: http://localhost:8000/
```

Click on any API and verify:
- Swagger UI loads the spec correctly
- All schemas and components are resolved
- No 404 errors in browser console
- All operations show proper request/response models

## Notes

- The Part1-MetaModel-Schemas and Part2-API-Schemas are referenced by all other specs
- Relative paths are calculated based on each file's location
- Both Part1 and Part2 schemas are kept in their original locations
- The conversion script can be run again if new files are added

## Script Files

- `convert-refs-to-local.sh` - Converts SwaggerHub refs to local paths
- `restore-from-backup.sh` - Restores original files from backups

---

**Date Converted**: 2026-04-30  
**Conversion Script**: convert-refs-to-local.sh v1.0
