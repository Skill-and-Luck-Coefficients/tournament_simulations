import pytest

import tournament_simulations.schedules.round_robin.double_round_robin as drrs


@pytest.fixture
def double_round_robin():

    return drrs.DoubleRoundRobin(
        num_teams=4,
        team_names=list(range(4)),
        first_schedule=[((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))],
    )


def test_second_schedule(double_round_robin: drrs.DoubleRoundRobin):

    expected = [((1, 0),), ((2, 0),), ((2, 1),)]
    assert (
        drrs.DoubleRoundRobin(
            4,
            list(range(4)),
            [((0, 1),), ((0, 2),), ((1, 2),)],
        ).second_schedule
        == expected
    )

    expected = [((1, 0), (3, 2)), ((2, 0), (3, 1)), ((3, 0), (2, 1))]
    assert double_round_robin.second_schedule == expected


def test_create_full_schedule_not_random(double_round_robin: drrs.DoubleRoundRobin):

    num_rounds = len(double_round_robin.first_schedule)
    first_schedule = double_round_robin.first_schedule
    second_schedule = double_round_robin.second_schedule

    one_schedule = list(
        double_round_robin.get_full_schedule(
            num_schedules=1, to_randomize_first=None, to_randomize_second=None
        )
    )
    assert double_round_robin.first_schedule == one_schedule[:num_rounds]
    assert double_round_robin.second_schedule == one_schedule[num_rounds:]

    two_schedules = list(
        double_round_robin.get_full_schedule(
            num_schedules=2, to_randomize_first=None, to_randomize_second=None
        )
    )
    assert first_schedule == two_schedules[:num_rounds]
    assert second_schedule == two_schedules[num_rounds : 2 * num_rounds]
    assert first_schedule == two_schedules[2 * num_rounds : 3 * num_rounds]
    assert second_schedule == two_schedules[3 * num_rounds :]

    


def test_create_full_schedule_not_random_flipped(
    double_round_robin: drrs.DoubleRoundRobin
):

    num_rounds = len(double_round_robin.first_schedule)
    first_schedule = double_round_robin.first_schedule

    one_schedule = list(
        double_round_robin.get_full_schedule(
            num_schedules=1, to_randomize_first=None, to_randomize_second="flipped"
        )
    )
    simulated_first = one_schedule[:num_rounds]
    assert first_schedule == simulated_first
    flipped = [tuple((a, h) for h, a in match) for match in simulated_first]
    assert flipped == one_schedule[num_rounds:]

    two_schedules = list(
        double_round_robin.get_full_schedule(
            num_schedules=2, to_randomize_first=None, to_randomize_second="mirrored"
        )
    )
    simulated_first = two_schedules[:num_rounds]
    assert first_schedule == simulated_first
    flipped = [tuple((a, h) for h, a in match) for match in simulated_first]
    assert flipped == two_schedules[num_rounds : 2 * num_rounds]

    simulated_first = two_schedules[2 * num_rounds : 3 * num_rounds]
    assert first_schedule == simulated_first
    flipped = [tuple((a, h) for h, a in match) for match in simulated_first]
    assert flipped == two_schedules[3 * num_rounds :]


def test_create_full_schedule_not_random_reversed(
    double_round_robin: drrs.DoubleRoundRobin
):

    num_rounds = len(double_round_robin.first_schedule)
    first_schedule = double_round_robin.first_schedule

    one_schedule = list(
        double_round_robin.get_full_schedule(
            num_schedules=1, to_randomize_first=None, to_randomize_second="reversed"
        )
    )
    simulated_first = one_schedule[:num_rounds]
    assert first_schedule == simulated_first
    flipped = [
        tuple((a, h) for h, a in reversed(match))
        for match in reversed(simulated_first)
    ]
    assert flipped == one_schedule[num_rounds:]

    two_schedules = list(
        double_round_robin.get_full_schedule(
            num_schedules=2, to_randomize_first=None, to_randomize_second="reversed"
        )
    )
    simulated_first = two_schedules[:num_rounds]
    assert first_schedule == simulated_first
    flipped = [
        tuple((a, h) for h, a in reversed(match))
        for match in reversed(simulated_first)
    ]
    assert flipped == two_schedules[num_rounds : 2 * num_rounds]

    simulated_first = two_schedules[2 * num_rounds : 3 * num_rounds]
    assert first_schedule == simulated_first
    flipped = [
        tuple((a, h) for h, a in reversed(match))
        for match in reversed(simulated_first)
    ]
    assert flipped == two_schedules[3 * num_rounds :]