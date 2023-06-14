from tournament_simulations.logs import log, tournament_simulations_logger

from ..utils.scheduling_types import Round


def _create_team_list(num_teams: int) -> list[int]:

    # need an additional team if it is an odd number
    if num_teams % 2 == 1:
        return list(range(-1, num_teams))

    return list(range(num_teams))


def _generate_round_matches(teams: list[int], matches_per_round: int) -> Round:
    return tuple((teams[i], teams[-i - 1]) for i in range(matches_per_round))


class CircleMethod:
    """
    Class responsible to generate schedules following the circle-method.
    Algorithm: https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method
    """

    @log(tournament_simulations_logger.debug)
    @staticmethod
    def generate_schedule(num_teams: int) -> list[Round]:
        """
        Generate a schedule following the circle-method algorithm.
        See: https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method

        ----
        Parameters:
            teams: int
                Number of teams.

        ----
        Returns:
            list[ # List of rounds
                tuple[ # Rounds (list of matches)
                    tuple[int, int], # Match
                    ...
            ]
                Teams are integers.
                You can think of it as the index in a list
                of team names.

                For example, team 0 would be associated with the
                the first position (index 0) in an array of team names.
        """

        teams = _create_team_list(num_teams)
        matches_per_round = len(teams) // 2

        teams_copy = teams.copy()
        rounds: list[Round] = []

        while True:

            round_: Round = _generate_round_matches(teams_copy, matches_per_round)

            # remove matches with the sentinel value -1
            # only happens if the number of teams is odd
            valid_round: Round = tuple(match for match in round_ if -1 not in match)

            rounds.append(valid_round)

            teams_copy.insert(1, teams_copy.pop())

            if teams_copy == teams:
                break

        return rounds
