# Installation Testing Protocol for python-hifimagnetParaview

## Objective
Test the HiFiMagnet ParaView package installation in clean environments to verify:
1. Package can be installed successfully
2. All imports work correctly
3. CLI entry point functions properly
4. Core functionality executes without errors

## Test Environments

### Environment 1: Clean Virtual Environment (Primary Test)
**Purpose**: Verify standard pip installation

**Setup:**
```bash
# Create fresh virtual environment
python3 -m venv test-hifimagnet-clean
source test-hifimagnet-clean/bin/activate  # Linux/Mac
# OR: test-hifimagnet-clean\Scripts\activate  # Windows

# Verify clean state
pip list  # Should show only pip, setuptools, wheel
```

### Environment 2: Docker Container (Isolation Test)
**Purpose**: Verify installation in completely isolated environment

**Setup:**
```bash
# Use official Python image
docker run -it --rm python:3.13-slim bash
```

### Environment 3: With ParaView Dependencies (Full Integration Test)
**Purpose**: Verify package works with actual ParaView installation

**Setup:**
```bash
# Use existing devcontainer or ParaView environment
# This tests real-world usage scenario
```

---

## Test Suite

### TEST 1: Package Installation

**Execute in each environment:**
```bash
# Clone repository (or use local path)
git clone https://github.com/MagnetDB/hifimagnet.paraview.git
cd hifimagnet.paraview

# Install in development mode
pip install -e .
```

**Expected Output:**
```
Successfully installed python-hifimagnetParaview-0.1.0
```

**✅ PASS Criteria:**
- No error messages during installation
- All dependencies installed successfully
- Command completes with success exit code

**❌ FAIL Indicators:**
- Import errors for dependencies
- Missing package files
- Build errors

**Capture Results:**
```bash
# Document installation output
pip install -e . > install_test_output.txt 2>&1

# Verify package is installed
pip show python-hifimagnetParaview
pip list | grep hifimagnet
```

---

### TEST 2: Package Import and Metadata

**Execute:**
```python
# Test basic import
import python_hifimagnetParaview

# Test metadata access
print("Package:", python_hifimagnetParaview.__name__)
print("Version:", python_hifimagnetParaview.__version__)
print("Author:", python_hifimagnetParaview.__author__)
print("Email:", python_hifimagnetParaview.__email__)

# Test submodule imports
from python_hifimagnetParaview import cli
from python_hifimagnetParaview import method
from python_hifimagnetParaview import json
from python_hifimagnetParaview.case2D import display2D
from python_hifimagnetParaview.case3D import display3D
from python_hifimagnetParaview.caseAxi import methodAxi

print("\n✅ All imports successful!")
```

**Expected Output:**
```
Package: python_hifimagnetParaview
Version: 0.1.0
Author: Christophe Trophime
Email: christophe.trophime@lncmi.cnrs.fr

✅ All imports successful!
```

**✅ PASS Criteria:**
- All imports execute without ImportError
- Metadata values are correct and non-empty
- Version is not "unknown"

**❌ FAIL Indicators:**
- ImportError for any module
- __version__ shows "unknown"
- Missing __author__ or __email__

**Save Test Script:**
```bash
# Create test_imports.py with above content
python test_imports.py > import_test_results.txt 2>&1
```

---

### TEST 3: CLI Entry Point

**Execute:**
```bash
# Test 1: Verify command exists
which hifimagnet-paraview  # Should show path to executable

# Test 2: Show main help
hifimagnet-paraview --help

# Test 3: Show subcommand help
hifimagnet-paraview 3D --help
hifimagnet-paraview 2D --help
hifimagnet-paraview Axi --help
```

**Expected Output for main help:**
```
usage: hifimagnet-paraview [-h] {3D,2D,Axi} ...

positional arguments:
  {3D,2D,Axi}  sub-dimmension help
    3D         3D model
    2D         2D model
    Axi        Axi model

optional arguments:
  -h, --help   show this help message and exit
```

**✅ PASS Criteria:**
- `hifimagnet-paraview` command is in PATH
- Help message displays correctly
- All three geometry types (3D, 2D, Axi) are available
- No Python traceback errors

**❌ FAIL Indicators:**
- Command not found
- ImportError when running command
- Missing subcommands
- Traceback errors

**Capture Results:**
```bash
hifimagnet-paraview --help > cli_help_output.txt 2>&1
hifimagnet-paraview 3D --help > cli_3d_help_output.txt 2>&1
```

---

### TEST 4: Dependency Resolution

**Execute:**
```bash
# Check all required dependencies are installed
pip check

# List installed dependencies
pip list | grep -E "(argcomplete|gmsh|meshlib|numpy|pint|tabulate)"
```

**Expected Output:**
```
No broken requirements found.

argcomplete      3.3.0
gmsh             4.13.1
meshlib          2.4.2.30
numpy            1.26.4
pint             0.23
tabulate         0.9.0
```

**✅ PASS Criteria:**
- `pip check` reports no broken requirements
- All dependencies from pyproject.toml are installed
- Version numbers meet minimum requirements

**❌ FAIL Indicators:**
- Broken requirements reported
- Missing dependencies
- Version conflicts

---

### TEST 5: Function Execution (Smoke Test)

**Create minimal test case:**
```python
# test_basic_functionality.py
import sys
from python_hifimagnetParaview.cli import init, options

# Test 1: Options parser
print("Testing options parser...")
parser = options("Test", "Test epilog")
print("✅ Options parser created successfully")

# Test 2: Pint configuration
print("\nTesting Pint configuration...")
from pint import UnitRegistry
ureg = UnitRegistry()
ureg.define("percent = 0.01 = %")
ureg.define("ppm = 1e-6")
test_quantity = ureg.Quantity(1.0, "meter")
print(f"✅ Pint working: 1 meter = {test_quantity.to('millimeter')}")

# Test 3: ParaView availability (may fail if ParaView not installed)
try:
    from paraview.simple import GetParaViewVersion
    version = GetParaViewVersion()
    print(f"✅ ParaView available: version {version}")
except ImportError:
    print("⚠️  ParaView not available (expected in minimal environment)")

print("\n✅ All basic functionality tests passed!")
```

**Execute:**
```bash
python test_basic_functionality.py
```

**✅ PASS Criteria:**
- Options parser creates without errors
- Pint unit conversion works
- Script completes successfully

**❌ FAIL Indicators:**
- Import errors
- Runtime errors in basic operations

---

### TEST 6: Real Data Test (If Available)

**Only if you have test data:**
```bash
# Test with actual ParaView export file
hifimagnet-paraview 3D ./test/cases/cfpdes-thmagel-3d-static-linear/Tore/np_1/cfpdes.exports/Export.case \
    --json ./test/models/cfpdes_Tore_3d_static/Tore_thmagel_3D.json \
    --stats

# Check if output was generated
ls -la cfpdes.exports/paraview.exports/stats/
```

**✅ PASS Criteria:**
- Command executes without Python errors
- Output directory is created
- Statistics CSV files are generated

**❌ FAIL Indicators:**
- Python traceback errors
- No output generated
- ParaView errors

---

## Test Results Template

Document your test results using this template:
```markdown
# Installation Test Results

**Date:** [DATE]
**Tester:** [NAME]
**System:** [OS, Python version, ParaView version if applicable]

## Environment Details
- Python version: 
- pip version: 
- OS: 
- ParaView: [Yes/No, version if available]

## Test Results Summary

| Test | Status | Notes |
|------|--------|-------|
| TEST 1: Installation | ✅/❌ | |
| TEST 2: Import & Metadata | ✅/❌ | |
| TEST 3: CLI Entry Point | ✅/❌ | |
| TEST 4: Dependencies | ✅/❌ | |
| TEST 5: Basic Functionality | ✅/❌ | |
| TEST 6: Real Data (optional) | ✅/❌/N/A | |

**Overall Status:** ✅ PASS / ❌ FAIL

## Detailed Notes

### TEST 1: Installation
[Paste installation output or describe issues]

### TEST 2: Import & Metadata
[Paste import test output or describe issues]

### TEST 3: CLI Entry Point
[Paste CLI help output or describe issues]

### TEST 4: Dependencies
[Paste dependency check output or describe issues]

### TEST 5: Basic Functionality
[Paste functionality test output or describe issues]

### TEST 6: Real Data
[Describe test results or note N/A]

## Issues Found
1. [Issue description]
2. [Issue description]

## Recommendations
1. [Recommendation]
2. [Recommendation]
```

---

## Cleanup After Testing
```bash
# Deactivate virtual environment
deactivate

# Optional: Remove test environment
rm -rf test-hifimagnet-clean

# Exit Docker container (if used)
exit
```

---

## Common Issues and Solutions

### Issue 1: "command not found: hifimagnet-paraview"
**Cause:** Entry point not installed or not in PATH
**Solution:**
```bash
# Reinstall package
pip uninstall python-hifimagnetParaview -y
pip install -e .

# Verify entry point
pip show -f python-hifimagnetParaview | grep "hifimagnet-paraview"
```

### Issue 2: "ModuleNotFoundError: No module named 'python_hifimagnetParaview'"
**Cause:** Package not properly installed or PYTHONPATH issue
**Solution:**
```bash
# Check installation
pip list | grep hifimagnet

# Reinstall in development mode
pip install -e . --force-reinstall --no-deps
```

### Issue 3: "__version__ is 'unknown'"
**Cause:** Package not installed, only imported from source
**Solution:**
```bash
# Must install package (even in dev mode) for metadata
pip install -e .
# Then __version__ will work correctly
```

### Issue 4: Dependency conflicts
**Cause:** Existing packages conflict with requirements
**Solution:**
```bash
# Create completely fresh environment
python -m venv fresh-test --clear
source fresh-test/bin/activate
pip install -e .
```

---

## Success Criteria Checklist

Mark each item when verified:

- [ ] Package installs without errors in clean environment
- [ ] All imports work (`import python_hifimagnetParaview`)
- [ ] Package metadata accessible (`__version__`, `__author__`, `__email__`)
- [ ] CLI command available (`hifimagnet-paraview --help`)
- [ ] All subcommands work (3D, 2D, Axi help messages)
- [ ] Dependencies properly resolved (`pip check` passes)
- [ ] Basic functionality tests pass
- [ ] No import errors in submodules
- [ ] Version shows "0.1.0" not "unknown"

**All items checked = Installation is fully functional** ✅

---

## Next Steps After Successful Testing

1. Update README.md with confirmed installation instructions
2. Tag release in git: `git tag v0.1.0`
3. Consider uploading to PyPI for `pip install python-hifimagnetParaview`
4. Document any environment-specific requirements (ParaView, system libraries)
