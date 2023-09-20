import pandas as pd
import pytest

import tournament_simulations.simulations.tournament_wide.batch as batch


@pytest.fixture
def id_to_probabilities_winner():

    return pd.Series(
        data=[
            {"h": 0, "d": 0, "a": 1},
            {"h": 0, "d": 1, "a": 0},
            {"h": 0, "d": 1, "a": 0},
        ],
        index=pd.Index(["1", "2", "3"], name="id"),
    )


@pytest.fixture
def id_to_probabilities_ppm():

    return pd.Series(
        data=[
            {(3, 0): 0, (1, 1): 0, (0, 3): 1},
            {(3, 0): 0, (1, 1): 1, (0, 3): 0},
            {(3, 0): 0, (1, 1): 1, (0, 3): 0},
        ],
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
            "team": ["A", "B", "B", "C", "b", "a", "c", "a", "2", "1", "1", "2"],
        }
    ).set_index(["id", "date number"])


def test_batch_simulate_winners_default(
    id_to_probabilities_winner: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_first: pd.DataFrame,
):

    num_iteration_simulation = (1, 3)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "2", "2", "3", "3"],
            "date number": [0, 1, 0, 1, 0, 0],
            "s0": ["a", "a", "d", "d", "d", "d"],
            "s1": ["a", "a", "d", "d", "d", "d"],
            "s2": ["a", "a", "d", "d", "d", "d"],
        }
    ).set_index(["id", "date number"])

    simulations = batch.batch_simulate_winners(
        id_to_probabilities_winner,
        id_to_num_matches,
        data_to_join_first.index,
        num_iteration_simulation,
        func_after_simulation=lambda x: x,
    )

    assert simulations.equals(expected)


def test_batch_simulate_winners_with_func_after(
    id_to_probabilities_winner: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_first: pd.DataFrame,
):

    # apply func
    def replace_home_with_away(df: pd.DataFrame):
        return df.replace({"h": "a"})

    num_iteration_simulation = (2, 3)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "2", "2", "3", "3"],
            "date number": [0, 1, 0, 1, 0, 0],
            "s0": ["a", "a", "d", "d", "d", "d"],
            "s1": ["a", "a", "d", "d", "d", "d"],
            "s2": ["a", "a", "d", "d", "d", "d"],
            "s3": ["a", "a", "d", "d", "d", "d"],
            "s4": ["a", "a", "d", "d", "d", "d"],
            "s5": ["a", "a", "d", "d", "d", "d"],
        }
    ).set_index(["id", "date number"])

    simulations = batch.batch_simulate_winners(
        id_to_probabilities_winner,
        id_to_num_matches,
        data_to_join_first.index,
        num_iteration_simulation,
        func_after_simulation=replace_home_with_away,
    )

    assert simulations.equals(expected)


def test_batch_simulate_points_per_match_default(
    id_to_probabilities_ppm: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_second: pd.DataFrame,
):

    num_iteration_simulation = (1, 4)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
            "date number": [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            "s0": [0, 3, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1],
            "s1": [0, 3, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1],
            "s2": [0, 3, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1],
            "s3": [0, 3, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1],
        }
    ).set_index(["id", "date number"])

    simulations = batch.batch_simulate_points_per_match(
        id_to_probabilities_ppm,
        id_to_num_matches,
        data_to_join_second.index,
        num_iteration_simulation,
        func_after_simulation=lambda x: x,
    )

    assert simulations.equals(expected)


def test_batch_simulate_points_per_match_with_func_after_one(
    id_to_probabilities_ppm: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_second: pd.DataFrame,
):

    # apply func
    def get_rankings(df: pd.DataFrame):
        return df.groupby(["id", "team"], observed=True).sum()

    num_iteration_simulation = (2, 4)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "1", "2", "2", "2", "3", "3"],
            "team": ["A", "B", "C", "a", "b", "c", "1", "2"],
            "s0": [0, 3, 3, 2, 1, 1, 2, 2],
            "s1": [0, 3, 3, 2, 1, 1, 2, 2],
            "s2": [0, 3, 3, 2, 1, 1, 2, 2],
            "s3": [0, 3, 3, 2, 1, 1, 2, 2],
            "s4": [0, 3, 3, 2, 1, 1, 2, 2],
            "s5": [0, 3, 3, 2, 1, 1, 2, 2],
            "s6": [0, 3, 3, 2, 1, 1, 2, 2],
            "s7": [0, 3, 3, 2, 1, 1, 2, 2],
        }
    ).set_index(["id", "team"])

    simulations = batch.batch_simulate_points_per_match(
        id_to_probabilities_ppm,
        id_to_num_matches,
        data_to_join_second.set_index("team", append=True).index,
        num_iteration_simulation,
        func_after_simulation=get_rankings,
    )

    assert simulations.equals(expected)


def test_batch_simulate_points_per_match_with_func_after_two(
    id_to_probabilities_ppm: pd.Series,
    id_to_num_matches: pd.Series,
    data_to_join_second: pd.DataFrame,
):

    # apply func
    def add_three(df: pd.DataFrame):
        return df + 3

    num_iteration_simulation = (2, 3)
    expected = pd.DataFrame(
        {
            "id": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
            "date number": [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            "s0": [3, 6, 3, 6, 4, 4, 4, 4, 4, 4, 4, 4],
            "s1": [3, 6, 3, 6, 4, 4, 4, 4, 4, 4, 4, 4],
            "s2": [3, 6, 3, 6, 4, 4, 4, 4, 4, 4, 4, 4],
            "s3": [3, 6, 3, 6, 4, 4, 4, 4, 4, 4, 4, 4],
            "s4": [3, 6, 3, 6, 4, 4, 4, 4, 4, 4, 4, 4],
            "s5": [3, 6, 3, 6, 4, 4, 4, 4, 4, 4, 4, 4],
        }
    ).set_index(["id", "date number"])

    simulations = batch.batch_simulate_points_per_match(
        id_to_probabilities_ppm,
        id_to_num_matches,
        data_to_join_second.index,
        num_iteration_simulation,
        func_after_simulation=add_three,
    )

    assert simulations.equals(expected)
