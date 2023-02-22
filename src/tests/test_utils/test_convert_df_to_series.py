import pandas as pd

import utils.convert_df_to_series as cds


def test_convert_df_to_series_of_tuples_one():

    test = pd.DataFrame(
        {
            "index": [0, 1, 2, 3],
            "col1": ["a", "b", "c", "d"],
            "col2": ["A", "B", "C", "D"],
        }
    ).set_index("index")

    expected = pd.Series(
        data=[("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")],
        index=[0, 1, 2, 3],
    )

    assert cds.convert_df_to_series_of_tuples(test).equals(expected)


def test_convert_df_to_series_of_tuples_two():

    test = pd.DataFrame(
        {
            "index": ["a", "a", "b", "b", "c"],
            "col1": [0, 1, 2, 3, 4],
            "col2": [5, 6, 7, 8, 9],
            "col3": [10, 11, 12, 13, 14],
        }
    ).set_index("index")

    expected = pd.Series(
        data=[(0, 5, 10), (1, 6, 11), (2, 7, 12), (3, 8, 13), (4, 9, 14)],
        index=["a", "a", "b", "b", "c"],
    )

    assert cds.convert_df_to_series_of_tuples(test).equals(expected)
