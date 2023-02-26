import logging
import random
from typing import Iterable

from logs import log

from .utils.rename_teams import rename_teams_in_rounds
from .utils.types import Round, Team

KwargsSRR = dict[str, int | list[Round]]


def _create_team_list(num_teams: int) -> list[int]:

    # need an additional team if it is an odd number
    if num_teams % 2 == 1:
        return list(range(-1, num_teams))

    return list(range(num_teams))


def _generate_round_matches(teams: list[int], matches_per_round: int) -> Round:

    return tuple((teams[i], teams[-i - 1]) for i in range(matches_per_round))


@log(logging.debug)
def _generate_schedule(teams: list[int]) -> list[Round]:

    matches_per_round = len(teams) // 2

    teams_copy = teams.copy()
    rounds: list[Round] = []

    # see https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method
    while True:

        round_: Round = _generate_round_matches(teams_copy, matches_per_round)

        # remove matches with the sentinel value -1
        # only happen if the number of teams is odd
        valid_round: Round = tuple(match for match in round_ if -1 not in match)

        rounds.append(valid_round)

        teams_copy.insert(1, teams_copy.pop())

        if teams_copy == teams:
            break

    return rounds


def _shuffle_home_away_in_matches(schedule: list[Round]) -> list[Round]:

    # shuffling is a good idea because otherwise some teams would be home too much
    # for example, the first team would be home all matches
    new_schedule: list[Round] = []

    for round_ in schedule:
        shuffled_home_away = tuple(tuple(random.sample(match, 2)) for match in round_)
        new_schedule.append(shuffled_home_away)

    return new_schedule


@log(logging.info)
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

    schedule = _generate_schedule(teams)
    shuffled_schedule = _shuffle_home_away_in_matches(schedule)

    return {
        "num_teams": num_teams,
        "schedule": random.sample(shuffled_schedule, k=len(shuffled_schedule)),
    }


@log(logging.info)
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
