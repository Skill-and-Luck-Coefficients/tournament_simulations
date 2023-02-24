import random

import pandas as pd

import schedules.permutation.match_date_numbers as md


def test_create_shuffled_matches_dates_copy():

    random.seed(1)

    test = md.MatchDateNumbers(
        pd.Series(
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
    )

    shuffled = test.create_shuffled_copy().series

    # check that all elements are there
    assert shuffled.apply(sorted).equals(test.series.apply(sorted))

    # check that it is shuffled
    assert any(
        list_shuffled != list_ for list_, list_shuffled in zip(test.series, shuffled)
    )
