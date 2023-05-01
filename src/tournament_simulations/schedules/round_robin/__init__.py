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

from .create_single_round_robin import generate_schedule
from .double_round_robin import DoubleRoundRobin
from .single_round_robin import SingleRoundRobin
from .utils.convert_rounds_to_dataframe import convert_list_of_rounds_to_dataframe
from .utils.rename_teams import rename_teams_in_rounds

__all__ = [
    "generate_schedule",
    "DoubleRoundRobin",
    "SingleRoundRobin",
    "convert_list_of_rounds_to_dataframe",
    "rename_teams_in_rounds",
]
