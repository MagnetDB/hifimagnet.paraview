# Test Suite Improvements - Implementation Prompt

## Context

The hifimagnet.paraview test suite is located in the `test/` directory and consists of three test files (`test_2D.py`, `test_3D.py`, `test_Axi.py`) that test 2D, 3D, and axisymmetric geometry types respectively. Each file contains three test functions: `test_init`, `test_views`, and `test_stats`.

**Recently completed:**
- ✅ Automated test data extraction using pytest fixture (`test/conftest.py`)
- ✅ Git LFS support for test data archive (`test/data.tar.gz`)
- ✅ CI/CD workflow template (`.github/workflows/tests.yml`)
- ✅ Comprehensive documentation (`test/README.md`, `docs/GIT_LFS.md`)

**Remaining improvements needed:**
The following issues were identified during the test suite review but have not yet been addressed.

## Task 1: Reduce Code Duplication

### Problem
The three test files (`test_2D.py`, `test_3D.py`, `test_Axi.py`) contain ~95% identical code with only minor differences:

**Differences between files:**
- Import statements (case2D/case3D/caseAxi modules)
- `dim` parameter (2D/Axi use `dim=2`, 3D uses `dim=3`)
- Field names tested in `test_views` and `test_stats`
- Test data paths (cases, models, reference images)
- Statistical tolerance values

**Current duplication:**
- `assert_images_equal` function duplicated 3 times (identical)
- `test_init` logic duplicated 3 times (~100 lines each)
- `test_views` logic duplicated 3 times (~50 lines each)  
- `test_stats` logic duplicated 3 times (~100 lines each)

### Implementation Strategy

**Option A: Parametrized single test file**
Create a single `test_all_geometries.py` with pytest parametrization:
```python
@pytest.mark.parametrize("geometry,dim,module", [
    ("2D", 2, "case2D"),
    ("3D", 3, "case3D"),
    ("Axi", 2, "caseAxi"),
])
def test_init(geometry, dim, module):
    # unified test logic
```

**Option B: Base test class with inheritance**
```python
# test/base_test.py
class BaseGeometryTest:
    geometry_type = None
    dim = None
    
    def test_init(self):
        # shared implementation
        
# test/test_2D.py
class Test2D(BaseGeometryTest):
    geometry_type = "2D"
    dim = 2
```

**Option C: Shared fixtures and helper functions**
Move common logic to `test/conftest.py` and keep separate test files but with minimal code.

**Recommendation:** Evaluate which approach best balances:
- Maintainability
- Test isolation and clarity
- Ease of debugging individual geometry types
- Minimal disruption to existing test structure

### Acceptance Criteria
- [ ] Code duplication reduced to <20% between geometry tests
- [ ] All 9 tests (3 geometries × 3 test types) still pass
- [ ] Test output clearly identifies which geometry type is being tested
- [ ] Individual geometry tests can still be run separately: `pytest test/test_2D.py`

## Task 2: Clean Up Commented Code

### Problem
`test/test_3D.py` contains large blocks of commented-out code that reduce code clarity:

**Lines 123-150 in test_3D.py:**
- Entire VonMises statistical validation commented out
- Temperature mean check commented out (lines 108-110)

**Questions to resolve:**
1. Why are these checks disabled?
2. Are there known issues with VonMises calculations in 3D?
3. Should tolerance values be adjusted instead?
4. Are the reference data files missing/incorrect?

### Implementation Strategy

1. **Investigate why code is commented:**
   - Check git history: `git log -p test/test_3D.py`
   - Search for related issues in the repository
   - Test if uncommenting causes failures

2. **Take action based on findings:**
   - If tests fail: Document reason in code comment and/or skip with `pytest.mark.skip`
   - If tests pass: Remove comment markers
   - If tolerance issue: Adjust tolerance and document why
   - If missing data: Add proper error handling or skip gracefully

3. **Use proper pytest patterns for known issues:**
   ```python
   @pytest.mark.skip(reason="VonMises validation disabled - see issue #123")
   def test_vonmises_3d():
       pass
   
   @pytest.mark.xfail(reason="Mean calculation differs >1% from Feel++")
   def test_temperature_mean():
       assert ...
   ```

### Acceptance Criteria
- [ ] No commented test code remains without clear documentation
- [ ] Known issues documented with pytest markers or inline comments
- [ ] All enabled tests pass
- [ ] Test coverage maintained or improved

## Task 3: Standardize Tolerance Values

### Problem
Different tolerance values are used across geometry types without clear justification:

**Current tolerances:**

| Test | Field | 2D | 3D | Axi |
|------|-------|----|----|-----|
| Stats | Temperature max | 0.1% | 1% | 0.1% |
| Stats | Temperature mean | 0.1% | (disabled) | 0.1% |
| Stats | Temperature min | 0.1% | 1% | 0.1% |
| Stats | VonMises max | 1% | (disabled) | 1% |
| Stats | VonMises mean | 1% | (disabled) | 1% |
| Stats | VonMises min | 1% | (disabled) | 1% |
| Views | Image difference | 0.1% | 0.1% | 0.1% |

**Questions:**
- Why does 3D use 10× looser tolerance for temperature?
- Is this a numerical precision issue or data quality issue?
- Should tolerances be field-dependent or geometry-dependent?

### Implementation Strategy

1. **Document current behavior:**
   - Run all tests and capture actual differences
   - Identify which tests would fail with tighter tolerances
   - Analyze if differences are systematic or random

2. **Establish tolerance policy:**
   - Define acceptable error margins per field type
   - Document rationale in code comments or test documentation
   - Consider creating a tolerance configuration file

3. **Implement standardized approach:**
   ```python
   # test/tolerances.py
   TOLERANCES = {
       "temperature": {"relative": 0.001, "absolute": 0.1},  # 0.1% or 0.1°C
       "vonmises": {"relative": 0.01, "absolute": 1.0},       # 1% or 1 MPa
       "displacement": {"relative": 0.01, "absolute": 1e-6},  # 1% or 1μm
   }
   ```

4. **Update assertions to use standardized values**

### Acceptance Criteria
- [ ] Tolerance values documented with rationale
- [ ] Consistent tolerance approach across all geometry types
- [ ] All tests pass with standardized tolerances
- [ ] Clear error messages when tolerance exceeded
- [ ] Configuration centralized in one location

## Task 4: Remove Duplicate Tests Directory

### Problem
Two test directories exist:
- `test/` - Active directory with test files
- `tests/` - Contains only `__init__.py~` (backup file)

This can cause confusion and pytest collects from both locations.

### Implementation Strategy

```bash
# Check if tests/ is used anywhere
grep -r "tests/" .

# Remove duplicate directory
rm -rf tests/

# Update .gitignore if needed
# Ensure pytest.ini or pyproject.toml only references test/
```

### Acceptance Criteria
- [ ] `tests/` directory removed
- [ ] No references to `tests/` in codebase
- [ ] `pyproject.toml` pytest configuration updated if needed
- [ ] All tests still discoverable with `pytest`

## Task 5: Add Missing Test Coverage (Optional Enhancement)

### Potential additions:
- [ ] Test error handling (invalid files, missing data)
- [ ] Test CLI argument parsing
- [ ] Test mesh info extraction edge cases
- [ ] Test histogram generation
- [ ] Test comparison functionality
- [ ] Performance regression tests
- [ ] Memory usage tests

## Implementation Order

Recommended sequence to minimize conflicts:

1. **Task 4** (Remove duplicate directory) - Quickest, prevents confusion
2. **Task 2** (Clean up commented code) - Understand current state
3. **Task 3** (Standardize tolerances) - Establish baseline
4. **Task 1** (Reduce duplication) - Major refactor, do last
5. **Task 5** (Additional coverage) - Future enhancement

## Success Metrics

After all improvements:
- [ ] Test suite runs successfully in CI/CD
- [ ] Code duplication < 20%
- [ ] No unexplained commented code
- [ ] Documented tolerance policy
- [ ] Single test directory structure
- [ ] Maintainable and extensible test suite
- [ ] Clear test output and error messages

## Files to Modify

- `test/test_2D.py` - Refactor/merge
- `test/test_3D.py` - Clean up comments, refactor/merge
- `test/test_Axi.py` - Refactor/merge
- `test/conftest.py` - Add shared fixtures/helpers
- `pyproject.toml` - Update pytest configuration if needed
- `test/README.md` - Update documentation
- New: `test/tolerances.py` - Centralized tolerance config
- New: `test/test_all_geometries.py` - If using Option A

## Testing Strategy

Before merging any changes:
1. Run full test suite: `pytest -v`
2. Run specific geometry: `pytest test/test_2D.py -v`
3. Run specific test type: `pytest -k test_stats -v`
4. Verify CI/CD workflow runs successfully
5. Check test coverage: `pytest --cov=python_hifimagnetParaview`

## References

- Current test suite: `test/`
- Test documentation: `test/README.md`
- CI workflow: `.github/workflows/tests.yml`
- Pytest docs: https://docs.pytest.org/
- Pytest parametrization: https://docs.pytest.org/en/stable/parametrize.html
