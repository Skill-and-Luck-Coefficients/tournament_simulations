from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd

from tournament_simulations.data_structures.matches import Matches

from .create_match_date_numbers import get_kwargs_from_matches


@dataclass
class MatchDateNumbers:

    """
    Dataclass to store all date numbers which each pair (home, away) played in.

    Remark: Index is automatically sorted after initialization.

        series: pd.Series[
            index=[
                "id"   -> pd.Categorical[str]
                    "{current_name}@/{sport}/{country}/{name-year}/",
                "home" -> pd.Categorical[str] (home team name),\n
                "away" -> pd.Categorical[str] (away team name),\n
            ],\n
            columns=[
                "date number" -> list[int]
                    List of date numbers in which "home" faced "away".

                    The list is padded by -1 until all (home, away) pairs in a
                    tournament have equal-length lists.

                    More specifically, let X be

                        max number of matches over all (home, away) pairs

                    Then, if two teams face each other Y < X times, the list will
                    be padded with -1 until its total length is X.

                    This is done so all X - Y (X minus Y) rounds these two
                    teams don't face each other are randomized.
            ]
        ]
    """

    series: pd.Series

    def __post_init__(self) -> None:
        self.series = self.series.sort_index().rename("date number")

    @classmethod
    def from_matches(cls, matches: Matches) -> MatchDateNumbers:

        """
        Create an instance of MatchDateNumbers from matches.

        ----
        Parameters:

            matches: Matches
                Matches for all tournaments.
        """
        parameters = get_kwargs_from_matches(matches)
        return cls(**parameters)

    def create_shuffled_copy(self) -> MatchDateNumbers:
        """
        Create a matches dates copy in which all date numbers lists have been shuffled.
        """
        # apply func
        def _sample_dates(list_):
            return random.sample(list_, k=len(list_))

        return MatchDateNumbers(self.series.apply(_sample_dates))
