from collections import Counter

import pytest

import schedules.round_robin.double_round_robin as drrs
import schedules.round_robin.single_round_robin as srrs


@pytest.fixture
def double_round_robin():

    return drrs.DoubleRoundRobin(
        4,
        srrs.SingleRoundRobin(
            4, [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
        ),
        srrs.SingleRoundRobin(
            4, [((1, 0), (3, 2)), ((2, 0), (3, 1)), ((3, 0), (2, 1))]
        ),
    )


def test_create_full_schedule(double_round_robin: drrs.DoubleRoundRobin):

    one_schedule = double_round_robin.get_full_schedule(num_schedules=1)
    assert all(
        (round in double_round_robin.first_single_round_robin.schedule)
        for round in one_schedule[0:3]
    )
    assert all(
        (round in double_round_robin.second_single_round_robin.schedule)
        for round in one_schedule[3:6]
    )
    counter = Counter(one_schedule)
    assert all(
        counter[round] == 1
        for round in double_round_robin.first_single_round_robin.schedule
    )
    assert all(
        counter[round] == 1
        for round in double_round_robin.second_single_round_robin.schedule
    )

    two_schedules = double_round_robin.get_full_schedule(num_schedules=2)
    assert all(
        (round in double_round_robin.first_single_round_robin.schedule)
        for round in two_schedules[0:3]
    )
    assert all(
        (round in double_round_robin.second_single_round_robin.schedule)
        for round in two_schedules[3:6]
    )
    assert all(
        (round in double_round_robin.first_single_round_robin.schedule)
        for round in two_schedules[6:9]
    )
    assert all(
        (round in double_round_robin.second_single_round_robin.schedule)
        for round in two_schedules[9:12]
    )
    counter = Counter(two_schedules)
    assert all(
        counter[round] == 2
        for round in double_round_robin.first_single_round_robin.schedule
    )
    assert all(
        counter[round] == 2
        for round in double_round_robin.second_single_round_robin.schedule
    )

    three_schedules = double_round_robin.get_full_schedule(num_schedules=3)
    assert all(
        (round in double_round_robin.first_single_round_robin.schedule)
        for round in three_schedules[0:3]
    )
    assert all(
        (round in double_round_robin.second_single_round_robin.schedule)
        for round in three_schedules[3:6]
    )
    assert all(
        (round in double_round_robin.first_single_round_robin.schedule)
        for round in three_schedules[6:9]
    )
    assert all(
        (round in double_round_robin.second_single_round_robin.schedule)
        for round in three_schedules[9:12]
    )
    assert all(
        (round in double_round_robin.first_single_round_robin.schedule)
        for round in three_schedules[12:15]
    )
    assert all(
        (round in double_round_robin.second_single_round_robin.schedule)
        for round in three_schedules[15:18]
    )

    counter = Counter(three_schedules)
    assert all(
        counter[round] == 3
        for round in double_round_robin.first_single_round_robin.schedule
    )
    assert all(
        counter[round] == 3
        for round in double_round_robin.second_single_round_robin.schedule
    )
