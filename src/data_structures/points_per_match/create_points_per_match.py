import logging

import numpy as np
import pandas as pd

import data_structures.matches as mat
from logs import log

from .points_per_match import PointsPerMatch

TeamPontuation = tuple[mat.Team, int]
TeamsMatchPoints = tuple[TeamPontuation, TeamPontuation]


def _get_teams_points_per_match(home_away_winner: pd.Series) -> pd.Series:

    # apply function
    def _get_team_point_pair_one_match(
        home_away_winner: tuple[mat.Team, mat.Team, mat.Winner]
    ) -> TeamsMatchPoints | float:

        home, away, winner = home_away_winner

        if winner == "h":
            return ((home, 3), (away, 0))

        elif winner == "a":
            return ((home, 0), (away, 3))

        elif winner == "d":
            return ((home, 1), (away, 1))

        else:
            logging.warning(f"Invalid parameter: {home_away_winner}.")
            return np.nan

    return (
        home_away_winner.apply(_get_team_point_pair_one_match)
        .dropna()  # ignores matches which cannot be converted
        .explode()  # breaks ((home, points_home), (away, points_away)) into two lines
    )


@log(logging.debug)
def create_points_per_match_from_home_away_winner(
    home_away_winner: pd.Series,
) -> PointsPerMatch:

    """
    Given a pd.Series with all matches, converts each match
    into two lines containing the teams (home and away) names
    and their points.

    Matches which cannot be converted will be ignored.

    --------
    Parameters:
        home_away_winner: pd.Series["match", tuple[str, str, str]]
            (home, away, winner) tuples for all matches.

    ------
    Returns:
        PointsPerMatch
            Points each team made in each match they played.
    """

    points_per_match = _get_teams_points_per_match(home_away_winner)

    # each entry of points_per_match is a tuple like (team_name, points_gained)
    df_columns = ["team", "points"]
    df_index: pd.MultiIndex = points_per_match.index
    df_data: list[TeamPontuation] = points_per_match.to_list()

    ppm_df = pd.DataFrame(df_data, df_index, df_columns)
    return PointsPerMatch(ppm_df.astype({"team": "category", "points": np.int16}))
