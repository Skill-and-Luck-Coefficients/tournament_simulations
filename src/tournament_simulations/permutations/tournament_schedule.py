from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, TypeVar

import pandas as pd

import tournament_simulations.utils.series_of_functions as sof
from tournament_simulations.schedules import Round

InputT = TypeVar("InputT")
SchedulingFunc = Callable[[InputT], list[Round]]


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
        self.series = self.series.sort_index().rename("schedule")

    @classmethod
    def from_functions(
        cls,
        func_schedule: SchedulingFunc | Mapping[str, SchedulingFunc],
        id_to_parameters: pd.Series,
    ) -> TournamentSchedule:

        """
        Create an instance of TournamentSchedule based on scheduling functions.

        ----
        Parameters:

            func_schedule: Callable[[...], list[tuple[tuple[T, T]]]] | Mapping
                Function that, given an input, returns a valid tournament schedule.

                Can also be dict-like mapping each tournament id to such a function.

            id_to_parameters: pd.Series
                Maps each tournament id to the parameters required by 'func_schedule'.

                Parameters should always be an Iterable, even if the function only
                takes one parameter.
                    Iterable[0] -> first parameter
                    Iterable[1] -> second parameter
                    ...
        """

        if isinstance(func_schedule, Callable):
            # .map takes each value as parameter, so we need to unpack it
            schedule = id_to_parameters.map(lambda iterable: func_schedule(*iterable))
        else:
            schedule = sof.call_functions_with_their_parameters(
                key_to_func=func_schedule,
                key_to_func_parameters=id_to_parameters,
            )

        return cls(schedule.rename("schedule"))
