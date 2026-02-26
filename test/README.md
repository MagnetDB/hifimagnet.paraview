# Test Suite

This directory contains the test suite for hifimagnet.paraview.

## Structure

```
test/
├── conftest.py              # Pytest fixtures (test data extraction)
├── base_test.py             # Shared test helper functions
├── tolerances.py            # Centralized tolerance configuration
├── data.tar.gz              # Test data archive (20MB, Git LFS)
├── test_unit.py             # Unit tests — no ParaView, no data needed
├── test_2D.py               # Integration tests for 2D geometry
├── test_3D.py               # Integration tests for 3D geometry
├── test_Axi.py              # Integration tests for axisymmetric geometry
├── cases/                   # [extracted] Simulation test cases
├── models/                  # [extracted] JSON configs and meshes
└── Pictures/                # [extracted] Reference images
```

## Test Types

Tests are split into two categories using pytest markers:

| Marker | File(s) | Requires |
|--------|---------|---------|
| `unit` | `test_unit.py` | Standard Python deps only — no ParaView, no test data |
| `integration` | `test_2D.py`, `test_3D.py`, `test_Axi.py` | ParaView + `data.tar.gz` |

## Running Tests

### Unit tests (no ParaView needed)

Unit tests cover pure-Python utility functions (`json.py`, `compare.py`,
`case3D/method3D.py`, `tolerances.py`) and run anywhere:

```bash
pip install -e ".[test]"
pytest -m unit -v
```

### Integration tests (ParaView required)

Integration tests exercise the full ParaView pipeline and require both a
working ParaView installation and the extracted test data.

Configure the Python path to use ParaView's Python bindings:

```bash
export PYTHONPATH=/opt/paraview/lib/python3.10/site-packages/
```

Run all integration tests:

```bash
pytest -m integration -v
```

Or a specific geometry:

```bash
pytest test/test_2D.py -v
pytest test/test_3D.py::test_stats -v
pytest test/test_Axi.py -v
```

The test data in `data.tar.gz` is extracted automatically on the first run
via the `test_data` fixture in `conftest.py`. Subsequent runs detect the
`.data_extracted` marker file and skip extraction.

## Continuous Integration

The CI workflow (`.github/workflows/tests.yml`) runs two jobs:

### `unit-tests`

- Triggered on **every push and pull request**
- Runs on Python 3.10, 3.11, and 3.12
- No ParaView installation required, no Git LFS files fetched

```bash
pytest -m unit -v --tb=short
```

### `integration-tests`

- Triggered on **push to `main`** and **manual `workflow_dispatch`**
- Downloads ParaView 5.12.0 (osmesa/headless build) on first run, then
  cached by version string so subsequent runs skip the ~400 MB download
- Fetches `data.tar.gz` via Git LFS (`lfs: true` in checkout), then caches
  the extracted data by content hash so extraction runs only once per
  archive version

```bash
pytest -m integration -v --tb=short
```

### Caching strategy

| Resource | Cache key | Approx. size |
|----------|-----------|--------------|
| ParaView `/opt/paraview` | `paraview-<version>-<flavor>-py<version>` | ~400 MB |
| Extracted test data | `test-data-<sha256 of data.tar.gz>` | ~100 MB |

Both caches are invalidated only when their respective inputs change, so
typical CI runs skip both the ParaView download and the data extraction
entirely.

### Git LFS bandwidth

`data.tar.gz` (~20 MB) is stored in Git LFS and fetched once per
integration run. GitHub provides 1 GB/month of free LFS bandwidth for
public repositories; ~20 MB per integration run leaves ample headroom for
normal development.

If LFS bandwidth becomes a concern, the extracted data cache can be
pre-populated to avoid LFS fetches on cache hits by also caching
`test/data.tar.gz` itself:

```yaml
- name: Cache LFS object
  uses: actions/cache@v4
  with:
    path: test/data.tar.gz
    key: lfs-data-${{ hashFiles('.git/lfs/objects/**') }}
```

## Test Coverage

Each geometry type (2D, 3D, Axi) has three test functions:

- **`test_init`**: Validates mesh loading and field initialization
- **`test_views`**: Image regression testing (compares against reference PNGs)
- **`test_stats`**: Statistical validation (compares against Feel++ solver outputs)

`test_unit.py` covers utility functions that have no ParaView dependency:
`json_get`, `get_materials_markers`, `filter_files`, `get_tolerance`, and
`dictTypeUnits` (including unit-correctness assertions).

## Code Organization

### Shared Helpers (`base_test.py`)

Common test logic shared across geometry types:

- `assert_images_equal()`: Image comparison with configurable tolerance
- `validate_temperature_stats()`: Temperature field validation against Feel++ data
- `validate_vonmises_stats()`: VonMises stress validation against Feel++ data
- `load_measures_csv()`: Safe CSV loading with error handling

### Tolerance Configuration (`tolerances.py`)

| Field Type | 2D | 3D | Axi | Notes |
|-----------|-----|-----|-----|-------|
| Temperature | 0.1% | 1% | 0.1% | 3D uses looser tolerance due to interpolation complexity |
| VonMises | 1% | 1% | 1% | Consistent across all geometries |
| Image comparison | 0.1% | 0.1% | 0.1% | Visual consistency check |

### Known Limitations

**3D Test Case:**
- Temperature mean validation is disabled due to discrepancies exceeding the 1% tolerance
- VonMises validation is disabled due to missing `elastic.measures/values.csv` reference data

See inline comments in `test_3D.py` for details and TODO items.

## Manually Re-extracting Data

Force re-extraction by removing the marker file:

```bash
rm test/.data_extracted
pytest -m integration
```

Or extract manually:

```bash
cd test
tar -xzf data.tar.gz
mv unzip_for_pytest/* .
rmdir unzip_for_pytest
touch .data_extracted
```

## Test Data Management

### Git LFS Setup

The test data archive (`data.tar.gz`, ~20MB) is tracked using Git LFS.

```bash
# Ubuntu/Debian
sudo apt-get install git-lfs

# macOS
brew install git-lfs

# Enable for your user
git lfs install
```

Git LFS handles the download of `test/data.tar.gz` transparently on clone.

### Updating the test data archive

```bash
cd test
tar -czf data.tar.gz -C unzip_for_pytest .

git add data.tar.gz
git commit -m "Update test data"
git push
```

### Verifying Git LFS status

```bash
git lfs ls-files
# Should show: test/data.tar.gz
```
