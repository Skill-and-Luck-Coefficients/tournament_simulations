"""
Module responsible for creating schedules for round-robin tournaments.

    SingleRoundRobin:
        If each team must only face each other once.

        Schedule is a list of rounds with its matches being
        tuple[int, int]. Each int value represents a team.

    DoubleRoundRobin:
        If each team must face each other as home team and as away.

        <first,second>_single_round_robin are each a SingleRoundRobin.
"""

from . import utils
from .double_round_robin import DoubleRoundRobin
from .single_round_robin import SingleRoundRobin

__all__ = [
    "utils",
    "DoubleRoundRobin",
    "SingleRoundRobin",
]
