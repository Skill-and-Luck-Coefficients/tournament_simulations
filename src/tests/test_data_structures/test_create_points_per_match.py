import data_structures as ds
import data_structures.points_per_match.create_points_per_match as cppm
import pandas as pd


def test_get_teams_points_per_match_first():

    values = [("A", "B", "a"), ("B", "C", "h"), ("a", "b", "d")]
    index = ["1", "1", "2"]
    test = pd.Series(values, index)

    result_to_points = {"h": (3, 0), "d": (1, 1), "a": (0, 3)}

    expected_values = [("A", 0), ("B", 3), ("B", 3), ("C", 0), ("a", 1), ("b", 1)]
    expected_index = ["1", "1", "1", "1", "2", "2"]
    expected = pd.Series(expected_values, expected_index)

    assert cppm._get_teams_points_per_match(test, result_to_points).equals(expected)

    result_to_points = {"h": (2, 1), "d": (0, 0), "a": (1, 2)}

    expected_values = [("A", 1), ("B", 2), ("B", 2), ("C", 1), ("a", 0), ("b", 0)]
    expected_index = ["1", "1", "1", "1", "2", "2"]
    expected = pd.Series(expected_values, expected_index)

    assert cppm._get_teams_points_per_match(test, result_to_points).equals(expected)


def test_get_teams_points_per_match_second():

    values = [("A", "C", "2-3"), ("B", "C", "1-1"), ("a", "d", "1-3"), ("a", "b", "n")]
    index = ["1", "1", "2", "2"]
    test = pd.Series(values, index)

    result_to_points = {"2-3": (1, 2), "1-1": (1, 1), "1-3": (0, 3)}

    expected_values = [("A", 1), ("C", 2), ("B", 1), ("C", 1), ("a", 0), ("d", 3)]
    expected_index = ["1", "1", "1", "1", "2", "2"]
    expected = pd.Series(expected_values, expected_index)

    assert cppm._get_teams_points_per_match(test, result_to_points).equals(expected)


def test_create_points_per_match_first():

    test_cols = {
        "id": ["1", "1", "2", "2", "2"],
        "date number": [0, 1, 0, 1, 2],
        "home": ["A", "B", "a", "a", "a"],
        "away": ["C", "C", "d", "b", "b"],
        "winner": ["d", "a", "h", "h", "d"],
    }
    test = ds.Matches(
        pd.DataFrame(data=test_cols).set_index(["id", "date number"])
    ).home_away_winner()

    expected_cols = {
        "id": ["1", "1", "1", "1", "2", "2", "2", "2", "2", "2"],
        "date number": [0, 0, 1, 1, 0, 0, 1, 1, 2, 2],
        "team": ["A", "C", "B", "C", "a", "d", "a", "b", "a", "b"],
        "points": [1, 1, 0, 3, 3, 0, 3, 0, 1, 1],
    }
    expected = (
        pd.DataFrame(expected_cols)
        .astype({"id": "category"})
        .set_index(["id", "date number"])
    )

    result_to_points = {"h": (3, 0), "d": (1, 1), "a": (0, 3)}
    ppm = cppm.get_kwargs_from_home_away_winner(test, result_to_points)["df"]
    assert ppm.equals(expected)


def test_create_points_per_match_second():

    test_cols = {
        "id": ["1", "2", "2", "3", "3", "3"],
        "date number": [0, 0, 1, 0, 0, 1],
        "home": [
            "A",
            "d",
            "a",
            "one",
            "three",
            "one",
        ],
        "away": [
            "C",
            "b",
            "d",
            "two",
            "four",
            "two",
        ],
        "winner": [
            "h",
            "d",
            "d",
            "a",
            "na",
            "d",
        ],
        "result": [
            "3:0",
            "1:1",
            "1:1",
            "0:3",
            "na",
            "1:1",
        ],
    }
    test = ds.Matches(
        pd.DataFrame(data=test_cols).set_index(["id", "date number"])
    ).home_away_winner("result")

    expected_cols = {
        "id": ["1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
        "date number": [0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
        "team": ["A", "C", "d", "b", "a", "d", "one", "two", "one", "two"],
        "points": [3, 0, 1, 1, 1, 1, 0, 3, 1, 1],
    }
    expected = (
        pd.DataFrame(expected_cols)
        .astype({"id": "category"})
        .set_index(["id", "date number"])
    )

    result_to_points = {"3:0": (3, 0), "1:1": (1, 1), "0:3": (0, 3)}
    ppm = cppm.get_kwargs_from_home_away_winner(test, result_to_points)["df"]
    assert ppm.equals(expected)
