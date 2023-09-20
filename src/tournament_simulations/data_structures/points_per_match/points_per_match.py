from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np
import pandas as pd

from .create_points_per_match import get_kwargs_from_home_away_winner

RESULT_TO_POINTS = {
    "h": (3, 0),
    "d": (1, 1),
    "a": (0, 3),
}


@dataclass
class PointsPerMatch:

    """
    Points a team gained in each match they played in.

        df:
            pd.DataFrame[
                index=[
                    "id" -> pd.Categorical[str]
                        "{current_name}@/{sport}/{country}/{name-year}/",
                    "date number" -> int (explained below),
                ],\n
                columns=[
                    "team"   -> pd.Categorical[str] (team name),\n
                    "points" -> np.int16 (points team gained in date-number match),
                ]
            ]

        Index is automatically sorted after initialization.

        Id is the tournament information: country, season, name and year.

            The reason there are two names (current_name and name) is because some
            tournaments have changed their names throughout the years.

            The second part, that is, /{sport}/{country}/{name-year}, is the
            hyperlink path to https://www.betexplorer.com/.


        Date number is a conversion from "date" to integers. The first date with
        tournament matches has date number 0 (zero); the second date has date number
        1; so on and so forth.

            Example:
                match_dates = [
                    "02.01.2014", "02.01.2014", "02.04.2014",
                    "02.04.2014", "02.01.2015"
                ]\n
                match_date_numbers = [0, 0, 1, 1, 2]
    """

    df: pd.DataFrame

    def __post_init__(self):

        index_cols = ["id", "date number"]

        # setting index_col as columns if they are in index
        # this is needed for data_type conversion
        index_to_reset = [name for name in index_cols if name in self.df.index.names]
        self.df = self.df.reset_index(index_to_reset)

        data_types: dict[str, type[int] | str] = {
            "id": "category",
            "date number": int,
            "team": "category",
            "points": np.int16,
        }

        self.df = self.df.astype(data_types).set_index(index_cols).sort_index()

    @classmethod
    def from_home_away_winner(
        cls,
        home_away_winner: pd.Series,
        result_to_points: Mapping[str, tuple[float, float]] = RESULT_TO_POINTS,
    ) -> PointsPerMatch:

        """
        Given a pd.Series with all matches, converts each match
        into two lines containing the teams (home and away) names
        and their points.

        Matches which cannot be converted will be ignored.

        --------
        Parameters:
            home_away_winner: pd.Series["desired_index", tuple[str, str, str]]
                Index -> home_away_winner index will be used for retuned df.
                (home, away, winner) tuples for all matches.

            result_to_points: Mapping[str, tuple[float, float]]
                Default: {"h": (3, 0),"d": (1, 1),"a": (0, 3)}

                Maps result to points gained (respectively) by home and away teams.

        ------
        Returns:
            PointsPerMatch
                Points each team made in each match they played.
        """
        kwargs = get_kwargs_from_home_away_winner(home_away_winner, result_to_points)
        return cls(**kwargs)

    @property
    def team_names_per_id(self) -> pd.Series:
        """
        Gets a list of team names for each tournament separately.
        """
        # apply function
        def _get_team_names_one_id(ppm_df: pd.DataFrame) -> list[str]:

            if "team" in ppm_df.columns:
                return sorted(ppm_df.loc[:, "team"].unique())

            return sorted(ppm_df.index.get_level_values("team").unique())

        return (
            self.df.groupby("id", observed=True)
            .apply(_get_team_names_one_id)
            .rename("teams")
        )

    @functools.cached_property
    def number_of_matches_per_id(self) -> pd.Series:
        """
        Gets the number of matches for each tournament separately.

        This property is cached because otherwise it would be called
        each iteration.
        """
        # apply function
        def _get_number_of_matches_one_id(ppm_df: pd.DataFrame) -> int:
            # each match is equivalent to 2 lines
            return ppm_df.shape[0] // 2

        return (
            self.df.groupby("id", observed=True)
            .apply(_get_number_of_matches_one_id)
            .rename("num matches")
        )

    @functools.cached_property
    def rankings(self) -> pd.DataFrame:
        """
        Calculates tournament rankings.
        """
        return self.df.groupby(["id", "team"], observed=True).sum().sort_index()

    def probabilities_per_id(
        self,
        point_pairs: Sequence[tuple[float, float]] = [(3, 0), (1, 1), (0, 3)]
    ) -> pd.Series:
        """
        Calculates probabilities of each result given team pontuations.

        ----
        Parameters:
            point_pairs: Sequence[tuple[float, float]] = [(3, 0), (1, 1), (0, 3)]
                List of points gained by home and away teams (respectively).

        Returns
        -----
            pd.Series[
                index = [
                    "id": str
                        tournament id
                ]

                value = [
                    "probabilities": Mapping[tuple[float, float], float]
                        tuple[float, float]: points gained -> (home team, away team)
                        float: probability
                ]
            ]
        """
        # apply function
        def _create_probabilities_one_id(
            df_col: pd.Series,
            desired_point_pairs: Sequence[tuple[float, float]],
        ) -> dict[tuple[float, float], float]:
            # even-numbered rows are home team's points; odds-numbered ones are away's
            points_home = df_col.to_numpy()[::2]
            points_away = df_col.to_numpy()[1::2]
            return {
                (home, away): np.mean((points_home == home) & (points_away == away))
                for home, away in desired_point_pairs
            }

        return (
            self.df["points"]
            .groupby("id", observed=True)
            .agg(_create_probabilities_one_id, desired_point_pairs=point_pairs)
            .rename("probabilities")
            .sort_index()
        )
