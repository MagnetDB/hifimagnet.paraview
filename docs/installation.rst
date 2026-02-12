Installation
============

Python Package with Virtual Environment
----------------------------------------

For Linux/Mac OS X:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/MagnetDB/hifimagnet.paraview.git
   cd hifimagnet.paraview

   # Create virtual environment with access to system site-packages (for Paraview)
   python3 -m venv --system-site-packages hifimagnetParaview-env

   # Activate the virtual environment
   source ./hifimagnetParaview-env/bin/activate

   # Install the package
   pip install -e .

.. note::
   The ``--system-site-packages`` flag is required to access Paraview's Python 
   bindings installed at the system level.

To deactivate the virtual environment:

.. code-block:: bash

   deactivate

Debian Package
--------------

Installation as a Debian package (to be implemented):

.. code-block:: bash

   # Download the .deb package
   wget https://github.com/MagnetDB/hifimagnet.paraview/releases/download/vX.Y.Z/python-hifimagnet-paraview_X.Y.Z_all.deb

   # Install the package
   sudo dpkg -i python-hifimagnet-paraview_X.Y.Z_all.deb

   # Install dependencies if needed
   sudo apt-get install -f

Docker Container
----------------

Standard Paraview
~~~~~~~~~~~~~~~~~

Build the Docker image from the provided Dockerfile:

.. code-block:: bash

   # Build with default settings (Python 3.10, Paraview 5.12)
   docker build -t hifimagnet-paraview:latest .

   # Build with custom versions
   docker build \
     --build-arg PYVER=3.11 \
     --build-arg PV_VERSION_MAJOR=5.12 \
     --build-arg PV_VERSION_MINOR=1 \
     -t hifimagnet-paraview:5.12.1 .

Headless Paraview (for HPC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Build with osmesa-MPI for offscreen rendering
   docker build -f Dockerfile.opengl \
     --build-arg PV_FLAVOR=osmesa-MPI \
     -t hifimagnet-paraview:osmesa .

   # Or with EGL support
   docker build -f Dockerfile.opengl \
     --build-arg PV_FLAVOR=egl-MPI \
     -t hifimagnet-paraview:egl .

Run the container
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Interactive mode
   docker run -it --rm \
     -v $(pwd)/data:/data \
     hifimagnet-paraview:latest bash

   # Run post-processing
   docker run --rm \
     -v $(pwd)/data:/data \
     hifimagnet-paraview:latest \
     pvbatch -m python_hifimagnetParaview.cli 3D /data/Export.case --stats --histos

Build Arguments
~~~~~~~~~~~~~~~

* ``PYVER``: Python version (default: 3.10)
* ``PV_VERSION_MAJOR``: Paraview major version (e.g., 5.12)
* ``PV_VERSION_MINOR``: Paraview minor version (e.g., 0)
* ``PV_FLAVOR``: Paraview flavor - valid values: ``osmesa-MPI``, ``egl-MPI``

Singularity Container
----------------------

Build from Docker image:

.. code-block:: bash

   # Build from Docker image
   singularity build hifimagnet-paraview.sif docker://hifimagnet-paraview:latest

   # Or build from definition file (if provided)
   sudo singularity build hifimagnet-paraview.sif hifimagnet-paraview.def

Run with Singularity
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Interactive mode
   singularity shell hifimagnet-paraview.sif

   # Execute post-processing
   singularity exec hifimagnet-paraview.sif \
     pvbatch -m python_hifimagnetParaview.cli 3D Export.case --stats --histos

   # Bind data directories
   singularity exec --bind /path/to/data:/data hifimagnet-paraview.sif \
     pvbatch -m python_hifimagnetParaview.cli Axi /data/Export.case --views
