import tournament_simulations.schedules.algorithms.circle_method as cm


def test_create_team_list():

    assert cm._create_team_list(0) == []
    assert cm._create_team_list(1) == [-1, 0]
    assert cm._create_team_list(2) == [0, 1]
    assert cm._create_team_list(3) == [-1, 0, 1, 2]
    assert cm._create_team_list(4) == [0, 1, 2, 3]


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

    assert cm.CircleMethod.generate_schedule(2) == [((0, 1),)]

    assert cm.CircleMethod.generate_schedule(3) == [((0, 1),), ((2, 0),), ((1, 2),)]

    assert cm.CircleMethod.generate_schedule(4) == [
        ((0, 3), (1, 2)),
        ((0, 2), (3, 1)),
        ((0, 1), (2, 3)),
    ]
