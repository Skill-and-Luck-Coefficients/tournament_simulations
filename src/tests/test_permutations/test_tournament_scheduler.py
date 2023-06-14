import pandas as pd

import tournament_simulations.permutations.tournament_scheduler as ts


def test_from_functions_simple():

    id_to_num_teams = pd.Series(
        index=["1", "0"],
        data=[[2], [3]],
    )

    def func_schedule(number):
        return [(i, i + 1) for i in range(number)]

    expected = pd.Series(
        index=["0", "1"],
        data=[
            [(0, 1), (1, 2), (2, 3)],
            [(0, 1), (1, 2)],
        ],
        name="schedule"
    )

    scheduler = ts.TournamentScheduler(func_schedule, id_to_num_teams)
    assert scheduler.generate_schedule().series.equals(expected)

    id_to_team_names = pd.Series(
        index=["1", "0"],
        data=[[["a", "b", "c"], [0]], [["A", "C", "B"], [0]]],
    )

    def func_schedule(team_names, other):
        return list(reversed(team_names)) + other

    expected = pd.Series(
        index=["0", "1"],
        data=[
            ["B", "C", "A", 0],
            ["c", "b", "a", 0],
        ],
        name="schedule"
    )

    scheduler = ts.TournamentScheduler(func_schedule, id_to_team_names)
    assert scheduler.generate_schedule().series.equals(expected)


def test_from_num_teams_complex():

    id_to_num_teams = pd.Series(
        index=["1", "0", "2"],
        data=[[2], [3], [4]],
    )

    id_to_func_schedule = pd.Series(
        index=["2", "1", "0"],
        data=[
            lambda number: (number, number - 1),
            lambda number: [(number, number), (number + 1, number + 1)],
            lambda number: number,
        ]
    )

    expected = pd.Series(
        index=["0", "1", "2"],
        data=[
            3,
            [(2, 2), (3, 3)],
            (4, 3),
        ],
        name="schedule"
    )

    scheduler = ts.TournamentScheduler(id_to_func_schedule, id_to_num_teams)
    assert scheduler.generate_schedule().series.equals(expected)

    id_to_team_names = pd.Series(
        index=["1", "0", "2"],
        data=[[["a", "b"]], [["C", "D"]], [["2", "1", "0"]]],
    )

    id_to_func_schedule = pd.Series(
        index=["2", "1", "0"],
        data=[
            sorted,
            lambda _: [],
            lambda list_: list_,
        ]
    )

    expected = pd.Series(
        index=["0", "1", "2"],
        data=[
            ["C", "D"],
            [],
            ["0", "1", "2"],
        ],
        name="schedule"
    )

    scheduler = ts.TournamentScheduler(id_to_func_schedule, id_to_team_names)
    assert scheduler.generate_schedule().series.equals(expected)
