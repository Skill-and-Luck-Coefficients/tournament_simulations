"""
    Provide a data structure to manage tournament matches.

    -------
    Dataclass Matches:

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

            Only "id", "date number", "home", "away", "winner" are required.

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


from .matches import DateNumber, HomeAwayWinner, Id, Matches, MatchesDFIndex, Team

__all__ = [
    "Matches",
    "HomeAwayWinner",
    "Id",
    "DateNumber",
    "MatchesDFIndex",
    "Team",
]
