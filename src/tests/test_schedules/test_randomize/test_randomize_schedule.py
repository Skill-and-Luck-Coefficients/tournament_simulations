from collections import Counter
from itertools import combinations

import pytest

import tournament_simulations.schedules.randomize.randomize_schedule as rs


@pytest.fixture
def complex_schedule():
    return [
        (("a", "d"), ("b", "c")),
        (("a", "c"), ("d", "b")),
        (("a", "b"), ("c", "d")),
    ]


@pytest.fixture
def schedule(complex_schedule):
    return rs.RandomizeSchedule(complex_schedule, ["a", "b", "c", "d"])


@pytest.fixture
def schedule_no_teams(complex_schedule):
    return rs.RandomizeSchedule(complex_schedule)


def test_randomize_home_away(schedule: rs.RandomizeSchedule):

    original_matches = [
        ("a", "d"), ("b", "c"), ("a", "c"), ("d", "b"), ("a", "b"), ("c", "d")
    ]
    flipped_original = [
        ("d", "a"), ("c", "b"), ("c", "a"), ("b", "d"), ("b", "a"), ("d", "c")
    ]

    schedule = schedule.randomize("home_away")
    flattened_schedule = [match for round_ in schedule for match in round_]

    assert len(flattened_schedule) == len(original_matches)
    assert all(
        (match in original_matches) ^ (match in flipped_original)
        for match in flattened_schedule
    )


def test_randomize_matches(schedule: rs.RandomizeSchedule):

    result = schedule.randomize("matches")
    counters = [Counter(round_) for round_ in result]

    expected_counters = [Counter(round_) for round_ in schedule.schedule]
    assert counters == expected_counters


def test_randomize_rounds(schedule: rs.RandomizeSchedule):

    result = schedule.randomize("rounds")
    counter = Counter(result)

    expected_counter = Counter(schedule.schedule)
    assert counter == expected_counter


def test_randomize_teams(
    schedule: rs.RandomizeSchedule, schedule_no_teams: rs.RandomizeSchedule
):

    result = schedule.randomize("teams")
    original_to_new = {}

    for old_round_, round_ in zip(schedule.schedule, result):
        for (old_home, old_away), (home, away) in zip(old_round_, round_):
            original_to_new[old_home] = home
            original_to_new[old_away] = away

    old_mapped_to_new = [
        tuple((original_to_new[home], original_to_new[away]) for home, away in round_)
        for round_ in schedule.schedule
    ]
    assert result == old_mapped_to_new

    result = schedule_no_teams.randomize("teams")
    original_to_new = {}

    for old_round_, round_ in zip(schedule_no_teams.schedule, result):
        for (old_home, old_away), (home, away) in zip(old_round_, round_):
            original_to_new[old_home] = home
            original_to_new[old_away] = away

    old_mapped_to_new = [
        tuple((original_to_new[home], original_to_new[away]) for home, away in round_)
        for round_ in schedule_no_teams.schedule
    ]
    assert result == old_mapped_to_new


def test_parse_to_randomize():

    schedule = rs.RandomizeSchedule("ScheduleMock", ["a", "b", "c"])

    assert schedule._parse_to_randomize(None) == []
    assert schedule._parse_to_randomize([]) == []

    all_options = ["teams", "home_away", "matches", "rounds"]
    for option in all_options:
        assert schedule._parse_to_randomize(option) == [option]

    assert schedule._parse_to_randomize("all") == sorted(all_options)

    for r in range(1, len(all_options) + 1):
        for options in combinations(all_options, r=r):
            assert schedule._parse_to_randomize(options) == sorted(options)

    options = ["matches", "matches", "teams"]
    assert schedule._parse_to_randomize(options) == sorted(["matches", "teams"])


def test_randomize_empty_options(schedule: rs.RandomizeSchedule):

    for option in [None, []]:
        result = schedule.randomize(option)
        assert result == schedule.schedule
        assert id(result) != id(schedule.schedule)


def test_randomize_iterable_options(schedule: rs.RandomizeSchedule):

    result = schedule.randomize(["matches"])
    counters = [Counter(round_) for round_ in result]

    expected_counters = [Counter(round_) for round_ in schedule.schedule]
    assert counters == expected_counters

    result = schedule.randomize(["matches", "rounds"])

    # Same number of rounds
    assert len(result) == len(schedule.schedule)

    # Same match distribution throughout the rounds
    len_rounds = [len(round_) for round_ in schedule.schedule]
    len_rounds_result = [len(round_) for round_ in result]
    assert sorted(len_rounds) == sorted(len_rounds_result)

    # Finding equivalent round in shuffled tournament
    sorted_matches = [tuple(sorted(round_)) for round_ in schedule.schedule]
    sorted_to_old = dict(zip(sorted_matches, schedule.schedule))

    new_to_old_round_map = dict()

    for round_ in result:
        sorted_shuffled_round = tuple(sorted(round_))
        new_to_old_round_map[round_] = sorted_to_old[sorted_shuffled_round]

    assert all(
        sorted(new) == sorted(old)
        for new, old in new_to_old_round_map.items()
    )
    # Assert that two rounds don't map to the same sorted round (uniqueness)
    assert len(set(new_to_old_round_map.values())) == len(new_to_old_round_map.values())
