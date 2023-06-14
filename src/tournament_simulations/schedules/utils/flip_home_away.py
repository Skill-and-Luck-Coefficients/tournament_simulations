from .scheduling_types import Round


def flip_home_away_in_schedule(schedule: list[Round]) -> list[Round]:

    """
    Turn all (home, away) matches into (away, home).
    """

    return [tuple((away, home) for home, away in matches) for matches in schedule]
