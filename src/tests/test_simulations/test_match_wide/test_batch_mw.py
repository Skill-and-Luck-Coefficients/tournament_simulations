import pandas as pd
import pytest

import tournament_simulations.simulations.match_wide.batch as batch


@pytest.fixture
def match_to_probabilities_winner():

    return pd.Series(
        data=[
            {"h": 0, "d": 0, "a": 1},
            {"h": 1, "d": 0, "a": 0},
            {"h": 0, "d": 1, "a": 0},
            {"h": 1, "d": 0, "a": 0},
        ],
        index=["match1", "match2", "match3", "match4"],
    )


@pytest.fixture
def match_to_probabilities_ppm():

    return pd.Series(
        data=[
            {(3, 0): 0, (1, 1): 0, (0, 3): 1},
            {(3, 0): 1, (1, 1): 0, (0, 3): 0},
            {(3, 0): 0, (1, 1): 1, (0, 3): 0},
            {(3, 0): 1, (1, 1): 0, (0, 3): 0},
        ],
        index=["match1", "match2", "match3", "match4"],
    )


@pytest.fixture
def data_to_join_first():

    return pd.DataFrame(
        {
            "id": ["1", "1", "2", "2"],
            "date number": [0, 1, 0, 0],
            "home": ["A", "B", "a", "c"],
            "away": ["C", "A", "b", "b"],
        }
    ).set_index(["id", "date number"])


@pytest.fixture
def data_to_join_second():

    return pd.DataFrame(
        {
            "id": ["1", "1", "1", "1", "2", "2", "2", "2"],
            "date number": [0, 0, 1, 1, 0, 0, 1, 1],
            "team": ["A", "B", "B", "C", "a", "b", "c", "a"],
        }
    ).set_index(["id", "date number"])


def test_batch_simulate_winners_default(
    match_to_probabilities_winner: pd.Series, data_to_join_first: pd.DataFrame
):

    num_iteration_simulation = (1, 3)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "2", "2"],
            "date number": [0, 1, 0, 0],
            "s0": ["a", "h", "d", "h"],
            "s1": ["a", "h", "d", "h"],
            "s2": ["a", "h", "d", "h"],
        }
    ).set_index(["id", "date number"])

    simulations = batch.batch_simulate_winners(
        match_to_probabilities_winner,
        data_to_join_first.index,
        num_iteration_simulation,
        func_after_simulation=lambda x: x,
    )

    assert simulations.equals(expected)


def test_batch_simulate_winners_with_func_after(
    match_to_probabilities_winner: pd.Series, data_to_join_first: pd.DataFrame
):

    # apply func
    def replace_home_with_away(df: pd.DataFrame):
        return df.replace({"h": "a"})

    num_iteration_simulation = (2, 3)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "2", "2"],
            "date number": [0, 1, 0, 0],
            "s0": ["a", "a", "d", "a"],
            "s1": ["a", "a", "d", "a"],
            "s2": ["a", "a", "d", "a"],
            "s3": ["a", "a", "d", "a"],
            "s4": ["a", "a", "d", "a"],
            "s5": ["a", "a", "d", "a"],
        }
    ).set_index(["id", "date number"])

    simulations = batch.batch_simulate_winners(
        match_to_probabilities_winner,
        data_to_join_first.index,
        num_iteration_simulation,
        func_after_simulation=replace_home_with_away,
    )

    assert simulations.equals(expected)


def test_batch_simulate_points_per_match_default(
    match_to_probabilities_ppm: pd.Series, data_to_join_second: pd.DataFrame
):

    num_iteration_simulation = (1, 3)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "1", "1", "2", "2", "2", "2"],
            "date number": [0, 0, 1, 1, 0, 0, 1, 1],
            "s0": [0, 3, 3, 0, 1, 1, 3, 0],
            "s1": [0, 3, 3, 0, 1, 1, 3, 0],
            "s2": [0, 3, 3, 0, 1, 1, 3, 0],
        }
    ).set_index(["id", "date number"])

    simulations = batch.batch_simulate_points_per_match(
        match_to_probabilities_ppm,
        data_to_join_second.index,
        num_iteration_simulation,
        func_after_simulation=lambda x: x,
    )

    assert simulations.equals(expected)


def test_batch_simulate_points_per_match_with_func_after_one(
    match_to_probabilities_ppm: pd.Series, data_to_join_second: pd.DataFrame
):

    # apply func
    def get_rankings(df: pd.DataFrame):
        return df.groupby(["id", "team"], observed=True).sum()

    num_iteration_simulation = (2, 3)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "1", "2", "2", "2"],
            "team": ["A", "B", "C", "a", "b", "c"],
            "s0": [0, 6, 0, 1, 1, 3],
            "s1": [0, 6, 0, 1, 1, 3],
            "s2": [0, 6, 0, 1, 1, 3],
            "s3": [0, 6, 0, 1, 1, 3],
            "s4": [0, 6, 0, 1, 1, 3],
            "s5": [0, 6, 0, 1, 1, 3],
        }
    ).set_index(["id", "team"])

    simulations = batch.batch_simulate_points_per_match(
        match_to_probabilities_ppm,
        data_to_join_second.set_index("team", append=True).index,
        num_iteration_simulation,
        func_after_simulation=get_rankings,
    )

    assert simulations.equals(expected)


def test_batch_simulate_points_per_match_with_func_after_two(
    match_to_probabilities_ppm: pd.Series, data_to_join_second: pd.DataFrame
):

    # apply func
    def add_three(df: pd.DataFrame):
        return df + 3

    num_iteration_simulation = (2, 3)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "1", "1", "2", "2", "2", "2"],
            "date number": [0, 0, 1, 1, 0, 0, 1, 1],
            "s0": [3, 6, 6, 3, 4, 4, 6, 3],
            "s1": [3, 6, 6, 3, 4, 4, 6, 3],
            "s2": [3, 6, 6, 3, 4, 4, 6, 3],
            "s3": [3, 6, 6, 3, 4, 4, 6, 3],
            "s4": [3, 6, 6, 3, 4, 4, 6, 3],
            "s5": [3, 6, 6, 3, 4, 4, 6, 3],
        }
    ).set_index(["id", "date number"])

    simulations = batch.batch_simulate_points_per_match(
        match_to_probabilities_ppm,
        data_to_join_second.index,
        num_iteration_simulation,
        func_after_simulation=add_three,
    )

    assert simulations.equals(expected)
