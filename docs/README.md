# AAS API Documentation Site

This directory contains the GitHub Pages site for hosting and rendering the Asset Administration Shell (AAS) OpenAPI specifications.

## Files

- **index.html** - Landing page with all API specifications organized by category
- **swagger-ui.html** - Interactive Swagger UI viewer for trying out APIs
- **redoc.html** - Documentation-focused Redoc viewer for reading APIs

## Features

### Landing Page (index.html)
- Categorized list of all API specifications
- Search functionality to find specific APIs
- Direct links to both Swagger UI and Redoc viewers
- Download links for raw YAML files
- Responsive design for mobile and desktop

### Swagger UI (swagger-ui.html)
- Interactive API documentation
- "Try it out" functionality to test endpoints
- Dropdown selector to switch between specifications
- Deep linking support
- Toggle between light/dark themes

### Redoc (redoc.html)
- Beautiful three-column layout
- Optimized for reading and reference
- Print-friendly
- Search within documentation
- Responsive sidebar navigation

## URL Structure

When deployed to GitHub Pages, the URLs will be:

```
https://[username].github.io/aas-specs-api/
https://[username].github.io/aas-specs-api/swagger-ui.html?url=../Entire-API-Collection/V3.2.yaml
https://[username].github.io/aas-specs-api/redoc.html?url=../Part1-MetaModel-Schemas/openapi_3.2.yaml
```

## Setup GitHub Pages

1. Go to repository Settings → Pages
2. Under "Source", select:
   - Branch: `main` (or your preferred branch)
   - Folder: `/docs`
3. Click Save
4. GitHub will provide your site URL (usually `https://[username].github.io/[repo-name]`)

## Local Development

**⚠️ Important:** You MUST serve from the **repository root** for the OpenAPI specs to load correctly.

The YAML files contain references like `../Part2-API-Schemas/openapi.yaml` which need access to the parent directory structure. Serving from `docs/` will cause "Could not resolve reference" errors.

### Correct Way (from repository root)
```bash
# From repository root
python3 -m http.server 8000
# Visit: http://localhost:8000/docs/
```

### Alternative Servers
```bash
# Node.js
npx http-server -p 8000
# Visit: http://localhost:8000/docs/

# PHP  
php -S localhost:8000
# Visit: http://localhost:8000/docs/
```

The JavaScript automatically detects the environment and adjusts the initial spec URLs, but the `$ref` references inside YAML files require proper directory structure access.

## Updating Documentation

The documentation automatically references the YAML files in the parent directories. When you update the YAML files in the repository, the documentation site will reflect those changes immediately - no rebuild required!

## Technologies Used

- **Swagger UI** v5.11.0 - Interactive API documentation
- **Redoc** latest - Beautiful API documentation
- Pure HTML/CSS/JavaScript - No build process required
- CDN-hosted assets - Fast loading, no local dependencies

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

Content licensed under CC BY 4.0 - Industrial Digital Twin Association (IDTA)
