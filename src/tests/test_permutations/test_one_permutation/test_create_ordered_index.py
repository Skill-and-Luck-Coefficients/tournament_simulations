import pandas as pd
import pytest

import tournament_simulations.permutations.one_permutation.create_ordered_index as coi


def test_generate_all_indexes_one_id():

    id_ = "id"

    dates_numbers = pd.Series(
        index=pd.MultiIndex.from_frame(
            pd.DataFrame(
                {
                    "home": ["a", "b", "c"],
                    "away": ["b", "a", "a"],
                }
            ).astype("category")
        ),
        data=[[1, 2, 3], [3, -1, -1], [-1, 5, -1]],
    )

    matches = (
        (("a", "b"),),
        (("b", "c"),),
        (("a", "c"),),
        (("b", "a"),),
        (("c", "b"),),
        (("c", "a"),),
        (("c", "b"),),
        (("b", "a"),),
        (("c", "a"),),
        (("a", "b"),),
        (("a", "c"),),
        (("b", "c"),),
        (("b", "a"),),
        (("a", "c"),),
        (("a", "b"),),
        (("c", "b"),),
        (("b", "c"),),
        (("c", "a"),),
    )

    expected = [
        ("id", 3, "a", "b"),
        ("id", 5, "c", "a"),
        ("id", 2, "a", "b"),
        ("id", 3, "b", "a"),
        ("id", 1, "a", "b"),
    ]

    assert coi._generate_all_indexes_one_id(matches, dates_numbers, id_) == expected

    dates_numbers = pd.Series(
        index=pd.MultiIndex.from_frame(
            pd.DataFrame(
                {
                    "home": ["a", "b", "c"],
                    "away": ["b", "a", "a"],
                }
            ).astype("category")
        ),
        data=[[1, 2, 3], [3, -1, -1], [-1, 5, -1]],
    )

    matches = (
        (("a", "b"), ("b", "c")),
        (("a", "c"), ("b", "a")),
        (("c", "b"), ("c", "a")),
        (("c", "b"), ("b", "a")),
        (("c", "a"), ("a", "b")),
        (("a", "c"), ("b", "c")),
        (("b", "a"), ("a", "c")),
        (("a", "b"), ("c", "b")),
        (("b", "c"), ("c", "a")),
    )

    expected = [
        ("id", 3, "a", "b"),
        ("id", 5, "c", "a"),
        ("id", 2, "a", "b"),
        ("id", 3, "b", "a"),
        ("id", 1, "a", "b"),
    ]

    assert coi._generate_all_indexes_one_id(matches, dates_numbers, id_) == expected


def test_generate_matches_permutation_index_one_id():

    schedule_list = [
        (("a", "b"), ("b", "c"), ("a", "c"), ("b", "a"), ("c", "b"), ("c", "a")),
        (("c", "b"), ("b", "a"), ("c", "a"), ("a", "b"), ("a", "c"), ("b", "c")),
        (("b", "a"), ("a", "c"), ("a", "b"), ("c", "b"), ("b", "c"), ("c", "a")),
    ]

    schedule = pd.Series(index=["schedule"], data=[schedule_list], name="1")

    matches_dates = pd.Series(
        index=pd.MultiIndex.from_frame(
            pd.DataFrame(
                {
                    "id": ["1", "1", "1"],
                    "home": ["a", "b", "c"],
                    "away": ["b", "a", "a"],
                }
            ).astype("category")
        ),
        data=[[1, 2, 3], [3, -1, -1], [-1, 5, -1]],
    )

    expected = [
        ("1", 3, "a", "b"),
        ("1", 5, "c", "a"),
        ("1", 2, "a", "b"),
        ("1", 3, "b", "a"),
        ("1", 1, "a", "b"),
    ]

    assert (
        coi._generate_matches_permutation_index_one_id(schedule, matches_dates)
        == expected
    )


@pytest.fixture
def id_to_permutation_schedule():

    return pd.DataFrame(
        {
            "id": pd.Categorical(["0", "1"]),
            "schedule": [
                [
                    (("C", "B"), ("B", "C"), ("A", "B")),
                    (("B", "A"), ("C", "B"), ("A", "B")),
                ],
                [
                    (
                        ("a", "b"),
                        ("b", "c"),
                        ("a", "c"),
                        ("b", "a"),
                        ("c", "b"),
                        ("c", "a"),
                    ),
                    (
                        ("c", "b"),
                        ("b", "a"),
                        ("c", "a"),
                        ("a", "b"),
                        ("a", "c"),
                        ("b", "c"),
                    ),
                    (
                        ("b", "a"),
                        ("a", "c"),
                        ("a", "b"),
                        ("c", "b"),
                        ("b", "c"),
                        ("c", "a"),
                    ),
                ],
            ],
        }
    ).set_index("id")["schedule"]


@pytest.fixture
def id_to_matches_dates():

    return pd.Series(
        index=pd.MultiIndex.from_frame(
            pd.DataFrame(
                {
                    "id": ["1", "1", "1", "0", "0"],
                    "home": ["a", "b", "c", "A", "C"],
                    "away": ["b", "a", "a", "B", "B"],
                }
            ).astype("category"),
        ),
        data=[[1, 2, 3], [3, -1, -1], [-1, 5, -1], [0, -1], [3, 2]],
    )


def test_get_kwargs(
    id_to_permutation_schedule: pd.Series,
    id_to_matches_dates: pd.Series,
):

    expected = pd.DataFrame(
        {
            "id": ["0", "1"],
            "index": [
                [("0", 2, "C", "B"), ("0", 3, "C", "B"), ("0", 0, "A", "B")],
                [
                    ("1", 3, "a", "b"),
                    ("1", 5, "c", "a"),
                    ("1", 2, "a", "b"),
                    ("1", 3, "b", "a"),
                    ("1", 1, "a", "b"),
                ],
            ],
        }
    ).set_index("id")["index"]

    params = coi._get_kwargs(id_to_permutation_schedule, id_to_matches_dates)
    assert params["series"].equals(expected)
