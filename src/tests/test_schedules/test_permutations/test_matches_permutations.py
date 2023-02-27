import pandas as pd

import schedules.permutation.matches_permutations as mp


def test_create_n_permutations():

    # Using post initialization for sorting and type casting!
    matches = mp.Matches(
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

    permutations = mp.MatchesPermutations(matches)

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
