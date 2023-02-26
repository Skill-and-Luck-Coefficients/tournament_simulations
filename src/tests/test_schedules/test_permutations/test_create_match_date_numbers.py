import pandas as pd

import data_structures as ds
import schedules.permutation.create_match_date_numbers as cmd


def test_get_date_numbers_per_match():

    test = ds.mat.Matches(
        pd.DataFrame(
            {
                "id": ["1", "1", "1", "1", "3", "3", "3", "3", "3", "2"],
                "home": ["a", "b", "a", "a", "A", "C", "C", "C", "A", "two"],
                "away": ["b", "c", "b", "b", "C", "B", "B", "B", "C", "one"],
                "date number": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            }
        ).set_index(["id", "date number"])
    )

    expected = pd.Series(
        index=pd.MultiIndex.from_frame(
            pd.DataFrame(
                {
                    "id": ["1", "1", "2", "3", "3"],
                    "home": ["a", "b", "two", "A", "C"],
                    "away": ["b", "c", "one", "C", "B"],
                }
            ).astype("category")
        ),
        data=[[1, 3, 4], [2], [10], [5, 9], [6, 7, 8]],
    )

    assert cmd._get_date_numbers_per_match(test).equals(expected)


def test_fill_date_number_one_line():

    matches_date_numbers = pd.Series(
        index=pd.MultiIndex.from_arrays(
            [
                ["1", "1", "2", "3", "3"],
                ["a", "b", "two", "A", "C"],
                ["b", "c", "one", "C", "B"],
            ],
            names=["id", "home", "away"],
        ),
        data=[[1, 3, 4], [2], [10], [5, 9], [6, 7, 8]],
    )

    id_to_num_schedules = pd.Series(index=["1", "2", "3"], data=[3, 1, 3])

    expected = pd.Series(
        index=pd.MultiIndex.from_arrays(
            [
                ["1", "1", "2", "3", "3"],
                ["a", "b", "two", "A", "C"],
                ["b", "c", "one", "C", "B"],
            ],
            names=["id", "home", "away"],
        ),
        data=[[1, 3, 4], [2, -1, -1], [10], [5, 9, -1], [6, 7, 8]],
        name="num schedules",
    )

    assert cmd._fill_date_numbers_per_match_per_id(
        matches_date_numbers, id_to_num_schedules
    ).equals(expected)


def test_get_kwargs_from_matches():

    matches = ds.mat.Matches(
        pd.DataFrame(
            {
                "id": ["1", "1", "1", "1", "3", "3", "3", "3", "3", "2"],
                "home": ["a", "b", "a", "a", "A", "C", "C", "C", "A", "two"],
                "away": ["b", "c", "b", "b", "C", "B", "B", "B", "C", "one"],
                "date number": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            }
        ).set_index(["id", "date number"])
    )

    expected = pd.Series(
        index=pd.MultiIndex.from_frame(
            pd.DataFrame(
                {
                    "id": ["1", "1", "2", "3", "3"],
                    "home": ["a", "b", "two", "A", "C"],
                    "away": ["b", "c", "one", "C", "B"],
                }
            ).astype("category")
        ),
        data=[[1, 3, 4], [2, -1, -1], [10], [5, 9, -1], [6, 7, 8]],
        name="num schedules",
    )

    assert cmd.get_kwargs_from_matches(matches)["series"].equals(expected)
