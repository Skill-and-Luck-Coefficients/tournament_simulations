"""
Simulations match-wide, that is, each matchhas its own probability:
[prob home win, prob draw, prob away win].
"""
from typing import Callable

import numpy as np
import pandas as pd

from data_structures.utils.types import Probabilities

from ..utils.simulate_functions import simulate_points_per_match, simulate_winners


def _simulate_match_wide_template(
    apply_func: Callable[[Probabilities, int], np.ndarray],
    num_simulations: int,
    id_to_probabilities: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
) -> pd.DataFrame:

    simulations = id_to_probabilities.apply(apply_func, num_simulations=num_simulations)

    data_for_df = np.vstack(simulations)
    return pd.DataFrame(data_for_df, index=simulation_index)


def simulate_winners__match_wide(
    num_simulations: int,
    id_to_probabilities: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
) -> pd.DataFrame:

    # apply function
    def _simulate_winners_one_match_one_id(
        probabilities: Probabilities,
        num_simulations: int,
    ) -> np.ndarray:

        return simulate_winners(probabilities, num_simulations, num_matches=1)

    return _simulate_match_wide_template(
        apply_func=_simulate_winners_one_match_one_id,
        num_simulations=num_simulations,
        id_to_probabilities=id_to_probabilities,
        simulation_index=simulation_index,
    )


def simulate_points_per_match__match_wide(
    num_simulations: int,
    id_to_probabilities: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
) -> pd.DataFrame:

    # apply function
    def _simulate_points_per_match_one_match_one_id(
        probabilities: Probabilities,
        num_simulations: int,
    ) -> np.ndarray:

        return simulate_points_per_match(probabilities, num_simulations, num_matches=1)

    return _simulate_match_wide_template(
        apply_func=_simulate_points_per_match_one_match_one_id,
        num_simulations=num_simulations,
        id_to_probabilities=id_to_probabilities,
        simulation_index=simulation_index,
    )
