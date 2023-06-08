import pandas as pd

import tournament_simulations.utils.series_of_functions as sof


def test_call_functions_with_their_parameters():

    parameters = pd.Series([0, 1, 2, 3]).apply(lambda number: [number])
    functions = pd.Series([lambda i: i + 1, lambda i: 2*i, lambda i: 2*i, lambda _: 0])

    expected = pd.Series([1, 2, 4, 0])
    result = sof.call_functions_with_their_parameters(functions, parameters)
    assert result.equals(expected)

    parameters = pd.Series([0, 1, 2, 3]).apply(lambda number: [number])
    functions = {
        0: lambda i: i + 1,
        1: lambda i: 2*i,
        2: lambda i: 2*i,
        3: lambda _: 0
    }

    expected = pd.Series([1, 2, 4, 0])
    result = sof.call_functions_with_their_parameters(functions, parameters)
    assert result.equals(expected)

    parameters = pd.Series([0, 1, 2, 3]).apply(lambda number: [number])
    functions = pd.Series(
        [
            lambda i: (i + 1, i + 2),
            lambda i: (2*i, 3*i),
            lambda i: (2*i, 4*i),
            lambda _: [0, 1]
        ]
    )

    expected = pd.Series([(1, 2), (2, 3), (4, 8), [0, 1]])
    result = sof.call_functions_with_their_parameters(functions, parameters)
    assert result.equals(expected)
