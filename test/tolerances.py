"""
Tolerance Configuration for Test Suite

This module defines standardized tolerance values for validating
computational results across different geometry types (2D, 3D, Axi).

RATIONALE:
- Temperature: 0.1% for 2D/Axi, 1% for 3D due to numerical precision differences
  in 3D calculations. The looser 3D tolerance accounts for additional complexity
  in 3D mesh interpolation and integration.

- VonMises: 1% for all geometry types due to derived nature of the stress
  calculation (involves derivatives and tensor operations).

- Image comparison: 0.1% for all types to ensure visual consistency.

USAGE:
    from test.tolerances import TOLERANCES
    
    tolerance = TOLERANCES["temperature"]["2D"]["relative"]
    assert abs(1 - measured/expected) < tolerance
"""

TOLERANCES = {
    # Temperature field tolerances
    "temperature": {
        "2D": {
            "relative": 0.001,  # 0.1%
            "description": "Standard precision for 2D thermal calculations"
        },
        "3D": {
            "relative": 0.01,   # 1% - Looser due to 3D interpolation complexity
            "description": "Relaxed tolerance for 3D thermal calculations"
        },
        "Axi": {
            "relative": 0.001,  # 0.1%
            "description": "Standard precision for axisymmetric thermal calculations"
        }
    },
    
    # VonMises stress tolerances
    "vonmises": {
        "2D": {
            "relative": 0.01,   # 1%
            "description": "Standard tolerance for derived stress calculations"
        },
        "3D": {
            "relative": 0.01,   # 1%
            "description": "Standard tolerance for derived stress calculations"
        },
        "Axi": {
            "relative": 0.01,   # 1%
            "description": "Standard tolerance for derived stress calculations"
        }
    },
    
    # Image comparison tolerances
    "image": {
        "2D": {
            "relative": 0.001,  # 0.1%
            "description": "Visual consistency check"
        },
        "3D": {
            "relative": 0.001,  # 0.1%
            "description": "Visual consistency check"
        },
        "Axi": {
            "relative": 0.001,  # 0.1%
            "description": "Visual consistency check"
        }
    }
}


def get_tolerance(field_type, geometry_type, tolerance_type="relative"):
    """
    Get tolerance value for a specific field and geometry type.
    
    Args:
        field_type: One of "temperature", "vonmises", "image"
        geometry_type: One of "2D", "3D", "Axi"
        tolerance_type: "relative" or "description"
        
    Returns:
        Tolerance value or description string
        
    Raises:
        KeyError: If field_type or geometry_type is invalid
    """
    return TOLERANCES[field_type][geometry_type][tolerance_type]
