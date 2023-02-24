import pandas as pd

from ..types import Round


def convert_list_of_rounds_to_dataframe(
    rounds: list[Round], tournament_id: str
) -> pd.DataFrame:

    """
    Converts a list of rounds into a dataframe.

    ----
    Parameters:

        rounds: list[
            tuple[  # Round: tuple of matches
                tuple[int, int]  # Match: each team is a number
            ]
        ]
            List of rounds.

        tournament_id: str
            Tournament name.

    ----
    Returns:

        pd.DataFrame[
            index=[
                "id": tournament_id\n
                "date number": which rounds the match belongs to
            ],
            columns=[
                "home": home team (integer)\n
                "away": away team (integer)
            ]
        ]
    """

    # don't need to set up the index, since exploded will already set all
    # matches to have the same index (which is our date number)
    exploded_rounds: pd.Series = pd.Series(rounds).explode()

    iterables = [[tournament_id], exploded_rounds.index]
    index = pd.MultiIndex.from_product(iterables, names=["id", "date number"])

    return pd.DataFrame(
        data=exploded_rounds.to_list(),
        index=index,
        columns=["home", "away"],
    )
