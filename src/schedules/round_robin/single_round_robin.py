from __future__ import annotations

import random
from dataclasses import dataclass

from .create_single_round_robin import get_kwargs_from_num_teams
from .types import Round


@dataclass
class SingleRoundRobin:

    """
    Dataclass which saves the matches for a single round-robin
    tournament.

    Each match is represented by two integers in
    the interval [0, num_teams), that is, the index position for
    a list with team names.

    ----
    Parameters:

        num_teams: int
            Number of teams in the round-robin tournament

        schedule: list[tuple[tuple[int, int], ...]
            Single round-robin schedule in which rounds are
            tuple[match, ...] and each match is a tuple[int, int].
    """

    num_teams: int
    schedule: list[Round]

    @classmethod
    def from_num_teams(cls, num_teams: int) -> SingleRoundRobin:

        parameters = get_kwargs_from_num_teams(num_teams)
        return cls(**parameters)

    def get_full_schedule(self, num_schedules: int) -> list[Round]:

        """
        Concatenate num_schedules single-round-robin schedules together.

        Each additional round-robin schedule has its rounds shuffled.

        ----
        Example:
            -> Suppose that we have a RoundRobinSchedule with:
                num_teams = 4 \n
                schedule = [
                    ( ((1,2), (3,0)), ((1,0), (2,3)), ((2,0), (1,3)) ),
                ]

            -> Then full_schedule(num_schedules = 2) can produce something like:

                [
                                                # first double round-robin\n
                    ( ((1,0), (2,3)), ((1,2), (3,0)), ((2,0), (1,3)) ),\n
                                                # second double round-robin\n
                    ( ((2,0), (1,3)), ((1,0), (2,3)), ((1,2), (3,0)) ),
                ]

            -> Notice that the 1st single-round-robin rounds were shuffled,
            as were the 2nd's.
        """
        rounds: list[Round] = []

        for _ in range(num_schedules):
            schedule_copy = self.schedule.copy()
            random.shuffle(schedule_copy)

            rounds.extend(schedule_copy)

        return rounds
