import pandas as pd
import pytest

import tournament_simulations.permutations.matches_permutations as mp


@pytest.fixture()
def matches():
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


@pytest.fixture()
def scheduler():
    return mp.TournamentScheduler(
        {
            "0": lambda p: [(("B", "C"),)],
            "1": lambda p: [(("a", "c"),)]
        },
        pd.Series(
            index=["1", "0"],
            data=[[0], [0]]
        )
    )


def test_create_n_permutations(matches, scheduler):

    permutations = mp.MatchesPermutations(matches, scheduler)

    # Using post initialization for sorting and type casting!
    expected = mp.Matches(
        pd.DataFrame(
            {
                "id": ["1@0", "0@0"],
                "date number": [0, 0],
                "home": ["a", "B"],
                "away": ["c", "C"],
                "winner": ["h", "a"],
            }
        )
    )

    assert permutations.create_n_permutations(1).df.equals(expected.df)

    # Using post initialization for sorting and type casting!
    expected = mp.Matches(
        pd.DataFrame(
            {
                "id": ["1@0", "0@0", "1@1", "0@1"],
                "date number": [0, 0, 0, 0],
                "home": ["a", "B", "a", "B"],
                "away": ["c", "C", "c", "C"],
                "winner": ["h", "a", "h", "a"],
            }
        )
    )

    assert permutations.create_n_permutations(2).df.equals(expected.df)


def test_create_n_permutations_with_identifiers(matches, scheduler):

    permutations = mp.MatchesPermutations(matches, scheduler)

    # Using post initialization for sorting and type casting!
    expected = mp.Matches(
        pd.DataFrame(
            {
                "id": ["1@ok", "0@ok"],
                "date number": [0, 0],
                "home": ["a", "B"],
                "away": ["c", "C"],
                "winner": ["h", "a"],
            }
        )
    )

    result = permutations.create_n_permutations(["ok"])
    assert result.df.equals(expected.df)

    expected = mp.Matches(
        pd.DataFrame(
            {
                "id": ["1@10", "0@10"],
                "date number": [0, 0],
                "home": ["a", "B"],
                "away": ["c", "C"],
                "winner": ["h", "a"],
            }
        )
    )

    result = permutations.create_n_permutations([10])
    assert result.df.equals(expected.df)

    # Using post initialization for sorting and type casting!
    expected = mp.Matches(
        pd.DataFrame(
            {
                "id": ["1@one", "0@one", "1@random_text", "0@random_text"],
                "date number": [0, 0, 0, 0],
                "home": ["a", "B", "a", "B"],
                "away": ["c", "C", "c", "C"],
                "winner": ["h", "a", "h", "a"],
            }
        )
    )

    result = permutations.create_n_permutations(["one", "random_text"])
    assert result.df.equals(expected.df)
