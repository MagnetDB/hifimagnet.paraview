# Test Suite

This directory contains the test suite for hifimagnet.paraview.

## Structure

```
test/
├── conftest.py              # Pytest configuration and fixtures
├── base_test.py             # Shared test helper functions
├── tolerances.py            # Centralized tolerance configuration
├── data.tar.gz              # Test data archive (20MB)
├── test_2D.py              # Tests for 2D geometry
├── test_3D.py              # Tests for 3D geometry
├── test_Axi.py             # Tests for axisymmetric geometry
├── cases/                   # [extracted] Simulation test cases
├── models/                  # [extracted] JSON configs and meshes
└── Pictures/                # [extracted] Reference images
```

## Running Tests

### Prerequisites

Configure Python path to use ParaView's Python bindings:

```bash
export PYTHONPATH=/opt/paraview/lib/python3.10/site-packages/
```

### Local Development

The test data is automatically extracted from `data.tar.gz` on first run:

```bash
pytest
```

Or run specific test modules:

```bash
pytest test/test_2D.py
pytest test/test_3D.py -v
pytest test/test_Axi.py::test_stats
```

### Continuous Integration (CI)

The fixture is optimized for CI environments:

1. **First run**: Extracts data from `data.tar.gz` (one-time cost)
2. **Subsequent runs**: Detects `.data_extracted` marker and skips extraction
3. **Optional cleanup**: Set `PYTEST_CLEANUP_DATA=true` to remove extracted data after tests

#### GitHub Actions Example

```yaml
- name: Extract test data (cached)
  run: pytest --collect-only  # Triggers fixture without running tests
  
- name: Run tests
  run: pytest -v
  env:
    PYTHONPATH: /opt/paraview/lib/python3.10/site-packages
```

#### Cache Configuration (optional)

To speed up CI, cache the extracted test data:

```yaml
- name: Cache test data
  uses: actions/cache@v3
  with:
    path: |
      test/cases
      test/models
      test/Pictures
      test/.data_extracted
    key: test-data-${{ hashFiles('test/data.tar.gz') }}
```

## Test Coverage

Each geometry type (2D, 3D, Axi) has three test functions:

- **`test_init`**: Validates mesh loading and field initialization
- **`test_views`**: Image regression testing (compares against reference PNGs)
- **`test_stats`**: Statistical validation (compares against Feel++ solver outputs)

## Code Organization

### Shared Helpers (`base_test.py`)

To reduce code duplication, common test logic is centralized in `base_test.py`:

- `assert_images_equal()`: Image comparison with configurable tolerance
- `validate_temperature_stats()`: Temperature field validation against Feel++ data
- `validate_vonmises_stats()`: VonMises stress validation against Feel++ data
- `load_measures_csv()`: Safe CSV loading with error handling

### Tolerance Configuration (`tolerances.py`)

Standardized tolerance values are defined in `tolerances.py`:

| Field Type | 2D | 3D | Axi | Notes |
|-----------|-----|-----|-----|-------|
| Temperature | 0.1% | 1% | 0.1% | 3D uses looser tolerance due to interpolation complexity |
| VonMises | 1% | 1% | 1% | Consistent across all geometries |
| Image comparison | 0.1% | 0.1% | 0.1% | Visual consistency check |

**Rationale:**
- **Temperature**: 3D uses 1% tolerance (vs 0.1% for 2D/Axi) to account for additional numerical precision differences in 3D mesh interpolation
- **VonMises**: 1% for all types due to the derived nature of stress calculations (involves derivatives and tensor operations)
- **Image comparison**: 0.1% ensures visual consistency across all geometry types

### Known Limitations

**3D Test Case:**
- Temperature mean validation is disabled due to discrepancies exceeding the 1% tolerance
- VonMises validation is disabled due to missing `elastic.measures/values.csv` reference data

See inline comments in `test_3D.py` for details and TODO items.

## Manually Re-extracting Data

If you need to force re-extraction:

```bash
rm test/.data_extracted
pytest
```

Or manually extract:

```bash
cd test
tar -xzf data.tar.gz
mv unzip_for_pytest/* .
rmdir unzip_for_pytest
touch .data_extracted
```

## Test Data Management

### Git LFS Setup

The test data archive (`data.tar.gz`, ~20MB) is tracked using Git LFS to keep the repository lightweight and improve clone performance.

**First-time setup:**

```bash
# Install Git LFS (if not already installed)
# Ubuntu/Debian:
sudo apt-get install git-lfs

# macOS:
brew install git-lfs

# Initialize Git LFS for your user
git lfs install
```

**Working with the test data:**

The archive is automatically downloaded when you clone the repository:

```bash
git clone https://github.com/MagnetDB/hifimagnet.paraview.git
cd hifimagnet.paraview
```

Git LFS will handle the download of `test/data.tar.gz` transparently.

**Updating the test data archive:**

If you need to update the test data:

```bash
# Create new archive
cd test
tar -czf data.tar.gz -C unzip_for_pytest .

# Add and commit (Git LFS handles it automatically)
git add data.tar.gz
git commit -m "Update test data"
git push
```

**Verifying Git LFS status:**

```bash
# Check which files are tracked by LFS
git lfs ls-files

# Should show:
# test/data.tar.gz
```
