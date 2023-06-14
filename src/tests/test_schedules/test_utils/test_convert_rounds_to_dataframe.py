import pandas as pd

import tournament_simulations.schedules.utils.convert_rounds_to_dataframe as crd


def test_convert_list_of_rounds_to_dataframe():

    rounds = [((0, 1),), ((0, 2),), ((3, 0),), ((1, 0),)]
    expected_cols = {
        "id": ["id"] * 4,
        "date number": [0, 1, 2, 3],
        "home": [0, 0, 3, 1],
        "away": [1, 2, 0, 0],
    }
    expected = pd.DataFrame(expected_cols).set_index(["id", "date number"])

    rounds = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((3, 0), (2, 1)), ((1, 0), (3, 2))]
    expected_cols = {
        "id": ["id"] * 8,
        "date number": [0, 0, 1, 1, 2, 2, 3, 3],
        "home": [0, 2, 0, 1, 3, 2, 1, 3],
        "away": [1, 3, 2, 3, 0, 1, 0, 2],
    }
    expected = pd.DataFrame(expected_cols).set_index(["id", "date number"])

    assert crd.convert_list_of_rounds_to_dataframe(rounds, "id").equals(expected)

    rounds = [((3, 2), (0, 1)), ((2, 0), (1, 3)), ((2, 1), (3, 0)), ((1, 0), (2, 3))]
    expected_cols = {
        "id": ["ok"] * 8,
        "date number": [0, 0, 1, 1, 2, 2, 3, 3],
        "home": [3, 0, 2, 1, 2, 3, 1, 2],
        "away": [2, 1, 0, 3, 1, 0, 0, 3],
    }
    expected = pd.DataFrame(expected_cols).set_index(["id", "date number"])

    assert crd.convert_list_of_rounds_to_dataframe(rounds, "ok").equals(expected)
