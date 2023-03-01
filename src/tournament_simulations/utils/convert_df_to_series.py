import pandas as pd


def convert_df_to_series_of_tuples(df: pd.DataFrame) -> pd.Series:

    """
    Converts a pd.DataFrame to a pd.Series of tuples.

    Example:

        df:
            pd.DataFrame(
                {
                    "index": [0, 1, 2, 3],
                    "col1": ["a", "b", "c", "d"],
                    "col2": ["A", "B", "C", "D"],
                }
            ).set_index("index")

        Returns:

            pd.Series(
                data = [("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")],
                index = [0, 1, 2, 3],
            )
    """

    return pd.Series(df.itertuples(index=False, name=None), df.index)
