from typing import Callable, Iterable

from tournament_simulations.logs import log, tournament_simulations_logger

from ..algorithms import name_to_scheduling_func
from ..utils.rename_teams import rename_teams_in_rounds
from ..utils.scheduling_types import Round, Team

KwargsSRR = dict[str, int | list[Team] | list[Round]]


@log(tournament_simulations_logger.info)
def get_kwargs_from_num_teams(
    num_teams: int,
    scheduling_func: str | Callable[[int], list[Round]],
) -> KwargsSRR:

    """
    Create a single round-robin schedule for a tournament with num_teams teams.

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

        Kwargs parameters for SingleRoundRobin:
            "num_teams": number of teams

            "team_names": team names

            "schedule": schedule for a single round-robin tournament.
    """
    if isinstance(scheduling_func, str):
        scheduling_func = name_to_scheduling_func[scheduling_func]

    return {
        "num_teams": num_teams,
        "team_names": list(range(num_teams)),
        "schedule": scheduling_func(num_teams),
    }


@log(tournament_simulations_logger.info)
def get_kwargs_from_team_names(
    team_names: Iterable[Team],
    scheduling_func: str | Callable[[int], list[Round]],
) -> KwargsSRR:

    """
    Create a single round-robin schedule for a tournament with teams named "team_names".

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

        Kwargs parameters for SingleRoundRobin:
            "num_teams": number of teams

            "team_names": team names

            "schedule": schedule for a single round-robin tournament.
    """

    params_teams_as_int = get_kwargs_from_num_teams(len(team_names), scheduling_func)

    schedule = params_teams_as_int["schedule"]
    schedule_generator = rename_teams_in_rounds(schedule, team_names)

    return {
        "num_teams": params_teams_as_int["num_teams"],
        "team_names": list(team_names),
        "schedule": list(schedule_generator),
    }
