import numpy as np
import pandas as pd
import pytest

import data_structures as ds


@pytest.fixture
def ppm_one():

    test = {
        "id": ["1", "1", "1", "1", "2", "2", "2", "2", "2", "2", "3", "3", "3", "3"],
        "team": ["A", "B", "A", "C", "a", "b", "c", "d", "c", "b", "o", "t", "t", "o"],
        "points": [1, 1, 3, 0, 0, 3, 1, 1, 0, 3, 1, 1, 0, 3],
        "date number": [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2],
    }

    return ds.ppm.PointsPerMatch(
        pd.DataFrame(data=test)
        .astype({"id": "category", "team": "category", "points": np.int16})
        .set_index(["id", "date number"])
    )


@pytest.fixture
def ppm_two():

    cols = {
        "id": ["1", "1", "1", "1", "2", "2", "2", "2", "2", "2"],
        "team": ["one", "two", "three", "four", "a1", "a2", "a3", "a4", "a5", "a6"],
        "points": [1, 1, 1, 1, 0, 3, 1, 1, 3, 0],
        "date number": [0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    }
    return ds.ppm.PointsPerMatch(
        pd.DataFrame(data=cols)
        .astype({"id": "category", "team": "category", "points": np.int16})
        .set_index(["id", "date number"])
    )


def test_team_names_per_id_ppm_one(ppm_one: ds.ppm.PointsPerMatch):

    expected_values = [{"A", "B", "C"}, {"a", "b", "c", "d"}, {"o", "t"}]
    expected = pd.Series(
        data=expected_values, index=pd.Index(["1", "2", "3"], dtype="category")
    )
    assert ppm_one.team_names_per_id.equals(expected)


def test_team_names_per_id_ppm_two(ppm_two: ds.ppm.PointsPerMatch):

    expected_values = [
        {"one", "two", "three", "four"},
        {"a1", "a2", "a3", "a4", "a5", "a6"},
    ]
    expected = pd.Series(
        data=expected_values, index=pd.Index(["1", "2"], dtype="category")
    )
    assert ppm_two.team_names_per_id.equals(expected)


def test_number_of_matches_per_id_ppm_one(ppm_one: ds.ppm.PointsPerMatch):

    expected_values = [2, 3, 2]
    expected = pd.Series(
        data=expected_values, index=pd.Index(["1", "2", "3"], dtype="category")
    )
    assert ppm_one.number_of_matches_per_id.equals(expected)


def test_number_of_matches_per_id_ppm_two(ppm_two: ds.ppm.PointsPerMatch):

    expected_values = [2, 3]
    expected = pd.Series(
        data=expected_values, index=pd.Index(["1", "2"], dtype="category")
    )
    assert ppm_two.number_of_matches_per_id.equals(expected)


def test_probabilities_per_id_ppm_one(ppm_one: ds.ppm.PointsPerMatch):

    expected_values = [
        (
            0.5,
            0.5,
            0,
        ),
        (
            0,
            1 / 3,
            2 / 3,
        ),
        (
            0,
            0.5,
            0.5,
        ),
    ]
    expected = pd.Series(
        data=expected_values, index=pd.Index(["1", "2", "3"], dtype="category")
    )
    assert ppm_one.probabilities_per_id.equals(expected)


def test_probabilities_per_id_ppm_two(ppm_two: ds.ppm.PointsPerMatch):

    expected_values = [
        (
            0,
            1,
            0,
        ),
        (
            1 / 3,
            1 / 3,
            1 / 3,
        ),
    ]
    expected = pd.Series(
        data=expected_values, index=pd.Index(["1", "2"], dtype="category")
    )
    assert ppm_two.probabilities_per_id.equals(expected)


def test_rankings_ppm_one(ppm_one: ds.ppm.PointsPerMatch):

    expected_cols = {
        "id": ["1", "1", "1", "2", "2", "2", "2", "3", "3"],
        "team": ["A", "B", "C", "a", "b", "c", "d", "o", "t"],
        "points": [4, 1, 0, 0, 6, 1, 1, 4, 1],
    }
    expected = (
        pd.DataFrame(data=expected_cols)
        .astype({"id": "category", "team": "category", "points": np.int16})
        .set_index(["id", "team"])
    )
    assert ppm_one.rankings.equals(expected)


def test_rankings_ppm_two(ppm_two: ds.ppm.PointsPerMatch):

    expected_cols = {
        "id": ["1", "1", "1", "1", "2", "2", "2", "2", "2", "2"],
        "team": ["four", "one", "three", "two", "a1", "a2", "a3", "a4", "a5", "a6"],
        "points": [1, 1, 1, 1, 0, 3, 1, 1, 3, 0],
    }
    expected = (
        pd.DataFrame(data=expected_cols)
        .astype({"id": "category", "team": "category", "points": np.int16})
        .set_index(["id", "team"])
    )
    assert ppm_two.rankings.equals(expected)
