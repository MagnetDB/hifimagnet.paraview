Usage
=====

Overview
--------

The ``python_hifimagnetParaview`` package provides a command-line interface for 
post-processing simulation results. The main entry point is the ``cli`` module, 
which can be invoked using ``pvbatch``.

Basic Usage
-----------

The CLI supports three geometry types:

* ``3D``: Three-dimensional geometries
* ``2D``: Two-dimensional geometries  
* ``Axi``: Axisymmetric geometries

Basic command structure:

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli <dimension> <input_file> [options]

Getting Help
------------

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli --help
   pvbatch -m python_hifimagnetParaview.cli 3D --help
   pvbatch -m python_hifimagnetParaview.cli 2D --help
   pvbatch -m python_hifimagnetParaview.cli Axi --help

Common Options
--------------

Required Arguments
~~~~~~~~~~~~~~~~~~

* ``dimension``: Choose between 3D, 2D or Axi
* ``file``: Input case file (e.g., Export.case)

Optional Arguments
~~~~~~~~~~~~~~~~~~

JSON Configuration
^^^^^^^^^^^^^^^^^^

* ``--json``: Give Feel++ json file to detect exported fields

Views
^^^^^

* ``--views``: Create views per PointData, CellData and save them to PNG
  
  * ``--field``: Select a field, by default get all fields
  * ``--transparentBG``: Enable transparent background on views
  * ``--customRangeHisto``: Enable custom range in views, recovered from histograms
  * ``--deformedfactor``: Select a deformation factor, by default 1

Statistics
^^^^^^^^^^

* ``--stats``: Compute stats per PointData, CellData per block (aka Feel++ marker)

Histograms
^^^^^^^^^^

* ``--histos``: Compute histogram per PointData, CellData per insert
  
  * ``--bins``: Select number of bins in histograms, by default 20

Plots
^^^^^

* ``--plots``: Create plots per PointData, CellData using given coordinates
  
  * ``--z``: Z coordinate(s) for plotting
  * ``--theta``: Angular coordinate(s) for plotting
  * ``--r``: Radial coordinate(s) for plotting
  * ``--plotmarker``: Choose marker for plots calculations
  * ``--greyspace``: Plot grey bar for holes (channels/slits) in plot
  * ``--show``: Show plots

2D-Specific Options
~~~~~~~~~~~~~~~~~~~

* ``--cliptheta``: Select an angle to clip the geometry

3D-Specific Options
~~~~~~~~~~~~~~~~~~~

* ``--channels``: Enable creation of STL files for test-meshlib.py
* ``--z``: With "--views", create an OxOy view at z
* ``--theta``: With "--views", create OrOz views at theta=0/30/60/90/120/150deg

Output Files
------------

All data files are saved in CSV format for further analysis:

* Statistics files: ``*-descriptivestats-create.csv``
* Histogram files: ``*-histogram.csv``
* Plot files: ``*-plot.csv``
* View images: ``*.png``
