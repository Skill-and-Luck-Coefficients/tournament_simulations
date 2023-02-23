import logging
import random

from logs import log

from .single_round_robin import Round, SingleRoundRobin

KwargsDRR = dict[str, int | SingleRoundRobin]


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
) -> KwargsDRR:

    first_rounds: list[Round] = random.sample(single.schedule, k=len(single.schedule))

    second_rounds = _create_rounds_second_portion(first_rounds)

    return {
        "num_teams": single.num_teams,
        "first_single_round_robin": single,
        "second_single_round_robin": SingleRoundRobin(single.num_teams, second_rounds),
    }


@log(logging.info)
def get_kwargs_from_num_teams(num_teams: int) -> KwargsDRR:

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

    single = SingleRoundRobin.from_num_teams(num_teams)

    return _create_double_round_robin_from_single(single)
