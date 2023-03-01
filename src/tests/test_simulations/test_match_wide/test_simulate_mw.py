import numpy as np
import pandas as pd
import pytest

import tournament_simulations.simulations.match_wide.simulate as simul


@pytest.fixture
def id_to_probabilities():

    return pd.Series(
        data=[(0, 0, 1), (1, 0, 0), (0, 1, 0)],
        index=pd.MultiIndex.from_arrays(
            [["1", "2", "3"], [0, 0, 0]], names=["id", "date number"]
        ),
    )


@pytest.fixture
def data_to_join_first():

    return pd.DataFrame(
        {
            "id": ["1", "2", "3"],
            "date number": [0, 0, 0],
            "home": ["A", "B", "A"],
            "away": ["C", "A", "B"],
        }
    ).set_index(["id", "date number"])


@pytest.fixture
def data_to_join_second():

    return pd.DataFrame(
        {
            "id": ["1", "1", "2", "2", "3", "3"],
            "date number": [0, 0, 1, 1, 0, 0],
            "team": ["A", "B", "b", "a", "two", "one"],
        }
    ).set_index(["id", "date number"])


def test_simulate_match_wide_template_first(
    id_to_probabilities: pd.Series, data_to_join_first: pd.DataFrame
):

    # apply func
    def apply_func(prob, num_simulations):
        return np.array([[*prob, num_simulations]])

    num_simulations = 5
    expected = pd.DataFrame(
        {
            "id": ["1", "2", "3"],
            "date number": [0, 0, 0],
            0: [0, 1, 0],
            1: [0, 0, 1],
            2: [1, 0, 0],
            3: [num_simulations] * 3,
        }
    ).set_index(["id", "date number"])

    simulations = simul._simulate_match_wide_template(
        apply_func, num_simulations, id_to_probabilities, data_to_join_first.index
    )

    assert simulations.equals(expected)


def test_simulate_match_wide_template_second(
    id_to_probabilities: pd.Series, data_to_join_second: pd.DataFrame
):

    # apply func
    def apply_func(prob, num_simulations):
        return np.array(
            [
                [num_simulations, num_simulations * 2],
                [num_simulations * 3, num_simulations * 4],
            ]
        )

    num_simulations = 3.0
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "2", "2", "3", "3"],
            "date number": [0, 0, 1, 1, 0, 0],
            0: [num_simulations, num_simulations * 3] * 3,
            1: [num_simulations * 2, num_simulations * 4] * 3,
        }
    ).set_index(["id", "date number"])

    simulations = simul._simulate_match_wide_template(
        apply_func, num_simulations, id_to_probabilities, data_to_join_second.index
    )

    assert simulations.equals(expected)


def test_simulate_winners__match_wide(
    id_to_probabilities: pd.Series, data_to_join_first: pd.DataFrame
):

    num_simulations = 4
    expected = pd.DataFrame(
        {
            "id": ["1", "2", "3"],
            "date number": [0, 0, 0],
            0: ["a", "h", "d"],
            1: ["a", "h", "d"],
            2: ["a", "h", "d"],
            3: ["a", "h", "d"],
        }
    ).set_index(["id", "date number"])

    simulations = simul.simulate_winners__match_wide(
        num_simulations, id_to_probabilities, data_to_join_first.index
    )

    assert simulations.equals(expected)


def test_simulate_points_per_match__match_wide(
    id_to_probabilities: pd.Series, data_to_join_second: pd.DataFrame
):

    num_simulations = 4
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "2", "2", "3", "3"],
            "date number": [0, 0, 1, 1, 0, 0],
            0: [0, 3, 3, 0, 1, 1],
            1: [0, 3, 3, 0, 1, 1],
            2: [0, 3, 3, 0, 1, 1],
            3: [0, 3, 3, 0, 1, 1],
        }
    ).set_index(["id", "date number"])

    simulations = simul.simulate_points_per_match__match_wide(
        num_simulations, id_to_probabilities, data_to_join_second.index
    )

    assert simulations.equals(expected)
