import functools
from dataclasses import dataclass
from typing import Literal, NewType

import pandas as pd

from utils.convert_df_to_series import convert_df_to_series_of_tuples

Id = NewType("Id", str)
DateNumber = NewType("DateNumber", int)
MatchesDFIndex = tuple[Id, DateNumber]

Team = NewType("Team", str)
Winner = Literal["h", "d", "a"]

HomeAwayWinner = tuple[Team, Team, Winner]


@dataclass
class Matches:
    """
    Dataclass responsible to store tournament matches.

    df:
        pd.DataFrame[
            index=[
                "id" -> "{current_name}@/{sport}/{country}/{name-year}/",\n
                "date number" -> int (explained below),
            ],\n
            columns=[
                "home"                -> str (home team name),\n
                "away"                -> str (away team name),\n
                "result"              -> "{home score}:{away score}",\n
                "winner"              -> Literal["h", "d", "a"]
                    "h" -> home\n
                    "d" -> draw\n
                    "a" -> away
                "date"                -> "{day}.{month}.{year}",\n
                "odds home"           -> np.float16,\n
                "odds tie (optional)" -> np.float16,\n
                "odds away"           -> np.float16,\n
            ]
        ]

        Only "id", "date number", "home", "away" and "winner" are required.

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
        self.df = self.df.sort_index()

    @functools.cached_property
    def team_names_per_id(self) -> pd.Series:
        """
        Gets a list of team names for each tournament separately.
        """
        # apply func
        def _get_team_names_one_id(matches_one_id: pd.DataFrame) -> list[str]:

            teams_home: set[str] = set(matches_one_id.loc[:, "home"])
            teams_away: set[str] = set(matches_one_id.loc[:, "away"])

            return sorted(teams_home | teams_away)

        return (
            self.df.groupby("id", observed=True)
            .apply(_get_team_names_one_id)
            .rename("teams")
        )

    @functools.cached_property
    def number_of_matches_per_id(self) -> pd.Series:
        """
        Gets the number of matches for each tournament separately.
        """
        # apply func
        def _get_number_of_matches_one_id(matches_one_id: pd.DataFrame) -> int:

            return matches_one_id.shape[0]

        return (
            self.df.groupby("id", observed=True)
            .apply(_get_number_of_matches_one_id)
            .rename("num matches")
        )

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

            num_home_wins: int = (df_col == "h").sum()
            num_draws: int = (df_col == "d").sum()
            num_away_wins: int = (df_col == "a").sum()

            num_matches = len(df_col)

            return (
                num_home_wins / num_matches,  # probability home win
                num_draws / num_matches,  # probability draw
                num_away_wins / num_matches,  # probability away win
            )

        return (
            self.df.loc[:, "winner"]
            .groupby("id", observed=True)
            .apply(_create_probabilities_one_id)
            .rename("probabilities")
        )

    @functools.cached_property
    def home_away_winner(self) -> pd.Series:

        """
        Creates a series containing tuples (home, away, winner) for all matches.
        """

        desired_cols = self.df[["home", "away", "winner"]]

        return convert_df_to_series_of_tuples(desired_cols).rename("home away winner")

    @functools.cached_property
    def home_vs_away_count_per_id(self) -> pd.Series:

        """
        How many times (home, away) faced each other for all pairs
        of teams for a tournament.

        If there are no matches between two teams in a tournament,
        it will be omitted.
        """

        return self.df.groupby(["id", "home", "away"]).apply(len)
