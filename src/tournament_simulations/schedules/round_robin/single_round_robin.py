from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, Iterator

from . import create_single_round_robin as create
from .utils.types import Round, Team


@dataclass
class SingleRoundRobin:

    """
    Dataclass which saves the matches for a single round-robin
    tournament.

    ----
    Parameters:

        num_teams: int
            Number of teams in the round-robin tournament

        schedule: list[tuple[tuple[Team, Team], ...]
            Single round-robin schedule in which:
                1) Rounds are tuple[Match, ...]

                2) Match is a tuple[Team, Team]

                3) Team can be int, str or something else.
    """

    num_teams: int
    schedule: list[Round]

    @classmethod
    def from_num_teams(
        cls, num_teams: int, randomize_teams: bool = True
    ) -> SingleRoundRobin:

        """
        In this case, teams will be integers.

        You can think of it as the the index position for
        a list with team names.

        -----
        Parameters:
            num_teams: int
                Number of teams

            randomize_teams: bool = True
                Whether or not teams should be randomized.

                If False, default ordering of the scheduling algorithm will be used.

        -----
        Remark:
            There will always be some randomness:
                1) Round ordering is shuffled in the schedule.

                2) In-match team ordering (who is home and who is away) is also random.
        """
        parameters = create.get_kwargs_from_num_teams(num_teams, randomize_teams)
        return cls(**parameters)

    @classmethod
    def from_team_names(
        cls,
        team_names: Iterable[Team],
        randomize_teams: bool = True,
    ) -> SingleRoundRobin:

        """
        In this case, a team will be whatever was passed as its name.
            i-th team will be represented by team_names[i]

        -----
        Parameters:
            team_names: Iterable[Team]
                Data that represents teams.

            randomize_teams: bool = True
                Whether or not teams should be randomized.
                If False, default ordering of the scheduling algorithm will be used.

        -----
        Remark:
            There will always be some randomness:
                1) Round ordering is shuffled in the schedule.

                2) In-match team ordering (who is home and who is away) is also random.
        """
        parameters = create.get_kwargs_from_team_names(team_names, randomize_teams)
        return cls(**parameters)

    def get_full_schedule(
        self, num_schedules: int, randomize_rounds: bool = True
    ) -> Iterator[Round]:

        """
        Concatenate num_schedules single-round-robin schedules together.

        ----
        Parameters:

            num_schedules: int
                Number of times schedule should be concatenated.

            randomize_rounds: bool = True
                If True, order of rounds will be randomized in each schedule.

        ----
        Returns:
            Iterator[Round]
                Generator for the entire schedule.

        ----
        Example:
            -> Suppose that we have a RoundRobinSchedule with:
                num_teams = 4 \n
                schedule = [
                    ( ((1,2), (3,0)), ((1,0), (2,3)), ((2,0), (1,3)) ),
                ]

            -> Then list(full_schedule(num_schedules = 2)) can produce something like:

                [
                                                # first single round-robin\n
                    ( ((1,0), (2,3)), ((1,2), (3,0)), ((2,0), (1,3)) ),\n
                                                # second single round-robin\n
                    ( ((2,0), (1,3)), ((1,0), (2,3)), ((1,2), (3,0)) ),
                ]

            -> Notice that the 1st single-round-robin rounds were shuffled,
            as were the 2nd's.
        """
        for _ in range(num_schedules):

            copy_schedule = self.schedule.copy()

            if randomize_rounds:
                random.shuffle(copy_schedule)

            yield from copy_schedule
