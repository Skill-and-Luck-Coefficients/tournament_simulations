"""
Module containing functions and classes responsible for creating
permutations of all tournament's matches.

Permutations in this context follow either a double round-robin schedule
in an attempt to avoid match sequences which would never happen in real life.

It is assumed that no (home, away) match occur in the same date number.
"""

from .matches_permutations import MatchesPermutations

__all__ = ["MatchesPermutations"]
