"""Unit tests for ParaView-independent utility functions.

These tests do NOT require ParaView or test data (data.tar.gz).
They cover pure-Python utility modules and run on every push/PR
in a standard CI environment.
"""

import pytest

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# json.py — json_get, get_materials_markers
# ---------------------------------------------------------------------------

from python_hifimagnetParaview.json import json_get, get_materials_markers


class TestJsonGet:
    def test_nested_keys(self):
        data = {"a": {"b": {"c": 42}}}
        assert json_get(data, "a", "b", "c") == 42

    def test_single_key(self):
        assert json_get({"hello": "world"}, "hello") == "world"

    def test_missing_key_returns_none(self):
        assert json_get({"a": 1}, "b") is None

    def test_partial_path_missing_returns_none(self):
        assert json_get({"a": {"b": 1}}, "a", "x") is None

    def test_non_dict_input_returns_none(self):
        assert json_get("not_a_dict", "key") is None

    def test_empty_dict_returns_none(self):
        assert json_get({}, "key") is None


class TestGetMaterialsMarkers:
    def test_markers_as_list(self):
        materials = {"mat1": {"markers": ["A", "B"]}}
        assert get_materials_markers(materials) == ["A", "B"]

    def test_markers_as_string(self):
        materials = {"mat1": {"markers": "A"}}
        assert get_materials_markers(materials) == ["A"]

    def test_no_markers_falls_back_to_material_key(self):
        materials = {"mat1": {}}
        assert get_materials_markers(materials) == ["mat1"]

    def test_multiple_materials(self):
        materials = {
            "mat1": {"markers": "A"},
            "mat2": {"markers": ["B", "C"]},
        }
        assert set(get_materials_markers(materials)) == {"A", "B", "C"}

    def test_empty_materials(self):
        assert get_materials_markers({}) == []


# ---------------------------------------------------------------------------
# compare.py — filter_files
# ---------------------------------------------------------------------------

from python_hifimagnetParaview.compare import filter_files


class TestFilterFiles:
    def test_single_file_returned_unchanged(self):
        files = ["dir/field.png"]
        assert filter_files(files) == ["dir/field.png"]

    def test_empty_list_returned_unchanged(self):
        assert filter_files([]) == []

    def test_exclude_terms_removes_matches(self):
        files = ["dir/foo.png", "dir/bar-OrOz.png", "dir/baz.png"]
        result = filter_files(files, exclude_terms=["OrOz"])
        assert result == ["dir/foo.png", "dir/baz.png"]

    def test_norm_preferred_when_multiple_files(self):
        files = ["dir/field.png", "dir/fieldnorm.png"]
        assert filter_files(files) == ["dir/fieldnorm.png"]

    def test_include_term_keeps_only_matching(self):
        files = ["dir/foo-OrOz.png", "dir/foo-OxOy.png"]
        result = filter_files(files, include_term="OrOz")
        assert result == ["dir/foo-OrOz.png"]

    def test_unique_term_custom(self):
        files = ["dir/field_r.png", "dir/field_z.png", "dir/field_norm.png"]
        result = filter_files(files, unique_term="_r")
        assert result == ["dir/field_r.png"]


# ---------------------------------------------------------------------------
# tolerances.py — get_tolerance
# ---------------------------------------------------------------------------

from test.tolerances import get_tolerance


class TestTolerances:
    def test_temperature_2D(self):
        assert get_tolerance("temperature", "2D") == pytest.approx(0.001)

    def test_temperature_3D_is_looser(self):
        assert get_tolerance("temperature", "3D") == pytest.approx(0.01)

    def test_temperature_axi(self):
        assert get_tolerance("temperature", "Axi") == pytest.approx(0.001)

    def test_vonmises_consistent_across_geometries(self):
        for geo in ("2D", "3D", "Axi"):
            assert get_tolerance("vonmises", geo) == pytest.approx(0.01)

    def test_image_consistent_across_geometries(self):
        for geo in ("2D", "3D", "Axi"):
            assert get_tolerance("image", geo) == pytest.approx(0.001)

    def test_invalid_field_type_raises_keyerror(self):
        with pytest.raises(KeyError):
            get_tolerance("invalid_field", "2D")

    def test_invalid_geometry_raises_keyerror(self):
        with pytest.raises(KeyError):
            get_tolerance("temperature", "4D")


# ---------------------------------------------------------------------------
# case3D/method3D.py — dictTypeUnits
# ---------------------------------------------------------------------------

import pint
from python_hifimagnetParaview.case3D.method3D import dictTypeUnits as dictTypeUnits3D


@pytest.fixture(scope="module")
def ureg():
    return pint.UnitRegistry()


class TestDictTypeUnits3D:
    def test_required_keys_present(self, ureg):
        units = dictTypeUnits3D(ureg, "mm")
        for key in (
            "Temperature",
            "ElectricConductivity",
            "MagneticField",
            "CurrentDensity",
            "VonMises",
            "ForceLaplace",
            "Displacement",
            "ElectricField",
        ):
            assert key in units, f"Missing key: {key}"

    def test_electric_field_components_are_V_per_m(self, ureg):
        units = dictTypeUnits3D(ureg, "mm")
        for component in (
            "ElectricField_x",
            "ElectricField_y",
            "ElectricField_z",
            "ElectricField_ur",
            "ElectricField_ut",
        ):
            in_unit = units[component]["Units"][0]
            assert in_unit == ureg.volt / ureg.meter, (
                f"{component}: expected V/m, got {in_unit}"
            )

    def test_electric_conductivity_naming_consistent(self, ureg):
        units = dictTypeUnits3D(ureg, "mm")
        assert "ElectricConductivity" in units
        assert "ElectricalConductivity" not in units

    def test_force_laplace_has_correct_units(self, ureg):
        units = dictTypeUnits3D(ureg, "mm")
        assert units["ForceLaplace"]["Units"][0] == ureg.newton / ureg.meter**3
