from typing import Any, Iterable, Iterator

from .types import Round


def rename_teams_in_rounds(
    rounds: list[Round], teams: Iterable[Any]
) -> Iterator[tuple[Any, Any]]:

    """
    Replace integers representing teams by the desired values.
    Team number "i" will be replaced by teams[i].

    ----
    Parameters:

        rounds: list[
            tuple[  # Round: tuple of matches
                tuple[int, int]  # Match: each team is a number
            ]
        ]
            List of rounds.

        teams: Iterable[Any]
            Names to replace integers by.
            Team number "i" will be replaced by teams[i].

    ----
    Returns:

        Iterator[
            tuple[  # Round: tuple of matches
                tuple[type[teams[i]], type[teams[i]]]  # Match: replaced names
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
