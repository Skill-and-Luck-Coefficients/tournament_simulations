from typing import Mapping

import numpy as np
import pandas as pd

import tournament_simulations.data_structures.matches as mat
from tournament_simulations.logs import log, tournament_simulations_logger

TeamPontuation = tuple[mat.Team, float]
TeamsMatchPoints = tuple[TeamPontuation, TeamPontuation]

KwargsPPM = dict[str, pd.DataFrame]


def _get_teams_points_per_match(
    home_away_winner: pd.Series,
    winner_to_points: Mapping[str, tuple[float, float]]
) -> pd.Series:

    # apply function
    def _get_team_point_pair_one_match(
        home_away_winner: mat.HomeAwayWinner,
    ) -> TeamsMatchPoints | float:

        *home_away, winner = home_away_winner
        points = winner_to_points.get(winner)

        if points is None:
            message = f"Invalid parameter: {home_away_winner}."
            tournament_simulations_logger.warning(message)
            return np.nan

        return tuple(zip(home_away, points))  # type: ignore

    return (
        home_away_winner.apply(_get_team_point_pair_one_match)
        .dropna()  # ignores matches which cannot be converted
        .explode()  # breaks ((home, points_home), (away, points_away)) into two lines
    )


@log(tournament_simulations_logger.debug)
def get_kwargs_from_home_away_winner(
    home_away_winner: pd.Series,
    winner_to_points: Mapping[str, tuple[float, float]]
) -> KwargsPPM:

    """
    Given a pd.Series with all matches, converts each match
    into two lines containing the teams (home and away) names
    and their points.

    Matches which cannot be converted will be ignored.

    --------
    Parameters:
        home_away_winner: pd.Series["desired_index", tuple[str, str, str]]
            Index -> home_away_winner index will be used for retuned df.
            Data -> (home, away, winner) tuples for all matches.

        winner_to_points: Mapping[str, tuple[float, float]]
            Default: {"h": (3, 0),"d": (1, 1),"a": (0, 3)}

            Maps winner to points gained (respectively) by home and away teams.

    ------
    Returns:
        Kwargs parameters for PointsPerMatch
            Points each team made in each match they played.

            Parameters:
                df -> pd.DataFrame
    """

    points_per_match = _get_teams_points_per_match(home_away_winner, winner_to_points)

    # each entry of points_per_match is a tuple like (team_name, points_gained)
    df_columns = ["team", "points"]
    df_index: pd.MultiIndex = points_per_match.index  # type: ignore
    df_data: list[TeamPontuation] = points_per_match.to_list()

    return {"df": pd.DataFrame(df_data, df_index, df_columns)}
