import numpy as np
from numpy.typing import NDArray

from tournament_simulations.data_structures.utils import types


def simulate_winners(
    probabilities: types.ResultProbability, num_simulations: int, num_matches: int
) -> np.ndarray:

    """
    Simulates winners 'num_simulations' times for 'num_matches' matches.

    -----
    Parameters:

        probabilities: Mapping[str, float]
            Probabilities of each result (string).
            Must have .keys() attribute.

        num_simulations: int
            How many simulations should be made.
            Shouldn't be a large number.

        num_matches: int
            Number of matches to be simulated.

    -----
    Returns:
        np.ndarray -> Shape = [num_matches, num_simulations]
            Each row has all simulations for a match.
            Each column is a different simulation.
    """
    possible_results = list(probabilities.keys())
    result_prob = [probabilities[key] for key in possible_results]
    simul_shape = (num_matches, num_simulations)

    return np.random.choice(possible_results, p=result_prob, size=simul_shape)


def simulate_points_per_match(
    probabilities: types.PontuationProbability, num_simulations: int, num_matches: int
) -> np.ndarray:

    """
    Simulates points 'num_simulations' times for (home, away) teams in
    'num_matches' matches.

    -----
    Parameters:

        probabilities: Mapping[tuple[float, float], float]
            Mapping like (must have .keys() attribute):
                (points gained by home team, points gained by away team): probability

        num_simulations: int
            How many simulations should be made.
            Shouldn't be a large number.

        num_matches: int
            Number of matches to be simulated.

    -----
    Returns:
        np.ndarray -> Shape = [2*num_matches, num_simulations]
            Each row has the points for a (team, match) pair.
            Each column is a different simulation.
    """
    possible_pontuations = [key for key in probabilities.keys()]
    pontuation_prob = [probabilities[key] for key in possible_pontuations]

    # 'choice' doesn't work with 2d arrays, so we need to simulate 'indexes' instead
    indexes = range(len(probabilities))
    simul_shape = (num_matches, num_simulations)
    index_simulation = np.random.choice(indexes, p=pontuation_prob, size=simul_shape)
    points_simulations: NDArray = np.array(possible_pontuations)[index_simulation]

    if points_simulations.size == 0:
        return np.array([])
    # transpose necessary since the desired result for a match isn't
    # [home points, away points].

    # it should be a column vector instead:
    #                "points"
    #    "team"
    #   team 1:  [ home points,
    #   team 2:    away points  ]
    return np.vstack(points_simulations.transpose(0, 2, 1))  # type: ignore
