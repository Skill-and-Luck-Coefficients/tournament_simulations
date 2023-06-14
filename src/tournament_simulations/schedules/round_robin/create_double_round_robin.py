from typing import Callable, Iterable

from tournament_simulations.logs import log, tournament_simulations_logger

from ..utils.scheduling_types import Round, Team
from .single_round_robin import SingleRoundRobin

KwargsDRR = dict[str, int | list[Team] | list[Round]]


@log(tournament_simulations_logger.info)
def get_kwargs_from_num_teams(
    num_teams: int,
    scheduling_func: str | Callable[[int], list[Round]],
) -> KwargsDRR:

    """
    Create a double round-robin schedule for a tournament with num_teams teams.

    Second portion has the same rounds as the first one, but they are flipped:
        Each (home, away) match in the first portion will be (away, home) in the second.

    -----
    Parameters:

        num_teams: int
            Number of teams the schedule should consider.

        scheduling_func: str | Callable[[int], list[Round]] = "circle"

            Function responsible for creating a schedule.

            Some methods are implemented, so you can use strings to call them.
                Options: "circle".

            You can also provide a function.
                Input:
                    int
                        number of teams as a parameter.

                Output:
                    list[
                        tuple[  # Round
                            tuple[Team, Team],  # Match
                            ...
                        ]
                    ]
                        A tournament Schedule

    ------
    Returns:

        Kwargs parameters for DoubleRoundRobin:
            "num_teams": number of teams

            "team_names": team names

            "first_schedule": schedule for a single round-robin tournament.
    """

    single_rr = SingleRoundRobin.from_num_teams(num_teams, scheduling_func)

    return {
        "num_teams": single_rr.num_teams,
        "team_names": single_rr.team_names,
        "first_schedule": single_rr.schedule,
    }


@log(tournament_simulations_logger.info)
def get_kwargs_from_team_names(
    team_names: Iterable[Team],
    scheduling_func: str | Callable[[int], list[Round]],
) -> KwargsDRR:

    """
    Create a double round-robin schedule for a tournament with teams named "team_names".

    Second portion has the same rounds as the first one, but they are flipped:
        Each (home, away) match in the first portion will be (away, home) in the second.

    -----
    Parameters:

        team_names: list[Team]
            Team names.
                i-th team is represented by team_names[i].

        scheduling_func: str | Callable[[int], list[Round]] = "circle"

            Function responsible for creating a schedule.

            Some methods are implemented, so you can use strings to call them.
                Options: "circle".

            You can also provide a function.
                Input:
                    int
                        number of teams as a parameter.

                Output:
                    list[
                        tuple[  # Round
                            tuple[Team, Team],  # Match
                            ...
                        ]
                    ]
                        A tournament Schedule

    ------
    Returns:

        Kwargs parameters for DoubleRoundRobin:
            "num_teams": number of teams

            "team_names": team names

            "first_schedule": schedule for a single round-robin tournament.
    """
    single_rr = SingleRoundRobin.from_team_names(team_names, scheduling_func)

    return {
        "num_teams": single_rr.num_teams,
        "team_names": single_rr.team_names,
        "first_schedule": single_rr.schedule,
    }
