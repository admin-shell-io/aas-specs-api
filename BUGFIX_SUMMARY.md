# GitHub Pages Swagger UI Bug Fix Summary

## Problem

When visiting the GitHub Pages site at:
```
https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html
```

And selecting version **v3.0.0** with service **AAS Repository Service - SSP-006**, the page displayed an error:

> ⚠️ Service Specification Not Available
> 
> This Service Specification is not part of the currently selected release version. Try a later version.

## Root Cause

The Swagger UI dropdown was populated based on the **maximum** SSP count defined in `serviceSSPRanges`, which shows the total number of SSP files in the latest version (v3.2.0). However, older versions have fewer SSP files:

- **v3.0.x**: AAS Repository Service only has SSP-001 and SSP-002
- **v3.1.x**: AAS Repository Service has SSP-001, SSP-002, and SSP-003
- **v3.2.0**: AAS Repository Service has SSP-001 through SSP-006

The dropdown was showing all 6 SSP options regardless of which version was selected, leading to broken links for non-existent files.

## Solution

Added a comprehensive version-specific mapping called `versionSSPLimits` that defines exactly which SSP files exist in each version for each service.

### Changes Made to `docs/swagger-ui.html`:

1. **Added `versionSSPLimits` object** (lines 149-257):
   - Complete mapping of all services across versions v3.0.0 through v3.1.2
   - Marks services that don't exist in certain versions with count = 0
   - Example: `ConceptDescriptionRepositoryServiceSpecification` doesn't exist in v3.0.x

2. **Updated `populateSpecDropdown` function** (lines 272-291):
   - Now checks `versionSSPLimits` before generating dropdown options
   - Uses `effectiveCount` based on version-specific limits instead of maximum count
   - Displays "Not available in <version>" for services that don't exist in selected version
   - Only shows SSP files that actually exist in the selected version

## Version-Specific SSP Counts

### AAS Repository Service
- v3.0.x: 2 SSP files (001-002)
- v3.1.x: 3 SSP files (001-003)
- v3.2.x: 6 SSP files (001-006)

### Submodel Repository Service
- v3.0.0-v3.0.3: 2 SSP files (001-002)
- v3.0.4: 4 SSP files (001-004)
- v3.1.x: 5 SSP files (001-005)
- v3.2.x: 7 SSP files (001-007)

### Registry Services
- v3.0.x: 2 SSP files (AAS Registry), 0 files (Submodel Registry - didn't exist)
- v3.1.x: 5 SSP files (AAS Registry), 4 files (Submodel Registry)
- v3.2.x: 5 SSP files (AAS Registry), 4 files (Submodel Registry)

### Concept Description Repository
- v3.0.x: 0 files (service didn't exist)
- v3.1.x: 2 SSP files (001-002)
- v3.2.x: 3 SSP files (001-003)

## Testing

The fix was verified by:
1. Checking actual file existence in git tags using `git ls-tree`
2. Testing the logic with a standalone JavaScript test
3. Confirming dropdown now only shows SSP files that exist in selected version

## Commit

- **Branch**: `github-pages`
- **Commit**: `f80b741`
- **Message**: "fix(swagger-ui): add version-specific SSP availability mapping"

## Deployment

The fix is committed to the `github-pages` branch. GitHub Pages will automatically deploy the updated site within a few minutes.

To verify the fix after deployment:
1. Visit https://industrialdigitaltwin.io/aas-specs-api/docs/swagger-ui.html
2. Select version v3.0.0
3. Select AAS Repository Service from a card on the home page
4. The dropdown should now only show SSP-001 and SSP-002 (not SSP-006)
5. Both options should load successfully without errors
