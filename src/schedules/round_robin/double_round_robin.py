from __future__ import annotations

import random
from dataclasses import dataclass

from .create_double_round_robin import get_kwargs_from_num_teams
from .single_round_robin import SingleRoundRobin
from .utils.types import Round


@dataclass
class DoubleRoundRobin:

    """
    Dataclass which saves the matches for a double round-robin
    tournament. Each match is represented by two integers in
    the interval [0, num_teams), that is, the index position for
    a list with team names.

    ----
    Parameters:

        num_teams: int
            Number of teams in the round-robin tournament

        <first,second>_schedule: list[Round]
            Two single round-robin schedules.

            Teams should face each other twice, once in the first (home vs away)
            and once in the second (away vs home).

    """

    num_teams: int
    first_schedule: list[Round]
    second_schedule: list[Round]

    @classmethod
    def from_num_teams(cls, num_teams: int) -> DoubleRoundRobin:

        parameters = get_kwargs_from_num_teams(num_teams)
        return cls(**parameters)

    def get_full_schedule(self, num_schedules: int) -> Iterator[Round]:

        """
        Concatenate num_schedules double-round-robin schedules together.
        Each additional round-robin schedule has its rounds shuffled.

        It returns a generator for the concatenation.
        ----
        Example:
            -> Suppose that we have a RoundRobinSchedule with:
                num_teams = 3 \n
                schedule = [
                    ( ((1,2), (3,0)), ((1,0), (2,3)), ((2,0), (1,3)) ),
                    ( ((0,1), (3,2)), ((2,1), (0,3)), ((0,2), (3,1)) ),
                ]

            -> Then list(full_schedule(num_schedules = 2)) can produce something like:

                [
                                                # first double round-robin\n
                    ( ((1,2), (3,0)), ((1,0), (2,3)), ((2,0), (1,3)) ),
                    ( ((0,1), (3,2)), ((2,1), (0,3)), ((0,2), (3,1)) ),
                                                # second double round-robin\n
                    ( ((2,0), (1,3)), ((1,0), (2,3)), ((1,2), (3,0)) ),
                    ( ((0,1), (3,2)), ((0,2), (3,1)), ((2,1), (0,3)) ),
                ]

            -> Notice that the 1st single-round-robin rounds were shuffled,
            as were the 2nd's.
        """

        for _ in range(num_schedules):

            first_schedule_copy = self.first_schedule.copy()
            random.shuffle(first_schedule_copy)
            yield from first_schedule_copy

            second_schedule_copy = self.second_schedule.copy()
            random.shuffle(second_schedule_copy)
            yield from second_schedule_copy
