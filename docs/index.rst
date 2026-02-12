.. HiFiMagnet Paraview documentation master file

Welcome to HiFiMagnet Paraview's documentation!
================================================

**HiFiMagnet Paraview** is a comprehensive Python package that provides automated 
post-processing capabilities for electromagnetics and thermomechanics simulations. 
It integrates with Paraview to enable batch processing of simulation exports, 
supporting 3D, 2D, and axisymmetric geometries.

Key Features
------------

* **Statistical Analysis**: Compute descriptive statistics per PointData/CellData for each block/marker
* **Histogram Generation**: Create histograms for field distributions with customizable bins
* **Visualization**: Generate automated views with customizable colormaps, ranges, and backgrounds
* **Plot Extraction**: Extract 1D plots along radial, axial, or angular coordinates
* **Multi-format Support**: Process Feel++ exports, Ansys VTK files, and other Paraview-compatible formats
* **Comparison Tools**: Compare results between different geometries or simulation approaches
* **CSV Export**: All computed data saved in CSV format for further analysis

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   cli
   modules
   examples
   development
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
