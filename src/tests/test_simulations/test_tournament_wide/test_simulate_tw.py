import numpy as np
import pandas as pd
import pytest

import tournament_simulations.simulations.tournament_wide.simulate as simul


@pytest.fixture
def id_to_probabilities():

    return pd.Series(
        data=[(0, 0, 1), (1, 0, 0), (0, 1, 0)],
        index=pd.Index(["1", "2", "3"], name="id"),
    )


@pytest.fixture
def id_to_num_matches():

    return pd.Series(
        data=[2, 2, 2],
        index=pd.Index(["1", "2", "3"], name="num matches"),
    )


@pytest.fixture
def data_to_join_first():

    return pd.DataFrame(
        {
            "id": ["1", "1", "2", "2", "3", "3"],
            "date number": [0, 1, 0, 1, 0, 0],
            "home": ["A", "B", "a", "b", "two", "one"],
            "away": ["C", "A", "b", "c", "one", "two"],
        }
    ).set_index(["id", "date number"])


@pytest.fixture
def data_to_join_second():

    return pd.DataFrame(
        {
            "id": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
            "date number": [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            "team": [
                "A",
                "B",
                "B",
                "C",
                "b",
                "a",
                "c",
                "a",
                "2",
                "1",
                "1",
                "2",
            ],
        }
    ).set_index(["id", "date number"])


def test_simulate_tournament_wide_template_first(
    id_to_probabilities: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_first: pd.DataFrame,
):

    # apply func
    def apply_func(prob__num_matches, num_simulations):
        prob, num_matches = prob__num_matches
        return np.array([[*prob, num_simulations]] * num_matches)

    num_simulations = 5
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "2", "2", "3", "3"],
            "date number": [0, 1, 0, 1, 0, 0],
            0: [0, 0, 1, 1, 0, 0],
            1: [0, 0, 0, 0, 1, 1],
            2: [1, 1, 0, 0, 0, 0],
            3: [num_simulations] * 6,
        }
    ).set_index(["id", "date number"])

    joined_id_maps = pd.concat([id_to_probabilities, id_to_num_matches], axis=1)
    id_to_prob__num_matches = pd.Series(
        joined_id_maps.itertuples(index=False, name=None), index=joined_id_maps.index
    )

    simulations = simul._simulate_tournament_wide_template(
        apply_func, num_simulations, id_to_prob__num_matches, data_to_join_first.index
    )

    assert simulations.equals(expected)


def test_simulate_tournament_wide_template_second(
    id_to_probabilities: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_second: pd.DataFrame,
):

    # apply func
    def apply_func(prob, num_simulations):
        return np.array(
            [
                [num_simulations, num_simulations * 2],
                [num_simulations * 3, num_simulations * 4],
            ]
            * num_simulations
        )

    num_simulations = 2
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
            "date number": [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            0: [num_simulations, num_simulations * 3] * 6,
            1: [num_simulations * 2, num_simulations * 4] * 6,
        }
    ).set_index(["id", "date number"])

    joined_id_maps = pd.concat([id_to_probabilities, id_to_num_matches], axis=1)
    id_to_prob__num_matches = pd.Series(
        joined_id_maps.itertuples(index=False, name=None), index=joined_id_maps.index
    )

    simulations = simul._simulate_tournament_wide_template(
        apply_func, num_simulations, id_to_prob__num_matches, data_to_join_second.index
    )

    assert simulations.equals(expected)


def test_simulate_winners__tournament_wide(
    id_to_probabilities: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_first: pd.DataFrame,
):

    num_simulations = 2
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "2", "2", "3", "3"],
            "date number": [0, 1, 0, 1, 0, 0],
            0: ["a", "a", "h", "h", "d", "d"],
            1: ["a", "a", "h", "h", "d", "d"],
        }
    ).set_index(["id", "date number"])

    simulations = simul.simulate_winners__tournament_wide(
        num_simulations,
        id_to_probabilities,
        id_to_num_matches,
        data_to_join_first.index,
    )

    assert simulations.equals(expected)


def test_simulate_points_per_match__tournament_wide(
    id_to_probabilities: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_second: pd.DataFrame,
):

    num_simulations = 4
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
            "date number": [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            0: [0, 3, 0, 3, 3, 0, 3, 0, 1, 1, 1, 1],
            1: [0, 3, 0, 3, 3, 0, 3, 0, 1, 1, 1, 1],
            2: [0, 3, 0, 3, 3, 0, 3, 0, 1, 1, 1, 1],
            3: [0, 3, 0, 3, 3, 0, 3, 0, 1, 1, 1, 1],
        }
    ).set_index(["id", "date number"])

    simulations = simul.simulate_points_per_match__tournament_wide(
        num_simulations,
        id_to_probabilities,
        id_to_num_matches,
        data_to_join_second.index,
    )

    assert simulations.equals(expected)
