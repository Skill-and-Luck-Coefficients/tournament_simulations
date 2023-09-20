from typing import Callable

import pandas as pd

from tournament_simulations.logs import log, tournament_simulations_logger

from ..utils.batch_simulations import batch_simulate_tournaments_template
from .simulate import (
    simulate_points_per_match__tournament_wide,
    simulate_winners__tournament_wide,
)


@log(tournament_simulations_logger.info)
def batch_simulate_winners(
    id_to_probabilities: pd.Series,
    id_to_num_matches: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
    num_iteration_simulation: tuple[int, int],
    func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
) -> pd.DataFrame:

    """
    Simulates the winner (of result) for all matches.

    All matches for a tournament will have the same probabilities.

    Simulations are split into 'num_simulations[0]' batches with
    'num_simulations[1]' simulations each.

    -----
    Parameters:

        id_to_probabilities: pd.Series["id", Probabilities]]
            Mapping from each tournament 'id' to the desired probabilities.
            Index should be in the same order as simulation_index.

                Probabilities are a Mapping:
                    keys: possible results (str)
                    values: probability for each possible result (float)

        id_to_num_matches: pd.Series["id", int]
            Mapping from each tournament 'id' to its total number of matches.
            Index should be in the same order as simulation_index.

        simulation_index: pd.Index | pd.MultiIndex
            Simulated dataframe will have its index set to this.

            Ideally, all that is necessary to identify each
            simulated dataframe line should be in this.

        num_iteration_simulation: tuple[int, int]
            Respectively, number of iterations and number of
            simulations per iteration (batch size).

            This helps avoid using too much memory.

        func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame]
            By default, does nothing -> lambda x: x.

            Function to be applied after simulating data.
                Input Index -> simulation_index'
                i-th column -> winners for i-th simulation
                        Note: i-th simulation (column) is named f"s{i}"

    -----
    Returns:
        pd.DataFrame
            By default, winner of matches for all simulations.
                Index -> 'simulation_index'
                i-th column -> winners for i-th simulation
                        Note: i-th simulation (column) is named f"s{i}"

            If func_after_simulation is not default, then it will be different.

    """

    num_iterations, num_simulation_per_iteration = num_iteration_simulation

    return batch_simulate_tournaments_template(
        simulate_winners__tournament_wide,
        num_iterations,
        func_after_simulation,
        # simulate_winners__tournament_wide parameters
        num_simulations=num_simulation_per_iteration,
        id_to_probabilities=id_to_probabilities,
        id_to_num_matches=id_to_num_matches,
        simulation_index=simulation_index,
    )


@log(tournament_simulations_logger.info)
def batch_simulate_points_per_match(
    id_to_probabilities: pd.Series,
    id_to_num_matches: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
    num_iteration_simulation: tuple[int, int],
    func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
) -> pd.DataFrame:

    """
    Simulates points each team gained in all matches.

    All matches for a tournament will have the same probabilities.

    Simulations are split into 'num_simulations[0]' batches with
    'num_simulations[1]' simulations each.

    -----
    Parameters:

        id_to_probabilities: pd.Series["id", Probabilities]]
            Mapping from each tournament 'id' to the desired probabilities.
            Index should be in the same order as simulation_index.

                Probabilities are a Mapping:
                    keys: possible results (str)
                    values: probability for each possible result (float)

        id_to_num_matches: pd.Series["id", int]
            Mapping from each tournament 'id' to its total number of matches.
            Index should be in the same order as simulation_index.

        simulation_index: pd.Index | pd.MultiIndex
            Simulated dataframe will have its index set to this.

            Ideally, all that is necessary to identify each
            simulated dataframe line should be in this.

        num_iteration_simulation: tuple[int, int]
            Respectively, number of iterations and number of
            simulations per iteration (batch size).

            This helps avoid using too much memory.

        func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame]
            By default, does nothing -> lambda x: x.

            Function to be applied after simulating data.
                Input Index -> 'simulation_index'
                i-th column -> points each team gained for matches in i-th simulation
                    Note: i-th simulation (column) is named f"s{i}"
    -----
    Returns:
        pd.DataFrame
             By default, points teams gained for all simulations.
                Index -> 'simulation_index'
                i-th column -> points each team gained for matches in i-th simulation
                        Note: i-th simulation (column) is named f"s{i}"

            If func_after_simulation is not default, then it will be different.

    """

    num_iterations, num_simulation_per_iteration = num_iteration_simulation

    return batch_simulate_tournaments_template(
        simulate_points_per_match__tournament_wide,
        num_iterations,
        func_after_simulation,
        # simulate_points_per_match__tournament_wide parameters
        num_simulations=num_simulation_per_iteration,
        id_to_probabilities=id_to_probabilities,
        id_to_num_matches=id_to_num_matches,
        simulation_index=simulation_index,
    )
