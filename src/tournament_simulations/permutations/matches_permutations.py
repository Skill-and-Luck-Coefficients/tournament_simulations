from dataclasses import dataclass
from typing import Sequence

import pandas as pd

from tournament_simulations.data_structures.matches import Matches
from tournament_simulations.logs import log, tournament_simulations_logger

from . import one_permutation as op
from .tournament_scheduler import TournamentScheduler


@dataclass
class MatchesPermutations:

    """
    Class responsible for creating permuted tournaments.

    matches: Matches
        Tournament matches.

        Make sure that all necessary information is there:
            "id", "date number", "home" and "away".

    scheduler: TournamentScheduler
        Scheduler used to create permuted schedules.

        For each tournament, it should generate schedules
        which contain (at least) all matches in 'matches'.
    """

    matches: Matches
    scheduler: TournamentScheduler

    def __post_init__(self):

        self._permuter = op.PermuteMatches(self.matches)
        self._matches_date_numbers = op.MatchDateNumbers.from_matches(self.matches)

    @log(tournament_simulations_logger.info)
    def create_n_permutations(
        self,
        n: int,
        date_numbers: Sequence[int] | pd.Series | None = None
    ) -> Matches:

        """
        Create n permutations of all tournaments.

        Remark: There can't be a (home, away) pair happening
        more than once in the same day for any real tournament.
            It is ok for (home, away) and (away, home) to occur
            in the same day though.

        ----
        Parameters:

            n: int
                Number of permutations

            date_numbers: Sequence[int] | pd.Series | None = None
                "date number" index for all new tournaments.

                If None, "date number" index from self.matches will be used for
                all new tournaments. That is, all permuted tournaments will have the
                same match dates as the original ones.

        ----
        Returns:

            Matches
                Permuted matches.

                If the original tournament in self.df has id "{id}",
                then its i-th permutation will be called "{id}@{i}"

                df: pd.DataFrame[
                    index=[
                        "id"          -> pd.Categorical[str]
                            "{current_name}@/{sport}/{country}/{name-year}/@{num_permutation}",\n
                        "date number" -> int,
                    ],\n
                    columns=[
                        "home"                -> pd.Categorical[str] (home team name),\n
                        "away"                -> pd.Categorical[str] (away team name),\n
                        "result"              -> "{home score}:{away score}",\n
                        "winner"              -> Literal["h", "d", "a"]
                            "h" -> home\n
                            "d" -> draw\n
                            "a" -> away
                        "date"                -> "{day}.{month}.{year}",\n
                        "odds home"           -> np.float16,\n
                        "odds tie (optional)" -> np.float16,\n
                        "odds away"           -> np.float16,\n
                    ]
                ]
        """
        permutations: list[pd.DataFrame] = []

        for i in range(n):

            def _rename_id(id_: str) -> str:
                return f"{id_}@{i}"

            shuffled_date_numbers = self._matches_date_numbers.create_shuffled_copy()
            permuted_schedule = self.scheduler.generate_schedule()

            _get_new_index = op.OrderedIndex.from_schedule__date_numbers
            new_index = _get_new_index(permuted_schedule, shuffled_date_numbers)
            permuted_matches = self._permuter.permute_matches(new_index, date_numbers)

            renamed_df = permuted_matches.df.rename(index=_rename_id, level="id")
            permutations.append(renamed_df)

        return Matches(pd.concat(permutations))
