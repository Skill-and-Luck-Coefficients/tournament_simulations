import logging
from typing import Iterable

from logs import log

from .single_round_robin import SingleRoundRobin
from .utils.rename_teams import rename_teams_in_rounds
from .utils.types import Team

KwargsDRR = dict[str, int | SingleRoundRobin]


@log(logging.info)
def get_kwargs_from_num_teams(
    num_teams: int,
    randomize_teams: bool,
) -> KwargsDRR:

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

    single_rr = SingleRoundRobin.from_num_teams(num_teams, randomize_teams)

    return {
        "num_teams": single_rr.num_teams,
        "first_schedule": single_rr.schedule,
    }


@log(logging.info)
def get_kwargs_from_team_names(
    team_names: Iterable[Team],
    randomize_teams: bool,
) -> KwargsDRR:

    """
    Create a double round-robin schedule for a tournament with teams named "team_names".

    Second portion has the same rounds as the first one, but they are shuffled.

    Each (home, away) match in the first portion will be (away, home) in the second.

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

    params_teams_as_int = get_kwargs_from_num_teams(len(team_names), randomize_teams)

    first_schedule = params_teams_as_int["first_schedule"]
    first_schedule_generator = rename_teams_in_rounds(first_schedule, team_names)

    return {
        "num_teams": params_teams_as_int["num_teams"],
        "first_schedule": list(first_schedule_generator),
    }
