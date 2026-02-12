Development
===========

Testing
-------

Running the Test Suite
~~~~~~~~~~~~~~~~~~~~~~

Configure the Python path to use Paraview's Python bindings:

.. code-block:: bash

   export PYTHONPATH=/opt/paraview/lib/python3.10/site-packages/

Run tests located in the ``test/`` directory:

.. code-block:: bash

   pytest

Development Roadmap
-------------------

Planned Features
~~~~~~~~~~~~~~~~

Performance
^^^^^^^^^^^

- [ ] Monitor memory - for stats, histos improve by using selectblock instead of extractblock?
- [ ] Test with MPI
- [ ] Offset rendering - requires specific build options for paraview (see paraview downloads - headless), ``--force-offscreen-rendering``

Completed Features
^^^^^^^^^^^^^^^^^^

- [x] Create a CLI with argparse command stats, plots, views
- [x] Split pv-statistics.py accordingly to CLI commands (note add subparser option)
- [x] Add field for Magnetostatics and ThermoElectric physics
- [x] Add PlotOr and PlotOz
- [x] Add min/max to legend
- [x] Change colormap for display
- [x] Use eventually CustomRange for display
- [x] Adapt for 2D
- [x] Adapt for Axi: trouble with stats, need to rewrite this part
- [x] Create fieldunits, ignored_keys from json
- [x] Create a CLI for post-processing operations by loading a json

Visualization Features
^^^^^^^^^^^^^^^^^^^^^^

- [ ] What about generate 3D from Axi?
- [ ] Display on selected points
- [ ] Export scene for VtkJs
- [ ] Streamline (see pv-thmagstreamline.py)
- [ ] Create Contour (see pv-contour.py)
- [ ] Support for tensor
- [ ] Create developed view of cylinder slice (see `Paraview Discourse <https://discourse.paraview.org/t/how-to-create-a-developed-view-of-a-cylinder-slice/14569>`_, `Kitware Blog <https://www.kitware.com/paraviews-python-programmable-filters-in-geophysics/>`_, `Dataset Resampling <https://www.kitware.com/dataset-resampling-filters/>`_)
- [ ] Compute spherical harmonics from Sphere slice? see shtools?

CLI and Configuration
^^^^^^^^^^^^^^^^^^^^^

- [ ] Add tools to read:write:add to fieldunits json
- [ ] Run in client/server mode
- [ ] Add user defined custom range for views (how?)
- [ ] Convert xaxis units in plots

Analysis Tools
^^^^^^^^^^^^^^

- [ ] Develop comparison of different results:
  
  - Merge histos
  - Better boxplot

Open Questions
--------------

* How to discard matplotlib plots when line is not in insert?
* Add statistics per matplotlib plot?

Contributing
------------

Guidelines for contributing to the project will be added here.

Code Style
~~~~~~~~~~

This project follows PEP 8 style guidelines for Python code.

Pull Requests
~~~~~~~~~~~~~

When submitting a pull request, please ensure:

1. All tests pass
2. New features include appropriate tests
3. Documentation is updated as needed
4. Commit messages are clear and descriptive

References
----------

* `Feel++ <https://docs.feelpp.org/home/index.html>`_
* `HiFiMagnet <https://github.com/feelpp/hifimagnet>`_
* `Paraview Python Scripting <https://docs.paraview.org/en/latest/Tutorials/SelfDirectedTutorial/batchPythonScripting.html>`_
