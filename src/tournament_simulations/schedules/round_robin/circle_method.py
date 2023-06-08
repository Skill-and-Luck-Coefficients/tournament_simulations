from tournament_simulations.logs import log, tournament_simulations_logger

from .utils.types import Round

KwargsSRR = dict[str, int | list[Round]]


def _generate_round_matches(teams: list[int], matches_per_round: int) -> Round:
    return tuple((teams[i], teams[-i - 1]) for i in range(matches_per_round))


@log(tournament_simulations_logger.debug)
def generate_schedule(teams: list[int]) -> list[Round]:

    """
    Generate a schedule following the circle-method algorithm.
    See: https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method

    ----
    Parameters:
        teams: list[int]
            List of team names (integers).

    ----
    Returns:
        list[ # List of rounds
            tuple[ # Rounds (list of matches)
                tuple[Team, Team], # Match
                ...
        ]
    """

    matches_per_round = len(teams) // 2

    teams_copy = teams.copy()
    rounds: list[Round] = []

    # see https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method
    while True:

        round_: Round = _generate_round_matches(teams_copy, matches_per_round)

        # remove matches with the sentinel value -1
        # only happen if the number of teams is odd
        valid_round: Round = tuple(match for match in round_ if -1 not in match)

        rounds.append(valid_round)

        teams_copy.insert(1, teams_copy.pop())

        if teams_copy == teams:
            break

    return rounds
