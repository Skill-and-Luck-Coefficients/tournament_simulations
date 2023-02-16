import schedules.round_robin.create_single_round_robin as csrr


def test_create_team_list():

    assert csrr._create_team_list(0) == []
    assert csrr._create_team_list(1) == [-1, 0]
    assert csrr._create_team_list(2) == [0, 1]
    assert csrr._create_team_list(3) == [-1, 0, 1, 2]
    assert csrr._create_team_list(4) == [0, 1, 2, 3]


def test_generate_round_matches():

    teams = [0, 1]
    assert csrr._generate_round_matches(teams, len(teams) // 2) == ((0, 1),)

    teams = [0, 1, 2, 3]
    assert csrr._generate_round_matches(teams, len(teams) // 2) == ((0, 3), (1, 2))

    teams = [-1, 0, 1, 2, 3, 4]
    assert csrr._generate_round_matches(teams, len(teams) // 2) == (
        (-1, 4),
        (0, 3),
        (1, 2),
    )


def test_generate_schedule():

    teams = [0, 1]

    assert csrr._generate_schedule(teams) == [((0, 1),)]

    teams = [-1, 0, 1, 2]
    assert csrr._generate_schedule(teams) == [((0, 1),), ((2, 0),), ((1, 2),)]

    teams = [0, 1, 2, 3]
    assert csrr._generate_schedule(teams) == [
        ((0, 3), (1, 2)),
        ((0, 2), (3, 1)),
        ((0, 1), (2, 3)),
    ]


def test_shuffle_home_away_in_matches():

    desired_matches = [(0, 1)]
    shuffled_desired = [(1, 0)]

    schedule = csrr._shuffle_home_away_in_matches([((0, 1),)])
    flattened_schedule = [match for round_ in schedule for match in round_]

    assert all(
        (match in desired_matches) ^ (match in shuffled_desired)
        for match in flattened_schedule
    )

    desired_matches = [(0, 1), (2, 0), (1, 2)]
    shuffled_desired = [(1, 0), (0, 2), (2, 1)]

    schedule = csrr._shuffle_home_away_in_matches([((0, 1),), ((2, 0),), ((1, 2),)])
    flattened_schedule = [match for round_ in schedule for match in round_]

    assert all(
        (match in desired_matches) ^ (match in shuffled_desired)
        for match in flattened_schedule
    )

    desired_matches = [(0, 3), (1, 2), (0, 2), (3, 1), (0, 1), (2, 3)]
    shuffled_desired = [(3, 0), (2, 1), (2, 0), (1, 3), (1, 0), (3, 2)]

    schedule = csrr._shuffle_home_away_in_matches(
        [
            ((0, 3), (1, 2)),
            ((0, 2), (3, 1)),
            ((0, 1), (2, 3)),
        ]
    )
    flattened_schedule = [match for round_ in schedule for match in round_]

    assert all(
        (match in desired_matches) ^ (match in shuffled_desired)
        for match in flattened_schedule
    )
