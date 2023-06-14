import pytest

import tournament_simulations.schedules.round_robin.single_round_robin as srrs


@pytest.fixture
def single_round_robin():

    return srrs.SingleRoundRobin(
        num_teams=4,
        team_names=list(range(4)),
        schedule=[((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))],
    )


def test_create_full_schedule_not_random(single_round_robin: srrs.SingleRoundRobin):

    num_rounds = len(single_round_robin.schedule)

    one_schedule = list(
        single_round_robin.get_full_schedule(num_schedules=1, to_randomize=None)
    )
    assert single_round_robin.schedule == one_schedule
    assert id(single_round_robin.schedule) != id(one_schedule)

    two_schedules = list(
        single_round_robin.get_full_schedule(num_schedules=2, to_randomize=None)
    )
    assert single_round_robin.schedule == two_schedules[:num_rounds]
    assert single_round_robin.schedule == two_schedules[num_rounds:]

    three_schedules = list(
        single_round_robin.get_full_schedule(num_schedules=3, to_randomize=None)
    )
    assert single_round_robin.schedule == three_schedules[:num_rounds]
    assert single_round_robin.schedule == three_schedules[num_rounds : 2 * num_rounds]
    assert single_round_robin.schedule == three_schedules[2 * num_rounds :]
