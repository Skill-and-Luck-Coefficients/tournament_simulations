from collections.abc import Iterator
from dataclasses import dataclass

import pandas as pd

import tournament_simulations.schedules.permutation.create_permutation_schedule as cps


@dataclass
class RoundRobinMock:

    num_teams: int

    def get_full_schedule(self, n):
        return (self.num_teams for _ in range(n))


def test_get_schedule_creator_per_id():

    id_to_team_names = pd.Series(
        index=pd.Index(pd.Categorical(["1", "3", "2"]), name="id"),
        data=[["a", "b", "c"], ["A", "B"], [0, 1, 2, 3]],
    )

    expected = pd.Series(
        index=pd.Index(pd.Categorical(["1", "2", "3"]), name="id"), data=[3, 4, 2]
    )
    result = cps._get_schedule_creator_per_id(id_to_team_names)

    assert result.apply(lambda cell: isinstance(cell, cps.rr.DoubleRoundRobin)).all()
    assert result.apply(lambda cell: cell.num_teams).equals(expected)

    id_to_team_names = pd.Series(
        index=pd.Index(pd.Categorical(["1", "3", "2"]), name="id"),
        data=[["a", "b", "c"], ["A", "B"], [0, 1, 2, 3]],
    )

    expected = pd.Series(
        index=pd.Index(pd.Categorical(["1", "2", "3"]), name="id"), data=[3, 4, 2]
    )
    result = cps._get_schedule_creator_per_id(id_to_team_names)

    assert result.apply(lambda cell: isinstance(cell, cps.rr.DoubleRoundRobin)).all()
    assert result.apply(lambda cell: cell.num_teams).equals(expected)


def test_create_schedule_per_id():

    test = pd.Series(
        index=pd.Index(pd.Categorical(["1", "3", "2"]), name="id"),
        data=[
            (RoundRobinMock(1), 3),
            (RoundRobinMock(3), 1),
            (RoundRobinMock(2), 2),
        ],
    )

    expected = pd.Series(
        index=pd.Index(pd.Categorical(["1", "2", "3"]), name="id"),
        data=[[1] * 3, [2] * 2, [3] * 1],
        name="schedule",
    )

    result = cps._create_schedule_per_id(test)

    assert result.apply(lambda cell: isinstance(cell, Iterator)).all()
    assert result.apply(list).equals(expected)
