# ✅ Deployment Checklist

Use this checklist to deploy your AAS API documentation to GitHub Pages.

## Pre-Deployment

- [ ] All YAML files are in the repository
- [ ] `docs/` folder contains all HTML files
- [ ] No build errors in the repository
- [ ] Test locally: From repository root run `python3 -m http.server 8000`, then visit `http://localhost:8000/docs/`

## GitHub Pages Setup

- [ ] Navigate to repository Settings → Pages
- [ ] Select Source: Branch `main`, Folder `/docs`
- [ ] Click Save
- [ ] Wait 1-2 minutes for initial deployment

## Post-Deployment Testing

- [ ] Visit the GitHub Pages URL
- [ ] Test landing page loads correctly
- [ ] Click on "Swagger UI" button - verify it loads an API spec
- [ ] Click on "Redoc" button - verify it loads an API spec
- [ ] Test the search bar on the landing page
- [ ] Test dropdown selector in Swagger UI and Redoc
- [ ] Test on mobile device or responsive mode
- [ ] Verify download links work for YAML files

## Update Documentation

- [ ] Update README.md with your actual GitHub Pages URL
- [ ] Update docs/index.html if needed (organization info, colors)
- [ ] Commit and push changes

## Optional Enhancements

- [ ] Add custom domain (create `docs/CNAME` file)
- [ ] Add Google Analytics tracking
- [ ] Customize colors and branding
- [ ] Add organization logo to `docs/assets/images/`
- [ ] Set up automatic deployment with GitHub Actions

## Troubleshooting

If something doesn't work:

1. **Check GitHub Actions tab** - look for deployment status
2. **Clear browser cache** - Hard refresh with Ctrl+Shift+R (Cmd+Shift+R on Mac)
3. **Check browser console** - Look for any JavaScript errors
4. **Verify file paths** - YAML references should be relative (`../Folder/file.yaml`)
5. **Wait longer** - Initial deployment can take 2-5 minutes

## Share Your Documentation

Once deployed, share with:
- Development team
- API consumers
- Documentation site
- Social media

Example announcement:
```
📚 Our AAS API documentation is now live!

Explore interactive API docs with Swagger UI and Redoc:
https://your-username.github.io/aas-specs-api/

Features:
✅ Interactive API testing
✅ Beautiful documentation
✅ All 12 API specifications
✅ Mobile-friendly
```

## Maintenance

Regular maintenance tasks:
- [ ] Update when new API versions are released
- [ ] Monitor GitHub Pages build status
- [ ] Review and respond to user feedback
- [ ] Update links if repository structure changes

## Support

Need help?
- See [docs/SETUP.md](./SETUP.md) for detailed instructions
- See [docs/README.md](./README.md) for technical details
- Open an issue in the repository
- Check GitHub Pages documentation

---

**Last Updated:** 2025-04-29
**Status:** Ready for deployment ✅
