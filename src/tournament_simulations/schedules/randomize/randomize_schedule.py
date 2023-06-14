from dataclasses import dataclass
from typing import Callable, Iterable, Literal, Mapping, Sequence

from ..utils.scheduling_types import Round, Team
from . import randomize_functions as rfunc

Option = Literal["teams", "home_away", "matches", "rounds", "all"]
RandFunc = Callable[[list[Round]], list[Round]]


@dataclass
class RandomizeSchedule:
    """
    Class responsible for randomizing schedules.
    """
    schedule: list[Round]
    team_names: Sequence[Team] | None = None

    def __post_init__(self):

        self._name_to_randomize_func: Mapping[Option, RandFunc] = {
            "home_away": rfunc.shuffle_home_away_in_matches,
            "matches": rfunc.shuffle_matches_in_rounds,
            "rounds": rfunc.shuffle_rounds_in_schedule,
            "teams": lambda schedule: rfunc.shuffle_teams(schedule, self.team_names),
        }

    def _parse_to_randomize(
        self, to_randomize: Option | Iterable[Option] | None
    ) -> list[Option]:

        if to_randomize is None or list(to_randomize) == []:
            return []

        # 'to_randomize' might not be hashable, so converting dict to list is necessary
        if to_randomize in list(self._name_to_randomize_func):
            return [to_randomize]

        if to_randomize == "all":
            return sorted(self._name_to_randomize_func)

        return sorted(set(to_randomize))

    def randomize(self, to_randomize: Option | Iterable[Option] | None) -> list[Round]:

        """
        Randomize self.schedule.

        It returns a new list[Round], so self.schedule is never changed.

        ----
        Parameters:

            to_randomize: Option | Iterable[Option] | None

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
            list[
                tuple[  # Round
                    tuple[Team, Team], # Match
                    ...
                ]
            ]
                Randomized schedule.
        """
        to_randomize = self._parse_to_randomize(to_randomize)
        functions = [self._name_to_randomize_func[option] for option in to_randomize]

        schedule = self.schedule

        if not functions:
            schedule = schedule.copy()

        for randomize_function in functions:
            schedule = randomize_function(schedule)

        return schedule
