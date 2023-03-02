from typing import Iterator

import pandas as pd

import tournament_simulations.schedules.round_robin as rr
from tournament_simulations.data_structures.matches import Matches
from tournament_simulations.logs import log, tournament_simulations_logger
from tournament_simulations.utils.convert_df_to_series import (
    convert_df_to_series_of_tuples,
)

KwargsPS = dict[str, pd.Series]


def _get_schedule_creator_per_id(id_to_team_names: pd.Series) -> pd.Series:

    return id_to_team_names.apply(rr.DoubleRoundRobin.from_team_names).sort_index()


def _create_schedule_per_id(id_to_schedule__max_count: pd.Series) -> pd.Series:

    # apply function
    def _create_schedule_one_id(
        schedule__max_match_count: tuple[rr.DoubleRoundRobin, int]
    ) -> Iterator[rr.utils.Round]:

        schedule, num_schedules = schedule__max_match_count
        return schedule.get_full_schedule(num_schedules)

    return (
        id_to_schedule__max_count.apply(_create_schedule_one_id)
        .sort_index()
        .rename("schedule")
    )


def _get_kwargs(
    id_to_team_names: pd.Series,
    id_to_max_match_count: pd.Series,
) -> KwargsPS:

    """
    Returns necessary parameters to initialize PermutationSchedule.
        PermutationSchedules:
            Iterators for each tournament's schedule - list of rounds
            with number as teams.

    ----
    Parameters:

        id_to_team_names: pd.Series
            Series mapping each tournament id to its teams.

        id_to_max_match_count: pd.Series
            Number of double round robin schedule to encompass all matches
            for each tournament.

            For a given tournament, this is maximum number of times teams
            faced each other over all possible team pairs (home, away).
    -----
    Returns:

        Kwargs parameter to initialize PermutationSchedule:
            "series" -> pd.Series
                Schedule for each tournament.
    """

    id_to_schedule_creator = _get_schedule_creator_per_id(id_to_team_names)

    concat_series = pd.concat([id_to_schedule_creator, id_to_max_match_count], axis=1)
    id_to_schedule__match_count = convert_df_to_series_of_tuples(concat_series)

    return {"series": _create_schedule_per_id(id_to_schedule__match_count)}


@log(tournament_simulations_logger.info)
def get_kwargs_from_matches(matches: Matches) -> KwargsPS:
    """
    Returns necessary parameters to initialize PermutationSchedule.
        PermutationSchedules:
            Iterators for each tournament's schedule - list of rounds
            with number as teams.

    ----
    Parameters:

        matches: Matches
            Matches for all tournaments.

    -----
    Returns:

        Kwargs parameter to initialize PermutationSchedule:
            "series" -> pd.Series
                Schedule for each tournament.
    """

    return _get_kwargs(
        matches.team_names_per_id,
        matches.home_vs_away_count_per_id.groupby("id", observed=True).max(),
    )
