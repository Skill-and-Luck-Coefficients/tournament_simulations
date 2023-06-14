import tournament_simulations.schedules.utils.rename_teams as rt


def test_empty_rename_teams_in_rounds_one():

    assert list(rt.rename_teams_in_rounds([], [])) == []
    assert list(rt.rename_teams_in_rounds([], ["a"])) == []
    assert list(rt.rename_teams_in_rounds([], {"a": "b"})) == []


def test_rename_teams_in_rounds_one():

    teams = ["one", "two", "three"]
    test = [((0, 1),), ((2, 1),), ((0, 2),)]

    expected = [(("one", "two"),), (("three", "two"),), (("one", "three"),)]
    assert list(rt.rename_teams_in_rounds(test, teams)) == expected

    teams = {"a": "one", "c": "two", "b": "three"}
    test = [(("a", "c"),), (("b", "c"),), (("a", "b"),)]

    expected = [(("one", "two"),), (("three", "two"),), (("one", "three"),)]
    assert list(rt.rename_teams_in_rounds(test, teams)) == expected


def test_rename_teams_in_rounds_two():

    teams = [
        (0,),
        "b",
        (2,),
        [4],
    ]
    test = [((0, 1), (2, 3)), ((0, 2), (3, 1)), ((3, 0), (1, 2))]

    expected = [
        (
            ((0,), "b"),
            (
                (2,),
                [4],
            ),
        ),
        (
            ((0,), (2,)),
            (
                [4],
                "b",
            ),
        ),
        (
            (
                [4],
                (0,),
            ),
            ("b", (2,)),
        ),
    ]

    assert list(rt.rename_teams_in_rounds(test, teams)) == expected
