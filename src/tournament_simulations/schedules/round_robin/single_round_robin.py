from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Iterator

from ..randomize import Option, RandomizeSchedule
from ..utils.scheduling_types import Round, Team
from . import create_single_round_robin as create


@dataclass
class SingleRoundRobin:

    """
    Dataclass which saves the matches for a single round-robin
    tournament.

    ----
    Parameters:

        num_teams: int
            Number of teams in the round-robin tournament

        team_names: list[Team]
            Teams namess

        schedule: list[tuple[tuple[Team, Team], ...]
            Single round-robin schedule in which:
                1) Rounds are tuple[Match, ...]

                2) Match is a tuple[Team, Team]

                3) Team can be int, str or something else.
    """

    num_teams: int
    team_names: list[Team]
    schedule: list[Round]

    @classmethod
    def from_num_teams(
        cls,
        num_teams: int,
        scheduling_func: str | Callable[[int], list[Round]] = "circle",
    ) -> SingleRoundRobin:

        """
        In this case, teams will be integers.

        You can think of it as the the index position for
        a list with team names.

        Default Algorithm:
            https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method

        -----
        Parameters:
            num_teams: int
                Number of teams

            scheduling_func: str | Callable[[int], list[Round]] = "circle"

                Function responsible for creating a schedule.

                Some methods are implemented, so you can use strings to call them.
                    Options: "circle".

                You can also provide a function.
                    Input:
                        int
                            number of teams as a parameter.

                    Output:
                        list[
                            tuple[  # Round
                                tuple[Team, Team],  # Match
                                ...
                            ]
                        ]
                            A tournament Schedule
        """
        parameters = create.get_kwargs_from_num_teams(num_teams, scheduling_func)
        return cls(**parameters)

    @classmethod
    def from_team_names(
        cls,
        team_names: Iterable[Team],
        scheduling_func: str | Callable[[int], list[Round]] = "circle",
    ) -> SingleRoundRobin:

        """
        In this case, a team will be whatever was passed as its name.
            i-th team will be represented by team_names[i]

        Default Algorithm:
            https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method

        -----
        Parameters:
            team_names: Iterable[Team]
                Data that represents teams.

            scheduling_func: str | Callable[[int], list[Round]] = "circle"

                Function responsible for creating a schedule.

                Some methods are implemented, so you can use strings to call them.
                    Options: "circle".

                You can also provide a function.
                    Input:
                        int
                            number of teams as a parameter.

                    Output:
                        list[
                            tuple[  # Round
                                tuple[Team, Team],  # Match
                                ...
                            ]
                        ]
                            A tournament Schedule
        """
        parameters = create.get_kwargs_from_team_names(team_names, scheduling_func)
        return cls(**parameters)

    def get_full_schedule(
        self, num_schedules: int, to_randomize: Option | Iterable[Option] | None = "all"
    ) -> Iterator[Round]:

        """
        Concatenate num_schedules single-round-robin schedules together.

        ----
        Parameters:

            num_schedules: int
                Number of times schedule should be concatenated.

            to_randomize: Option | Iterable[Option] | None = "all"

                What should be randomized.

                If it is an empty iterable or None, a copy of schedule will be returned.

                Option
                    "teams":
                        Randomizes what matches each team plays.
                    "home_away":
                        Randomizes which team played as home-team.
                    "matches":
                        Randomizes order of matches for each round.
                    "rounds":
                        Randomizes order of rounds in the schedule.
                    "all":
                        Equivalent to ["teams", "home_away", "matches", "rounds"]
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
        rand_schedule = RandomizeSchedule(self.schedule, self.team_names)

        for _ in range(num_schedules):
            yield from rand_schedule.randomize(to_randomize)
