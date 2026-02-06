# python_hifimagnetParaview/__init__.py
"""HiFiMagnet ParaView post-processing tools."""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # For Python < 3.8
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("python-hifimagnetParaview")
except PackageNotFoundError:
    # Package is not installed, fallback to reading pyproject.toml
    __version__ = "unknown"

__author__ = "Christophe Trophime"
__email__ = "christophe.trophime@lncmi.cnrs.fr"

# python_hifimagnetParaview/case2D/__init__.py
"""2D geometry post-processing modules."""

# python_hifimagnetParaview/case3D/__init__.py
"""3D geometry post-processing modules."""

# python_hifimagnetParaview/caseAxi/__init__.py
"""Axisymmetric geometry post-processing modules."""
