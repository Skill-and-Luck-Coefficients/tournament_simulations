from collections import Counter

import pytest

import schedules.round_robin.single_round_robin as srrs


@pytest.fixture
def single_round_robin():

    return srrs.SingleRoundRobin(
        4, [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    )


def test_create_full_schedule(single_round_robin: srrs.SingleRoundRobin):

    one_schedule = single_round_robin.get_full_schedule(num_schedules=1)
    assert all((round in single_round_robin.schedule) for round in one_schedule)
    counter = Counter(one_schedule)
    assert all(counter[round] == 1 for round in single_round_robin.schedule)

    two_schedules = single_round_robin.get_full_schedule(num_schedules=2)
    for i, j in zip([0, 3], [3, 6]):
        assert all(
            (round in single_round_robin.schedule) for round in two_schedules[i:j]
        )
    counter = Counter(two_schedules)
    assert all(counter[round] == 2 for round in single_round_robin.schedule)

    three_schedules = single_round_robin.get_full_schedule(num_schedules=3)
    for i, j in zip([0, 3, 6], [3, 6, 9]):
        assert all(
            (round in single_round_robin.schedule) for round in three_schedules[i:j]
        )
    counter = Counter(three_schedules)
    assert all(counter[round] == 3 for round in single_round_robin.schedule)
