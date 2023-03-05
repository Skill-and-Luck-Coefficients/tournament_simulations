"""
Data Structures for this directory.

Most of them are wrappers around pd.DataFrame explaining
what indexes and columns represent.
    This is useful for clarity and type hinting.

For specific information about a data structure, read its respective
"__init__.py" file or its class documentation.
"""

from .matches import Matches
from .points_per_match import PointsPerMatch

__all__ = ["Matches", "PointsPerMatch"]
