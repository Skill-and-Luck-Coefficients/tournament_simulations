import random
from typing import Sequence

from ..utils.rename_teams import rename_teams_in_rounds
from ..utils.scheduling_types import Match, Round, Team


def shuffle_home_away_in_matches(schedule: list[Round]) -> list[Round]:
    """
    Shuffle all (home, away) matches.
    Each match can either stay as (home, away) or turn into (away, home).

    It does not shuffle inplace, a new list will be returned.
    """
    def _shuffle_match(match: Match) -> Match:
        return tuple(random.sample(match, 2))

    # shuffling is a good idea because otherwise some teams could be home too much
    # for example, the first team would be home all matches
    return [
        tuple(_shuffle_match(match) for match in round_)
        for round_ in schedule
    ]


def shuffle_matches_in_rounds(schedule: list[Round]) -> list[Round]:
    """
    Given a single round-robin schedule, shuffle matches in all rounds.

    It does not shuffle inplace, a new list will be returned.
    """
    return [
        tuple(random.sample(round_, k=len(round_)))
        for round_ in schedule
    ]


def shuffle_rounds_in_schedule(schedule: list[Round]) -> list[Round]:
    """
    Given a single round-robin schedule, shuffle its rounds.

    It does not shuffle inplace, a new list will be returned.
    """
    return random.sample(schedule, k=len(schedule))


def _get_names_from_schedule(schedule: list[Round]) -> list[Team]:
    flat_schedule = (team for round_ in schedule for match in round_ for team in match)
    return sorted(set(flat_schedule))


def shuffle_teams(
    schedule: list[Round], team_names: Sequence[Team] | None = None
) -> list[Round]:
    """
    Shuffle all team names in matches.

    If 'team_names' is None, they will be infered from 'schedule'.

    It does not shuffle inplace, a new list will be returned.
    """
    if team_names is None:
        team_names = _get_names_from_schedule(schedule)

    shuffled_names = random.sample(team_names, k=len(team_names))

    old_team_to_new = dict(zip(team_names, shuffled_names))
    return list(rename_teams_in_rounds(schedule, old_team_to_new))
