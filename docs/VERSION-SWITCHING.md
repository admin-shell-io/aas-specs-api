# Version Switching Feature

## Overview

The documentation site now supports viewing multiple versions of the AAS API specifications (v3.0.x, v3.1.x, v3.2.x) without duplicating files on the GitHub Pages branch.

## How It Works

### Dynamic Loading (Option D Implementation)

1. **Current version (v3.2.0)**: Loaded from local files in the `docs/` directory
2. **Previous versions (v3.0.x, v3.1.x)**: Loaded directly from GitHub raw URLs pointing to git tags

### Version Selector

Located at the top of the index page, the version selector lists every release tag of the repository
(`vMAJOR.MINOR` or `vMAJOR.MINOR.PATCH`, from v3.0 onwards). The newest one is marked "(Latest)".

The list is built at runtime by `docs/assets/js/versions.js`, which is shared by all three pages:

1. Fetches the tags from the GitHub API (`/repos/admin-shell-io/aas-specs-api/tags`)
2. Uses the SSP counts from its built-in `KNOWN_VERSIONS` table for known tags
3. For any other tag, counts the `V<major.minor>_SSP-<n>.yaml` files per service in that tag's file tree
4. Caches the result in `localStorage` for one hour

If the GitHub API is unreachable or rate-limited (60 unauthenticated requests per hour per IP),
the pages fall back to the built-in `KNOWN_VERSIONS` table.

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
✅ **Instant availability** - New release tags appear in the dropdown automatically
✅ **Bookmarkable** - Users can share links to specific versions
✅ **Fast loading** - GitHub's CDN serves the raw files efficiently

## Adding New Versions

Push a release tag (e.g. `v3.2.1`). It shows up in the version selector automatically,
no change to the github-pages branch is needed.

Optionally add the tag to `KNOWN_VERSIONS` in `docs/assets/js/versions.js` so it is also
available when the GitHub API cannot be reached.

When a new major/minor version (e.g. v3.3) replaces the spec files on the github-pages
branch, update `DEFAULT_VERSION` in `versions.js` and the default `version`/`V3.2` paths
in `index.html`, `swagger-ui.html` and `redoc.html`.

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
