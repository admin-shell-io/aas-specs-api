// Shared version configuration for index.html, swagger-ui.html and redoc.html.
//
// Released versions are discovered at runtime from the repository's git tags
// (vMAJOR.MINOR or vMAJOR.MINOR.PATCH), so publishing a new release tag makes
// it selectable without touching the docs. For a tag that is not listed in
// KNOWN_VERSIONS below, the number of SSP files per service is read from the
// tag's file tree.
//
// KNOWN_VERSIONS doubles as the fallback when the GitHub API is unreachable or
// rate-limited (60 unauthenticated requests per hour per IP), so the site keeps
// working offline from the API. Results are cached in localStorage for an hour.
(function () {
    const REPO = 'admin-shell-io/aas-specs-api';
    const GITHUB_RAW_BASE = `https://raw.githubusercontent.com/${REPO}`;
    const GITHUB_API_BASE = `https://api.github.com/repos/${REPO}`;

    // Version whose spec files the static links in index.html point to.
    const DEFAULT_VERSION = 'v3.2.0';

    // Oldest major version the viewers support (older tags use another layout).
    const MIN_MAJOR = 3;

    const CACHE_KEY = 'aas-specs-api:versions:v1';
    const CACHE_TTL_MS = 60 * 60 * 1000;

    const SERVICES = [
        'AssetAdministrationShellRegistryServiceSpecification',
        'AssetAdministrationShellRepositoryServiceSpecification',
        'AssetAdministrationShellServiceSpecification',
        'SubmodelRegistryServiceSpecification',
        'SubmodelRepositoryServiceSpecification',
        'SubmodelServiceSpecification',
        'DiscoveryServiceSpecification',
        'ConceptDescriptionRepositoryServiceSpecification',
        'AasxFileServerServiceSpecification'
    ];

    // Number of SSP files per service (0 = service not part of the release)
    const SSP_V3_0 = {
        'AssetAdministrationShellRegistryServiceSpecification': 2,
        'AssetAdministrationShellRepositoryServiceSpecification': 2,
        'AssetAdministrationShellServiceSpecification': 2,
        'SubmodelRegistryServiceSpecification': 0,
        'SubmodelRepositoryServiceSpecification': 2,
        'SubmodelServiceSpecification': 3,
        'DiscoveryServiceSpecification': 1,
        'ConceptDescriptionRepositoryServiceSpecification': 0,
        'AasxFileServerServiceSpecification': 1
    };
    const SSP_V3_0_4 = {
        'AssetAdministrationShellRegistryServiceSpecification': 2,
        'AssetAdministrationShellRepositoryServiceSpecification': 2,
        'AssetAdministrationShellServiceSpecification': 2,
        'SubmodelRegistryServiceSpecification': 2,
        'SubmodelRepositoryServiceSpecification': 4,
        'SubmodelServiceSpecification': 3,
        'DiscoveryServiceSpecification': 1,
        'ConceptDescriptionRepositoryServiceSpecification': 0,
        'AasxFileServerServiceSpecification': 1
    };
    const SSP_V3_1 = {
        'AssetAdministrationShellRegistryServiceSpecification': 5,
        'AssetAdministrationShellRepositoryServiceSpecification': 3,
        'AssetAdministrationShellServiceSpecification': 2,
        'SubmodelRegistryServiceSpecification': 4,
        'SubmodelRepositoryServiceSpecification': 5,
        'SubmodelServiceSpecification': 3,
        'DiscoveryServiceSpecification': 2,
        'ConceptDescriptionRepositoryServiceSpecification': 2,
        'AasxFileServerServiceSpecification': 1
    };
    const SSP_V3_2 = {
        'AssetAdministrationShellRegistryServiceSpecification': 5,
        'AssetAdministrationShellRepositoryServiceSpecification': 6,
        'AssetAdministrationShellServiceSpecification': 2,
        'SubmodelRegistryServiceSpecification': 4,
        'SubmodelRepositoryServiceSpecification': 7,
        'SubmodelServiceSpecification': 3,
        'DiscoveryServiceSpecification': 2,
        'ConceptDescriptionRepositoryServiceSpecification': 3,
        'AasxFileServerServiceSpecification': 2
    };

    // Tag name -> SSP counts for releases verified by hand
    const KNOWN_VERSIONS = {
        'v3.0': SSP_V3_0,
        'v3.0.1': SSP_V3_0,
        'v3.0.2': SSP_V3_0,
        'v3.0.3': SSP_V3_0,
        'v3.0.4': SSP_V3_0_4,
        'v3.1.0': SSP_V3_1,
        'v3.1.1': SSP_V3_1,
        'v3.1.2': SSP_V3_1,
        'v3.1.3': SSP_V3_1,
        'v3.2.0': SSP_V3_2
    };

    const TAG_PATTERN = /^v(\d+)\.(\d+)(?:\.(\d+))?$/;

    // 'v3.0' -> { key: 'v3.0.0', format: '3.0', sortKey: [3, 0, 0] }
    function parseTag(tag) {
        const m = TAG_PATTERN.exec(tag);
        if (!m) return null;
        const parts = [Number(m[1]), Number(m[2]), Number(m[3] || 0)];
        if (parts[0] < MIN_MAJOR) return null;
        return { key: `v${parts.join('.')}`, format: `${parts[0]}.${parts[1]}`, sortKey: parts };
    }

    function compareDesc(a, b) {
        for (let i = 0; i < 3; i++) {
            if (a.sortKey[i] !== b.sortKey[i]) return b.sortKey[i] - a.sortKey[i];
        }
        return 0;
    }

    function readCache() {
        try {
            const cached = JSON.parse(localStorage.getItem(CACHE_KEY));
            if (cached && Date.now() - cached.time < CACHE_TTL_MS) return cached.tags;
        } catch (e) { /* storage unavailable */ }
        return null;
    }

    function writeCache(tags) {
        try {
            localStorage.setItem(CACHE_KEY, JSON.stringify({ time: Date.now(), tags }));
        } catch (e) { /* storage unavailable */ }
    }

    async function fetchJson(url) {
        const response = await fetch(url, { headers: { Accept: 'application/vnd.github+json' } });
        if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
        return response.json();
    }

    // Count V<format>_SSP-<n>.yaml files per service in the tag's file tree
    async function fetchSSPCounts(tag, format) {
        const tree = await fetchJson(`${GITHUB_API_BASE}/git/trees/${encodeURIComponent(tag)}?recursive=1`);
        const counts = {};
        SERVICES.forEach(service => { counts[service] = 0; });
        const pattern = new RegExp(`^([^/]+)/V${format.replace('.', '\\.')}_SSP-(\\d+)\\.yaml$`);
        tree.tree.forEach(entry => {
            const m = pattern.exec(entry.path);
            if (m && m[1] in counts) counts[m[1]] = Math.max(counts[m[1]], Number(m[2]));
        });
        return counts;
    }

    // Resolve {tag: sspCounts} for every release tag, using KNOWN_VERSIONS where possible
    async function discoverTags() {
        const cached = readCache();
        if (cached) return cached;

        const tagList = await fetchJson(`${GITHUB_API_BASE}/tags?per_page=100`);
        const tags = {};
        for (const { name } of tagList) {
            const parsed = parseTag(name);
            if (!parsed) continue;
            if (KNOWN_VERSIONS[name]) {
                tags[name] = KNOWN_VERSIONS[name];
                continue;
            }
            try {
                tags[name] = await fetchSSPCounts(name, parsed.format);
            } catch (e) {
                console.warn(`Could not read SSP files for ${name}, skipping it`, e);
            }
        }
        writeCache(tags);
        return tags;
    }

    let loadPromise = null;

    // Resolves to:
    //   versions:        version keys, newest first (e.g. ['v3.2.0', 'v3.1.3', ...])
    //   latest:          newest version key
    //   versionConfig:   { [version]: { tag, local, format } }
    //   versionSSPLimits:{ [version]: { [serviceFolder]: sspCount } }
    // Never rejects; falls back to KNOWN_VERSIONS if tag discovery fails.
    function load() {
        if (loadPromise) return loadPromise;
        loadPromise = discoverTags()
            .catch(error => {
                console.warn('Could not load release tags from GitHub, using built-in version list', error);
                return {};
            })
            .then(discovered => {
                const tags = Object.assign({}, KNOWN_VERSIONS, discovered);
                const entries = Object.keys(tags)
                    .map(tag => Object.assign({ tag }, parseTag(tag)))
                    .sort(compareDesc);

                const result = { versions: [], latest: null, versionConfig: {}, versionSSPLimits: {} };
                entries.forEach(entry => {
                    if (result.versionConfig[entry.key]) return; // e.g. both v3.0 and v3.0.0 tagged
                    result.versions.push(entry.key);
                    result.versionConfig[entry.key] = { tag: entry.tag, local: false, format: entry.format };
                    result.versionSSPLimits[entry.key] = tags[entry.tag];
                });
                result.latest = result.versions[0];
                return result;
            });
        return loadPromise;
    }

    // Fill a <select> with all versions, marking the newest as "(Latest)"
    function populateVersionSelect(select, data, selected) {
        select.innerHTML = '';
        data.versions.forEach(version => {
            const option = document.createElement('option');
            option.value = version;
            option.textContent = version === data.latest ? `${version} (Latest)` : version;
            select.appendChild(option);
        });
        select.value = selected;
    }

    window.AASVersions = {
        GITHUB_RAW_BASE,
        DEFAULT_VERSION,
        SERVICES,
        load,
        populateVersionSelect
    };
})();
