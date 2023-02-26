import logging

import pandas as pd

from data_structures.matches import Matches
from logs import log

KwargsMD = dict[str, pd.DataFrame]


def _get_date_numbers_per_match(matches: Matches) -> pd.Series:

    """
    Maps team pair (home, away) to a list with all date numbers
    in which they faced each other in the tournament.
    """

    return (
        matches.df.reset_index("date number")
        .groupby(["id", "home", "away"], observed=True)["date number"]
        .agg(list)
    )


def _fill_date_numbers_per_match_per_id(
    date_numbers_per_match: pd.Series, max_match_count: pd.Series
) -> pd.Series:

    """
    Pad date numbers (with -1) until all lists for an id has the
    same number of matches.

    -----
    Example:
        Suppose for a given "id" we have:
            teamA x teamB -> [0, 2, 4]
            teamB X teamC -> [0, 1, 2, 3]
            teamC X teamA -> [1, 2]

        After
            teamA x teamB -> [0, 2, 4, -1]
            teamB X teamC -> [0, 1, 2, 3]
            teamC X teamA -> [1, 2, -1, -1]
    """

    # make max_match_count have the same index as matches_date_numbers
    desired_ids = date_numbers_per_match.index.get_level_values("id")
    expanded_max_match_count = max_match_count[desired_ids]

    correct_index_max_match_count = expanded_max_match_count.set_axis(
        date_numbers_per_match.index, axis="index"
    )

    # pad with negative ones
    padding_size = correct_index_max_match_count - date_numbers_per_match.apply(len)
    padding_negative_ones = padding_size.apply(lambda num: num * [-1])

    return date_numbers_per_match + padding_negative_ones


@log(logging.debug)
def get_kwargs_from_matches(matches: Matches) -> KwargsMD:

    """
    Creates an instance of MatchesDates containing, for each team pair (home, away),
    a list with all date numbers in which they faced each other in the tournament.

    For a tournament, all lists are padded with -1 until they have the same length.

    -----
    Parameters:

        matches: Matches
            Tournament matches for a given sport.

    ------
    Returns:

        Kwargs parameters to intiialize MatchesDates
            "series" -> pd.Series
                list with all date number two teams faced each other per tournament.
    """

    date_numbers_per_match = _get_date_numbers_per_match(matches)
    max_match_count_per_id = matches.home_vs_away_count_per_id.groupby("id").max()

    return {
        "series": _fill_date_numbers_per_match_per_id(
            date_numbers_per_match, max_match_count_per_id
        )
    }
