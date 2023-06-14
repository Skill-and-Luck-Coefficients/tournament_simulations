from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

import pandas as pd

import tournament_simulations.utils.series_of_functions as sof

from .one_permutation import TournamentSchedule


@dataclass
class TournamentScheduler:

    """
    Class responsible for creating schedules for each tournament ("id") given
    scheduling functions and their parameters.

    func_schedule: Callable[[Any], Output] | Mapping
        Function that, given an input, returns a valid tournament schedule.

        Can also be dict-like mapping each tournament id to such a function.

    id_to_parameters: pd.Series
        Maps each tournament id to the parameters required by 'func_schedule'.

        Parameters should always be an Iterable, even if the function only
        takes one parameter.
            Iterable[0] -> first parameter
            Iterable[1] -> second parameter
            ...

        Remark: Index is automatically sorted after initialization.
    """

    func_schedule: Callable | Mapping[str, Callable]
    id_to_parameters: pd.Series

    def __post_init__(self) -> None:
        self.id_to_parameters = self.id_to_parameters.sort_index()

    def generate_schedule(self) -> TournamentSchedule:
        """
        Create a tournament schedule for each id given self.func_schedule
        and self.id_to_parameters.

        ----
        Retuns:
            TournamentSchedule
                Variable 'series'
                    Schedule for each tournament (pd.Series)
        """
        if isinstance(self.func_schedule, Callable):
            # .map uses all parameters as a single one, so we need to unpack it
            def _unpack_parameters(iterable):
                return self.func_schedule(*iterable)

            schedule = self.id_to_parameters.map(_unpack_parameters)
        else:
            schedule = sof.call_functions_with_their_parameters(
                key_to_func=self.func_schedule,
                key_to_func_parameters=self.id_to_parameters,
            )

        return TournamentSchedule(schedule.rename("schedule"))
