from typing import Callable

import numpy as np
import pandas as pd

from data_structures.types import Probabilities
from utils.convert_df_to_series import convert_df_to_series_of_tuples

from ..utils.simulate_functions import simulate_points_per_match, simulate_winners


def _simulate_tournament_wide_template(
    apply_func: Callable[[tuple[Probabilities, int], int], np.ndarray],
    num_simulations: int,
    id_to_prob__num_matches: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
) -> pd.DataFrame:

    simulations = id_to_prob__num_matches.apply(
        apply_func, num_simulations=num_simulations
    )

    data_for_df = np.vstack(simulations)
    return pd.DataFrame(data_for_df, simulation_index)


def simulate_winners__tournament_wide(
    num_simulations: int,
    id_to_probabilities: pd.Series,
    id_to_num_matches: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
) -> pd.DataFrame:

    # apply function
    def _simulate_winners_one_id(
        prob__num_matches: tuple[Probabilities, int],
        num_simulations: int,
    ) -> np.ndarray:

        probabilities, num_matches = prob__num_matches
        return simulate_winners(probabilities, num_simulations, num_matches)

    concatenated_series = pd.concat([id_to_probabilities, id_to_num_matches], axis=1)
    id_to_prob__num_matches = convert_df_to_series_of_tuples(concatenated_series)

    return _simulate_tournament_wide_template(
        apply_func=_simulate_winners_one_id,
        num_simulations=num_simulations,
        id_to_prob__num_matches=id_to_prob__num_matches,
        simulation_index=simulation_index,
    )


def simulate_points_per_match__tournament_wide(
    num_simulations: int,
    id_to_probabilities: pd.Series,
    id_to_num_matches: pd.Series,
    simulation_index: pd.Index | pd.MultiIndex,
) -> pd.DataFrame:

    # apply function
    def _simulate_points_per_match_one_id(
        prob__num_matches: tuple[Probabilities, int],
        num_simulations: int,
    ) -> np.ndarray:

        probabilities, num_matches = prob__num_matches
        return simulate_points_per_match(probabilities, num_simulations, num_matches)

    concatenated_series = pd.concat([id_to_probabilities, id_to_num_matches], axis=1)
    id_to_prob__num_matches = convert_df_to_series_of_tuples(concatenated_series)

    return _simulate_tournament_wide_template(
        apply_func=_simulate_points_per_match_one_id,
        num_simulations=num_simulations,
        id_to_prob__num_matches=id_to_prob__num_matches,
        simulation_index=simulation_index,
    )
