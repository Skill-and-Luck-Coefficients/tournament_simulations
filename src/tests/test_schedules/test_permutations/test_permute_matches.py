import pandas as pd
import pytest

import tournament_simulations.schedules.permutation.permute_matches as pm


@pytest.fixture
def matches():

    # Using post initialization for sorting and type casting!
    return pm.Matches(
        pd.DataFrame(
            {
                "id": ["2", "2", "2", "1", "1"],
                "date number": [0, 1, 1, 0, 1],
                "home": ["a", "b", "a", "A", "B"],
                "away": ["c", "a", "c", "B", "A"],
                "winner": ["h", "a", "a", "d", "d"],
            }
        ).set_index(["id", "date number"])
    )


def test_set_original_dates_back(matches: pm.Matches):

    matches_df = pd.DataFrame(
        {
            "id": pd.Categorical(["1", "1", "2", "2", "2"]),
            # only date number has been changed
            "date number": [3, 17, 38, 10, 4895],
            "home": pd.Categorical(["A", "B", "a", "b", "a"]),
            "away": pd.Categorical(["B", "A", "c", "a", "c"]),
            "winner": ["d", "d", "h", "a", "a"],
        }
    ).set_index(["id", "date number"])

    original = matches.df.index.get_level_values("date number")
    assert pm._set_date_numbers(matches_df, original).equals(matches.df)


def test_index_matches_appropriately(matches: pm.Matches):

    expected = pd.DataFrame(
        {
            "id": pd.Categorical(["2"], categories=["1", "2"]),
            "date number": [1],
            "home": pd.Categorical(["b"], categories=["a", "b", "A", "B"]),
            "away": pd.Categorical(["a"], categories=["a", "c", "A", "B"]),
            "winner": ["a"],
        }
    ).set_index(["id", "date number"])

    indexes = [("2", 1, "b", "a")]

    assert pm._index_matches_appropriately(matches.df, indexes).equals(expected)

    expected = pd.DataFrame(
        {
            "id": pd.Categorical(["1", "2", "2"]),
            "date number": [1, 1, 0],
            "home": pd.Categorical(["B", "b", "a"], categories=["a", "b", "A", "B"]),
            "away": pd.Categorical(["A", "a", "c"], categories=["a", "c", "A", "B"]),
            "winner": ["d", "a", "h"],
        }
    ).set_index(["id", "date number"])

    indexes = [("1", 1, "B", "A"), ("2", 1, "b", "a"), ("2", 0, "a", "c")]

    assert pm._index_matches_appropriately(matches.df, indexes).equals(expected)


@pytest.fixture
def simple_matches():

    # Using post initialization for sorting and type casting!
    return pm.Matches(
        pd.DataFrame(
            {
                "id": ["1", "0"],
                "date number": [0, 0],
                "home": ["a", "B"],
                "away": ["c", "C"],
                "winner": ["h", "a"],
            }
        )
    )


@pytest.fixture
def simple_index():

    return pm.OrderedIndex(
        pd.Series(
            index=pd.Categorical(["1", "0"]),
            data=[[("1", 0, "a", "c")], [("0", 0, "B", "C")]],
        )
    )


@pytest.fixture
def complex_matches():

    # Using post initialization for sorting and type casting!
    return pm.Matches(
        pd.DataFrame(
            {
                "id": ["1", "1", "1", "0", "0"],
                "date number": [0, 1, 1, 0, 1],
                "home": ["a", "b", "a", "C", "B"],
                "away": ["c", "a", "c", "A", "D"],
                "winner": ["h", "a", "d", "h", "a"],
            }
        )
    )


@pytest.fixture
def complex_index():

    return pm.OrderedIndex(
        pd.Series(
            index=pd.Categorical(["0", "1"]),
            data=[
                [("0", 1, "B", "D"), ("0", 0, "C", "A")],
                [("1", 1, "b", "a"), ("1", 1, "a", "c"), ("1", 0, "a", "c")]
            ],
        )
    )


def test_permute_matches_simple(
    simple_matches: pm.Matches, simple_index: pm.OrderedIndex
):
    permute_matches = pm.PermuteMatches(simple_matches)
    result = permute_matches.permute_matches(simple_index)
    assert result.df.equals(simple_matches.df)

    for date_numbers in [[10, 10], pd.Series([15, 12])]:
        expected = pm.Matches(
            pd.DataFrame(
                {
                    "id": ["1", "0"],
                    "date number": list(reversed(date_numbers)),
                    "home": ["a", "B"],
                    "away": ["c", "C"],
                    "winner": ["h", "a"],
                }
            )
        )
        result = permute_matches.permute_matches(simple_index, date_numbers)
        assert result.df.equals(expected.df)


def test_permute_matches_complex(
    complex_matches: pm.Matches, complex_index: pm.OrderedIndex
):

    permute_matches = pm.PermuteMatches(complex_matches)

    expected = pm.Matches(
        pd.DataFrame(
            {
                "id": ["1", "1", "1", "0", "0"],
                "date number": [0, 1, 1, 0, 1],
                "home": ["b", "a", "a", "B", "C"],
                "away": ["a", "c", "c", "D", "A"],
                "winner": ["a", "d", "h", "a", "h"],
            }
        )
    )
    result = permute_matches.permute_matches(complex_index)
    assert result.df.equals(expected.df)

    data_numbers = [10, 11, 0, 1, 2]
    expected = pm.Matches(
        pd.DataFrame(
            {
                "id": ["1", "1", "1", "0", "0"],
                "date number": [0, 1, 2, 10, 11],
                "home": ["b", "a", "a", "B", "C"],
                "away": ["a", "c", "c", "D", "A"],
                "winner": ["a", "d", "h", "a", "h"],
            }
        )
    )
    result = permute_matches.permute_matches(complex_index, data_numbers)
    assert result.df.equals(expected.df)
