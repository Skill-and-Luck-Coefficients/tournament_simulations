from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, Iterator

from . import create_double_round_robin as create
from .utils.flip_home_away import flip_home_away_in_schedule
from .utils.types import Round, Team


@dataclass
class DoubleRoundRobin:

    """
    Dataclass which saves the matches for a double round-robin
    tournament.

    ----
    Parameters:

        num_teams: int
            Number of teams in the round-robin tournament

        first_schedule: list[Round]
            Single round-robin schedule in which:
                1) Rounds are tuple[Match, ...]

                2) Match is a tuple[Team, Team]

                3) Team can be int, str or something else.

    ----
    Variables automatically initiated:

        second_schedule: list[Round]
            Same as first_schedule but in-match order is flipped, that is,
            a (home, away) in the first_schedule turns into (away, home).

    """

    num_teams: int
    first_schedule: list[Round]

    def __post_init__(self) -> None:
        self.second_schedule = flip_home_away_in_schedule(self.first_schedule)

    @classmethod
    def from_num_teams(
        cls, num_teams: int, randomize_teams: bool = True
    ) -> DoubleRoundRobin:

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
    ) -> DoubleRoundRobin:

        """
        In this case, a team will be whatever was passed as its name.
            i-th team will be represented by team_names[i]

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
        parameters = create.get_kwargs_from_team_names(team_names, randomize_teams)
        return cls(**parameters)

    def get_full_schedule(
        self,
        num_schedules: int,
        randomize_first_rounds: bool = True,
        randomize_second_rounds: bool = True,
    ) -> Iterator[Round]:

        """
        Concatenate num_schedules double-round-robin schedules together.

        ----
        Parameters:

            num_schedules: int
                Number of times schedule should be concatenated.

            randomize_first_rounds: bool = True
                If True, order of rounds in the first portion will be randomized
                in each schedule.

                If False, the first portion of the tournament will be the same
                in all schedules.

            randomize_second_rounds: bool = True
                If True, order of rounds in the second portion will be randomized
                in each schedule.

                If False, order will be the same as first_rounds in each schedule,
                meaning that if (A, B) happened in the forth round for the first portion
                of the tournament, (B, A) will happen in the forth round for the second.

        ----
        Returns:
            Iterator[Round]
                Generator for the entire schedule.

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

            -> Notice that everything was shuffled.
        """

        for _ in range(num_schedules):

            first_schedule_copy = self.first_schedule.copy()

            if randomize_first_rounds:
                random.shuffle(first_schedule_copy)

            second_schedule_copy = flip_home_away_in_schedule(first_schedule_copy)

            if randomize_second_rounds:
                random.shuffle(second_schedule_copy)

            yield from first_schedule_copy
            yield from second_schedule_copy
