import pandas as pd

import schedules.permutation.permutation_index as pi


def test_to_list():

    instance = pi.PermutationIndex(pd.Series(dtype=object))
    assert instance.to_flat_list() == []

    instance = pi.PermutationIndex(
        pd.Series(
            index=pd.Index(pd.Categorical(["1", "3", "4", "2"]), name="id"),
            data=[
                ["one", "1", 1],
                ["three", "3", 3],
                ["four", "4", 4],
                ["two", "2", 2],
            ],
        )
    )
    expected = ["one", "1", 1, "two", "2", 2, "three", "3", 3, "four", "4", 4]
    assert instance.to_flat_list() == expected
