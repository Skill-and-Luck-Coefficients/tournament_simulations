from collections import Counter

import pytest

import tournament_simulations.schedules.randomize.randomize_functions as rfunc


@pytest.fixture
def simple_schedule():
    return [((0, 1),), ((2, 0),), ((1, 2),)]


@pytest.fixture
def complex_schedule():
    return [
        (("a", "d"), ("b", "c")),
        (("a", "c"), ("d", "b")),
        (("a", "b"), ("c", "d")),
    ]


def test_shuffle_home_away_in_matches(simple_schedule, complex_schedule):

    original_matches = [(0, 1), (2, 0), (1, 2)]
    flipped_original = [(1, 0), (0, 2), (2, 1)]

    schedule = rfunc.shuffle_home_away_in_matches(simple_schedule)
    flattened_schedule = [match for round_ in schedule for match in round_]

    assert len(flattened_schedule) == len(original_matches)
    assert all(
        (match in original_matches) ^ (match in flipped_original)
        for match in flattened_schedule
    )

    original_matches = [
        ("a", "d"), ("b", "c"), ("a", "c"), ("d", "b"), ("a", "b"), ("c", "d")
    ]
    flipped_original = [
        ("d", "a"), ("c", "b"), ("c", "a"), ("b", "d"), ("b", "a"), ("d", "c")
    ]

    schedule = rfunc.shuffle_home_away_in_matches(complex_schedule)
    flattened_schedule = [match for round_ in schedule for match in round_]

    assert len(flattened_schedule) == len(original_matches)
    assert all(
        (match in original_matches) ^ (match in flipped_original)
        for match in flattened_schedule
    )


def test_shuffle_home_away_in_matches__for_different_order(complex_schedule):

    not_equal_to_original = []

    for _ in range(100):
        result = rfunc.shuffle_home_away_in_matches(complex_schedule)
        not_equal_to_original.append(result != complex_schedule)

    assert any(not_equal_to_original)


def test_shuffle_matches_in_rounds(simple_schedule, complex_schedule):

    result = rfunc.shuffle_matches_in_rounds(simple_schedule)
    counters = [Counter(round_) for round_ in result]

    expected_counters = [Counter(round_) for round_ in simple_schedule]
    assert counters == expected_counters

    result = rfunc.shuffle_matches_in_rounds(complex_schedule)
    counters = [Counter(round_) for round_ in result]

    expected_counters = [Counter(round_) for round_ in complex_schedule]
    assert counters == expected_counters


def test_shuffle_matches_in_rounds__for_different_order(complex_schedule):

    not_equal_to_original = []

    for _ in range(100):
        result = rfunc.shuffle_home_away_in_matches(complex_schedule)
        not_equal_to_original.append(result != complex_schedule)

    assert any(not_equal_to_original)


def test_shuffle_rounds_in_schedule(simple_schedule, complex_schedule):

    result = rfunc.shuffle_rounds_in_schedule(simple_schedule)
    counter = Counter(result)

    expected_counter = Counter(simple_schedule)
    assert counter == expected_counter

    result = rfunc.shuffle_rounds_in_schedule(complex_schedule)
    counter = Counter(result)

    expected_counter = Counter(complex_schedule)
    assert counter == expected_counter


def test_shuffle_rounds_in_schedule__for_different_order(complex_schedule):

    not_equal_to_original = []

    for _ in range(100):
        result = rfunc.shuffle_home_away_in_matches(complex_schedule)
        not_equal_to_original.append(result != complex_schedule)

    assert any(not_equal_to_original)


def test_get_names_from_schedule(simple_schedule, complex_schedule):

    result = rfunc._get_names_from_schedule(simple_schedule)
    expected = [0, 1, 2]

    assert result == expected

    result = rfunc._get_names_from_schedule(complex_schedule)
    expected = ["a", "b", "c", "d"]

    assert result == expected


def test_shuffle_teams(simple_schedule, complex_schedule):

    result = rfunc.shuffle_teams(simple_schedule)
    original_to_new = {}

    for old_round_, round_ in zip(simple_schedule, result):
        for (old_home, old_away), (home, away) in zip(old_round_, round_):
            original_to_new[old_home] = home
            original_to_new[old_away] = away

    old_mapped_to_new = [
        tuple((original_to_new[home], original_to_new[away]) for home, away in round_)
        for round_ in simple_schedule
    ]
    assert result == old_mapped_to_new

    result = rfunc.shuffle_teams(complex_schedule)
    original_to_new = {}

    for old_round_, round_ in zip(complex_schedule, result):
        for (old_home, old_away), (home, away) in zip(old_round_, round_):
            original_to_new[old_home] = home
            original_to_new[old_away] = away

    old_mapped_to_new = [
        tuple((original_to_new[home], original_to_new[away]) for home, away in round_)
        for round_ in complex_schedule
    ]
    assert result == old_mapped_to_new


def test_shuffle_teams__for_different_order(complex_schedule):

    not_equal_to_original = []

    for _ in range(100):
        result = rfunc.shuffle_home_away_in_matches(complex_schedule)
        not_equal_to_original.append(result != complex_schedule)

    assert any(not_equal_to_original)
