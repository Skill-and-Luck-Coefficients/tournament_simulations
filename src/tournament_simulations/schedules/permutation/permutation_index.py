from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .create_permutation_index import get_kwargs_from_schedule__date_number
from .match_date_numbers import MatchDateNumbers
from .permutation_schedule import PermutationSchedule
from .utils.types import MatchIndexWithTeams


@dataclass
class PermutationIndex:

    """
    Permuted tournaments index required to create MatchesPermutation.

    Remark: Index is automatically sorted after initialization.

        series: pd.Series[
            index=[
                "id"   -> pd.Categorical[str]
                    "{current_name}@/{sport}/{country}/{name-year}/",
            ],\n
            columns=[
                "index" -> list[
                    # tournament id, date number, home team, away team
                    tuple[Id, DateNumber, Team, Team],
                ]
                    List of indexes.
            ]

    """

    series: pd.Series

    def __post_init__(self) -> None:
        self.series = self.series.sort_index().rename("index")

    def to_flat_list(self) -> list[MatchIndexWithTeams]:
        """
        Returns a list aggregating all tournaments' indexes.
        """
        return self.series.explode(ignore_index=True).to_list()

    @classmethod
    def from_schedule__date_number(
        cls,
        permuatation_schedule: PermutationSchedule,
        match_date_numbers: MatchDateNumbers,
    ) -> PermutationIndex:

        parameters = get_kwargs_from_schedule__date_number(
            permuatation_schedule, match_date_numbers
        )
        return cls(**parameters)
