import pandas as pd
import pytest

import data_structures as ds


@pytest.fixture
def first_matches():
    cols = {
        "id": ["1", "2", "2"],
        "date number": [0, 0, 0],
        "home": ["one", "A", "C"],
        "away": ["four", "B", "D"],
        "winner": ["h", "d", "a"],
    }
    df = pd.DataFrame(data=cols).set_index(["id", "date number"])

    return ds.mat.Matches(df)


@pytest.fixture
def second_matches():

    cols = {
        "id": ["1", "1", "2", "2", "2"],
        "date number": [0, 1, 0, 1, 1],
        "home": ["one", "three", "A", "B", "C"],
        "away": ["two", "four", "B", "A", "A"],
        "winner": ["d", "d", "h", "a", "d"],
    }
    df = pd.DataFrame(data=cols).set_index(["id", "date number"])

    return ds.mat.Matches(df)


def test_number_of_matches_per_id_first_matches(first_matches: ds.mat.Matches):

    expected_index = ["1", "2"]
    expected_data = [1, 2]
    expected = pd.Series(expected_data, expected_index)

    assert first_matches.number_of_matches_per_id.equals(expected)


def test_number_of_matches_per_id_second_matches(second_matches: ds.mat.Matches):

    expected_index = ["1", "2"]
    expected_data = [2, 3]
    expected = pd.Series(expected_data, expected_index)

    assert second_matches.number_of_matches_per_id.equals(expected)


def test_probabilities_per_id_first_matches(first_matches: ds.mat.Matches):

    expected_index = ["1", "2"]
    expected_data = [(1, 0, 0), (0, 0.5, 0.5)]
    expected = pd.Series(expected_data, expected_index)

    assert first_matches.probabilities_per_id.equals(expected)


def test_probabilities_per_id_second_matches(second_matches: ds.mat.Matches):

    expected_index = ["1", "2"]
    expected_data = [(0, 1, 0), (1 / 3, 1 / 3, 1 / 3)]
    expected = pd.Series(expected_data, expected_index)

    assert second_matches.probabilities_per_id.equals(expected)


def test_home_away_winner_first_matches(first_matches: ds.mat.Matches):

    expected_data = [("one", "four", "h"), ("A", "B", "d"), ("C", "D", "a")]
    expected = pd.Series(expected_data, first_matches.df.index)

    assert first_matches.home_away_winner.equals(expected)


def test_home_away_winner_second_matches(second_matches: ds.mat.Matches):

    expected_data = [
        ("one", "two", "d"),
        ("three", "four", "d"),
        ("A", "B", "h"),
        ("B", "A", "a"),
        ("C", "A", "d"),
    ]
    expected = pd.Series(expected_data, second_matches.df.index)

    assert second_matches.home_away_winner.equals(expected)