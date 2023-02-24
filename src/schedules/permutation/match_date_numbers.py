from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd

from data_structures.matches import Matches

from .create_match_date_numbers import get_kwargs_from_matches


@dataclass
class MatchDateNumbers:

    """
    Dataclass to store all date numbers which each pair (home, away) played in.

    series: pd.Series[
        index=[
            "id" -> "{current_name}@/{sport}/{country}/{name-year}/",\n
            "home"                -> str (home team name),\n
            "away"                -> str (away team name),\n
        ],\n
        columns=[
            "date number" -> list[int]
                Date number in which "home" faced "away".

                -1 is a sentinel value for a match that doesn't exist.
                More specifically, let X be

                    max_{home, away} number of matches between home and away

                Then, if two teams face each other Y < X times, the list will
                be padded with -1 until its total length is X.

                This is done so all X - Y (X minus Y) rounds in which these two
                teams don't face each other is randomized.
        ]
    """

    series: pd.Series

    @classmethod
    def from_matches(cls, matches: Matches) -> MatchDateNumbers:

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
