# Version Switching Feature

## Overview

The documentation site now supports viewing multiple versions of the AAS API specifications (v3.0.x, v3.1.x, v3.2.x) without duplicating files on the GitHub Pages branch.

## How It Works

### Dynamic Loading (Option D Implementation)

1. **Current version (v3.2.0)**: Loaded from local files in the `docs/` directory
2. **Previous versions (v3.0.x, v3.1.x)**: Loaded directly from GitHub raw URLs pointing to git tags

### Version Selector

Located at the top of the index page, the version selector allows users to switch between:
- v3.2.0 (Latest) - local files
- v3.1.2, v3.1.1, v3.1.0 - from git tags
- v3.0.4, v3.0.3, v3.0.2, v3.0.1, v3.0.0 - from git tags

### URL Structure

When a user selects an older version, the JavaScript dynamically updates all links to point to:

```
https://raw.githubusercontent.com/admin-shell-io/aas-specs-api/{TAG}/{PATH}
```

For example:
- **v3.2.0 (local)**: `../AssetAdministrationShellRegistryServiceSpecification/V3.2_SSP-001.yaml`
- **v3.1.2 (remote)**: `https://raw.githubusercontent.com/admin-shell-io/aas-specs-api/v3.1.2/AssetAdministrationShellRegistryServiceSpecification/V3.1_SSP-001.yaml`

### Version Number Mapping

The system automatically converts version numbers in file paths:
- `V3.2` → `V3.1` or `V3.0` based on selected version
- `openapi_3.2.yaml` → `openapi.yaml` for Part1/Part2 schemas

### Supported Pages

All three viewer pages support version switching:
1. **index.html** - Main documentation page with version selector
2. **swagger-ui.html** - Receives version via URL parameter
3. **redoc.html** - Receives version via URL parameter

### URL Parameters

The version is preserved in the URL:
```
https://yourdomain.com/docs/?version=v3.1.2
https://yourdomain.com/docs/swagger-ui.html?url=...&version=v3.1.2
```

## Benefits

✅ **No file duplication** - Only v3.2.0 files are stored on github-pages branch
✅ **Zero maintenance** - Old versions are served from existing git tags
✅ **Instant availability** - New versions can be added by just updating the dropdown
✅ **Bookmarkable** - Users can share links to specific versions
✅ **Fast loading** - GitHub's CDN serves the raw files efficiently

## Adding New Versions

To add a new version (e.g., v3.3.0):

1. **Update index.html** - Add new option to version selector:
   ```javascript
   const versionConfig = {
       'v3.3.0': { tag: 'github-pages', local: true, format: '3.3' },
       'v3.2.0': { tag: 'v3.2.0', local: false, format: '3.2' }, // Move to remote
       // ... rest
   };
   ```

2. **Tag the release** in git:
   ```bash
   git tag v3.2.0
   git push origin v3.2.0
   ```

3. **Update local files** to v3.3.0 specs on github-pages branch

That's it! The old v3.2.0 will automatically be served from the git tag.

## Limitations

- **Internet required**: Users need an internet connection to view old versions (loaded from GitHub)
- **GitHub availability**: Dependent on GitHub being accessible
- **CORS**: GitHub raw URLs support CORS, so this works in browsers
- **Version format consistency**: Assumes consistent file naming across versions (V3.0, V3.1, V3.2)

## Fallback

If GitHub raw URLs are blocked or unavailable, the system will gracefully fail and users can:
1. Clone the repository at the specific tag
2. Use the local file server
3. Download the YAML files directly from GitHub releases
