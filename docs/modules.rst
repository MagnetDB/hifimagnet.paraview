Main Modules
============

The ``python_hifimagnetParaview`` package consists of several main modules:

CLI Module
----------

:mod:`python_hifimagnetParaview.cli`
    Command-line interface for batch post-processing operations. Supports 3D, 2D, 
    and axisymmetric geometries.

Statistics Modules
------------------

:mod:`python_hifimagnetParaview.stats`
    Statistical analysis for 3D and 2D cases. Computes descriptive statistics 
    (min, max, mean, standard deviation) for each PointData/CellData field.

:mod:`python_hifimagnetParaview.statsAxi`
    Statistical analysis specifically for axisymmetric cases.

Histogram Modules
-----------------

:mod:`python_hifimagnetParaview.histo`
    Histogram generation for 3D and 2D cases. Creates distribution histograms 
    for field values.

:mod:`python_hifimagnetParaview.histoAxi`
    Histogram generation for axisymmetric cases.

Visualization
-------------

:mod:`python_hifimagnetParaview.view`
    Automated visualization creation with customizable colormaps, ranges, and 
    backgrounds. Generates PNG images of field distributions.

Comparison Tools
----------------

:mod:`python_hifimagnetParaview.compare`
    Compare results between different simulations, geometries, or solution 
    approaches. Supports comparison of statistics, histograms, and views.

Mesh Information
----------------

:mod:`python_hifimagnetParaview.meshinfo`
    Extract mesh information for 3D and 2D cases.

:mod:`python_hifimagnetParaview.meshinfoAxi`
    Extract mesh information for axisymmetric cases.

Utility Modules
---------------

:mod:`python_hifimagnetParaview.json`
    JSON file handling for configuration and field definitions.

:mod:`python_hifimagnetParaview.method`
    Common methods and utilities used across different modules.

Case-Specific Modules
---------------------

:mod:`python_hifimagnetParaview.case2D`
    2D-specific processing routines.

:mod:`python_hifimagnetParaview.case3D`
    3D-specific processing routines.

:mod:`python_hifimagnetParaview.caseAxi`
    Axisymmetric-specific processing routines.
