from collections import Counter

import pytest

import schedules.round_robin.single_round_robin as srrs


@pytest.fixture
def single_round_robin():

    return srrs.SingleRoundRobin(
        4, [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    )


def test_create_full_schedule_not_random(single_round_robin: srrs.SingleRoundRobin):

    num_rounds = len(single_round_robin.schedule)

    one_schedule = list(
        single_round_robin.get_full_schedule(num_schedules=1, randomize_rounds=False)
    )
    assert single_round_robin.schedule == one_schedule

    two_schedules = list(
        single_round_robin.get_full_schedule(num_schedules=2, randomize_rounds=False)
    )
    assert single_round_robin.schedule == two_schedules[:num_rounds]
    assert single_round_robin.schedule == two_schedules[num_rounds:]

    three_schedules = list(
        single_round_robin.get_full_schedule(num_schedules=3, randomize_rounds=False)
    )
    assert single_round_robin.schedule == three_schedules[:num_rounds]
    assert single_round_robin.schedule == three_schedules[num_rounds : 2 * num_rounds]
    assert single_round_robin.schedule == three_schedules[2 * num_rounds :]


def test_create_full_schedule(single_round_robin: srrs.SingleRoundRobin):

    one_schedule = list(single_round_robin.get_full_schedule(num_schedules=1))
    assert all((round in single_round_robin.schedule) for round in one_schedule)
    counter = Counter(one_schedule)
    assert all(counter[round] == 1 for round in single_round_robin.schedule)

    two_schedules = list(single_round_robin.get_full_schedule(num_schedules=2))
    for i, j in zip([0, 3], [3, 6]):
        assert all(
            (round in single_round_robin.schedule) for round in two_schedules[i:j]
        )
    counter = Counter(two_schedules)
    assert all(counter[round] == 2 for round in single_round_robin.schedule)

    three_schedules = list(single_round_robin.get_full_schedule(num_schedules=3))
    for i, j in zip([0, 3, 6], [3, 6, 9]):
        assert all(
            (round in single_round_robin.schedule) for round in three_schedules[i:j]
        )
    counter = Counter(three_schedules)
    assert all(counter[round] == 3 for round in single_round_robin.schedule)
