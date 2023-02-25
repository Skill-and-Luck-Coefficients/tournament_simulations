import schedules.round_robin.create_double_round_robin as cdrr


def test_create_rounds_second_portion_first():

    rounds = [((1, 2), (0, 3)), ((3, 1), (0, 2)), ((2, 3), (0, 1))]
    expected = [((2, 1), (3, 0)), ((1, 3), (2, 0)), ((3, 2), (1, 0))]

    assert cdrr._create_rounds_second_portion(rounds) == expected

    rounds = [((1, 2),), ((0, 1),), ((2, 0),)]
    expected = [((2, 1),), ((1, 0),), ((0, 2),)]

    assert cdrr._create_rounds_second_portion(rounds) == expected


def test_create_rounds_second_portion_second():

    schedule = [((0, 1),)]
    assert cdrr._create_rounds_second_portion(schedule) == [((1, 0),)]

    schedule = [((0, 1),), ((2, 0),), ((1, 2),)]
    assert cdrr._create_rounds_second_portion(schedule) == [
        ((1, 0),),
        ((0, 2),),
        ((2, 1),),
    ]

    schedule = [
        ((0, 3), (1, 2)),
        ((0, 2), (3, 1)),
        ((0, 1), (2, 3)),
    ]
    assert cdrr._create_rounds_second_portion(schedule) == [
        ((3, 0), (2, 1)),
        ((2, 0), (1, 3)),
        ((1, 0), (3, 2)),
    ]
