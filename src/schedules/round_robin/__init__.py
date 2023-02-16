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

from .convert_rounds_to_dataframe import convert_list_of_rounds_to_dataframe
from .create_double_round_robin import create_double_round_robin_from_num_teams
from .create_single_round_robin import create_single_round_robin_from_num_teams
from .double_round_robin import DoubleRoundRobin
from .single_round_robin import Round, SingleRoundRobin

__all__ = [
    "convert_list_of_rounds_to_dataframe",
    "create_double_round_robin_from_num_teams",
    "create_single_round_robin_from_num_teams",
    "DoubleRoundRobin",
    "Round",
    "SingleRoundRobin",
]
