import functools
from dataclasses import dataclass
from typing import Literal, NewType, Sequence

import pandas as pd

from tournament_simulations.utils.convert_df_to_series import (
    convert_df_to_series_of_tuples,
)

Id = NewType("Id", str)
DateNumber = NewType("DateNumber", int)
MatchesDFIndex = tuple[Id, DateNumber]

Team = NewType("Team", str)

HomeAwayWinner = tuple[Team, Team, str]


@dataclass
class Matches:
    """
    Dataclass responsible to store tournament matches.

        df:
            pd.DataFrame[
                index=[
                    "id" -> pd.Categorical[str]
                        "{current_name}@/{sport}/{country}/{name-year}/",,\n
                    "date number" -> int (explained below),
                ],\n
                columns=[
                    "home"                -> pd.Categorical[str] (home team name),\n
                    "away"                -> pd.Categorical[str] (away team name),\n
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

        index_cols = ["id", "date number"]

        # setting index_col as columns if they are in index
        # this is needed for data_type conversion
        index_to_reset = [name for name in index_cols if name in self.df.index.names]
        self.df = self.df.reset_index(index_to_reset)

        data_types: dict[str, type[int] | str] = {
            "id": "category",
            "date number": int,
            "home": "category",
            "away": "category",
        }

        self.df = self.df.astype(data_types).set_index(index_cols).sort_index()

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
    def home_vs_away_count_per_id(self) -> pd.Series:

        """
        How many times (home, away) faced each other for all pairs
        of teams for a tournament.

        If there are no matches between two teams in a tournament,
        it will be omitted.
        """

        return (
            self.df.groupby(["id", "home", "away"], observed=True)
            .apply(len)
            .sort_index()  # BUG: it is not sorting after groupby
            .rename("match count")
        )

    def probabilities_per_id(
        self,
        column: str = "winner",
        results: Sequence[str] | None = ("h", "d", "a")
    ) -> pd.Series:
        """
        Calculates probabilities of each result for a given column.

        ----
        Parameters:
            column: str
                Desired column

            results: Sequence[str] | None = ("h", "d", "a")
                Results to be considered.

                If it is None, it will be set to all unique values for the column.

        Returns
        -----
            pd.Series[
                index = [
                    "id": str
                        tournament id
                ]

                value = [
                    "probabilities": pd.Series[str, float]
                        str (result): float (probability)
                ]
            ]
        """
        # apply function
        def _create_probabilities_one_id(
            df_col: pd.Series, results: Sequence[str]
        ) -> dict[str, float]:
            return {
                result: (df_col == result).sum() / len(df_col)
                for result in results
            }

        if results is None:
            results = self.df[column].unique().tolist()

        return (
            self.df[column]
            .groupby("id", observed=True)
            .agg(_create_probabilities_one_id, results=results)
            .rename("probabilities")
            .sort_index()
        )

    def home_away_winner(
        self, winner_type: Literal["winner", "result"] = "winner"
    ) -> pd.Series:
        """
        Creates a series containing tuples (home, away, winner) for all matches.

        ---
        Parameters:
            winner_type: Literal["winner", "result"] = "winner"
                winner: Which team won, that is, "h", "d" or "a"
                result: Match result, that is, "{home score}-{away score}"
        """
        desired_cols = self.df[["home", "away", winner_type]]
        return convert_df_to_series_of_tuples(desired_cols).rename("home away winner")
