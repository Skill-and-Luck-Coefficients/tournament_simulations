from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class TournamentSchedule:
    """
    Pandas series mapping each id to its respective schedule: list of
    rounds that should be used to create its schedule.

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
                Schedule big enough for a complete tournament schedule, i.e.,
                it contain (at least) all possible real tournament matches.

                Matches in this context are tuples of integers
                representing indexes of a list with team names.
            ]
        ]
    """
    series: pd.Series

    def __post_init__(self) -> None:
        self.series = self.series.sort_index()
