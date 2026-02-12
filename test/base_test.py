"""
Base test helpers and utilities for hifimagnet.paraview test suite.

This module provides shared functionality to reduce code duplication across
2D, 3D, and Axi geometry test files.
"""

import numpy as np
import pandas as pd
from PIL import Image
from test.tolerances import get_tolerance
from python_hifimagnetParaview.method import convert_data


def assert_images_equal(image_1: str, image_2: str, geometry_type: str):
    """
    Compare two images and assert they are within tolerance.
    
    Args:
        image_1: Path to first image (reference)
        image_2: Path to second image (generated)
        geometry_type: One of "2D", "3D", "Axi" for tolerance lookup
    """
    img1 = Image.open(image_1)
    img2 = Image.open(image_2)

    # Convert to same mode and size for comparison
    img2 = img2.convert(img1.mode)
    img2 = img2.resize(img1.size)

    sum_sq_diff = np.sum(
        (np.asarray(img1).astype("float") - np.asarray(img2).astype("float")) ** 2
    )

    tolerance = get_tolerance("image", geometry_type)
    if sum_sq_diff == 0:
        # Images are exactly the same
        pass
    else:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
        assert (
            normalized_sum_sq_diff < tolerance
        ), f'{image_1.split("/")[-1]}: {normalized_sum_sq_diff} > {tolerance}'


def validate_temperature_stats(
    heatmeasures: pd.DataFrame,
    statsheat: pd.DataFrame,
    fieldunits: dict,
    geometry_type: str,
    validate_mean: bool = True
):
    """
    Validate temperature statistics against Feel++ reference data.
    
    Args:
        heatmeasures: DataFrame from heat.measures/values.csv
        statsheat: DataFrame from stats CSV with temperature data
        fieldunits: Dictionary of field units
        geometry_type: One of "2D", "3D", "Axi" for tolerance lookup
        validate_mean: Whether to validate mean temperature (disabled for some 3D cases)
    """
    units = {"temperature": fieldunits["temperature"]["Units"]}

    Feel_T_max = convert_data(
        units, heatmeasures["Statistics_Stat_T_max"].iloc[0], "temperature"
    )
    Feel_T_mean = convert_data(
        units, heatmeasures["Statistics_Stat_T_mean"].iloc[0], "temperature"
    )
    Feel_T_min = convert_data(
        units, heatmeasures["Statistics_Stat_T_min"].iloc[0], "temperature"
    )

    temp_tol = get_tolerance("temperature", geometry_type)
    
    assert (
        abs(1 - Feel_T_max / statsheat["Maximum"].iloc[0]) < temp_tol
    ), f'Tmax: abs(1-Feel:{Feel_T_max}/Paraview:{statsheat["Maximum"].iloc[0]}) > {temp_tol}'
    
    if validate_mean:
        assert (
            abs(1 - Feel_T_mean / statsheat["Mean"].iloc[0]) < temp_tol
        ), f'Tmean: abs(1-Feel:{Feel_T_mean}/Paraview:{statsheat["Mean"].iloc[0]}) > {temp_tol}'
    
    assert (
        abs(1 - Feel_T_min / statsheat["Minimum"].iloc[0]) < temp_tol
    ), f'Tmin: abs(1-Feel:{Feel_T_min}/Paraview:{statsheat["Minimum"].iloc[0]}) > {temp_tol}'


def validate_vonmises_stats(
    elasticmeasures: pd.DataFrame,
    statselastic: pd.DataFrame,
    fieldunits: dict,
    geometry_type: str,
    field_name: str = "VonMises"
):
    """
    Validate VonMises stress statistics against Feel++ reference data.
    
    Args:
        elasticmeasures: DataFrame from elastic.measures/values.csv
        statselastic: DataFrame from stats CSV with VonMises data
        fieldunits: Dictionary of field units
        geometry_type: One of "2D", "3D", "Axi" for tolerance lookup
        field_name: Field name in fieldunits ("VonMises" or "Vonmises")
    """
    units = {field_name: fieldunits[field_name]["Units"]}
    
    # Determine column names based on geometry type
    if geometry_type == "Axi":
        max_col = "Statistics_VonMises_Tore_max"
        mean_col = "Statistics_VonMises_Tore_mean"
        min_col = "Statistics_VonMises_Tore_min"
    else:
        max_col = "Statistics_Stat_VonMises_max"
        mean_col = "Statistics_Stat_VonMises_mean"
        min_col = "Statistics_Stat_VonMises_min"

    Feel_VM_max = convert_data(
        units, elasticmeasures[max_col].iloc[0], field_name
    )
    Feel_VM_mean = convert_data(
        units, elasticmeasures[mean_col].iloc[0], field_name
    )
    Feel_VM_min = convert_data(
        units, elasticmeasures[min_col].iloc[0], field_name
    )

    vm_tol = get_tolerance("vonmises", geometry_type)
    
    assert (
        abs(1 - Feel_VM_max / statselastic["Maximum"].iloc[0]) < vm_tol
    ), f'VonMisesmax: abs(1-Feel:{Feel_VM_max}/Paraview:{statselastic["Maximum"].iloc[0]}) > {vm_tol}'
    assert (
        abs(1 - Feel_VM_mean / statselastic["Mean"].iloc[0]) < vm_tol
    ), f'VonMisesmean: abs(1-Feel:{Feel_VM_mean}/Paraview:{statselastic["Mean"].iloc[0]}) > {vm_tol}'
    assert (
        abs(1 - Feel_VM_min / statselastic["Minimum"].iloc[0]) < vm_tol
    ), f'VonMisesmin: abs(1-Feel:{Feel_VM_min}/Paraview:{statselastic["Minimum"].iloc[0]}) > {vm_tol}'


def load_measures_csv(basedir: str, measure_type: str):
    """
    Load a measures CSV file with error handling.
    
    Args:
        basedir: Base directory containing paraview exports
        measure_type: Type of measures ("heat" or "elastic")
        
    Returns:
        DataFrame if file exists and loads successfully, None otherwise
    """
    try:
        measures_path = basedir.replace(
            "cfpdes.exports/paraview.exports",
            f"{measure_type}.measures/values.csv"
        )
        return pd.read_csv(measures_path)
    except Exception:
        return None
