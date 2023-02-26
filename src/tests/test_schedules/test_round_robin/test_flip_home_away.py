import schedules.round_robin.utils.flip_home_away as fha


def test_flip_home_away_in_schedule_first():

    rounds = [((1, 2), (0, 3)), ((3, 1), (0, 2)), ((2, 3), (0, 1))]
    expected = [((2, 1), (3, 0)), ((1, 3), (2, 0)), ((3, 2), (1, 0))]

    assert fha.flip_home_away_in_schedule(rounds) == expected

    rounds = [((1, 2),), ((0, 1),), ((2, 0),)]
    expected = [((2, 1),), ((1, 0),), ((0, 2),)]

    assert fha.flip_home_away_in_schedule(rounds) == expected


def test_flip_home_away_in_schedule_second():

    schedule = [((0, 1),)]
    assert fha.flip_home_away_in_schedule(schedule) == [((1, 0),)]

    schedule = [((0, 1),), ((2, 0),), ((1, 2),)]
    assert fha.flip_home_away_in_schedule(schedule) == [
        ((1, 0),),
        ((0, 2),),
        ((2, 1),),
    ]

    schedule = [
        ((0, 3), (1, 2)),
        ((0, 2), (3, 1)),
        ((0, 1), (2, 3)),
    ]
    assert fha.flip_home_away_in_schedule(schedule) == [
        ((3, 0), (2, 1)),
        ((2, 0), (1, 3)),
        ((1, 0), (3, 2)),
    ]
