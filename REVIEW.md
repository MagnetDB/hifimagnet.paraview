# Package Review: python-hifimagnetParaview

## Overview

This review covers the `python-hifimagnetParaview` package — a post-processing toolkit for [Feel++](https://docs.feelpp.org/) HiFiMagnet simulation results using ParaView's Python API.

- **Entry point**: `python_hifimagnetParaview/cli.py` → `hifimagnet-paraview` CLI
- **Sub-packages**: `case2D/`, `case3D/`, `caseAxi/`
- **Core modules**: `method.py`, `stats.py`, `meshinfo.py`, `view.py`, `histo.py`, `histoAxi.py`, `json.py`, `compare.py`

---

## 🔴 Critical Bugs

### 1. `view.py` — Broken f-strings and wrong type comparison in `scaleField` / `addField`

**`scaleField` (line 37):** Extra `"` inside the f-string produces invalid ParaView calculator expressions:
```python
# BUG
calculator1.Function = f'{key}/{factor}")'
# FIX
calculator1.Function = f'{key}/{factor}'
```

**`addField` (lines 61–64):** `float` (a type object) is compared instead of the parameter `factor`, and f-strings have the same extraneous `"`:
```python
# BUG: always evaluates to False; broken f-strings
if float < 0:
    calculator1.Function = f'{key}-{abs(factor)}")'
else:
    calculator1.Function = f'{key}+{factor}")'
# FIX
if factor < 0:
    calculator1.Function = f'{key}-{abs(factor)}'
else:
    calculator1.Function = f'{key}+{factor}'
```

### 2. `method.py` — `torque()` function incomplete (lines 305–314)

The function creates a `Calculator` but never calls `.UpdatePipeline()` and never returns it, unlike the similar `momentN()` function:
```python
# FIX: add at end of torque()
calculator1.UpdatePipeline()
return calculator1
```

### 3. `cli.py` — `fieldtype` used before assignment when `--json` is not given (lines 240–241)

`fieldtype` is only defined inside the `if args.json:` block but is used unconditionally by `getB0()` later, causing `NameError`:
```python
# FIX: initialize fieldtype before the conditional
fieldtype = {}
if args.json:
    fieldtype = returnExportFields(args.json, basedir)
    fieldunits, ignored_keys = create_dicts_fromjson(fieldtype, ureg, distance_unit, basedir)
else:
    fieldunits, ignored_keys = create_dicts(ureg, distance_unit, basedir)
```

### 4. `cli.py` — `case "_":` leaves core variables undefined (lines 220–221)

When no valid dimension is matched, `dim`, `axis`, `meshinfo`, `makeplot`, `makeview`, `create_dicts`, `create_dicts_fromjson` are never assigned, causing `NameError` on the next use:
```python
# FIX
case _:
    parser.error(f"Unknown dimension: {args.dimmension}. Must be 3D, 2D, or Axi.")
    return 1
```

### 5. `case3D/method3D.py` — Duplicate `ForceLaplace` key silently overrides first definition

`dictTypeUnits()` defines `"ForceLaplace"` at lines 236–250 and again at lines 313–320 with an identical value. The second definition silently overwrites the first. The duplicate should be removed.

### 6. `method.py` — `savedkey` potentially used before assignment in `getB0()` (lines 546–558)

If neither the CellData nor PointData branch assigns `savedkey`, it is then used at line 550, causing `NameError`. Fix: initialize `savedkey = None` before the key-scan loop.

### 7. `json.py` — Hardcoded relative path for `FeelppType.json` (line 128)

```python
# BUG: breaks when CWD is not project root
with open("./python_hifimagnetParaview/FeelppType.json", "r") as jsonfile:

# FIX: use importlib.resources (Python 3.9+)
from importlib.resources import files
with files("python_hifimagnetParaview").joinpath("FeelppType.json").open() as jsonfile:
```

---

## 🟠 High-Priority Issues

### 8. `pyproject.toml` — Subpackages missing from distribution (line 66)

`case2D`, `case3D`, `caseAxi` are not included in the `packages` list and will be absent from an installed wheel:
```toml
# FIX: replace explicit listing with find
[tool.setuptools.packages.find]
where = ["."]
include = ["python_hifimagnetParaview*"]
```

### 9. `compare.py` — `need` variable used before assignment (lines 318–322)

If `--plots` is set without `--r`, `--z`, or `--theta`, `need` is never defined but is passed to `get_files_list()`:
```python
# FIX: initialize before conditional
need = ""
if args.r:
    need = "vs-r"
elif args.z:
    need = "vs-z"
elif args.theta:
    need = "vs-theta"
```

### 10. `case3D/method3D.py` — `ElectricField` component units wrong (lines 124–162)

`ElectricField_x/y/z/ur/ut` all use `ureg.volt / ureg.meter**2` (V/m²) but should be `ureg.volt / ureg.meter` (V/m), the correct unit for electric field components.

### 11. `case3D/method3D.py` — `ElectricConductivity` vs `ElectricalConductivity` naming mismatch

- `dictTypeUnits()` uses key `"ElectricConductivity"` (line 33)
- `create_dicts()` uses key `"ElectricalConductivity"` (line 762)

These must be consistent to avoid `KeyError` at runtime.

---

## 🟡 Medium-Priority Issues

### 12. `histo.py` / `histoAxi.py` — `show` parameter has no effect

Both `plotHisto()` and `plotHistoAxi()` accept `show` but immediately override it with `show = False` (lines 99 and 95 respectively). The parameter should either be honored or removed.

### 13. `method.py` / `stats.py` — Bare `except:` clauses

- `method.py` line 558: `except: return None` in `getB0()`
- `stats.py` lines 250–253: `except: pass` in file cleanup

Bare `except` catches `KeyboardInterrupt`, `SystemExit`, and other control-flow exceptions. Replace with specific types:
```python
except (FileNotFoundError, OSError):
    pass
```

### 14. `meshinfo.py` — Large commented-out code block (lines 346–493)

A prototype block is commented out but still present (148 lines). It contains an `exit(1)` call that would terminate the program if accidentally uncommented. The block should be removed or moved to a feature branch.

### 15. `stats.py` — Malformed docstring in `getresultStats` (lines 280–283)

The function contains two separate string literals instead of a single docstring:
```python
) -> str:
    """ """

    """
    ...
    """
```
Should be unified into a single docstring.

---

## 🟢 Low-Priority / Style Issues

### 16. `__init__.py` — Dead Python < 3.8 fallback code (lines 6–8)

Package requires Python >= 3.10 (`pyproject.toml` line 14), making the `importlib_metadata` fallback import dead code.

### 17. `json.py` — Variable `dict` shadows built-in (line 61)

`dict = {}` shadows Python's built-in `dict` type within the function. Rename to `field_dict` or similar.

### 18. `method.py` — Local variable `keyinfo` shadows function name (line 252)

```python
def keyinfo(key: str) -> tuple:
    keyinfo = key.split(".")  # shadows itself
```
Rename the local variable to `parts` or `key_parts`.

### 19. `case3D/method3D.py` — Typo `mSymobol` (lines 29, 765)

`"mSymobol"` should be `"mSymbol"`. This typo causes the field to be stored under the wrong key name.

### 20. `view.py` — Overly broad check in `deformed()` (lines 34–35)

```python
if not warpByVector1.PointData.keys():
    warpByVector1.Vectors = ["POINTS", "cfpdes.elastic.displacement"]
```
Checks whether PointData is entirely empty rather than whether the specific key `"elasticity.displacement"` exists. Should use an explicit key membership check.

---

## Missing Infrastructure

| Gap | Description |
|-----|-------------|
| No CI test runner | `.github/workflows/docs.yml` only builds documentation; no workflow runs `pytest` |
| No linting config | No ruff/flake8/pylint configuration in `pyproject.toml` |
| No type checking | No mypy or pyright configuration |

---

## Summary Table

| # | Severity | File | Issue |
|---|----------|------|-------|
| 1 | 🔴 Critical | `view.py` | Broken f-strings in `scaleField`/`addField`; wrong `float` type comparison |
| 2 | 🔴 Critical | `method.py` | `torque()` missing `UpdatePipeline()` and return |
| 3 | 🔴 Critical | `cli.py` | `fieldtype` NameError when `--json` not provided |
| 4 | 🔴 Critical | `cli.py` | Unhandled `case "_":` leaves variables undefined |
| 5 | 🔴 Critical | `case3D/method3D.py` | Duplicate `ForceLaplace` key silently overrides first entry |
| 6 | 🔴 Critical | `method.py` | `savedkey` used before assignment in `getB0()` |
| 7 | 🔴 Critical | `json.py` | Hardcoded relative path for `FeelppType.json` |
| 8 | 🟠 High | `pyproject.toml` | Subpackages `case2D`, `case3D`, `caseAxi` missing from package distribution |
| 9 | 🟠 High | `compare.py` | `need` used before assignment in plot comparison |
| 10 | 🟠 High | `case3D/method3D.py` | ElectricField component units V/m² should be V/m |
| 11 | 🟠 High | `case3D/method3D.py` | `ElectricConductivity` vs `ElectricalConductivity` inconsistency |
| 12 | 🟡 Medium | `histo.py`, `histoAxi.py` | `show` parameter immediately overridden; has no effect |
| 13 | 🟡 Medium | `method.py`, `stats.py` | Bare `except:` clauses swallow all exceptions |
| 14 | 🟡 Medium | `meshinfo.py` | 148-line commented-out block with latent `exit(1)` |
| 15 | 🟡 Medium | `stats.py` | Malformed split docstring in `getresultStats` |
| 16 | 🟢 Low | `__init__.py` | Dead Python < 3.8 fallback code |
| 17 | 🟢 Low | `json.py` | Variable `dict` shadows built-in |
| 18 | 🟢 Low | `method.py` | Local variable `keyinfo` shadows function name |
| 19 | 🟢 Low | `case3D/method3D.py` | Typo `mSymobol` (×2) |
| 20 | 🟢 Low | `view.py` | Overly broad check in `deformed()` for displacement vector |
