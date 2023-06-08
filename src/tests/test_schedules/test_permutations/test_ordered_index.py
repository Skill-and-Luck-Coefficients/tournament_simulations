import pandas as pd

import tournament_simulations.schedules.permutation.ordered_index as oi


def test_to_list():

    instance = oi.OrderedIndex(pd.Series(dtype=object))
    assert instance.to_flat_list() == []

    instance = oi.OrderedIndex(
        pd.Series(
            index=pd.Index(pd.Categorical(["1", "3", "4", "2"]), name="id"),
            data=[
                [["one", "1", 1]],
                [["three", "3", 3]],
                [["four", "4", 4]],
                [["two", "2", 2]],
            ],
        )
    )
    expected = [["one", "1", 1], ["two", "2", 2], ["three", "3", 3], ["four", "4", 4]]
    assert instance.to_flat_list() == expected

    instance = oi.OrderedIndex(
        pd.Series(
            index=pd.Index(pd.Categorical(["1", "3", "2"]), name="id"),
            data=[
                [("one", "1", 1)],
                [("three", "3", 3), ("four", "4", 4)],
                [("two", "2", 2)],
            ],
        )
    )
    expected = [("one", "1", 1), ("two", "2", 2), ("three", "3", 3), ("four", "4", 4)]
    assert instance.to_flat_list() == expected
