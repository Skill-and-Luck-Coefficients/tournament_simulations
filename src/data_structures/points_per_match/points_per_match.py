import functools
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class PointsPerMatch:

    """
    Points a team gained in each match they played in.

        df:
            pd.DataFrame[
                index=[
                    "id" -> "{current_name}@/{sport}/{country}/{name-year}/",\n
                    "date number" -> int (explained below),
                ],\n
                columns=[
                    "team"   -> str (team name),\n
                    "points" -> np.int16 (points team gained in date-number match),
                ]
            ]

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

    @property
    def team_names_per_id(self) -> pd.Series:
        """
        Gets a list of team names for each tournament separately.
        """
        # apply function
        def _get_team_names_one_id(ppm_df: pd.DataFrame) -> set[str]:

            if "team" in ppm_df.columns:
                return set(ppm_df.loc[:, "team"])

            return set(ppm_df.index.get_level_values("team"))

        return self.df.groupby("id", observed=True).apply(_get_team_names_one_id)

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

        return self.df.groupby("id", observed=True).apply(_get_number_of_matches_one_id)

    @functools.cached_property
    def probabilities_per_id(self) -> pd.Series:
        """
        Calculates probabilities of home-team win, draw and away-team win
        for each tournament separately.

        Each probability is a tuple of floats.

        This property is cached because otherwise it would be called
        each iteration.
        """
        # apply function
        def _create_probabilities_one_id(
            df_col: pd.Series,
        ) -> tuple[float, float, float]:

            # even rows are all home-teams' points while odds are all away-teams'
            only_points_home: np.ndarray = df_col.to_numpy()[::2]

            num_home_wins: int = only_points_home[only_points_home == 3].size
            num_draws: int = only_points_home[only_points_home == 1].size
            num_away_wins: int = only_points_home[only_points_home == 0].size

            num_matches = only_points_home.size

            return (
                num_home_wins / num_matches,  # probability home win
                num_draws / num_matches,  # probability draw
                num_away_wins / num_matches,  # probability away win
            )

        return (
            self.df.loc[:, "points"]
            .groupby("id", observed=True)
            .apply(_create_probabilities_one_id)
        )

    @functools.cached_property
    def rankings(self) -> pd.DataFrame:
        """
        Calculates tournament rankings.
        """
        return self.df.groupby(["id", "team"], observed=True).sum().sort_index()
