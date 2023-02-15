import logging
from typing import Callable

import pandas as pd

from logs import log

from ..utils.batch_simulations import batch_simulate_tournaments_template
from .simulate import (
    simulate_points_per_match__match_wide,
    simulate_winners__match_wide,
)


@log(logging.info)
def batch_simulate_winners(
    match_to_probabilities: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
    num_iteration_simulation: tuple[int, int],
    func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
) -> pd.DataFrame:

    """
    Simulates who is the winner of all matches.

        "h": home team win
        "d": draw
        "a": away team win

    All matches for a tournament will have the same probabilities.

    Simulations are split into 'num_simulations[0]' batches with
    'num_simulations[1]' simulations each.

    -----
    Parameters:

        match_to_probabilities: pd.Series["match", Probabilities]]
            Mapping each match to its probabilities.

            Probabilities are a tuple:
                (prob home team win, prob draw, prob away team win)

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
        simulate_winners__match_wide,
        num_iterations,
        func_after_simulation,
        # simulate_winners__match_wide parameters
        num_simulations=num_simulation_per_iteration,
        id_to_probabilities=match_to_probabilities,
        simulation_index=simulation_index,
    )


@log(logging.info)
def batch_simulate_points_per_match(
    match_to_probabilities: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
    num_iteration_simulation: tuple[int, int],
    func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
) -> pd.DataFrame:

    """
    Simulates points each team gained in all matches.

        Win: 3 points
        Draw: 1 point
        Loss: 0 points

    All matches for a tournament will have the same probabilities.

    Simulations are split into 'num_simulations[0]' batches with
    'num_simulations[1]' simulations each.

    -----
    Parameters:

        match_to_probabilities: pd.Series["match", Probabilities]]
            Mapping each match to its probabilities.

            Probabilities are a tuple:
                (prob home team win, prob draw, prob away team win)

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
        simulate_points_per_match__match_wide,
        num_iterations,
        func_after_simulation,
        # simulate_points_per_match__match_wide parameters
        num_simulations=num_simulation_per_iteration,
        id_to_probabilities=match_to_probabilities,
        simulation_index=simulation_index,
    )
