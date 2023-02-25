import logging
import random
from typing import Iterable

from logs import log

from .single_round_robin import SingleRoundRobin
from .utils.rename_teams import rename_teams_in_rounds
from .utils.types import Round, Team

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
        "first_schedule": first_rounds,
        "second_schedule": second_rounds,
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

        Kwargs parameters for DoubleRoundRobin:
            "num_teams": number of teams
            "first_schedule": schedule for a single round-robin tournament.
            "second_schedule": complementary schedule.
                (home, away) from the first round-robin are flipped to (away, home)
    """

    single = SingleRoundRobin.from_num_teams(num_teams)

    return _create_double_round_robin_from_single(single)


@log(logging.info)
def get_kwargs_from_team_names(
    team_names: Iterable[Team],
) -> KwargsDRR:

    """
    Create a single round-robin schedule for a tournament with num_teams teams.

    -----
    Parameters:

        team_names: list[Team]
            Team names.
                i-th team is represented by team_names[i].

    ------
    Returns:

        Kwargs parameters for DoubleRoundRobin:
            "num_teams": number of teams
            "first_schedule": schedule for a single round-robin tournament.
            "second_schedule": complementary schedule.
                (home, away) from the first round-robin are flipped to (away, home)
    """

    params_teams_as_int = get_kwargs_from_num_teams(len(team_names))

    first_schedule = params_teams_as_int["first_schedule"]
    first_schedule_generator = rename_teams_in_rounds(first_schedule, team_names)

    second_schedule = params_teams_as_int["second_schedule"]
    second_schedule_generator = rename_teams_in_rounds(second_schedule, team_names)

    return {
        "num_teams": params_teams_as_int["num_teams"],
        "first_schedule": list(first_schedule_generator),
        "second_schedule": list(second_schedule_generator),
    }
