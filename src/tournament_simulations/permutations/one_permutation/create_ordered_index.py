from typing import Iterator

import pandas as pd

from tournament_simulations.data_structures.matches import Id
from tournament_simulations.logs import log, tournament_simulations_logger
from tournament_simulations.schedules import Round

from ..utils.types import MatchIndexWithTeams
from .match_date_numbers import MatchDateNumbers
from .tournament_schedule import TournamentSchedule

KwargsPI = dict[str, pd.Series]


def _generate_all_indexes_one_id(
    rounds: Iterator[Round], dates_numbers: pd.Series, id_: Id
) -> list[MatchIndexWithTeams]:

    # date_number is a mapping of (home, away) pairs to lists
    # containing all date numbers they faced each other in
    real_matches = set(dates_numbers.index)

    list_ = []

    for round in rounds:
        for home_away in round:

            if home_away not in real_matches:
                continue

            date_number = dates_numbers[home_away].pop()
            if date_number == -1:  # -1 is padding number
                continue

            list_.append((id_, date_number) + home_away)

    return list_


def _generate_matches_permutation_index_one_id(
    schedule: pd.Series, id_to_matches_dates: pd.Series
) -> list[MatchIndexWithTeams]:

    id_: Id = schedule.name
    rounds: Iterator[Round] = schedule["schedule"]
    dates_numbers: pd.Series = id_to_matches_dates.loc[id_]

    return _generate_all_indexes_one_id(rounds, dates_numbers, id_)


def _get_kwargs(
    id_to_permutation_schedule: pd.Series,
    id_to_matches_dates: pd.Series,
) -> dict[str, pd.Series]:

    return {
        "series": id_to_permutation_schedule.to_frame("schedule")
        .apply(
            _generate_matches_permutation_index_one_id,
            axis=1,
            id_to_matches_dates=id_to_matches_dates,
        )
        .sort_index()
    }


@log(tournament_simulations_logger.debug)
def get_kwargs_from_schedule__date_number(
    permuatation_schedule: TournamentSchedule,
    match_date_numbers: MatchDateNumbers,
) -> KwargsPI:

    return _get_kwargs(permuatation_schedule.series, match_date_numbers.series)
