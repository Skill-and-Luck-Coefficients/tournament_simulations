import tournament_simulations.schedules.utils.reversed_schedule as rs


def test_reverse_schedule_first():

    rounds = [((1, 2), (0, 3)), ((3, 1), (0, 2)), ((2, 3), (0, 1))]
    expected = [((1, 0), (3, 2)), ((2, 0), (1, 3)), ((3, 0), (2, 1))]

    assert rs.reverse_schedule(rounds) == expected

    rounds = [((1, 2),), ((0, 1),), ((2, 0),)]
    expected = [((0, 2),), ((1, 0),), ((2, 1),)]

    assert rs.reverse_schedule(rounds) == expected


def test_reverse_schedule_second():

    schedule = [((0, 1),)]
    assert rs.reverse_schedule(schedule) == [((1, 0),)]

    schedule = [((0, 1),), ((2, 0),), ((1, 2),)]
    assert rs.reverse_schedule(schedule) == [
        ((2, 1),),
        ((0, 2),),
        ((1, 0),),
    ]

    schedule = [
        ((0, 3), (1, 2)),
        ((0, 2), (3, 1)),
        ((0, 1), (2, 3)),
    ]
    assert rs.reverse_schedule(schedule) == [
        ((3, 2), (1, 0)),
        ((1, 3), (2, 0)),
        ((2, 1), (3, 0)),
    ]
