import tournament_simulations.schedules.round_robin.create_double_round_robin as cdrr


def test_get_kwargs_from_num_teams():

    def _scheduling_func(integer):
        return []

    for num_teams in range(15):
        kwargs = cdrr.get_kwargs_from_num_teams(num_teams, _scheduling_func)

        assert kwargs["num_teams"] == num_teams
        assert kwargs["team_names"] == list(range(num_teams))
        assert kwargs["first_schedule"] == []

    def _scheduling_func(integer):
        return list(range(integer))

    for num_teams in range(15):

        kwargs = cdrr.get_kwargs_from_num_teams(num_teams, _scheduling_func)

        assert kwargs["num_teams"] == num_teams
        assert kwargs["team_names"] == list(range(num_teams))
        assert kwargs["first_schedule"] == list(range(num_teams))


def test_get_kwargs_from_team_names():

    def _scheduling_func(integer):
        return []

    for team_names in [["a", "b", "c"], (0, 1, 2)]:
        kwargs = cdrr.get_kwargs_from_team_names(team_names, _scheduling_func)

        assert kwargs["num_teams"] == len(team_names)
        assert kwargs["team_names"] == list(team_names)
        assert kwargs["first_schedule"] == []

    def _scheduling_func(integer):
        return [((i, i), ) for i in range(integer)]

    for team_names in [["a", "b", "c"], [0, 1, 2]]:

        kwargs = cdrr.get_kwargs_from_team_names(team_names, _scheduling_func)

        assert kwargs["num_teams"] == len(team_names)
        assert kwargs["team_names"] == team_names
        assert kwargs["first_schedule"] == [((i, i), ) for i in team_names]
