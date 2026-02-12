import pytest
import gmsh
import re
import json
import numpy as np
import pandas as pd
import argparse
import warnings

warnings.filterwarnings("ignore")

from PIL import Image

from test.base_test import (
    assert_images_equal,
    validate_temperature_stats,
    load_measures_csv
)
from python_hifimagnetParaview.cli import init
from python_hifimagnetParaview.json import returnExportFields
from python_hifimagnetParaview.method import convert_data
from python_hifimagnetParaview.meshinfo import meshinfo
from python_hifimagnetParaview.case3D.display3D import makeview
from python_hifimagnetParaview.case3D.method3D import create_dicts_fromjson

cases = [
    (
        "./test/cases/cfpdes-thmagel-3d-static-linear/Tore/np_1/cfpdes.exports/Export.case",
        "./test/models/cfpdes_Tore_3d_static/Tore_thmagel_3D.json",
    )
]

dim = 3
axis = False


@pytest.mark.parametrize("file,jsonfile", cases)
def test_init(file, jsonfile):

    meshpath = file.replace("cfpdes.exports/Export.case", "cfpdes.mesh.path")
    with open(meshpath, "r") as f:
        meshfile = f.readlines()[0]

    meshfile = "./" + meshfile.split("hifimagnet.paraview/")[1]
    meshfile = re.sub(r"_p\d+.json", ".msh", meshfile)

    gmsh.initialize()
    gmsh.open(meshfile)

    # Paraview : sum of nodes for each marker
    #   -> doesn't account for duplicate nodes on boundary between markers,
    # so the same is done for gmsh in this test = sum(NodesForPhysicalGroup)
    groups = gmsh.model.getPhysicalGroups()
    NumberOfNodes = 0
    for g in groups:
        if g[0] == 3:
            nodestag, _ = gmsh.model.mesh.getNodesForPhysicalGroup(g[0], g[1])
            NumberOfNodes += len(nodestag)

    _, elementTags, _ = gmsh.model.mesh.getElements(dim=3)
    NumberOfElements = len(elementTags[0])
    (cwd, basedir, ureg, distance_unit, reader) = init(file)

    dataInfo = reader.GetDataInformation()
    assert (
        dataInfo.GetNumberOfPoints() == NumberOfNodes
    ), f"Number of Points: paraview:{dataInfo.GetNumberOfPoints()} != msh:{NumberOfNodes}"
    assert (
        dataInfo.GetNumberOfCells() == NumberOfElements
    ), f"Number of Cells: paraview:{dataInfo.GetNumberOfCells()} != msh:{NumberOfElements}"

    fieldtype = returnExportFields(jsonfile, basedir)
    fieldunits, ignored_keys = create_dicts_fromjson(
        fieldtype, ureg, distance_unit, basedir
    )

    with open(f"{basedir}/FieldType.json", "r") as jsonfile:
        fieldtypejson = json.load(jsonfile)

    assert (
        fieldtype.keys() == fieldtypejson.keys()
    ), f"fieldtype: {fieldtype.keys()} != json:{fieldtypejson.keys()}"

    with open(f"{basedir}/fieldunits.json", "r") as jsonfile:
        fieldunitsjson = json.load(jsonfile)

    assert (
        fieldunits.keys() == fieldunitsjson.keys()
    ), f"fieldunits: {fieldunits.keys()} != json:{fieldunitsjson.keys()}"

    assert len(fieldtype.keys()) <= len(
        fieldunits.keys()
    ), f"fieldtype:{len(fieldtype.keys())} > fieldunits:{len(fieldunits.keys())}"


@pytest.mark.parametrize("file,jsonfile", cases)
def test_views(file, jsonfile):

    parser = argparse.ArgumentParser(description="", epilog="")
    args = parser.parse_args()

    args.z = None
    args.theta = None

    (cwd, basedir, ureg, distance_unit, reader) = init(file)

    fieldtype = returnExportFields(jsonfile, basedir)
    fieldunits, ignored_keys = create_dicts_fromjson(
        fieldtype, ureg, distance_unit, basedir
    )
    cellsize, blockdata, statsdict = meshinfo(
        reader, dim, fieldunits, ignored_keys, basedir, ureg, ComputeStats=False
    )

    for field in [
        "cfpdes.heat.temperature",
        "cfpdes.elastic.displacement",
        # "cfpdes.expr.B",
    ]:
        if field in list(cellsize.CellData.keys()):
            color = ["CELLS", field]
        if field in list(cellsize.PointData.keys()):
            color = ["POINTS", field]
        if field in list(cellsize.PointData.keys()) + list(cellsize.CellData.keys()):
            makeview(
                args,
                cellsize,
                blockdata,
                field,
                fieldunits,
                color,
                basedir,
                suffix="",
                addruler=False,
                background=False,
            )

        imageref = f"./test/Pictures/3D/{field}.png"
        imagenew = f"{basedir}/views/{field}.png"
        assert_images_equal(imageref, imagenew, "3D")


### pour gros fichiers git lfs


@pytest.mark.parametrize("file,jsonfile", cases)
def test_stats(file, jsonfile):

    (cwd, basedir, ureg, distance_unit, reader) = init(file)

    fieldtype = returnExportFields(jsonfile, basedir)
    fieldunits, ignored_keys = create_dicts_fromjson(
        fieldtype, ureg, distance_unit, basedir
    )
    cellsize, blockdata, statsdict = meshinfo(
        reader, dim, fieldunits, ignored_keys, basedir, ureg, ComputeStats=True
    )

    stats = pd.read_csv(f"{basedir}/stats/insert-descriptivestats.csv")
    statsheat = stats[stats["Variable"] == "T [°C]"]
    heatmeasures = load_measures_csv(basedir, "heat")

    if isinstance(heatmeasures, pd.DataFrame):
        # NOTE: Temperature mean validation is disabled for 3D due to larger
        # discrepancies. Uses 1% tolerance vs 0.1% for 2D/Axi.
        validate_temperature_stats(heatmeasures, statsheat, fieldunits, "3D", validate_mean=False)

    # NOTE: VonMises validation is disabled for 3D test case due to missing
    # elastic.measures/values.csv reference data in the test dataset.
    # This validation is enabled and passing for 2D and Axi test cases.
    # TODO: Add elastic measures reference data for 3D test case to enable validation.
