from typing import Callable, Concatenate, ParamSpec, TypeVar

import pandas as pd

T = TypeVar("T", bound=pd.DataFrame)
P = ParamSpec("P")


def _batch_simulate_tournaments(
    simulation_function: Callable[[Concatenate[int, P]], T],  # int: num_simulations
    num_iterations: int,
    num_simul_per_iteration: int,
    func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame],
    *args: P.args,
    **kwargs: P.kwargs,
) -> pd.DataFrame:

    simulations_to_concat: list[pd.DataFrame] = []

    for _ in range(num_iterations):

        simulation = simulation_function(
            *args, num_simulations=num_simul_per_iteration, **kwargs
        )
        final_df = func_after_simulation(simulation)
        simulations_to_concat.append(final_df)

    return pd.concat(simulations_to_concat, axis=1)


def _create_column_names(num_simulations) -> list[str]:
    return [f"s{i}" for i in range(num_simulations)]


def batch_simulate_tournaments_template(
    simulation_function: Callable[[Concatenate[int, P]], T],  # int: num_simulations
    num_iteration_simulation: tuple[int, int],
    func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame],
    *args: P.args,
    **kwargs: P.kwargs,
) -> pd.DataFrame:

    """
    Template for simulating a lot of tournaments in batches.

    Simulations are split into 'num_simulations[0]' batches with
    'num_simulations[1]' simulations each.

    -----
    Parameters:

        simulation_function: Callable
            Simulation function.

        num_iteration_simulation: tuple[int, int]
            Respectively, number of iterations and number of
            simulations per iteration (batch size).

            This helps avoid using too much memory.

        func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame]
            Function to be applied after simulating data.

            It mustn't modify the number of columns, that is, mustn't
            aggregate results from different simulations together.

        *args, **kwargs
            'simulation_function' parameters other than 'num_simulations'.

    -----
    Returns:
        pd.DataFrame
            By default, Information.
                Index -> same as "ppm"
                Columns -> each column has the points for a simulation
                    i-th simulation is named f"s{i}"

    """

    num_iterations, num_simul_per_iteration = num_iteration_simulation

    simulations = _batch_simulate_tournaments(
        simulation_function,
        num_iterations,
        num_simul_per_iteration,
        func_after_simulation,
        *args,
        **kwargs,
    )

    total_simulations = num_iterations * num_simul_per_iteration
    return simulations.set_axis(_create_column_names(total_simulations), axis="columns")
