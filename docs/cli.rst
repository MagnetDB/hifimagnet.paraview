Command-Line Interface
======================

The ``python_hifimagnetParaview.cli`` module provides the main command-line 
interface for post-processing operations.

Basic Commands
--------------

Statistics & Histograms
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D Export.case --stats --histos

Views
~~~~~

Create views with custom options:

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D Export.case --views \
     --customRangeHisto --transparentBG --deformedfactor 5

Plots
~~~~~

Create plots vs radial coordinate:

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D Export.case --plots \
     --r 0.2 0.34 --theta 0.0 4.21875 5.625 --greyspace

Create plots vs angular coordinate:

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D Export.case --plots \
     --r 0.20895

Combined Operations
~~~~~~~~~~~~~~~~~~~

You can combine multiple operations in a single command:

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli Axi Export.case \
     --stats --histos --views --json simulation.json

Comparison Tool
---------------

The ``python_hifimagnetParaview.compare`` module allows comparing results 
between different simulations.

Required Arguments
~~~~~~~~~~~~~~~~~~

* ``--mdata``: Dictionary with 2 results directories

  .. code-block:: bash

     --mdata '{"geo1":"directory1", "geo2":"directory2"}'

Optional Arguments
~~~~~~~~~~~~~~~~~~

* ``--name``: Magnet/site name
* ``--views``: Activate views calculations
  
  * ``--theta``: If geometry is 3D, select OrOz views
  * ``--z``: If geometry is 3D, select OxOy views

* ``--plots``: Activate plots calculations
  
  * ``--r``: Plots vs r
  * ``--theta``: Plots vs theta
  * ``--z``: Plots vs z
  * ``--r`` && ``--theta``: Make boxplots of plot vs theta on plot vs r

* ``--histos``: Activate histograms calculations
* ``--cooling``: Give cooling for pictures name
* ``--friction``: Give friction for pictures name

Example
~~~~~~~

.. code-block:: bash

   python -m python_hifimagnetParaview.compare \
     --mdata '{"3D": "tmp/HL-31/thermo-electric.exports/paraview.exports",
              "Axi": "tmp/M19061901/cfpdes.exports/paraview.exports"}' \
     --name M19061901 --cooling grad --friction Constant \
     --plots --r --theta --histos --views
