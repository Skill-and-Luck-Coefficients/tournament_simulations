from typing import Callable

import pandas as pd
import pytest

import tournament_simulations.simulations.utils.batch_simulations as bat


def test_create_column_names():

    assert bat._create_column_names(0, 0) == []
    assert bat._create_column_names(0, 1) == []
    assert bat._create_column_names(0, 2) == []
    assert bat._create_column_names(1, 0) == ["s0"]
    assert bat._create_column_names(1, 2) == ["s2"]
    assert bat._create_column_names(3, 4) == ["s12", "s13", "s14"]
    assert bat._create_column_names(6, 0) == ["s0", "s1", "s2", "s3", "s4", "s5"]
    assert bat._create_column_names(6, 3) == ["s18", "s19", "s20", "s21", "s22", "s23"]


@pytest.fixture
def simul_func():
    def simulation_func(num_simulations):
        dfs = [pd.DataFrame({"ok": [0, 1, 2]})] * num_simulations
        return pd.concat(dfs, ignore_index=True)

    return simulation_func


@pytest.fixture
def first_after_func():
    def after_func(df):
        return df + 2

    return after_func


@pytest.fixture
def second_after_func():
    def after_func(df):
        return df.set_axis(["col"] * len(df.columns), axis="columns")

    return after_func


def test_batch_simulate_tournaments_template_first(simul_func: Callable):

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iterations=1,
        num_simulations=1,
        func_after_simulation=lambda x: x,
    )
    data = [[0], [1], [2]]
    expected = pd.DataFrame(data=data, columns=["s0"])
    assert simulated.equals(expected)

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iterations=3,
        num_simulations=1,
        func_after_simulation=lambda x: x,
    )
    data = [[0] * 3, [1] * 3, [2] * 3]
    expected = pd.DataFrame(data=data, columns=["s0", "s1", "s2"])
    assert simulated.equals(expected)

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iterations=1,
        num_simulations=3,
        func_after_simulation=lambda x: x,
    )
    data = [[0], [1], [2]] * 3
    expected = pd.DataFrame(data=data, columns=["s0"])
    assert simulated.equals(expected)

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iterations=2,
        num_simulations=3,
        func_after_simulation=lambda x: x,
    )
    data = [[0] * 2, [1] * 2, [2] * 2] * 3
    expected = pd.DataFrame(data=data, columns=["s0", "s1"])
    assert simulated.equals(expected)


def test_batch_simulate_tournaments_template_second(
    simul_func: Callable, first_after_func: Callable
):

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iterations=1,
        num_simulations=1,
        func_after_simulation=first_after_func,
    )
    data = [[2], [3], [4]]
    expected = pd.DataFrame(data=data, columns=["s0"])
    assert simulated.equals(expected)

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iterations=2,
        num_simulations=3,
        func_after_simulation=first_after_func,
    )
    data = [[2] * 2, [3] * 2, [4] * 2] * 3
    expected = pd.DataFrame(data=data, columns=["s0", "s1"])
    assert simulated.equals(expected)


def test_batch_simulate_tournaments_template_third(
    simul_func: Callable, second_after_func: Callable
):

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iterations=4,
        num_simulations=1,
        func_after_simulation=second_after_func,
    )
    data = [[0] * 4, [1] * 4, [2] * 4]
    expected = pd.DataFrame(data=data, columns=["col"] * 4)
    assert simulated.equals(expected)

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iterations=2,
        num_simulations=3,
        func_after_simulation=second_after_func,
    )
    data = [[0] * 2, [1] * 2, [2] * 2] * 3
    expected = pd.DataFrame(data=data, columns=["col"] * 2)
    assert simulated.equals(expected)
