from typing import Callable, ParamSpec

import pandas as pd

P = ParamSpec("P")


def _create_column_names(num_cols: int, num_iteration: int) -> list[str]:
    return [f"s{i + num_cols * num_iteration}" for i in range(num_cols)]


def batch_simulate_tournaments_template(
    simulation_function: Callable[P, pd.DataFrame],
    num_iterations: int,
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

        simulation_function: Callable[[*args, **kwargs], pd.DataFrame]
            Simulation function.

        num_iterations: tuple[int, int]
            Number of iterations (number of batches).

        func_after_simulation: Callable[[pd.DataFrame], pd.DataFrame]
            Function to be applied after simulating data.

        *args, **kwargs
            'simulation_function' parameters.

    -----
    Returns:
        pd.DataFrame
            By default:
                Index -> Index returned by simulation_function/func_after_simulated
                Columns -> each column has data for a simulation
                    i-th simulation is named f"s{i}"
    """

    to_concat: list[pd.DataFrame] = []

    for num_iteration in range(num_iterations):

        simulation = simulation_function(*args, **kwargs)

        # simulated dataframes in all iterations have the same size, so this works
        num_cols = len(simulation.columns)
        col_names = _create_column_names(num_cols, num_iteration)
        simulation_correct_cols = simulation.set_axis(col_names, axis="columns")

        final_df = func_after_simulation(simulation_correct_cols)
        to_concat.append(final_df)

    return pd.concat(to_concat, axis=1)
