# Quick Start Guide for Sphinx Documentation

## Overview

This project uses [Sphinx](https://www.sphinx-doc.org/) for documentation. The documentation is written in reStructuredText (`.rst`) format and can be built into various formats including HTML, PDF, and EPUB.

## Quick Build

```bash
# From the project root
cd docs
make html

# View the documentation
xdg-open _build/html/index.html  # Linux
open _build/html/index.html      # macOS
start _build/html/index.html     # Windows
```

## Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation page
├── installation.rst     # Installation guide
├── usage.rst            # Usage guide
├── cli.rst              # CLI reference
├── examples.rst         # Examples
├── modules.rst          # Module overview
├── api.rst              # API reference
├── development.rst      # Development guide
├── Makefile             # Build script (Unix)
├── make.bat             # Build script (Windows)
└── README.md            # This file
```

## Common Tasks

### Clean Build

Remove all built files:

```bash
make clean
```

### Build Different Formats

```bash
# HTML (default)
make html

# PDF (requires LaTeX)
make latexpdf

# EPUB
make epub

# Single HTML file
make singlehtml
```

### Auto-generate API Documentation

To regenerate API docs from Python docstrings:

```bash
sphinx-apidoc -o api ../python_hifimagnetParaview --force
```

Then rebuild:

```bash
make html
```

## Writing Documentation

### reStructuredText Basics

**Headers:**
```rst
Chapter Title
=============

Section Title
-------------

Subsection Title
~~~~~~~~~~~~~~~~
```

**Code Blocks:**
```rst
.. code-block:: python

   def example():
       return "Hello"
```

**Links:**
```rst
`Link text <https://example.com>`_
```

**Internal References:**
```rst
See :ref:`section-label` for details.
```

### Documenting Python Code

Use docstrings in your Python code:

```python
def process_data(input_file: str, output_format: str = "csv") -> None:
    """Process simulation data and export results.
    
    Args:
        input_file: Path to the input case file
        output_format: Output format (csv, json, or xml)
    
    Returns:
        None
        
    Raises:
        ValueError: If output_format is not supported
        FileNotFoundError: If input_file doesn't exist
    """
    pass
```

Sphinx will automatically extract these docstrings when you use the `automodule` directive.

## Continuous Documentation

### Watch for Changes (Linux/macOS)

Install sphinx-autobuild:

```bash
pip install sphinx-autobuild
```

Run the auto-build server:

```bash
sphinx-autobuild docs docs/_build/html
```

This will:
- Watch for changes in the `docs/` directory
- Automatically rebuild when files change
- Serve the docs at http://127.0.0.1:8000

## GitHub Pages Deployment

This project automatically deploys documentation to GitHub Pages via GitHub Actions.

### Initial Setup

1. Go to repository Settings → Pages
2. Under "Build and deployment", set Source to "GitHub Actions"
3. Push to `main` branch to trigger automatic deployment

### View Published Docs

Once deployed, documentation is available at:
- `https://magnetdb.github.io/hifimagnet.paraview/`

### Manual Deployment

Trigger a manual build from the Actions tab:
1. Go to "Actions" → "Build and Deploy Documentation"
2. Click "Run workflow"

### Local Preview

Preview what will be deployed:

```bash
cd docs
make html
python -m http.server -d _build/html 8000
# Visit http://localhost:8000
```

## Troubleshooting

### "Module not found" errors

Make sure the package is installed:

```bash
pip install -e .
```

### Import errors for Paraview

The documentation build doesn't need Paraview installed. API docs will still build from docstrings.

### LaTeX/PDF build errors

Install LaTeX:

```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-extra

# macOS
brew install mactex

# Or use a minimal installation
sudo apt-get install texlive-latex-base texlive-latex-recommended
```

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Sphinx RTD Theme Docs](https://sphinx-rtd-theme.readthedocs.io/)
- [Napoleon Extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) (for Google/NumPy docstrings)
