from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from data_structures.matches import Matches

from .create_permutation_schedule import get_kwargs_from_matches


@dataclass
class PermutationSchedule:

    """
    Pandas series mapping each id to its respective schedule: list of
    rounds that should be used to create its permutations.

    "Round" in this context is a tuple of matches in which each match
    contains two values that represent two different teams.

    Remark: Index is automatically sorted after initialization.

        series: pd.Series[
            index=[
                "id" -> "{current_name}@/{sport}/{country}/{name-year}/"
            ],
            columns=[
                "schedule" -> list[
                        tuple[
                            tuple[Team, Team]  # two teams (Match)
                        ]  # Round
                    ]
                Matches for a complete double round robin schedule
                big enough to 'fit' all real tournament matches.

                Matches in this context are tuples of integers
                representing indexes of a list with team names.
            ]
        ]
    """

    series: pd.Series

    def __post_init__(self) -> None:
        self.series = self.series.sort_index().rename("schedule")

    @classmethod
    def from_matches(cls, matches: Matches) -> PermutationSchedule:

        """
        Create an instance of PermutationSchedule based on single round-robin schedules.

        Remark: Resulting schedules are completely random.
        ----
        Parameters:

            matches: Matches
                Matches for all tournaments.

        """
        parameters = get_kwargs_from_matches(matches)
        return cls(**parameters)
