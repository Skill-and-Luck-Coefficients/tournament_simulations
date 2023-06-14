from typing import Iterator, Mapping, Sequence, TypeVar

from .scheduling_types import Round, Team

Name = TypeVar("Name")


def rename_teams_in_rounds(
    rounds: list[Round], teams: Mapping[Team, Name] | Sequence[Name]
) -> Iterator[tuple[tuple[Name, Name], ...]]:

    """
    Replace teams by the desired names.

    If a team in 'rounds' is called "team" then it will
    be replaced by teams["team"].

    ----
    Parameters:

        rounds: list[
            tuple[  # Round: tuple of matches
                tuple[Team, Team]  # Match
            ]
        ]
            List of rounds.

        teams: Mapping[Team, Name] | Sequence[Name]
            Names to replace integers by.

            If a team in round_ is called "team" then it will
            be replaced by teams["team"].

            If Team is int, then 'teams' can be a Sequence.

    ----
    Returns:

        Iterator[
            tuple[  # Round: tuple of matches
                tuple[Name, Name]  # Match: replaced names
            ]
        ]
    """

    return (
        tuple(
            (teams[int_team_one], teams[int_team_two])
            for int_team_one, int_team_two in round
        )
        for round in rounds
    )
