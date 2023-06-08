import tournament_simulations.schedules.round_robin.circle_method as cm


def test_generate_round_matches():

    teams = [0, 1]
    assert cm._generate_round_matches(teams, len(teams) // 2) == ((0, 1),)

    teams = [0, 1, 2, 3]
    assert cm._generate_round_matches(teams, len(teams) // 2) == ((0, 3), (1, 2))

    teams = [-1, 0, 1, 2, 3, 4]
    assert cm._generate_round_matches(teams, len(teams) // 2) == (
        (-1, 4),
        (0, 3),
        (1, 2),
    )


def testgenerate_schedule():

    teams = [0, 1]

    assert cm.generate_schedule(teams) == [((0, 1),)]

    teams = [-1, 0, 1, 2]
    assert cm.generate_schedule(teams) == [((0, 1),), ((2, 0),), ((1, 2),)]

    teams = [0, 1, 2, 3]
    assert cm.generate_schedule(teams) == [
        ((0, 3), (1, 2)),
        ((0, 2), (3, 1)),
        ((0, 1), (2, 3)),
    ]
