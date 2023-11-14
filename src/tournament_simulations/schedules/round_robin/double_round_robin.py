from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Iterator, Literal

from ..randomize import Option, RandomizeSchedule
from ..utils.flip_home_away import flip_home_away_in_schedule
from ..utils.reversed_schedule import reverse_schedule
from ..utils.scheduling_types import Round, Team
from . import create_double_round_robin as create

ToRandomizeType = Option | Iterable[Option] | None


@dataclass
class DoubleRoundRobin:

    """
    Dataclass which saves the matches for a double round-robin
    tournament.

    ----
    Parameters:

        num_teams: int
            Number of teams in the round-robin tournament

        team_names: list[Team]
            Teams namess

        first_schedule: list[Round]
            Single round-robin schedule in which:
                1) Rounds are tuple[Match, ...]

                2) Match is a tuple[Team, Team]

                3) Team can be int, str or something else.

    ----
    Variables automatically initiated:

        second_schedule: list[Round]
            Same as first_schedule but in-match order is flipped, that is,
            a (home, away) in first_schedule turns into (away, home).

    """

    num_teams: int
    team_names: list[Team]
    first_schedule: list[Round]

    def __post_init__(self) -> None:
        self.second_schedule = flip_home_away_in_schedule(self.first_schedule)

    @classmethod
    def from_num_teams(
        cls, num_teams: int,
        scheduling_func: str | Callable[[int], list[Round]] = "circle",
    ) -> DoubleRoundRobin:

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
    ) -> DoubleRoundRobin:

        """
        In this case, a team will be whatever was passed as its name.
            i-th team will be represented by team_names[i]

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
        parameters = create.get_kwargs_from_team_names(team_names, scheduling_func)
        return cls(**parameters)

    def get_full_schedule(
        self,
        num_schedules: int,
        to_randomize_first: ToRandomizeType = "all",
        to_randomize_second: ToRandomizeType | Literal["flipped", "mirrored", "reversed"] = "flipped",
    ) -> Iterator[Round]:

        """
        Concatenate num_schedules double-round-robin schedules together.

        ----
        Parameters:

            num_schedules: int
                Number of times schedule should be concatenated.

            to_randomize_first: Option | Iterable[Option] | None = "all"

                What should be randomized in the first portion of the double
                round-robin schedule.

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

            to_randomize_second:
                type: Option | Iterable[Option] | None | Literal["flipped"] = "flipped"

                Similar to 'to_randomize_first', but there is a new option.

                New option:
                    "flipped": (or "mirrored")
                        The schedule will be symmetric, that is, the second portion
                        will have the same order as the first, but (home, away) matches
                        will be flipped to (away, home).
                    "reversed":
                        The second portion will be the same as the first one, but reversed.

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
        """
        rand_first_schedule = RandomizeSchedule(self.first_schedule, self.team_names)
        rand_second_schedule = RandomizeSchedule(self.second_schedule, self.team_names)

        for _ in range(num_schedules):

            first_schedule = rand_first_schedule.randomize(to_randomize_first)
            yield from first_schedule

            match to_randomize_second:
                case "flipped" | "mirrored":
                    yield from flip_home_away_in_schedule(first_schedule)
                case "reversed":
                    yield from reverse_schedule(first_schedule)
                case _:
                    yield from rand_second_schedule.randomize(to_randomize_second)
