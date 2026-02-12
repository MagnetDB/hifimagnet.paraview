import pytest
import gmsh
import re
import json
import numpy as np
import pandas as pd

from PIL import Image

from test.base_test import (
    assert_images_equal,
    validate_temperature_stats,
    validate_vonmises_stats,
    load_measures_csv
)
from python_hifimagnetParaview.cli import init
from python_hifimagnetParaview.json import returnExportFields
from python_hifimagnetParaview.method import convert_data
from python_hifimagnetParaview.meshinfoAxi import meshinfo
from python_hifimagnetParaview.case2D.display2D import makeview
from python_hifimagnetParaview.caseAxi.methodAxi import create_dicts_fromjson


axi_cases = [
    (
        "./test/cases/cfpdes-thmagel-Axi-static-linear/Tore/np_1/cfpdes.exports/Export.case",
        "./test/models/cfpdes_Tore_axi_static/Toretest-cfpdes-thmagel_hcurl-Axi-sim.json",
    )
]
dim = 2
axis = True


@pytest.mark.parametrize("file,jsonfile", axi_cases)
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
        if g[0] == 2:
            nodestag, _ = gmsh.model.mesh.getNodesForPhysicalGroup(g[0], g[1])
            NumberOfNodes += len(nodestag)

    _, elementTags, _ = gmsh.model.mesh.getElements(dim=2)
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


@pytest.mark.parametrize("file,jsonfile", axi_cases)
def test_views(file, jsonfile):

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
                None,
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

        imageref = f"./test/Pictures/Axi/{field}.png"
        imagenew = f"{basedir}/views/{field}.png"
        assert_images_equal(imageref, imagenew, "Axi")


### pour gros fichiers git lfs


@pytest.mark.parametrize("file,jsonfile", axi_cases)
def test_stats(file, jsonfile):

    (cwd, basedir, ureg, distance_unit, reader) = init(file)

    fieldtype = returnExportFields(jsonfile, basedir)
    fieldunits, ignored_keys = create_dicts_fromjson(
        fieldtype, ureg, distance_unit, basedir
    )
    cellsize, blockdata, statsdict = meshinfo(
        reader, dim, fieldunits, ignored_keys, basedir, ureg, ComputeStats=True
    )

    statsheat = pd.read_csv(
        f"{basedir}/stats/cfpdes.heat.temperature-descriptivestats-create.csv"
    )
    heatmeasures = load_measures_csv(basedir, "heat")

    if isinstance(heatmeasures, pd.DataFrame):
        validate_temperature_stats(heatmeasures, statsheat, fieldunits, "Axi")

    statselastic = pd.read_csv(
        f"{basedir}/stats/cfpdes.expr.Vonmises-descriptivestats-create.csv"
    )
    elasticmeasures = load_measures_csv(basedir, "elastic")

    if isinstance(elasticmeasures, pd.DataFrame):
        validate_vonmises_stats(elasticmeasures, statselastic, fieldunits, "Axi", field_name="Vonmises")
