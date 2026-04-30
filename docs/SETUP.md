# GitHub Pages Setup Guide for AAS API Documentation

This guide will help you deploy the AAS API documentation to GitHub Pages.

## 🚀 Quick Setup (5 minutes)

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** (top menu)
3. Scroll down to **Pages** section (left sidebar)
4. Under **Source**:
   - Select branch: `main` (or your current branch)
   - Select folder: `/docs`
5. Click **Save**

### Step 2: Wait for Deployment

GitHub will automatically build and deploy your site. This takes 1-2 minutes.

You'll see a message like:
```
Your site is published at https://[username].github.io/aas-specs-api/
```

### Step 3: Visit Your Site

Click on the URL provided or visit:
```
https://[username].github.io/aas-specs-api/
```

## ✅ What's Included

Your documentation site includes:

- **Landing Page** (`index.html`) - Browse all API specifications
- **Swagger UI** (`swagger-ui.html`) - Interactive API testing
- **Redoc** (`redoc.html`) - Beautiful documentation viewer
- **404 Page** - Custom error page
- **All YAML files** - Referenced from parent directories

## 📁 File Structure

```
docs/
├── index.html           # Landing page (REQUIRED)
├── swagger-ui.html      # Swagger UI viewer
├── redoc.html          # Redoc viewer
├── 404.html            # Custom 404 page
├── README.md           # Documentation
├── _config.yml         # GitHub Pages config
└── .nojekyll           # Disable Jekyll processing
```

## 🔧 Customization

### Change the Theme Colors

Edit the CSS in `index.html`, `swagger-ui.html`, or `redoc.html`:

```css
/* Current gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Add Your Logo

1. Add your logo image to `docs/assets/images/logo.png`
2. Edit the header in each HTML file:

```html
<div class="custom-header">
    <img src="assets/images/logo.png" alt="Logo" height="40">
    <h1>Your Title</h1>
</div>
```

### Update Organization Info

Edit the footer section in `index.html`:

```html
<div class="footer">
    <p>&copy; 2025 Your Organization</p>
    <p>Your custom links here</p>
</div>
```

## 🌐 Custom Domain (Optional)

To use a custom domain like `docs.yourdomain.com`:

1. Add a file named `CNAME` to the `docs/` folder with your domain:
   ```
   docs.yourdomain.com
   ```

2. Configure your DNS with your domain provider:
   - Add a CNAME record pointing to `[username].github.io`

3. In GitHub Settings → Pages, enter your custom domain

## 🧪 Local Testing

**⚠️ IMPORTANT:** You MUST serve from the **repository root** (not from inside `docs/`) for the OpenAPI specifications to work correctly.

### Why Repository Root?

The YAML files contain `$ref` references like:
```yaml
$ref: '../Part2-API-Schemas/openapi.yaml#/components/...'
```

These references need access to folders outside of `docs/`. When you serve from the repository root, these paths resolve correctly.

### Start the Server

```bash
# Make sure you're in the repository root (not in docs/)
python3 -m http.server 8000
# Visit: http://localhost:8000/docs/
```

### Other HTTP Servers

```bash
# Node.js
npx http-server -p 8000
# Visit: http://localhost:8000/docs/

# PHP
php -S localhost:8000
# Visit: http://localhost:8000/docs/
```

### Helper Script

Use the provided helper script (already in repository root):

```bash
./start-docs-server.sh
```

This automatically starts from the correct location.

## 🔄 Updating Documentation

### Automatic Updates

The docs site automatically references YAML files from parent directories. When you:

1. Update any YAML file in the repo
2. Commit and push to GitHub
3. The docs site will reflect changes immediately (no rebuild needed!)

### Adding New API Specifications

To add a new API spec to the landing page:

1. Open `docs/index.html`
2. Find the `<div class="api-grid">` section
3. Copy an existing card and modify:

```html
<div class="api-card" data-search="your api keywords">
    <h3>Your API Name</h3>
    <p class="description">Description of your API</p>
    <div class="specs">
        <span class="spec-badge">V3.2</span>
    </div>
    <div class="actions">
        <a href="swagger-ui.html?url=../YourFolder/spec.yaml" class="btn btn-primary">Swagger UI</a>
        <a href="redoc.html?url=../YourFolder/spec.yaml" class="btn btn-secondary">Redoc</a>
    </div>
</div>
```

4. Add to the dropdown in `swagger-ui.html` and `redoc.html`:

```html
<option value="../YourFolder/spec.yaml">Your API Name</option>
```

## 🐛 Troubleshooting

### Site Not Loading

1. Check GitHub Pages is enabled (Settings → Pages)
2. Verify the branch and folder are correct (`main` branch, `/docs` folder)
3. Wait 1-2 minutes after enabling for initial deployment

### YAML Files Not Loading

1. Verify file paths are correct (relative to `docs/` folder)
2. Check that YAML files exist in parent directories
3. Test locally to see browser console errors

### Styles Not Applying

1. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
2. Check browser console for errors
3. Verify CSS is inline in HTML files

### 404 on Spec URLs

The `url` parameter should be relative to the `docs/` folder:
```
✅ Correct: ?url=../Part1-MetaModel-Schemas/openapi.yaml
❌ Wrong:   ?url=/Part1-MetaModel-Schemas/openapi.yaml
```

## 📊 Analytics (Optional)

To track visitors, add Google Analytics:

1. Get your GA4 Measurement ID
2. Add to `<head>` of each HTML file:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## 🔒 Security

- All content is static (HTML/CSS/JS)
- No server-side processing
- No user data collected
- Served over HTTPS by default

## 📱 Mobile Support

The site is fully responsive and works on:
- iOS (Safari, Chrome)
- Android (Chrome, Firefox)
- Tablets
- Desktop browsers

## 🆘 Need Help?

- GitHub Pages Documentation: https://docs.github.com/en/pages
- Swagger UI: https://swagger.io/tools/swagger-ui/
- Redoc: https://redoc.ly/docs/

## 📝 License

Licensed under CC BY 4.0 - Industrial Digital Twin Association (IDTA)
