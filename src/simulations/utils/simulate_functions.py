import numpy as np

from data_structures.types import Probabilities


def simulate_winners(
    probabilities: Probabilities, num_simulations: int, num_matches: int
) -> np.ndarray:

    """
    Simulates winners 'num_simulations' times for 'num_matches' matches.

    -----
    Parameters:

        probabilities: tuple[float, float, float]
            Probabilities of home team win, draw and away team win.

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

    indexes = range(len(probabilities))
    simul_shape = (num_matches, num_simulations)
    index_simulation = np.random.choice(indexes, p=probabilities, size=simul_shape)

    points_simulations: np.ndarray = np.array(["h", "d", "a"])[index_simulation]
    return points_simulations


def simulate_points_per_match(
    probabilities: Probabilities, num_simulations: int, num_matches: int
) -> np.ndarray:

    """
    Simulates points 'num_simulations' times for (home, away) teams in
    'num_matches' matches.

    -----
    Parameters:

        probabilities: tuple[float, float, float]
            Probabilities of home team win, draw and away team win.

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

    indexes = range(len(probabilities))
    simul_shape = (num_matches, num_simulations)
    index_simulation = np.random.choice(indexes, p=probabilities, size=simul_shape)

    points_simulations: np.ndarray = np.array([[3, 0], [1, 1], [0, 3]])[
        index_simulation
    ]

    if points_simulations.size == 0:
        return np.array([])
    # transpose necessary since the desired result for a match isn't
    # [home points, away points].

    # it should be a column vector instead:
    #                "points"
    #    "team"
    #   team 1:  [ home points,
    #   team 2:    away points  ]
    return np.vstack(points_simulations.transpose(0, 2, 1))
