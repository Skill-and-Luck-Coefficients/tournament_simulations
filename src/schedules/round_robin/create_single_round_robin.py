import logging
import random

from logs import log

from .single_round_robin import Round, SingleRoundRobin


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
def create_single_round_robin_from_num_teams(num_teams: int) -> SingleRoundRobin:

    """
    Create a single round-robin schedule for a tournament with num_teams teams.

    -----
    Parameters:

        num_teams: int
            Number of teams the schedule should consider.

    ------
    Returns:

        SingleRoundRobin:
            Schedule for a single round-robin tournament where each team
            is represented by an integer.

    """

    teams = _create_team_list(num_teams)

    schedule = _generate_schedule(teams)
    shuffled_schedule = _shuffle_home_away_in_matches(schedule)

    return SingleRoundRobin(num_teams, shuffled_schedule)
