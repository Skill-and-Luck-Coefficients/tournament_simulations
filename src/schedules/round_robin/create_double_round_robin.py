import logging
import random

from logs import log

from .create_single_round_robin import create_single_round_robin_from_num_teams
from .double_round_robin import DoubleRoundRobin
from .single_round_robin import Round, SingleRoundRobin


def _create_rounds_second_portion(rounds: list[Round]) -> list[Round]:

    """
    The section portion contains the same rounds as the first one, however:
        (1) the rounds are shuffled\n
        (2) match (teamA, teamB) becomes (teamB, teamA)
    """

    return [
        tuple((team_two, team_one) for team_one, team_two in matches)
        for matches in rounds
    ]


def _create_double_round_robin_from_single(
    single: SingleRoundRobin,
) -> DoubleRoundRobin:

    first_rounds: list[Round] = random.sample(single.schedule, k=len(single.schedule))

    second_rounds = _create_rounds_second_portion(first_rounds)

    return DoubleRoundRobin(
        single.num_teams,
        [single, SingleRoundRobin(single.num_teams, second_rounds)],
    )


@log(logging.info)
def create_double_round_robin_from_num_teams(num_teams: int) -> DoubleRoundRobin:

    """
    Create a double round-robin schedule for a tournament with num_teams teams.

    Second portion has the same rounds as the first one, but they are shuffled.
    Each (home, away) match in the first portion will be (away, home) in the second.

    -----
    Parameters:

        num_teams: int
            Number of teams the schedule should consider.

    ------
    Returns:

        DoubleRoundRobin:
            Schedule for a double round-robin tournament where each team
            is represented by an integer.

    """

    single = create_single_round_robin_from_num_teams(num_teams)

    return _create_double_round_robin_from_single(single)