import random

import pandas as pd
import pytest

import schedules.permutation.matches_permutation as mp


@pytest.fixture
def matches():

    # Using post initialization for sorting and type casting!
    return mp.Matches(
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


def test_set_original_dates_back(matches: mp.Matches):

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
    assert mp._set_original_date_numbers_back(matches_df, original).equals(matches.df)


def test_get_tournament_matches_from_indexes(matches: mp.Matches):

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

    assert mp._get_tournament_matches_from_indexes(matches.df, indexes).equals(expected)

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

    assert mp._get_tournament_matches_from_indexes(matches.df, indexes).equals(expected)


@pytest.fixture
def simple_matches():

    # Using post initialization for sorting and type casting!
    return mp.Matches(
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
def simple_matches_dates():

    return mp.MatchDateNumbers(
        pd.Series(
            index=pd.MultiIndex.from_frame(
                pd.DataFrame(
                    {
                        "id": ["1", "0"],
                        "home": ["a", "B"],
                        "away": ["c", "C"],
                    }
                ).astype("category")
            ),
            data=[[0], [0]],
        )
    )


@pytest.fixture
def complex_matches():

    # Using post initialization for sorting and type casting!
    return mp.Matches(
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
def complex_matches_dates():

    return mp.MatchDateNumbers(
        pd.Series(
            index=pd.MultiIndex.from_frame(
                pd.DataFrame(
                    {
                        "id": ["1", "1", "0", "0"],
                        "home": ["a", "b", "C", "B"],
                        "away": ["c", "a", "A", "D"],
                    }
                ).astype("category")
            ),
            data=[[0, 1], [-1, 1], [0], [1]],
        )
    )


def test_select_matches_in_the_desired_order_simple(
    simple_matches: mp.Matches, simple_matches_dates: mp.MatchDateNumbers
):

    permutation_schedule = mp.PermutationSchedule(
        pd.Series(
            index=pd.Categorical(["0", "1"]), data=[[(("B", "C"),)], [(("a", "c"),)]]
        )
    )

    assert mp._select_matches_in_the_desired_order(
        simple_matches, permutation_schedule, simple_matches_dates
    ).df.equals(simple_matches.df)


def test_select_matches_in_the_desired_order_complex(
    complex_matches: mp.Matches, complex_matches_dates: mp.MatchDateNumbers
):

    permutation_schedule = mp.PermutationSchedule(
        pd.Series(
            index=pd.Categorical(["0", "1"]),
            data=[
                [(("B", "D"), ("A", "D"), ("C", "A"))],
                [(("b", "a"), ("a", "c")), (("b", "c"), ("a", "c"))],
            ],
        )
    )

    expected = mp.Matches(
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

    assert mp._select_matches_in_the_desired_order(
        complex_matches, permutation_schedule, complex_matches_dates
    ).df.equals(expected.df)


def test_create_one_permutation_simple(
    simple_matches: mp.Matches, simple_matches_dates: mp.MatchDateNumbers
):
    for _ in range(5):
        assert mp.create_one_permutation(
            simple_matches, simple_matches_dates
        ).df.equals(simple_matches.df)


def test_create_one_permutation_complex(
    complex_matches: mp.Matches, complex_matches_dates: mp.MatchDateNumbers
):

    random.seed(5)

    original_data = list(
        complex_matches.df.reset_index("date number").itertuples(index=False, name=None)
    )

    different_ordering = []

    for _ in range(10):

        # check that all matches were considered
        permutations = mp.create_one_permutation(
            complex_matches, complex_matches_dates
        ).df

        permuted_data = list(
            permutations.reset_index("date number").itertuples(index=False, name=None)
        )
        assert len(original_data) == len(permuted_data)

        set_no_id_original = set(data[1:] for data in original_data)
        assert all(data[1:] in set_no_id_original for data in permuted_data)

        set_no_id_permuted = set(data[1:] for data in permuted_data)
        assert all(data[1:] in set_no_id_permuted for data in original_data)

        # check that the ordering is different
        different_ordering.append(
            permutations["home"].to_list() != complex_matches.df["home"].to_list()
        )

    # any true means that there was an iteration with different ordering
    assert any(different_ordering)
