"""
Module containing functions and classes responsible for creating
permutations of all tournament's matches.

Permutations in this context follow a double round robin schedule
in an attempt to avoid schedules which would never happen in real life.

It is assumed that no (home, away) match occur in the same date number.
"""

from .permutation_matches import (
    PermutationMatches,
    convert_matches_to_permutation_matches,
)

__all__ = [
    "PermutationMatches",
    "PermutationMatchesBuilder",
    "create_matches_permutation_builder",
    "convert_matches_to_permutation_matches",
]
