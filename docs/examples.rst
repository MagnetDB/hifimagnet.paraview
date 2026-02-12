Examples
========

Ansys Files
-----------

Processing Ansys VTK Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open the file with Paraview to inspect the fields:

.. code-block:: bash

   paraview output.vtk

Create a JSON file describing the fields and their types:

``output.json``:

.. code-block:: json

   {
       "S_EQV": {
           "Type": "VonMises",
           "Exclude": []
       }
   }

Basic Command
~~~~~~~~~~~~~

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D tmp/ansys.exports/output.vtk \
     --json tmp/output.json

Statistics & Histograms
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D tmp/ansys.exports/output.vtk \
     --json tmp/output.json --stats --histos

Views
~~~~~

Create views with custom range, transparent background, and deformed view:

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D tmp/ansys.exports/output.vtk \
     --json tmp/output.json --views \
     --customRangeHisto --transparentBG --deformedfactor 5

Plots vs Radial Coordinate
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D tmp/ansys.exports/output.vtk \
     --json tmp/output.json --plots \
     --r 0.2 0.34 --theta 0.0 4.21875 5.625 --greyspace

Plots vs Angular Coordinate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D tmp/ansys.exports/output.vtk \
     --json tmp/output.json --plots --r 0.20895

Feel++ Examples
---------------

3D Example
~~~~~~~~~~

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 3D \
     ../../HL-31/test/hybride-Bh27.7T-Bb9.15T-Bs9.05T_HPfixed_BPfree/bmap/np_32/elasticity.exports/Export.case \
     --plots --z -0.15 -0.1 -0.05 0 0.05 0.1 0.15 --r 1.94e-2 2.52e-2 3.17e-2

2D Example with Views
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli 2D \
     tmp/cfpdes-thmagel_hcurl-Axi-static-nonlinear/M9Bitters_18MW_laplace/gradH/Montgomery/Colebrook/np_16/cfpdes.exports/Export.case \
     --views

Axisymmetric Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pvbatch -m python_hifimagnetParaview.cli Axi \
     tmp/cfpdes-thmagel_hcurl-Axi-static-nonlinear/M9Bitters_18MW_laplace/gradH/Montgomery/Colebrook/np_16/cfpdes.exports/Export.case \
     --stats --histos --json tmp/M9Bitters_18MW-cfpdes-thmagel_hcurl-nonlinear-Axi-sim.json

Comparison Between Simulations
-------------------------------

Compare 3D vs Axisymmetric Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -m python_hifimagnetParaview.compare \
     --mdata '{"3D": "tmp/HL-31_HPfixed_BPfixed/grad/Constant/np_32/thermo-electric.exports/paraview.exports",
              "Axi": "tmp/M19061901_laplace_dilatation31k/grad/Montgomery/Constant/np_16/cfpdes.exports/paraview.exports"}' \
     --name M19061901 --cooling grad --friction Constant \
     --plots --r --theta --histos --views

Custom Matplotlib Plots
-----------------------

Viewing Custom Plots
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python vonmises-vs-theta.py \
     --file 'r=0.0194m-z=0.07m-1.csv' 'r=0.0194m-z=0.07m-0.csv' \
     --key thermo_electric.heat.temperature \
     --ylabel 'T [K]' \
     --title 'Temperature in H1: r=xx, z=yy' \
     --show

MeshLib Integration
-------------------

Channel Width Estimation
~~~~~~~~~~~~~~~~~~~~~~~~~

Install MeshLib in a separate virtual environment:

.. code-block:: bash

   python3 -m venv --system-site-packages meshlib-env
   source ./meshlib-env/bin/activate
   python3 -m pip install meshlib

Run the channel width estimation:

.. code-block:: bash

   python test-meshlib.py H*_Cu0.stl \
     --rfiles R[0-9]0.stl R1[0-3]0.stl --deformed

References
~~~~~~~~~~

* `MeshLib <https://github.com/MeshInspector/MeshLib>`_
* `Measuring distance between meshes <https://stackoverflow.com/questions/61159587/measure-distance-between-meshes>`_
