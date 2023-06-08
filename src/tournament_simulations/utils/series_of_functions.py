from typing import Callable, Mapping, TypeVar

import pandas as pd

KT = TypeVar("KT")
InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


def call_functions_with_their_parameters(
    key_to_func: Mapping[KT, Callable[[InputT], OutputT]],
    key_to_func_parameters: pd.Series,
) -> pd.Series:
    """
    Call the function for each key separately with its appropriate parameters.

    ----
    Parameters:
        key_to_func: Mapping[KT, Callable[[InputT], OutputT]]
            Dict-like mapping keys to functions.

            Input of the function will be a sequence of its parameters.

        key_to_func_parameters: pd.Series
            Maps each key (KT from key_to_func) to its parameters (Iterable).

            Parameters are unpacked, so they should always be an Iterable.

    ----
    Returns:
        pd.Series
            Maps each key (KT) to its respective function output (OutputT).

    """
    def _call_func_with_its_parameters(series: pd.Series) -> OutputT:
        parameters = series.iloc[0]
        return key_to_func[series.name](*parameters)

    key_to_func_parameters = key_to_func_parameters.to_frame()
    return key_to_func_parameters.apply(_call_func_with_its_parameters, axis="columns")
