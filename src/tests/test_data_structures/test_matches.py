import data_structures as ds
import pandas as pd
import pytest


@pytest.fixture
def first_matches():
    cols = {
        "id": ["2", "2", "2", "1"],
        "date number": [0, 0, 1, 0],
        "home": ["A", "C", "A", "one"],
        "away": ["B", "D", "B", "four"],
        "winner": ["d", "a", "a", "h"],
    }
    df = pd.DataFrame(data=cols).set_index(["id", "date number"])

    return ds.Matches(df)


@pytest.fixture
def second_matches():

    cols = {
        "id": ["1", "1", "2", "2", "2"],
        "date number": [0, 1, 0, 1, 1],
        "home": ["one", "three", "A", "C", "B"],
        "away": ["two", "four", "B", "A", "A"],
        "winner": ["d", "d", "h", "a", "d"],
        "result": ["1-1", "1-1", "1-0", "0-1", "1-1"],
    }
    df = pd.DataFrame(data=cols).set_index(["id", "date number"])

    return ds.Matches(df)


def test_team_names_per_id_first_matches(first_matches: ds.Matches):

    expected_index = ["1", "2"]
    expected_data = [["four", "one"], ["A", "B", "C", "D"]]
    expected = pd.Series(expected_data, expected_index)

    assert first_matches.team_names_per_id.equals(expected)


def test_team_names_per_id_second_matches(second_matches: ds.Matches):

    expected_index = ["1", "2"]
    expected_data = [["four", "one", "three", "two"], ["A", "B", "C"]]
    expected = pd.Series(expected_data, expected_index)

    assert second_matches.team_names_per_id.equals(expected)


def test_number_of_matches_per_id_first_matches(first_matches: ds.Matches):

    expected_index = ["1", "2"]
    expected_data = [1, 3]
    expected = pd.Series(expected_data, expected_index)

    assert first_matches.number_of_matches_per_id.equals(expected)


def test_number_of_matches_per_id_second_matches(second_matches: ds.Matches):

    expected_index = ["1", "2"]
    expected_data = [2, 3]
    expected = pd.Series(expected_data, expected_index)

    assert second_matches.number_of_matches_per_id.equals(expected)


def test_probabilities_per_id_first_matches(first_matches: ds.Matches):

    expected_index = pd.Categorical(["1", "2"])
    expected_data = [
        {"a": 0, "d": 0, "h": 1},
        {"a": 2 / 3, "d": 1 / 3, "h": 0},
    ]
    expected = pd.Series(expected_data, expected_index, name="probabilities")

    assert first_matches.probabilities_per_id().equals(expected)
    assert first_matches.probabilities_per_id(results=None).equals(expected)

    expected_data = [
        {"d": 0, "h": 1},
        {"d": 1 / 3, "h": 0},
    ]
    expected = pd.Series(expected_data, expected_index, name="probabilities")

    assert first_matches.probabilities_per_id(results=["h", "d"]).equals(expected)


def test_probabilities_per_id_second_matches(second_matches: ds.Matches):

    expected_index = pd.Categorical(["1", "2"])
    expected_data = [
        {"a": 0, "d": 1, "h": 0},
        {"a": 1 / 3, "d": 1 / 3, "h": 1 / 3},
    ]
    expected = pd.Series(expected_data, expected_index, name="probabilities")

    assert second_matches.probabilities_per_id().equals(expected)

    expected_data = [
        {"0-1": 0, "1-0": 0, "1-1": 1},
        {"0-1": 1 / 3, "1-0": 1 / 3, "1-1": 1 / 3},
    ]
    expected = pd.Series(expected_data, expected_index, name="probabilities")

    result = second_matches.probabilities_per_id(column="result", results=None)
    assert result.equals(expected)


def test_home_away_winner_first_matches(first_matches: ds.Matches):

    expected_data = [
        ("one", "four", "h"),
        ("A", "B", "d"),
        ("C", "D", "a"),
        ("A", "B", "a"),
    ]
    expected = pd.Series(expected_data, first_matches.df.index)

    assert first_matches.home_away_winner().equals(expected)


def test_home_away_winner_second_matches(second_matches: ds.Matches):

    expected_data = [
        ("one", "two", "d"),
        ("three", "four", "d"),
        ("A", "B", "h"),
        ("C", "A", "a"),
        ("B", "A", "d"),
    ]
    expected = pd.Series(expected_data, second_matches.df.index)

    assert second_matches.home_away_winner().equals(expected)

    expected_data = [
        ("one", "two", "1-1"),
        ("three", "four", "1-1"),
        ("A", "B", "1-0"),
        ("C", "A", "0-1"),
        ("B", "A", "1-1"),
    ]
    expected = pd.Series(expected_data, second_matches.df.index)

    assert second_matches.home_away_winner(winner_type="result").equals(expected)


def test_home_vs_away_count_per_id_first_matches(first_matches: ds.Matches):

    expected = pd.Series(
        index=pd.MultiIndex.from_frame(
            pd.DataFrame(
                {
                    "id": ["1", "2", "2"],
                    "home": ["one", "A", "C"],
                    "away": ["four", "B", "D"],
                }
            ).astype("category")
        ),
        data=[1, 2, 1],
    ).rename("match count")

    assert first_matches.home_vs_away_count_per_id.equals(expected)


def test_home_vs_away_count_per_id_second_matches(second_matches: ds.Matches):

    expected = pd.Series(
        index=pd.MultiIndex.from_frame(
            pd.DataFrame(
                {
                    "id": ["1", "1", "2", "2", "2"],
                    "home": ["one", "three", "A", "B", "C"],
                    "away": ["two", "four", "B", "A", "A"],
                }
            ).astype("category")
        ),
        data=[1, 1, 1, 1, 1],
    ).rename("match count")

    assert second_matches.home_vs_away_count_per_id.equals(expected)
