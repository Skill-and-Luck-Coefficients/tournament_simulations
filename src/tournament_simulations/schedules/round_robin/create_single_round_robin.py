import random
from typing import Iterable

from tournament_simulations.logs import log, tournament_simulations_logger

from .circle_method import generate_schedule
from .utils.rename_teams import rename_teams_in_rounds
from .utils.types import Round, Team

KwargsSRR = dict[str, int | list[Round]]


def _create_team_list(num_teams: int) -> list[int]:

    # need an additional team if it is an odd number
    if num_teams % 2 == 1:
        return list(range(-1, num_teams))

    return list(range(num_teams))


def _shuffle_home_away_in_matches(schedule: list[Round]) -> list[Round]:

    # shuffling is a good idea because otherwise some teams would be home too much
    # for example, the first team would be home all matches
    new_schedule: list[Round] = []

    for round_ in schedule:
        shuffled_home_away = tuple(tuple(random.sample(match, 2)) for match in round_)
        new_schedule.append(shuffled_home_away)

    return new_schedule


@log(tournament_simulations_logger.info)
def get_kwargs_from_num_teams(
    num_teams: int,
    randomize_teams: bool,
) -> KwargsSRR:

    """
    Create a single round-robin schedule for a tournament with num_teams teams.

    -----
    Parameters:

        num_teams: int
            Number of teams the schedule should consider.

        randomize_teams: bool = True
            Whether or not teams should be randomized.

            If False, default ordering of the scheduling algorithm will be used.

        randomize_rounds: bool = True
            Whether or not the order of rounds in a schedule should be randomized.

            If False, default ordering of the scheduling algorithm will be used.

    ------
    Returns:

        Kwargs parameters for SingleRoundRobin:
            "num_teams": number of teams

            "schedule": schedule for a single round-robin tournament.
    """

    teams = _create_team_list(num_teams)

    if randomize_teams:
        random.shuffle(teams)

    schedule = generate_schedule(teams)
    shuffled_schedule = _shuffle_home_away_in_matches(schedule)

    return {
        "num_teams": num_teams,
        "schedule": random.sample(shuffled_schedule, k=len(shuffled_schedule)),
    }


@log(tournament_simulations_logger.info)
def get_kwargs_from_team_names(
    team_names: Iterable[Team],
    randomize_teams: bool,
) -> KwargsSRR:

    """
    Create a single round-robin schedule for a tournament with teams named "team_names".

    -----
    Parameters:

        team_names: list[Team]
            Team names.
                i-th team is represented by team_names[i].

        randomize_teams: bool = True
                Whether or not teams should be randomized.
                If False, default ordering of the scheduling algorithm will be used.

        randomize_rounds: bool = True
            Whether or not the order of rounds in a schedule should be randomized.
            If False, default ordering of the scheduling algorithm will be used.

    ------
    Returns:

        Kwargs parameters for SingleRoundRobin:
            "num_teams": number of teams
            "schedule": schedule for a single round-robin tournament.
    """

    params_teams_as_int = get_kwargs_from_num_teams(len(team_names), randomize_teams)

    schedule = params_teams_as_int["schedule"]
    schedule_generator = rename_teams_in_rounds(schedule, team_names)

    return {
        "num_teams": params_teams_as_int["num_teams"],
        "schedule": list(schedule_generator),
    }
