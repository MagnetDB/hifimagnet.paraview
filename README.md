# HiFiMagnet Paraview - Post-processing Tools

A Python module for post-processing and visualization of HiFiMagnet/Feel++ simulation results using Paraview.

## Description

`python_hifimagnetParaview` is a comprehensive Python package that provides automated post-processing capabilities for electromagnetics and thermomechanics simulations. It integrates with Paraview to enable batch processing of simulation exports, supporting 3D, 2D, and axisymmetric geometries.

**Key Features:**
- **Statistical Analysis**: Compute descriptive statistics per PointData/CellData for each block/marker
- **Histogram Generation**: Create histograms for field distributions with customizable bins
- **Visualization**: Generate automated views with customizable colormaps, ranges, and backgrounds
- **Plot Extraction**: Extract 1D plots along radial, axial, or angular coordinates
- **Multi-format Support**: Process Feel++ exports, Ansys VTK files, and other Paraview-compatible formats
- **Comparison Tools**: Compare results between different geometries or simulation approaches
- **CSV Export**: All computed data saved in CSV format for further analysis

**Main Modules:**
- `cli`: Command-line interface for batch post-processing
- `stats`, `statsAxi`: Statistical analysis for 3D/2D and axisymmetric cases
- `histo`, `histoAxi`: Histogram generation
- `view`: Automated visualization creation
- `compare`: Result comparison between different simulations
- `meshinfo`, `meshinfoAxi`: Mesh information extraction

## Installation

### Prerequisites

**Git LFS (Large File Storage):**

This repository uses Git LFS to manage large test data files. Install Git LFS before cloning:

```bash
# Ubuntu/Debian
sudo apt-get install git-lfs

# macOS
brew install git-lfs

# Windows (with Git for Windows)
# Git LFS is included in recent versions

# Initialize Git LFS for your user (first-time only)
git lfs install
```

Then clone the repository (Git LFS will automatically download tracked files):

```bash
git clone https://github.com/MagnetDB/hifimagnet.paraview.git
cd hifimagnet.paraview
```

### Python Package with Virtual Environment

For Linux/Mac OS X:

```bash
# Clone the repository
git clone https://github.com/MagnetDB/hifimagnet.paraview.git
cd hifimagnet.paraview

# Create virtual environment with access to system site-packages (for Paraview)
python3 -m venv --system-site-packages hifimagnetParaview-env

# Activate the virtual environment
source ./hifimagnetParaview-env/bin/activate

# Install the package
pip install -e .
```

**Note:** The `--system-site-packages` flag is required to access Paraview's Python bindings installed at the system level.

To deactivate the virtual environment:
```bash
deactivate
```

### Debian Package

Installation as a Debian package (to be implemented):

```bash
# Download the .deb package
wget https://github.com/MagnetDB/hifimagnet.paraview/releases/download/vX.Y.Z/python-hifimagnet-paraview_X.Y.Z_all.deb

# Install the package
sudo dpkg -i python-hifimagnet-paraview_X.Y.Z_all.deb

# Install dependencies if needed
sudo apt-get install -f
```

### Docker Container

Build the Docker image from the provided Dockerfile:

**Standard Paraview:**
```bash
# Build with default settings (Python 3.10, Paraview 5.12)
docker build -t hifimagnet-paraview:latest .

# Build with custom versions
docker build \
  --build-arg PYVER=3.11 \
  --build-arg PV_VERSION_MAJOR=5.12 \
  --build-arg PV_VERSION_MINOR=1 \
  -t hifimagnet-paraview:5.12.1 .
```

**Headless Paraview (for HPC):**
```bash
# Build with osmesa-MPI for offscreen rendering
docker build -f Dockerfile.opengl \
  --build-arg PV_FLAVOR=osmesa-MPI \
  -t hifimagnet-paraview:osmesa .

# Or with EGL support
docker build -f Dockerfile.opengl \
  --build-arg PV_FLAVOR=egl-MPI \
  -t hifimagnet-paraview:egl .
```

**Run the container:**
```bash
# Interactive mode
docker run -it --rm \
  -v $(pwd)/data:/data \
  hifimagnet-paraview:latest bash

# Run post-processing
docker run --rm \
  -v $(pwd)/data:/data \
  hifimagnet-paraview:latest \
  pvbatch -m python_hifimagnetParaview.cli 3D /data/Export.case --stats --histos
```

**Build Arguments:**
- `PYVER`: Python version (default: 3.10)
- `PV_VERSION_MAJOR`: Paraview major version (e.g., 5.12)
- `PV_VERSION_MINOR`: Paraview minor version (e.g., 0)
- `PV_FLAVOR`: Paraview flavor - valid values: `osmesa-MPI`, `egl-MPI`

### Singularity Container

Build from Docker image:

```bash
# Build from Docker image
singularity build hifimagnet-paraview.sif docker://hifimagnet-paraview:latest

# Or build from definition file (if provided)
sudo singularity build hifimagnet-paraview.sif hifimagnet-paraview.def
```

**Run with Singularity:**
```bash
# Interactive mode
singularity shell hifimagnet-paraview.sif

# Execute post-processing
singularity exec hifimagnet-paraview.sif \
  pvbatch -m python_hifimagnetParaview.cli 3D Export.case --stats --histos

# Bind data directories
singularity exec --bind /path/to/data:/data hifimagnet-paraview.sif \
  pvbatch -m python_hifimagnetParaview.cli Axi /data/Export.case --views
```

## Documentation

Full documentation is available online at: **https://magnetdb.github.io/hifimagnet.paraview/**

### Building the Documentation Locally

To build the HTML documentation locally:

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build the documentation
cd docs
make html
```

The built documentation will be available in `docs/_build/html/index.html`.

For more information, see [docs/README.md](docs/README.md).

## Usage

### Command-line Interface - `python_hifimagnetParaview.cli`

* get range per PointData, CellData
* compute stats per PointData, CellData for insert
* compute histogram per PointData, CellData for insert
* display 3D/2D/Axi view
* display 2D OrOz view for theta in 

All data file are saved in csv format for other use.

Required
* `dimmension`: choose between 3D, 2D or Axi
* `file`: input case file (ex. Export.case)

Optional
* `--json`: 
    * give `feelpp` json file to detect exported fields
* `--views`: 
    * create views per PointData, CellData and save them to png
    * `--field`: select a field, by default get all fields
    * `--transparentBG`: enable transparent background on views
    * `--customRangeHisto`: enable custom range in views, recovered from histograms
    * `--deformedfactor`: select a deformation factor, by default 1
* `--stats`: 
    * compute stats per PointData, CellData per block (aka `feelpp` marker) 
* `--histos`: 
    * compute histogram per PointData, CellData per insert
    * `--bins`: select number of bins in histograms, by default 20
* `--plots`: 
    * create plots per PointData, CellData using given coordinates :
    * `--z`: 
    * `--theta`: 
    * `--r`: 
    * `--plotmarker`: choose marker for plots calculations
    * `--greyspace`: plot grey bar for holes (channels/slits) in plot 
    * `--show`: show plots

Optional specific to 2D:
* `--cliptheta`: select an angle to clip the geometry

Optional specific to 3D:
* `--channels`: enable creation of stl files for test-meshlib.py
* `--z`: with "--views", create a OxOy view at z
* `--theta`: with "--views", create OrOz views at theta=0/30/60/90/120/150deg

### Getting Help

```bash
pvbatch -m python_hifimagnetParaview.cli --help
pvbatch -m python_hifimagnetParaview.cli 3D --help
pvbatch -m python_hifimagnetParaview.cli 2D --help
pvbatch -m python_hifimagnetParaview.cli Axi --help
```

## Examples

### Example for Ansys files (output.vtk)

Open the file with paraview

```bash
paraview output.vtk
```

Write the fields in a json with their type:

`output.json`:
```json
{
    "S_EQV": {
        "Type": "VonMises",
        "Exclude": []
    }
}
```

Run the command with any post-processing operation:

Basic command
```bash
pvbatch -m python_hifimagnetParaview.cli 2D  tmp/ansys.exports/output.vtk --json tmp/output.json
```


Statistics & histograms
```bash
pvbatch -m python_hifimagnetParaview.cli 2D  tmp/ansys.exports/output.vtk --json tmp/output.json --stats --histos
```

Views (custom range from histograms, transparent background, deformed view)
```bash
pvbatch -m python_hifimagnetParaview.cli 2D  tmp/ansys.exports/output.vtk --json tmp/output.json --views [--customRangeHisto] [--transparentBG] [--deformedfactor 5]
```

Plots
    vs r
```bash
pvbatch -m python_hifimagnetParaview.cli 2D  tmp/ansys.exports/output.vtk --json tmp/output.json --plots --r 0.2 0.34 --theta 0.0 4.21875 5.625 [--greyspace]
```
    vs theta
```bash
pvbatch -m python_hifimagnetParaview.cli 2D  tmp/ansys.exports/output.vtk --json tmp/output.json --plots --r 0.20895
```

### Feel++ Examples

```bash
pvbatch -m python_hifimagnetParaview.cli 3D  ../../HL-31/test/hybride-Bh27.7T-Bb9.15T-Bs9.05T_HPfixed_BPfree/bmap/np_32/elasticity.exports/Export.case --plots --z -0.15 -0.1 -0.05 0 0.05 0.1 0.15  --r 1.94e-2 2.52e-2 3.17e-2
pvbatch -m python_hifimagnetParaview.cli 2D  tmp/cfpdes-thmagel_hcurl-Axi-static-nonlinear/M9Bitters_18MW_laplace/gradH/Montgomery/Colebrook/np_16/cfpdes.exports/Export.case --views
pvbatch -m python_hifimagnetParaview.cli Axi  tmp/cfpdes-thmagel_hcurl-Axi-static-nonlinear/M9Bitters_18MW_laplace/gradH/Montgomery/Colebrook/np_16/cfpdes.exports/Export.case --stats --histos --json tmp/M9Bitters_18MW-cfpdes-thmagel_hcurl-nonlinear-Axi-sim.json
```

### Comparing Results Between Simulations

Compare results between 2 paraview.exports using `python_hifimagnetParaview.compare`.

Required
* `--mdata`: give a dict with 2 results directory ('{geo1:directory1, geo2:directory2}')

Optional
* `--name`: 
    * give magnet/site name
* `--views`: 
    * activate views calculations
    * `--theta`: if geometry is 3D, select OrOz views
    * `--z`: if geometry is 3D, select OxOy views
* `--plots`: 
    * activate plots calculations
    * `--r`: plots vs r
    * `--theta`: plots vs theta
    * `--z`: plots vs z
    * `--r` && `--theta` : make boxplots of plot vs theta on plot vs r
* `--histos`: 
    * activate histograms calculations
* `--cooling`: 
    * give cooling for pictures name
* `--friction`: 
    * give friction for pictures name

**Example:**
```bash
python -m python_hifimagnetParaview.compare --mdata '{"3D": "tmp/HL-31_HPfixed_BPfixed/grad/Constant/np_32/thermo-electric.exports/paraview.exports","Axi": "tmp/M19061901_laplace_dilatation31k/grad/Montgomery/Constant/np_16/cfpdes.exports/paraview.exports"}'  --name M19061901 --cooling grad --friction Constant --plots --r --theta --histos --views
```

### Using Matplotlib for Custom Plots

To view the plot:

```bash
python vonmises-vs-theta.py --file 'r=0.0194m-z=0.07m-1.csv' 'r=0.0194m-z=0.07m-0.csv' --key thermo_electric.heat.temperature --ylabel 'T [K]' --title 'Temperature in H1: r=xx, z=yy' --show
```

### Channel Width Estimation with MeshLib

Need to install MeshLib:

```bash
python3 -m venv --system-site-packages meshlib-env
source ./meshlib-env/bin/activate
python3 -m pip install meshlib
```

Run:

```bash
python3 ./test-meshlib.py --help
python test-meshlib.py H*_Cu0.stl [--rfiles R[0-9]0.stl R1[0-3]0.stl] --deformed
```

To start the virtual env:

```bash
source ./meshlib-env/bin/activate
```

To exit the virtual env:

```bash
deactivate
```

**References:**
* [MeshLib](https://github.com/MeshInspector/MeshLib)
* [Measuring distance between meshes](https://stackoverflow.com/questions/61159587/measure-distance-between-meshes)

## Testing

### Running the Test Suite

The test suite uses pytest with automatic test data management. Test data is automatically extracted from `test/data.tar.gz` on first run.

Configure the Python path to use Paraview's Python bindings:
```bash
export PYTHONPATH=/opt/paraview/lib/python3.10/site-packages/
```

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run specific test modules:
```bash
pytest test/test_2D.py
pytest test/test_3D.py
pytest test/test_Axi.py
```

For more details on the test suite structure, CI integration, and caching strategies, see [test/README.md](test/README.md).

## Development Roadmap
- [ ] monitor memory - for stats,histos improve by using selectblock instead of extractblock?
- [x] create a cli with argsparse command stats,plots,views
- [x] split pv-statistics.py accordingly to cli commands (note add subparser option)
- [x] Add field for Magnetostatics and ThermoElectric physics
- [x] Add PlotOr and PlotOz
- [ ] Test with MPI
- [ ] Offset rendering - requires specific build options for paraview (see paraview downloads - headless ), '--force-offscreen-rendering'
- [x] Add min/max to legend
- [x] Change colormap for display
- [x] Use eventually CustomRange for display
- [x] Adapt for 2D
- [x] Adapt for Axi: trouble with stats, need to rewrite this part
- [ ] what about generate 3D from Axi?
- [ ] Display on selected points
- [ ] Export scene for VtkJs
- [ ] Streamline (see pv-thmagstreamline.py)
- [ ] Create Contour (see pv-contour.py)
- [ ] Support for tensor
- [ ] Create developed view of cylinder slice (see https://discourse.paraview.org/t/how-to-create-a-developed-view-of-a-cylinder-slice/14569, https://www.kitware.com/paraviews-python-programmable-filters-in-geophysics/, https://www.kitware.com/dataset-resampling-filters/)
- [ ] Compute spherical harmonics from Sphere slice ? see shtools?
- [x] Create fieldunits, ignored_keys from json 
- [ ] Add tools to read:write:add to fieldunits json
- [x] Create a CLI for post-processing operations by loading a json
- [ ] Run in client/server mode
- [ ] Add user defined custom range for views (how?)
- [ ] Convert xaxis units in plots
- [ ] Develop comparison of different results
        -merge histos
        -better boxplot

**Open Questions:**
  - How to discard matplotlib plots when line is not in insert?
  - Add statics per matplotlib?

## References

- [Feel++](https://docs.feelpp.org/home/index.html)
- [HiFiMagnet](https://github.com/feelpp/hifimagnet)
- [Paraview Python Scripting](https://docs.paraview.org/en/latest/Tutorials/SelfDirectedTutorial/batchPythonScripting.html)

---

## Deprecated Scripts

The following scripts are deprecated and kept for reference only. Use `python_hifimagnetParaview.cli` instead.

### `pv-statistics` (Deprecated)

* get range per PointData, CellData
* compute stats per PointData, CellData for insert
* compute histogram per PointData, CellData for insert
* display 3D view
* display 2D OrOz view for theta in 

All data file are saved in csv format for other use.

Optional
* `--views`: 
    * `--field`: select a field, by default get first PointData array
* `--stats`: 
    * compute stats per PointData, CellData per block (aka `feelpp` marker) 
* `--histos`: 
    * compute histogram per PointData, CellData per block (aka `feelpp` marker)
* `--plots`: 
    * `--z`: 
       * display 2D OxOy view for z in `args.z`
       * `--r`: display theta plot for r in `args.r` and z in `args.z`
    * `--save`: save plots  

**Examples:**
```bash
python statistics.py --help
python pv-statistics.py ../../HL-31/test/hybride-Bh27.7T-Bb9.15T-Bs9.05T_HPfixed_BPfree/bmap/np_32/thermo-electric.exports/Export.case
pvbatch pv-statistics.py ../../HL-31/test/hybride-Bh27.7T-Bb9.15T-Bs9.05T_HPfixed_BPfree/bmap/np_32/elasticity.exports/Export.case --z -0.15 -0.1 -0.05 0 0.05 0.1 0.15  --r 1.94e-2 2.52e-2 3.17e-2 
```

### `pv-statistics2D` (Deprecated)

* for 2D

**Examples:**
```bash
pvbatch pv-statistics2D.py M9Bitters_18MW_thmagel/M9Bi_18MW_elas_laplace_withoutTierod/gradH/Montgomery/Colebrook/np_1/cfpdes.exports/Export.case
```

All data file are saved in csv format for other use.

Optional
* `--views`: 
    * `--field`: select a field, by default get all PointData and CellData array
    * `--transparent`: make background transparent and fonts black
    * `--colormap`: use a given colormap 
* `--stats`: 
    * compute stats per PointData, CellData per block (aka `feelpp` marker) 
* `--histos`: 
    * compute histogram per PointData, CellData per block (aka `feelpp` marker)
* `--plots`: 
    * `--theta`: 
    * `--r`: 
    * `--save`: save plots  

### `pv-statisticsAxi` (Deprecated)

* for Axi

All data file are saved in csv format for other use.

Optional
* `--views`: 
    * `--field`: select a field, by default get all PointData and CellData array
    * `--transparent`: make background transparent and fonts black
    * `--colormap`: use a given colormap 
* `--stats`: 
    * compute stats per PointData, CellData per block (aka `feelpp` marker) 
* `--histos`: 
    * compute histogram per PointData, CellData per block (aka `feelpp` marker)
* `--plots`: 
    * `--z`: 
    * `--r`: 
    * `--save`: save plots  

**Examples:**
```bash
pvbatch pv-statisticsAxi.py M9Bitters_18MW_laplace/gradH/Montgomery/Colebrook/np_1/np_1/cfpdes.exports/Export.case
```

