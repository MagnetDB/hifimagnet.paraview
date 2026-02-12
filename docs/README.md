# HiFiMagnet Paraview Documentation

This directory contains the Sphinx documentation for the HiFiMagnet Paraview project.

## Building the Documentation

### Install Dependencies

First, install the documentation dependencies:

```bash
# Install with pip
pip install -e ".[docs]"
```

### Build HTML Documentation

```bash
cd docs
make html
```

The built documentation will be in `docs/_build/html/`. Open `docs/_build/html/index.html` in your browser to view it.

### Other Build Formats

```bash
# PDF (requires LaTeX)
make latexpdf

# EPUB
make epub

# Clean build files
make clean
```

## Sphinx Quick Reference

### Updating Documentation

- **conf.py**: Main Sphinx configuration file
- **index.rst**: Main documentation page
- **\*.rst files**: Individual documentation pages in reStructuredText format

### Auto-generating API Documentation

To regenerate API documentation from docstrings:

```bash
cd docs
sphinx-apidoc -o api ../python_hifimagnetParaview --force
```

## GitHub Pages Deployment

This project deploys documentation automatically to GitHub Pages via GitHub Actions.

### Setup GitHub Pages

1. Go to your repository Settings → Pages
2. Under "Build and deployment":
   - Source: Select "GitHub Actions"
3. Push to the `main` branch to trigger deployment
4. Documentation will be available at: `https://magnetdb.github.io/hifimagnet.paraview/`

### Manual Deployment

To manually trigger a documentation build and deployment:

1. Go to the "Actions" tab in your repository
2. Select "Build and Deploy Documentation" workflow
3. Click "Run workflow"

The workflow will:
- Build the Sphinx documentation
- Check for warnings
- Deploy to GitHub Pages (only on pushes to main)
- Upload documentation artifacts for pull requests

### Local Preview

To preview exactly what will be deployed:

```bash
cd docs
make html
python -m http.server -d _build/html 8000
```

Then visit http://localhost:8000

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Sphinx RTD Theme](https://sphinx-rtd-theme.readthedocs.io/)
