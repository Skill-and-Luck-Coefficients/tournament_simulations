"""

    Module responsible for simulating tournament results.

    This module is specifically designed to simulate results according to
    the probabilities of home-team win, draw and away-team win.

    Simulations can be done in two ways:

        Tournament-wide: The entire tournament will have the same probability.
        Match-wide: Each match will have its is own probability.

    Output can follow the following types:

        Winner -> simulates winners:

            "h" -> home team win
            "d" -> draw
            "a" -> away team win

            In this case, the default result follows the structure of
            data_structure.matches.Matches.

        Points per Match -> simulates points teams gained for each match:

            3 -> points for win
            1 -> points for draw
            0 -> points for loss

            Default result follows the structure of
                data_structure.points_per_match.PointsPerMatch.
"""

from . import match_wide, tournament_wide

__all__ = ["match_wide", "tournament_wide"]
