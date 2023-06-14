from dataclasses import dataclass
from typing import Sequence

import pandas as pd

from tournament_simulations.data_structures.matches import DateNumber, Matches
from tournament_simulations.logs import log, tournament_simulations_logger

from .ordered_index import OrderedIndex
from .utils.types import MatchIndexWithTeams


def _index_matches_appropriately(
    matches_df: pd.DataFrame, indexes: list[MatchIndexWithTeams]
) -> pd.DataFrame:

    # need to set ["home", "away"] to index since the indexes depend on it
    matches_teams_in_index = matches_df.set_index(["home", "away"], append=True)
    desired_matches = matches_teams_in_index.loc[indexes]

    return desired_matches.reset_index(["home", "away"])


def _set_date_numbers(
    permuted_matches: pd.DataFrame, date_numbers: list[DateNumber]
) -> pd.DataFrame:

    new_matches = permuted_matches.sort_index(level="id", sort_remaining=False)
    new_matches = new_matches.reset_index("date number")

    new_matches["date number"] = date_numbers

    return new_matches.set_index("date number", append=True)


@dataclass
class PermuteMatches:

    matches: Matches

    @log(tournament_simulations_logger.info)
    def permute_matches(
        self,
        ordered_index: OrderedIndex,
        date_numbers: Sequence[int] | pd.Series | None = None,
    ) -> Matches:

        """
        Creates a new schedule to all tournaments by properly indexing 'matches'
        in the desired order.
        -----
        Parameters:

            ordered_index: OrderedIndex
                Desired order for new tournament.

            date_numbers: Sequence[int] | pd.Series | None = None
                If None, "date number" index from self.matches will be used for
                the new tournament.

                If a valid sequence is passed, then it will be used instead.

        -----
        Returns:
            Matches:
                Permutation for all tournaments inside matches.

                It will mantain the same "date numbers" as the
                initial tournament, but the matches that happen in
                each date will be different.
        """
        flat_index = ordered_index.to_flat_list()
        new_matches_df = _index_matches_appropriately(self.matches.df, flat_index)

        if date_numbers is None:
            date_numbers = self.matches.df.index.get_level_values("date number")
        new_matches_df = _set_date_numbers(new_matches_df, list(date_numbers))

        return Matches(new_matches_df)
