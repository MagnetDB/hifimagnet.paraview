# Debian Packaging for python-hifimagnetparaview

This directory contains the Debian packaging files for building the `python3-hifimagnetparaview` package for Debian Trixie.

## Package Information

- **Source Package**: python-hifimagnetparaview
- **Binary Package**: python3-hifimagnetparaview
- **Target Distribution**: Debian Trixie
- **Debian Policy Version**: 4.6.2
- **Debhelper Compatibility**: 13

## Building the Package

### Prerequisites

Install the required build dependencies:

```bash
sudo apt-get install debhelper-compat dh-python pybuild-plugin-pyproject \
                     python3-all python3-setuptools python3-wheel devscripts
```

### Build Process

1. **Clean build**:
   ```bash
   dpkg-buildpackage -us -uc -b
   ```

2. **Build with signing** (requires GPG key):
   ```bash
   dpkg-buildpackage -b
   ```

3. **Build source package**:
   ```bash
   dpkg-buildpackage -S
   ```

### Using pbuilder/cowbuilder (Recommended)

For a clean build environment:

```bash
# Create base trixie environment (first time only)
sudo cowbuilder --create --distribution trixie --basepath /var/cache/pbuilder/trixie-amd64.cow

# Build the package
pdebuild --pbuilder cowbuilder -- --basepath /var/cache/pbuilder/trixie-amd64.cow
```

## Package Contents

The package includes:
- Python module: `python_hifimagnetParaview`
- Command-line tool: `hifimagnet-paraview`
- JSON configuration files
- ParaView plugins (XML files)
- Documentation (README.md, HISTORY.rst)

## Files Overview

- **changelog**: Package version history and changes
- **control**: Package metadata, dependencies, and descriptions
- **copyright**: License and copyright information
- **rules**: Build instructions (uses dh with pybuild)
- **compat**: Debhelper compatibility level
- **source/format**: Source package format (3.0 quilt)
- **watch**: Upstream release monitoring
- **install**: Additional files to install
- **docs**: Documentation files to include

## Lintian Checks

After building, check the package for policy compliance:

```bash
lintian ../python3-hifimagnetparaview_*.deb
```

## Installing the Built Package

```bash
sudo dpkg -i ../python3-hifimagnetparaview_*.deb
sudo apt-get install -f  # Fix any missing dependencies
```

## Updating the Package

When updating to a new upstream version:

1. Update `debian/changelog`:
   ```bash
   dch -v 0.2.0-1 "New upstream release"
   ```

2. Review and update dependencies in `debian/control` if needed

3. Rebuild the package

## Notes

- The package uses `pybuild` for building Python packages
- Compatible with Python 3.10, 3.11, and 3.12
- Requires ParaView to be installed for full functionality
- Some dependencies may need to be packaged separately if not available in Debian Trixie
