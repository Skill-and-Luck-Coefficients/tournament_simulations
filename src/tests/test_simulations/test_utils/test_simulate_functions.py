import numpy as np

import tournament_simulations.simulations.utils.simulate_functions as sf


def test_simulate_winners():

    probabilities = {"h": 1, "d": 0, "a": 0}
    assert sf.simulate_winners(probabilities, 0, 0).size == 0
    assert sf.simulate_winners(probabilities, 1, 0).size == 0
    assert sf.simulate_winners(probabilities, 0, 1).size == 0

    for winner, prob in [("h", (1, 0, 0)), ("d", (0, 1, 0)), ("a", (0, 0, 1))]:

        probability = dict(zip(("h", "d", "a"), prob))
        expected = np.array([[winner]])
        winners = sf.simulate_winners(probability, 1, 1)

        assert winners.shape == expected.shape
        assert np.all(winners == expected)

    possible_results = ("one", "two", "three", "four")
    probabilities = dict(zip(possible_results, (1, 0, 0, 0)))
    winners = sf.simulate_winners(probabilities, 4, 1)
    expected = np.array([["one"] * 4])
    assert winners.shape == expected.shape
    assert np.all(winners == expected)

    probabilities = dict(zip(possible_results, (0, 0, 0, 1)))
    winners = sf.simulate_winners(probabilities, 1, 4)
    expected = np.array([["four"] for _ in range(4)])
    assert winners.shape == expected.shape
    assert np.all(winners == expected)

    possible_results = ("h", "d", "a")
    probabilities = dict(zip(possible_results, (0, 0.5, 0.5)))
    winners = sf.simulate_winners(probabilities, 10, 10)
    assert winners.shape == (10, 10)
    assert np.all((winners == "d") | (winners == "a"))

    probabilities = dict(zip(possible_results, (0.5, 0, 0.5)))
    winners = sf.simulate_winners(probabilities, 15, 15)
    assert winners.shape == (15, 15)
    assert np.all((winners == "h") | (winners == "a"))

    probabilities = dict(zip(possible_results, (0.5, 0.5, 0)))
    winners = sf.simulate_winners(probabilities, 20, 20)
    assert winners.shape == (20, 20)
    assert np.all((winners == "h") | (winners == "d"))

    probabilities = dict(zip(possible_results, (1 / 3, 1 / 3, 1 / 3)))
    winners = sf.simulate_winners(probabilities, 7, 14)
    assert winners.shape == (14, 7)
    assert np.all((winners == "h") | (winners == "d") | (winners == "a"))


def test_simulate_simulate_points_per_match():

    probabilities = {"h": 1, "d": 0, "a": 0}
    assert sf.simulate_points_per_match(probabilities, 0, 0).size == 0
    assert sf.simulate_points_per_match(probabilities, 1, 0).size == 0
    assert sf.simulate_points_per_match(probabilities, 0, 1).size == 0

    for point, prob in [
        ([[3], [0]], (1, 0, 0)),
        ([[1], [1]], (0, 1, 0)),
        ([[0], [3]], (0, 0, 1)),
    ]:
        probability = dict(zip(((3, 0), (1, 1), (0, 3)), prob))
        expected = np.array(point)
        points = sf.simulate_points_per_match(probability, 1, 1)

        assert points.shape == expected.shape
        assert np.all(points == expected)

    possible_results = ((3, 0), (1, 1), (0, 0), (0, 3))
    probabilities = dict(zip(possible_results, (1, 0, 0, 0)))
    points = sf.simulate_points_per_match(probabilities, 4, 1)
    expected = np.array([[3, 3, 3, 3], [0, 0, 0, 0]])
    assert points.shape == expected.shape
    assert np.all(points == expected)

    probabilities = dict(zip(possible_results, (0, 0, 0, 1)))
    points = sf.simulate_points_per_match(probabilities, 1, 4)
    expected = np.array([[0], [3], [0], [3], [0], [3], [0], [3]])
    assert points.shape == expected.shape
    assert np.all(points == expected)

    possible_results = ((3, 0), (1, 1), (0, 3))
    probabilities = dict(zip(possible_results, (0, 0.5, 0.5)))
    points = sf.simulate_points_per_match(probabilities, 10, 10)
    assert points.shape == (20, 10)
    assert np.all((points == 3) | (points == 1) | (points == 0))
    assert np.all((points[::2] == 1) | (points[::2] == 0))
    assert np.all((points[1::2] == 3) | (points[1::2] == 1))

    probabilities = dict(zip(possible_results, (0.5, 0, 0.5)))
    points = sf.simulate_points_per_match(probabilities, 15, 15)
    assert points.shape == (30, 15)
    assert np.all((points == 3) | (points == 0))
    assert np.all((points[::2] == 3) | (points[::2] == 0))
    assert np.all((points[1::2] == 3) | (points[1::2] == 0))

    probabilities = dict(zip(possible_results, (0.5, 0.5, 0)))
    points = sf.simulate_points_per_match(probabilities, 20, 20)
    assert points.shape == (40, 20)
    assert np.all((points == 3) | (points == 1) | (points == 0))
    assert np.all((points[::2] == 3) | (points[::2] == 1))
    assert np.all((points[1::2] == 1) | (points[1::2] == 0))

    probabilities = dict(zip(possible_results, (1 / 3, 1 / 3, 1 / 3)))
    points = sf.simulate_points_per_match(probabilities, 7, 14)
    assert points.shape == (28, 7)
    assert np.all((points == 3) | (points == 1) | (points == 0))
