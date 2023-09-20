from dataclasses import dataclass
from typing import Callable

import pandas as pd

from tournament_simulations.data_structures.points_per_match import PointsPerMatch

from . import match_wide as mw
from . import tournament_wide as tw


@dataclass
class SimulatePointsPerMatch:

    """
    Simulate tournament from Matches.

    matches: Matches
        Tournament matches.
    """

    ppm: PointsPerMatch

    def tournament_wide(
        self,
        num_iteration_simulation: tuple[int, int],
        id_to_probabilities: pd.Series | None = None,
        func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
    ) -> pd.DataFrame:

        """
        Simulations tournament-wide, that is, each tournament has a single
        probability: [prob home win, prob draw, prob away win].

        All matches for a tournament will have the same probability.

        ----
        Parameters:

            num_iteration_simulation: tuple[int, int]
                Respectively, number of iterations and number of
                simulations per iteration (batch size).

                This helps avoid using too much memory.

            func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame]
                By default, does nothing -> lambda x: x.

                Function to be applied after simulating data.
                    Input Index:
                        self.ppm.df.set_index("team", append=True).index
                            Team names are in index so that they are also returned
                    Input Column:
                        i-th column -> winners for i-th simulation
                            Note: i-th simulation (column) is named f"s{i}"

            id_to_probabilities: pd.Series | None = None
                Series mapping each tournament id to the desired probabilities.

                Probabilities are a Mapping:
                    keys: possible results (str)
                    values: probability for each possible result (float)

                If not provided, probabilities will be taken from self.matches.
                    For each tournament the number of home-team wins, draws and
                    away-team wins will be counted to estimate it.

        -----
        Returns:
            pd.DataFrame
                By default, points teams gained for all simulations.
                    Index:
                        self.ppm.df.set_index("team", append=True).index
                            Team names are in index so that they are also returned
                    Columns:
                        f"s{i}" -> points teams gained for matches in i-th simulation
                            Note: i-th simulation (column) is named f"s{i}"

                If func_after_simulation is not default, then it will be different.

        """
        if id_to_probabilities is None:
            id_to_probabilities = self.ppm.probabilities_per_id()

        return tw.batch_simulate_points_per_match(
            id_to_probabilities=id_to_probabilities,
            id_to_num_matches=self.ppm.number_of_matches_per_id,
            simulation_index=self.ppm.df.set_index("team", append=True).index,
            num_iteration_simulation=num_iteration_simulation,
            func_after_simulation=func_after_simulation,
        )

    def match_wide(
        self,
        num_iteration_simulation: tuple[int, int],
        match_to_probabilities: pd.Series,
        func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
    ) -> pd.DataFrame:

        """
        Simulations match-wide, that is, each match has its own
        probability: [prob home win, prob draw, prob away win].

        ----
        Parameters:

            match_to_probabilities: pd.Series["match", Probabilities]]
                Mapping each match to its probabilities.
                Index should be in the same order as simulation_index.

                    Probabilities are a tuple:
                        (prob home team win, prob draw, prob away team win)

            num_iteration_simulation: tuple[int, int]
                Respectively, number of iterations and number of
                simulations per iteration (batch size).

                This helps avoid using too much memory.

            func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame]
                By default, does nothing -> lambda x: x.

                Function to be applied after simulating data.
                    Input Index:
                        self.ppm.df.set_index("team", append=True).index
                            Team names are in index so that they are also returned
                    Input Column:
                        i-th column -> winners for i-th simulation
                            Note: i-th simulation (column) is named f"s{i}"

        -----
        Returns:
            pd.DataFrame
                By default, points teams gained for all simulations.
                    Index:
                        self.ppm.df.set_index("team", append=True).index
                            Team names are in index so that they are also returned
                    Columns:
                        f"s{i}" -> points teams gained for matches in i-th simulation
                            Note: i-th simulation (column) is named f"s{i}"

                If func_after_simulation is not default, then it will be different.
        """

        return mw.batch_simulate_points_per_match(
            match_to_probabilities=match_to_probabilities,
            simulation_index=self.ppm.df.set_index("team", append=True).index,
            num_iteration_simulation=num_iteration_simulation,
            func_after_simulation=func_after_simulation,
        )
