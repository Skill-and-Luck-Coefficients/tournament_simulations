from .scheduling_types import Round


def reverse_schedule(schedule: list[Round]) -> list[Round]:

    """
    Reverses:
        1: order of rounds
        2: order of matches in a round
        3: who plays as home/away.
    """

    return [
        tuple((away, home) for home, away in reversed(matches))
        for matches in reversed(schedule)
    ]
