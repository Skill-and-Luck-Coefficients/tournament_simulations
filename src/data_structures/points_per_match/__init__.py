"""
    Provide a data structure to manage points each team made each match.

    -------
    Dataclass PointsPerMatch:

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
                hyperlink path to the site we scraped it from. Currently, this site
                is https://www.betexplorer.com/, but if it changes, so should each id.


            Date number is a conversion from "date" to integers. The first date with
            tournament matches has date number 0 (zero); the second date has date number
            1; so on and so forth.

                Example:
                    match_dates = [
                        "02.01.2014", "02.01.2014", "02.04.2014",
                        "02.04.2014", "02.01.2015"
                    ]
                    match_date_numbers = [0, 0, 1, 1, 2]

            All other information is pretty self-explanatory.
"""
from .create_points_per_match import create_points_per_match_from_home_away_winner
from .points_per_match import PointsPerMatch

__all__ = [
    "create_points_per_match_from_home_away_winner",
    "PointsPerMatch",
]
