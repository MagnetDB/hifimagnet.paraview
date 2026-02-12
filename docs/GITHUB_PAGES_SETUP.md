# GitHub Pages Setup Guide

This guide will help you enable GitHub Pages deployment for the Sphinx documentation.

## Quick Setup (3 Steps)

### Step 1: Enable GitHub Pages in Repository Settings

1. Go to your repository on GitHub: https://github.com/MagnetDB/hifimagnet.paraview
2. Click on **Settings** (top right)
3. In the left sidebar, click **Pages**
4. Under **Build and deployment**:
   - **Source**: Select **GitHub Actions** from the dropdown
5. Save the settings

That's it! No other configuration needed.

### Step 2: Push to Main Branch

The documentation will automatically build and deploy when you push to the `main` branch:

```bash
git add .
git commit -m "Setup Sphinx documentation with GitHub Pages"
git push origin main
```

### Step 3: Access Your Documentation

After the GitHub Action completes (usually 2-3 minutes):

**Your documentation will be available at:**
- https://magnetdb.github.io/hifimagnet.paraview/

## Monitoring Deployment

### Check Build Status

1. Go to the **Actions** tab in your repository
2. Look for the "Build and Deploy Documentation" workflow
3. Click on a run to see detailed logs

### Build Triggers

Documentation builds automatically when:
- Code is pushed to the `main` branch
- A pull request is created (builds but doesn't deploy)
- Manual trigger from the Actions tab

## Manual Deployment

To manually trigger a documentation build:

1. Go to the **Actions** tab
2. Select **Build and Deploy Documentation**
3. Click **Run workflow** button
4. Select the branch and confirm

## Troubleshooting

### Documentation Not Showing Up

1. **Check GitHub Actions**: Make sure the workflow completed successfully
2. **Check Pages Settings**: Verify Source is set to "GitHub Actions"
3. **Wait**: First deployment can take 5-10 minutes

### 404 Error

- Ensure the workflow completed successfully
- Check that `_build/html/index.html` exists in build logs
- Clear your browser cache

### Build Failures

Check the Actions logs for errors:
- Python dependency issues
- Sphinx build warnings/errors
- Missing files

Common fixes:
```bash
# Test locally first
cd docs
make clean
make html

# If it works locally, the Action should work too
```

## Features

### What's Included

✅ **Automatic Deployment**: Pushes to `main` trigger builds and deployment
✅ **Pull Request Previews**: PRs build docs as artifacts (downloadable from Actions)
✅ **Manual Triggers**: Deploy on-demand from Actions tab
✅ **Build Artifacts**: Documentation available for download from any build
✅ **Proper Caching**: Dependencies cached for faster builds

### The Workflow Does:

1. Checks out code
2. Sets up Python 3.10
3. Installs package with docs dependencies
4. Builds Sphinx documentation
5. Adds `.nojekyll` file (fixes Jekyll processing)
6. Uploads build artifacts
7. Deploys to GitHub Pages (main branch only)

## Customization

### Change Python Version

Edit `.github/workflows/docs.yml`:

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Change version here
```

### Add Build Checks

To fail builds on warnings, modify the workflow:

```yaml
- name: Build documentation with strict mode
  run: |
    cd docs
    make html SPHINXOPTS="-W --keep-going"
```

### Custom Domain

To use a custom domain:

1. Add a `CNAME` file to `docs/_static/`:
   ```
   docs.yourdomain.com
   ```

2. Configure DNS with your domain provider

3. Update workflow to copy CNAME:
   ```yaml
   - name: Add CNAME
     run: cp docs/_static/CNAME docs/_build/html/
   ```

## Next Steps

After setup:

1. ✅ Review the deployed documentation
2. 📝 Update documentation content as needed
3. 🎨 Customize theme and styling in `docs/conf.py`
4. 📊 Add more documentation pages
5. 🔗 Update README badges with documentation link

## Documentation Badge

Add this badge to your README.md:

```markdown
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://magnetdb.github.io/hifimagnet.paraview/)
```

Result:
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://magnetdb.github.io/hifimagnet.paraview/)

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions for Pages](https://github.com/actions/deploy-pages)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
