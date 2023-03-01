import logging

import pandas as pd

from tournament_simulations.data_structures.matches import DateNumber, Matches
from tournament_simulations.logs import log

from .match_date_numbers import MatchDateNumbers
from .permutation_index import PermutationIndex
from .permutation_schedule import PermutationSchedule
from .utils.types import MatchIndexWithTeams


def _set_original_date_numbers_back(
    permuted_matches: pd.DataFrame, original_date_numbers: list[DateNumber]
) -> pd.DataFrame:

    new_matches = permuted_matches.sort_index(level="id", sort_remaining=False)
    new_matches = new_matches.reset_index("date number")

    new_matches["date number"] = original_date_numbers

    return new_matches.set_index("date number", append=True)


def _get_tournament_matches_from_indexes(
    matches_df: pd.DataFrame, indexes: list[MatchIndexWithTeams]
) -> pd.DataFrame:

    # need to set ["home", "away"] to index since the indexes depend on it
    matches_teams_in_index = matches_df.set_index(["home", "away"], append=True)
    desired_matches = matches_teams_in_index.loc[indexes]

    return desired_matches.reset_index(["home", "away"])


def _select_matches_in_the_desired_order(
    matches: Matches,
    permutation_schedule: PermutationSchedule,
    matches_date_numbers: MatchDateNumbers,
) -> Matches:

    """
    Creates a new schedule to all tournaments by properly indexing 'matches'
    in the desired order: it is infered from 'matches_date_numbers' and
    'permutation_schedule'.

        permutation_schedule:
            Tournament orderings from double round-robin schedules.

        matches_date_numbers:
            Ordering of matches that occur more than once.

            If a match (home, away) happened more than once, the round
            in which each instance ends up will be randomized.

    Remark: This is a deterministic procedure, so 'matches_date_numbers'
            and 'permutations_schedules' must already be randomized.
    -----
    Parameters:

        matches: Matches
            Tournament matches.

        permutation_schedule: PermutationSchedule
            Maps each tournament to a single/double round-robin schedule.

        matches_dates: MatchDateNumbers
            Maps teams (home and away) to padded date number in
            which they faced each other.

            Padded means that single round-robin schedules in which
            they didn't face it other will be filled with -1.
    -----
    Returns:
        Matches:
            Permutation for all tournaments inside matches.

            It will mantain the same "date numbers" as the
            initial tournament, but the matches that happen in
            each date will be different.
    """
    ordered_index = (
        PermutationIndex.from_schedule__date_number(  # infering desired order
            permutation_schedule, matches_date_numbers
        )
    )

    flat_index = ordered_index.to_flat_list()
    new_matches_df = _get_tournament_matches_from_indexes(matches.df, flat_index)

    date_numbers = matches.df.index.get_level_values("date number")
    new_matches_df = _set_original_date_numbers_back(new_matches_df, date_numbers)

    return Matches(new_matches_df)


@log(logging.info)
def create_one_permutation(
    matches: Matches,
    matches_date_numbers: MatchDateNumbers,
) -> Matches:

    """
    Create a permutation for all tournaments.

    -----
    Parameters:

        matches: Matches
            Tournament matches.

        matches_dates: MatchDateNumbers
            Maps teams (home and away) to padded date number in
            which they faced each other.

            Padded means that single round-robin schedules in which
            they didn't face it other will be filled with -1.
    -----
    Returns:
        Matches:
            Permutation for all tournaments inside matches.
    """

    # randomizing team names (permutation_schedule) and date numbers
    permutation_schedule = PermutationSchedule.from_matches(matches)
    suffled_matches_dates = matches_date_numbers.create_shuffled_copy()

    return _select_matches_in_the_desired_order(
        matches,
        permutation_schedule,
        suffled_matches_dates,
    )
