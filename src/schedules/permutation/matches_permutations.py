from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from data_structures.matches import Matches

from .match_date_numbers import MatchDateNumbers
from .matches_permutation import create_one_permutation


@dataclass
class MatchesPermutations:

    """
    Subclass of matches which creates permuted tournaments.

    -----
    Parameters:

        matches: Matches
            Tournament matches.

            Make sure that all necessary information is there:
                "id", "date number", "home" and "away".
    """

    matches: Matches

    def create_n_permutations(self, n: int) -> Matches:

        """
        Create n permutations of all tournaments.

        Remark: There can't be a (home, away) pair happening
        more than once in the same day for a tournament.
            It is ok for (home, away) and (away, home) to occur
            in the same day though.

        ----
        Parameters:

            n: int
                Number of permutations
        ----
        Returns:

            Matches
                Permuted matches.

                If the original tournament in self.df has id "{id}",
                then its i-th permutation will be called "{id}@{i}"

                df: pd.DataFrame[
                    index=[
                        "id"          -> pd.Categorical[str]
                            "{current_name}@/{sport}/{country}/{name-year}/@{num_permutation}",\n
                        "date number" -> int,
                    ],\n
                    columns=[
                        "home"                -> pd.Categorical[str] (home team name),\n
                        "away"                -> pd.Categorical[str] (away team name),\n
                        "result"              -> "{home score}:{away score}",\n
                        "winner"              -> Literal["h", "d", "a"]
                            "h" -> home\n
                            "d" -> draw\n
                            "a" -> away
                        "date"                -> "{day}.{month}.{year}",\n
                        "odds home"           -> np.float16,\n
                        "odds tie (optional)" -> np.float16,\n
                        "odds away"           -> np.float16,\n
                    ]
                ]
        """
        permutations: list[pd.DataFrame] = []

        matches_date_numbers = MatchDateNumbers.from_matches(self.matches)

        for i in range(n):

            permuted = create_one_permutation(self.matches, matches_date_numbers)

            renamed_df = permuted.df.rename(index=lambda id_: f"{id_}@{i}", level="id")
            permutations.append(renamed_df)

        return Matches(pd.concat(permutations))
