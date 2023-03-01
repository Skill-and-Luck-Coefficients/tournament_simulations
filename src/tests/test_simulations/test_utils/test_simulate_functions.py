import numpy as np

import tournament_simulations.simulations.utils.simulate_functions as sf


def test_simulate_winners():

    probabilities = (1, 0, 0)
    assert sf.simulate_winners(probabilities, 0, 0).size == 0
    assert sf.simulate_winners(probabilities, 1, 0).size == 0
    assert sf.simulate_winners(probabilities, 0, 1).size == 0

    for winner, prob in [("h", (1, 0, 0)), ("d", (0, 1, 0)), ("a", (0, 0, 1))]:

        expected = np.array([[winner]])
        winners = sf.simulate_winners(prob, 1, 1)

        assert winners.shape == expected.shape
        assert np.all(winners == expected)

    winners = sf.simulate_winners((1, 0, 0), 4, 1)
    expected = np.array([["h", "h", "h", "h"]])
    assert winners.shape == expected.shape
    assert np.all(winners == expected)

    winners = sf.simulate_winners((1, 0, 0), 1, 4)
    expected = np.array([["h"], ["h"], ["h"], ["h"]])
    assert winners.shape == expected.shape
    assert np.all(winners == expected)

    winners = sf.simulate_winners((0, 0.5, 0.5), 10, 10)
    assert winners.shape == (10, 10)
    assert np.all((winners == "d") | (winners == "a"))

    winners = sf.simulate_winners((0.5, 0, 0.5), 15, 15)
    assert winners.shape == (15, 15)
    assert np.all((winners == "h") | (winners == "a"))

    winners = sf.simulate_winners((0.5, 0.5, 0), 20, 20)
    assert winners.shape == (20, 20)
    assert np.all((winners == "h") | (winners == "d"))

    winners = sf.simulate_winners((1 / 3, 1 / 3, 1 / 3), 7, 14)
    assert winners.shape == (14, 7)
    assert np.all((winners == "h") | (winners == "d") | (winners == "a"))


def test_simulate_simulate_points_per_match():

    probabilities = (1, 0, 0)
    assert sf.simulate_points_per_match(probabilities, 0, 0).size == 0
    assert sf.simulate_points_per_match(probabilities, 1, 0).size == 0
    assert sf.simulate_points_per_match(probabilities, 0, 1).size == 0

    for point, prob in [
        ([[3], [0]], (1, 0, 0)),
        ([[1], [1]], (0, 1, 0)),
        ([[0], [3]], (0, 0, 1)),
    ]:
        expected = np.array(point)
        points = sf.simulate_points_per_match(prob, 1, 1)

        assert points.shape == expected.shape
        assert np.all(points == expected)

    points = sf.simulate_points_per_match((1, 0, 0), 4, 1)
    expected = np.array([[3, 3, 3, 3], [0, 0, 0, 0]])
    assert points.shape == expected.shape
    assert np.all(points == expected)

    points = sf.simulate_points_per_match((1, 0, 0), 1, 4)
    expected = np.array([[3], [0], [3], [0], [3], [0], [3], [0]])
    assert points.shape == expected.shape
    assert np.all(points == expected)

    points = sf.simulate_points_per_match((0, 0.5, 0.5), 10, 10)
    assert points.shape == (20, 10)
    assert np.all((points == 3) | (points == 1) | (points == 0))
    assert np.all((points[::2] == 1) | (points[::2] == 0))
    assert np.all((points[1::2] == 3) | (points[1::2] == 1))

    points = sf.simulate_points_per_match((0.5, 0, 0.5), 15, 15)
    assert points.shape == (30, 15)
    assert np.all((points == 3) | (points == 0))
    assert np.all((points[::2] == 3) | (points[::2] == 0))
    assert np.all((points[1::2] == 3) | (points[1::2] == 0))

    points = sf.simulate_points_per_match((0.5, 0.5, 0), 20, 20)
    assert points.shape == (40, 20)
    assert np.all((points == 3) | (points == 1) | (points == 0))
    assert np.all((points[::2] == 3) | (points[::2] == 1))
    assert np.all((points[1::2] == 1) | (points[1::2] == 0))

    points = sf.simulate_points_per_match((1 / 3, 1 / 3, 1 / 3), 7, 14)
    assert points.shape == (28, 7)
    assert np.all((points == 3) | (points == 1) | (points == 0))
